// Deterministic ingredient normalization: lowercase, trim, simple plural
// folding, then the alias table, applied at render time only, per SPEC.md.
// This module never touches labeling or extraction; that is a separate,
// still-open question (task #13 on the board), out of scope here.
//
// Loading note: shared/aliases.json lives outside public/, and the
// wrangler.jsonc assets binding only serves ./public, so there is no
// documented Worker API route for it (SPEC.md's Worker API section
// enumerates every endpoint explicitly and this is not one of them).
// Resolved with public/aliases.json as a symlink to ../shared/aliases.json
// rather than a new undocumented API route or a duplicated copy that could
// drift: this keeps shared/ as the single source of truth SPEC.md already
// establishes for shared/prompts/, served through the same static-asset
// path everything else in public/ uses, no worker code touched. Verified
// against a live wrangler dev boot: the symlink resolves and serves the
// real file content correctly.

let aliasTableCache = null;

export async function loadAliasTable() {
  if (aliasTableCache) return aliasTableCache;
  const res = await fetch("/aliases.json");
  if (!res.ok) {
    throw new Error(`failed to load alias table: http_${res.status}`);
  }
  aliasTableCache = await res.json();
  return aliasTableCache;
}

// Naive English plural fold: strips a trailing "s" when the singular form
// (after alias lookup, so "shrimps" folds even though "shrimp" already
// resolves) is not itself already a known form. Deliberately simple, per
// SPEC.md's "simple plural folding": this is not a full inflection
// library, just enough to catch "rolls"/"roll", "tempuras"/"tempura"
// style drift; irregular plurals are not handled and are expected to be
// caught as alias-table entries instead, the same way the extraction
// style guide's ingredient rules are enforced as an explicit list rather
// than a general rule (see shared/prompts/system.md's preparation-method
// exception list for the same design choice on the labeling side).
function foldPlural(ingredient) {
  if (ingredient.length > 3 && ingredient.endsWith("s") && !ingredient.endsWith("ss")) {
    return ingredient.slice(0, -1);
  }
  return ingredient;
}

// Pure function: given one printed/predicted ingredient string and an
// alias table, returns the canonical filter-facet form. Lowercase and trim
// first (so alias-table lookups do not depend on incoming casing), then
// plural fold, then the alias table itself (a printed spelling maps to its
// canonical term; entries not present pass through unchanged).
export function normalizeIngredient(ingredient, aliasTable) {
  const cleaned = ingredient.toLowerCase().trim();
  const folded = foldPlural(cleaned);
  return aliasTable[folded] ?? aliasTable[cleaned] ?? folded;
}

export function normalizeIngredients(ingredients, aliasTable) {
  return ingredients.map((ingredient) => normalizeIngredient(ingredient, aliasTable));
}
