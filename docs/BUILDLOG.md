Append-only log of scoped agent work sessions: what was authorized, what was
touched, and with what result. Newest entry last.

---

## Session 2026-07-21: post-review consistency pass over c091e40

Base commit: c091e40

### Authorized scope (verbatim)

SCOPE (pre-approved; do not re-confirm, do not exceed):

Task: post-review consistency pass over commit c091e40. Rule-check sweep
of the golden set, review-snapshot update, two doc drift fixes, genesis
entry in the session receipts log. One commit.
Files, modify only these:
  evals/menus/*/golden.json   (9 files, category (a) fixes only, see Task 1)
  evals/menus/README.md       (human-review snapshot section only)
  docs/EVALS.md               (integrate one missing passage only)
  docs/HANDOFF.md             (remove one stale pointer line, if present)
  docs/BUILDLOG.md            (new, append-only session receipts, Task 5)
Not touching: everything else. Explicitly: nothing under shared/, src/,
public/, .github/. No new files except docs/BUILDLOG.md. No wrangler. No
eval-harness runs. No Anthropic API calls. No Phase 1 work. Anything not
in the files list is out of scope: if it appears to need changing, report
it, do not change it.
Dependencies: repo at origin/main c091e40; the locked labeling conventions
in evals/menus/README.md, which are the source of truth for this sweep.
Done when: pre-flight passed; all 9 goldens swept against every convention;
category (a) fixes applied; category (b) findings listed with verbatim
evidence and zero edits; snapshot reads all 9 reviewed 2026-07-20; the
EVALS.md passage integrated; the HANDOFF.md pointer handled; BUILDLOG
genesis entry appended; one commit pushed to origin/main; closing report
printed.
Priority: this is the only task this session.

### Manifest (files touched)

- evals/menus/km-sushi-cold-appetizer/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-dinner/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-hot-appetizer-salad/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-lunch/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-nigiri/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-noodles-kitchen/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-sashimi/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-special-rolls/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/kuu-sushi-happy-hour/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/README.md: human-review snapshot updated to all 9 reviewed 2026-07-20
- docs/EVALS.md: locked-conventions and unscored-metadata passage integrated into Golden set layout
- docs/HANDOFF.md: stale docs/RUNBOOK.md pointer removed from the preflight lead-in
- docs/BUILDLOG.md: created (this file)

---

## Session 2026-07-22: reconciliation and rule-enforcement pass over af0c029

Base commit: af0c029 (descendant of 2823343; Tom's adjudication commit
"Adjudicate sweep findings: wrap enum to none, egg canonical, KUU naming")

### Authorized scope (verbatim)

SCOPE (pre-approved; do not re-confirm, do not exceed):

Task: reconciliation and rule-enforcement pass. Bring the locked
conventions in evals/menus/README.md to parity with the master rule
list below, fix the restaurant naming in the photos description, then
sweep all 9 goldens against the newly added rules only and apply
mechanical fixes. One commit.
Files, modify only these:
  evals/menus/README.md       (LOCKED conventions section and the
                               photos description section only)
  evals/menus/*/golden.json   (9 files, category (a) fixes under the
                               newly added rules only, see Task 3)
  docs/BUILDLOG.md            (append one entry)
Not touching: everything else. Explicitly: nothing under shared/,
src/, public/, .github/, docs/ other than BUILDLOG.md. No wrangler,
no eval runs, no Anthropic API calls, no Phase 1 work. Anything
outside the listed files is report-only.
Dependencies: Tom's adjudication commit at origin/main (a descendant
of 2823343) carrying his four manual edits.
Done when: pre-flight passed; missing rules integrated; naming fixed;
all 9 goldens swept against the new rules with (a) applied and (b)
escalated with verbatim evidence; BUILDLOG entry appended; one commit
pushed; closing report printed with the full updated LOCKED section
verbatim.
Priority: this is the only task this session.

### Amendment (mid-session, user-authorized)

Two locked decisions from the 2026-07-2x sweep were formalized on top of the
original scope: (1) preparation-method stripping gains a contested-term
exception; "fried garlic" and "fried onion" recur across items as named crispy
garnishes, so they stay whole as canonical ingredients (same test as
pickle/cucumber) rather than stripping to garlic/onion. (2) The n=33
special-rolls golden, which had stripped "garlic" in ingredients with
"fried garlic" only in notes, is corrected to canonical "fried garlic" and the
now-redundant note fragment removed (the wrapper note is retained, as the
wrap-none rule requires it). A review gate (diffs shown before commit) was
honored.

### Manifest (files touched)

- evals/menus/README.md: LOCKED section brought to parity with the 7-rule
  master list (3 bullets extended: canonical/roe-family + egg-not-tamago, wrap
  physical-wrap-none + enum-never-grows, is_raw shrimp/octopus default false;
  4 bullets added: prep-method stripping + recurring-garnish exception,
  species/type qualifiers, vague-terms notes-only, combo choice sets). Photos
  description section: restaurant name "KM Sushi" corrected to "KUU SUSHI" with
  a parenthetical noting the km-sushi- folder slugs are kept stable (minimal-
  literal scope; the "two restaurants" intro and "KM" shorthands left as-is and
  flagged in the closing report)
- evals/menus/km-sushi-special-rolls/golden.json: n=17 "Vegas" ingredient
  "feep fried eel" -> "eel" (typo'd prep prefix, the known instance); n=33
  ingredient "garlic" -> "fried garlic" with the redundant "; fried garlic"
  note fragment trimmed (wrapper note retained)
- evals/menus/km-sushi-cold-appetizer/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-dinner/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-hot-appetizer-salad/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-lunch/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-nigiri/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-noodles-kitchen/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/km-sushi-sashimi/golden.json: swept, no category (a) fix needed (unchanged)
- evals/menus/kuu-sushi-happy-hour/golden.json: swept, no category (a) fix needed (unchanged)
- docs/BUILDLOG.md: this entry appended

### Category (b) findings (escalated, verbatim evidence, zero edits)

- km-sushi-special-rolls "seared pepper salmon" (item with ingredients spicy
  tuna, cilantro, avocado, cucumber, jalapeno, seared pepper salmon): compound
  prep, is_raw-relevant, not a recurring garnish; left as printed.
- km-sushi-nigiri n=2 "Sweet Shrimp" is_raw: true and km-sushi-sashimi n=12
  "Live-Sweet Shrimp" is_raw: true: contradict the shrimp default false, but
  sweet shrimp (amaebi) is conventionally raw; menu evidence is in photos not
  opened, so no edit per rule.

### Patterns (alias-table seeds for T-1.4, not created this pass)

- freshwater eel -> eel
- unagi -> eel
- tamago -> egg
- (implied by the new roe-family scope) smelt roe -> masago, flying fish roe ->
  tobiko, salmon roe -> ikura
- The recurring-garnish exception means "fried garlic" and "fried onion" are
  canonical leaves, NOT alias sources to garlic/onion.

---

## Session 2026-07-22: convention clarifications follow-up over 2843c21

Base commit: 2843c21

### Authorized scope (verbatim)

SCOPE (pre-approved; do not re-confirm, do not exceed):
Task: convention clarifications follow-up. Six small edits to
evals/menus/README.md, receipt, one commit.
Files, modify only: evals/menus/README.md, docs/BUILDLOG.md (append).
Not touching: everything else. Goldens explicitly untouched this
session. No wrangler, no eval runs, no Anthropic API calls.
Done when: six edits applied, BUILDLOG entry appended, one commit
pushed to origin/main, closing report printed.

### Manifest (files touched)

- evals/menus/README.md: six edits. (1) is_raw bullet: printed-name-is-evidence
  clarification (sweet shrimp/live default raw; is_raw tracks the item as served;
  explicit whole-item cooking method overrides the live default). (2) ingredients
  bullet: seared-fish compounds (seared tuna, seared pepper salmon) stay whole as
  is_raw evidence. (3) photos intro reworded to one restaurant KUU SUSHI captured
  as two menu artifacts; happy-hour bullet lead-in relabeled to "KUU SUSHI happy
  hour". (4) coverage sentence: four restaurant-shorthand "KM" changed to "KUU"
  (slug references left). (5) prep-strip bullet: exception list is explicit and
  closed, joined only via documented convention change; ingredients transcribed
  as printed, never renamed to a category. (6) placeholder "2026-07-2x" replaced
  with "2026-07-22".
- docs/BUILDLOG.md: this entry appended

---

## Session 2026-07-22: Phase 1 product artifacts (schemas, prompts, aliases) over 68c878c

Base commit: 68c878c

### Authorized scope (verbatim)

SCOPE (pre-approved; do not re-confirm, do not exceed):

Task: author the Phase 1 product artifacts. Schemas, prompts, and the
expanded alias table. No API calls, no wrangler, no eval-harness runs.
Also confirm the consistency-gate menu designation by visual inspection.
Files, modify only these:
  shared/schema/index.schema.json      (new)
  shared/schema/details.schema.json    (new)
  shared/schema/url.schema.json        (new, combined URL schema)
  shared/prompts/system.md             (new)
  shared/prompts/index-task.md         (new)
  shared/prompts/details-task.md       (new)
  shared/prompts/url-task.md           (new)
  shared/aliases.json                  (expand existing 5 entries)
  docs/BUILDLOG.md                     (append)
Not touching: everything else. Explicitly: nothing under src/, public/,
.github/, evals/run_evals.py, any golden.json. No wrangler, no eval
runs, no Anthropic API calls. This session writes files and commits;
it does not spend.
Dependencies: evals/menus/README.md (LOCKED conventions, single source
per T-1.3), SPEC.md schema shapes, shared/aliases.json's existing
5 entries and the alias seeds already logged (freshwater eel to eel,
unagi to eel, tamago to egg, smelt roe to masago, flying fish roe to
tobiko, salmon roe to ikura).
Done when: all seven files written and internally consistent with
each other and with README; aliases.json expanded; consistency-gate
menus confirmed by visual check; BUILDLOG entry appended; one commit
pushed; closing report printed with the full system.md content
verbatim for oversight cross-check.
Priority: this is the only task this session.

### Pre-flight

1. Working tree clean; HEAD == origin/main == 68c878cfcd4c5ea31b6f585b99498ce864a8bdec. Pass.
2. shared/schema/ and shared/prompts/ confirmed empty. Pass.
3. shared/aliases.json confirmed exactly 5 entries. Pass.
4. evals/menus/README.md LOCKED section confirmed present with all three
   named 2026-07-22 clarifications (is_raw item-as-served semantics,
   seared-fish compounds, closed garnish-exception list). Flagged one
   discrepancy: the check describes "7 master rules" but the LOCKED
   section is an unlabeled list of 14 bullets, not a countable 7. Resolved
   against this file's own history: the "7-rule master list" phrase
   originates in the 2026-07-22 rule-parity session above and was the
   count before that session's own extensions and the following
   clarifications session grew it further. Substantive content check
   passed; treated as non-blocking and proceeded.

### Manifest (files touched)

- shared/schema/index.schema.json: created, transcribed verbatim from SPEC.md
- shared/schema/details.schema.json: created, transcribed verbatim from SPEC.md
- shared/schema/url.schema.json: created, combined shape (details item shape
  plus section, price_text, price per item, plus top-level sections array),
  no restaurant_name field (SPEC.md's prose description of the combined
  schema does not name one; see findings below)
- shared/prompts/system.md: created, style guide mirroring all 14 LOCKED
  README rules in expanded substance (not summary), ~2,727 words / ~16.8k
  characters, comfortably over the 2,500-token cache-floor target. Adds one
  clause beyond a literal README mirror: preserve the verbatim printed
  spelling in notes when a normalized ingredient (currently: krab to
  imitation crab) differs materially from what was printed, per SPEC.md's
  own description of this prompt's crab guidance
- shared/prompts/index-task.md: created, index-pass instruction referencing index.schema.json
- shared/prompts/details-task.md: created, details-pass instruction referencing details.schema.json
- shared/prompts/url-task.md: created, combined-pass instruction referencing url.schema.json
- shared/aliases.json: expanded from 5 to 8 entries (added freshwater eel ->
  eel, unagi -> eel, tamago -> egg). Confirmed fried garlic and fried onion
  are not present as alias sources. The 5 original entries left untouched
  (see findings below on one pre-existing entry)
- docs/BUILDLOG.md: this entry appended

### Consistency-gate menu designation (visual inspection)

Opened evals/menus/raw/IMG_3434.jpeg (km-sushi-nigiri), IMG_3433.jpeg
(km-sushi-sashimi), IMG_3440.jpeg (km-sushi-cold-appetizer), and
IMG_3441.jpeg (km-sushi-hot-appetizer-salad) directly.

- Densest: `km-sushi-nigiri` (IMG_3434). Confirmed: single photo, three
  menu sections (Premium Sushi, Sushi, Basic Roll), roughly 40 priced items,
  visible glare and 90-degree rotation.
- Ugliest: `km-sushi-sashimi` (IMG_3433). IMG_3433 carries comparably severe
  rotation and glare to IMG_3434 (a bright wash over the gold Premium
  Sashimi panel) but far fewer items, making it a distinct stress case from
  the density pick rather than a duplicate. IMG_3440 and IMG_3441 were also
  checked and ruled out: both rotated but clean and fully legible, no
  meaningful glare, consistent with README tagging them "rotated" only.

### Findings for Tom (report-only, no edits made)

- url.schema.json has no `restaurant_name` field. SPEC.md's prose for the
  combined URL schema names only "the details item shape plus section,
  price_text, and price per item, and the sections array," with no mention
  of restaurant_name. Implemented literally as described, but this means a
  URL-only parse can never produce a real restaurant name and always falls
  back to "Menu, <date>." Possible gap worth a deliberate decision, not
  patched here (design-level, out of scope to resolve unilaterally).
- shared/aliases.json's pre-existing entry `"bonito flake": "katsuo bushi"`
  runs the opposite direction from the general non-roe convention (plain
  English canonical, Japanese aliases inward, e.g. tamago -> egg), and
  README does not mention bonito or katsuobushi at all under either
  pattern. Left untouched: this entry predates this session and the task
  was to expand, not to correct existing entries. Flagging for a deliberate
  call on which direction is intended.
- Considered but did not add `anago -> eel` (saltwater eel, distinct from
  unagi) or `mayo sauce -> mayo` as further aliases. Neither is named in
  README or in the seed list this session was given; adding either would
  have been an unverified guess rather than an implied requirement.
- README's roe-family rule states "the alias table... maps English -> the
  menu term, never the reverse," a fact about alias-table directionality
  that system.md does not restate verbatim, since it describes a
  downstream client mechanic rather than an extraction instruction. Judged
  non-blocking, noting for the record per the self-check task.
- The "preserve verbatim spelling in notes" clause added to system.md's
  crab section (per SPEC.md's explicit description) was not generalized to
  the roe family or tamago/egg, since only the crab case is stated
  explicitly anywhere in the source docs. Worth a deliberate decision on
  whether it should generalize.
- None of this session's seven artifacts have been run through the model or
  the eval harness (both explicitly out of scope this session); T-1.3's
  "run the eval harness" step remains the actual verification of whether
  these prompts and schemas work in practice.

### Patterns established

- Alias-table seeds logged in the prior 2026-07-22 session (freshwater eel,
  unagi, tamago; roe family) are now implemented in shared/aliases.json.
- System-prompt style guide content should mirror README's LOCKED section
  rule-for-rule but is expected to expand each into fuller extraction
  guidance (rationale, edge cases, examples) rather than restate it as a
  summary; SPEC.md's own prose about system.md's content is an equally
  authoritative source for prompt content, not just a schema-shape
  reference, and this session found one place (crab/notes preservation)
  where SPEC.md's prose said more than README's bullet did.

### Single next action

Run `uv run evals/run_evals.py --menu km-sushi-nigiri` (or `--all`) once
Tom authorizes an Anthropic API spend, to get first empirical signal on
whether these schemas and prompts produce valid, accurate output before
iterating further.

---

## Session 2026-07-23: Phase 1 request layer over 3e53b4a

Base commit: 3e53b4a (Phase 1: extraction schemas, prompts, and expanded
alias table)

### Authorized scope (verbatim)

SCOPE (pre-approved; do not re-confirm, do not exceed):

Task: Phase 1 request layer. Write src/extract.ts, complete the eval
harness pipeline wiring, and apply four adjudicated corrections to the
shared artifacts. This session ends at the spend gate: it makes ZERO
Anthropic API calls. Wiring the gun is in scope; firing it is not.
Files, modify only these:
  src/extract.ts               (new)
  evals/run_evals.py           (complete run_pipeline_for_menu, --batch
                                and --url-smoke plumbing, report
                                cost/cache lines)
  shared/schema/url.schema.json  (add nullable restaurant_name)
  shared/prompts/url-task.md     (one clause: restaurant_name only when
                                  literally printed on the fetched page,
                                  else null)
  shared/aliases.json          (flip bonito entry, add three)
  docs/SPEC.md                 (one-line amendment: combined URL schema
                                includes nullable restaurant_name)
  docs/BUILDLOG.md              (append)
Not touching: everything else. Explicitly: no other src/ files, nothing
under public/ or .github/, no golden.json, no system.md, no
index/details schemas or task files. No wrangler. NO Anthropic API
calls of any kind. The only permitted harness invocations are
`uv run evals/run_evals.py --check` and its built-in self-test; never
--menu, --all, --repeat, --batch, or --url-smoke this session, since
after your wiring those spend real credits.
Dependencies: HEAD 3e53b4a artifacts (schemas, prompts, aliases);
SPEC.md call specification; CLAUDE.md live-docs mandate.
Done when: live-docs checks recorded; extract.ts written with both
output paths; run_pipeline_for_menu implemented mirroring extract.ts's
request shape; corrections applied; --check green; BUILDLOG entry
appended; one commit pushed; closing report printed. No spend.
Priority: this is the only task this session.

### Amendment (mid-session, user-authorized)

At the plan-mode checkpoint, extract.ts's design ran into a real
architectural gap: it needs shared/prompts/*.md content at build time,
but Wrangler's bundler (esbuild) has no default loader for .md (verified
against live Cloudflare docs: defaults are .txt/.html/.sql/.bin/.wasm
only), and adding one requires a wrangler.jsonc "rules" entry, which the
original scope's "Not touching" line excluded ("No wrangler"). Asked the
user how to proceed (inline copies vs. real imports vs. escalate); the
user authorized wrangler.jsonc joining the touched-files list for
exactly one change: a `rules` entry declaring shared/prompts/*.md as
Text modules (fallthrough true), so extract.ts imports the real prompt
files rather than holding duplicate copies. Verification: a build-only
check with no deploy, no dev server, no account interaction, if one
exists; otherwise skip and tag unverified. See Verification below for
what was actually run.

### Pre-flight

1. Working tree clean; HEAD == origin/main == 3e53b4a3b49d246ed17b0c1647977687d1297789. Pass.
2. All seven shared artifacts from 3e53b4a present (index/details/url
   schemas; system/index-task/details-task/url-task prompts). Pass.
3. evals/run_evals.py's run_pipeline_for_menu still raised
   NotImplementedError before this session's edits. Pass.
4. ANTHROPIC_API_KEY present in env (needed for nothing this session,
   present so a later --check exit-criteria read would be valid). Pass.

### Live-docs findings (verified this session, not from training memory)

- Structured outputs: `output_config: {"format": {"type": "json_schema",
  "schema": {...}}}`, no `name` field. claude-haiku-4-5-20251001 is
  explicitly listed as supported.
- Strict tool fallback: `strict: true` plus `additionalProperties: false`
  and `required` on `input_schema`; forced via top-level
  `tool_choice: {"type": "tool", "name": "..."}`; result read from the
  `tool_use` block's `.input`.
- Prompt caching: `cache_control: {"type": "ephemeral"}` (or with
  `ttl: "1h"`), placeable on image blocks. Minimum cacheable prefix for
  Haiku 4.5 confirmed 4,096 tokens (matches SPEC.md's existing claim).
  Usage fields: cache_creation_input_tokens, cache_read_input_tokens,
  input_tokens (uncached remainder only, not the total).
- Message Batches API: `POST /v1/messages/batches`,
  `{"requests": [{"custom_id", "params"}]}`; poll `processing_status`
  until "ended"; stream results from `results_url`; results arrive in
  any order, keyed by custom_id; `result.type` in
  succeeded/errored/canceled/expired.
- Web fetch, model-support finding that diverges from an implicit
  SPEC.md assumption: the dynamic-filtering tool versions
  (web_fetch_20260209 and later) are documented to support Fable 5,
  Opus 4.8, Mythos 5/Preview, Opus 4.7, Opus 4.6, Sonnet 5, and Sonnet
  4.6 only. claude-haiku-4-5-20251001, the pinned default model, is not
  on that list. extract.ts and the harness therefore use the basic
  web_fetch_20250910 tool (GA, no beta header) for the URL pass, not a
  _202602xx variant. Also flagging: structured outputs
  (output_config.format) is documented incompatible with citations
  (returns 400), so citations stay off on the web_fetch tool; SPEC.md
  does not mention this interaction.

### Manifest (files touched)

- src/extract.ts: created. Provider interface (ExtractionProvider) plus
  AnthropicExtractionProvider, calling the Messages API directly via
  fetch (no new npm dependency; package.json out of scope). Both output
  paths implemented and reachable: json_schema (primary, default) and
  strict_tool (fallback), selected by a real constructor parameter, not
  described-only. Identical image-first, cache_control-on-image message
  shape shared by runIndex and runDetails. runUrl's strict_tool mode
  runs as two calls (fetch, then a forced-tool follow-up), since forcing
  a single tool via tool_choice precludes also calling web_fetch in the
  same turn; this two-call shape is this session's inferred design,
  flagged since SPEC.md does not address the interaction. Model pinned
  from env.MODEL (default claude-haiku-4-5-20251001); max_tokens
  pinned per endpoint (2048/2048/8192), never client-supplied. Returns
  and logs cache_creation_input_tokens/cache_read_input_tokens on every
  call. Real imports of the four shared/prompts/*.md files and three
  shared/schema/*.json files (see Amendment). tsc --noEmit passes clean
  (four .md imports carry a documented @ts-expect-error each, since this
  TypeScript version, 7.0.2, only accepts wildcard/ambient module
  declarations from a file with no top-level import/export of its own,
  i.e. a separate .d.ts, which is out of scope; this has no effect on
  wrangler's esbuild bundle, which does not run tsc).
- evals/run_evals.py: run_pipeline_for_menu implemented (was
  NotImplementedError), mirroring extract.ts's request shapes via shared
  _index_params/_details_params/_url_params builders. Per-photo pipeline
  (index, details in batches of 8 with batch 1 solo to warm cache, one
  reconcile retry, unknown-flagged never-dropped misses) plus multi-photo
  fuzzy merge/dedupe (photoIndex:n, name match >= 85 AND compatible
  price, keep richer ingredients, union notes), matching SPEC.md's rules
  exactly. --batch routed through _run_pipeline_for_menu_batch (two or
  three Message Batches jobs: index, details, retry), written in full
  and verified against the installed anthropic SDK's actual types
  (caught and fixed a wrong Request import path during review; Request
  is a TypedDict, so plain dict literals are used instead), reachable
  only via --batch, never invoked this session. --url-smoke wired to a
  real cmd_url_smoke gated on a new --urls flag; genuinely inert with no
  --urls given (prints guidance, touches no network). write_report gained
  a call_usages parameter, a per-call-kind cache write/read table, and
  the named "cache check (details calls 2+)" bug-check line. Added
  url_schema to SharedAssets (was missing entirely). Also fixed one
  stale line in cmd_check()'s final print (referenced "Phase 1" as
  future work; now accurate). `uv run evals/run_evals.py --check` passes
  green, scoring self-test PASS, zero API calls made.
- shared/schema/url.schema.json: added top-level
  `"restaurant_name": {"type": ["string", "null"]}`, not required.
- shared/prompts/url-task.md: added a restaurant_name bullet to the
  top-level-fields list, mirroring index-task.md's phrasing (literally
  printed on the fetched page, else null).
- shared/aliases.json: flipped `"bonito flake": "katsuo bushi"` to
  `"katsuo bushi": "bonito flake"` (resolving the direction flagged in
  the prior session's findings); added `"anago": "eel"` and
  `"mayo sauce": "mayo"`. 10 entries total; validated with
  python3 -m json.tool.
- docs/SPEC.md: one sentence in the /api/extract/url section extended to
  name the nullable restaurant_name field in the combined schema
  description.
- wrangler.jsonc: added a `rules` entry (see Amendment). No other field
  changed.
- docs/BUILDLOG.md: this entry appended.

### Verification

- `uv run evals/run_evals.py --check`: exit 0, "scoring self-test: PASS",
  zero API calls (confirmed by design: --check never imports a network
  path in its own control flow, and no ANTHROPIC_API_KEY-consuming call
  appears in the shell history this session).
- `python3 -m json.tool` on shared/aliases.json and
  shared/schema/url.schema.json: both parse.
- `npx tsc --noEmit`: exit 0 across the whole src/ tree.
- `npx wrangler deploy --dry-run --outdir <tmp>`: exit 0, no
  authentication prompt, no deploy. This bundles src/worker.ts (the
  actual entry point) plus the new wrangler.jsonc rules block
  successfully, but does not exercise extract.ts's new .md/.json
  imports, since extract.ts is not wired into worker.ts's router this
  session (out of scope). To verify that specifically: a standalone,
  config-file-free `esbuild src/extract.ts --bundle --loader:.md=text`
  (the exact loader type the new wrangler rule specifies) succeeded,
  exit 0, and the resulting bundle was confirmed to contain the real
  system.md content inlined, not a placeholder or unresolved import.
- Confirmed no `--menu`, `--all`, `--repeat`, `--batch`, or
  `--url-smoke` invocation occurred anywhere this session, and no
  Anthropic API call was made.

### Findings for Tom (report-only, no edits made)

- Web fetch tool version: SPEC.md's /api/extract/url section says to
  "verify the current web fetch tool name, beta header, and parameters
  against live docs at build time" without naming a version. Live docs
  this session show the newer dynamic-filtering variants
  (web_fetch_20260209+) do not list Haiku 4.5 as a supported model.
  Implemented using the basic web_fetch_20250910 (GA, no beta header)
  for the pinned default model. If MODEL is ever escalated to a
  dynamic-filtering-supported model, this choice should be revisited.
- Structured outputs plus citations: output_config.format is documented
  incompatible with citations (400 error). SPEC.md's URL pass
  description doesn't mention this; citations are left off on the
  web_fetch tool in both extract.ts and the harness. Worth a note in
  SPEC.md if citations are ever wanted on fetched URL content.
- runUrl's strict_tool fallback mode is a two-call design (let web_fetch
  resolve, then force the extraction tool on a follow-up turn), since a
  single forced tool_choice cannot also permit calling web_fetch. This
  is this session's own design, not specified anywhere in SPEC.md.
  Reasonable and doc-consistent, but untested against a live response
  since no API calls were made; worth extra scrutiny on the first real
  --url-smoke run.
- The eval harness's --batch path (Message Batches API) is written in
  full, type-verified against the installed anthropic SDK (0.119.0), but
  has never executed. First invocation should be treated as a fresh
  integration test, not an assumed-working path, since batch semantics
  (async, arrive-in-any-order results) are easy to get subtly wrong
  without a live run to check against.
- extract.ts is not wired into src/worker.ts's router this session
  (worker.ts wasn't in the authorized files list). The next session that
  touches worker.ts should import createExtractionProvider from
  extract.ts rather than reconstructing request logic inline.

### Patterns established

- Python (harness) and TypeScript (extract.ts) independently mirror the
  same Anthropic request shapes since there is no cross-language code
  sharing in this repo; changes to one must be manually mirrored to the
  other. A future session could add a lightweight fixture-based test
  that diffs the two languages' constructed request bodies for a fixed
  input, to catch drift automatically.
- When a TypeScript file needs to import a file type Wrangler's bundler
  doesn't support by default (here, .md), the fix is a wrangler.jsonc
  "rules" entry, not a workaround in the .ts file; but tsc itself still
  needs either a companion .d.ts with wildcard ambient module
  declarations, or a per-import `@ts-expect-error` if a new file is out
  of scope. Wrangler's esbuild bundle never runs tsc, so the choice
  between the two only affects standalone `tsc --noEmit` runs, not the
  actual deploy.
- Build-only verification of a bundler-dependent design decision (like
  the .md import rule) doesn't require wiring the new code into the
  live entry point: a standalone esbuild invocation with the same loader
  flags is a legitimate, config-free way to test the mechanism in
  isolation.

### Single next action

The human spend gate: a single index-only probe on km-sushi-sashimi
(`uv run evals/run_evals.py --menu km-sushi-sashimi`, which will also
run the details pass and reconcile per the pipeline as implemented; a
true index-only probe would need a smaller, separate invocation this
session did not build, since it wasn't in scope), pending Tom's
explicit go. This is the first live signal on whether extract.ts's
request shapes and the shared prompts/schemas actually produce valid,
schema-conformant, accurate output.

## Session 2026-07-23: T-1.12 iteration r1, name-matching fixes over 5a59f68

Base commit: 5a59f68 (Probe report: infrastructure validated, name
matching issues identified)

### Authorized scope (verbatim)

SCOPE
Task: T-1.12 iteration, round 1. Fix the two name-matching issues
  surfaced by the 2026-07-23-probe report.
Files:
  - shared/prompts/system.md (primary, add naming rules)
  - shared/prompts/index-task.md (if index-pass naming guidance needed)
  - shared/prompts/details-task.md (if details-pass guidance needed)
Not touching: extract.ts, run_evals.py, schemas, goldens, aliases.json
Dependencies: probe report evals/reports/2026-07-23-probe.md (read for
  context)
Done when:
  1. system.md instructs the model to use the primary English name
     only, placing parenthetical Japanese/alternate names in notes.
  2. system.md instructs the model that description lines under combo
     or set items are part of that item (notes or ingredients), not
     separate items.
  3. uv run evals/run_evals.py --menu km-sushi-sashimi --timestamp
     2026-07-23-r1 shows improved recall and precision on this menu.
  4. Commit the prompt change and the new report together.
Priority: name-convention rules only; do not tune other aspects yet.

### Pre-flight

1. Working tree clean at 5a59f68. Pass.
2. The three named prompt files all present and readable. Pass.
3. Probe report evals/reports/2026-07-23-probe.md present, read for
   context (item_recall 0.50, item_precision 0.40, both failing the
   0.97 gate; ingredient_f1_macro and price_accuracy both 1.00). Pass.

### Root cause (read-only investigation, verified against source)

Two distinct causes behind the probe's 15 pred vs. 12 gold on
km-sushi-sashimi, both confirmed by tracing evals/run_evals.py:

- Parentheticals left in `name` (`TUNA BELLY (MAGURO TORO)`, `SPANISH
  MACKEREL (AJI)`, `LIVE-SWEET SHRIMP (AMAEBI)`, `SPECIAL A (20PCS)`).
  `normalize_name` in run_evals.py only lowercases and collapses
  whitespace, no parenthetical stripping, and `match_items` requires
  `token_sort_ratio >= 85`; a trailing parenthetical is enough to drop
  a true match below threshold, so the dish counts as both a MISSED
  golden and an EXTRA predicted item.
- Combo contents lines (the "3pcs Each of Assorted Sashimi w/..." text
  under Special A/B/C) emitted as their own items instead of folded
  into the named item above them, per the golden's shape.
- Architectural constraint that shaped the fix: `_merge_details_into_index`
  in run_evals.py takes `name` from the index pass only, overwriting
  just ingredients/wrap/is_raw/notes from the details pass. The index
  schema has no `notes` field. So the parenthetical must be dropped in
  the index pass and can only be recorded in the details pass's notes;
  this drove where each instruction was placed in the fix below.

### Manifest (files touched)

- shared/prompts/system.md: added a new "Item names" section (after
  "Reading the photo", before "Ingredient naming") instructing that
  `name` is the primary English name only, with parenthetical
  Japanese/alternate names and piece-count qualifiers dropped and moved
  to notes, plus the reasoning about the evaluation set's name-match
  threshold. Augmented "Combo and choice-set items" with a paragraph
  stating that a contents/description line printed beneath a named
  combo or set item is part of that item, not a separate item, and
  must never get its own `n`.
- shared/prompts/index-task.md: replaced the `name` bullet (was "the
  item name as printed", which directly contradicted the fix) with the
  primary-English-name instruction; added a sentence to the reading
  guidance that a combo/set description line underneath an item is
  part of that item, not a separate entry.
- shared/prompts/details-task.md: extended the `notes` bullet to state
  that notes is also where the parenthetical alternate name and the
  combo contents line (pulled out of `name` and out of the index pass)
  get recorded; added a one-line clarifier to the `name` bullet not to
  re-add a parenthetical.
- evals/reports/2026-07-23-r1.md: new eval report from this session's
  verification run.
- docs/BUILDLOG.md: this entry appended.

### Verification

- Confirmed via grep: zero em dashes across all three edited prompt
  files.
- Re-read all three files in full for internal consistency (each task
  file's bullets reference the style guide section they draw from; the
  index/details split is stated consistently in both directions).
- Ran (credit-spend gate confirmed with Tom first, via AskUserQuestion,
  before executing): `uv run evals/run_evals.py --menu km-sushi-sashimi
  --timestamp 2026-07-23-r1`. Result, evals/reports/2026-07-23-r1.md:
  - item_recall: 0.50 to 1.00 (gate >= 0.97, PASS)
  - item_precision: 0.40 to 1.00 (gate >= 0.97, PASS)
  - price_accuracy: 1.00, unchanged (PASS)
  - pred/gold item counts: 15/12 to 12/12, exact match
  - ingredient_f1_macro: 1.00 to 0.7946 (gate >= 0.90, now FAILS; see
    Findings below, not fixed this session, out of scope)
  - overall GATES line: FAIL (solely on the ingredient gate above; every
    gate this task's Done-when list named is met)

### Findings for Tom (report-only, no edits made)

- ingredient_f1_macro regressed from 1.00 (probe) to 0.7946 (this run),
  now failing its 0.90 gate. This is not a regression this session's
  edits caused directly: it is newly visible because the five items now
  correctly matching (Special A, Special B, Special C, Japanese Sea
  Bream, Live-Sweet Shrimp) previously scored no ingredient F1 at all
  (they were unmatched in the probe, so their ingredient sets were never
  compared). Two distinct pre-existing gaps are exposed, per the new
  run's diffs:
  - `ebi` is predicted where gold says `shrimp` (Special A, B, C all
    show this exact missing/extra pair). This looks like an
    aliases.json gap (no `ebi` to `shrimp` entry), which this round's
    scope explicitly excludes from editing.
  - `japanese sea bream` and `live-sweet shrimp` are predicted where
    gold says `sea bream` and `sweet shrimp` (the item's own printed
    species/state qualifier is not being stripped from the ingredient
    the way system.md's existing rules strip other qualifiers). This
    looks like a system.md ingredient-naming rule gap, distinct from
    the naming-convention fix this round was scoped to, and from the
    "species qualifiers stay local to the item" rule already in the
    style guide (that rule is about not importing a qualifier from a
    different item, not about stripping the item's own printed one).
  Per this round's Priority line ("name-convention rules only; do not
  tune other aspects yet") and the Not-touching list (aliases.json,
  schemas), neither was touched this session. Flagging both as
  candidates for the next iteration round, pending Tom's prioritization
  and an explicit go on which one (or both) to take on next, and on
  whether the fix belongs in aliases.json, system.md, or both.

### Patterns established

- In this repo's two-pass extraction pipeline, `name` is fixed by the
  index pass and never overwritten by the details pass merge; any fix
  that changes what ends up in the final `name` must be made in
  index-task.md's instructions (and system.md's shared rule), not
  details-task.md, even though details-task.md is where `notes` (a
  details-only field) gets populated. A naming-convention fix that
  needs both a name change and a notes addition necessarily touches
  both task files plus system.md.
- Fixing item-count/name-matching gates can expose previously-invisible
  ingredient-content gaps, since ingredient F1 is only ever computed on
  matched pairs: a matching fix and an ingredient-accuracy fix are not
  independent from the gate's perspective, even though they are
  independent from a scope perspective. Expect this pattern again on
  future name-matching rounds against other menus.

### Single next action

Tom's prioritization call on the newly-exposed ingredient_f1_macro
failure (0.7946, gate >= 0.90): whether to run a round 2 iteration now
on the `ebi` to `shrimp` alias gap and the sea-bream/sweet-shrimp
species-qualifier-stripping gap identified above, or hold this menu at
its current recall/precision win and prioritize a different menu or
task next.

## Session 2026-07-23: T-1.12 iteration r2, ingredient fixes over 15f9d8f

Base commit: 15f9d8f (T-1.12 r1: fix item name matching on
parentheticals and combo sub-lines)

### Authorized scope (verbatim)

SCOPE
Task: T-1.12 iteration, round 2. Fix the two ingredient gaps surfaced
  by the 2026-07-23-r1 report on km-sushi-sashimi (ingredient_f1_macro
  0.7946, gate >= 0.90).
Files:
  - shared/aliases.json (add ebi -> shrimp alias)
  - shared/prompts/system.md (add rule: strip an item's own printed
    qualifier from its ingredients, e.g. "japanese sea bream" -> "sea
    bream", "live-sweet shrimp" -> "sweet shrimp"; this is separate
    from the existing "don't import qualifiers from other items" rule)
Not touching: extract.ts, run_evals.py, schemas, goldens, task files
Dependencies: round 1 report evals/reports/2026-07-23-r1.md
Done when:
  1. aliases.json includes ebi -> shrimp.
  2. system.md has the own-qualifier stripping rule.
  3. uv run evals/run_evals.py --menu km-sushi-sashimi --timestamp
     2026-07-23-r2 shows ingredient_f1_macro >= 0.90.
  4. Commit aliases + prompt change + report together.
Priority: these two ingredient fixes only; do not tune other aspects.

### Pre-flight

1. Working tree clean at 15f9d8f. Pass.
2. shared/aliases.json and shared/prompts/system.md both present and
   readable. Pass.
3. Round 1 report evals/reports/2026-07-23-r1.md present, read for
   context (ingredient_f1_macro 0.7946, gate >= 0.90 FAIL; two named
   gaps: ebi/shrimp on Special A/B/C, own-qualifier stripping on
   Japanese Sea Bream and Live-Sweet Shrimp). Pass.

### Manifest (files touched)

- shared/aliases.json: added `"ebi": "shrimp"` (11 entries total).
- shared/prompts/system.md: added one new bolded paragraph in
  "Ingredient naming", immediately after the existing "Species and type
  qualifiers stay local to the item that prints them" paragraph. States
  the complementary rule: an item's own printed name qualifier (a
  nationality like "japanese", a liveness marker like "live") strips
  from that item's ingredient even though it stays in the item name,
  with a guard sentence that this applies only to the item's own name,
  not to a qualifier printed on an ingredient inside a combo's contents
  line (so it does not license stripping "japanese scallop" on Special
  B's contents line).
- evals/reports/2026-07-23-r2.md: new eval report from this session's
  verification run.
- docs/BUILDLOG.md: this entry appended.

### Verification

- Ran (credit spend pre-authorized in the approved plan for this
  session, per the standing spend-gate rule): `uv run evals/run_evals.py
  --menu km-sushi-sashimi --timestamp 2026-07-23-r2`. Result,
  evals/reports/2026-07-23-r2.md:
  - ingredient_f1_macro: 0.7946 to 0.9745 (gate >= 0.90, PASS)
  - item_recall, item_precision, price_accuracy: 1.00, unchanged (PASS)
  - overall GATES line: PASS
  - Japanese Sea Bream and Live-Sweet Shrimp diffs fully cleared (zero
    diff lines for either item this run); the own-qualifier stripping
    rule worked as intended.
  - Special A, B, C still show `missing=['shrimp']` this run, but with
    `extra=[]` rather than r1's `extra=['ebi']`: the model did not emit
    `ebi` or `shrimp` for these items' shrimp component at all this run.
    Since the alias table only converts whatever the model outputs, and
    system.md's shrimp-related wording did not change this session, this
    reads as ordinary sampling variance between runs, not an effect of
    either fix. Flagged as unverified inference, not confirmed by a
    repeat run (out of scope this session).
  - Special B's residual `scallop` vs. gold `japanese scallop` diff
    (flagged as a known, out-of-scope residual in the r1 findings)
    persists unchanged.

### Findings for Tom (report-only, no edits made)

- Special A/B/C's `missing=['shrimp']` diff this run has a different
  shape than r1's (no `extra=['ebi']` companion), suggesting the model
  dropped the shrimp ingredient outright rather than mislabeling it.
  This did not block the gate (macro F1 lands at 0.9745), so it was not
  chased further per this round's ingredient-fixes-only priority, but a
  repeat run would help distinguish genuine sampling variance from a
  systematic gap worth a future round.
- Special B's `scallop`/`japanese scallop` residual (predicted strips
  "japanese", gold keeps it) is a miss against the existing "species
  qualifiers stay local" rule, not the two rules touched this round.
  Left unfixed per scope; still the most likely next single-menu
  ingredient target if further iteration on km-sushi-sashimi is wanted.

### Patterns established

- The own-qualifier-stripping rule's guard sentence (limiting the new
  rule to an item's own printed name, not to ingredients named on a
  combo's contents line) was necessary and appears to have worked: the
  residual Special B diff did not get worse by the new rule being
  over-applied to "japanese scallop" in its contents line.
- Per-run model sampling variance is visible even with an unchanged
  prompt for the affected ingredient (the ebi/shrimp component on
  Special A/B/C emitted differently between r1 and r2 despite no prompt
  change targeting it). Treat a single eval run's diff detail as one
  sample, not a deterministic characterization of the prompt, when
  reasoning about anything the round's own fix did not target.

### Single next action

Tom's call on whether to spend a further round on the two residuals
surfaced above (Special B's scallop qualifier, and confirming whether
the Special A/B/C shrimp-drop is sampling noise or systematic), run the
eval suite against other menus now that this menu's ingredient gate
passes, or move to a different T-1.x task.

## Session 2026-07-24: T-1.12 iteration r3, universal prompt fixes over b51350e

Base commit: b51350e (T-1.12 r2: fix ebi/shrimp alias and own-qualifier
ingredient stripping)

### Authorized scope (verbatim)

SCOPE
Task: T-1.12 iteration, round 3. Universal prompt fixes from the
  2026-07-23-all-r1 full-suite run. Only fixes that would be wrong on
  ANY restaurant's menu. Restaurant-specific tuning deferred per R-8.
Files:
  - shared/prompts/system.md (primary: 3 rule additions/refinements)
  - shared/prompts/index-task.md (parenthetical rule refinement)
  - shared/aliases.json (one spelling-only alias)
Not touching: extract.ts, run_evals.py, schemas, goldens,
  details-task.md
Dependencies: full-suite report evals/reports/2026-07-23-all-r1.md
Done when:
  1. Parenthetical rule refined: strip Japanese alternate names and
     standalone piece counts; KEEP parentheticals that disambiguate
     otherwise-identical item names (e.g. "Sushi Combo (9pcs Sushi +
     Roll)" stays intact because another item is also called "Sushi
     Combo"). Update both system.md and index-task.md.
  2. system.md has a combo pricing rule: when a printed price covers
     multiple items in a set (e.g. "2 for 17.50"), price is null and
     price_text carries the verbatim text. Upcharge modifiers like
     "+1" or "+2" also get price null with price_text carrying the
     modifier.
  3. Prep method stripping reinforced in system.md with concrete
     examples from the diffs: "deep fried soft shell crab" -> "soft
     shell crab", "chopped spicy salmon" -> "spicy salmon", "sauteed
     steak" -> "steak", "sliced jalapeno" -> "jalapeno", "baked
     salmon" -> "salmon". Reference the existing exception list
     (pickle, fried garlic, fried onion).
  4. aliases.json: add "soy bean" -> "soybean" (spelling fix only).
  5. uv run evals/run_evals.py --all --timestamp 2026-07-24-r3 runs
     and the report is committed with the changes.
  6. The report includes a note: "Single-restaurant golden set (KUU
     SUSHI). Further iteration deferred pending dataset broadening
     (R-8, A-1)."
Priority: these four universal fixes only. Do not chase ingredient
  completeness gaps, meaning-level aliases, or OCR misread patterns.
  If new diffs surface, report them, do not fix them.

### Clarification (asked before writing, plan mode)

The scoped report note says "Single-restaurant golden set (KUU
SUSHI)," but the golden set actually spans two restaurant-name
prefixes (km-sushi-*, 8 menus; kuu-sushi-happy-hour, 1 menu), confirmed
by both `--check`'s menu listing and direct inspection. Asked Tom via
AskUserQuestion whether to write the note verbatim as scoped or correct
it to match the data; Tom chose verbatim. Written exactly as scoped
(see Verification); flagged again here and in Findings for the record.

### Pre-flight

1. Working tree clean at b51350e except the pre-existing untracked
   evals/reports/2026-07-23-all-r1.md (present since before this
   session; not in this session's files list, left untouched). Pass.
2. `uv run evals/run_evals.py --check`: shared assets load, 9 menus
   discovered (8 km-sushi-*, 1 kuu-sushi-happy-hour), scoring self-test
   PASS, ANTHROPIC_API_KEY present. Pass.
3. Read all four named files (system.md, index-task.md, aliases.json,
   the r1 report) plus details-task.md and run_evals.py for scoring
   mechanics, to ground each fix in exactly the diff evidence cited in
   scope. Pass.

### Manifest (files touched)

- shared/prompts/system.md: three additions. (1) Item names section:
  a new paragraph stating the parenthetical-disambiguation exception,
  using the scoped Sushi Combo example, with a guard that it fires
  only on an actual same-menu name collision, not whenever a
  parenthetical looks descriptive. (2) Price fields section: replaced
  the vague combo-price sentence with an explicit rule (shared-set
  price and upcharge-only modifiers both get `price: null` with the
  verbatim text in `price_text`; never split or estimate a per-item
  number). (3) Preparation methods paragraph: added the five scoped
  worked examples (deep fried soft shell crab, chopped spicy salmon,
  sauteed steak, sliced jalapeno, baked salmon), framed as
  illustrations of the existing rule and exception list, not a new
  rule.
- shared/prompts/index-task.md: mirrored the parenthetical
  disambiguation exception in the `name` bullet, one sentence,
  referencing the style guide.
- shared/aliases.json: added `"soy bean": "soybean"` (12 entries
  total). Did not add edamame -> soybean (meaning-level, deferred per
  scope).
- evals/reports/2026-07-24-r3.md: new eval report from this session's
  verification run, with the scoped note inserted verbatim after the
  model line.
- docs/BUILDLOG.md: this entry appended.

### Verification

- `uv run evals/run_evals.py --check` re-run after all four edits:
  shared assets still load (system.md 20384 to 22491 chars, aliases 11
  to 12 entries), self-test PASS.
- Ran (spend gate confirmed by Tom approving the plan with the spend
  step explicit, per the standing intervention/spend-gate rule):
  `uv run evals/run_evals.py --all --timestamp 2026-07-24-r3`. Result,
  evals/reports/2026-07-24-r3.md:
  - All four gates still FAIL: item_recall 0.7613 (was 0.7883),
    item_precision 0.6842 (was 0.7353), ingredient_f1_macro 0.7157
    (was 0.6986), price_accuracy 0.8166 (was 0.8400). Expected: this
    was a targeted universal-fix round against a single-restaurant
    golden set, not a gate-passing round (per the scoped report note
    and R-8/A-1).
  - Fix 4 (soy bean spelling alias) confirmed working: on
    km-sushi-hot-appetizer-salad, the soy bean/soybean mismatch is
    gone from Garlic Soy Beans, Spicy Soy Beans, and plain Soy Beans
    (present in r1's diffs, absent from r3's). kuu-sushi-happy-hour's
    Edamame/Garlic Edamame/Spicy Edamame still show the mismatch, as
    expected (a different, meaning-level alias, correctly out of
    scope).
  - Fix 3 (prep-method examples) partially confirmed: Deep Fried Soft
    Shell Crab, Baked Salmon, and Crazy Horse no longer show their
    prep-word-prefixed ingredient as an extra (the exact behavior the
    fix targeted). But one of the scope's own named examples did not
    take: km-sushi's Gyumori/kuu-sushi-happy-hour still shows
    `extra=['crab meat', 'sauteed steak', ...]`, the identical
    "sauteed steak" case named in scope item 3, unresolved this run.
  - Fix 2 (combo/upcharge pricing) partially confirmed: on
    km-sushi-lunch, items whose only printed price is an upcharge
    modifier (Salmon Teriyaki, Steak Teriyaki, Assorted Sashimi)
    changed from a numeric price with a plain-number price_text in
    prior rounds to `price: null` with the verbatim modifier
    (`'ADD$2'`, `'ADD$1'`) this run, matching the new rule's intent.
    But plain "2 for 17.50" items with no modifier on the same menu
    (Chicken Teriyaki, Garlic Chicken, Sesame Chicken, Spicy Chicken,
    Vegetable Tempura, Lemon Shrimp, California Roll, Spicy Tuna Roll,
    Vegetable Roll, Mixed Tempura) still emit a numeric price
    unchanged from r1, and km-sushi-dinner's combo-priced items now
    show `price_text: None` rather than the expected verbatim "2 for
    23.00". See Findings for the likely cause.
  - Fix 1 (parenthetical disambiguation) did not resolve its target
    case. See Findings: the fix's own premise does not hold in the
    actual golden data.

### Findings for Tom (report-only, no further edits made)

- **Design-level, escalating rather than patching further**: Fix 1's
  evidence, both in this round's scope and in the original r1 report,
  describes km-sushi-dinner's "Sushi Combo (9pcs Sushi + Roll)" and
  "Sushi & Sashimi Combo (5pcs Sushi + 6pcs Sashimi + Roll)" as
  colliding with another same-named item after parenthetical
  stripping. Read evals/menus/km-sushi-dinner/golden.json directly to
  confirm: there is no second "Sushi Combo" or "Sushi & Sashimi Combo"
  item on this menu. Each combo name is unique even before stripping.
  So the disambiguation exception, as scoped and as implemented
  (fires only on an actual same-menu name collision), never triggers
  for this example, and this run's diff confirms it: both items are
  still MISSED, with a bare "Sushi Combo" and "Sushi & Sashimi Combo"
  still predicted as EXTRA. The real defect is different from what was
  scoped: the golden set's canonical name for a combo item includes
  its contents/piece-count parenthetical even with no collision,
  while the general parenthetical-stripping rule (unchanged from r1)
  still strips it for combo items same as any other item. Fixing that
  would mean broadening the exception from "collision-only" to
  "combo/set items with a contents-describing parenthetical always
  keep it," a materially different and broader rule than what was
  authorized this round. Not implemented; escalating for a deliberate
  decision rather than expanding scope unilaterally.
- The report note ("Single-restaurant golden set (KUU SUSHI)") is
  committed verbatim per Tom's explicit confirmation this session,
  though the scored set spans km-sushi (8 menus) and kuu-sushi (1
  menu). Recorded here for anyone reading the report cold.
- Fix 2's partial adoption (upcharge-only items changed behavior,
  plain "2 for X" items did not) is plausibly a menu-layout signal
  gap rather than a wording gap: items with an explicit per-row "+1"/
  "+2" marker gave the model an unambiguous per-item cue to null out;
  items sharing an unmarked "2 for 17.50" banner price may print that
  number directly on their own row with no per-item "shared" marker,
  so the model has no textual signal distinguishing "this item's own
  price" from "the section's shared price" without reading the section
  layout as a whole. Not re-worded further this session (would be
  iterating past the single scoped attempt); worth a targeted look at
  the actual photo if a future round takes this back up.
- Fix 3's one confirmed miss (Gyumori's "sauteed steak") is the exact
  example named in scope, unresolved despite the added worked example.
  Given only one sample per condition, this could be ordinary sampling
  variance (as flagged in the r2 entry above) rather than the fix
  failing to register; not chased further this round per the "report,
  do not fix" priority line.
- Aggregate gate deltas versus r1 are mixed and mostly small (item
  recall/precision/price down a few points, ingredient F1 up a couple
  points), against a backdrop of large, fix-unrelated per-run swings
  already visible in km-sushi-dinner, km-sushi-noodles-kitchen, and
  km-sushi-special-rolls (wildly different sets of invented combo/roll
  items each run, unrelated to any of the four fixes). Consistent with
  the sampling-variance pattern already noted in the r2 entry; a
  single `--all` run cannot separate real regression from noise. A
  `--repeat` consistency run would be needed to say more, and was not
  in this round's scope.

### Patterns established

- When a scope item's evidence cites "another item is also called X,"
  verify that claim against the actual golden.json before implementing
  the fix it justifies, not just against the diff report's MISSED/
  EXTRA lines. The diff report shows a name-match failure but not why
  it failed; this round's Fix 1 evidence read correctly from the r1
  diffs alone but was wrong once checked against the underlying data,
  and the fix as scoped could not have worked regardless of wording.
- A narrowly-scoped prompt fix (collision-only exception, upcharge-
  only null pricing) can partially generalize to unscoped-but-similar
  cases inconsistently, exposing what textual signal the model
  actually keyed on (an explicit per-item "+N" marker) versus what the
  rule's prose implied it should key on (any shared-set pricing). This
  is useful information for wording a broader version of the rule
  later, distinct from a bug in this round's wording.

### Single next action

Tom's call on the two escalated design-level items: (1) whether to
broaden the parenthetical-disambiguation exception to cover any combo/
set item with a contents-describing parenthetical, not just an actual
name collision, and (2) whether the "2 for X" combo-price rule needs a
follow-up pass informed by looking at the actual menu photo layout
rather than another prose-only prompt iteration. Also open: whether to
run `--repeat` on one or two menus to separate real signal from
sampling noise before further prompt iteration.

## Session 2026-07-25: T-1.12 iteration r4, parenthetical rule broadened over b9e4d12

Base commit: b9e4d12 (T-1.12 r3: universal prompt fixes from all-r1
full-suite run)

### Authorized scope (chat-authorized, not a pasted SCOPE block)

Tom answered the r3 closing report's three escalated open items
directly in chat:
1. Broaden the parenthetical rule: "combo items always keep their
   contents parenthetical" is still a universal fix, not
   restaurant-specific; r3's collision-only implementation was wrong,
   not the underlying idea. Authorized one more targeted round to fix
   it correctly.
2. Skip the menu-photo inspection for Fix 2's residual "2 for X"
   pricing gap; noted it may resolve once combo items start matching
   under item 1's fix, not worth a separate round on its own.
3. Skip `--repeat`; sampling-variance measurement isn't the best use
   of budget before the golden set broadens past one restaurant (R-8).
Treated as this round's scope: files touched limited to
shared/prompts/system.md and shared/prompts/index-task.md (same
footprint as r3, corrected content), verified with targeted single-
menu runs rather than a full `--all` spend, mirroring item 3's
cost-consciousness.

### Pre-flight

1. Working tree clean at b9e4d12. Pass.
2. Read the actual golden.json for every one of the 9 menus (not just
   km-sushi-dinner) to find every item whose gold `name` contains a
   parenthetical, before writing the broadened rule: confirmed only
   the same two km-sushi-dinner combo items ("Sushi Combo (9pcs Sushi
   + Roll)", "Sushi & Sashimi Combo (5pcs Sushi + 6pcs Sashimi +
   Roll)") have one anywhere in the golden set, so the broadened rule
   cannot regress any other menu's data. Pass.
3. Checked km-sushi-sashimi's Special A/B/C (also combo/set items,
   used as this doc's own hypothetical "Special A (20pcs)" stripping
   example) against their real golden data: their contents are printed
   on a separate description line and land in `notes`, with zero
   parenthetical in the golden `name` at all. Confirms the new rule's
   distinction (inline contents parenthetical vs. separate description
   line) does not create an internal contradiction with that existing
   example. Pass.
4. `uv run evals/run_evals.py --check`: assets load, self-test PASS.
   Pass.

### Manifest (files touched)

- shared/prompts/system.md: replaced r3's collision-only exception
  paragraph in the Item names section. New criterion: a combo or set
  item (per the Combo and choice-set items section: multiple food
  components bundled under one printed name and price) keeps its
  contents-describing parenthetical in `name` whenever the menu prints
  it directly after the item's own name, as a property of the item
  type, not a per-menu collision coincidence. A Japanese alternate name
  or a bare piece/size count on a single, non-combo dish still strips
  as before.
- shared/prompts/index-task.md: mirrored the same broadened exception
  in the `name` bullet.
- evals/reports/2026-07-25-r4-dinner.md: new, targeted single-menu
  verification run on km-sushi-dinner (the menu with the two
  parenthetical-bearing combo items).
- evals/reports/2026-07-25-r4-lunch.md: new, targeted single-menu
  verification run on km-sushi-lunch (checks Tom's hypothesis that
  Fix 2's residual pricing gap resolves incidentally).
- docs/BUILDLOG.md: this entry appended.

### Verification

- `uv run evals/run_evals.py --check` re-run after edits: assets load
  (system.md 22491 to 22860 chars), self-test PASS.
- Spend gate: flagged the two targeted single-menu runs explicitly
  before firing (progress-check note in chat), consistent with the
  standing intervention/spend-gate rule; proceeded given Tom's
  round-opening authorization plus the explicit flag.
- `uv run evals/run_evals.py --menu km-sushi-dinner --timestamp
  2026-07-25-r4-dinner` ($0.0374): **fix did not resolve the target
  case.** Both "Sushi Combo (9pcs Sushi + Roll)" and "Sushi & Sashimi
  Combo (5pcs Sushi + 6pcs Sashimi + Roll)" are still MISSED golden
  items; a bare "Sushi Combo" (no parenthetical) is still predicted as
  EXTRA, plus a new "Sashimi Combo" EXTRA that doesn't even match the
  gold's "Sushi & Sashimi Combo" wording. Identical failure signature
  to both r1 and r3. This run's overall extraction on this menu was
  also unusually noisy: 29 predicted vs. 18 gold items, item_recall
  0.1667 (worse than r1's 0.278 and r3's 0.333), with many fabricated
  extras unrelated to any of this project's four fixes (Boston Roll,
  Yellowtail Jalapeño Roll, Daikon Radish, Ginger Root, Pickled
  Radish, Oshinko Takuwan). See Findings.
- `uv run evals/run_evals.py --menu km-sushi-lunch --timestamp
  2026-07-25-r4-lunch` ($0.0420): item_recall 0.9474, consistent with
  prior rounds (this menu has no parenthetical-bearing gold items, so
  it does not directly test Fix 1). Tom's hypothesis that Fix 2's
  residual pricing gap would resolve once combo items start matching:
  **not confirmed.** All ten "2 for 17.50" plain numeric-price
  mismatches (Chicken Teriyaki, Garlic Chicken, Sesame Chicken, Spicy
  Chicken, Vegetable Tempura, Lemon Shrimp, California Roll, Spicy
  Tuna Roll, Vegetable Roll, Mixed Tempura) are byte-for-byte unchanged
  from r3's diff. The three upcharge-only items (Salmon Teriyaki,
  Steak Teriyaki, Assorted Sashimi: null price plus verbatim 'ADD$1'/
  'ADD$2') held steady across r3 and r4, confirming that half of Fix 2
  is stable, not a one-off.

### Findings for Tom (report-only, no further edits made)

- **Escalating rather than attempting a third wording iteration**:
  this is now three runs (r1, r3, r4) and two structurally different
  prompt-wording attempts (r3's collision-only test, r4's item-type
  test, the latter verified against the real golden data first) that
  have all failed identically on the same two combo items. Per this
  project's own pattern-recognition rule, a recurring fix should be
  upgraded, not iterated on with more prose. Not attempting a third
  wording variant unilaterally; flagging for a deliberate decision on
  whether prose-only prompt engineering is the right lever here at
  all, versus (for example) a concrete few-shot example embedded in
  the prompt, or accepting this as a known single-restaurant-menu
  limitation and prioritizing R-8/A-1 dataset broadening instead, since
  a second restaurant's combo-naming conventions may look nothing like
  this one's.
- km-sushi-dinner's own-menu extraction quality looks unstable across
  rounds independent of any of the four fixes (item_recall 0.278 in
  r1, 0.333 in r3, 0.167 in r4, with a different, mostly nonoverlapping
  set of hallucinated extra items each time). This menu's photo was
  never flagged in the original consistency-gate visual inspection
  (2026-07-22 BUILDLOG entry) as one of the harder photos, but its
  results are the worst and most volatile in every full-suite report
  to date. Worth a direct visual check of this specific photo before
  investing further prompt effort aimed at it specifically, since a
  hard-to-read source photo would explain volatility no amount of
  prompt wording can fix.
- Tooling gap noticed while trying to diagnose the Fix 1 failure: the
  eval harness reports only name-level diffs (MISSED/EXTRA/mismatch
  summaries), not the raw per-call model JSON. There's no way from the
  committed report alone to tell whether the model dropped the
  parenthetical outright, moved it to `notes` instead of `name`, or
  never recognized the item as a combo at all. A future harness change
  to optionally dump raw predicted JSON per run (behind a flag, so it
  doesn't bloat every report) would make this kind of failure much
  faster to diagnose. Not built this session (out of the two-file
  scope authorized).
- Fix 2's upcharge-only branch (null price, verbatim "+N" text) is
  confirmed stable across two independent runs (r3, r4) with identical
  results; treating that half of the fix as solid, distinct from the
  still-unresolved plain "2 for X" branch.

### Patterns established

- Before broadening a prompt rule's trigger condition, grep every
  golden.json for the literal pattern the new condition is meant to
  catch (here, any parenthetical in a gold `name`), not just the one
  menu named in the evidence. This caught that the rule's other
  cited-in-doc example ("Special A (20pcs)") never actually occurs in
  the real data, avoiding a wasted worry about internal contradiction
  and confirming the broadened rule is a strict, safe widening with
  zero blast radius on the other 8 menus' scoring.
- Two consecutive prompt-wording attempts failing identically on the
  same target, even when the second attempt is verified correct against
  the underlying data (unlike the first), is itself a signal: the
  lever being pulled (prose instruction wording) may not be the
  effective one for this behavior on this model, independent of
  whether the wording is "correct." Recurrence across independently-
  reasoned attempts outweighs confidence in any single attempt's
  internal logic.

### Single next action

Tom's call on: (1) whether to try a structurally different lever for
the combo-parenthetical case (e.g., a literal few-shot example in
system.md) instead of a third prose-only iteration, or accept it as a
known gap pending R-8 dataset broadening; (2) whether a direct visual
check of km-sushi-dinner's source photo is worth doing before any
further prompt investment aimed at that menu, given its volatility
looks independent of any of the four fixes; and (3) whether the
harness is worth extending with an optional raw-JSON dump for faster
future diagnosis.

## Session 2026-08-02: masa-sushi golden intake and raw/ reorganization over 7cc1c5e

Base commit: 7cc1c5e (Restaurant 2 raw photos: paper order sheet, 2
images)

### Authorized scope (verbatim build card)

Commit the already-staged masa-sushi golden and the 14 staged raw/
renames exactly as staged: no add, remove, restage, or reformat of
any kind, no `git add -A`. This is the only unit permitted to run
before any README, SPEC, or sweep edit. Zero spend: no eval run, no
model call, for this or any unit of the session.

### Pre-flight

1. `git rev-parse --short HEAD` prints 7cc1c5e. Pass.
2. `git status --porcelain`: one `A` line for
   evals/menus/masa-sushi/golden.json, exactly 14 `R` lines (12 into
   evals/menus/raw/kuu-sushi/, 2 into evals/menus/masa-sushi/photos/),
   nothing else. Pass.
3. Staged golden is `A`, not `AM`: `git diff --stat` against the
   staged path returns empty, confirming no unstaged delta and a
   determinate commit. Pass.
4. Per the session's baseline note, the two commits already on top
   of 439398e (490deef, 7cc1c5e) are pre-reconciled by oversight and
   get no retrospective entry here and no finding. The 3-line diff
   inside the staged golden itself (notes at n:11 Calamari Leg, n:13
   Soft Shell Crab, n:17 Salmon Collar, lowercased to "inferred prep
   (...)") is Tom applying the INFERRED-token-scope decision directly.
   It is Tom-verified ground truth and ships as staged, unexamined
   further by this session.

### Manifest (files touched)

- evals/menus/masa-sushi/golden.json: new, staged prior to this
  session. 133 items, 8 sections (Appetizers, Sushi & Sashimi,
  Traditional Roll, New House Special Roll, Fresh Roll, Baked Roll,
  Tempura Roll, Simple Roll), restaurant_name "Masa Sushi",
  source_photos IMG_3498 and IMG_3499. Drafted zero-spend and
  human-verified by Tom on 2026-07-27. Tom's review found 11 real
  errors, of which the drafter's own confidence flags caught 2; that
  gap is what drove the lint issue (RAID I-4).
- evals/menus/masa-sushi/photos/1.jpeg, 2.jpeg: renamed from
  evals/menus/raw/restaurant-2/IMG_3498.jpeg and IMG_3499.jpeg. Photo
  order confirmed by Tom, with 1.jpeg as the front page.
- evals/menus/raw/kuu-sushi/IMG_3433.jpeg through IMG_3444.jpeg (12
  files): renamed from evals/menus/raw/ directly, as part of the
  same reorganization, separating KUU's raw provenance photos from
  the flat raw/ drop folder.
- docs/BUILDLOG.md: this entry appended.

### Verification

- `git show --stat HEAD` after the commit: 16 paths total, exactly
  the golden, the 14 renames (12 KUU, 2 masa), and this BUILDLOG
  entry. No phantom paths.
- `git status --porcelain` after the commit: empty.
- No API call made for this unit. Spend: $0.

### Findings for Tom (report-only, no edits made)

None for this unit. The staged content was reviewed only for shape
(item count, section count, photo count, rename count) against the
build card's stated figures and the staged index itself, which it
matches; content correctness of the golden itself is Tom's trust
gate per the build card and was not re-examined.

### Patterns established

- Committing an already-staged, already-reviewed tree as its own
  first unit, before any same-session edit touches other files,
  keeps that commit's diff provably equal to exactly what was staged
  going in. Verified after the fact with `git show --stat` against
  the pre-flight's own porcelain listing, rather than trusted from
  the add step alone.
- Count every rename from the staged index (`git status --porcelain`,
  `git show --stat`), never from a doc's descriptive prose. A first
  draft of this entry took the KUU photo count from
  evals/menus/README.md's "10-page spiral menu" description and wrote
  10 renamed files; the actual figure is 12, because the reorganization
  also moves the 2 happy-hour photos (IMG_3438, IMG_3439) that the
  README describes as a separate artifact. The doc's page count and
  the reorganization's file count answer different questions.

### Single next action

None outstanding for this unit. Sessions B and C are unblocked once
this commit lands; the remaining units of this session (README
convention propagation, SPEC line 58, KUU wrap sweep) proceed
independently and land in a second commit.

## Session 2026-08-02: ten locked conventions into README, SPEC line 58, KUU wrap sweep over 8f36da3

Base commit: 8f36da3 (this session's own commit 1)

### Authorized scope (verbatim build card)

Edit evals/menus/README.md to carry ten locked conventions (four of
them amendments to standing text, edited in place, not duplicated);
correct docs/SPEC.md line 58 (one line, photo path extensions); and
run a read-only specialty-wrap sweep across the nine KUU golden.json
files (not masa-sushi), reporting findings without editing any
golden. Explicitly out of scope: shared/aliases.json (owned by
session C), shared/prompts/system.md (mirrored by session C),
evals/run_evals.py (owned by session B), any golden.json content, and
the price sort key (a render-time T-2.5 implementation detail, noted
here only). Zero spend for this unit as for the whole session.

### Pre-flight

1. evals/menus/README.md (129 lines) and docs/SPEC.md exist. SPEC.md
   line 58 read verbatim before edit: `menus/<slug>/photos/1.jpg
   (ordered, one or more per menu)`. Pass.
2. evals/run_evals.py:214 read to confirm the harness's accepted
   photo extensions before writing the SPEC fix: `{".jpg", ".jpeg",
   ".png"}`. Pass.
3. No API call required for README/SPEC edits or for the sweep (pure
   file read and grep/parse over already-committed golden.json data).
   Pass.

### Manifest (files touched)

- evals/menus/README.md: all ten conventions added. Amendments in
  place (superseded wording removed, not left standing): the
  prep-strip exception list closed at seven members (pickle, mayo,
  fried garlic, fried onion, tempura, smoked, cajun; conventions 2
  and 3); the wrap-field bullet no longer claims the wrapper is never
  an ingredient, and now also names the wrapper in `ingredients` when
  `wrap` is `none` (convention 4); the species-qualifier bullet now
  points to a newly stated alias-direction governing principle
  (convention 10), with anatomical parts (convention 9) added as its
  own bullet immediately before it. New bullets: dual-name rows
  (convention 1), the crispy-rice carve-out folded into the existing
  rice bullet (convention 5), conditional ingredients (convention 6),
  small-choice-sets-included stated explicitly alongside the existing
  combo bullet (convention 7), and INFERRED token scope, ingredient-
  only, with the itemized vs. whole-list form distinction (convention
  8) folded into the existing INFERRED bullet. Verified by grep that
  neither superseded string ("currently: pickle, mayo, fried garlic,
  fried onion" nor "the wrapper is never an ingredient") remains
  anywhere in the file.
- evals/menus/README.md: separately, at the reviewer's request mid-
  session, personal-name references were replaced with "the reviewer"
  throughout this file (the repo is a public portfolio artifact and
  this file is mirrored into system.md, where a personal name has no
  referent for the model). One line was explicitly kept unchanged at
  the reviewer's instruction (the LOCKED header's attribution line).
  Not touched by this rename, per explicit scope: docs/BUILDLOG.md
  (this file, an append-only governance log where the named reviewer
  is the point), any golden.json, shared/prompts/system.md, and the
  rest of docs/. Occurrence counts at time of check, unedited:
  docs/EVALS.md 2, docs/HANDOFF.md 7, docs/DEPLOY.md 2, docs/SPEC.md
  5, docs/BUILDLOG.md 34 (pre-existing, before this entry),
  shared/prompts/system.md 1, and three golden.json files (km-sushi-
  hot-appetizer-salad, km-sushi-special-rolls, masa-sushi) contain a
  personal-name reference; left as-is, golden content is the
  reviewer's own trust gate.
- docs/SPEC.md: line 58 only, rewritten to `menus/<slug>/photos/1.
  {jpg,jpeg,png} (ordered, one or more per menu)`, matching the three
  extensions run_evals.py:214 actually accepts. No other line
  touched.
- docs/BUILDLOG.md: this entry appended.
- No golden.json anywhere was modified by this unit.

### Verification

- `git diff` on docs/SPEC.md shows exactly one changed line.
- Grep confirms both superseded README strings are gone and the
  renamed-conventions' cross-references (wrap bullet to convention 4,
  species-qualifier bullet to the alias-direction bullet) resolve to
  text that exists in the file.
- No API call made for this unit. Spend: $0.

### KUU specialty-wrap sweep (read-only, zero golden files modified)

Scope: the nine KUU goldens (the eight km-sushi-* slugs plus kuu-
sushi-happy-hour). masa-sushi excluded. Total items measured directly
from each golden.json: 222 (this session's build card stated 232;
222 is the measured figure and is what this sweep is based on. Card-
asserted vs. measured discrepancy noted here, not corrected in the
card itself, which is out of scope to edit).

Per the reviewer's scope tightening mid-session: `wrap == "none"` is
the correct value for all nigiri and sashimi items, so that value
alone is not a candidate signal. Two sets were built instead:

- CANDIDATES: every item whose name or notes contain a wrapper-
  suggesting token (cucumber, naruto, wrap, wrapped, paper, soy
  paper, tofu skin, inari, no rice), regardless of wrap value. 12
  items. Full detail (slug, n, name, wrap, ingredients, notes,
  assessment) is in this session's closing report, not duplicated
  here since BUILDLOG is append-only and ships public with the repo.
  Headline finding: of the 12, only 4 are genuine convention-4
  specialty-wrap cases (km-sushi-nigiri n=21 Bean Curd/inari; km-
  sushi-special-rolls n=33 Tiffany, n=38 OMG, n=43 House Cucumber),
  and in all four the wrapper is already present in that item's
  `ingredients` array. Convention 4, applied to the existing KUU
  goldens, indicates zero golden edits across all nine files. The
  remaining 8 hits are token false positives: cucumber as a filling
  or salad ingredient, or cucumber appearing only inside a large
  choice-set list in `notes`, not as a chosen or physical wrap.
  Also assessed against convention 5 (not a wrapper-token hit, pulled
  in separately): km-sushi-special-rolls n=40 Crispy Rice Cake
  currently has no "crispy rice" ingredient entry at all (its
  `ingredients` array holds only "spicy tuna"; the rice preparation
  is described in `notes` prose, not the convention's exact term).
  Flagged for the reviewer's adjudication, not edited.
- ROSTER: every other `wrap == "none"` item, one compact line each
  (slug, n, name only), proving full coverage with no item skipped.
  128 items. Full roster is in the closing report only. Counts by
  slug only, recorded here: km-sushi-cold-appetizer 8, km-sushi-
  dinner 15, km-sushi-hot-appetizer-salad 17, km-sushi-lunch 13,
  km-sushi-nigiri 19, km-sushi-noodles-kitchen 15, km-sushi-sashimi
  12, km-sushi-special-rolls 2, kuu-sushi-happy-hour 27 (sums to 128).

Zero golden.json files were changed by this sweep. All adjudication
and any resulting edits are the reviewer's.

### Findings for Tom (report-only, no further edits made)

- Convention 4 applied to the nine existing KUU goldens changes
  nothing: every genuine specialty-wrap item already names its
  wrapper in `ingredients`. No backfill pass is needed for this
  convention specifically.
- km-sushi-special-rolls n=40 Crispy Rice Cake is a live candidate
  for convention 5 (the crispy-rice carve-out): "crispy rice" is not
  currently in its `ingredients` array. Reviewer's call whether to
  add it.
- Forward note, not actioned: the price sort key is a render-time
  derived key belonging in filters.js (not yet built, T-2.5), per
  explicit build-card scope. It does not appear in README or any
  prompt asset and should not until T-2.5.
- This session's build card stated 232 KUU items; the measured total
  from the nine golden.json files is 222. Left unresolved, since
  reconciling it is outside this unit's edit scope (no card or README
  edit was authorized for that count).

### Patterns established

- When a scan token can match on both structural fields (wrap) and
  free-text fields (name, notes), false positives from the free-text
  side dominate a small sweep. Splitting into "genuine candidates
  after reading full context" vs. "roster proving coverage" keeps the
  reviewer's adjudication list short without hiding the completeness
  proof.
- A convention that says "add X" can, once checked against real data,
  turn out to already be satisfied everywhere it applies. Reporting
  that as a headline finding (zero edits needed) is more useful to
  the reviewer than silently confirming each item one by one.

### Single next action

Reviewer's call on: (1) whether to add "crispy rice" to km-sushi-
special-rolls n=40's ingredients per convention 5; (2) whether the
232-vs-222 KUU item count discrepancy in the build card is worth
reconciling, and where; (3) whether the personal-name-to-"the
reviewer" rename should extend to any of the other docs/ files or
shared/prompts/system.md, flagged here for session C since system.md
is outside this session's Files list.

## Session 2026-08-05: P1-SB continuation after transport failure, over b6f36cf

Base commit: b6f36cfa03869afcb6e15e539fb8725d0036822a (unchanged; nothing
was committed by the prior session)

### Transport failure and inheritance re-proof (card-mandated)

A prior session working this same build card died mid-turn on a connection
failure. Nothing was committed. Its uncommitted work (a 725-line addition to
`evals/run_evals.py` and a new `evals/accepted_vocabulary.json`) was left on
disk in the working tree. Per this session's binding inheritance rule, that
prior session's account of what it completed was treated as unreliable and
not cited; every item below was re-proven inside this session with command
output, not read off the plan file's claims.

### Authorized scope (verbatim build card)

Zero spend, no API calls, no network. Re-prove the pre-flight and the
inherited lint code (asserts A through G, T3-1, T3-2), then finish four
proofs the prior session never produced (T3-2 byte-identical, raw drop
folder order, synthetic 1/2/10 case, exit code 1), investigate and explain
an assert F delta without changing assert F, write two doc sections
(`evals/menus/README.md` sidecar/vocabulary conventions, `docs/EVALS.md`
harness lint section), write this BUILDLOG entry, and commit (never push).
Not touching: any `golden.json`, `shared/*`, `normalize_ingredient` and all
scoring/matching/merge/dedupe/gate logic, `src/*`, `docs/SPEC.md`,
`PLAN.yaml`, `.dev.vars`, `.envrc`, wrangler config, existing
`evals/reports/*`. No environment variable unset, exported, or modified
beyond the single mandated `env -u ANTHROPIC_API_KEY` invocation.

Three amendments were authorized mid-session, after the plan was approved
and before any doc text was written, folded in below as amendments 6-8
alongside the five amendments the prior session's plan had already recorded
(1-5, reconfirmed against the code on disk, not re-litigated).

### Pre-flight (all five re-run this session, command output produced, not cited)

1. `git rev-parse HEAD` = `b6f36cfa03869afcb6e15e539fb8725d0036822a`. Pass.
2. `git status --porcelain`: exactly ` M evals/run_evals.py` and
   `?? evals/accepted_vocabulary.json`. `git diff --stat` confirms
   `1 file changed, 725 insertions(+), 7 deletions(-)`. No `golden.json`
   modified, no `sections.json` under `evals/menus/` anywhere. Pass.
3. Inherited lint code read in full (`evals/run_evals.py` lines 196-744 and
   1439-1656) before any change was made. Pass.
4. `_lint_self_test` (lines 1537-1655) read line by line: every assert A
   through G has at least one negative fixture, and the two amended asserts
   (D, G) additionally carry a positive regression guard. **The PASS line's
   claim was TRUE as inherited; no fixture was missing.** See closing report
   item 7 for the full per-assert table.
5. `find` swept for scratch/fixture directories inside the repo: none found
   beyond the pre-existing, gitignored `evals/__pycache__/`. Pass.

### Manifest (files touched)

- `evals/run_evals.py`: inherited from the prior session's uncommitted work,
  re-proven this session, **unchanged by this session** (no proof failed, so
  no code edit was needed).
- `evals/accepted_vocabulary.json`: inherited, unchanged, 153 verbatim
  ingredient strings, sorted, deduped, with the amendment-3 `_comment`.
- `evals/menus/README.md`: new `## Sidecar and vocabulary conventions`
  section added before `## Status`.
- `docs/EVALS.md`: `## Harness (evals/run_evals.py)` extended with a new
  `### Offline golden lint (--check)` subsection.
- `docs/BUILDLOG.md`: this entry.

### Card amendments 1 through 5 (from the prior session's plan, verbatim,
reconfirmed against the code on disk this session, not re-litigated)

**Amendment 1, assert G.** Original card wording: "wrap values are inside
the enum, and is_raw is boolean." Amended: `is_raw` in `{true, false,
null}`, where `null` carries the README meaning "not determinable" and is
valid. Cause: card-asserted as *card defect caught in plan mode*, the
original would ERROR on three correct, human-verified goldens
(`km-sushi-lunch` n:4, `masa-sushi` n:9, n:10). Confirmed implemented at
`_composed_item_schema` (`is_raw` typed `["boolean", "null"]`) with a
regression guard in `_lint_self_test` at line 1652 (`is_raw=None` must not
fire).

**Amendment 2, assert F.** Original: "Romaji present on items in Sushi and
Sashimi sections." Amended: WARN, never ERROR, never gating; detect romaji
across `name` AND `notes`, case insensitive, accepting both the structured
`romaji: X` form and bare prose; WARN when absent, reported per menu not
per item. Cause: card-asserted, no locked convention exists for how romaji
is recorded and the goldens use three different forms. Confirmed
implemented at `_assert_f_romaji` (lines 651-680) and `ROMAJI_LEXICON`
(line 280).

**Amendment 3, vocabulary file stores raw strings.** Original mandate: seed
`accepted_vocabulary.json` through `normalize_ingredient`. Amended: the
file stores 153 verbatim ingredient strings, sorted, deduped, unnormalized
at write time; assert E normalizes both the ingredient under test and each
vocabulary entry at lookup time. Cause: card-asserted, `normalize_ingredient`'s
plural fold turns `asparagus` into `asparagu` and `octopus` into `octopu`;
committing folded forms into a reviewer artifact would look like a
golden-set defect when it is a `normalize_ingredient` defect. Confirmed
implemented at `load_accepted_vocabulary` (line 308) and `_assert_e_vocabulary`
(line 634); confirmed by direct call this session,
`normalize_ingredient("asparagus", {})` -> `"asparagu"`,
`normalize_ingredient("octopus", {})` -> `"octopu"`.

**Amendment 4, assert D null price is WARN not ERROR.** Amended: when
`price` is null, parse `price_text` for a single unambiguous number; if
found, WARN (never ERROR). Cause: card-asserted, correct goldens legitimately
carry a null `price` with a combo or market-price `price_text`. Measured
this session (`uv run --no-project python`, direct scan of all 10
`golden.json`): **54 items** carry `price: null`
(`km-sushi-dinner` 15, `km-sushi-lunch` 15, `km-sushi-noodles-kitchen` 1,
`km-sushi-sashimi` 4, `masa-sushi` 19). Of those 54, **0** have a
`price_text` with exactly one parseable number (combo rows embed two
numbers, market-price rows embed zero). The WARN sub-condition is
implemented and self-tested (line 1614) but fires 0 times against the real
goldens; both facts (54-item population, 0-firing sub-condition) are
reported, not conflated.

**Amendment 5, assert D adjacent-equal reports runs, not items.** Amended:
collapse consecutive equal prices within a section into runs; report
length-2 runs (the carry-down/transposition suspect) first, length-3+ runs
after as informational. Cause: card-asserted, one line per pair over-reports
a real price tier as N-1 separate suspicious pairs. Measured this session
(same direct scan): **27 pair-runs** and **3 longer runs** (`masa-sushi`
`Traditional Roll` n:58-60 length 3, `Fresh Roll` n:78-81 length 4,
`Baked Roll` n:96-99 length 4). Coverage check: 27x1 + (3-1)+(4-1)+(4-1) =
27+8 = **35**, matching the original per-pair count exactly, confirming the
run-collapse changes presentation, not coverage.

**T3-1 constraint, recursive sort determinism.** `_photo_sort_key` keys on
the stem alone, correct for one `photos/` directory but not for the
recursive `raw/` walk (two files in different subdirectories could key
identically and fall back to filesystem order). Fix: `_raw_photo_sort_key`
keys on `(str(parent), *_photo_sort_key(p))`. Confirmed implemented at line
217, used at `cmd_check` line 1475; `_photo_sort_key` itself (single
directory) is unaffected.

### Amendments 6 through 8 (this session, authorized mid-session before any
doc text was written)

**Amendment 6, assert F's lexicon and detector are a NAMED FINDING, not
fixed.** The sashimi delta investigation (below) surfaced two distinct
detector failures:

- Under-reporting: `km-sushi-sashimi` n:1, 2, 3 (Special A/B/C) detect as
  "has romaji" only because the lexicon term `ebi` appears inside a count
  phrase describing a platter component (`"...assorted sashimi with 2
  ebi"`), not the item's own romaji name. The detector cannot distinguish
  an item's own romaji from a romaji term appearing incidentally in a
  component list.
- Over-reporting: `km-sushi-sashimi` n:10 (Japanese Sea Bream) genuinely
  gives its romaji inline in `notes` (`"Tai; seasonal, market price"`,
  the same pattern as n:9/11/12's `Maguro`/`Aji`/`Amaebi`), but `tai` is
  not in `ROMAJI_LEXICON`, so it counts as missing when it is not.
- Swept the rest of the applicable population (all four menus) for any
  other lexicon term present in the data but absent from `ROMAJI_LEXICON`:
  none found. Every `masa-sushi` structured `romaji: X` field's `X` is
  already in the lexicon (the lexicon's own comment states it was built
  from these goldens). `tai` is the one confirmed absence.
- **Consequence, stated explicitly: the shipped 30 is a LOWER BOUND on
  items missing their own romaji, not a measurement of it.**
- **Not fixed, deliberately.** Assert F is a survey feeding a romaji
  convention decision that has not been made; expanding the lexicon or the
  detector now would bias the survey toward whichever terms a fixer
  happened to think of. Reported to oversight, not resolved in this diff.

**Amendment 7, applicable-item population stated per menu.** Missing over
applicable, all four menus with a Sushi or Sashimi section, reproduced this
session via `env -u ANTHROPIC_API_KEY uv run evals/run_evals.py --check`:

| Menu | Missing / Applicable | n (missing) |
|---|---|---|
| km-sushi-nigiri | 16/23 | 1,2,3,4,5,6,7,8,9,10,12,14,15,16,20,23 |
| km-sushi-sashimi | 6/12 | 4,5,6,7,8,10 |
| kuu-sushi-happy-hour | 7/7 | 8,9,10,11,12,13,14 |
| masa-sushi | 1/26 | 34 |

**Amendment 8, section-matching substring is a stated limitation.**
Confirmed by reading `_assert_f_romaji` (lines 666-667): the match is
`section = it.get("section") or ""` then `"sushi" not in section.lower()
and "sashimi" not in section.lower()`. The `slug` parameter is used only
inside the returned `LintFinding` for labeling; it never enters the match
condition. Confirmed: the match is against the `section` field only, never
the slug or menu name. Empirically, across all 10 menus' distinct section
names, the substring match fires on exactly `Sushi`, `Sushi & Sashimi`,
`Premium Sushi`, `H.H Sushi Sampler`, `Sashimi`, `Sashimi Special`,
`Premium Sashimi`, `H.H Sashimi`, all correct for this survey.
**Limitation, reported not fixed:** the match is substring, not exact-set;
a future section whose name merely contains "sushi" or "sashimi" (for
example a hypothetical "Sushi Bar Sides" with no actual sushi) would be
swept into the applicable population with no reviewer signal that it
happened.

### Proofs produced this session (command output, not cited from the plan)

1. **Baseline reproduction.** `env -u ANTHROPIC_API_KEY uv run
   evals/run_evals.py --check`: 10 menus discovered, 355 items
   (8+18+18+19+41+15+12+43+48+133, confirmed by direct sum), 0 ERROR / 34
   WARN / 20 SKIP, exit 0. `--check --menu masa-sushi`: exactly 1 menu
   linted (20 WARN, 2 SKIP for that menu alone), exit 0.
2. **T3-2 byte-identical proof.** Mandated method: a scratchpad script
   outside the repo (`/tmp/.../scratchpad/t3_2_proof.py`), read-only glob
   over the real `evals/menus/*/photos/`, comparing bare `sorted(paths)`
   (the pre-fix behavior) against `sorted(paths, key=_photo_sort_key)` per
   menu. No `git stash`, no `git checkout`, no repo mutation. Result: all
   10 menus identical (every current stem is a single digit or `1.jpeg`/
   `2.jpeg`, so lexicographic and natural order coincide today; the fix
   changes future behavior, not today's).
3. **Raw drop folder order.** Scratchpad script
   (`t3_1_and_synthetic.py`), read-only glob over the real
   `evals/menus/raw/`: 12 files, all under `raw/kuu-sushi/`, `IMG_3433.jpeg`
   through `IMG_3444.jpeg` in that order, each keying to
   `(".../raw/kuu-sushi", 1, 0, "img_34xx")`, proving directory-qualified
   determinism.
4. **Synthetic 1/2/10 case.** Same scratchpad script, throwaway temp files,
   no repo file touched: bare `sorted()` gives `1.jpg, 10.jpg, 2.jpg`;
   `_photo_sort_key` gives `1.jpg, 2.jpg, 10.jpg`.
5. **Exit code 1.** Scratchpad script (`exit_code_1_proof.py`), `uv run`
   with the same PEP 723 header as `run_evals.py`, imports the shipped
   module and builds a synthetic menu (photos/ + golden.json with one
   deliberate assert-A ERROR) in a temp directory, points the module's
   `MENUS_DIR` at it in memory only (restored after), and calls the real
   `cmd_check()`. Result: 1 ERROR / 0 WARN / 2 SKIP, returned exit code 1.
   No repo golden used; `MENUS_DIR` restored, no trace left on disk.
6. `git diff --stat -- evals/menus/*/golden.json`: empty. Zero goldens
   modified.
7. `find evals/menus -name sections.json`: empty. All 10 menus SKIP assert
   C, zero sidecars committed.

### Assert F delta: both numbers, and the cause

Shipped, this session: **30** missing (nigiri 16, sashimi **6**, happy-hour
7, masa 1). The prior session's plan's read-only dry run predicted **36**
(nigiri 16, sashimi **12**, happy-hour 7, masa 1). Assert F was **not**
changed to make the numbers match.

Established this session, item by item, from `km-sushi-sashimi/golden.json`:
six of the twelve applicable sashimi items detect romaji, all from `notes`
prose: n:1/2/3 via `ebi` (inside a component-count phrase, see amendment 6),
n:9 via `maguro`+`toro`, n:11 via `aji`, n:12 via `amaebi`. The other six
(n:4,5,6,7,8,10) carry no lexicon term in the shipped detector's terms
(`served with 7 pcs`), except n:10 whose romaji `Tai` is a genuine lexicon
gap (amendment 6).

Cause: five candidate detector variants were run this session against all
10 goldens (lexicon over name+notes as shipped; name only; notes only;
structured `romaji:` prefix only; structured OR name-lexicon; case-sensitive
lowercase lexicon). None reproduces the dry run's `(16, 12, 7, 1)`
simultaneously. Only the structured-prefix variants give sashimi 12, and
both of those give nigiri 22-23, not 16 (nigiri's 16 requires bare-prose
notes matching, which the structured-only variants exclude). So the dry
run's sashimi cell is inconsistent with its own nigiri cell under every
uniform detector tested this session. Tagged: the shipped **6** is
**ESTABLISHED**, verified item by item above. The dry run's **12** is
**INFERRED** to be an artifact rather than a measurement, most probably
(tagged **SPECULATIVE**, no dry-run artifact survives to confirm it) the
sashimi cell recording the menu's applicable-item count (which is exactly
12) rather than a missing-count, possibly computed before amendment 2
replaced structured-only detection with name+notes and not recomputed
alongside the other three cells. The shipped behavior stands as correct;
this session did not change assert F.

### Findings for Tom (report-only, no further edits made)

- Assert G's negative fixture was **not missing**. The prior session's PASS
  line claim ("one negative fixture per assert A-G") is true as inherited.
- `normalize_ingredient`'s internal order, confirmed by reading lines
  751-766: alias lookup on the raw lowercased string runs first and
  short-circuits on a hit; the plural fold runs second; a second alias
  lookup on the folded form runs third. On record ahead of session C's
  alias edits.
- `normalize_ingredient`'s plural fold turns `asparagus` into `asparagu`
  and `octopus` into `octopu` (confirmed by direct call this session).
  Reported, not fixed: scoring logic, out of this session's scope.
- Assert F's detector and lexicon are incomplete in two distinct,
  documented ways (amendment 6); the shipped WARN count of 30 is a lower
  bound, not a measurement. This is a decision for oversight: whether and
  how to expand `ROMAJI_LEXICON` and disambiguate an item's own romaji
  from an incidentally-mentioned component term.
- Assert F's section match is substring, not exact-set (amendment 8);
  reported as a standing limitation for any future section naming.
- Every assert result this session (0 ERROR, 34 WARN, 20 SKIP across the
  real goldens) matched what was already observed in the card, reproduced
  independently rather than cited, except the assert F sashimi cell
  (6 vs. the card's cited ~12/36 total), explained above.

### Patterns established

- When a card's "already observed" section cites a count from a prior
  session's dry run, re-deriving it independently (multiple detector
  variants, cross-checked against a second dimension like nigiri's own
  count) is what surfaces whether the cited number is a measurement or an
  artifact. A single re-run that reproduces the total without breaking it
  into per-menu cells would have missed this.
- A completeness survey (assert F) that shares a detector with a possible
  false-positive path (a lexicon term appearing incidentally, not as the
  item's own label) needs its under-reporting and over-reporting failure
  modes named separately; averaging them into one WARN count would have
  hidden that the two errors partly cancel in the total but not per menu.

### Single next action

Oversight's call on assert F's lexicon and detector (amendment 6): whether
to expand `ROMAJI_LEXICON` (starting candidate: `tai`), and how to
disambiguate an item's own romaji from a romaji term inside a component
list, before the WARN count is used to drive any romaji-convention
decision.

---

## Session 2026-08-06: P1-SC part 1, system.md mirror, alias edits, blocked receipt

Base commit: e8f96e1

### Authorized scope (verbatim build card)

BUILD CARD: P1-SC, system.md mirror, alias edits, full-suite baseline. Mirror
the ten locked conventions from evals/menus/README.md into
shared/prompts/system.md (zero spend); three shared/aliases.json edits (zero
spend); a rule-governed reviewer rename check in system.md (zero spend); the
offline lint gate before and after (zero spend); one paid --all run (roughly
$0.45) producing an eval report with two aggregations (all 10 menus, and 9
excluding km-sushi-dinner) plus consistency recorded NOT MEASURED; one commit
of the prompt, alias, and report changes together with this entry. Not
touching: any golden.json, evals/run_evals.py, evals/menus/README.md,
ROMAJI_LEXICON and assert F, normalize_ingredient and all scoring/matching/
merge/dedupe/gate logic, evals/accepted_vocabulary.json, src/*, docs/SPEC.md,
PLAN.yaml, .dev.vars, .envrc, wrangler config.

### Pre-flight

1. `git rev-parse HEAD` and `git rev-parse origin/main` both `e8f96e1`. Pass.
2. `git status --porcelain` empty. Pass.
3. Six paths resolved by `realpath`: shared/prompts/system.md,
   shared/aliases.json, evals/menus/README.md, evals/run_evals.py,
   evals/reports/, docs/BUILDLOG.md. Pass.
4. README read in full (221 lines), ten conventions extracted verbatim before
   any system.md edit.
5. `env -u ANTHROPIC_API_KEY uv run evals/run_evals.py --check`: 10 menus,
   355 items, 0 ERROR, 34 WARN, 20 SKIP, exit 0. Matches the card's
   expectation exactly.
6. `ANTHROPIC_API_KEY` confirmed present in env by name, not value, ahead of
   the paid step.

### Amendments authorized during plan review, before execution

- **C-1**: alias edit (a), removing a `smoked salmon` to `salmon` mapping,
  is a verified no-op. No such mapping exists in shared/aliases.json to
  remove; the card anticipated one that was never there. `lox`, `nova`, and
  `smoked sake` measure zero occurrences in any golden's `ingredients` array
  (the lone `nova` substring hit is the printed item name "Casanova",
  km-sushi-special-rolls n=29). Oversight confirmed: do not add the three
  inward aliases either, since the alias direction rule requires direction
  measured from real printed data, and there is none. Step 2 shipped as two
  edits, not three.
- **C-2**: wrap accuracy is not a gate. `GATES` in evals/run_evals.py has four
  keys plus consistency; wrap is not among them, and `aggregate()` never
  touches it. Oversight confirmed: report wrap in both aggregation tables as
  an unweighted mean over menus with wrap data, annotated "(no gate,
  unweighted mean)", computed by hand from the harness's own per-menu table
  at zero extra spend. No scratchpad wrapper built.
- **C-3**: the Step 3 reviewer rename is governed by a rule, not by the
  card's cited count of one occurrence. Rule: a generic reviewer/end-user
  reference renames to "the reviewer" or "the user"; a reference genuinely
  requiring Tom specifically (golden verification, hand corrections, spend
  authorization) is kept; an ambiguous case is kept and flagged, never
  guessed. Applied to shared/prompts/system.md, the file in scope, the
  measured count was zero both before and after the Step 1 edits, so the
  disposition set is empty.
- **Rider 1** (numbering precedence): evals/menus/README.md is the source of
  truth for convention content and placement. The "convention 1" through
  "convention 10" labels used in this entry and in the c6f980d entry are
  identifiers borrowed from that prior entry's narrative for readability;
  the README itself carries no numbering on its bullets. No divergence was
  found between the borrowed labels and README bullet content this session.
- **Rider 2**: the explanation offered for the c6f980d entry's "system.md 1"
  figure (a case-insensitive grep matching the word "bottom" at
  shared/prompts/system.md:34, "top to bottom, left column...") is INFERRED,
  not established. Session A's actual command does not survive anywhere in
  the repo or this session's context; the inference rests only on "bottom"
  being the sole case-insensitive `tom` match in the file.
- **Rider 3** (this section): correcting the c6f980d figure inside this
  append-only log, not by chat report alone. The c6f980d entry's manifest
  line reads "shared/prompts/system.md 1" for the reviewer-rename occurrence
  count. Measured this session, twice (before and after the Step 1 mirror
  edits): zero. `git log -- shared/prompts/system.md` shows the file
  unchanged between 439398e and this session's edits, so the figure was
  wrong when it was written, not made stale by a later edit. Cause:
  INFERRED per Rider 2 above, not established. The c6f980d entry itself is
  not edited; this is the later correcting record.

### Manifest (files touched)

- `shared/prompts/system.md`: six edits mirroring the ten README
  conventions (two of the ten, prep-strip list expansion and general-test
  subordination, landed as one combined edit at the same paragraph).
  Verified faithful to README wording at each edit site. New paragraph in
  `## Item names` (dual-name rows). Rewrote the prep-strip exception block
  in `## Ingredient naming` from four to seven members, with the principle
  restated as rationale only and the list as what the model checks against.
  New paragraph pair after the species-qualifier block (anatomical parts;
  labeling-facing half of the alias-direction principle, aliases.json
  mechanics deliberately excluded since the model never applies aliases).
  New paragraph (conditional ingredients) before the rewritten wrap
  paragraph (specialty wraps now also name the wrapper in `ingredients`).
  New paragraph (crispy rice carve-out) after the rice paragraph. One
  appended sentence in `## Combo and choice-set items` (explicit small/large
  choice-set statement; the section was already faithful in substance).
  Two appended paragraphs in `## Inferred ingredients for undescribed
  items` (INFERRED token's ingredient-only scope; itemized vs. whole-list
  forms). PRICE SORT KEY confirmed absent before and after by grep. Zero
  em dashes introduced, confirmed by grep for U+2013/U+2014/U+2015. File
  grew 22860 to 27792 chars.
- `shared/aliases.json`: two edits. `katsuo bushi: bonito flake` flipped to
  `bonito flake: katsuo bushi` (katsuo bushi is the printed form, 1 golden
  occurrence vs. 0 for bonito flake). `anago: eel` removed (anago is
  saltwater conger, a different species from unagi; 0 golden occurrences
  either way, so the removal is zero blast radius per the alias direction
  rule). 12 entries to 11. The five card-named entries (`freshwater eel`,
  `unagi`, `tamago`, `mayo sauce`, `ebi`) confirmed untouched by direct
  read. Edit (a) recorded as a verified no-op per C-1 above.
- `shared/prompts/system.md` / Step 3: no edit. Disposition set measured
  empty (see C-3 above); reported, not silently reconciled against the
  card's cited count of one.
- `docs/BUILDLOG.md`: this entry.
- No `evals/reports/*.md` file this commit. See "Blocked receipt" below.
- No `golden.json` anywhere was modified. `git diff --stat` confirms only
  shared/prompts/system.md, shared/aliases.json, and docs/BUILDLOG.md
  changed.
- `evals/run_evals.py` not modified.

### Step 4: offline lint gate, before and after

| | Menus | Items | ERROR | WARN | SKIP | Exit |
|---|---|---|---|---|---|---|
| Pre-edit | 10 | 355 | 0 | 34 | 20 | 0 |
| Post-edit | 10 | 355 | 0 | 34 | 20 | 0 |

Zero delta in WARN or SKIP. Explained, not waved through: every WARN/SKIP in
both runs comes from assert C (missing sections.json sidecars), assert D
(adjacent-equal price pairs, a layout signal), or assert F (missing romaji),
none of which the alias edits touch. The only assert the edits could affect
is assert E (vocabulary lookup), and both edited terms have zero surface
area on the changed side: `anago` and `bonito flake` each measure zero
occurrences in any golden's `ingredients` array, and `katsuo bushi` (1
occurrence) stays in accepted_vocabulary.json as a literal string regardless
of which direction the alias table now points, since assert E re-normalizes
both the tested string and the vocabulary entry at lookup time through
`normalize_ingredient(x, aliases)`. No vocabulary entry became unreachable.

### Blocked receipt: Step 5 crashed twice, no report produced

Both attempts used the same command:
`uv run evals/run_evals.py --all --timestamp 2026-08-06-p1-sc-all`

Both raised the identical unhandled exception at the identical call site,
`_extract_json()` parsing an index-pass response inside
`_run_photo_pipeline()`:

```
Attempt 1: json.decoder.JSONDecodeError: Unterminated string starting at:
           line 1 column 4665 (char 4664)
Attempt 2: json.decoder.JSONDecodeError: Unterminated string starting at:
           line 1 column 4679 (char 4678)
```

Neither attempt reached `write_report()`; `evals/reports/` is unchanged from
before this session, and per-run token usage (`all_call_usages`) is held
only in an in-memory list in `cmd_run()` with no incremental persistence, so
whatever calls succeeded before each crash have their usage lost, not
merely unreported.

Oversight declined a third blind `--all` retry and declined single-menu
diagnostic runs (both would spend further before hardening). Zero-spend
diagnosis performed instead:

- `INDEX_MAX_TOKENS = 2048` (evals/run_evals.py:70), the cap on the call
  that crashed both times.
- Arithmetic check, UNCERTAIN (a rough heuristic, not a token count from
  the API, which was never captured): at roughly 4 characters per token for
  mixed English/JSON text, 2048 tokens is roughly 8192 characters of
  budget. Both crash points (character 4664 and 4678) fall at roughly 57%
  of that estimated budget, around 1166 to 1170 tokens by the same
  heuristic. On this arithmetic, the truncation does not obviously look
  like it hit the 2048-token ceiling; it reads more consistent with a
  transport or stream-level cutoff unrelated to the token budget, which
  has a documented precedent in this repo (e8f96e1's commit message
  references a prior run "re-proven after transport failure"). This is
  reported as the best-supported reading of the arithmetic, not as a
  confirmed cause: the harness keeps no raw-response log, so the actual
  truncated payload and its real token count are unrecoverable from either
  crashed attempt.
- Which menu or photo crashed is UNCERTAIN: `cmd_run()` prints nothing
  per-menu, only at the very end via `write_report()`, so neither crash
  left any trace of progress. INFERRED, not established: `masa-sushi` is
  the likeliest candidate. All 9 KUU menus completed the full pipeline
  without crashing in the 2026-07-23-all-r1.md report (confirmed by direct
  read: nine per-menu rows, all populated, no masa-sushi row since its
  golden did not exist yet). `masa-sushi`'s golden was added later
  (8f36da3) and has never been run through `--all` or `--menu` before this
  session; it is also the largest golden by a wide margin (133 items
  across 2 photos, versus the next largest at 48). The inference rests on
  "never run before, largest by far" as the standing risk factor, not on
  any direct evidence from either crash.
- Estimated spend across both crashed attempts: roughly $0.80 to $0.90,
  UNCERTAIN, console-pending. This is CARD-ASSERTED arithmetic (two
  attempts at the card's own ~$0.45 single-run estimate), not measured:
  the harness's own token accounting was never reached by either crash, so
  no actual figure exists in this repo to cite. The real number is
  whatever the Anthropic console shows for this window; it is not
  reconciled here.

### Deviation from the build card, explicit

The card's Step 6 specifies one commit carrying the prompt, alias, and
report changes together with this entry. That is not possible this
session: the report does not exist, because the run that would produce it
is blocked by the harness defect described above. Per oversight's explicit
instruction, this commit (part 1) ships the prompt and alias changes with
this entry alone; a future commit (part 2, under a fresh card) ships the
eval report once the harness issue is understood and a successful `--all`
run completes. The prompt change therefore lands one commit ahead of its
own eval receipt. This is named here as a deviation, not folded into the
manifest silently.

### Findings for Tom (report-only, no further edits made)

- **Harness gap 1**: the index-pass call (`_run_photo_pipeline`,
  evals/run_evals.py around line 1113) has no retry and no defensive
  handling around a malformed or truncated JSON response. The details pass
  has a one-shot domain retry for items missing after the first batch
  (`details_retry`); the index pass has nothing equivalent, and a bad
  response there is fatal to the whole `--all` run via an uncaught
  exception.
- **Harness gap 2**: `cmd_run()` accumulates `all_call_usages` only in a
  local Python list and calls `write_report()` once, at the very end.  A
  crash on menu N loses all usage and cost accounting for menus 1 through
  N-1, even though real spend was incurred for them. There is no
  incremental report or usage checkpoint.
- **Harness gap 3**: there is no raw-response logging anywhere in the
  pipeline. When `_extract_json()` fails, the malformed payload that
  caused the failure is gone; diagnosis is limited to the exception
  message and character offset, with no way to inspect what the model
  actually returned. Both crashes this session were diagnosed by
  arithmetic inference alone, not by reading the actual failing response.
- Session B (owner of evals/run_evals.py) is the appropriate owner for
  hardening any of the above; none were touched this session per explicit
  scope.

### Patterns established

- A card's spend-gate language ("no re-runs without returning to
  oversight") earns its keep exactly at a crash like this one: the second
  crash, at nearly the same character offset as the first, was the signal
  to stop treating the failure as transient and escalate instead of
  retrying a third time blind.
- When a crash prevents the harness's own accounting from ever running,
  reaching for CARD-ASSERTED arithmetic ("roughly N attempts at roughly $X
  each") and tagging it as such is more honest than a report that omits
  a cost line entirely because no measured figure exists.
- Correcting a prior append-only entry's wrong figure belongs in a later
  append-only entry (Rider 3), not only in a chat transcript that will not
  travel with the repo.

### Single next action

Oversight's call, likely as a fresh hardening card: whether to harden the
index-pass call (retry on parse failure, raw-response logging, incremental
usage persistence) before attempting Step 5 again, and whether to run a
single-menu diagnostic on `masa-sushi` first once that hardening exists, to
confirm or rule out the INFERRED culprit named above before spending on
another full `--all` attempt.

## Session 2026-08-07: P1-SB2 part 1, harness hardening and index cap (zero spend)

Base commit: a9d5fe9

### Authorized scope (verbatim build card)

BUILD CARD: P1-SB2, harness hardening + index cap, then verified
baseline. Code work is ZERO SPEND. Two spend gates inside the
session, each halting for Tom's explicit go.

BASELINE STATE: HEAD a9d5fe9, origin/main e8f96e1, exactly one
commit ahead, tree clean. Any other state: HALT, print, stop.

CAUSE STATUS, read before planning: two --all crashes at
_extract_json on an index-pass response, char 4664 and 4678. Both
candidate causes are UNCERTAIN. Do not anchor on either. Note:
the 14-char spread between crashes is the signature of a fixed
token ceiling (char offset varies slightly per generation),
while two transport cutoffs within 14 chars at 4.6KB would be
coincidence; the 4-chars-per-token arithmetic in the P1-SC entry
is a prose ratio, and JSON tokenizes denser; the cited transport
precedent was the Claude Code chat connection, a different layer
from a harness API call. The discriminator is empirical and built
into Step 3 below.

PRE-FLIGHT (halt on any failure):
1. SHAs and tree per BASELINE STATE.
2. Read the P1-SC part 1 BUILDLOG entry: both tracebacks, the
   three named harness gaps.
3. Read _extract_json and EVERY call site. Read and print EVERY
   max_tokens value in run_evals.py (index, details, any other).
4. Free gate: env -u ANTHROPIC_API_KEY uv run evals/run_evals.py
   --check. Expect 10 menus, 355 items, 0 ERROR, exit 0.

STEP 1, ZERO SPEND, harden evals/run_evals.py:
a. Defensive parse at every model-output JSON parse site: on
   JSONDecodeError, write the FULL raw response text plus metadata
   (menu slug, call type, photo, model, stop_reason, usage) to a
   crash file under evals/crash/ (add evals/crash/ to .gitignore),
   print the path, raise a clean labeled error naming menu and
   call type. No silent recovery. No new auto-retries beyond the
   existing details_retry.
b. stop_reason on every call is recorded. If a parse SUCCEEDS but
   stop_reason is max_tokens, that menu FAILS with a named error:
   silently scoring truncated output is worse than crashing.
c. Incremental usage persistence: append one JSONL line per API
   call (timestamp, slug, call type, token counts) as calls
   complete, so a crash never again loses accounting. Final report
   aggregation unchanged.
d. Per-menu progress: one stdout line at each menu start and
   completion (slug, calls, running cost), so failures localize.
e. Raise the index call max_tokens from 2048 to 8192. Print the
   details cap and compute worst-case details output headroom on
   the largest batch (masa); if worst case exceeds half that cap,
   raise it to 8192 too and report.
f. Offline self-test for the new crash path: synthetic truncated
   JSON in a temp location proves the crash file is written and
   the labeled error raised. Never a repo golden, never a real
   API call.
SCORING NEUTRALITY IS A HARD CONSTRAINT: no change to scoring,
matching, merge, dedupe, gates, or normalize_ingredient. State
explicitly in the report that no metric-computing code path
changed. --check totals must be identical before and after.

STEP 2: COMMIT 1: run_evals.py, .gitignore, BUILDLOG hardening
entry. Do not push.

STEP 3, SPEND GATE 1, HALT for Tom's explicit go (~$0.10-0.15):
uv run evals/run_evals.py --menu masa-sushi --timestamp
2026-08-06-p1-sb2-diag-masa
[Step 3 and Step 4 not yet run; see "Status at commit 1" below.]

NOT TOUCHING: any golden.json (zero edits, report only),
shared/prompts/*, shared/aliases.json, shared/schema/*,
evals/menus/README.md, evals/accepted_vocabulary.json,
ROMAJI_LEXICON and assert F, all scoring/matching/merge/dedupe/
gate logic, normalize_ingredient, src/*, docs/SPEC.md, PLAN.yaml,
.dev.vars, .envrc, wrangler config.

### Amendments authorized during plan review, before execution

Three open questions were put to Tom via AskUserQuestion before writing the
plan file, all three answers taken as-is, no silent interpretation:

- **A-1** (details cap): the card's rule raises `DETAILS_MAX_TOKENS` only if
  the largest batch's worst case exceeds half the cap. A normal 8-item
  details batch measures 1911 chars on masa (does not trigger the rule by
  itself), but the one-shot `details_retry` call is unbounded, all
  still-missing items of a photo in a single call, and its worst case on
  masa is roughly 12000 chars, well over half the old 2048-token cap. Tom's
  call: raise `DETAILS_MAX_TOKENS` to 8192 alongside `INDEX_MAX_TOKENS`,
  reasoning that a raised ceiling costs nothing unless the model actually
  generates more, and the retry path's hazard is real even though the
  literal batch-size case does not trigger the rule's letter.
- **A-2** (truncation handling): a call that parses successfully but carries
  `stop_reason == "max_tokens"` aborts the whole run, the same as a parse
  crash, rather than failing only that menu and continuing the rest. Chosen
  for symmetry with the existing crash path and because it keeps scoring
  neutrality trivially provable (no new path into report assembly or the
  aggregation input set).
- **A-3** (usage JSONL location): `evals/usage/<stem>.jsonl`, gitignored,
  parallel to `evals/crash/`. The committed report stays the record of note;
  the JSONL is a local run artifact reconciled into the BUILDLOG prose at
  commit 2, not shipped in git.

### Pre-flight

1. `git rev-parse HEAD` and `git rev-parse origin/main`: `a9d5fe9` and
   `e8f96e1`. `git rev-list --left-right --count origin/main...HEAD`: `0	1`
   (0 behind, 1 ahead). `git status --porcelain` empty. Pass, matches
   BASELINE STATE exactly.
2. P1-SC part 1 BUILDLOG entry read in full: both tracebacks (char 4664 and
   4678, both `Unterminated string starting at` inside `_extract_json`
   parsing an index-pass response), and the three named harness gaps (no
   defensive parse/crash capture, no incremental usage persistence, no
   per-menu progress).
3. `_extract_json` and every call site read. `max_tokens` values, ESTABLISHED
   by direct read before any edit:

   | Constant | Line (pre-edit) | Value |
   |---|---|---|
   | `INDEX_MAX_TOKENS` | `evals/run_evals.py:70` | 2048 |
   | `DETAILS_MAX_TOKENS` | `evals/run_evals.py:71` | 2048 |
   | `URL_MAX_TOKENS` | `evals/run_evals.py:72` | 8192 |

   No other `max_tokens` value exists in the file. Seven `_extract_json`
   call sites found: sync index (`:1113`), sync details batch (`:1124`),
   sync details retry (`:1134`), batch-API index (`:1239`), batch-API
   details (`:1276`), batch-API details retry (`:1304`), `--url-smoke`
   (`:1749`). All seven updated in Step 1 (below); the batch-API path is
   written and reviewed but not exercised this session (no `--batch` run),
   same caveat the original author of that path recorded.
4. Free gate: `env -u ANTHROPIC_API_KEY uv run evals/run_evals.py --check`:
   10 menus, 355 items, 0 ERROR, 34 WARN, 20 SKIP, exit 0. Matches
   expectation exactly. Full-output md5 captured for later diffing:
   `197766075710706f95fa43792f852db0`.

### Sizing measurements, ESTABLISHED offline from `evals/menus/masa-sushi/golden.json`

Computed before writing any code, to ground Step 1e's "compute worst-case
details output headroom" instruction in a real number rather than the P1-SC
entry's UNCERTAIN 4-chars-per-token heuristic:

- masa: 133 golden items over 2 photos, roughly 66 items per index call.
- Index-shaped JSON (n, name, section, price_text, price) for all 133 items:
  14220 chars, roughly 7100 chars per photo. Both P1-SC crash offsets (4664,
  4678) land at roughly 66% of that per-photo figure.
- Worst 8-item details payload (the normal batch size): 1911 chars.
- Worst-case `details_retry` payload (unbounded, all items of one photo in
  one call): roughly 12000 chars. This is the number that drove A-1 above.

Character-to-token conversion stays UNCERTAIN; no cause claim is made from
this arithmetic alone. It only sizes the token caps. Step 3's usage JSONL is
the actual measurement.

### Step 1: hardening, implemented

`evals/run_evals.py`, all six sub-items (a through f):

- **a, defensive parse**: new `HarnessParseError` and `HarnessTruncationError`
  exception classes; new `CallContext` dataclass (run stem, menu slug, call
  kind, model, photo index, source path or URL) threaded through all 7
  `_extract_json` call sites; new `_write_crash_file()` writes the FULL raw
  response text plus `menu_slug`, `call_kind`, `photo_index`, `source`,
  `model`, `stop_reason`, all four usage counters, and the decoder error
  detail, to `evals/crash/<stem>-<slug>-p<photo>-<kind>-<seq>.json` (seq is
  `time.time_ns()`, collision-proof within a run). The crash path prints the
  file path to stderr and raises the labeled error naming menu and call
  kind. No silent recovery; the existing `details_retry` (a domain retry for
  items missing after the first batch, not an error retry) is unchanged.
- **b, stop_reason guard**: same `_extract_json`, after a successful parse,
  checks `stop_reason == "max_tokens"`; if so, writes a crash file (the
  parsed payload is evidence, not garbage) and raises
  `HarnessTruncationError`. Per A-2, this aborts the run exactly like a
  parse crash; no new code path in report assembly.
- **c, incremental usage persistence**: new `_record_call()` helper replaces
  every inline `call_usages.append(CallUsage(...))` at all 7 sites. It
  appends to the in-memory list exactly as before, and also appends one
  JSONL line to `evals/usage/<stem>.jsonl` (timestamp, stem, slug,
  photo_index, kind, model, all four token counts, stop_reason), opened in
  append mode and flushed per line. Called before `_extract_json`, so the
  usage for a call that then fails to parse is still captured, not only
  usage for calls before it. `write_report()`'s signature and the totals it
  computes are unchanged; it still receives the same `all_call_usages` list.
- **d, per-menu progress**: `cmd_run()` now prints one flushed stdout line at
  each menu's start (slug, photo count) and one at completion (slug, call
  count, running cost via the existing `estimate_cost(_sum_usage(...))`, no
  new cost math), numbered `[i/N]`.
- **e, token caps**: `INDEX_MAX_TOKENS` 2048 to 8192.
  `DETAILS_MAX_TOKENS` 2048 to 8192 per A-1. `URL_MAX_TOKENS` unchanged at
  8192. Table again, post-edit:

  | Constant | Old | New |
  |---|---|---|
  | `INDEX_MAX_TOKENS` | 2048 | 8192 |
  | `DETAILS_MAX_TOKENS` | 2048 | 8192 |
  | `URL_MAX_TOKENS` | 8192 | 8192 (unchanged) |

- **f, offline self-test**: new `_crash_path_self_test()`, hooked into
  `cmd_check()` beside the existing `_self_test()` / `_lint_self_test()` /
  `_schema_composition_self_test()` calls, following their established
  pattern. Uses `tempfile.TemporaryDirectory()` (already imported, already
  used at the manifest-skeleton self-test) as a swapped-in `CRASH_DIR`, and
  two synthetic `_FakeResp` objects (never a repo golden, never an API
  call): one with truncated, unterminated JSON (asserts a crash file is
  written containing the FULL raw text and expected metadata, and that
  `HarnessParseError` is raised naming the menu and kind), one with valid
  JSON but `stop_reason == "max_tokens"` (asserts `HarnessTruncationError`
  is raised). The two "crash file written" stderr lines the self-test's own
  crashes would otherwise print are swallowed with
  `contextlib.redirect_stderr(io.StringIO())`, so `--check`'s output gains
  exactly one new line (the self-test's own PASS line), not four.

### Scoring neutrality: verified, not asserted

`git diff evals/run_evals.py` reviewed hunk by hunk. Grepped for every name
on the untouched list (`normalize_ingredient`, `normalize_name`,
`match_items`, `ingredient_sets`, `f1`, `price_matches`, `score_menu`,
`aggregate`, `evaluate_gates`, `_fuzzy_merge`, `_merge_details_into_index`,
every `_assert_a` through `_assert_g`, `lint_menu`, `GATES`,
`NAME_MATCH_THRESHOLD`) against the diff: zero hits. None of those functions
or constants appear anywhere in the changed lines. The only functions with
changed signatures are pipeline orchestration (`_run_photo_pipeline`,
`run_pipeline_for_menu`, `_run_pipeline_for_menu_batch`, `_extract_json`),
none of them scoring, matching, merge, dedupe, or gate code.

`--check` full-output diff, `ANTHROPIC_API_KEY` unset, before vs after
(captured via `git stash` / `git stash pop` on the same tree so both runs
saw identical goldens):

```
22a23
> crash-path self-test: PASS (synthetic truncated JSON in a temp dir, no repo golden, no API call)
```

One line added, nothing else. Line counts: 92 before, 93 after. Totals row
identical both sides: `lint totals: 0 ERROR, 34 WARN, 20 SKIP`. Menu count
(10) and item count (355, summed from the per-menu `golden items` lines)
identical. Exit code 0 both times.

`uv run --no-project python -m py_compile evals/run_evals.py`: clean.

### Manifest (files touched, this commit)

- `evals/run_evals.py`: hardening per Step 1a-f above. 293 insertions, 33
  deletions. No `golden.json` anywhere touched (confirmed by `git diff
  --stat`, only `evals/run_evals.py`, `.gitignore`, and this entry appear).
- `.gitignore`: two lines added, `evals/crash/` and `evals/usage/`, with a
  comment explaining both are local run artifacts and the committed report
  stays the record of note.
- `docs/BUILDLOG.md`: this entry.
- Not touched: any `golden.json`, `shared/prompts/*`, `shared/aliases.json`,
  `shared/schema/*`, `evals/menus/README.md`,
  `evals/accepted_vocabulary.json`, `ROMAJI_LEXICON`, `src/*`,
  `docs/SPEC.md`, `PLAN.yaml`, `.dev.vars`, `.envrc`, wrangler config.
  Confirmed by `git diff --stat` showing exactly the three paths above.

### Status at commit 1: Steps 3, 4, 5 not yet run

This entry covers Step 1 (hardening) and Step 2 (this commit) only. Step 3
(spend gate 1, the masa-sushi diagnostic run and cause discriminator) and
Step 4 (spend gate 2, the `--all` baseline) both require Tom's explicit go
before any API spend, per the card's two spend gates and per
[[feedback_intervention_gates]] (flag human-gate steps explicitly, stop
before any API-credit spend until Tom confirms). Neither has been requested
yet as of this commit. Step 5 (commit 2, both report files plus BUILDLOG
part 2 with JSONL-to-report reconciliation) follows only after Step 4
completes.

### Patterns established

- A build card's "compute worst-case X, raise the cap only if it exceeds
  half" rule can read two ways when the call site in question is unbounded
  (here, `details_retry`) rather than fixed-size (the normal 8-item batch).
  Surfacing both readings to Tom as an explicit question, rather than
  picking one silently, is the correct move exactly when the card's own
  arithmetic doesn't resolve which call site the rule was written against.
- Recording usage (`_record_call`) before attempting to parse
  (`_extract_json`), not after, means a crashing call's own token spend is
  never lost, not just the calls that came before it. This is a stronger
  reading of the card's "so a crash never again loses accounting" than
  "everything up to but not including the crash."
- Swallowing a self-test's own side-effect stderr output
  (`contextlib.redirect_stderr`) is necessary once a self-test exercises a
  code path that itself prints, or the "one line added" neutrality claim in
  Step 1h breaks on a technicality (four lines added, not one) even though
  the actual check-relevant totals (menus, items, ERROR/WARN/SKIP, exit
  code) never moved.

### Single next action

Report Step 1 and commit 1 complete to Tom; halt for explicit go on Step 3
(`uv run evals/run_evals.py --menu masa-sushi --timestamp
2026-08-06-p1-sb2-diag-masa`, roughly $0.10 to $0.15), the empirical
discriminator between the two candidate causes named in the card's CAUSE
STATUS section.

## Session 2026-08-08: P1-SB2 part 2, discriminator run and --all baseline

Base commit: cd431fd

### Spend gates: both run under Tom's explicit go

Both spend gates in the P1-SB2 card were blocked once at the Claude Code
tool-permission layer (an auto-mode classifier denial, not Tom declining):
the first direct attempt at Step 3 was denied, as was a follow-up attempt to
configure a Bash permission rule myself via the update-config skill. Per the
harness's own guidance (a denied call means work within the restriction, not
around it), this was reported to Tom rather than retried through another
tool path. Tom added the permission rule himself via `/permissions` and gave
explicit go ("Retry Step 3, this is my go"); Step 4's go ("go, this is my
go") came after Step 3's result was reported. Both gates are on the record
as Tom's explicit authorization, not inferred.

### Step 3: masa-sushi diagnostic run, the discriminator

Command run exactly as specified:
```
uv run evals/run_evals.py --menu masa-sushi --timestamp 2026-08-06-p1-sb2-diag-masa
```

Result: COMPLETED. 23 calls, no crash, no `HarnessParseError`, no
`HarnessTruncationError`. `GATES: FAIL` (exit 1), expected for a single
weak-fit menu on its own; not a harness failure. Cost, from the run's own
accounting: $0.1463, inside the card's $0.10-0.15 estimate.

Discriminator read from `evals/usage/2026-08-06-p1-sb2-diag-masa.jsonl`:

| Photo | Index call output_tokens | vs old 2048 cap | stop_reason |
|---|---|---|---|
| 0 | 3440 | over by 1392 (68%) | `end_turn` |
| 1 | 1799 | under | `end_turn` |

**Verdict: ESTABLISHED, by measurement, not arithmetic inference.** Photo 0's
index call needed 3440 output tokens; the old `INDEX_MAX_TOKENS = 2048` cap
would have cut generation off at roughly 59.5% of that (2048/3440), which
lands close to the P1-SC crash offsets' roughly 66% of the per-photo char
budget estimated offline before this run (a coarse char-based figure, not
directly comparable token-for-token, but directionally consistent, not
contradictory). Under the new 8192 cap, both calls completed with
`stop_reason: end_turn`, no truncation.

Reconciliation: JSONL sums (input 19507, output 13310, cache write 34938,
cache read 165319) match the report's "Token usage and cost" section
exactly. All 23 calls recorded `stop_reason: end_turn`; the truncation guard
built in Step 1b never fired this run, correctly, since nothing was
truncated once the cap was raised. Cache check line: 19/19 `details_batch_n`
calls had cache reads > 0 [ok].

Report: `evals/reports/2026-08-06-p1-sb2-diag-masa.md`, labeled diagnostic,
not part of the baseline of record. Its per-item diffs (ingredient
mismatches, price mismatches on multi-tier sushi/sashimi pricing, several
missed/extra items) are not analyzed here; per the card, this run exists
only to answer the discriminator question, not to critique masa-sushi's
extraction quality.

### Step 4: full `--all` baseline run

Command run exactly as specified:
```
uv run evals/run_evals.py --all --timestamp 2026-08-06-p1-sc-all
```

Result: COMPLETED, all 10 menus, 70 calls, no crash, no truncation error.
`GATES: FAIL` (exit 1), the card's predicted result, not a halt condition.
Per-menu progress lines (Step 1d) printed and localized every menu; no
localization guesswork was needed this time, unlike the two P1-SC crashes.
Cost, from the run's own accounting: $0.5828.

Reconciliation: JSONL sums (input 58959, output 36309, cache write 244566,
cache read 365442, 70 calls total) match the report's "Token usage and
cost" section exactly, and the per-menu call counts printed during the run
(2, 5, 4, 4, 7, 4, 3, 9, 9, 23) sum to 70, matching the JSONL line count.
Zero calls with a `stop_reason` other than `end_turn`, confirmed by scanning
the full JSONL, not sampled.

Cause-confirmation line, second independent measurement: masa-sushi's two
index calls this run needed 2919 (photo 0) and 2522 (photo 1) output
tokens, both over the old 2048 cap (by 871 and 474 respectively), both
`end_turn` under the new cap. Two different runs, both photos of masa's
index pass exceeding 2048 tokens on at least one photo each time: the
max_tokens cause is not a one-photo fluke.

Both required aggregation tables computed by hand from the harness's own
per-menu breakdown table, at zero extra spend, and appended to the report
under a clearly marked "P1-SB2 supplementary aggregation" heading; the
harness's own Gates table, per-menu table, and token usage section above
that heading are untouched.

**(i) All 10 menus** (identical to the harness's own Gates table, restated
for the side-by-side): item_recall 0.8282, item_precision 0.7577,
ingredient_f1_macro 0.7286, price_accuracy 0.8333, all FAIL against their
>= 0.97 / >= 0.97 / >= 0.90 / >= 0.97 thresholds. consistency_f1_spread_max
NOT MEASURED. Wrap accuracy 0.9407, annotated "(no gate, unweighted mean
over menus with wrap data)", all 10 of 10 menus have wrap data. Totals:
gold 355, pred 388, matched 294.

**(ii) 9 menus, excluding km-sushi-dinner**: item_recall 0.8605,
item_precision 0.7989, ingredient_f1_macro 0.7447, price_accuracy 0.8412,
all still FAIL. consistency_f1_spread_max NOT MEASURED. Wrap accuracy
0.9341, same annotation, 9 of 9 menus have wrap data. Totals: gold 337,
pred 363, matched 290.

Method: each menu's integer `n_matched` was recovered from the harness's
3-decimal-rounded per-menu recall and precision figures
(`round(recall * n_gold)` cross-checked against `round(precision * n_pred)`;
all 10 menus agreed exactly between the two derivations, so `n_matched`
itself carries no rounding ambiguity here). The all-10-menu aggregation was
then recomputed by this same method as a validation step before trusting
the excl-dinner figures: it reproduced the harness's own Gates table to
within 0.0001 on `ingredient_f1_macro` and matched exactly on the other
three. Rounding bound stated once, in the report itself, beneath both
tables: at most a few parts in the last printed digit, immaterial next to
gate misses of double-digit percentage points.

Consistency gate recorded NOT MEASURED with its reason (no `--repeat` run
performed, per the card's explicit single-run instruction): stated plainly
as no number existing to report, not as a rounding of a small number.

No prompt iteration was performed. No disposition recommendation was made
for km-sushi-dinner. Numbers only, per the card.

### Manifest (files touched, this commit)

- `evals/reports/2026-08-06-p1-sb2-diag-masa.md`: written by the harness
  (Step 3), unmodified after.
- `evals/reports/2026-08-06-p1-sc-all.md`: written by the harness (Step 4),
  then the supplementary aggregation section appended by hand under a
  clearly marked heading; everything above that heading is the harness's
  own unaltered output.
- `docs/BUILDLOG.md`: this entry.
- `evals/usage/2026-08-06-p1-sb2-diag-masa.jsonl` and
  `evals/usage/2026-08-06-p1-sc-all.jsonl`: written incrementally by the
  hardened harness during both runs; gitignored per commit 1, not part of
  this commit, reconciled into this entry's prose instead (both reconcile
  exactly against their respective reports' totals, per above).
- No `golden.json` anywhere touched. Confirmed by `git status --porcelain`
  (only the two report files untracked before this commit) and by
  `git diff --name-only e8f96e1 HEAD -- 'evals/menus/*/golden.json'`
  returning nothing for any commit in this session's range; the last commit
  to touch any golden predates this session (b6f36cf).
- Not touched: `shared/prompts/*`, `shared/aliases.json`, `shared/schema/*`,
  `evals/menus/README.md`, `evals/accepted_vocabulary.json`,
  `ROMAJI_LEXICON`, `evals/run_evals.py` (unchanged since commit 1's
  `cd431fd`), `src/*`, `docs/SPEC.md`, `PLAN.yaml`, `.dev.vars`, `.envrc`,
  wrangler config.

### Patterns established

- A tool-permission denial at the classifier layer is not the same thing as
  Tom declining a spend gate, and should be reported and escalated to Tom
  rather than routed around through another tool (a config-edit skill, a
  different shell invocation). This held even when the alternate route
  looked benign (adding a permission rule, not spending money): the
  restriction itself, not just its immediate effect, is what to respect.
- Cross-checking a hand-built aggregation against the harness's own
  pre-computed all-menus figures, before trusting the same method's output
  on a subset the harness never directly reports, is a cheap way to bound
  the rounding error without a second paid run. The bound is then stated
  once in the report, not asserted without a check behind it.
- Two independent measurements of the same signal (masa's index tokens,
  once in the Step 3 diagnostic, once inside Step 4's full run) is stronger
  evidence than one; the second run wasn't spent for this purpose alone,
  but recording it here upgrades the Step 3 verdict from a single
  measurement to a repeated one.

### Done-when, walked item by item

1. All `max_tokens` values printed old and new: table in the part 1 entry
   and in `evals/run_evals.py`'s own comment above the constants. Done.
2. Crash-path self-test proven with a synthetic fixture: part 1 entry,
   `--check` output, `_crash_path_self_test()`. Done. (Not exercised for
   real this session, since neither run crashed, by design: the fix worked.)
3. `--check` identical before and after hardening, totals shown: part 1
   entry, one-line diff, identical totals. Done.
4. Usage JSONL exists and reconciles with report totals: both runs this
   session, shown above. Done.
5. Step 3 outcome recorded with the discriminator read, cause tagged
   ESTABLISHED: above. Done.
6. Baseline report with both aggregations, wrap annotation, rounding bound,
   consistency NOT MEASURED: `evals/reports/2026-08-06-p1-sc-all.md`,
   supplementary section. Done.
7. Zero goldens modified, proven by git diff: above. Done.
8. Two commits, neither pushed: `cd431fd` (part 1) and this commit (part 2).
   Confirmed by `git log --oneline origin/main..HEAD` and `git status`
   below.

### Single next action

None outstanding on this card. `evals/run_evals.py` now has raw-response
capture, incremental usage accounting, and per-menu progress, the three
gaps named in the P1-SC entry; the `--all` gate failures recorded in the
baseline report are numbers only, not a disposition, and were explicitly
out of scope for this card. A future card would decide what, if anything,
to do about the FAIL rows (prompt iteration, golden review, or a scoped
investigation of km-sushi-dinner specifically), starting from this session's
baseline report as the reference point.

## Session 2026-08-10: P1-SD, prompt iteration round 5, blocked

Base commit: 97b6aeb

### Scope

Task #10 from the agent-pm board. Spend session, up to $1 authorized
directly by Tom. Diagnose the baseline per-menu before editing anything;
targets in priority order: precision (over-splitting), price (carry-down),
ingredient F1. One change-set per session.

### Round 1: masa-sushi neta-splitting hypothesis, wrong, reverted

Hypothesis: the report-tail lead's named example (Ebi, Tamago, Inari, Uzura
appearing as extra predicted items) was a choice-set list without individual
prices getting exploded into separate items. Drafted a `system.md` edit on
this theory. Checked against `evals/menus/masa-sushi/golden.json` before
spending: wrong. These are individually priced gold items (`n:48-51`,
English `name`, `romaji: X` in `notes`), not a choice-set at all.

Verification run anyway, to be sure: `uv run evals/run_evals.py --menu
masa-sushi --timestamp 2026-08-10-p1-sd-masa-verify` ($0.1491). Item count
unchanged (156/133, identical to baseline), targeted items still EXTRA.
Confirms the edit had no effect, consistent with the wrong-premise finding.
Edit reverted (`git checkout`), working tree clean.

### Round 2: free diagnosis, 4 parallel subagents, zero spend

Dispatched four read-only diagnostic subagents (Explore type) to bucket
every EXTRA/MISSED item against `golden.json` for masa-sushi,
km-sushi-dinner, km-sushi-special-rolls, km-sushi-noodles-kitchen. Findings,
each independently cross-checked against golden data, not asserted from the
report diffs alone:

- masa-sushi (23/33 diff rows, 70%): the model correctly matches the
  English-named gold item AND separately emits a duplicate under the bare
  Japanese/romaji term for the same fish. Fixing this would mean the prompt
  suppressing a second printed occurrence as not-a-new-item, but `system.md`
  already states the opposite principle explicitly ("do not merge two
  visually distinct printed items into one just because they sound similar;
  that judgment belongs to the client-side dedupe step"). A design-level
  question (prompt exception vs. client-side dedupe enhancement), escalated
  to Tom as task #13 rather than patched unilaterally.
- km-sushi-dinner (13/21 EXTRA, 62%): hallucinated generic roll names
  (Dynamite, Dragon, Salmon Skin, Philadelphia, Eel Avocado) not on this
  specific menu photo at all, several duplicated in long+short form. Already
  task #2's territory, no new action.
- km-sushi-special-rolls (26/52 rows, 50%): illegible/handwritten roll
  names, model falls back to describing contents as the name; ingredients
  themselves match gold roll-for-roll. Likely not prompt-fixable (a
  photo-legibility limit, not a wording gap). Logged as task #14.
- km-sushi-noodles-kitchen (13/28, 46%): under-application of the EXISTING
  "Combo and choice-set items" section (ramen flavor-matrix explosion,
  "Children's Combo" dropped in favor of its listed choices, tempura
  components pulled out standalone). The one target that is in-scope,
  prompt-fixable, and does not require a convention call.

Oversight reviewed and directed round 3 at km-sushi-noodles-kitchen only.

### Round 3: km-sushi-noodles-kitchen combo fix, inconclusive-to-negative

Added one paragraph to `system.md`'s "Combo and choice-set items" section:
a combo/multi-choice dish keeps exactly one entry regardless of how its
choices are printed (never dropped in favor of only its listed choices,
never split into per-modifier items).

Verification: `uv run evals/run_evals.py --menu km-sushi-noodles-kitchen
--timestamp 2026-08-10-p1-sd-noodles-verify` ($0.0419). Result: WORSE than
baseline (recall 0.133 vs. 0.267, precision 0.080 vs. 0.190, items 25/15 vs.
21/15), not better.

Before concluding the edit caused it, ran a control: same menu, unedited
prompt, `--timestamp 2026-08-10-p1-sd-noodles-control` ($0.0415). Result:
0.333 recall, 0.179 precision, 28/15 items, notably better than both the
edited run and the original baseline. Two runs of the identical unedited
prompt on this one menu span 0.267 to 0.333 recall: real, substantial
single-run variance, large enough to swallow whatever a small edit's true
effect is. Per the gates-decide-not-vibes principle, could not certify the
edit as an improvement (or, cleanly, as a regression) on n=1. Did not
commit. Edit abandoned (`git stash` then `git stash drop`), working tree
clean, verified via `git status --porcelain`.

### Manifest (files touched, this commit)

- `evals/reports/2026-08-10-p1-sd-masa-verify.md`: written by the harness
  (round 1's verification run), kept as the record that the round-1
  hypothesis was tested and found to have no effect.
- `evals/reports/2026-08-10-p1-sd-noodles-verify.md`: written by the harness
  (round 3's verification run), kept as the negative result.
- `evals/reports/2026-08-10-p1-sd-noodles-control.md`: written by the
  harness (round 3's control run), kept as the variance evidence.
- `docs/BUILDLOG.md`: this entry.
- Not touched: `shared/prompts/*` (both edits reverted before this commit,
  confirmed clean via `git status` and `git diff` before writing), `shared/
  schema/*`, `shared/aliases.json`, `evals/menus/*/golden.json` (no golden
  touched, confirmed by `git diff --name-only 97b6aeb HEAD --
  'evals/menus/*/golden.json'` returning nothing), `src/*`, `public/*`.

### Patterns established

- A verification run's single-sample result is not sufficient evidence to
  certify a prompt edit, positive or negative, when a same-menu control run
  on the unedited prompt shows variance of comparable magnitude. Running the
  control before concluding causation (rather than after, or not at all) is
  the affordable way to catch this without a full `--repeat` measurement.
- "The report-tail INFERRED leads" in a task's acceptance criteria can mean
  a lead PROJECT-STATE.md derived from reading a report's tail, not a
  literal tag in the repo. When the phrase does not resolve to a findable
  artifact, asking rather than guessing at its referent (routed through
  oversight here) avoided diagnosing against the wrong target.
- New findings that fall outside a card's original scope (the km-sushi-
  dinner alias-duplication lead, the masa-sushi dedup-architecture
  collision) get logged as new tasks for Tom's decision, not folded
  silently into the current change-set and not decided unilaterally, even
  when the finding is well-evidenced.

### Done-when, walked item by item

1. Per-menu diagnosis confirming or revising the report-tail leads: done,
   round 2, independently re-derived and cross-checked against
   `golden.json` for all four worst-precision menus, not just asserted.
2. A change-set lands with its eval receipt: NOT done. Two hypotheses
   tried, both failed to demonstrate improvement, both correctly not
   committed rather than shipped on hope.
3. Gate deltas reported: done for both attempted edits, including the
   negative/inconclusive round 3 result and the variance finding behind it.

Task #10 marked `blocked` on the board (not `failed`): the diagnosis work
was real and produced two new decision tasks (#13, #14) plus a finding that
argues for reconsidering task #12's hold. Blocked pending either a
`--repeat` consistency measurement or Tom's own call on unblocking it.

### Single next action

None outstanding on this card; task #10 is blocked pending task #12 or
Tom's direction. A future round should not retry km-sushi-noodles-kitchen's
combo fix as a single n=1 verification again without either a `--repeat`
run or explicit acceptance of the noise floor found here.

## Session 2026-08-10: P1-S4, worker spine

Base commit: 1a891a1

### Scope

Task #11 from the agent-pm board. Zero-spend. Covers T-1.1 preprocess.js,
T-1.6 session.ts, T-1.7 ratelimit.ts, T-1.8 worker router, T-1.9 app.js
state machine.

### Pre-existing state, checked before writing anything

`src/extract.ts` (Anthropic request construction) and `src/worker.ts` (a
Phase 0 skeleton: health check, CORS, route table, `/api/*` other than
`/health` explicitly 404ing) already existed. `src/session.ts`, `src/
ratelimit.ts`, `public/preprocess.js` did not exist. `public/app.js`
existed as a 16-line stub, not the state machine.

### T-1.6, T-1.7: session.ts, ratelimit.ts

Verified live docs before writing (CLAUDE.md's requirement, training data
may be stale): Turnstile siteverify endpoint, request fields including
`idempotency_key`, response fields; the native `RateLimit` binding's
`limit({key}): Promise<{success}>` signature; period constrained to 10 or
60 seconds (already satisfied by the existing wrangler.jsonc config).

Session token minted and verified exactly per SPEC.md's wire format:
`base64url(payload) + "." + base64url(hmacSHA256(payload, secret))`, HMAC
computed over the raw serialized payload bytes, not the base64url-encoded
string (a deliberate departure from JWT convention already present in the
spec, implemented as specified rather than substituted for the more common
pattern). Signature check uses `crypto.subtle.verify` (constant-time), never
a string or byte comparison, per SPEC.md's security controls.

### T-1.8: worker router

Wired `/api/session`, `/api/extract/index`, `/api/extract/details`, `/api/
extract/url` using session.ts, ratelimit.ts, and the existing extract.ts
provider. Body size capped at 1.5MB (content-length check plus an explicit
byte-length check for clients that omit or lie about the header), matching
SPEC.md. One structured JSON log line per Anthropic call (endpoint, model,
usage, latency, outcome), per SPEC.md's observability requirement.

Found and fixed a real, pre-existing bug in wrangler.jsonc while wiring
this: the `shared/prompts/*.md` Text-module rule never actually worked.
`base_dir` defaults to the directory containing `main` (`src/`), not the
project root, so the glob silently matched nothing. Confirmed empirically,
not just from docs: even after setting `base_dir` to the project root, the
narrow glob still failed against a live `wrangler dev` boot; only the
recursive `**/*.md` form worked. Neither problem had surfaced before this
session because nothing imported `extract.ts` (whose `.md` imports trigger
the rule) through the worker until this router wiring.

### T-1.1: preprocess.js

`createImageBitmap(file, { imageOrientation: 'from-image' })` for EXIF
rotation, with a canvas-based fallback for browsers where that option is
unsupported. Downscale to a 1568px longest edge, JPEG re-encode at 0.8
quality, stepping down to 0.7 then 0.6 if the result exceeds 1.2MB, base64
encode. Matches SPEC.md's five-step sequence exactly.

### T-1.9: app.js state machine

States IDLE, PREPROCESS, INDEX, DETAILS, RECONCILE, READY, ERROR per
SPEC.md. Multi-photo merge with global ids (`photoIndex:n`), photo-order
merge, dedupe on fuzzy name match plus compatible price (equal numeric, or
at least one side null), keeping the record with more ingredients and
unioning notes on a match. Fuzzy matching is a Levenshtein-ratio
approximation of the harness's `token_sort_ratio`, explicitly documented in
a comment as not byte-identical to Python's fuzzywuzzy/rapidfuzz
(different algorithm, same idea: sort tokens, measure similarity), since no
bundler exists to pull in a matching library and the client only needs to
catch overlapping-photo duplicates, not reproduce the harness's exact
score. DETAILS batch 1 fires alone to warm the prompt cache, remaining
batches fan out at concurrency 3, batches of 8. One retry for items missing
a details result after reconciliation, tracked per photo to stay idempotent
across a resumed job. Full job state persists to `localStorage` under
`ss:job:<jobHash>` after every transition; a job younger than 30 minutes
resumes from its last completed step. `restaurant_name` merge takes the
first non-null value in photo order.

Caught and fixed one bug before it shipped: `perPhotoRetried` was
originally typed as `Set` per photo, which does not survive the
`JSON.stringify`/`parse` round-trip every job save goes through via
localStorage; a resumed job would have silently lost its retry-tracking
state. Changed to a plain array with `includes`/`push` before this was ever
exercised at runtime, caught by re-reading the code, not by a failing test
(no test harness exists for this frontend code yet).

### Verification

`tsc --noEmit`: clean throughout. `node --input-type=module --check` on
both new frontend files: clean. Live `wrangler dev` boot (multiple times,
across the base_dir fix and the final integration check): `/api/health`
200, `/api/session` 400 on missing Turnstile token, `/api/extract/index`
401 without a valid session (auth gate confirmed working), `/api/menus/*`
and unknown `/api/*` both 404, static assets including the two new JS files
serving 200 with the correct content type. No secrets echoed anywhere
(wrangler's own masking, confirmed in captured output). Zero Anthropic
calls made; zero spend, matching the card's zero-spend tag.

Not exercised end to end: Turnstile's success path (no real site/secret key
pair available locally, only the `REPLACE_WITH_TURNSTILE_SITE_KEY`
placeholder), and the full browser parse flow (no ui.js yet to drive it;
that file is out of scope for this card, T-1.9 covers app.js only).

### Manifest (files touched, this commit)

- `src/session.ts`: new. Turnstile verification, HMAC session token
  mint/verify.
- `src/ratelimit.ts`: new. Thin wrapper over the two native RateLimit
  bindings.
- `src/worker.ts`: rewritten from the Phase 0 skeleton to the full Phase 1
  router.
- `public/preprocess.js`: new. Image normalization per SPEC.md.
- `public/app.js`: rewritten from a 16-line stub to the full orchestration
  state machine.
- `wrangler.jsonc`: `base_dir` added, the Text-module rule's glob
  broadened, both required to make the existing `.md`-as-text rule (added
  2026-07-23) actually work.
- `docs/BUILDLOG.md`: this entry.
- Not touched, out of scope for this card: `public/ui.js`, `public/
  filters.js`, `public/aliases.js` (none exist yet, all named in SPEC.md's
  repo layout but not in this card's T-numbers), `shared/*`, `evals/*`.

### Patterns established

- A module-resolution bug in bundler config can hide indefinitely behind an
  unexercised import path; the fix surfaced only because this session
  finally wired the file that exercises it, not because anything about the
  config itself changed. Worth a standing habit: when wiring two
  already-written pieces together for the first time, expect latent
  integration bugs neither piece's own author could have caught alone.
- A data type that will round-trip through `JSON.stringify`/`parse`
  (anything persisted to localStorage, here) needs to be JSON-safe from the
  start; `Set`, `Map`, and `Date` are the common traps. Worth checking this
  explicitly for any new persisted field, not just at the point something
  breaks on resume.

### Done-when, walked item by item

1. `wrangler dev` serves the app: done, verified live, multiple boots,
   shown above.
2. Session/ratelimit/router wired per SPEC.md endpoint contracts: done, all
   four endpoints, verified against live docs before writing, smoke-tested.
3. No spend incurred: done, zero Anthropic calls made this session, `.dev.
   vars`'s ANTHROPIC_API_KEY never invoked outside task 10's separate,
   already-authorized eval runs.

### Single next action

`public/ui.js`, `public/filters.js`, `public/aliases.js` remain unbuilt;
app.js's state machine has no renderer yet to drive it in a real browser.
Turnstile's success path is untested locally (needs a real site/secret key
pair, likely a staging deploy or Tom supplying test keys). Both are natural
next cards, neither is this one's scope.

## Session 2026-08-10: P1-S4 cont., renderer (ui.js, filters.js, aliases.js)

Base commit: 8d899a7

### Scope

Task #15 from the agent-pm board, the natural continuation of #11 flagged
in that session's own closing note. Zero-spend. Per SPEC.md's UI contract:
filter drawer as a bottom sheet, tri-state ingredient chips plus wrap/
is_raw as dedicated chips, item search, three sort modes, Omakase no-repeat
shuffle with an exhaustion state. Mobile standards (44px targets, 16px+
inputs, safe-area insets, bottom sheet not side panel, dark palette,
reduced-motion) are contractual per SPEC, not aspirational.

### filters.js, aliases.js

Pure logic, no DOM. Functionally verified with 20 assertions (include/
exclude filtering, wrap+is_raw combination, empty-state detection, name/
ingredient search, all three sort modes including null-price sinking and
non-mutation, the tri-state chip cycle, vocabulary building, alias
normalization case-insensitivity/plural-folding/pass-through). All 20
pass.

### A real spec gap: how does the browser reach shared/aliases.json

`shared/aliases.json` lives outside `public/`, and wrangler.jsonc's assets
binding only serves `./public`; SPEC.md's Worker API section enumerates
every endpoint explicitly and has none for this. Resolved with
`public/aliases.json` as a symlink to `../shared/aliases.json`, keeping
`shared/` as the single source of truth already established for
`shared/prompts/`, using the existing static-asset path, touching no
worker code. Verified against a live `wrangler dev` boot: the symlink
resolves and serves the real content (200).

A second, analogous gap surfaced while building the capture flow:
`TURNSTILE_SITE_KEY` is a worker `var`, "public by design" per its own
wrangler.jsonc comment, but nothing served it to `public/` either. Resolved
by adding `turnstileSiteKey` to the existing `/api/health` response rather
than a new route, the same reasoning as the aliases fix: minimal, reuses
an existing public GET endpoint, no new undocumented API surface.

### ui.js

`index.html`'s script tag now loads `/ui.js` (not `/app.js` directly):
ui.js owns the DOM and imports app.js's `JobController` internally, per
SPEC.md's file split (app.js knows nothing about rendering). `index.html`'s
body is now just the `#app` mount point; ui.js constructs everything else
via `document.createElement`, using `textContent` rather than
interpolated `innerHTML` anywhere menu-derived data appears (item names,
ingredients, notes are vision-model output from a photo, not trusted
input).

Three screens (Home/capture, Progress, Menu), the filter bottom sheet,
item cards with raw/wrap/needs-review badges, and the Omakase shuffle
button and exhaustion state. Turnstile's widget renders when
`window.turnstile` and a real site key are both present; degrades to a
visible "unavailable" message otherwise (this repo's site key is still
the `REPLACE_WITH_TURNSTILE_SITE_KEY` placeholder, so that path is
exercised, not the real widget). Flagged item-correction (the three-tier
chip/autocomplete/free-text bottom sheet described under app.js's
RECONCILE handling) was left out of this card's build: task #15's
acceptance criterion names filters/search/sort/Omakase specifically, that
correction flow is a separate feature under a different SPEC.md heading,
and flagged items already render with a visible badge per app.js's own
`flagged`/`flagReason` fields, so nothing is silently dropped in the
meantime.

### Browser verification

No headless-browser tool (Playwright, Puppeteer, a Chrome binary) is
available in this environment; installing one would mean downloading a
full browser binary with no prior authorization to do so. Used `jsdom`
instead, installed isolated in the session scratchpad (no footprint on
this repo's `package.json`/lockfile), to execute the actual shipped files
unmodified (a copy of `public/{app,ui,filters,aliases,preprocess}.js` in
an ESM-mode directory, imported directly into a jsdom `document`/`window`)
against a live `wrangler dev` server for the `fetch()` calls
(`/api/health`, `/aliases.json`). This exercises real DOM construction and
real event dispatch, not a reimplementation or a mock of the rendering
logic; short of an actual browser, this is the closest available
substitute for "actual browser testing, not just code review."

Seeded a realistic menu into `localStorage` under `ss:menu:*` and drove
the app exactly as a returning user would: tap a recent menu (the same
code path a real completed parse would populate), search, sort, filter
chips, five Omakase presses. 27 assertions, all pass.

**Caught a real bug in the process, not from code review**: the fifth
Omakase press silently reshuffled a new queue instead of showing the
exhaustion state. Root cause: `state.omakaseQueue = []` was used to mean
both "not started yet" and "just ran out," so the reshuffle-on-empty check
fired before the exhaustion check ever got a chance to. Fixed by
distinguishing `null` (not yet shuffled) from `[]` (shuffled and
exhausted) as two different states, at every one of the four sites that
touched `omakaseQueue`. Re-ran the full 27-assertion suite after the fix:
all pass, including the previously-failing exhaustion check.

Not verified even by jsdom: actual visual layout, CSS correctness (tap
target sizes, safe-area insets, bottom-sheet slide animation), and the
real Turnstile widget (jsdom has no rendering engine; CSS sizing claims in
this session rest on the stylesheet's own `--tap-min`/16px declarations,
reviewed but not measured).

### Manifest (files touched, this commit)

- `public/filters.js`, `public/aliases.js`: new, pure logic.
- `public/aliases.json`: new, a symlink to `../shared/aliases.json`.
- `public/ui.js`: new, the rendering/interaction layer.
- `public/index.html`: script tag repointed to `/ui.js`; placeholder
  markup removed, `#app` is now the sole static element.
- `public/styles.css`: extended with the full Phase 2 component set
  (capture flow, progress, menu screen, filter sheet, cards, Omakase,
  recent menus) on top of the existing Phase 0 shell/safe-area/dark-palette
  foundation.
- `src/worker.ts`: `/api/health` now also returns `turnstileSiteKey`.
- `docs/BUILDLOG.md`: this entry.
- Not touched: `shared/*`, `evals/*`, `src/session.ts`, `src/ratelimit.ts`,
  `src/extract.ts` (no change needed for a render-only card).

### Patterns established

- When two states that look identical (`[]` in both cases here) actually
  mean different things ("not started" vs. "ran out"), collapsing them
  into one representation is a latent bug waiting for the exact sequence
  that exposes it; a jsdom/browser-level test found this in a few seconds
  where reading the code twice did not. Worth defaulting to a real
  execution check for any state machine with an emptiable collection,
  not just trusting the logic by inspection.
- The `shared/`-file-reachable-from-`public/`-only gap (aliases.json, then
  the same shape again for the Turnstile site key) is a recurring pattern
  in this repo's architecture, not a one-off: worth watching for a third
  occurrence and, if it comes, considering whether it deserves its own
  documented convention in SPEC.md rather than being solved ad hoc each
  time.
- A missing verification tool (no browser automation available) does not
  mean skipping verification; picking the closest available substitute
  (jsdom, running the real files) and being explicit about what it does
  and does not cover beats either fabricating a browser test or silently
  downgrading to code review only.

### Done-when, walked item by item

1. `wrangler dev` serves a page where the state machine renders and is
   drivable: done, verified via jsdom driving the real shipped files
   against a live server, not just asserted.
2. Filters, search, sort, and Omakase function per SPEC.md's UI contract:
   done, 27 passing assertions, including a real bug caught and fixed
   during verification, not before it.
3. Mobile standards met: done by code review and CSS authoring (44px
   `--tap-min` on every interactive element, explicit 16px inputs,
   `env()` safe-area insets, bottom sheet never a side panel, dark
   palette via `prefers-color-scheme`, reduced-motion respected); not
   independently verified by measurement, no rendering engine available
   to do so this session.
4. Zero spend: done, no Anthropic calls made.

### Single next action

The flagged-item correction flow (Tier 1/2/3 chips/autocomplete/free-text)
is unbuilt, out of scope for this card. Turnstile's real widget is
unverified pending real site/secret keys. Actual visual/CSS correctness
is unverified pending a real rendering engine (a future session could
reach for a screenshot-capable tool if one becomes available, or Tom
eyeballing a deployed preview).

## Session 2026-08-10: flagged-item correction UI (fix-ingredients sheet)

Base commit: 4243b3a

### Scope

Task #16, the flagged-item correction card #15 itself flagged as the next
natural piece. Zero-spend. Per SPEC.md's RECONCILE handling: "Retry this
item" (single-item details re-call) then a "Fix ingredients" bottom sheet
with tier 1 menu-vocabulary chips, tier 2 autocomplete over that same
vocabulary, tier 3 free text only when nothing matches. Edits run through
the existing normalization/alias pipeline, swap the flagged marker for an
edited marker, persist with the cached menu. The live retry call itself is
explicitly out of scope for exercising end to end (needs a real API call
and a real Turnstile solve), per the card's own acceptance criterion.

### A deeper gap than it first looked: retry needs the original photo

Tracing through what "wire the Retry button to the existing endpoint"
actually requires: the completed job's `items` carry no reference back to
the photo bytes that produced them. `app.js`'s `JobController.start()`
holds `images` as a local variable, never stored on `this.job` (correctly:
`job` is persisted to localStorage on every state transition, and base64
photo data is easily multi-MB per photo, an easy way to blow the storage
quota). Fixed by adding `this.photoImages` as a plain instance field,
deliberately outside `job`, never touched by `saveJob`. Consequence, made
explicit rather than hidden: a single-item retry only works for a job
completed in the current page load; a menu reopened later from
`ss:menu:*` (Recent) has no photo to retry with. `ui.js` tracks this via
`state.canRetryItems` and hides the Retry button entirely when it's false,
rather than showing a button that would always fail.

### The correction sheet

Tier 1 (menu vocabulary chips), tier 2 (autocomplete over the same
vocabulary, live-filtered as you type), tier 3 (a "Add ... anyway" button
that appears only when tier 2 finds zero matches, per SPEC.md's explicit
ordering). Edits accumulate in a working copy; Cancel discards it, Save
runs the final list through `normalizeIngredients` (the same aliases.js
pipeline every extracted ingredient goes through) and flips the item from
`flagged` to `edited`, persisting via the existing `saveMenu`. "Retry this
item," when available, calls the real `/api/session` then
`/api/extract/details` endpoints with the item's actual photo and item
number; on failure (expected in this environment: no Turnstile widget is
mounted on the menu screen to solve a fresh challenge with, so the session
call fails `turnstile_failed` exactly as it should against a real
deployment) it renders an honest inline error rather than pretending to
succeed, and on success it applies the returned ingredients/wrap/is_raw
through the same correction pipeline as a manual edit.

### Verification

jsdom again (no browser automation tool in this environment, same as
#15), the real shipped files, against a live `wrangler dev` boot. 25 new
assertions covering: the correction trigger appearing only on flagged
items and disappearing once corrected; tier 1/2/3 each independently
(chip add, autocomplete-then-add, free-text-only-when-no-match); the
remove button; Save closing the sheet, flipping the badge, and updating
the rendered ingredients; and, deliberately, that the persisted
`localStorage` copy carries the *normalized* ingredient ("shrimp"), not
the raw typed one ("Ebi") — proving Save actually ran the alias pipeline
rather than storing what was typed verbatim.

**Caught a second real bug in the process**: `state.aliasTable` was only
ever loaded in `onJobReady` (the live-parse completion path). Opening a
menu from Recent skipped it entirely, so the first correction attempt on
a reopened menu crashed on a null alias table inside `normalizeIngredients`
(`Cannot read properties of null`). Fixed with the same load-once guard
already used in `onJobReady`, added to the recent-menu open handler too.
Re-ran both this session's suite and #15's full 27-assertion suite
afterward (the recent-menu handler became async, which needed a polling
wait instead of a fixed tick in both test harnesses, a harness-only fix,
not an app change) to confirm nothing regressed. 52 total assertions pass
across both suites.

### Manifest (files touched, this commit)

- `public/app.js`: `JobController.photoImages` (in-memory only) and
  `getPhotoImage()`.
- `public/ui.js`: the correction sheet, `retryItem`/`applyCorrection`, the
  fix-ingredients trigger on flagged cards, the `edited` badge, and the
  recent-menu-open alias-table-loading fix.
- `public/styles.css`: correction-sheet-specific styles (editable
  ingredient chips, tier-2 autocomplete list, tier-3 free-text row, retry
  status line, edited badge).
- `docs/BUILDLOG.md`: this entry.
- Not touched: `shared/*`, `evals/*`, `src/*` (no worker change needed,
  the retry call reuses `/api/session` and `/api/extract/details`
  unmodified from earlier tasks), `public/filters.js`, `public/aliases.js`
  (both reused as-is, `buildIngredientVocabulary`, `filterChipVocabulary`,
  and `normalizeIngredients` already did everything this card needed).
- Deliberately not committed: `.claude/statusline.sh` and
  `.claude/settings.local.json`'s new `statusLine` entry, added this
  session at Tom's direct authorization but personal session tooling, not
  a project deliverable; `settings.local.json` is already gitignored.

### Patterns established

- "Wire the button to the existing endpoint" can hide a real data-
  availability question underneath it (does the data the endpoint needs
  still exist by the time the button is pressed?), not just a plumbing
  question. Worth tracing the full data lifecycle, not just the network
  call, before assuming a UI wire-up is purely mechanical.
- The `state.aliasTable` gap is the third occurrence this repo has now
  hit of "a resource loaded on one entry path silently missing on
  another" (aliases.json's reachability, the Turnstile site key, now
  this). Worth treating as a standing pattern going forward: whenever a
  screen/flow gains a second way to reach it, check what the first path's
  setup steps assumed were already done.
- Async-ifying a click handler for a legitimate reason (loading data
  before proceeding) is easy to do without noticing every test that
  exercises that handler now needs to wait properly instead of assuming
  synchronous completion; caught immediately by re-running the existing
  suite, not by inspection.

### Done-when, walked item by item

1. Bottom sheet renders and is drivable, tier 1/2/3 all function: done,
   verified via jsdom, not just code review, 16 of the 25 new assertions
   cover this directly.
2. Edits apply through the existing normalization/alias pipeline and
   update the marker from flagged to edited: done, verified including the
   specific alias-resolution proof (Ebi to shrimp) and persistence to
   localStorage.
3. Zero spend: done, no Anthropic calls made. The one real network call
   this session made (`/api/session` reachability, not exercised as part
   of the assertion suite, only reasoned about) is free (Cloudflare
   Turnstile siteverify has no cost) and was not actually invoked during
   verification, only wired correctly.
4. Live single-item retry call: explicitly not exercised, per the card's
   own acceptance criterion. Noted here as the follow-up needing a real
   API call and a real Turnstile solve, same class of gap as #11's and
   #15's Turnstile-widget limitations.

### Single next action

Live-verify the retry call end to end once real Turnstile site/secret
keys exist (would also need a widget mounted somewhere reachable from the
menu screen, not just the Home screen capture flow, since retry can
happen well after the original session token has expired). Visual/CSS
correctness for the new sheet elements remains unverified for the same
reason as #15's: no rendering engine available this session.

## Session 2026-08-10: consistency measurement (task #12)

Base commit: d793e5b

### Scope

Task #12, unblocked by Tom following task #10's round-3 finding of real
single-run recall variance on km-sushi-noodles-kitchen. Spend cap $1
(Tom-approved, confirmed to this session directly, same standing as task
#10's cap). Measure item-count consistency and ingredient F1 spread
across 3 repeat runs each on km-sushi-nigiri (densest) and
km-sushi-sashimi (ugliest, per the card).

### Found before spending anything: --repeat is a documented no-op

`evals/run_evals.py` declares `--repeat` as a CLI argument (line 2025),
names it in the usage banner ("`--all --repeat 3` # consistency runs",
line 22), and the gate config carries `consistency_f1_spread_max: 0.03`
(line 106) as if consistency measurement were implemented. It is not:
`args.repeat` is never read anywhere in `cmd_run` or the rest of the file
(confirmed by grep, zero usages). Running the task as literally specified
would have silently executed as a single run per menu and spent money on
data that could not answer the task's actual question.

Not treated as a harness bug to fix under this card's budget: worked
around instead, using the same hand-aggregation technique already
precedented in this BUILDLOG (P1-SB2's supplementary aggregation, task
#10's control run): 3 independent manual invocations of `--menu
km-sushi-nigiri` and 3 of `--menu km-sushi-sashimi`, each its own
timestamp, aggregated by hand. Same spend, same deliverable as what
`--repeat 3` was supposed to produce. The no-op itself is flagged here as
a real gap for a future harness-hardening card, not patched in place.

### Results

Commands run exactly, 6 total:
```
uv run evals/run_evals.py --menu km-sushi-nigiri --timestamp 2026-08-10-p1-repeat-nigiri-r{1,2,3}
uv run evals/run_evals.py --menu km-sushi-sashimi --timestamp 2026-08-10-p1-repeat-sashimi-r{1,2,3}
```

**km-sushi-nigiri**, 3 runs:

| Run | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| r1 | 41/41 | 1.000 | 1.000 | 0.898 | 0.951 | 0.927 |
| r2 | 41/41 | 1.000 | 1.000 | 0.873 | 0.951 | 0.927 |
| r3 | 41/41 | 1.000 | 1.000 | 0.849 | 0.951 | 0.927 |

Item count, recall, precision, price accuracy, and wrap accuracy are
bit-identical across all 3 runs. Ingredient F1 macro spread: 0.898 -
0.849 = **0.049, exceeds the 0.03 consistency gate.**

**km-sushi-sashimi**, 3 runs:

| Run | Items (pred/gold) | Recall | Precision | Ing F1 (macro) | Price acc | Wrap acc |
|---|---|---|---|---|---|---|
| r1 | 12/12 | 1.000 | 1.000 | 0.961 | 1.000 | 1.000 |
| r2 | 12/12 | 1.000 | 1.000 | 0.950 | 1.000 | 1.000 |
| r3 | 12/12 | 1.000 | 1.000 | 0.961 | 1.000 | 1.000 |

Same pattern: item count, recall, precision, price, and wrap accuracy
identical across all 3 runs. Ingredient F1 macro spread: 0.961 - 0.950 =
**0.011, within the 0.03 consistency gate.**

Total cost: nigiri $0.0500 + $0.0273 + $0.0276 = $0.1049; sashimi $0.0318
+ $0.0112 + $0.0117 = $0.0547. **$0.1596 of the $1 cap.**

### Reading, feeding back into task #10's blocker

Item count, recall, and precision are perfectly reproducible on both of
these menus, three runs each, zero variance. That is a meaningfully
different picture than task #10's noodles-kitchen finding (recall itself
swinging 0.267 to 0.333): these two menus already score near-perfect on
the baseline, and at that quality level the harness's extraction is
completely stable on item-level metrics. The instability that does exist
is narrower and metric-specific: ingredient F1 macro alone wobbles run to
run, and by how much depends on the menu, not a fixed constant, 0.049 on
the denser nigiri menu (over the 0.03 gate on its own, before any prompt
edit is even in the picture) against 0.011 on sashimi (comfortably
inside it).

This does not resolve task #10's blocker on its own; it sharpens the
question. A single-run verification is unsafe to trust specifically for
ingredient F1 deltas on dense/repetitive menus (nigiri-shaped: many
items sharing overlapping ingredient vocabulary), and that unsafety is
not uniform across the menu set the way a single global noise-floor
number would suggest. Item-count and recall/precision deltas, by
contrast, look trustworthy on a single run for menus already this close
to the gate. Task #10's own targets (precision on km-sushi-dinner and
km-sushi-noodles-kitchen, price carry-down) are recall/precision/price
questions, not ingredient F1 questions, so this specific consistency data
does not directly cover the metric task #10 was actually trying to move,
though the general lesson (verify against a menu-specific noise floor,
not a single global assumption) still applies.

### Manifest (files touched, this commit)

- `evals/reports/2026-08-10-p1-repeat-nigiri-r{1,2,3}.md`: written by the
  harness, unmodified after.
- `evals/reports/2026-08-10-p1-repeat-sashimi-r{1,2,3}.md`: written by the
  harness, unmodified after.
- `docs/BUILDLOG.md`: this entry.
- Not touched: `evals/run_evals.py` (the `--repeat` no-op is flagged, not
  fixed, per this card's scope), `shared/*`, `src/*`, `public/*`,
  `evals/menus/*/golden.json`.

### Patterns established

- A flag can be fully wired into a script's help text, usage examples, and
  even its own gate-threshold configuration while doing literally nothing
  at runtime. `grep` for the argument's actual read sites, not just its
  declaration, before trusting a documented flag exists to do what its
  name and help string claim.
- Consistency/noise-floor data is menu-specific and metric-specific, not
  a single number that generalizes. Two menus with identical item-level
  stability (0 variance) can still differ by 4x on ingredient-F1 spread.
  A future consistency measurement should not assume one menu's noise
  floor stands in for the whole golden set's.

### Done-when, walked item by item

1. Three repeat runs land for each of km-sushi-nigiri and km-sushi-
   sashimi, within the $1 cap: done, $0.1596 spent, all 6 reports
   committed.
2. Report per-menu item-count consistency and ingredient F1 spread: done,
   tables above, both computed by hand from the harness's own per-menu
   breakdown rows (the same accepted method as P1-SB2's aggregation).
3. Findings feed back into task #10's blocker: done, with the caveat
   made explicit that this data covers ingredient F1 stability
   specifically, not the recall/precision/price questions task #10's own
   prompt-fix targets actually turn on.

### Single next action

Task #10 stays blocked; this data is evidence for Tom/oversight to weigh
when deciding whether/how to reopen it, not an automatic unblock. The
`--repeat` no-op is a real, separate finding worth its own harness-
hardening card if consistency measurement is going to be run again
without hand-aggregating every time.
