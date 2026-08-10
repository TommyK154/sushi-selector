// Session issuance: Turnstile siteverify, then a signed, short-lived HMAC
// token per SPEC.md's POST /api/session contract. Not bound to client IP by
// design: phones roam between wifi and cellular mid-parse, and the token is
// unforgeable and short-lived on its own, so IP binding would add breakage
// without adding protection (extract rate limiting keys on the token
// itself, not the IP).

// Endpoint and field names verified against live Turnstile docs before
// writing this file: POST https://challenges.cloudflare.com/turnstile/v0/siteverify,
// body { secret, response, remoteip?, idempotency_key? }, response includes
// a boolean `success` and an `error-codes` array on failure.
const SITEVERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify";

const SESSION_TTL_SECONDS = 600;

export interface SessionPayload {
  exp: number;
  jti: string;
}

interface SiteverifyResponse {
  success: boolean;
  "error-codes"?: string[];
}

export async function verifyTurnstile(
  token: string,
  secretKey: string,
  remoteIp: string | null,
): Promise<boolean> {
  const body = new URLSearchParams({ secret: secretKey, response: token });
  // A random idempotency key per attempt lets a network-level retry of this
  // same fetch (Workers' own fetch retry, a client resubmission after a
  // timeout) be treated as the same verification by Turnstile's side rather
  // than rejected as replay of an already-consumed token.
  body.set("idempotency_key", crypto.randomUUID());
  if (remoteIp) body.set("remoteip", remoteIp);

  const res = await fetch(SITEVERIFY_URL, { method: "POST", body });
  if (!res.ok) return false;
  const result = (await res.json()) as SiteverifyResponse;
  return result.success === true;
}

function base64UrlEncode(bytes: Uint8Array): string {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function base64UrlDecode(value: string): Uint8Array {
  const padded = value.replace(/-/g, "+").replace(/_/g, "/");
  const padding = padded.length % 4 === 0 ? "" : "=".repeat(4 - (padded.length % 4));
  const binary = atob(padded + padding);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

async function importHmacKey(
  secret: string,
  usage: "sign" | "verify",
): Promise<CryptoKey> {
  return crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    [usage],
  );
}

// Token shape, exactly as specified: base64url(payload) + "." +
// base64url(hmacSHA256(payload, secret)). The signature covers the raw
// serialized payload bytes directly, not the base64url-encoded string (a
// deliberate departure from JWT convention, per SPEC.md's own wire format).
export async function mintSessionToken(secret: string): Promise<string> {
  const payload: SessionPayload = {
    exp: Math.floor(Date.now() / 1000) + SESSION_TTL_SECONDS,
    jti: crypto.randomUUID(),
  };
  const payloadBytes = new TextEncoder().encode(JSON.stringify(payload));
  const key = await importHmacKey(secret, "sign");
  const signature = await crypto.subtle.sign("HMAC", key, payloadBytes);
  return `${base64UrlEncode(payloadBytes)}.${base64UrlEncode(new Uint8Array(signature))}`;
}

export interface VerifyResult {
  valid: boolean;
  payload: SessionPayload | null;
}

// Signature check uses crypto.subtle.verify (constant-time), never a string
// or byte-array equality comparison, per SPEC.md's security controls.
export async function verifySessionToken(
  token: string,
  secret: string,
): Promise<VerifyResult> {
  const parts = token.split(".");
  if (parts.length !== 2) return { valid: false, payload: null };
  const [encodedPayload, encodedSignature] = parts;

  let payloadBytes: Uint8Array;
  let signatureBytes: Uint8Array;
  try {
    payloadBytes = base64UrlDecode(encodedPayload);
    signatureBytes = base64UrlDecode(encodedSignature);
  } catch {
    return { valid: false, payload: null };
  }

  const key = await importHmacKey(secret, "verify");
  const signatureValid = await crypto.subtle.verify(
    "HMAC",
    key,
    signatureBytes,
    payloadBytes,
  );
  if (!signatureValid) return { valid: false, payload: null };

  let payload: SessionPayload;
  try {
    payload = JSON.parse(new TextDecoder().decode(payloadBytes));
  } catch {
    return { valid: false, payload: null };
  }

  if (typeof payload.exp !== "number" || typeof payload.jti !== "string") {
    return { valid: false, payload: null };
  }
  if (payload.exp < Math.floor(Date.now() / 1000)) {
    return { valid: false, payload: null };
  }

  return { valid: true, payload };
}
