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
