// Client orchestration state machine, per SPEC.md's "Client orchestration
// state machine (app.js)" section. This module owns fetch orchestration,
// multi-photo merge/dedupe, retry, and localStorage persistence. Rendering,
// the filter sheet, and Omakase live in ui.js (not this file, not yet
// built); this module exposes state via subscribe() so ui.js can render it
// without app.js knowing anything about the DOM.

import { preprocessPhoto } from "./preprocess.js";

export const STATES = Object.freeze({
  IDLE: "IDLE",
  PREPROCESS: "PREPROCESS",
  INDEX: "INDEX",
  DETAILS: "DETAILS",
  RECONCILE: "RECONCILE",
  READY: "READY",
  ERROR: "ERROR",
});

const JOB_TTL_MS = 30 * 60 * 1000;
const DETAILS_BATCH_SIZE = 8;
const DETAILS_CONCURRENCY = 3;
const RETRY_COUNT = 1;
const FUZZY_MATCH_THRESHOLD = 85;
const REQUEST_TIMEOUT_MS = 30_000;

// --------------------------------------------------------------------------
// fetch with one retry on 429/5xx/timeout, jittered backoff, per SPEC.md's
// "the client owns orchestration state" rationale.
// --------------------------------------------------------------------------

function jitteredDelay(attempt) {
  const base = 500 * (attempt + 1);
  const jitter = Math.random() * 300;
  return new Promise((resolve) => setTimeout(resolve, base + jitter));
}

async function fetchWithRetry(url, options) {
  let lastError;
  for (let attempt = 0; attempt <= RETRY_COUNT; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
    try {
      const res = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(timer);
      if ((res.status === 429 || res.status >= 500) && attempt < RETRY_COUNT) {
        await jitteredDelay(attempt);
        continue;
      }
      return res;
    } catch (err) {
      clearTimeout(timer);
      lastError = err;
      if (attempt < RETRY_COUNT) {
        await jitteredDelay(attempt);
        continue;
      }
    }
  }
  throw lastError ?? new Error("fetchWithRetry: exhausted retries");
}

async function postJson(path, body) {
  const res = await fetchWithRetry(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const code = data && typeof data.error === "string" ? data.error : `http_${res.status}`;
    throw new Error(code);
  }
  return data;
}

// --------------------------------------------------------------------------
// Fuzzy name matching for dedupe. An honest Levenshtein-ratio approximation
// of token_sort_ratio, not byte-identical to Python's fuzzywuzzy/rapidfuzz
// (the eval harness's implementation): same idea (sort tokens, then measure
// similarity), different underlying algorithm (edit-distance ratio here vs
// difflib's SequenceMatcher there). Close enough for client-side dedupe,
// which only needs to catch near-duplicate overlapping-photo shots, not
// reproduce the harness's exact score.
// --------------------------------------------------------------------------

function normalizeForMatch(name) {
  return name.toLowerCase().trim().split(/\s+/).filter(Boolean).sort().join(" ");
}

function levenshteinDistance(a, b) {
  const rows = a.length + 1;
  const cols = b.length + 1;
  const dist = Array.from({ length: rows }, (_, i) => [i, ...Array(cols - 1).fill(0)]);
  for (let j = 0; j < cols; j++) dist[0][j] = j;
  for (let i = 1; i < rows; i++) {
    for (let j = 1; j < cols; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      dist[i][j] = Math.min(
        dist[i - 1][j] + 1,
        dist[i][j - 1] + 1,
        dist[i - 1][j - 1] + cost,
      );
    }
  }
  return dist[rows - 1][cols - 1];
}

function tokenSortRatio(nameA, nameB) {
  const a = normalizeForMatch(nameA);
  const b = normalizeForMatch(nameB);
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 100;
  const distance = levenshteinDistance(a, b);
  return Math.round((1 - distance / maxLen) * 100);
}

// Two items merge only when BOTH fuzzy name match AND compatible price
// hold, per SPEC.md: equal numeric price, or at least one side null.
function pricesCompatible(priceA, priceB) {
  if (priceA == null || priceB == null) return true;
  return priceA === priceB;
}

function itemsAreDuplicates(itemA, itemB) {
  return (
    tokenSortRatio(itemA.name, itemB.name) >= FUZZY_MATCH_THRESHOLD &&
    pricesCompatible(itemA.price, itemB.price)
  );
}

// --------------------------------------------------------------------------
// Content hashing for job identity (resume support).
// --------------------------------------------------------------------------

async function sha256Hex(text) {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

async function computeJobHash(photoHashes) {
  return sha256Hex(photoHashes.join("|"));
}

// --------------------------------------------------------------------------
// localStorage persistence
// --------------------------------------------------------------------------

function jobStorageKey(jobHash) {
  return `ss:job:${jobHash}`;
}

function saveJob(job) {
  try {
    localStorage.setItem(jobStorageKey(job.jobHash), JSON.stringify(job));
  } catch {
    // Storage full or unavailable (private browsing): the job still
    // completes in memory this session, it just cannot resume after a
    // reload. Not fatal, per SPEC.md's error-UX principle of degrading
    // gracefully rather than blocking the parse.
  }
}

function loadJob(jobHash) {
  try {
    const raw = localStorage.getItem(jobStorageKey(jobHash));
    if (!raw) return null;
    const job = JSON.parse(raw);
    if (Date.now() - job.updatedAt > JOB_TTL_MS) return null;
    return job;
  } catch {
    return null;
  }
}

export function saveMenu(slug, menu) {
  try {
    localStorage.setItem(`ss:menu:${slug}`, JSON.stringify(menu));
  } catch {
    // Same graceful-degradation reasoning as saveJob.
  }
}

// --------------------------------------------------------------------------
// Reconciliation and merge
// --------------------------------------------------------------------------

// Every index item's n must appear in exactly one details result for its
// photo. Returns the n values with no matching details entry.
function findMissingDetails(indexItems, detailsItems) {
  const detailsNs = new Set(detailsItems.map((d) => d.n));
  return indexItems.filter((i) => !detailsNs.has(i.n)).map((i) => i.n);
}

// Merge one photo's index + details into flat items carrying a global id
// ("photoIndex:n"), per SPEC.md's multi-photo merge rules.
function reconcilePhoto(photoIndex, indexResult, detailsByN, stillMissingNs) {
  const stillMissing = new Set(stillMissingNs);
  return indexResult.items.map((indexItem) => {
    const details = detailsByN.get(indexItem.n);
    const globalId = `${photoIndex}:${indexItem.n}`;
    if (!details) {
      return {
        id: globalId,
        name: indexItem.name,
        section: indexItem.section,
        price: indexItem.price,
        price_text: indexItem.price_text,
        ingredients: [],
        wrap: "unknown",
        is_raw: null,
        notes: null,
        flagged: true,
        flagReason: stillMissing.has(indexItem.n) ? "missing_details" : null,
      };
    }
    return {
      id: globalId,
      name: indexItem.name,
      section: indexItem.section,
      price: indexItem.price,
      price_text: indexItem.price_text,
      ingredients: details.ingredients,
      wrap: details.wrap,
      is_raw: details.is_raw,
      notes: details.notes ?? null,
      flagged: false,
      flagReason: null,
    };
  });
}

// Merge across photos in photo order. Overlapping-shot duplicates collapse
// (fuzzy name + compatible price); keep the record with more ingredients,
// union the notes. Genuinely different dishes at different prices never
// collapse, by design (this is the guard SPEC.md calls out explicitly).
function mergeAcrossPhotos(perPhotoItems) {
  const merged = [];
  for (const photoItems of perPhotoItems) {
    for (const item of photoItems) {
      const dupIndex = merged.findIndex((existing) => itemsAreDuplicates(existing, item));
      if (dupIndex === -1) {
        merged.push(item);
        continue;
      }
      const existing = merged[dupIndex];
      const winner = item.ingredients.length > existing.ingredients.length ? item : existing;
      const loser = winner === item ? existing : item;
      merged[dupIndex] = {
        ...winner,
        notes: [winner.notes, loser.notes].filter(Boolean).join("; ") || null,
      };
    }
  }
  return merged;
}

function mergeRestaurantName(perPhotoResults) {
  for (const result of perPhotoResults) {
    if (result.restaurant_name) return result.restaurant_name;
  }
  return null;
}

// --------------------------------------------------------------------------
// JobController: owns one parse job's lifecycle end to end.
// --------------------------------------------------------------------------

export class JobController {
  constructor() {
    this.state = STATES.IDLE;
    this.job = null;
    this.listeners = new Set();
    // Deliberately NOT part of `job` (never touches saveJob/localStorage):
    // base64 photo data is easily multi-MB per photo, and job state is
    // persisted to localStorage on every single-state transition per
    // SPEC.md. Storing images there would risk the browser's storage
    // quota on every save, not just once. Living only as an in-memory
    // instance field means a single-item retry is only possible for a job
    // completed in the current page load, not one reopened later from
    // ss:menu:* (recent menus); ui.js gates the "Retry this item" action
    // on that distinction rather than pretending it always works.
    this.photoImages = null;
  }

  subscribe(callback) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  // Returns the ImageInput for a given photo index if this job's images are
  // still in memory (same page load, not a reopened recent menu), or null.
  getPhotoImage(photoIndex) {
    return this.photoImages ? (this.photoImages[photoIndex] ?? null) : null;
  }

  _setState(state) {
    this.state = state;
    if (this.job) {
      this.job.state = state;
      this.job.updatedAt = Date.now();
      saveJob(this.job);
    }
    for (const listener of this.listeners) listener(this.state, this.job);
  }

  // Resume a job younger than JOB_TTL_MS from its last completed step, per
  // SPEC.md. Returns true if a resumable job was found and loaded.
  tryResume(jobHash) {
    const job = loadJob(jobHash);
    if (!job) return false;
    this.job = job;
    this.state = job.state;
    for (const listener of this.listeners) listener(this.state, this.job);
    return true;
  }

  // files: File[] (1-6 photos). turnstileToken: obtained by the caller
  // (index.html's widget, not this module's concern) before calling start.
  async start(files, turnstileToken) {
    if (files.length < 1 || files.length > 6) {
      throw new Error("a parse job accepts 1 to 6 photos");
    }

    this._setState(STATES.PREPROCESS);
    const images = await Promise.all(files.map((f) => preprocessPhoto(f)));
    this.photoImages = images;
    const photoHashes = await Promise.all(images.map((img) => sha256Hex(img.data)));
    const jobHash = await computeJobHash(photoHashes);

    if (this.tryResume(jobHash)) return this.job;

    this.job = {
      jobHash,
      photoHashes,
      state: STATES.PREPROCESS,
      updatedAt: Date.now(),
      perPhotoIndex: images.map(() => null),
      perPhotoDetails: images.map(() => []),
      perPhotoRetried: images.map(() => []),
      items: null,
      restaurantName: null,
      error: null,
    };
    saveJob(this.job);

    try {
      const { sessionToken } = await postJson("/api/session", { turnstileToken });

      this._setState(STATES.INDEX);
      const indexResults = await Promise.all(
        images.map((image) => postJson("/api/extract/index", { sessionToken, image })),
      );
      this.job.perPhotoIndex = indexResults;
      saveJob(this.job);

      this._setState(STATES.DETAILS);
      for (let photoIndex = 0; photoIndex < images.length; photoIndex++) {
        await this._runDetailsForPhoto(photoIndex, images[photoIndex], sessionToken);
      }

      this._setState(STATES.RECONCILE);
      const perPhotoItems = [];
      for (let photoIndex = 0; photoIndex < images.length; photoIndex++) {
        const indexResult = this.job.perPhotoIndex[photoIndex];
        const detailsByN = new Map(
          this.job.perPhotoDetails[photoIndex].map((d) => [d.n, d]),
        );
        const missing = findMissingDetails(indexResult.items, this.job.perPhotoDetails[photoIndex]);
        perPhotoItems.push(reconcilePhoto(photoIndex, indexResult, detailsByN, missing));
      }
      this.job.items = mergeAcrossPhotos(perPhotoItems);
      this.job.restaurantName = mergeRestaurantName(this.job.perPhotoIndex);
      saveJob(this.job);

      this._setState(STATES.READY);
      return this.job;
    } catch (err) {
      this.job.error = String(err && err.message ? err.message : err);
      this._setState(STATES.ERROR);
      throw err;
    }
  }

  // Batch 1 fires alone to warm the prompt cache (cache entries only become
  // readable after the first response begins); the remaining batches then
  // fan out with concurrency 3, per SPEC.md.
  async _runDetailsForPhoto(photoIndex, image, sessionToken) {
    const indexResult = this.job.perPhotoIndex[photoIndex];
    const items = indexResult.items.map((i) => ({ n: i.n, name: i.name }));
    const batches = [];
    for (let i = 0; i < items.length; i += DETAILS_BATCH_SIZE) {
      batches.push(items.slice(i, i + DETAILS_BATCH_SIZE));
    }
    if (batches.length === 0) return;

    const runBatch = async (batch) => {
      const result = await postJson("/api/extract/details", {
        sessionToken,
        image,
        items: batch,
      });
      this.job.perPhotoDetails[photoIndex].push(...result.items);
      saveJob(this.job);
    };

    await runBatch(batches[0]);
    const rest = batches.slice(1);
    for (let i = 0; i < rest.length; i += DETAILS_CONCURRENCY) {
      const chunk = rest.slice(i, i + DETAILS_CONCURRENCY);
      await Promise.all(chunk.map(runBatch));
    }

    // One retry for items that still have no details result at all, per
    // SPEC.md's RECONCILE handling. perPhotoRetried is a plain array (not a
    // Set: this job round-trips through JSON.stringify/parse via
    // localStorage on every save/resume, and Set does not survive that
    // round-trip), tracking which items already had their one retry so
    // this method stays idempotent if the job resumes mid-photo.
    const missingNs = findMissingDetails(indexResult.items, this.job.perPhotoDetails[photoIndex]);
    const retried = this.job.perPhotoRetried[photoIndex];
    const toRetry = missingNs.filter((n) => !retried.includes(n));
    if (toRetry.length > 0) {
      const retryItems = items.filter((i) => toRetry.includes(i.n));
      retried.push(...toRetry);
      await runBatch(retryItems);
    }
  }
}
