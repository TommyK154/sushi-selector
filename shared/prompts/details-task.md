# Details pass task instruction

This is a details pass. You have just been shown the same menu photo used in
this job's index pass, again as the first content block with a prompt-cache
breakpoint, so the image tokens for this photo are shared and cached across
every details batch for this job. Following the image, you are given a batch
of up to 10 items already identified on this photo by the index pass, as a
list of `{ "n": <integer>, "name": "<string>" }` pairs. Your job in this pass
is ingredient-level: for exactly the items in this batch, locate them on the
photo by their printed name and position, and extract their ingredients,
wrap, and raw/cooked status.

Produce a single JSON object that validates against
`shared/schema/details.schema.json`, with one entry in `items` for every item
in this batch's input list (same count, same `n` values, none added, none
skipped):

- `n`: copy the same `n` given for this item in the input batch.
- `name`: copy the same `name` given for this item in the input batch.
- `ingredients`: the canonical lowercase singular ingredient list for this
  item, per every rule in the style guide's ingredient naming section
  (compound preparations stay whole, preparation methods strip except the
  closed exception list, roe uses the menu term, egg is canonical over
  tamago, crab is never normalized, species qualifiers stay local to this
  item, vague collective terms go to notes instead, rice is never listed).
- `wrap`: exactly one of `nori`, `soy_paper`, `rice_paper`, `none`, or
  `unknown`, per the style guide's wrap rules.
- `is_raw`: `true`, `false`, or `null`, per the style guide's is_raw rules,
  including the seared-fish-is-raw case and the shrimp and octopus cooked
  defaults.
- `notes`: any modifiers, caveats, vague collective descriptions, or combo
  choice-set descriptions printed for this item, or `null` if there is
  nothing to note. If this item's ingredients were inferred from standard
  sushi knowledge rather than printed on the menu, `notes` must contain the
  literal token `INFERRED`.

Look only at what is printed for this specific item; never import a
qualifier or ingredient from a different item on the same photo, even one
that looks similar. Return only the JSON object, no commentary, no markdown
fences.
