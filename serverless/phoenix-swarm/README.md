# Phoenix Serverless Swarm (bounded first adapter)

## Honest runtime boundary
This is a deploy-ready Cloudflare Worker + Durable Object starter. Durable Object storage coordinates task state and append-only per-task receipt chains. The first worker executes only deterministic `echo` and `sum` operations. It is a real serverless execution endpoint, **not** a distributed LLM-agent swarm. Model roles remain unavailable until a server-side provider adapter is configured and independently verified.

## Deploy
1. Install Node.js 20+ and authenticate Cloudflare: `npx wrangler login`.
2. Set `ALLOWED_ORIGIN` in `wrangler.toml` to the exact published Phoenix app origin.
3. Set a strong secret without committing it: `npx wrangler secret put SWARM_TOKEN`.
4. From this directory run `npm install -D wrangler typescript vitest` (or use your existing toolchain), then `npx wrangler deploy`.
5. Save the deployment URL and configure it in Phoenix Swarm as a remote endpoint. Never embed SWARM_TOKEN in browser code; add an authenticated server-side proxy before calling from a public browser.

## Smoke test
```sh
export BASE_URL='https://YOUR-WORKER.YOUR-SUBDOMAIN.workers.dev'
export SWARM_TOKEN='your-secret-from-secret-manager'
curl -sS "$BASE_URL/health"
curl -sS -X POST "$BASE_URL/tasks" \
  -H "Authorization: Bearer $SWARM_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: smoke-sum-001' \
  --data '{"operation":"sum","values":[2,3,5]}'
# Copy task id from response:
curl -sS -H "Authorization: Bearer $SWARM_TOKEN" "$BASE_URL/tasks/TASK_ID/verify"
curl -sS -H "Authorization: Bearer $SWARM_TOKEN" "$BASE_URL/tasks/TASK_ID/receipts"
```

## Limits and safety
- POST body is limited by operation schema: echo text <= 2,000 chars; sum 1-100 finite numbers.
- Configurable active-task cap defaults to 3, max 10. No arbitrary code execution or external side effects.
- Authorization required except health; exact-origin CORS allowlist; idempotency key required.
- Durable Object coordinates a single named global namespace for this starter. Expand sharding only after measured tests.
- Hash-chain receipts are tamper-evident, not cryptographic signatures or external timestamps. A compromised coordinator/storage account could rewrite the chain; export and externally anchor receipt heads for stronger evidence.
- Do not send secrets in task payloads. Configure logging/retention and billing alerts before production use.
- Rollback: deploy a reviewed previous commit/version with Wrangler; retain receipt exports before schema migrations.
