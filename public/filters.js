// Pure filter/sort/search functions. No DOM access here, per SPEC.md's
// separation: ui.js owns rendering and the chip list, this module owns the
// logic that decides which items show and in what order. Every function
// here takes plain data in and returns plain data out, so it is testable
// and reviewable without a browser.

export const CHIP_STATE = Object.freeze({
  NEUTRAL: "neutral",
  INCLUDE: "include",
  EXCLUDE: "exclude",
});

// Tri-state cycle: tap advances neutral -> include -> exclude -> neutral.
export function nextChipState(current) {
  if (current === CHIP_STATE.NEUTRAL) return CHIP_STATE.INCLUDE;
  if (current === CHIP_STATE.INCLUDE) return CHIP_STATE.EXCLUDE;
  return CHIP_STATE.NEUTRAL;
}

// filterState shape: { chips: Map<canonicalIngredient, CHIP_STATE>, wrap:
// wrapEnumValue|null, isRaw: true|false|null }. null/neutral means no
// constraint from that facet.
export function createFilterState() {
  return { chips: new Map(), wrap: null, isRaw: null };
}

function includedIngredients(filterState) {
  const included = [];
  for (const [ingredient, state] of filterState.chips) {
    if (state === CHIP_STATE.INCLUDE) included.push(ingredient);
  }
  return included;
}

function excludedIngredients(filterState) {
  const excluded = [];
  for (const [ingredient, state] of filterState.chips) {
    if (state === CHIP_STATE.EXCLUDE) excluded.push(ingredient);
  }
  return excluded;
}

// Include semantics: item must contain ALL included ingredients. Exclude:
// item must contain NONE of the excluded ones. wrap and is_raw are
// dedicated chips, not part of the ingredient set, per SPEC.md.
export function applyFilters(items, filterState) {
  const included = includedIngredients(filterState);
  const excluded = excludedIngredients(filterState);

  return items.filter((item) => {
    const ingredientSet = new Set(item.ingredients);
    for (const ingredient of included) {
      if (!ingredientSet.has(ingredient)) return false;
    }
    for (const ingredient of excluded) {
      if (ingredientSet.has(ingredient)) return false;
    }
    if (filterState.wrap != null && item.wrap !== filterState.wrap) return false;
    if (filterState.isRaw != null && item.is_raw !== filterState.isRaw) return false;
    return true;
  });
}

// True when no chip, wrap, or is_raw constraint is active, i.e. the filter
// drawer would show everything. Useful for ui.js to decide whether to show
// a "clear filters" affordance.
export function isFilterStateEmpty(filterState) {
  if (filterState.wrap != null || filterState.isRaw != null) return false;
  for (const state of filterState.chips.values()) {
    if (state !== CHIP_STATE.NEUTRAL) return false;
  }
  return true;
}

// Item search: case-insensitive substring across name and ingredients, per
// SPEC.md. Distinct from the chip-list search below, which filters the
// facet list itself, not the item results.
export function searchItems(items, query) {
  const trimmed = query.trim().toLowerCase();
  if (!trimmed) return items;
  return items.filter((item) => {
    if (item.name.toLowerCase().includes(trimmed)) return true;
    return item.ingredients.some((ingredient) => ingredient.toLowerCase().includes(trimmed));
  });
}

// Filters the ingredient chip vocabulary itself, for the search box at the
// top of the filter drawer (SPEC.md: "a search box that filters the
// ingredient chip list itself").
export function filterChipVocabulary(vocabulary, query) {
  const trimmed = query.trim().toLowerCase();
  if (!trimmed) return vocabulary;
  return vocabulary.filter((ingredient) => ingredient.toLowerCase().includes(trimmed));
}

export const SORT_MODE = Object.freeze({
  MENU: "menu",
  PRICE_ASC: "price-asc",
  PRICE_DESC: "price-desc",
});

// Menu order is the input order (the merge in app.js already establishes
// photo-then-reading order); price sorts sink null-price items to the
// bottom, per SPEC.md, and never mutate the input array.
export function sortItems(items, mode) {
  if (mode === SORT_MODE.MENU) return [...items];

  const priced = items.filter((item) => item.price != null);
  const unpriced = items.filter((item) => item.price == null);
  priced.sort((a, b) => (mode === SORT_MODE.PRICE_ASC ? a.price - b.price : b.price - a.price));
  return [...priced, ...unpriced];
}

// Builds the ingredient vocabulary for the filter drawer's chip list: every
// distinct ingredient across the current item set, alphabetical, so the
// list is stable and scannable.
export function buildIngredientVocabulary(items) {
  const seen = new Set();
  for (const item of items) {
    for (const ingredient of item.ingredients) seen.add(ingredient);
  }
  return [...seen].sort();
}
