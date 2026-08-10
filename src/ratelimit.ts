// Rate limiting: Cloudflare's native ratelimit binding (GA since September
// 2025, free), not a hand-rolled counter. Two namespaces are declared in
// wrangler.jsonc: EXTRACT_LIMITER (6 per 60s, keyed on session token) and
// SESSION_LIMITER (3 per 60s, keyed on client IP), per SPEC.md's security
// controls table. Verified against live docs before writing this file: the
// binding's limit() method takes { key: string } and returns
// { success: boolean }, and the period field only accepts 10 or 60 seconds
// (already satisfied by the existing wrangler.jsonc config, both at 60).

// The binding is permissive and eventually consistent with per-location
// counters (documented caveat). That is acceptable here because the
// Anthropic workspace spend cap, not this limiter, is the control that
// guarantees the blast radius; this limiter absorbs the common case of one
// abusive client, not an adversary spread across edge locations.

export async function checkRateLimit(
  binding: RateLimit,
  key: string,
): Promise<boolean> {
  const { success } = await binding.limit({ key });
  return success;
}

// Extract endpoints key on the session token: every photo, index call, and
// details batch within one parse job shares the token, so the limit is per
// parse session, not per request.
export function checkExtractLimit(
  env: { EXTRACT_LIMITER: RateLimit },
  sessionToken: string,
): Promise<boolean> {
  return checkRateLimit(env.EXTRACT_LIMITER, sessionToken);
}

// Session issuance keys on client IP: this is the one call a client makes
// before it has a session token at all, so IP is the only key available.
// CF-Connecting-IP is set by Cloudflare's edge and cannot be spoofed by the
// client (unlike X-Forwarded-For).
export function checkSessionLimit(
  env: { SESSION_LIMITER: RateLimit },
  clientIp: string,
): Promise<boolean> {
  return checkRateLimit(env.SESSION_LIMITER, clientIp);
}
