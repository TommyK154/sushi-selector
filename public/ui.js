// Rendering, filter sheet, cards, Omakase. Owns the DOM; app.js (the state
// machine) and filters.js/aliases.js (pure logic) know nothing about the
// DOM, per SPEC.md's file split. No framework, no bundler: this file
// renders by direct DOM construction, using textContent (never innerHTML
// with interpolated strings) for anything derived from menu content, since
// item names/ingredients/notes come from a vision model reading a photo
// and are not trusted input.

import { JobController, STATES, saveMenu } from "./app.js";
import {
  applyFilters,
  searchItems,
  sortItems,
  SORT_MODE,
  CHIP_STATE,
  nextChipState,
  buildIngredientVocabulary,
  createFilterState,
  isFilterStateEmpty,
  filterChipVocabulary,
} from "./filters.js";
import { loadAliasTable, normalizeIngredients } from "./aliases.js";

// --------------------------------------------------------------------------
// Tiny DOM helper. Not a framework: no diffing, no components, just less
// boilerplate for the manual createElement calls this file needs a lot of.
// --------------------------------------------------------------------------

function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key.startsWith("on") && typeof value === "function") {
      node.addEventListener(key.slice(2).toLowerCase(), value);
    } else if (value !== null && value !== undefined) {
      node.setAttribute(key, value);
    }
  }
  for (const child of [].concat(children)) {
    if (child == null) continue;
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return node;
}

function clear(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
}

// --------------------------------------------------------------------------
// App state (not persisted directly; app.js's job object is the
// source of truth for anything that survives a reload).
// --------------------------------------------------------------------------

const state = {
  screen: "home", // "home" | "progress" | "menu"
  pendingFiles: [],
  menu: null, // { restaurantName, items } once a job reaches READY, ingredients normalized
  filterState: createFilterState(),
  searchQuery: "",
  sortMode: SORT_MODE.MENU,
  filterSheetOpen: false,
  omakaseQueue: null, // null = not yet shuffled; [] = shuffled and exhausted (see resetOmakaseQueue)
  omakasePickId: null,
  omakaseExhausted: false,
  aliasTable: null,
  turnstileSiteKey: null,
  turnstileWidgetId: null,
  correctionItemId: null, // id of the item currently open in the fix-ingredients sheet, or null
  canRetryItems: false, // true only for a job completed this page load (see JobController.photoImages)
};

const controller = new JobController();
const app = document.getElementById("app");

function render() {
  clear(app);
  if (state.screen === "home") app.appendChild(renderHome());
  else if (state.screen === "progress") app.appendChild(renderProgress());
  else if (state.screen === "menu") app.appendChild(renderMenuScreen());

  if (state.filterSheetOpen) app.appendChild(renderFilterSheet());
  if (state.correctionItemId) app.appendChild(renderCorrectionSheet());
}

controller.subscribe((jobState, job) => {
  if (jobState === STATES.READY) {
    onJobReady(job);
    return;
  }
  if (jobState === STATES.ERROR) {
    state.screen = "progress";
    render();
    return;
  }
  if (jobState !== STATES.IDLE) {
    state.screen = "progress";
    render();
  }
});

async function onJobReady(job) {
  if (!state.aliasTable) state.aliasTable = await loadAliasTable();
  const items = job.items.map((item) => ({
    ...item,
    ingredients: normalizeIngredients(item.ingredients, state.aliasTable),
  }));
  const restaurantName = job.restaurantName;
  const slug = slugify(restaurantName);
  const menu = { restaurantName, items, savedAt: Date.now() };
  saveMenu(slug, menu);

  state.menu = menu;
  state.filterState = createFilterState();
  state.searchQuery = "";
  state.sortMode = SORT_MODE.MENU;
  state.omakaseQueue = null;
  state.omakasePickId = null;
  state.omakaseExhausted = false;
  state.canRetryItems = true; // this job's photoImages are live in the controller, same page load
  state.screen = "menu";
  render();
}

function slugify(name) {
  if (!name) return `menu-${new Date().toISOString().slice(0, 10)}`;
  return name
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

// --------------------------------------------------------------------------
// Home screen: capture flow (photo or URL, never both), recent menus.
// --------------------------------------------------------------------------

function renderHome() {
  const container = el("main", { class: "screen" });

  container.appendChild(
    el("header", { class: "app-header" }, [
      el("h1", { class: "app-title", text: "Sushi Selector" }),
      el("p", { class: "app-tagline", text: "Snap the menu, filter the raw stuff out." }),
    ]),
  );

  const thumbList = el("div", { class: "thumb-list" });
  renderThumbs(thumbList);

  const fileInput = el("input", {
    type: "file",
    accept: "image/*",
    multiple: "multiple",
    capture: "environment",
    class: "sr-only",
    id: "photo-input",
    onchange: (e) => {
      const incoming = Array.from(e.target.files || []);
      const combined = [...state.pendingFiles, ...incoming].slice(0, 6);
      state.pendingFiles = combined;
      renderThumbs(thumbList);
    },
  });

  const urlInput = el("input", {
    type: "url",
    id: "menu-url",
    class: "text-input",
    placeholder: "Or paste a menu page URL",
    "aria-label": "Menu page URL",
  });

  const parseButton = el("button", {
    class: "primary-action",
    type: "button",
    text: `Parse ${state.pendingFiles.length || ""} photo${state.pendingFiles.length === 1 ? "" : "s"}`.trim(),
    onclick: () => startParse(urlInput.value.trim()),
  });
  parseButton.disabled = state.pendingFiles.length === 0 && !urlInput.value;
  urlInput.addEventListener("input", () => {
    parseButton.disabled = state.pendingFiles.length === 0 && !urlInput.value.trim();
  });

  const turnstileMount = el("div", { id: "turnstile-container", class: "turnstile-mount" });

  container.appendChild(
    el("section", { id: "home", class: "panel", "aria-label": "Capture" }, [
      el("label", { for: "photo-input", class: "capture-cta" }, "Take or choose photos"),
      fileInput,
      thumbList,
      el("div", { class: "url-alt" }, [urlInput]),
      turnstileMount,
      parseButton,
    ]),
  );

  container.appendChild(renderRecentMenus());

  queueMicrotask(() => mountTurnstile(turnstileMount));
  return container;
}

function renderThumbs(thumbList) {
  clear(thumbList);
  state.pendingFiles.forEach((file, index) => {
    const url = URL.createObjectURL(file);
    const thumb = el("div", { class: "thumb" }, [
      el("img", { src: url, alt: `Photo ${index + 1}`, class: "thumb-img" }),
      el("button", {
        class: "thumb-remove",
        type: "button",
        "aria-label": `Remove photo ${index + 1}`,
        text: "×",
        onclick: () => {
          state.pendingFiles = state.pendingFiles.filter((_, i) => i !== index);
          renderThumbs(thumbList);
        },
      }),
    ]);
    thumbList.appendChild(thumb);
  });
}

function renderRecentMenus() {
  const menus = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (!key || !key.startsWith("ss:menu:")) continue;
    try {
      const menu = JSON.parse(localStorage.getItem(key));
      menus.push({ slug: key.slice("ss:menu:".length), menu });
    } catch {
      // A corrupted entry from a previous version should not crash the
      // home screen; skip it rather than surface raw parse errors.
    }
  }
  menus.sort((a, b) => (b.menu.savedAt || 0) - (a.menu.savedAt || 0));

  if (menus.length === 0) return el("section", { class: "panel" });

  return el("section", { class: "panel recent-menus", "aria-label": "Recent menus" }, [
    el("h2", { class: "section-title", text: "Recent" }),
    el(
      "ul",
      { class: "recent-list" },
      menus.map(({ slug, menu }) =>
        el("li", {}, [
          el("button", {
            class: "recent-item",
            type: "button",
            text: menu.restaurantName || `Menu, ${new Date(menu.savedAt).toLocaleDateString()}`,
            onclick: async () => {
              // The alias table is needed for corrections (applyCorrection
              // normalizes through it) and was previously only loaded on
              // the live-parse path (onJobReady); reopening a menu from
              // Recent skipped it entirely, a real bug caught by task
              // #16's jsdom verification (correcting an item crashed on a
              // null alias table). Same load-once guard as onJobReady.
              if (!state.aliasTable) state.aliasTable = await loadAliasTable();
              state.menu = menu;
              state.filterState = createFilterState();
              state.searchQuery = "";
              state.sortMode = SORT_MODE.MENU;
              state.omakaseQueue = null;
              state.omakasePickId = null;
              state.omakaseExhausted = false;
              state.canRetryItems = false; // reopened from ss:menu:*, its photos are not in memory
              state.screen = "menu";
              render();
            },
          }),
        ]),
      ),
    ),
  ]);
}

async function mountTurnstile(container) {
  if (state.turnstileSiteKey === null) {
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      state.turnstileSiteKey = data.turnstileSiteKey || "";
    } catch {
      state.turnstileSiteKey = "";
    }
  }
  if (!state.turnstileSiteKey || typeof window.turnstile === "undefined") {
    // Degrade visibly rather than silently: the parse button stays enabled
    // (start() will surface the real Turnstile failure from the server if
    // a token is genuinely required and missing) but the widget mount
    // shows why nothing rendered, for local dev without real keys.
    container.appendChild(
      el("p", { class: "turnstile-unavailable", text: "Verification widget unavailable (no site key configured)." }),
    );
    return;
  }
  state.turnstileWidgetId = window.turnstile.render(container, { sitekey: state.turnstileSiteKey });
}

async function startParse(url) {
  state.screen = "progress";
  render();
  try {
    const turnstileToken =
      state.turnstileWidgetId != null ? window.turnstile.getResponse(state.turnstileWidgetId) : "";
    if (url) {
      // URL-path parsing is app.js's future extension point; this build
      // covers the photo path per SPEC.md's primary flow. Surfacing the
      // gap plainly rather than pretending to submit it.
      throw new Error("url_path_not_yet_wired");
    }
    await controller.start(state.pendingFiles, turnstileToken || "");
  } catch (err) {
    state.screen = "progress";
    render();
  }
}

// --------------------------------------------------------------------------
// Progress screen
// --------------------------------------------------------------------------

const STATE_LABEL = {
  [STATES.PREPROCESS]: "Preparing photos",
  [STATES.INDEX]: "Reading the menu",
  [STATES.DETAILS]: "Reading ingredients",
  [STATES.RECONCILE]: "Putting it together",
  [STATES.ERROR]: "Something went wrong",
};

function renderProgress() {
  const job = controller.job;
  const jobState = controller.state;

  if (jobState === STATES.ERROR) {
    return el("main", { class: "screen" }, [
      el("section", { class: "panel error-panel", role: "alert" }, [
        el("p", { class: "error-message", text: "The kitchen is slammed, try again in a bit." }),
        el("button", {
          class: "primary-action",
          type: "button",
          text: "Retry",
          onclick: () => {
            state.screen = "home";
            render();
          },
        }),
      ]),
    ]);
  }

  const total = job ? job.perPhotoIndex.length : state.pendingFiles.length;
  const completed = job ? job.perPhotoIndex.filter(Boolean).length : 0;

  return el("main", { class: "screen" }, [
    el("section", { class: "panel progress-panel", "aria-live": "polite" }, [
      el("p", { class: "progress-label", text: STATE_LABEL[jobState] || "Working" }),
      el("p", { class: "progress-detail", text: total > 1 ? `Photo ${Math.min(completed + 1, total)} of ${total}` : "" }),
    ]),
  ]);
}

// --------------------------------------------------------------------------
// Menu screen: search, sort, filter trigger, item list, Omakase.
// --------------------------------------------------------------------------

function visibleItems() {
  const { items } = state.menu;
  const searched = searchItems(items, state.searchQuery);
  const filtered = applyFilters(searched, state.filterState);
  return sortItems(filtered, state.sortMode);
}

function renderMenuScreen() {
  const container = el("main", { class: "screen menu-screen" });
  const items = visibleItems();

  const searchInput = el("input", {
    type: "search",
    class: "text-input search-input",
    placeholder: "Search this menu",
    "aria-label": "Search menu",
    value: state.searchQuery,
    oninput: (e) => {
      state.searchQuery = e.target.value;
      resetOmakaseQueue();
      renderList();
      renderOmakaseButton();
    },
  });

  const sortToggle = el("button", {
    class: "sort-toggle",
    type: "button",
    text: sortLabel(state.sortMode),
    onclick: () => {
      state.sortMode = nextSortMode(state.sortMode);
      sortToggle.textContent = sortLabel(state.sortMode);
      renderList();
    },
  });

  const filterButton = el("button", {
    class: "filter-trigger",
    type: "button",
    text: isFilterStateEmpty(state.filterState) ? "Filters" : "Filters •",
    onclick: () => {
      state.filterSheetOpen = true;
      render();
    },
  });

  const topBar = el("div", { class: "menu-topbar" }, [searchInput, sortToggle, filterButton]);
  const list = el("div", { class: "item-list", id: "item-list" });
  const omakaseSlot = el("div", { class: "omakase-slot" });

  function renderList() {
    clear(list);
    const current = visibleItems();
    if (current.length === 0) {
      list.appendChild(
        el("p", { class: "zero-results", text: "No rolls match these filters. Loosen one to see more." }),
      );
      return;
    }
    for (const item of current) {
      list.appendChild(renderCard(item));
    }
  }

  function renderOmakaseButton() {
    clear(omakaseSlot);
    if (visibleItems().length === 0) return;
    omakaseSlot.appendChild(
      el("button", {
        class: "omakase-button",
        type: "button",
        "aria-label": "Omakase, chef's pick",
        text: "🍣",
        onclick: onOmakasePress,
      }),
    );
  }

  renderList();
  renderOmakaseButton();

  container.appendChild(topBar);
  container.appendChild(list);
  container.appendChild(omakaseSlot);
  container.appendChild(renderOmakaseExhaustion());

  // Expose for the search/sort handlers above, defined before this point
  // in closure scope; re-render hooks assigned here so they see the latest
  // `list`/`omakaseSlot` nodes for this render pass.
  container._renderList = renderList;
  container._renderOmakaseButton = renderOmakaseButton;
  currentMenuRenderHooks = { renderList, renderOmakaseButton };

  return container;
}

let currentMenuRenderHooks = null;

function sortLabel(mode) {
  if (mode === SORT_MODE.PRICE_ASC) return "Price ↑";
  if (mode === SORT_MODE.PRICE_DESC) return "Price ↓";
  return "Menu order";
}

function nextSortMode(mode) {
  if (mode === SORT_MODE.MENU) return SORT_MODE.PRICE_ASC;
  if (mode === SORT_MODE.PRICE_ASC) return SORT_MODE.PRICE_DESC;
  return SORT_MODE.MENU;
}

function renderCard(item) {
  const badges = [];
  if (item.is_raw === true) badges.push(el("span", { class: "badge badge-raw", text: "raw" }));
  if (item.wrap && item.wrap !== "none" && item.wrap !== "unknown") {
    badges.push(el("span", { class: "badge badge-wrap", text: item.wrap.replace("_", " ") }));
  }
  if (item.flagged) badges.push(el("span", { class: "badge badge-flag", text: "needs review" }));
  else if (item.edited) badges.push(el("span", { class: "badge badge-edited", text: "edited" }));

  const query = state.searchQuery.trim().toLowerCase();
  const ingredientNodes = item.ingredients.map((ingredient) => {
    const matched = query.length > 0 && ingredient.toLowerCase().includes(query);
    return el("li", { class: matched ? "ingredient matched" : "ingredient", text: ingredient });
  });

  const priceNode = el(
    "span",
    { class: "item-price" },
    item.price != null ? `$${item.price.toFixed(2)}` : item.price_text || "",
  );

  const children = [
    el("div", { class: "item-card-header" }, [
      el("h3", { class: "item-name", text: item.name }),
      priceNode,
    ]),
    badges.length > 0 ? el("div", { class: "badge-row" }, badges) : null,
    el("ul", { class: "ingredient-list" }, ingredientNodes),
  ];

  if (item.flagged) {
    children.push(
      el("button", {
        class: "secondary-action fix-ingredients-trigger",
        type: "button",
        text: "Fix ingredients",
        onclick: () => openCorrectionSheet(item.id),
      }),
    );
  }

  return el("article", { class: "item-card", "data-item-id": item.id }, children);
}

// --------------------------------------------------------------------------
// Filter bottom sheet
// --------------------------------------------------------------------------

function renderFilterSheet() {
  const overlay = el("div", { class: "sheet-overlay", role: "presentation" });
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closeFilterSheet();
  });

  const vocabulary = buildIngredientVocabulary(state.menu.items);
  const chipSearch = el("input", {
    type: "search",
    class: "text-input chip-search",
    placeholder: "Search ingredients",
    "aria-label": "Search ingredient filters",
  });

  const chipList = el("div", { class: "chip-list", role: "group", "aria-label": "Ingredient filters" });

  function renderChips(filterQuery) {
    clear(chipList);
    for (const ingredient of filterChipVocabulary(vocabulary, filterQuery)) {
      const currentState = state.filterState.chips.get(ingredient) || CHIP_STATE.NEUTRAL;
      const chip = el("button", {
        type: "button",
        class: `chip chip-${currentState}`,
        text: ingredient,
        "aria-pressed": currentState !== CHIP_STATE.NEUTRAL ? "true" : "false",
        onclick: () => {
          const updated = nextChipState(currentState);
          if (updated === CHIP_STATE.NEUTRAL) state.filterState.chips.delete(ingredient);
          else state.filterState.chips.set(ingredient, updated);
          chip.className = `chip chip-${updated}`;
          chip.setAttribute("aria-pressed", updated !== CHIP_STATE.NEUTRAL ? "true" : "false");
          resetOmakaseQueue();
        },
      });
      chipList.appendChild(chip);
    }
  }
  renderChips("");
  chipSearch.addEventListener("input", (e) => renderChips(e.target.value));

  const wrapRow = el(
    "div",
    { class: "facet-row", role: "group", "aria-label": "Wrap" },
    ["nori", "soy_paper", "rice_paper", "none"].map((wrap) =>
      el("button", {
        type: "button",
        class: `chip ${state.filterState.wrap === wrap ? "chip-include" : "chip-neutral"}`,
        text: wrap.replace("_", " "),
        onclick: (e) => {
          state.filterState.wrap = state.filterState.wrap === wrap ? null : wrap;
          resetOmakaseQueue();
          renderFilterSheetInPlace();
        },
      }),
    ),
  );

  const rawRow = el("div", { class: "facet-row", role: "group", "aria-label": "Raw or cooked" }, [
    el("button", {
      type: "button",
      class: `chip ${state.filterState.isRaw === true ? "chip-include" : "chip-neutral"}`,
      text: "raw",
      onclick: () => {
        state.filterState.isRaw = state.filterState.isRaw === true ? null : true;
        resetOmakaseQueue();
        renderFilterSheetInPlace();
      },
    }),
    el("button", {
      type: "button",
      class: `chip ${state.filterState.isRaw === false ? "chip-include" : "chip-neutral"}`,
      text: "cooked",
      onclick: () => {
        state.filterState.isRaw = state.filterState.isRaw === false ? null : false;
        resetOmakaseQueue();
        renderFilterSheetInPlace();
      },
    }),
  ]);

  const sheet = el("div", { class: "sheet", role: "dialog", "aria-modal": "true", "aria-label": "Filters" }, [
    el("div", { class: "sheet-handle" }),
    chipSearch,
    chipList,
    el("h3", { class: "section-title", text: "Wrap" }),
    wrapRow,
    el("h3", { class: "section-title", text: "Raw or cooked" }),
    rawRow,
    el("button", { class: "primary-action sheet-done", type: "button", text: "Done", onclick: closeFilterSheet }),
  ]);

  overlay.appendChild(sheet);
  return overlay;
}

function renderFilterSheetInPlace() {
  const existing = document.querySelector(".sheet-overlay");
  if (!existing) return;
  const fresh = renderFilterSheet();
  existing.replaceWith(fresh);
}

function closeFilterSheet() {
  state.filterSheetOpen = false;
  render();
  if (currentMenuRenderHooks) {
    currentMenuRenderHooks.renderList();
    currentMenuRenderHooks.renderOmakaseButton();
  }
}

// --------------------------------------------------------------------------
// Omakase: no-repeat shuffle over the currently visible items.
// --------------------------------------------------------------------------

function shuffledIds(items) {
  const ids = items.map((item) => item.id);
  for (let i = ids.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [ids[i], ids[j]] = [ids[j], ids[i]];
  }
  return ids;
}

function resetOmakaseQueue() {
  // null means "no queue built yet, shuffle a fresh one on next press";
  // [] means "a queue was built and every item in it has been shown",
  // a genuinely different state (queue null and queue empty must not
  // collapse to the same check, see onOmakasePress: that was a real bug,
  // caught by the jsdom verification pass, where an empty-after-shift
  // queue silently reshuffled itself instead of ever reaching exhaustion).
  state.omakaseQueue = null;
  state.omakasePickId = null;
  state.omakaseExhausted = false;
}

function onOmakasePress() {
  if (state.omakaseQueue === null) {
    state.omakaseQueue = shuffledIds(visibleItems());
  }
  if (state.omakaseQueue.length === 0) {
    state.omakaseExhausted = true;
    state.omakaseQueue = null; // ready to reshuffle on the next press (Second lap)
    render();
    return;
  }
  const nextId = state.omakaseQueue.shift();
  state.omakasePickId = nextId;

  if (currentMenuRenderHooks) currentMenuRenderHooks.renderList();
  revealPick(nextId);
}

function revealPick(itemId) {
  document.querySelectorAll(".item-card.omakase-pick").forEach((node) => node.classList.remove("omakase-pick"));
  const card = document.querySelector(`.item-card[data-item-id="${cssEscape(itemId)}"]`);
  if (!card) return;
  card.classList.add("omakase-pick");
  const tag = el("span", { class: "chefs-pick-tag", text: "chef's pick" });
  card.querySelector(".item-card-header").appendChild(tag);
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
}

function cssEscape(value) {
  return window.CSS && window.CSS.escape ? window.CSS.escape(value) : value.replace(/[":]/g, "\\$&");
}

function renderOmakaseExhaustion() {
  if (!state.omakaseExhausted) return el("div", {});
  return el("div", { class: "omakase-exhaustion panel", role: "status" }, [
    el("p", { text: "The chef has shown you everything. Trust your gut, or take a second lap." }),
    el("div", { class: "exhaustion-actions" }, [
      el("button", {
        class: "secondary-action",
        type: "button",
        text: "Second lap",
        onclick: () => {
          state.omakaseExhausted = false;
          state.omakaseQueue = shuffledIds(visibleItems());
          onOmakasePress();
        },
      }),
      el("button", {
        class: "secondary-action",
        type: "button",
        text: "Open filters",
        onclick: () => {
          state.omakaseExhausted = false;
          state.filterSheetOpen = true;
          render();
        },
      }),
    ]),
  ]);
}

// --------------------------------------------------------------------------
// Flagged-item correction: "Retry this item" (single-item details re-call)
// and "Fix ingredients" (tier 1/2/3 manual correction), per SPEC.md's
// RECONCILE handling.
// --------------------------------------------------------------------------

function findMenuItem(itemId) {
  return state.menu.items.find((item) => item.id === itemId) || null;
}

function openCorrectionSheet(itemId) {
  state.correctionItemId = itemId;
  render();
}

function closeCorrectionSheet() {
  state.correctionItemId = null;
  render();
}

// Applies an edited ingredient list to the item: runs it through the same
// normalization/alias pipeline every extracted ingredient goes through (so
// a hand-typed "Ebi" and a model-extracted "Ebi" land on the identical
// canonical facet), swaps the flagged marker for the edited marker, and
// persists the change with the cached menu, per SPEC.md.
function applyCorrection(item, newIngredients) {
  item.ingredients = normalizeIngredients(newIngredients, state.aliasTable);
  item.flagged = false;
  item.flagReason = null;
  item.edited = true;
  const slug = slugify(state.menu.restaurantName);
  saveMenu(slug, state.menu);
}

// "Retry this item": a real single-item /api/extract/details call, wired
// to the same endpoint every batch during the original parse used. Two
// honest, documented gaps, neither exercised live this session (per task
// #16's own scope, the same class of thing as #15's Turnstile-widget gap):
// (1) this needs a fresh session token, and there is no Turnstile widget
// mounted on the menu screen to solve a fresh challenge with, so the
// /api/session call below will reach the server with an empty token and
// fail turnstile_failed against a real deployment, exactly as it should;
// (2) it needs the original photo, only available when canRetryItems is
// true (this job completed in the current page load). Both failure paths
// are real, reachable code, not stubs: they render an honest inline error
// rather than pretending to succeed.
async function retryItem(item, statusNode) {
  const photoIndex = Number(item.id.split(":")[0]);
  const image = controller.getPhotoImage(photoIndex);
  if (!image) {
    statusNode.textContent =
      "This photo isn't available to retry (menu was reopened from Recent). Use Fix ingredients instead.";
    return;
  }
  statusNode.textContent = "Retrying…";
  try {
    const sessionRes = await fetch("/api/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ turnstileToken: "" }),
    });
    const sessionData = await sessionRes.json().catch(() => null);
    if (!sessionRes.ok) {
      throw new Error((sessionData && sessionData.error) || `http_${sessionRes.status}`);
    }
    const n = Number(item.id.split(":")[1]);
    const detailsRes = await fetch("/api/extract/details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sessionToken: sessionData.sessionToken,
        image,
        items: [{ n, name: item.name }],
      }),
    });
    const detailsData = await detailsRes.json().catch(() => null);
    if (!detailsRes.ok) {
      throw new Error((detailsData && detailsData.error) || `http_${detailsRes.status}`);
    }
    const result = detailsData.items && detailsData.items[0];
    if (!result) throw new Error("empty_result");
    applyCorrection(item, result.ingredients);
    item.wrap = result.wrap;
    item.is_raw = result.is_raw;
    closeCorrectionSheet();
    if (currentMenuRenderHooks) currentMenuRenderHooks.renderList();
  } catch (err) {
    statusNode.textContent = `Retry failed (${err.message}). Try Fix ingredients instead.`;
  }
}

function renderCorrectionSheet() {
  const item = findMenuItem(state.correctionItemId);
  if (!item) {
    state.correctionItemId = null;
    return el("div", {});
  }

  // Working copy: edits apply only on Save, Cancel discards them.
  let working = [...item.ingredients];

  const overlay = el("div", { class: "sheet-overlay", role: "presentation" });
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closeCorrectionSheet();
  });

  const vocabulary = buildIngredientVocabulary(state.menu.items);

  const currentList = el("ul", { class: "ingredient-list editable" });
  function renderCurrentList() {
    clear(currentList);
    for (const ingredient of working) {
      currentList.appendChild(
        el("li", { class: "ingredient editable-ingredient" }, [
          el("span", { text: ingredient }),
          el("button", {
            type: "button",
            class: "ingredient-remove",
            "aria-label": `Remove ${ingredient}`,
            text: "×",
            onclick: () => {
              working = working.filter((i) => i !== ingredient);
              renderCurrentList();
            },
          }),
        ]),
      );
    }
  }
  renderCurrentList();

  function addIngredient(ingredient) {
    const trimmed = ingredient.trim().toLowerCase();
    if (!trimmed || working.includes(trimmed)) return;
    working.push(trimmed);
    renderCurrentList();
  }

  // Tier 1: chips of the menu's own vocabulary, tap to add.
  const tier1 = el(
    "div",
    { class: "chip-list", role: "group", "aria-label": "Common ingredients on this menu" },
    vocabulary.map((ingredient) =>
      el("button", {
        type: "button",
        class: "chip chip-neutral",
        text: ingredient,
        onclick: () => addIngredient(ingredient),
      }),
    ),
  );

  // Tier 2: autocomplete over that same vocabulary. Tier 3: free text,
  // offered only when nothing in the vocabulary matches what was typed,
  // per SPEC.md.
  const tierInput = el("input", {
    type: "text",
    class: "text-input tier-input",
    placeholder: "Type an ingredient",
    "aria-label": "Add an ingredient",
  });
  const suggestions = el("div", { class: "chip-list autocomplete-suggestions" });
  const freeTextRow = el("div", { class: "free-text-row" });

  function renderSuggestions() {
    clear(suggestions);
    clear(freeTextRow);
    const query = tierInput.value.trim();
    if (!query) return;
    const matches = filterChipVocabulary(vocabulary, query);
    for (const match of matches) {
      suggestions.appendChild(
        el("button", {
          type: "button",
          class: "chip chip-neutral",
          text: match,
          onclick: () => {
            addIngredient(match);
            tierInput.value = "";
            renderSuggestions();
          },
        }),
      );
    }
    if (matches.length === 0) {
      freeTextRow.appendChild(
        el("button", {
          type: "button",
          class: "secondary-action",
          text: `Add "${query}" anyway`,
          onclick: () => {
            addIngredient(query);
            tierInput.value = "";
            renderSuggestions();
          },
        }),
      );
    }
  }
  tierInput.addEventListener("input", renderSuggestions);

  const retryStatus = el("p", { class: "retry-status" });
  const retryButton = el("button", {
    class: "secondary-action",
    type: "button",
    text: "Retry this item",
    onclick: () => retryItem(item, retryStatus),
  });

  const sheetChildren = [
    el("div", { class: "sheet-handle" }),
    el("h3", { class: "section-title", text: item.name }),
  ];
  if (state.canRetryItems) {
    sheetChildren.push(retryButton, retryStatus);
  }
  sheetChildren.push(
    el("h3", { class: "section-title", text: "Current ingredients" }),
    currentList,
    el("h3", { class: "section-title", text: "Common on this menu" }),
    tier1,
    el("h3", { class: "section-title", text: "Or type one" }),
    tierInput,
    suggestions,
    freeTextRow,
    el("button", {
      class: "primary-action",
      type: "button",
      text: "Save",
      onclick: () => {
        applyCorrection(item, working);
        closeCorrectionSheet();
        if (currentMenuRenderHooks) currentMenuRenderHooks.renderList();
      },
    }),
    el("button", {
      class: "secondary-action sheet-done",
      type: "button",
      text: "Cancel",
      onclick: closeCorrectionSheet,
    }),
  );

  const sheet = el(
    "div",
    {
      class: "sheet",
      role: "dialog",
      "aria-modal": "true",
      "aria-label": `Fix ingredients for ${item.name}`,
    },
    sheetChildren,
  );
  overlay.appendChild(sheet);
  return overlay;
}

render();
