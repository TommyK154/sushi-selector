# EVALS.md: extraction quality gates

Extraction reliability is the product, and this harness is the working
definition of "reliable". No prompt or schema change merges without a passing
run, and the report from that run gets committed alongside the change.

## Golden set layout

```
evals/menus/<slug>/photos/1.jpg   ordered photos, one or more per menu
evals/menus/<slug>/photos/2.jpg   (front and back pages, and so on)
evals/menus/<slug>/golden.json    hand-verified truth for the merged menu
evals/reports/<timestamp>.md      generated reports
```

golden.json uses the merged result shape: one items array covering all of the
menu's photos combined, where each item has name, section, price_text, price,
ingredients, wrap, and is_raw, matching the schemas in SPEC.md. The harness
runs the full per-photo pipeline plus the merge and dedupe step from SPEC.md
before scoring, so multi-photo menus exercise the merge logic and any
false-merge or duplicate leakage shows up directly in item precision and
recall.

Labeling conventions are LOCKED in evals/menus/README.md in the repo and
must be mirrored into shared/prompts/system.md (T-1.3): rice stays out of
ingredients, wrapper lives only in the wrap field, seared tuna is raw,
beverages are excluded, standard fillings for undescribed rolls are
inferred and flagged in notes, and restaurant_name is null unless
literally printed in the photo. Goldens also carry unscored metadata:
source_photos, and notes fields holding INFERRED and LOW/MED confidence
flags for reviewer attention.

## Producing goldens (workflow and rule)

Claude Code drafts each golden by reading the photo directly and hand-labeling
it in a separate, careful pass. Tom reviews and corrects every golden before
it counts. The hard rule: never generate goldens by running the extraction
pipeline or its prompts, because a system must not grade its own homework.
Draft labels with fresh eyes, item by item, zoomed in.

## Metrics

Matching: predicted items map to golden items by normalized-name fuzzy match
(rapidfuzz token_sort_ratio >= 85, greedy best-match, one-to-one).

- Item recall: matched golden items / all golden items.
- Item precision: matched predictions / all predictions (hallucinated or
  duplicated items hurt here).
- Ingredient F1: per matched item, F1 between predicted and golden normalized
  ingredient sets (after the same alias table the app uses). Report macro
  (mean per item) and micro (pooled).
- Price accuracy: over matched items, exact numeric equality, or both null
  with matching price_text intent.
- Wrap accuracy: over matched items where golden wrap is not unknown.
- Consistency: the two designated menus (pick the densest and the ugliest)
  run three times each; report item-count variance and ingredient F1 spread.

## Gates (all must pass)

- Item recall >= 0.97 and precision >= 0.97 across the golden set.
- Macro ingredient F1 >= 0.90.
- Price accuracy >= 0.97.
- Consistency: identical item counts across all three runs on both designated
  menus, and ingredient F1 spread <= 0.03.

If gates cannot be met on the default model after honest prompt iteration
(style guide tightening, batch size tuning, image quality guidance), escalate
the model per SPEC.md and record the decision and cost delta in the report.

## Harness (evals/run_evals.py)

- PEP 723 inline dependencies (anthropic, rapidfuzz at minimum); executed via
  `uv run evals/run_evals.py`. Reads ANTHROPIC_API_KEY from the environment.
- Loads shared/prompts/ and shared/schema/ directly, so evals exercise the
  exact production assets, and mirrors the production request shapes,
  including prompt caching and the index/details/reconcile flow.
- Flags: `--all`, `--menu <slug>`, `--repeat <n>` (consistency runs),
  `--batch` (route calls through the Message Batches API at the 50 percent
  discount for full tuning sweeps where latency does not matter).
- Output: a markdown report in evals/reports/ with an aggregate gates table
  (pass/fail per gate), a per-menu breakdown, per-item diffs for failures,
  token usage, and estimated cost.
- Cost expectation: a full run over 8 golden menus should land well under
  $0.50 with caching, and half that with --batch. The tuning loop is designed
  to fit comfortably inside the $5 workspace cap alongside real usage.

### Offline golden lint (`--check`)

`--check` makes zero API calls and needs no `ANTHROPIC_API_KEY`; it is safe to
run any time. Beyond loading shared assets and discovering menus, it runs
seven asserts (A through G) against every `golden.json`, bounding the class of
mechanical error that is otherwise invisible until it shows up as a scoring
artifact in a run that costs credits. `--check --menu <slug>` narrows the lint
step to one menu; discovery and the raw-photo count above it stay unconditional.
`--emit-manifest-skeleton <slug> [--out <path>]` writes an empty
`sections.json` skeleton (see `evals/menus/README.md`), refuses to overwrite an
existing file, and never opens `golden.json`.

Goldens are human owned. A lint finding is reported for hand correction, never
auto-fixed by the harness.

| Assert | Checks | Severity |
|---|---|---|
| A | no confidence or inference token (`INFERRED`, `LOW`, `MED`, `HIGH`) outside `notes` | ERROR |
| B | `n` values are contiguous from 1, no gaps, no duplicates | ERROR |
| C | item counts and section name/order match the hand-written `sections.json` sidecar, when one exists | ERROR when present, SKIP when the sidecar is absent |
| D | `price_text` present; non-null `price` agrees with the number `price_text` parses to; no negative or zero price | ERROR |
| D | a null `price` whose `price_text` parses to exactly one number | WARN |
| D | adjacent items in the same section sharing a price, collapsed into runs (length-2 pairs reported first as the carry-down/transposition suspect, length-3+ runs reported after as informational) | WARN |
| D | adjacent-column price signature | SKIP always; these goldens carry no column data to check against |
| E | every ingredient string resolves in `shared/aliases.json` or `evals/accepted_vocabulary.json`, both sides normalized through `normalize_ingredient` at lookup time | ERROR |
| F | romaji present in `name` or `notes` (structured `romaji: X` or bare prose, case insensitive) for items in a Sushi or Sashimi section | WARN, reported once per menu as missing-over-applicable, never gating |
| G | each item validates against the item schema composed from `shared/schema/index.schema.json` union `details.schema.json` (proven equal to `url.schema.json`'s item subschema by a self-test on every run); `wrap` is in the closed enum; `is_raw` is `true`, `false`, or `null` | ERROR |

Exit code: `1` if any assert produced an ERROR anywhere in the lint menus,
`0` when only WARN and SKIP findings exist. Every `--check` run also executes
`_lint_self_test`, a synthetic in-memory fixture per assert that proves each
one fires (and, where amended, does not fire where it should not); no repo
golden is ever used as a fixture.

Assert F is a completeness survey feeding a future romaji convention
decision, not a defect list: it cannot distinguish a drafter omission from a
menu that genuinely never printed romaji, and its current detector and
lexicon are known to be incomplete (see `docs/BUILDLOG.md`'s P1-SB entries for
the measured gaps). Its WARN count is a lower bound, not a measurement.

## Tom's photo collection guidance

6 to 10 menus, shot like a normal impatient human at a table, not a
photographer. Deliberately include:

- one shot in dim restaurant lighting
- one laminated menu with glare
- one taken at a lazy angle
- one dense multi-column menu (the 60+ item kind)
- one specials board or handwritten insert if available
- one non-sushi menu as the stretch case
- at least one menu spanning two photos, to exercise multi-photo merge

Drop them in evals/menus/raw/ and Claude Code will organize, slugify, and
draft goldens for review.
