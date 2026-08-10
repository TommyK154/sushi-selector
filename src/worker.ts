// Sushi Selector worker: thin proxy and router. The intelligence of this
// product lives in shared/prompts/ and shared/schema/, not here. Phase 1:
// session issuance, rate limiting, and the three extraction endpoints wired
// per SPEC.md's Worker API contracts.

import {
  verifyTurnstile,
  mintSessionToken,
  verifySessionToken,
} from "./session";
import { checkExtractLimit, checkSessionLimit } from "./ratelimit";
import {
  createExtractionProvider,
  resolveModel,
  type ImageInput,
  type DetailsItem,
  type ExtractionResult,
} from "./extract";

export interface Env {
  ASSETS: Fetcher;
  EXTRACT_LIMITER: RateLimit;
  SESSION_LIMITER: RateLimit;
  MODEL: string;
  TURNSTILE_SITE_KEY: string;
  ALLOWED_ORIGINS: string;
  // Secrets (present at runtime, never committed): ANTHROPIC_API_KEY,
  // TURNSTILE_SECRET_KEY, SESSION_HMAC_SECRET.
  ANTHROPIC_API_KEY?: string;
  TURNSTILE_SECRET_KEY?: string;
  SESSION_HMAC_SECRET?: string;
}

const MAX_BODY_BYTES = 1_500_000;
const MAX_URL_LENGTH = 2048;

function allowedOrigins(env: Env): string[] {
  return (env.ALLOWED_ORIGINS || "")
    .split(",")
    .map((o) => o.trim())
    .filter(Boolean);
}

// CORS is advisory (trivially spoofed outside browsers); the session token is
// the real endpoint guard. We reflect only known origins and never wildcard.
function corsHeaders(request: Request, env: Env): Record<string, string> {
  const origin = request.headers.get("Origin");
  const headers: Record<string, string> = {
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
  if (origin && allowedOrigins(env).includes(origin)) {
    headers["Access-Control-Allow-Origin"] = origin;
  }
  return headers;
}

function json(
  body: unknown,
  status: number,
  extra: Record<string, string> = {},
): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...extra },
  });
}

function errorResponse(
  status: number,
  code: string,
  cors: Record<string, string>,
): Response {
  return json({ error: code }, status, cors);
}

// One structured JSON log line per Anthropic call, per SPEC.md, so cost and
// cache behavior are auditable from Workers observability logs alone.
function logExtraction(
  endpoint: string,
  model: string,
  usage: ExtractionResult["usage"],
  latencyMs: number,
  outcome: "ok" | "error",
): void {
  console.log(
    JSON.stringify({
      endpoint,
      model,
      usage,
      latency_ms: latencyMs,
      outcome,
    }),
  );
}

// Reject oversized bodies before parsing, per SPEC.md, using the
// content-length header where the client sends one honestly. A client that
// omits or lies about content-length still hits the same cap once the body
// is actually read, via the explicit byte-length check below.
async function readBoundedJson(
  request: Request,
  cors: Record<string, string>,
): Promise<{ ok: true; body: unknown } | { ok: false; response: Response }> {
  const contentLength = request.headers.get("Content-Length");
  if (contentLength && Number(contentLength) > MAX_BODY_BYTES) {
    return { ok: false, response: errorResponse(413, "payload_too_large", cors) };
  }
  const text = await request.text();
  if (new TextEncoder().encode(text).length > MAX_BODY_BYTES) {
    return { ok: false, response: errorResponse(413, "payload_too_large", cors) };
  }
  try {
    return { ok: true, body: JSON.parse(text) };
  } catch {
    return { ok: false, response: errorResponse(400, "invalid_json", cors) };
  }
}

function isImageInput(value: unknown): value is ImageInput {
  return (
    typeof value === "object" &&
    value !== null &&
    typeof (value as ImageInput).media_type === "string" &&
    typeof (value as ImageInput).data === "string"
  );
}

async function requireSession(
  body: Record<string, unknown>,
  env: Env,
  cors: Record<string, string>,
): Promise<{ ok: true } | { ok: false; response: Response }> {
  const token = body.sessionToken;
  if (typeof token !== "string" || !env.SESSION_HMAC_SECRET) {
    return { ok: false, response: errorResponse(401, "invalid_session", cors) };
  }
  const { valid } = await verifySessionToken(token, env.SESSION_HMAC_SECRET);
  if (!valid) {
    return { ok: false, response: errorResponse(401, "invalid_session", cors) };
  }
  const withinLimit = await checkExtractLimit(env, token);
  if (!withinLimit) {
    return { ok: false, response: errorResponse(429, "rate_limited", cors) };
  }
  return { ok: true };
}

async function handleSession(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  const clientIp = request.headers.get("CF-Connecting-IP") || "unknown";
  const withinLimit = await checkSessionLimit(env, clientIp);
  if (!withinLimit) {
    return errorResponse(429, "rate_limited", cors);
  }

  const parsed = await readBoundedJson(request, cors);
  if (!parsed.ok) return parsed.response;
  const body = parsed.body as Record<string, unknown>;
  const turnstileToken = body.turnstileToken;
  if (typeof turnstileToken !== "string" || !env.TURNSTILE_SECRET_KEY) {
    return errorResponse(400, "missing_turnstile_token", cors);
  }

  const verified = await verifyTurnstile(
    turnstileToken,
    env.TURNSTILE_SECRET_KEY,
    clientIp === "unknown" ? null : clientIp,
  );
  if (!verified) {
    return errorResponse(403, "turnstile_failed", cors);
  }

  if (!env.SESSION_HMAC_SECRET) {
    return errorResponse(500, "server_misconfigured", cors);
  }
  const sessionToken = await mintSessionToken(env.SESSION_HMAC_SECRET);
  const { payload } = await verifySessionToken(sessionToken, env.SESSION_HMAC_SECRET);
  return json({ sessionToken, exp: payload?.exp }, 200, cors);
}

async function handleExtractIndex(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  const parsed = await readBoundedJson(request, cors);
  if (!parsed.ok) return parsed.response;
  const body = parsed.body as Record<string, unknown>;

  const sessionCheck = await requireSession(body, env, cors);
  if (!sessionCheck.ok) return sessionCheck.response;

  if (!isImageInput(body.image)) {
    return errorResponse(400, "invalid_image", cors);
  }

  const model = resolveModel(env);
  const provider = createExtractionProvider(env);
  const startedAt = Date.now();
  try {
    const result = await provider.runIndex(body.image, model);
    logExtraction("index", model, result.usage, Date.now() - startedAt, "ok");
    return json({ ...(result.data as object), usage: result.usage }, 200, cors);
  } catch (err) {
    logExtraction("index", model, zeroUsage(), Date.now() - startedAt, "error");
    return errorResponse(502, "extraction_failed", cors);
  }
}

async function handleExtractDetails(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  const parsed = await readBoundedJson(request, cors);
  if (!parsed.ok) return parsed.response;
  const body = parsed.body as Record<string, unknown>;

  const sessionCheck = await requireSession(body, env, cors);
  if (!sessionCheck.ok) return sessionCheck.response;

  if (!isImageInput(body.image)) {
    return errorResponse(400, "invalid_image", cors);
  }
  const items = body.items;
  if (!Array.isArray(items) || items.length === 0 || items.length > 10) {
    return errorResponse(400, "invalid_items", cors);
  }
  const detailsItems: DetailsItem[] = [];
  for (const item of items) {
    if (
      typeof item !== "object" ||
      item === null ||
      typeof (item as DetailsItem).n !== "number" ||
      typeof (item as DetailsItem).name !== "string"
    ) {
      return errorResponse(400, "invalid_items", cors);
    }
    detailsItems.push(item as DetailsItem);
  }

  const model = resolveModel(env);
  const provider = createExtractionProvider(env);
  const startedAt = Date.now();
  try {
    const result = await provider.runDetails(body.image, detailsItems, model);
    logExtraction("details", model, result.usage, Date.now() - startedAt, "ok");
    return json({ ...(result.data as object), usage: result.usage }, 200, cors);
  } catch (err) {
    logExtraction("details", model, zeroUsage(), Date.now() - startedAt, "error");
    return errorResponse(502, "extraction_failed", cors);
  }
}

async function handleExtractUrl(
  request: Request,
  env: Env,
  cors: Record<string, string>,
): Promise<Response> {
  const parsed = await readBoundedJson(request, cors);
  if (!parsed.ok) return parsed.response;
  const body = parsed.body as Record<string, unknown>;

  const sessionCheck = await requireSession(body, env, cors);
  if (!sessionCheck.ok) return sessionCheck.response;

  const url = body.url;
  if (typeof url !== "string" || url.length === 0 || url.length > MAX_URL_LENGTH) {
    return errorResponse(400, "invalid_url", cors);
  }
  let parsedUrl: URL;
  try {
    parsedUrl = new URL(url);
  } catch {
    return errorResponse(400, "invalid_url", cors);
  }
  if (parsedUrl.protocol !== "http:" && parsedUrl.protocol !== "https:") {
    return errorResponse(400, "invalid_url", cors);
  }

  const model = resolveModel(env);
  const provider = createExtractionProvider(env);
  const startedAt = Date.now();
  try {
    const result = await provider.runUrl(url, model);
    logExtraction("url", model, result.usage, Date.now() - startedAt, "ok");
    return json({ ...(result.data as object), usage: result.usage }, 200, cors);
  } catch (err) {
    logExtraction("url", model, zeroUsage(), Date.now() - startedAt, "error");
    return errorResponse(502, "extraction_failed", cors);
  }
}

function zeroUsage(): ExtractionResult["usage"] {
  return {
    input_tokens: 0,
    output_tokens: 0,
    cache_creation_input_tokens: 0,
    cache_read_input_tokens: 0,
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const cors = corsHeaders(request, env);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    // Static assets and non-/api paths are handled by the asset worker; only
    // /api/* reaches here thanks to run_worker_first.
    if (!url.pathname.startsWith("/api/")) {
      return env.ASSETS.fetch(request);
    }

    if (url.pathname === "/api/health" && request.method === "GET") {
      return json({ status: "ok", model: env.MODEL }, 200, cors);
    }

    // Reserved for post-MVP KV share links; documented and 404ing per SPEC.
    if (url.pathname.startsWith("/api/menus/")) {
      return json({ error: "not_found" }, 404, cors);
    }

    if (url.pathname === "/api/session" && request.method === "POST") {
      return handleSession(request, env, cors);
    }
    if (url.pathname === "/api/extract/index" && request.method === "POST") {
      return handleExtractIndex(request, env, cors);
    }
    if (url.pathname === "/api/extract/details" && request.method === "POST") {
      return handleExtractDetails(request, env, cors);
    }
    if (url.pathname === "/api/extract/url" && request.method === "POST") {
      return handleExtractUrl(request, env, cors);
    }

    return json({ error: "not_found" }, 404, cors);
  },
} satisfies ExportedHandler<Env>;
