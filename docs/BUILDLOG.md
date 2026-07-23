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
