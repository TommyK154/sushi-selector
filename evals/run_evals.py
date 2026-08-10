# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "anthropic>=0.40",
#   "rapidfuzz>=3.9",
# ]
# ///
"""Sushi Selector eval harness.

Extraction reliability is the product, and this harness is the working
definition of "reliable" (see docs/EVALS.md). It loads the exact production
assets under shared/, runs the per-photo index/details/reconcile pipeline plus
the merge and dedupe step, scores predictions against hand-verified goldens,
and writes a markdown report with a pass/fail gates table, per-menu breakdown,
per-item diffs, token usage, and estimated cost.

Run with uv (never pip or python directly):

    uv run evals/run_evals.py --check              # offline readiness check, no API calls
    uv run evals/run_evals.py --all                # full run over the golden set
    uv run evals/run_evals.py --menu <slug>        # single menu, for debugging
    uv run evals/run_evals.py --all --repeat 3     # consistency runs
    uv run evals/run_evals.py --all --batch        # route via Message Batches API (50% cheaper)
    uv run evals/run_evals.py --url-smoke          # loose URL-path smoke checks (reported, not gated)

STATUS: Phase 1 request layer wired. The deterministic layer (asset loading,
menu discovery, matching, metrics, gates, reporting) and the extraction
pipeline (index/details/reconcile/merge, --batch, --url-smoke) are both
implemented. Nothing runs without an explicit --menu/--all/--batch/--url-smoke
invocation and a real ANTHROPIC_API_KEY in the environment; --check stays
fully offline regardless.
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import anthropic
from rapidfuzz.fuzz import token_sort_ratio

# --------------------------------------------------------------------------
# Paths and constants
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SHARED = REPO_ROOT / "shared"
PROMPTS_DIR = SHARED / "prompts"
SCHEMA_DIR = SHARED / "schema"
ALIASES_PATH = SHARED / "aliases.json"
MENUS_DIR = REPO_ROOT / "evals" / "menus"
REPORTS_DIR = REPO_ROOT / "evals" / "reports"
CRASH_DIR = REPO_ROOT / "evals" / "crash"
USAGE_DIR = REPO_ROOT / "evals" / "usage"

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

# Name-match threshold, shared with the client dedupe rule (SPEC.md).
NAME_MATCH_THRESHOLD = 85

# Anthropic request-shape constants, mirroring src/extract.ts exactly so
# evals exercise the same request shapes production sends.
#
# P1-SB2: both raised from 2048 to 8192. INDEX_MAX_TOKENS raised because two
# --all crashes (P1-SC) truncated an index-pass response at roughly 66% of
# masa-sushi's full index payload; masa needs roughly 7100 chars per photo,
# and 2048 tokens was cutting it close on the largest golden. DETAILS_MAX_TOKENS
# raised because the one-shot details_retry call below is unbounded (every
# still-missing item of a photo in one call, not batched at DETAILS_BATCH_SIZE
# like the first pass): worst case for masa is roughly 12000 chars, well over
# half the old cap. A normal 8-item details batch measures roughly 1911 chars
# and is unaffected either way; raising the ceiling costs nothing unless the
# model actually generates more.
INDEX_MAX_TOKENS = 8192
DETAILS_MAX_TOKENS = 8192
URL_MAX_TOKENS = 8192
DETAILS_BATCH_SIZE = 8  # SPEC.md: batch 1 fires solo to warm the cache, then
                         # the rest fan out (sequential here; see _run_photo_pipeline).

# Basic web fetch, not a dynamic-filtering _202602xx variant: those are
# verified (live docs, this session) to support Fable 5, Opus 4.8, Mythos
# 5/Preview, Opus 4.7, Opus 4.6, Sonnet 5, and Sonnet 4.6 only. Haiku 4.5,
# the default model here, is not on that list. GA, no beta header required.
WEB_FETCH_TOOL_TYPE = "web_fetch_20250910"
WEB_FETCH_MAX_USES = 3
WEB_FETCH_MAX_CONTENT_TOKENS = 100_000

# Gate thresholds (docs/EVALS.md). Kept here so the report can print the exact
# number each gate was measured against.
GATES = {
    "item_recall": 0.97,
    "item_precision": 0.97,
    "ingredient_f1_macro": 0.90,
    "price_accuracy": 0.97,
    "consistency_f1_spread_max": 0.03,
}

# Rough per-token pricing for the default model, used only for the report's
# cost estimate. Verify against live pricing before trusting the number; the
# workspace spend cap is the real guardrail.
PRICE_PER_MTOK = {
    "input": 1.00,
    "cache_write": 1.25,
    "cache_read": 0.10,
    "output": 5.00,
}


# --------------------------------------------------------------------------
# Shared asset loading (evals exercise the exact production assets)
# --------------------------------------------------------------------------


@dataclass
class SharedAssets:
    system_prompt: str
    index_task: str
    details_task: str
    url_task: Optional[str]
    index_schema: dict
    details_schema: dict
    url_schema: Optional[dict]
    aliases: dict[str, str]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_shared_assets() -> SharedAssets:
    """Load prompts, schemas, and the alias table straight from shared/.

    Missing files raise with an actionable message. The URL task and alias
    table are optional in the Phase 0 skeleton; everything else is required
    before a scored run is meaningful.
    """
    missing: list[str] = []

    def required(path: Path) -> str:
        if not path.exists():
            missing.append(str(path.relative_to(REPO_ROOT)))
            return ""
        return _read_text(path)

    system_prompt = required(PROMPTS_DIR / "system.md")
    index_task = required(PROMPTS_DIR / "index-task.md")
    details_task = required(PROMPTS_DIR / "details-task.md")

    url_task_path = PROMPTS_DIR / "url-task.md"
    url_task = _read_text(url_task_path) if url_task_path.exists() else None

    index_schema: dict = {}
    details_schema: dict = {}
    index_schema_path = SCHEMA_DIR / "index.schema.json"
    details_schema_path = SCHEMA_DIR / "details.schema.json"
    if index_schema_path.exists():
        index_schema = json.loads(_read_text(index_schema_path))
    else:
        missing.append(str(index_schema_path.relative_to(REPO_ROOT)))
    if details_schema_path.exists():
        details_schema = json.loads(_read_text(details_schema_path))
    else:
        missing.append(str(details_schema_path.relative_to(REPO_ROOT)))

    url_schema_path = SCHEMA_DIR / "url.schema.json"
    url_schema: Optional[dict] = (
        json.loads(_read_text(url_schema_path)) if url_schema_path.exists() else None
    )

    aliases: dict[str, str] = {}
    if ALIASES_PATH.exists():
        aliases = json.loads(_read_text(ALIASES_PATH))

    if missing:
        raise FileNotFoundError(
            "Missing shared assets (built in Phase 1): " + ", ".join(missing)
        )

    return SharedAssets(
        system_prompt=system_prompt,
        index_task=index_task,
        details_task=details_task,
        url_task=url_task,
        index_schema=index_schema,
        details_schema=details_schema,
        url_schema=url_schema,
        aliases=aliases,
    )


# --------------------------------------------------------------------------
# Menu discovery
# --------------------------------------------------------------------------


@dataclass
class Menu:
    slug: str
    photos: list[Path]
    golden: dict


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def _photo_sort_key(p: Path) -> tuple:
    """Natural sort on the numeric stem, so 10 follows 2, never 1 (T3-2).

    Documented fallback: a non-numeric stem sorts after every numeric stem,
    then case-insensitively among itself. Front-page-first (SPEC.md's merge
    order) holds because 1 < 2 < 10 numerically. Scoped to filenames within
    one directory; see _raw_photo_sort_key for the recursive raw/ walk,
    where the stem alone is not enough to stay deterministic.
    """
    stem = p.stem
    if stem.isdigit():
        return (0, int(stem), "")
    return (1, 0, stem.lower())


def _raw_photo_sort_key(p: Path) -> tuple:
    """Deterministic ordering for the recursive raw/ walk (T3-1).

    _photo_sort_key alone is not enough here: raw/a/1.jpg and raw/b/1.jpg
    both key to (0, 1, ""), so two files in different subdirectories would
    fall back to filesystem insertion order. Keying on the parent path
    first, then _photo_sort_key, makes the walk fully deterministic across
    directories. The single-directory photos/ discovery below is unaffected
    by this and keeps the plain _photo_sort_key.
    """
    return (str(p.parent), *_photo_sort_key(p))


def discover_menus() -> list[Menu]:
    """Find scored menus: evals/menus/<slug>/ with photos/ and golden.json.

    The raw/ drop folder is skipped; it holds unsorted photos before they are
    slugified into per-menu directories (T-1.10).
    """
    menus: list[Menu] = []
    if not MENUS_DIR.exists():
        return menus
    for entry in sorted(MENUS_DIR.iterdir()):
        if not entry.is_dir() or entry.name == "raw":
            continue
        golden_path = entry / "golden.json"
        photos_dir = entry / "photos"
        if not golden_path.exists():
            continue
        photos = (
            sorted(
                (p for p in photos_dir.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES),
                key=_photo_sort_key,
            )
            if photos_dir.exists()
            else []
        )
        golden = json.loads(_read_text(golden_path))
        menus.append(Menu(slug=entry.name, photos=photos, golden=golden))
    return menus


# --------------------------------------------------------------------------
# Golden lint (offline, --check only, P1-SB)
#
# Bounds mechanical errors in golden.json files: dropped n, a price that
# disagrees with its price_text, an ingredient string nobody taught the
# alias table, a confidence token leaking out of notes. Goldens are
# human-owned; a lint finding is reported, never auto-fixed here. Two
# asserts (G, F) carry amendments made in plan mode, recorded in
# docs/BUILDLOG.md alongside the original card wording.
# --------------------------------------------------------------------------

VOCABULARY_PATH = REPO_ROOT / "evals" / "accepted_vocabulary.json"

CONFIDENCE_TOKEN_RE = re.compile(r"(?i)\b(?:INFERRED|LOW|MED|HIGH)\b")

# Romaji terms actually printed across the golden set (masa-sushi's
# structured "romaji: X" notes and KUU nigiri's bare prose), used by
# assert F. Deliberately excludes gunkan, nigiri, maki, temaki, sashimi:
# those are preparation or format words, not species/ingredient names, and
# an item can carry one without ever giving the fish's romaji name, so
# including them would mask the exact omission this assert exists to find.
ROMAJI_LEXICON = frozenset(
    {
        "toro", "maguro", "hon maguro", "hiro maguro",
        "uni", "amaebi", "kanpachi", "hirame", "aji", "ono",
        "sake", "sake gunsai", "hamachi", "unagi", "saba", "tako",
        "kaibashira", "ikura", "masago", "hokigai", "ika", "ebi",
        "tamago", "inari", "uzura",
    }
)


@dataclass
class LintFinding:
    assert_id: str  # "A".."G"
    severity: str  # "ERROR" | "WARN" | "SKIP"
    slug: str
    n: Optional[int]  # item n, or None for a menu-level finding
    message: str


@dataclass
class LintContext:
    aliases: dict[str, str]
    vocabulary_normalized: frozenset[str]
    composed_schema: dict
    menus_dir: Path


def load_accepted_vocabulary() -> list[str]:
    """Raw, unnormalized ingredient strings (design amendment: the file
    stays reviewable; normalization happens at assert E's lookup time, not
    here). Returns [] if the file does not exist yet.
    """
    if not VOCABULARY_PATH.exists():
        return []
    data = json.loads(_read_text(VOCABULARY_PATH))
    return data.get("ingredients", [])


def _composed_item_schema() -> dict:
    """The merged golden item schema: index.schema.json's item properties
    union details.schema.json's, which _schema_composition_self_test proves
    (at every --check run, using the real schema files, not a hardcoded
    claim) is exactly url.schema.json's item subschema. is_raw allows null
    per the assert G amendment: the locked README convention and the
    schemas already in shared/schema/ both treat null as "not determinable",
    not an error.
    """
    return {
        "required": [
            "n", "name", "section", "price_text", "price",
            "ingredients", "wrap", "is_raw",
        ],
        "properties": {
            "n": {"type": "integer"},
            "name": {"type": "string"},
            "section": {"type": ["string", "null"]},
            "price_text": {"type": ["string", "null"]},
            "price": {"type": ["number", "null"]},
            "ingredients": {"type": "array"},
            "wrap": {"enum": ["nori", "soy_paper", "rice_paper", "none", "unknown"]},
            "is_raw": {"type": ["boolean", "null"]},
            "notes": {"type": ["string", "null"]},
        },
    }


def _schema_composition_self_test(assets: "SharedAssets") -> None:
    """Proves the schema-ownership claim rather than asserting it: that
    index.schema.json's item properties, unioned with details.schema.json's,
    equal url.schema.json's item subschema exactly (required set, per-
    property type/enum constraints, property set). Runs against the real
    files loaded this run, not a hardcoded copy.
    """

    def _strip_desc(d: dict) -> dict:
        return {k: v for k, v in d.items() if k != "description"}

    idx_item = assets.index_schema["properties"]["items"]["items"]
    det_item = assets.details_schema["properties"]["items"]["items"]
    url_item = assets.url_schema["properties"]["items"]["items"]

    composed_props = {**idx_item["properties"], **det_item["properties"]}
    composed_req = set(idx_item["required"]) | set(det_item["required"])

    assert set(composed_props) == set(url_item["properties"]), (
        set(composed_props), set(url_item["properties"])
    )
    for key, spec in composed_props.items():
        assert _strip_desc(spec) == _strip_desc(url_item["properties"][key]), key
    assert composed_req == set(url_item["required"]), (composed_req, set(url_item["required"]))


def _matches_any_type(val: Any, types: list[str]) -> bool:
    for t in types:
        if t == "string" and isinstance(val, str):
            return True
        if t == "integer" and isinstance(val, int) and not isinstance(val, bool):
            return True
        if t == "number" and isinstance(val, (int, float)) and not isinstance(val, bool):
            return True
        if t == "boolean" and isinstance(val, bool):
            return True
        if t == "array" and isinstance(val, list):
            return True
        if t == "object" and isinstance(val, dict):
            return True
        if t == "null" and val is None:
            return True
    return False


def _validate_item(item: dict, schema: dict) -> list[str]:
    """Hand-written validator over the composed item schema: type, enum,
    required, additionalProperties. No jsonschema dependency (out of scope
    per the card: no new third-party packages).
    """
    problems: list[str] = []
    props = schema["properties"]
    missing = [k for k in schema["required"] if k not in item]
    if missing:
        problems.append(f"missing required field(s): {sorted(missing)}")
    extra = [k for k in item if k not in props]
    if extra:
        problems.append(f"unexpected field(s): {sorted(extra)}")
    for key, val in item.items():
        if key not in props:
            continue
        spec = props[key]
        if "type" in spec:
            types = spec["type"] if isinstance(spec["type"], list) else [spec["type"]]
            if not _matches_any_type(val, types):
                problems.append(f"{key}: expected type {types}, got {type(val).__name__} ({val!r})")
        if "enum" in spec and val not in spec["enum"]:
            problems.append(f"{key}: {val!r} not in enum {spec['enum']}")
        if key == "ingredients" and isinstance(val, list):
            bad = [x for x in val if not isinstance(x, str)]
            if bad:
                problems.append(f"ingredients: non-string entries {bad!r}")
    return problems


def _assert_a_confidence_tokens(golden: dict, slug: str, ctx: LintContext) -> list[LintFinding]:
    """ERROR. No confidence or inference token (INFERRED, LOW, MED, HIGH,
    case variants) in name, section, price_text, wrap, or any ingredients
    entry. notes is exempt (docs/EVALS.md: it legitimately carries them).
    """
    findings: list[LintFinding] = []
    for it in golden.get("items", []):
        n = it.get("n")
        for field in ("name", "section", "price_text", "wrap"):
            v = it.get(field)
            if isinstance(v, str) and CONFIDENCE_TOKEN_RE.search(v):
                findings.append(LintFinding("A", "ERROR", slug, n, f"{field}={v!r} carries a confidence token"))
        for ing in it.get("ingredients", []) or []:
            if isinstance(ing, str) and CONFIDENCE_TOKEN_RE.search(ing):
                findings.append(LintFinding("A", "ERROR", slug, n, f"ingredient {ing!r} carries a confidence token"))
    return findings


def _assert_b_n_contiguity(golden: dict, slug: str, ctx: LintContext) -> list[LintFinding]:
    """ERROR. n values contiguous from 1, no gaps, no duplicates."""
    items = golden.get("items", [])
    ns = [it.get("n") for it in items]
    expected = set(range(1, len(items) + 1))
    actual = set(ns)
    missing = sorted(expected - actual)
    dupes = sorted({x for x in ns if ns.count(x) > 1})
    findings: list[LintFinding] = []
    if missing:
        findings.append(LintFinding("B", "ERROR", slug, None, f"n gap(s), missing {missing}"))
    if dupes:
        findings.append(LintFinding("B", "ERROR", slug, None, f"n duplicate(s): {dupes}"))
    return findings


def _assert_c_section_manifest(golden: dict, slug: str, ctx: LintContext) -> list[LintFinding]:
    """ERROR when a sections.json sidecar exists: per-section item counts
    and the section name set/order match the manifest exactly. SKIP when
    the sidecar is absent, reported per menu. Section names and counts in
    the sidecar are hand written from the printed page; this assert reads
    the sidecar and the golden, and never derives one from the other.
    """
    sidecar = ctx.menus_dir / slug / "sections.json"
    if not sidecar.exists():
        try:
            rel = sidecar.relative_to(REPO_ROOT)
        except ValueError:
            rel = sidecar  # fixture path outside the repo (self-test), print in full
        return [LintFinding("C", "SKIP", slug, None, f"no sidecar at {rel}, assert C skipped")]
    try:
        manifest = json.loads(sidecar.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return [LintFinding("C", "ERROR", slug, None, f"sections.json unreadable: {e}")]

    findings: list[LintFinding] = []
    manifest_sections = manifest.get("sections", [])
    manifest_names = [s.get("section") for s in manifest_sections]
    manifest_counts = {s.get("section"): s.get("expected_count") for s in manifest_sections}

    golden_names: list[str] = []
    golden_counts: dict[str, int] = {}
    for it in golden.get("items", []):
        s = it.get("section")
        if s not in golden_names:
            golden_names.append(s)
        golden_counts[s] = golden_counts.get(s, 0) + 1

    if manifest_names != golden_names:
        findings.append(
            LintFinding(
                "C", "ERROR", slug, None,
                f"section name set/order mismatch: manifest={manifest_names} golden={golden_names}",
            )
        )
    for name in set(manifest_names) | set(golden_names):
        mc = manifest_counts.get(name)
        gc = golden_counts.get(name, 0)
        if mc != gc:
            findings.append(
                LintFinding("C", "ERROR", slug, None, f"section '{name}' count mismatch: manifest={mc} golden={gc}")
            )
    return findings


def _parse_single_price(price_text: Optional[str]) -> Optional[float]:
    """Parse price_text to a float only when exactly one number is present.
    Combo and market-price text ('2 for 23.00', 'MP', '8/15') is not a
    mismatch, it is unparseable, and this returns None so callers skip it.
    """
    if not isinstance(price_text, str):
        return None
    matches = re.findall(r"\d+(?:\.\d+)?", price_text)
    if len(matches) != 1:
        return None
    return float(matches[0])


def _assert_d_price_invariants(golden: dict, slug: str, ctx: LintContext) -> list[LintFinding]:
    """ERROR on price invariants: price_text present on every item; when
    price is non-null it equals the value parsed from price_text; no
    negative prices; no zero prices.

    WARN (amendment 4): a null price whose price_text has exactly one
    parseable number. The combo-pricing convention keeps price null with a
    verbatim price_text at section level, so a hard ERROR here would fail
    correct, human-owned goldens; this WARNs instead, listed by n.

    WARN (amendment 5): the I-4 carry-down signature, identical price on
    adjacent n within a section, collapsed into runs and reported as runs,
    not one line per pair. Runs of length 2 (the suspicious signature) are
    emitted first; runs of length 3+ (almost certainly a real price tier)
    are emitted after, informational.

    SKIP: the adjacent-column signature (a price matching the item one row
    up in the adjacent column) can never fire against these goldens, which
    carry no column data; every item's keys are exactly n, name, section,
    price_text, price, ingredients, wrap, is_raw, notes. Implemented as an
    explicit SKIP with reason rather than silently absent.
    """
    items = golden.get("items", [])
    findings: list[LintFinding] = []

    for it in items:
        n = it.get("n")
        price_text = it.get("price_text")
        price = it.get("price")
        if not isinstance(price_text, str) or not price_text.strip():
            findings.append(LintFinding("D", "ERROR", slug, n, "price_text missing or empty"))
            continue
        if isinstance(price, (int, float)) and not isinstance(price, bool):
            if price < 0:
                findings.append(LintFinding("D", "ERROR", slug, n, f"negative price {price}"))
            if price == 0:
                findings.append(LintFinding("D", "ERROR", slug, n, f"zero price {price}"))
            parsed = _parse_single_price(price_text)
            if parsed is not None and abs(parsed - price) > 1e-6:
                findings.append(
                    LintFinding(
                        "D", "ERROR", slug, n,
                        f"price {price} disagrees with price_text {price_text!r} (parsed {parsed})",
                    )
                )
        elif price is None:
            parsed = _parse_single_price(price_text)
            if parsed is not None:
                findings.append(
                    LintFinding(
                        "D", "WARN", slug, n,
                        f"price is null but price_text {price_text!r} parses to a single number {parsed}",
                    )
                )

    pair_runs: list[tuple] = []
    long_runs: list[tuple] = []
    i = 0
    while i < len(items):
        j = i
        while (
            j + 1 < len(items)
            and items[j + 1].get("section") == items[i].get("section")
            and items[j + 1].get("price") == items[i].get("price")
            and items[i].get("price") is not None
        ):
            j += 1
        run_len = j - i + 1
        if run_len >= 2:
            entry = (items[i].get("section"), items[i].get("n"), items[j].get("n"), items[i].get("price"), run_len)
            (pair_runs if run_len == 2 else long_runs).append(entry)
        i = j + 1

    for section, n_start, n_end, price, _ in pair_runs:
        findings.append(
            LintFinding(
                "D", "WARN", slug, None,
                f"adjacent-equal price pair in '{section}': n={n_start}..{n_end} price={price} "
                f"(carry-down/transposition suspect)",
            )
        )
    for section, n_start, n_end, price, run_len in long_runs:
        findings.append(
            LintFinding(
                "D", "WARN", slug, None,
                f"adjacent-equal price run (informational, likely a real tier) in '{section}': "
                f"n={n_start}..{n_end} price={price} length={run_len}",
            )
        )

    findings.append(
        LintFinding(
            "D", "SKIP", slug, None,
            "adjacent-column price signature: goldens carry no column data, this check cannot fire",
        )
    )
    return findings


def _assert_e_vocabulary(golden: dict, slug: str, ctx: LintContext) -> list[LintFinding]:
    """ERROR. Every ingredient string resolves in the aliases file or in
    accepted_vocabulary.json. This is the assert that catches the
    tofu-skin class: a string nobody ever taught the alias table or the
    vocabulary floor.

    Amendment 3: accepted_vocabulary.json stores raw, unnormalized strings.
    Symmetry is preserved by normalizing BOTH sides at lookup time here,
    through the same normalize_ingredient the scoring layer uses.
    """
    findings: list[LintFinding] = []
    alias_targets = set(ctx.aliases.values())
    for it in golden.get("items", []):
        n = it.get("n")
        for ing in it.get("ingredients", []) or []:
            if not isinstance(ing, str) or not ing.strip():
                continue
            normalized = normalize_ingredient(ing, ctx.aliases)
            if normalized in alias_targets or normalized in ctx.vocabulary_normalized:
                continue
            findings.append(
                LintFinding(
                    "E", "ERROR", slug, n,
                    f"ingredient {ing!r} (normalized {normalized!r}) not in aliases or accepted_vocabulary.json",
                )
            )
    return findings


def _has_romaji(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(rf"\b{re.escape(term)}\b", lowered) for term in ROMAJI_LEXICON)


def _assert_f_romaji(golden: dict, slug: str, ctx: LintContext) -> list[LintFinding]:
    """WARN, never ERROR, never gating (amended). Romaji present on items
    in Sushi and Sashimi sections: WARN when absent, detected across name
    and notes together, case insensitive, accepting both the structured
    'romaji: X' form (masa-sushi) and bare prose (KUU nigiri) equally.
    Reported one line per menu, not per item.

    This is a completeness heuristic, not a mechanical invariant: it
    cannot distinguish a drafter omission from a menu that never printed
    romaji at all. It is a survey that feeds a future convention decision,
    not a defect list.
    """
    missing_ns: list[Optional[int]] = []
    applicable = 0
    for it in golden.get("items", []):
        section = it.get("section") or ""
        if "sushi" not in section.lower() and "sashimi" not in section.lower():
            continue
        applicable += 1
        text = f"{it.get('name') or ''} {it.get('notes') or ''}"
        if not _has_romaji(text):
            missing_ns.append(it.get("n"))
    if applicable == 0 or not missing_ns:
        return []
    return [
        LintFinding(
            "F", "WARN", slug, None,
            f"{len(missing_ns)}/{applicable} items in Sushi/Sashimi sections missing romaji, n={missing_ns}",
        )
    ]


def _assert_g_schema(golden: dict, slug: str, ctx: LintContext) -> list[LintFinding]:
    """ERROR (amended). Each item validates against the merged item schema,
    wrap is in the closed enum, is_raw is true, false, or null (null is the
    README's 'not determinable' and is valid). Validates the item shape
    only: the golden's top-level envelope (restaurant_name, source_photos,
    notes) has no shared schema and is governed by evals/menus/README.md.
    """
    findings: list[LintFinding] = []
    for it in golden.get("items", []):
        n = it.get("n")
        for problem in _validate_item(it, ctx.composed_schema):
            findings.append(LintFinding("G", "ERROR", slug, n, problem))
    return findings


LINT_ASSERTS = (
    _assert_a_confidence_tokens,
    _assert_b_n_contiguity,
    _assert_c_section_manifest,
    _assert_d_price_invariants,
    _assert_e_vocabulary,
    _assert_f_romaji,
    _assert_g_schema,
)


def lint_menu(menu: "Menu", ctx: LintContext) -> list[LintFinding]:
    findings: list[LintFinding] = []
    for fn in LINT_ASSERTS:
        findings.extend(fn(menu.golden, menu.slug, ctx))
    return findings


def cmd_emit_manifest_skeleton(slug: str, out_path: Optional[Path]) -> int:
    """Write an EMPTY sections.json skeleton for a menu. Never reads
    golden.json: section names and expected_count come from counting the
    printed page by hand (design call 1: deriving them from the golden
    would make assert C circular). Refuses to overwrite an existing file.
    """
    target = out_path or (MENUS_DIR / slug / "sections.json")
    if target.exists():
        print(f"refusing to overwrite existing {target}", file=sys.stderr)
        return 2
    skeleton = {
        "_comment": (
            "Hand written from the printed menu page. Section names and "
            "expected_count come from counting the photo, never from "
            "golden.json: deriving them from the golden would make assert C "
            "circular."
        ),
        "sections": [],
        "provenance": {
            "counted_by": None,
            "counted_on": None,
            "source_photo": None,
        },
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(skeleton, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote empty manifest skeleton: {target}")
    return 0


# --------------------------------------------------------------------------
# Ingredient normalization (mirrors the client's deterministic pipeline)
# --------------------------------------------------------------------------


def normalize_ingredient(name: str, aliases: dict[str, str]) -> str:
    """Lowercase, trim, simple plural fold, then alias lookup.

    Mirrors the client normalization so eval scoring matches what users see.
    """
    n = name.strip().lower()
    if n in aliases:
        return aliases[n]
    # Simple plural folding: cheap and reversible, matches the client rule.
    if n.endswith("ies") and len(n) > 4:
        n = n[:-3] + "y"
    elif n.endswith("es") and len(n) > 3 and n[-3] in "sxzo":
        n = n[:-2]
    elif n.endswith("s") and not n.endswith("ss") and len(n) > 3:
        n = n[:-1]
    return aliases.get(n, n)


def normalize_name(name: str) -> str:
    return " ".join(name.strip().lower().split())


# --------------------------------------------------------------------------
# Matching and metrics (docs/EVALS.md)
# --------------------------------------------------------------------------


@dataclass
class MatchResult:
    pairs: list[tuple[int, int]]  # (pred_index, gold_index)
    unmatched_pred: list[int]
    unmatched_gold: list[int]


def match_items(pred: list[dict], gold: list[dict]) -> MatchResult:
    """Greedy one-to-one match by normalized-name token_sort_ratio >= 85.

    Candidate pairs are ranked by score descending; each prediction and each
    golden item is consumed at most once.
    """
    candidates: list[tuple[float, int, int]] = []
    for pi, p in enumerate(pred):
        pname = normalize_name(p.get("name", ""))
        for gi, g in enumerate(gold):
            gname = normalize_name(g.get("name", ""))
            score = token_sort_ratio(pname, gname)
            if score >= NAME_MATCH_THRESHOLD:
                candidates.append((score, pi, gi))
    candidates.sort(key=lambda c: c[0], reverse=True)

    used_pred: set[int] = set()
    used_gold: set[int] = set()
    pairs: list[tuple[int, int]] = []
    for _score, pi, gi in candidates:
        if pi in used_pred or gi in used_gold:
            continue
        used_pred.add(pi)
        used_gold.add(gi)
        pairs.append((pi, gi))

    unmatched_pred = [i for i in range(len(pred)) if i not in used_pred]
    unmatched_gold = [i for i in range(len(gold)) if i not in used_gold]
    return MatchResult(pairs, unmatched_pred, unmatched_gold)


def ingredient_sets(item: dict, aliases: dict[str, str]) -> set[str]:
    return {
        normalize_ingredient(x, aliases)
        for x in item.get("ingredients", [])
        if isinstance(x, str) and x.strip()
    }


def f1(pred_set: set[str], gold_set: set[str]) -> tuple[float, int, int, int]:
    """Return (f1, true_pos, false_pos, false_neg)."""
    tp = len(pred_set & gold_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    if tp == 0:
        return (0.0 if (fp or fn) else 1.0, tp, fp, fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return (2 * precision * recall / (precision + recall), tp, fp, fn)


def price_matches(pred: dict, gold: dict) -> bool:
    pp, gp = pred.get("price"), gold.get("price")
    if pp is None and gp is None:
        # Both null: intent matches when the verbatim text agrees.
        return normalize_name(str(pred.get("price_text") or "")) == normalize_name(
            str(gold.get("price_text") or "")
        )
    if pp is None or gp is None:
        return False
    return abs(float(pp) - float(gp)) < 1e-6


@dataclass
class MenuScore:
    slug: str
    item_recall: float
    item_precision: float
    ingredient_f1_macro: float
    ingredient_f1_micro: float
    price_accuracy: float
    wrap_accuracy: Optional[float]
    n_pred: int
    n_gold: int
    n_matched: int
    diffs: list[str] = field(default_factory=list)


@dataclass
class ConsistencyRow:
    """One menu's data across --repeat N independent runs. Item counts are
    expected to be bit-identical (a deterministic pipeline reading the same
    photo); ingredient_f1_macro is the metric task #12 found to actually
    vary run to run, so its spread is what the consistency gate measures."""

    slug: str
    n_preds: list[int]
    f1_values: list[float]

    @property
    def item_counts_identical(self) -> bool:
        return len(set(self.n_preds)) <= 1

    @property
    def f1_spread(self) -> float:
        return max(self.f1_values) - min(self.f1_values) if self.f1_values else 0.0


def evaluate_consistency_gate(
    rows: list["ConsistencyRow"],
) -> Optional[tuple[str, float, float, bool]]:
    """None when --repeat was not used (nothing measured, same as before this
    fix). Otherwise a normal gate-row tuple, shaped identically to
    evaluate_gates()'s rows, so it slots into the same Gates table instead of
    needing separate rendering.

    An item-count mismatch across repeats is folded into the same PASS/FAIL
    as the F1-spread threshold, one gate, not two, matching task #12's own
    card phrasing ("gate is identical item counts across 3 runs plus
    ingredient F1 spread <= 0.03"): both conditions gate together.
    """
    if not rows:
        return None
    threshold = GATES["consistency_f1_spread_max"]
    max_spread = max(row.f1_spread for row in rows)
    all_identical = all(row.item_counts_identical for row in rows)
    ok = all_identical and max_spread <= threshold
    return ("consistency_f1_spread_max", max_spread, threshold, ok)


def score_menu(slug: str, pred: list[dict], gold: list[dict], aliases: dict[str, str]) -> MenuScore:
    match = match_items(pred, gold)
    n_matched = len(match.pairs)

    recall = n_matched / len(gold) if gold else 0.0
    precision = n_matched / len(pred) if pred else 0.0

    f1s: list[float] = []
    micro_tp = micro_fp = micro_fn = 0
    price_hits = 0
    wrap_total = wrap_hits = 0
    diffs: list[str] = []

    for pi, gi in match.pairs:
        p, g = pred[pi], gold[gi]
        pset = ingredient_sets(p, aliases)
        gset = ingredient_sets(g, aliases)
        item_f1, tp, fp, fn = f1(pset, gset)
        f1s.append(item_f1)
        micro_tp += tp
        micro_fp += fp
        micro_fn += fn

        if price_matches(p, g):
            price_hits += 1
        else:
            diffs.append(
                f"price mismatch on '{g.get('name')}': pred={p.get('price')!r}/{p.get('price_text')!r} gold={g.get('price')!r}/{g.get('price_text')!r}"
            )

        gold_wrap = g.get("wrap")
        if gold_wrap not in (None, "unknown"):
            wrap_total += 1
            if p.get("wrap") == gold_wrap:
                wrap_hits += 1

        if item_f1 < 1.0:
            missing = gset - pset
            extra = pset - gset
            diffs.append(
                f"ingredients on '{g.get('name')}': missing={sorted(missing)} extra={sorted(extra)}"
            )

    for gi in match.unmatched_gold:
        diffs.append(f"MISSED golden item: '{gold[gi].get('name')}'")
    for pi in match.unmatched_pred:
        diffs.append(f"EXTRA predicted item: '{pred[pi].get('name')}'")

    macro_f1 = sum(f1s) / len(f1s) if f1s else 0.0
    micro_f1, _, _, _ = (
        (2 * (micro_tp / (micro_tp + micro_fp)) * (micro_tp / (micro_tp + micro_fn))
         / ((micro_tp / (micro_tp + micro_fp)) + (micro_tp / (micro_tp + micro_fn))),
         0, 0, 0)
        if micro_tp
        else (0.0, 0, 0, 0)
    )
    price_acc = price_hits / n_matched if n_matched else 0.0
    wrap_acc = (wrap_hits / wrap_total) if wrap_total else None

    return MenuScore(
        slug=slug,
        item_recall=recall,
        item_precision=precision,
        ingredient_f1_macro=macro_f1,
        ingredient_f1_micro=micro_f1,
        price_accuracy=price_acc,
        wrap_accuracy=wrap_acc,
        n_pred=len(pred),
        n_gold=len(gold),
        n_matched=n_matched,
        diffs=diffs,
    )


# --------------------------------------------------------------------------
# Extraction pipeline
# --------------------------------------------------------------------------


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


@dataclass
class CallUsage:
    """One Anthropic call's usage, tagged by menu, photo, and kind.

    The kind tag lets the report distinguish the cache-warming details call
    (batch 1) from the calls that should read from cache (batch 2+), per
    SPEC.md's caching requirement and the named bug check in write_report.
    """

    menu_slug: str
    photo_index: int
    kind: str  # index | details_batch_1 | details_batch_n | details_retry
    usage: Usage


class HarnessParseError(RuntimeError):
    """Model output could not be parsed as JSON, or carried no text block.

    P1-SB2: raised instead of letting json.JSONDecodeError propagate raw. The
    full response is already on disk under evals/crash/ by the time this is
    raised; the message names the menu and call kind so a crashed --all run
    localizes without re-reading tracebacks against arithmetic guesses.
    """


class HarnessTruncationError(RuntimeError):
    """Model output parsed cleanly but stop_reason was max_tokens.

    P1-SB2: a parse success on truncated output is not treated as a pass.
    Silently scoring truncated JSON is worse than crashing, so this call
    fails the whole run exactly like HarnessParseError does.
    """


@dataclass
class CallContext:
    """Identifies one Anthropic call for crash-file and usage-JSONL naming.

    photo_index is None only for the --url-smoke path, which has no photo;
    source there is the URL string instead of a photo path.
    """

    run_stem: str
    menu_slug: str
    kind: str
    model: str
    photo_index: Optional[int] = None
    source: str = ""


def _sum_usage(call_usages: list[CallUsage]) -> Usage:
    total = Usage()
    for c in call_usages:
        total.input_tokens += c.usage.input_tokens
        total.output_tokens += c.usage.output_tokens
        total.cache_creation_input_tokens += c.usage.cache_creation_input_tokens
        total.cache_read_input_tokens += c.usage.cache_read_input_tokens
    return total


def _media_type_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in (".jpg", ".jpeg"):
        return "image/jpeg"
    if suffix == ".png":
        return "image/png"
    raise ValueError(f"unsupported image type: {path}")


def _image_block(photo: Path) -> dict:
    """Image-first content block with a prompt-cache breakpoint.

    Mirrors src/extract.ts's imageBlock() exactly: same source shape, same
    cache_control placement.
    """
    data = base64.b64encode(photo.read_bytes()).decode("ascii")
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": _media_type_for(photo), "data": data},
        "cache_control": {"type": "ephemeral"},
    }


def _usage_from_response(resp: Any) -> Usage:
    u = resp.usage
    return Usage(
        input_tokens=u.input_tokens,
        output_tokens=u.output_tokens,
        cache_creation_input_tokens=getattr(u, "cache_creation_input_tokens", 0) or 0,
        cache_read_input_tokens=getattr(u, "cache_read_input_tokens", 0) or 0,
    )


def _write_crash_file(ctx: CallContext, resp: Any, raw_text: Optional[str], error_detail: str) -> Path:
    """Dump the FULL raw response plus metadata so a crash is diagnosable
    from disk, not from arithmetic inference (P1-SC's crashes never left
    a payload behind; this is the fix). One file per crash; the run stem,
    menu, photo, call kind, and a time-based sequence make the name unique
    and self-describing without needing to open it to know what happened.
    """
    CRASH_DIR.mkdir(parents=True, exist_ok=True)
    photo_tag = f"p{ctx.photo_index}" if ctx.photo_index is not None else "p-"
    seq = time.time_ns()
    path = CRASH_DIR / f"{ctx.run_stem}-{ctx.menu_slug}-{photo_tag}-{ctx.kind}-{seq}.json"
    usage = _usage_from_response(resp) if resp is not None else None
    payload = {
        "menu_slug": ctx.menu_slug,
        "call_kind": ctx.kind,
        "photo_index": ctx.photo_index,
        "source": ctx.source,
        "model": ctx.model,
        "stop_reason": getattr(resp, "stop_reason", None) if resp is not None else None,
        "usage": {
            "input_tokens": usage.input_tokens if usage else None,
            "output_tokens": usage.output_tokens if usage else None,
            "cache_creation_input_tokens": usage.cache_creation_input_tokens if usage else None,
            "cache_read_input_tokens": usage.cache_read_input_tokens if usage else None,
        },
        "error_detail": error_detail,
        "raw_response_text": raw_text,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _usage_jsonl_path(run_stem: str) -> Path:
    return USAGE_DIR / f"{run_stem}.jsonl"


def _record_call(call_usages: list[CallUsage], ctx: CallContext, resp: Any) -> CallUsage:
    """Append to the in-memory list exactly as before, and immediately
    append one JSONL line to disk (P1-SB2 1e), so a crash on menu N never
    again loses accounting for menus 1..N-1, or even for the crashing call
    itself: this runs before _extract_json is given a chance to raise.
    """
    usage = _usage_from_response(resp)
    call = CallUsage(ctx.menu_slug, ctx.photo_index if ctx.photo_index is not None else -1, ctx.kind, usage)
    call_usages.append(call)
    USAGE_DIR.mkdir(parents=True, exist_ok=True)
    line = {
        "ts": time.time(),
        "stem": ctx.run_stem,
        "slug": ctx.menu_slug,
        "photo_index": ctx.photo_index,
        "kind": ctx.kind,
        "model": ctx.model,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cache_creation_input_tokens": usage.cache_creation_input_tokens,
        "cache_read_input_tokens": usage.cache_read_input_tokens,
        "stop_reason": getattr(resp, "stop_reason", None),
    }
    with open(_usage_jsonl_path(ctx.run_stem), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
        f.flush()
    return call


def _extract_json(resp: Any, ctx: CallContext) -> dict:
    """Read json_schema-mode structured output: the first text block,
    JSON-parsed. output_config.format constrains generation, it does not
    change the response envelope (verified against live docs this session).

    P1-SB2: defensive at every call site. A JSONDecodeError, or no text
    block at all, writes the FULL raw response to evals/crash/ and raises
    HarnessParseError naming the menu and call kind. No silent recovery, no
    new auto-retry beyond the existing details_retry (a domain retry for
    items missing after the first batch, untouched here). A response that
    parses cleanly but carries stop_reason == "max_tokens" also writes a
    crash file (the payload is evidence, not garbage) and raises
    HarnessTruncationError: silently scoring truncated output is worse than
    crashing.
    """
    text_block = None
    for block in resp.content:
        if block.type == "text":
            text_block = block.text
            break

    if text_block is None:
        path = _write_crash_file(ctx, resp, None, "no text block in Anthropic response")
        print(f"crash file written: {path}", file=sys.stderr)
        raise HarnessParseError(
            f"{ctx.menu_slug} [{ctx.kind}]: no text block in Anthropic response; "
            f"raw response saved to {path}"
        )

    try:
        data = json.loads(text_block)
    except json.JSONDecodeError as e:
        path = _write_crash_file(ctx, resp, text_block, str(e))
        print(f"crash file written: {path}", file=sys.stderr)
        raise HarnessParseError(
            f"{ctx.menu_slug} [{ctx.kind}]: JSON parse failed ({e}); raw response saved to {path}"
        ) from e

    stop_reason = getattr(resp, "stop_reason", None)
    if stop_reason == "max_tokens":
        path = _write_crash_file(
            ctx, resp, text_block, "parsed successfully but stop_reason == max_tokens"
        )
        print(f"crash file written: {path}", file=sys.stderr)
        raise HarnessTruncationError(
            f"{ctx.menu_slug} [{ctx.kind}]: stop_reason == max_tokens (truncated output); "
            f"raw response saved to {path}"
        )

    return data


def _index_params(assets: SharedAssets, photo: Path, model: str) -> dict:
    return {
        "model": model,
        "max_tokens": INDEX_MAX_TOKENS,
        "system": assets.system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [_image_block(photo), {"type": "text", "text": assets.index_task}],
            }
        ],
        "output_config": {"format": {"type": "json_schema", "schema": assets.index_schema}},
    }


def _details_params(assets: SharedAssets, photo: Path, batch_items: list[dict], model: str) -> dict:
    task_text = assets.details_task + "\n\nItems for this batch:\n" + json.dumps(
        [{"n": it["n"], "name": it["name"]} for it in batch_items]
    )
    return {
        "model": model,
        "max_tokens": DETAILS_MAX_TOKENS,
        "system": assets.system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [_image_block(photo), {"type": "text", "text": task_text}],
            }
        ],
        "output_config": {"format": {"type": "json_schema", "schema": assets.details_schema}},
    }


def _url_params(assets: SharedAssets, url: str, model: str) -> dict:
    if assets.url_schema is None or assets.url_task is None:
        raise RuntimeError("url schema or url task prompt not loaded")
    return {
        "model": model,
        "max_tokens": URL_MAX_TOKENS,
        "system": assets.system_prompt,
        "messages": [{"role": "user", "content": f"{url}\n\n{assets.url_task}"}],
        "tools": [
            {
                "type": WEB_FETCH_TOOL_TYPE,
                "name": "web_fetch",
                "max_uses": WEB_FETCH_MAX_USES,
                "max_content_tokens": WEB_FETCH_MAX_CONTENT_TOKENS,
            }
        ],
        "output_config": {"format": {"type": "json_schema", "schema": assets.url_schema}},
    }


def _merge_details_into_index(index_items: list[dict], details_by_n: dict[int, dict]) -> list[dict]:
    merged_items: list[dict] = []
    for idx_item in index_items:
        n = idx_item["n"]
        det = details_by_n.get(n)
        merged = dict(idx_item)
        if det:
            for key in ("ingredients", "wrap", "is_raw", "notes"):
                if key in det:
                    merged[key] = det[key]
        else:
            # Reconcile miss: never silently dropped, flagged instead.
            merged["ingredients"] = []
            merged["wrap"] = "unknown"
            merged["is_raw"] = None
            merged["notes"] = "RECONCILE_MISSING"
        merged_items.append(merged)
    return merged_items


def _run_photo_pipeline(
    client: "anthropic.Anthropic",
    assets: SharedAssets,
    menu_slug: str,
    photo_index: int,
    photo: Path,
    model: str,
    run_stem: str,
) -> tuple[list[dict], list[CallUsage]]:
    """index -> details in batches of 8, batch 1 solo to warm the cache,
    then the rest -> reconcile.

    Mirrors src/extract.ts's request shapes exactly. The browser client's
    concurrency-3 fan-out for the remaining batches is not reproduced here;
    evals run sequentially for determinism and debuggability. That is a
    deliberate, noted divergence from production orchestration, not from
    the request shape, which matches exactly.
    """
    call_usages: list[CallUsage] = []

    index_resp = client.messages.create(**_index_params(assets, photo, model))
    idx_ctx = CallContext(run_stem, menu_slug, "index", model, photo_index, str(photo))
    _record_call(call_usages, idx_ctx, index_resp)
    index_items = _extract_json(index_resp, idx_ctx).get("items", [])

    batches = [
        index_items[i : i + DETAILS_BATCH_SIZE] for i in range(0, len(index_items), DETAILS_BATCH_SIZE)
    ]
    details_by_n: dict[int, dict] = {}

    for batch_idx, batch in enumerate(batches):
        kind = "details_batch_1" if batch_idx == 0 else "details_batch_n"
        resp = client.messages.create(**_details_params(assets, photo, batch, model))
        det_ctx = CallContext(run_stem, menu_slug, kind, model, photo_index, str(photo))
        _record_call(call_usages, det_ctx, resp)
        for it in _extract_json(resp, det_ctx).get("items", []):
            details_by_n[it["n"]] = it

    # One retry batch for whatever's still missing after the first pass.
    missing = [it for it in index_items if it["n"] not in details_by_n]
    if missing:
        retry_resp = client.messages.create(**_details_params(assets, photo, missing, model))
        retry_ctx = CallContext(run_stem, menu_slug, "details_retry", model, photo_index, str(photo))
        _record_call(call_usages, retry_ctx, retry_resp)
        for it in _extract_json(retry_resp, retry_ctx).get("items", []):
            details_by_n[it["n"]] = it

    merged_items = _merge_details_into_index(index_items, details_by_n)
    return merged_items, call_usages


def _fuzzy_merge(all_photo_items: list[list[dict]]) -> list[dict]:
    """Multi-photo merge and dedupe, per SPEC.md exactly: global id
    photoIndex:n; two items merge only when fuzzy name match (the same
    token_sort_ratio >= 85 rule used for golden scoring) AND compatible
    price (equal, or either side null) both hold; on merge, keep the
    record with more ingredients and union the notes.
    """
    merged: list[dict] = []
    for photo_idx, items in enumerate(all_photo_items):
        for it in items:
            candidate = dict(it)
            candidate["_global_id"] = f"{photo_idx}:{it['n']}"
            match_idx = None
            for i, existing in enumerate(merged):
                name_score = token_sort_ratio(
                    normalize_name(existing["name"]), normalize_name(candidate["name"])
                )
                if name_score < NAME_MATCH_THRESHOLD:
                    continue
                ep, cp = existing.get("price"), candidate.get("price")
                compatible = ep is None or cp is None or abs(float(ep) - float(cp)) < 1e-6
                if compatible:
                    match_idx = i
                    break
            if match_idx is None:
                merged.append(candidate)
                continue
            existing = merged[match_idx]
            if len(candidate.get("ingredients", [])) > len(existing.get("ingredients", [])):
                kept, other = candidate, existing
            else:
                kept, other = existing, candidate
            kept = dict(kept)
            notes = " ".join(x for x in (kept.get("notes"), other.get("notes")) if x)
            kept["notes"] = notes or None
            merged[match_idx] = kept
    return merged


def run_pipeline_for_menu(
    menu: Menu, assets: SharedAssets, model: str, use_batch: bool, run_stem: str
) -> tuple[list[dict], list[CallUsage]]:
    """Run the full per-photo index/details/reconcile pipeline plus merge.

    Returns the merged predicted items and the per-call usage records.
    Mirrors src/extract.ts's request shapes, including prompt caching and
    the warm-then-fan-out batch ordering, so evals measure the real system.
    """
    if use_batch:
        return _run_pipeline_for_menu_batch(menu, assets, model, run_stem)

    client = anthropic.Anthropic()
    per_photo_items: list[list[dict]] = []
    call_usages: list[CallUsage] = []
    for photo_index, photo in enumerate(menu.photos):
        items, usages = _run_photo_pipeline(
            client, assets, menu.slug, photo_index, photo, model, run_stem
        )
        per_photo_items.append(items)
        call_usages.extend(usages)
    merged = _fuzzy_merge(per_photo_items)
    return merged, call_usages


def _poll_batch(client: "anthropic.Anthropic", batch_id: str) -> Any:
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            return batch
        time.sleep(5)


def _run_pipeline_for_menu_batch(
    menu: Menu, assets: SharedAssets, model: str, run_stem: str
) -> tuple[list[dict], list[CallUsage]]:
    """Route the full per-photo pipeline through the Message Batches API.

    Two Batches jobs: one for every photo's index call, then (once item
    counts are known) one for every details batch across every photo, then
    a third if any items are still missing after that (mirroring the
    sync path's one-retry rule). Batch results arrive in any order; keyed
    by custom_id throughout. Written in full but only reachable via
    --batch, never invoked this session.
    """
    client = anthropic.Anthropic()
    call_usages: list[CallUsage] = []

    # Request is a TypedDict (anthropic.types.messages.batch_create_params.Request);
    # a plain dict literal satisfies it at runtime with no import needed.
    index_requests = [
        {"custom_id": f"{photo_idx}:index", "params": _index_params(assets, photo, model)}
        for photo_idx, photo in enumerate(menu.photos)
    ]
    index_batch = client.messages.batches.create(requests=index_requests)
    index_batch = _poll_batch(client, index_batch.id)

    index_items_by_photo: dict[int, list[dict]] = {}
    for result in client.messages.batches.results(index_batch.id):
        photo_idx = int(result.custom_id.split(":", 1)[0])
        if result.result.type == "succeeded":
            idx_ctx = CallContext(
                run_stem, menu.slug, "index", model, photo_idx, str(menu.photos[photo_idx])
            )
            _record_call(call_usages, idx_ctx, result.result.message)
            data = _extract_json(result.result.message, idx_ctx)
            index_items_by_photo[photo_idx] = data.get("items", [])
        else:
            index_items_by_photo[photo_idx] = []

    details_requests = []
    batch_map: dict[str, int] = {}
    for photo_idx, photo in enumerate(menu.photos):
        items = index_items_by_photo.get(photo_idx, [])
        batches = [
            items[i : i + DETAILS_BATCH_SIZE] for i in range(0, len(items), DETAILS_BATCH_SIZE)
        ]
        for batch_idx, batch_items in enumerate(batches):
            custom_id = f"{photo_idx}:{batch_idx}"
            batch_map[custom_id] = photo_idx
            details_requests.append(
                {
                    "custom_id": custom_id,
                    "params": _details_params(assets, photo, batch_items, model),
                }
            )

    details_by_photo: dict[int, dict[int, dict]] = {i: {} for i in range(len(menu.photos))}
    if details_requests:
        details_batch = client.messages.batches.create(requests=details_requests)
        details_batch = _poll_batch(client, details_batch.id)
        for result in client.messages.batches.results(details_batch.id):
            photo_idx = batch_map[result.custom_id]
            batch_idx = int(result.custom_id.split(":", 1)[1])
            kind = "details_batch_1" if batch_idx == 0 else "details_batch_n"
            if result.result.type == "succeeded":
                det_ctx = CallContext(
                    run_stem, menu.slug, kind, model, photo_idx, str(menu.photos[photo_idx])
                )
                _record_call(call_usages, det_ctx, result.result.message)
                for it in _extract_json(result.result.message, det_ctx).get("items", []):
                    details_by_photo[photo_idx][it["n"]] = it

    missing_by_photo: dict[int, list[dict]] = {}
    for photo_idx in range(len(menu.photos)):
        index_items = index_items_by_photo.get(photo_idx, [])
        missing = [it for it in index_items if it["n"] not in details_by_photo[photo_idx]]
        if missing:
            missing_by_photo[photo_idx] = missing

    if missing_by_photo:
        retry_requests = [
            {
                "custom_id": f"{photo_idx}:retry",
                "params": _details_params(assets, menu.photos[photo_idx], missing, model),
            }
            for photo_idx, missing in missing_by_photo.items()
        ]
        retry_batch = client.messages.batches.create(requests=retry_requests)
        retry_batch = _poll_batch(client, retry_batch.id)
        for result in client.messages.batches.results(retry_batch.id):
            photo_idx = int(result.custom_id.split(":", 1)[0])
            if result.result.type == "succeeded":
                retry_ctx = CallContext(
                    run_stem, menu.slug, "details_retry", model, photo_idx, str(menu.photos[photo_idx])
                )
                _record_call(call_usages, retry_ctx, result.result.message)
                for it in _extract_json(result.result.message, retry_ctx).get("items", []):
                    details_by_photo[photo_idx][it["n"]] = it

    per_photo_items: list[list[dict]] = []
    for photo_idx in range(len(menu.photos)):
        index_items = index_items_by_photo.get(photo_idx, [])
        merged_items = _merge_details_into_index(index_items, details_by_photo[photo_idx])
        per_photo_items.append(merged_items)

    merged = _fuzzy_merge(per_photo_items)
    return merged, call_usages


def estimate_cost(usage: Usage) -> float:
    return (
        usage.input_tokens * PRICE_PER_MTOK["input"]
        + usage.cache_creation_input_tokens * PRICE_PER_MTOK["cache_write"]
        + usage.cache_read_input_tokens * PRICE_PER_MTOK["cache_read"]
        + usage.output_tokens * PRICE_PER_MTOK["output"]
    ) / 1_000_000


# --------------------------------------------------------------------------
# Gates and report
# --------------------------------------------------------------------------


def aggregate(scores: list[MenuScore]) -> dict[str, float]:
    total_gold = sum(s.n_gold for s in scores)
    total_pred = sum(s.n_pred for s in scores)
    total_matched = sum(s.n_matched for s in scores)
    macro_f1 = sum(s.ingredient_f1_macro for s in scores) / len(scores) if scores else 0.0
    price_matched = sum(s.price_accuracy * s.n_matched for s in scores)
    return {
        "item_recall": total_matched / total_gold if total_gold else 0.0,
        "item_precision": total_matched / total_pred if total_pred else 0.0,
        "ingredient_f1_macro": macro_f1,
        "price_accuracy": price_matched / total_matched if total_matched else 0.0,
    }


def evaluate_gates(agg: dict[str, float]) -> list[tuple[str, float, float, bool]]:
    rows = []
    for key in ["item_recall", "item_precision", "ingredient_f1_macro", "price_accuracy"]:
        threshold = GATES[key]
        value = agg.get(key, 0.0)
        rows.append((key, value, threshold, value >= threshold))
    return rows


def write_report(
    scores: list[MenuScore],
    agg: dict[str, float],
    gate_rows: list[tuple[str, float, float, bool]],
    total_usage: Usage,
    call_usages: list[CallUsage],
    model: str,
    timestamp: str,
    consistency_rows: Optional[list["ConsistencyRow"]] = None,
) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / f"{timestamp}.md"
    lines: list[str] = []
    lines.append(f"# Eval report {timestamp}")
    lines.append("")
    lines.append(f"Model: `{model}`")
    lines.append("")
    lines.append("## Gates")
    lines.append("")
    lines.append("| Gate | Measured | Threshold | Result |")
    lines.append("|---|---|---|---|")
    for key, value, threshold, ok in gate_rows:
        lines.append(f"| {key} | {value:.4f} | >= {threshold:.2f} | {'PASS' if ok else 'FAIL'} |")
    lines.append("")
    if consistency_rows:
        lines.append(f"## Consistency (--repeat {len(consistency_rows[0].n_preds)})")
        lines.append("")
        lines.append("| Menu | Item counts per run | Identical | Ing F1 per run | Spread |")
        lines.append("|---|---|---|---|---|")
        for row in consistency_rows:
            counts = ", ".join(str(n) for n in row.n_preds)
            f1s = ", ".join(f"{v:.3f}" for v in row.f1_values)
            identical = "yes" if row.item_counts_identical else "NO"
            lines.append(f"| {row.slug} | {counts} | {identical} | {f1s} | {row.f1_spread:.4f} |")
        lines.append("")
    lines.append("## Per-menu breakdown")
    lines.append("")
    lines.append("| Menu | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |")
    lines.append("|---|---|---|---|---|---|---|")
    for s in scores:
        wrap = f"{s.wrap_accuracy:.3f}" if s.wrap_accuracy is not None else "n/a"
        lines.append(
            f"| {s.slug} | {s.n_pred}/{s.n_gold} | {s.item_recall:.3f} | {s.item_precision:.3f} | "
            f"{s.ingredient_f1_macro:.3f} | {s.price_accuracy:.3f} | {wrap} |"
        )
    lines.append("")
    lines.append("## Token usage and cost")
    lines.append("")
    lines.append(f"- input: {total_usage.input_tokens}")
    lines.append(f"- cache write: {total_usage.cache_creation_input_tokens}")
    lines.append(f"- cache read: {total_usage.cache_read_input_tokens}")
    lines.append(f"- output: {total_usage.output_tokens}")
    lines.append(f"- estimated cost: ${estimate_cost(total_usage):.4f}")
    lines.append("")
    if call_usages:
        lines.append("### Cache counters by call kind")
        lines.append("")
        lines.append("| Kind | Calls | Cache write | Cache read |")
        lines.append("|---|---|---|---|")
        for kind in sorted({c.kind for c in call_usages}):
            kind_calls = [c for c in call_usages if c.kind == kind]
            cw = sum(c.usage.cache_creation_input_tokens for c in kind_calls)
            cr = sum(c.usage.cache_read_input_tokens for c in kind_calls)
            lines.append(f"| {kind} | {len(kind_calls)} | {cw} | {cr} |")
        lines.append("")

        # Named bug check (T-1.11): details batches 2+ should read from the
        # cache the index call and details batch 1 warmed. Zero reads here
        # across every batch-2+ call means caching is broken.
        details_2plus = [c for c in call_usages if c.kind == "details_batch_n"]
        if details_2plus:
            with_reads = [c for c in details_2plus if c.usage.cache_read_input_tokens > 0]
            bug_flag = "ok" if with_reads else "BUG SUSPECTED"
            lines.append(
                f"- cache check (details calls 2+): {len(with_reads)}/{len(details_2plus)} "
                f"had cache reads > 0 [{bug_flag}]"
            )
        else:
            lines.append("- cache check (details calls 2+): no batch-2+ details calls this run")
        lines.append("")
    for s in scores:
        if not s.diffs:
            continue
        lines.append(f"## Diffs: {s.slug}")
        lines.append("")
        for d in s.diffs:
            lines.append(f"- {d}")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------


def cmd_check(args: Optional[argparse.Namespace] = None) -> int:
    """Offline readiness check, plus the offline golden lint (P1-SB).

    Makes zero API calls, so it is safe to run any time. This is the Phase 0
    proof that the harness plumbing works before any prompt or schema exists.
    --menu, if given, narrows only the lint step's reporting; discovery and
    the raw photo count above it are unconditional.
    """
    print("Sushi Selector eval harness: readiness check (no API calls)")
    print(f"repo root: {REPO_ROOT}")

    assets: Optional[SharedAssets] = None
    try:
        assets = load_shared_assets()
        print("shared assets: loaded")
        print(f"  system.md: {len(assets.system_prompt)} chars")
        print(f"  aliases: {len(assets.aliases)} entries")
        print(f"  url task: {'present' if assets.url_task else 'absent (optional)'}")
    except FileNotFoundError as e:
        print(f"shared assets: NOT READY ({e})")

    menus = discover_menus()
    print(f"scored menus discovered: {len(menus)}")
    for m in menus:
        print(f"  - {m.slug}: {len(m.photos)} photo(s), {len(m.golden.get('items', []))} golden items")

    # T3-1: raw/ is now organized into per-restaurant subdirectories (session
    # A's reorganization), so a non-recursive count silently reads 0. Fixed
    # to walk recursively; both numbers print so the fix is visible, not
    # assumed. Sorted with the same directory-qualified natural-sort key as
    # the recursive walk elsewhere, so the printed order is deterministic.
    raw = MENUS_DIR / "raw"
    if raw.exists():
        old_raw_imgs = [p for p in raw.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES]
        new_raw_imgs = sorted(
            (p for p in raw.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES),
            key=_raw_photo_sort_key,
        )
        print(
            f"raw drop folder: {len(new_raw_imgs)} original photo(s) kept as provenance "
            f"(organized into menus) [T3-1 fix: recursive; non-recursive count was "
            f"{len(old_raw_imgs)}]"
        )

    key_present = bool(os.environ.get("ANTHROPIC_API_KEY"))
    print(f"ANTHROPIC_API_KEY in env: {'yes' if key_present else 'no'}")

    # Prove the deterministic scoring layer works, offline, on a tiny fixture.
    _self_test()
    print("scoring self-test: PASS")

    if assets is not None:
        _schema_composition_self_test(assets)
        print("schema composition self-test: PASS (index schema union details schema == url item subschema)")

    _lint_self_test()
    print("lint self-test: PASS (one negative fixture per assert A-G, synthetic, no repo golden used)")

    _crash_path_self_test()
    print(
        "crash-path self-test: PASS (synthetic truncated JSON in a temp dir, "
        "no repo golden, no API call)"
    )

    aliases = assets.aliases if assets is not None else {}
    vocabulary_raw = load_accepted_vocabulary()
    vocabulary_normalized = frozenset(normalize_ingredient(v, aliases) for v in vocabulary_raw)
    ctx = LintContext(
        aliases=aliases,
        vocabulary_normalized=vocabulary_normalized,
        composed_schema=_composed_item_schema(),
        menus_dir=MENUS_DIR,
    )

    lint_target_slug = getattr(args, "menu", None) if args is not None else None
    lint_menus = menus
    if lint_target_slug:
        lint_menus = [m for m in menus if m.slug == lint_target_slug]
        if not lint_menus:
            print(f"no menu with slug '{lint_target_slug}'", file=sys.stderr)
            return 2

    print(f"\ngolden lint: {len(lint_menus)} menu(s)")
    all_findings: list[LintFinding] = []
    for m in lint_menus:
        findings = lint_menu(m, ctx)
        all_findings.extend(findings)
        errors = [f for f in findings if f.severity == "ERROR"]
        warns = [f for f in findings if f.severity == "WARN"]
        skips = [f for f in findings if f.severity == "SKIP"]
        print(f"  - {m.slug}: {len(errors)} ERROR, {len(warns)} WARN, {len(skips)} SKIP")
        for f in errors + warns + skips:
            where = f" n={f.n}" if f.n is not None else ""
            print(f"      [{f.assert_id} {f.severity}]{where} {f.message}")

    error_count = sum(1 for f in all_findings if f.severity == "ERROR")
    warn_count = sum(1 for f in all_findings if f.severity == "WARN")
    skip_count = sum(1 for f in all_findings if f.severity == "SKIP")
    print(f"\nlint totals: {error_count} ERROR, {warn_count} WARN, {skip_count} SKIP")

    print("\nreadiness check complete. Run --menu <slug> or --all to spend API credits.")
    return 1 if error_count else 0


def _lint_self_test() -> None:
    """Synthetic, in-memory fixtures proving each assert A-G fires when it
    should (and, for the two amended asserts, does NOT fire where the
    amendment says it must not). Never uses a repo golden as a fixture.

    Assert C is file-based by design (it reads a hand-written sidecar off
    disk), so its fixture lives in a throwaway temporary directory, never
    under evals/menus/.
    """
    aliases = {"krab": "imitation crab"}
    vocab_normalized = frozenset({"tuna", "rice", "nori", "imitation crab"})
    schema = _composed_item_schema()
    ctx = LintContext(
        aliases=aliases,
        vocabulary_normalized=vocab_normalized,
        composed_schema=schema,
        menus_dir=MENUS_DIR,
    )

    def _item(**kw: Any) -> dict:
        base = {
            "n": 1,
            "name": "Test Roll",
            "section": "Test",
            "price_text": "5.00",
            "price": 5.0,
            "ingredients": ["tuna"],
            "wrap": "nori",
            "is_raw": False,
            "notes": None,
        }
        base.update(kw)
        return base

    # A: a confidence token outside notes fires ERROR.
    golden = {"items": [_item(name="INFERRED Spicy Roll")]}
    assert any(f.severity == "ERROR" for f in _assert_a_confidence_tokens(golden, "fixture", ctx)), (
        "assert A did not fire on a confidence token in name"
    )
    # A exemption: the same token in notes must not fire (docs/EVALS.md).
    golden = {"items": [_item(notes="INFERRED: tuna")]}
    assert not _assert_a_confidence_tokens(golden, "fixture", ctx), (
        "assert A fired on the notes field, which is exempt"
    )

    # B: a gap in n fires ERROR.
    golden = {"items": [_item(n=1), _item(n=3)]}
    assert any(f.severity == "ERROR" for f in _assert_b_n_contiguity(golden, "fixture", ctx)), (
        "assert B did not fire on a gap in n"
    )

    # C: a sidecar count mismatch fires ERROR; an absent sidecar SKIPs.
    with tempfile.TemporaryDirectory() as tmp:
        tmp_menus = Path(tmp)
        (tmp_menus / "fixture-menu").mkdir()
        (tmp_menus / "fixture-menu" / "sections.json").write_text(
            json.dumps({"sections": [{"section": "Test", "expected_count": 99}]}),
            encoding="utf-8",
        )
        c_ctx = LintContext(
            aliases=aliases, vocabulary_normalized=vocab_normalized, composed_schema=schema, menus_dir=tmp_menus
        )
        golden = {"items": [_item(n=1)]}
        assert any(f.severity == "ERROR" for f in _assert_c_section_manifest(golden, "fixture-menu", c_ctx)), (
            "assert C did not fire on a section count mismatch"
        )
        assert any(f.severity == "SKIP" for f in _assert_c_section_manifest(golden, "no-sidecar-menu", c_ctx)), (
            "assert C did not SKIP when the sidecar is absent"
        )

    # D: a negative price fires ERROR.
    golden = {"items": [_item(price=-1.0, price_text="-1.00")]}
    assert any(f.severity == "ERROR" for f in _assert_d_price_invariants(golden, "fixture", ctx)), (
        "assert D did not fire on a negative price"
    )
    # D, amendment 4: null price with a single-parseable price_text is WARN,
    # never ERROR.
    golden = {"items": [_item(price=None, price_text="5.00")]}
    d_findings = _assert_d_price_invariants(golden, "fixture", ctx)
    assert any(f.assert_id == "D" and f.severity == "WARN" for f in d_findings), (
        "assert D amendment 4 (null price, single-number price_text) did not WARN"
    )
    assert not any(f.severity == "ERROR" for f in d_findings), (
        "assert D amendment 4 fired ERROR on a null price, which the amendment forbids"
    )
    # D, amendment 5: an adjacent-equal-price pair (run length 2) is
    # reported as a collapsed pair-run, not two separate item lines.
    golden = {
        "items": [
            _item(n=1, price=8.0, price_text="8.00"),
            _item(n=2, price=8.0, price_text="8.00"),
        ]
    }
    assert any("adjacent-equal price pair" in f.message for f in _assert_d_price_invariants(golden, "fixture", ctx)), (
        "assert D amendment 5 pair-run did not fire"
    )

    # E: an ingredient absent from both the aliases and the vocabulary fires ERROR.
    golden = {"items": [_item(ingredients=["durian"])]}
    assert any(f.severity == "ERROR" for f in _assert_e_vocabulary(golden, "fixture", ctx)), (
        "assert E did not fire on an unknown ingredient"
    )

    # F: a Sushi-section item with no romaji anywhere WARNs.
    golden = {"items": [_item(section="Sushi", name="Tuna", notes=None)]}
    assert any(f.severity == "WARN" for f in _assert_f_romaji(golden, "fixture", ctx)), (
        "assert F did not fire when romaji is absent"
    )

    # G: a wrap value outside the closed enum fires ERROR.
    golden = {"items": [_item(wrap="paper")]}
    assert any(f.severity == "ERROR" for f in _assert_g_schema(golden, "fixture", ctx)), (
        "assert G did not fire on an invalid wrap value"
    )
    # G, amendment 1 regression guard: is_raw: null must NOT fire.
    golden = {"items": [_item(is_raw=None)]}
    assert not _assert_g_schema(golden, "fixture", ctx), (
        "assert G fired on is_raw: null, which the amendment requires to be valid"
    )


def _self_test() -> None:
    """Sanity-check matching and metrics on a hand-built fixture (no API)."""
    gold = [
        {"name": "Spicy Tuna Roll", "price": 8.0, "price_text": "8", "ingredients": ["spicy tuna", "rice", "nori"], "wrap": "nori"},
        {"name": "California Roll", "price": 7.0, "price_text": "7", "ingredients": ["imitation crab", "avocado", "cucumber"], "wrap": "nori"},
    ]
    pred = [
        {"name": "spicy tuna roll", "price": 8.0, "price_text": "8", "ingredients": ["spicy tuna", "rice", "nori"], "wrap": "nori"},
        {"name": "California Roll", "price": 7.0, "price_text": "7", "ingredients": ["krab", "avocado", "cucumber"], "wrap": "nori"},
    ]
    aliases = {"krab": "imitation crab"}
    s = score_menu("fixture", pred, gold, aliases)
    assert s.n_matched == 2, s.n_matched
    assert abs(s.item_recall - 1.0) < 1e-9
    assert abs(s.item_precision - 1.0) < 1e-9
    assert abs(s.price_accuracy - 1.0) < 1e-9
    # With the alias table, krab -> imitation crab, so ingredient F1 is perfect.
    assert abs(s.ingredient_f1_macro - 1.0) < 1e-9, s.ingredient_f1_macro


class _FakeBlock:
    def __init__(self, text: str) -> None:
        self.type = "text"
        self.text = text


class _FakeUsage:
    def __init__(self) -> None:
        self.input_tokens = 111
        self.output_tokens = 222
        self.cache_creation_input_tokens = 0
        self.cache_read_input_tokens = 0


class _FakeResp:
    """Stands in for an anthropic.types.Message: just enough shape for
    _extract_json (.content, .stop_reason, .usage) to exercise the crash
    path without a real API call.
    """

    def __init__(self, text: str, stop_reason: str) -> None:
        self.content = [_FakeBlock(text)]
        self.stop_reason = stop_reason
        self.usage = _FakeUsage()


def _crash_path_self_test() -> None:
    """Offline proof of the P1-SB2 crash path (1h): synthetic truncated JSON
    written to a temp directory shows the crash file gets written with the
    full raw payload, and the labeled error is raised. Never a repo golden,
    never a real API call. Restores the real CRASH_DIR when done, and
    swallows the "crash file written" stderr lines the real path prints, so
    --check's own output stays exactly one line longer (the PASS line),
    which is what the neutrality check in Step 1h measures.
    """
    global CRASH_DIR
    real_crash_dir = CRASH_DIR
    with tempfile.TemporaryDirectory() as tmp:
        CRASH_DIR = Path(tmp) / "crash"
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                # Case 1: truncated JSON, cut mid-string, unterminated.
                truncated = '{"items": [{"n": 1, "name": "Spicy Tuna Rol'
                ctx = CallContext("selftest", "fixture-menu", "index", "fixture-model", 0, "fixture.jpg")
                resp = _FakeResp(truncated, "end_turn")
                try:
                    _extract_json(resp, ctx)
                    raise AssertionError("expected HarnessParseError, got no exception")
                except HarnessParseError as e:
                    assert "fixture-menu" in str(e) and "index" in str(e), str(e)

                crash_files = sorted(CRASH_DIR.glob("*.json"))
                assert len(crash_files) == 1, f"expected 1 crash file, found {len(crash_files)}"
                payload = json.loads(crash_files[0].read_text(encoding="utf-8"))
                assert payload["raw_response_text"] == truncated, "crash file must hold the FULL raw text"
                assert payload["menu_slug"] == "fixture-menu"
                assert payload["call_kind"] == "index"
                assert payload["stop_reason"] == "end_turn"
                assert "usage" in payload and "error_detail" in payload

                # Case 2: valid JSON, but stop_reason == max_tokens.
                valid = json.dumps({"items": []})
                ctx2 = CallContext(
                    "selftest", "fixture-menu", "details_batch_1", "fixture-model", 0, "fixture.jpg"
                )
                resp2 = _FakeResp(valid, "max_tokens")
                try:
                    _extract_json(resp2, ctx2)
                    raise AssertionError("expected HarnessTruncationError, got no exception")
                except HarnessTruncationError as e:
                    assert "fixture-menu" in str(e) and "max_tokens" in str(e), str(e)

                crash_files_after = sorted(CRASH_DIR.glob("*.json"))
                assert len(crash_files_after) == 2, (
                    f"expected 2 crash files total, found {len(crash_files_after)}"
                )
        finally:
            CRASH_DIR = real_crash_dir


def cmd_run(args: argparse.Namespace) -> int:
    """Full or single-menu scored run. Requires the Phase 1 pipeline."""
    model = os.environ.get("MODEL", DEFAULT_MODEL)
    try:
        assets = load_shared_assets()
    except FileNotFoundError as e:
        print(f"cannot run: {e}", file=sys.stderr)
        print("run `uv run evals/run_evals.py --check` for readiness.", file=sys.stderr)
        return 2

    menus = discover_menus()
    if args.menu:
        menus = [m for m in menus if m.slug == args.menu]
        if not menus:
            print(f"no menu with slug '{args.menu}'", file=sys.stderr)
            return 2
    if not menus:
        print("no scored menus found under evals/menus/", file=sys.stderr)
        return 2

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2

    # Computed before the loop (P1-SB2): it names the incremental usage JSONL
    # (evals/usage/<timestamp>.jsonl) as well as the final report, so usage
    # persists under the same stem from the very first call.
    timestamp = args.timestamp or "report"

    # repeat < 1 (a stray --repeat 0) is nonsensical for a "how many times do
    # we run this" count; treat it the same as the unset default (1 run,
    # today's behavior, nothing measured), rather than looping zero times
    # and reporting on scores that were never computed.
    repeat = max(1, args.repeat)

    all_call_usages: list[CallUsage] = []
    scores: list[MenuScore] = []
    consistency_rows: list[ConsistencyRow] = []
    for i, menu in enumerate(menus, start=1):
        repeat_note = f", {repeat} repeat run(s)" if repeat > 1 else ""
        print(f"[{i}/{len(menus)}] {menu.slug}: starting, {len(menu.photos)} photo(s){repeat_note}", flush=True)

        menu_calls = 0
        repeat_scores: list[MenuScore] = []
        for _ in range(repeat):
            pred, call_usages = run_pipeline_for_menu(menu, assets, model, args.batch, timestamp)
            all_call_usages.extend(call_usages)
            menu_calls += len(call_usages)
            repeat_scores.append(score_menu(menu.slug, pred, menu.golden.get("items", []), assets.aliases))

        # The first repeat's score feeds the normal Gates table and per-menu
        # breakdown, unchanged in shape from before this fix; every repeat's
        # score feeds the consistency row when repeat > 1.
        scores.append(repeat_scores[0])
        if repeat > 1:
            consistency_rows.append(
                ConsistencyRow(
                    slug=menu.slug,
                    n_preds=[s.n_pred for s in repeat_scores],
                    f1_values=[s.ingredient_f1_macro for s in repeat_scores],
                )
            )

        running_cost = estimate_cost(_sum_usage(all_call_usages))
        print(
            f"[{i}/{len(menus)}] {menu.slug}: done, {menu_calls} call(s), "
            f"running cost ${running_cost:.4f}",
            flush=True,
        )

    total_usage = _sum_usage(all_call_usages)
    agg = aggregate(scores)
    gate_rows = evaluate_gates(agg)
    consistency_gate = evaluate_consistency_gate(consistency_rows)
    if consistency_gate:
        gate_rows.append(consistency_gate)
    path = write_report(
        scores, agg, gate_rows, total_usage, all_call_usages, model, timestamp, consistency_rows
    )
    print(f"report written: {path}")
    all_pass = all(ok for *_x, ok in gate_rows)
    print("GATES: " + ("PASS" if all_pass else "FAIL"))
    return 0 if all_pass else 1


def cmd_url_smoke(args: argparse.Namespace) -> int:
    """Loose, ungated URL-path smoke checks against --urls.

    Per EVALS.md these never contribute to the pass/fail gates (there is no
    URL golden set); they only report item and section counts per URL.
    Genuinely inert without --urls: prints usage guidance and exits without
    touching the network.
    """
    if not args.urls:
        print("no --urls given; nothing to smoke-test. Example:", file=sys.stderr)
        print("  uv run evals/run_evals.py --url-smoke --urls https://example.com/menu", file=sys.stderr)
        return 2
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2
    try:
        assets = load_shared_assets()
    except FileNotFoundError as e:
        print(f"cannot run: {e}", file=sys.stderr)
        return 2
    if assets.url_task is None or assets.url_schema is None:
        print("url task or url schema missing; cannot smoke-test", file=sys.stderr)
        return 2

    model = os.environ.get("MODEL", DEFAULT_MODEL)
    run_stem = getattr(args, "timestamp", None) or "url-smoke"
    client = anthropic.Anthropic()
    for url in args.urls:
        try:
            resp = client.messages.create(**_url_params(assets, url, model))
            ctx = CallContext(run_stem, "url-smoke", "url", model, None, url)
            data = _extract_json(resp, ctx)
            n_items = len(data.get("items", []))
            n_sections = len(data.get("sections", []))
            print(f"{url}: {n_items} item(s), {n_sections} section(s)")
            if n_items < 5:
                print("  NOTE: fewer than 5 items, matches SPEC.md's low-yield URL warning")
        except Exception as e:  # smoke checks report failures, never raise
            print(f"{url}: FAILED to parse structured output ({e})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Sushi Selector eval harness")
    p.add_argument("--check", action="store_true", help="offline readiness check, no API calls")
    p.add_argument("--all", action="store_true", help="run every menu in the golden set")
    p.add_argument("--menu", type=str, help="run a single menu by slug")
    p.add_argument("--repeat", type=int, default=1, help="consistency runs per menu")
    p.add_argument("--batch", action="store_true", help="route via the Message Batches API")
    p.add_argument("--url-smoke", action="store_true", help="loose URL-path smoke checks (reported, not gated)")
    p.add_argument("--urls", type=str, nargs="*", help="URLs for --url-smoke (space separated)")
    p.add_argument("--timestamp", type=str, help="report filename stem (caller supplies a real timestamp)")
    p.add_argument(
        "--emit-manifest-skeleton",
        type=str,
        metavar="SLUG",
        help="write an empty sections.json skeleton for <slug>, never reads golden.json",
    )
    p.add_argument(
        "--out",
        type=str,
        help="output path for --emit-manifest-skeleton (default evals/menus/<slug>/sections.json)",
    )
    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    if args.emit_manifest_skeleton:
        out_path = Path(args.out) if args.out else None
        return cmd_emit_manifest_skeleton(args.emit_manifest_skeleton, out_path)
    if args.check:
        return cmd_check(args)
    if args.url_smoke:
        return cmd_url_smoke(args)
    if args.all or args.menu:
        return cmd_run(args)
    build_parser().print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
