# Index pass task instruction

This is the index pass. You have just been shown one menu photo as the first
content block of this message, with a prompt-cache breakpoint on that image
block. Your job in this pass is structural: read every item on the page and
report its name, section, and price, in reading order. You are not extracting
ingredients, wrap, or is_raw in this pass; that happens in a later details
pass over batches of the items you report here, so do not include or invent
those fields now.

Produce a single JSON object that validates against
`shared/schema/index.schema.json`, with these top-level fields:

- `restaurant_name`: the restaurant's name, only if it is literally printed
  somewhere in this photo, per the style guide's restaurant_name rule.
  Otherwise `null`.
- `sections`: the ordered list of section headers actually printed on this
  page (for example "Nigiri", "Special Rolls", "Lunch Combos"). Each entry is
  an object with just a `name` string. If the page has no printed section
  headers at all, return an empty array rather than inventing one.
- `items`: every menu item visible on the page, in reading order, each with:
  - `n`: a 1-based reading-order index. Assign this carefully and stably; the
    details pass will reference items by this same number against this same
    photo, so it must not shift between passes.
  - `name`: the item name as printed.
  - `section`: the name of the section this item falls under (matching one
    of the strings in `sections`), or `null` if the item is not under any
    printed section header.
  - `price_text`: the verbatim price string as printed, or `null` if no price
    is printed or it is illegible.
  - `price`: the parsed numeric price, or `null` per the style guide's price
    rules (market price, illegible, ambiguous multi-size pricing).

Follow the reading-order and legibility guidance in the system prompt: read
around glare, rotation, and lamination artifacts rather than skipping
sections, and never guess a price or name that cannot actually be read. Skip
beverage-only lines entirely, per the style guide. Return only the JSON
object, no commentary, no markdown fences.
