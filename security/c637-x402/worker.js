/**
 * C637 fail-closed x402 reference worker.
 *
 * Safety properties:
 * - Missing/malformed payment payloads never authorize access.
 * - Facilitator network errors and non-2xx responses fail closed.
 * - Settlement must succeed and include a transaction identifier before content is released.
 * - Revenue is never inferred from a request counter.
 *
 * Configure PAYMENT_REQUIREMENTS as the exact payment-requirements object expected
 * by your installed x402 facilitator/version. Confirm schema compatibility before use.
 */
const json = (body, status = 200, headers = {}) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...headers },
  });

function decodePaymentHeader(value) {
  if (!value) return null;
  try {
    // x402 PAYMENT-SIGNATURE is a base64-encoded JSON payment payload.
    const decoded = atob(value);
    const parsed = JSON.parse(decoded);
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

async function facilitatorPost(baseUrl, route, payload, fetchImpl) {
  const base = String(baseUrl || "").replace(/\/+$/, "");
  if (!/^https:\/\//i.test(base)) throw new Error("FACILITATOR_URL must be HTTPS");
  const response = await fetchImpl(`${base}${route}`, {
    method: "POST",
    headers: { "content-type": "application/json", "accept": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(`Facilitator ${route} returned HTTP ${response.status}`);
  const body = await response.json();
  if (!body || typeof body !== "object" || Array.isArray(body)) throw new Error("Invalid facilitator response");
  return body;
}

export async function handleRequest(request, env, fetchImpl = fetch) {
  const url = new URL(request.url);
  if (url.pathname === "/health") return json({ ok: true, mode: "fail-closed-reference" });
  if (url.pathname !== "/api/beacon") return json({ error: "not_found" }, 404);

  let requirements;
  try {
    requirements = JSON.parse(env.PAYMENT_REQUIREMENTS || "null");
  } catch {
    return json({ error: "payment_configuration_invalid" }, 503);
  }
  if (!requirements || typeof requirements !== "object" || Array.isArray(requirements)) {
    return json({ error: "payment_not_configured" }, 503);
  }
  if (!env.FACILITATOR_URL) return json({ error: "facilitator_not_configured" }, 503);

  const raw = request.headers.get("PAYMENT-SIGNATURE");
  const paymentPayload = decodePaymentHeader(raw);
  if (!paymentPayload) {
    const required = btoa(JSON.stringify(requirements));
    return json(
      { error: "payment_required", paymentRequired: requirements },
      402,
      { "PAYMENT-REQUIRED": required }
    );
  }

  try {
    const verified = await facilitatorPost(
      env.FACILITATOR_URL,
      "/verify",
      { paymentPayload, paymentRequirements: requirements },
      fetchImpl
    );
    if (verified.isValid !== true) {
      return json({ error: "payment_invalid", reason: verified.invalidReason || "verification_rejected" }, 402);
    }

    // Do not release the paid resource until settlement has been confirmed.
    const settled = await facilitatorPost(
      env.FACILITATOR_URL,
      "/settle",
      { paymentPayload, paymentRequirements: requirements },
      fetchImpl
    );
    if (settled.success !== true || typeof settled.transaction !== "string" || settled.transaction.length < 8) {
      return json({ error: "settlement_unconfirmed" }, 502);
    }

    return json({
      ok: true,
      data: { message: "Beacon access granted" },
      settlement: { transaction: settled.transaction, network: settled.network || null },
    }, 200, { "PAYMENT-RESPONSE": btoa(JSON.stringify(settled)) });
  } catch {
    // Deliberately do not leak upstream details or convert failure into authorization.
    return json({ error: "payment_verification_unavailable" }, 503);
  }
}

export default { fetch: handleRequest };
