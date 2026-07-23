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
