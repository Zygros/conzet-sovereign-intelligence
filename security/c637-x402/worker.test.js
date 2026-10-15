import test from "node:test";
import assert from "node:assert/strict";
import { handleRequest } from "./worker.js";

const requirements = { scheme: "exact", network: "eip155:8453", amount: "1000", asset: "test-token", payTo: "0x0000000000000000000000000000000000000001" };
const env = { FACILITATOR_URL: "https://facilitator.example", PAYMENT_REQUIREMENTS: JSON.stringify(requirements) };
const payloadHeader = btoa(JSON.stringify({ x402Version: 2, payload: { test: true } }));
const request = (header = payloadHeader) => new Request("https://worker.example/api/beacon", {
  headers: header ? { "PAYMENT-SIGNATURE": header } : {},
});
function fakeFetch(verify, settle, options = {}) {
  const calls = [];
  const fn = async (url, init) => {
    calls.push({ url: String(url), body: JSON.parse(init.body) });
    if (options.throwOn) throw new Error("network failure");
    if (String(url).endsWith("/verify")) {
      return new Response(JSON.stringify(verify), { status: options.verifyStatus || 200 });
    }
    return new Response(JSON.stringify(settle), { status: options.settleStatus || 200 });
  };
  fn.calls = calls;
  return fn;
}

test("health endpoint is available without payment", async () => {
  const r = await handleRequest(new Request("https://worker.example/health"), {}, fetch);
  assert.equal(r.status, 200);
  assert.equal((await r.json()).ok, true);
});

test("unknown route is 404", async () => {
  const r = await handleRequest(new Request("https://worker.example/nope"), env, fetch);
  assert.equal(r.status, 404);
});

test("missing payment returns 402 and never calls facilitator", async () => {
  const f = fakeFetch({}, {});
  const r = await handleRequest(request(null), env, f);
  assert.equal(r.status, 402);
  assert.equal(f.calls.length, 0);
});

test("malformed payment returns 402", async () => {
  const r = await handleRequest(request("not-base64-json"), env, fetch);
  assert.equal(r.status, 402);
});

test("missing configuration fails closed", async () => {
  const r = await handleRequest(request(), {}, fetch);
  assert.equal(r.status, 503);
});

test("verification rejection never settles", async () => {
  const f = fakeFetch({ isValid: false, invalidReason: "bad_signature" }, { success: true, transaction: "0x12345678" });
  const r = await handleRequest(request(), env, f);
  assert.equal(r.status, 402);
  assert.equal(f.calls.length, 1);
  assert.match(f.calls[0].url, /\/verify$/);
});

test("verification response without strict true fails closed", async () => {
  const f = fakeFetch({ isValid: "true" }, { success: true, transaction: "0x12345678" });
  const r = await handleRequest(request(), env, f);
  assert.equal(r.status, 402);
  assert.equal(f.calls.length, 1);
});

test("valid verification and confirmed settlement release resource", async () => {
  const f = fakeFetch({ isValid: true }, { success: true, transaction: "0x1234567890abcdef", network: "eip155:8453" });
  const r = await handleRequest(request(), env, f);
  assert.equal(r.status, 200);
  assert.equal(f.calls.length, 2);
  assert.match(f.calls[0].url, /\/verify$/);
  assert.match(f.calls[1].url, /\/settle$/);
  assert.equal((await r.json()).settlement.transaction, "0x1234567890abcdef");
});

test("settlement failure never releases resource", async () => {
  const f = fakeFetch({ isValid: true }, { success: false, transaction: "0x1234567890abcdef" });
  const r = await handleRequest(request(), env, f);
  assert.equal(r.status, 502);
});

test("settlement without transaction identifier never releases resource", async () => {
  const f = fakeFetch({ isValid: true }, { success: true });
  const r = await handleRequest(request(), env, f);
  assert.equal(r.status, 502);
});

test("facilitator network error fails closed", async () => {
  const f = fakeFetch({}, {}, { throwOn: true });
  const r = await handleRequest(request(), env, f);
  assert.equal(r.status, 503);
});

test("facilitator HTTP error fails closed", async () => {
  const f = fakeFetch({}, {}, { verifyStatus: 500 });
  const r = await handleRequest(request(), env, f);
  assert.equal(r.status, 503);
});

test("non-HTTPS facilitator is rejected", async () => {
  const r = await handleRequest(request(), { ...env, FACILITATOR_URL: "http://facilitator.example" }, fetch);
  assert.equal(r.status, 503);
});
