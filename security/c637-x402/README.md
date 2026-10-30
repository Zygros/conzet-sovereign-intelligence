# C637: Fail-Closed x402 Payment Gate

This is a **reference implementation and mocked test suite**, not a claim that the current production endpoint is fixed or that the code is ready for mainnet.

## Security invariants

1. Payment is not authorization until facilitator verification returns strict `isValid: true`.
2. Verification failure, timeout, malformed data, missing configuration, or non-2xx response fails closed.
3. The paid resource is not returned until settlement returns strict `success: true` and a transaction identifier.
4. Request counts are not revenue. Revenue must be reconciled from confirmed settlement receipts and chain data.
5. Never use a public development facilitator for production settlement without confirming its supported networks and operational guarantees.

## Files

- `worker.js`: Cloudflare Worker-style reference gate.
- `worker.test.js`: Node built-in test suite with mocked facilitator responses.
- `package.json`: test command.

## Run tests

Requires Node.js 20 or later:

```sh
npm test
```

## Required before any deployment

- Pin the exact x402 protocol/SDK version and use its canonical payload and requirements schema.
- Confirm the configured facilitator's actual `/verify` and `/settle` contract. This sample assumes those routes and fields; adapt through the official SDK if the deployed facilitator differs.
- Validate network, asset contract, recipient, amount, scheme, expiry, and replay/idempotency behavior according to the selected protocol version.
- Add a persistent idempotency store for settlement retries and duplicate requests.
- Run testnet integration tests and reconcile transaction hashes with a chain RPC or explorer.
- Keep credentials in platform secrets, never source control.
- Do not count a settlement as revenue until transaction status and the intended recipient/amount are independently verified.

The tests intentionally mock the facilitator. They prove fail-closed behavior of this code path under the listed responses, not facilitator correctness, chain settlement, protocol conformance, or live endpoint availability.
