# Phoenix Ω∞ — Serverless Friction-Resilience Blueprint
Date: 2026-10-16
Status: Architecture blueprint; not a deployment claim.

## Objective
Make temporary failure of a tool, provider, serverless endpoint, or build environment a recoverable routing event rather than a total system stop, while keeping the sovereign core private by default.

## Non-negotiable invariants
- Sovereignty first: private memory, personal data, strategy, credentials, and the complete master architecture are not published by default.
- Always Add, Never Take: corrections are appended as superseding versions; historical evidence is retained.
- Always Add does not mean Always Accept: untrusted outputs enter quarantine until validated.
- No false execution claims: simulated, implemented, tested, independently reproduced, and verified are distinct evidence states.
- Least privilege: each adapter receives only the data and authority needed for its task.
- Provider independence: a provider is an adapter, not the system's single point of failure.
- No secret in browser code, source control, public logs, or task payloads.

## Layered topology
1. Sovereign Core (private/local): master memory, policy, question chain, private ledger, local configuration.
2. Local Executor (Android/Termux where feasible): offline-capable deterministic tasks, validation, queueing, and replay.
3. Router: selects local execution first where capable; otherwise selects an approved provider/worker by health, capability, cost, privacy class, and evidence requirements.
4. Adapter Plane: versioned interfaces for Cloudflare Worker, model APIs, MCP/A2A endpoints, and future providers. No provider-specific assumptions leak into the core.
5. Evidence Plane: append-only task events, input/output digests, adapter/version identity, timestamps, status, and receipt-chain head.
6. Witness Plane: independent verification of outputs where possible; external anchoring is optional and must be explicitly confirmed.
7. Public Plane: intentionally selected source/interfaces/proofs only. Never sync the private core by default.

## Failure protocol
For each task:
1. Classify sensitivity and required capability.
2. Create a task ID and append a DISPATCHED event.
3. Choose the least-privilege eligible adapter.
4. Apply bounded retries with exponential backoff and jitter for transient failures only.
5. If the adapter is unavailable, route to a preapproved alternate or queue the task locally. Do not silently downgrade privacy or verification.
6. Validate schema, task-specific acceptance criteria, and evidence requirements.
7. Append success/failure and receipt references; preserve the original failed attempt.
8. If all routes fail, return a specific blocker and a reproducible recovery action, not a fabricated success.
9. Replay only idempotent tasks automatically; require explicit policy for external side effects.

## Serverless-specific safeguards
- Health endpoint separate from authenticated task endpoints.
- Exact CORS origin allowlist and bearer token stored as a platform secret.
- Explicit raw request byte cap before JSON parsing.
- Schema limits, task deadline, active-task cap, rate limits, and bounded retry budget.
- Idempotency key with atomic storage semantics; test concurrent duplicate requests.
- Cancellation contract states whether cancellation is queued-only, cooperative, or guaranteed before execution.
- Durable Object/global coordinator limits are measured before sharding; never assume global scale from logical slot arithmetic.
- Receipt hash chain is tamper-evident but not a signature, independent witness, or Bitcoin anchor.
- Export receipt heads and optionally anchor them externally; mark anchoring confirmed only after verifier output proves it.

## Data disclosure gate
Classify each outbound artifact as PUBLIC_SAFE, PRIVATE, SECRET, or REVIEW_REQUIRED.
- PUBLIC_SAFE: approved interface, non-sensitive code, or minimal proof.
- PRIVATE: personal memory, unpublished strategy, private architecture.
- SECRET: tokens, keys, credentials, signing material.
- REVIEW_REQUIRED: ambiguous data, logs with possible identifiers, or mixed-content artifacts.
Only PUBLIC_SAFE may publish automatically. PRIVATE and SECRET are blocked. REVIEW_REQUIRED requires owner approval and redaction. Hashes do not make sensitive source content safe to publish.

## Permanent question-cycle protocol
For each verified answer:
- Preserve question, answer, evidence class, and limitations.
- Generate at least one higher-capacity follow-up question.
- Score follow-ups for leverage density and whether they improve generation, scoring, memory, routing, or verification.
- Preserve every candidate, but execute only the highest-value candidate that passes safety and evidence gates.
- Treat scoring changes as versioned proposals; run a fixed regression set before activation. Never let a scoring rule rewrite itself silently.

## Resilience acceptance tests
- Local deterministic task succeeds with network disabled.
- Provider A failure routes to Provider B only if privacy and capability policy permit.
- If no alternate is eligible, task queues or returns a precise blocker without data leakage.
- Invalid and oversized bodies are rejected before expensive processing.
- Concurrent duplicate idempotency keys create one logical task.
- Retry budget and task deadline are enforced.
- Cancellation response matches actual execution state.
- Receipt tampering fails verification.
- Receipt chain is independently reproduced from exported bytes.
- Secret scanning covers current tracked files; history review is a separate gate.
- Reboot/restart preserves permitted local memory and ledger state.
- Public export contains only approved artifacts.

## Immediate implementation sequence
P0: Freeze further public disclosures until the owner reviews repository visibility and sensitive history.
P1: Establish local private core and encrypted backup; no credentials in Git.
P2: Add request byte cap, task deadline, atomic idempotency behavior, and focused regression tests to the Worker.
P3: Implement a provider-neutral adapter contract and explicit local queue/fallback state machine.
P4: Add a disclosure classifier to every export/publication path.
P5: Deploy only with the owner's authenticated Cloudflare session, real origin, and secret.
P6: Run one live deterministic task; retain exact request/response and receipt export.
P7: Have a separate reviewer reproduce the receipt check before promoting evidence status.
P8: Add model-backed roles only after the bounded worker passes the above acceptance tests.

## Current known state
The existing Phoenix Worker README describes deterministic echo/sum operations, Cloudflare Worker + Durable Object, bearer-token authorization, idempotency keys, a concurrency cap, and append-only per-task hash-chain receipts. It explicitly states this is not yet a distributed LLM-agent swarm. The current `wrangler.toml` still has a placeholder ALLOWED_ORIGIN. Deployment requires Cloudflare authentication and a secret. This blueprint does not claim that deployment, live fallback, local Termux execution, or a provider-backed swarm has been performed.

## Definition of done
The system demonstrates, with retained evidence, that a bounded task completes locally or through an approved serverless adapter, recovers from a simulated provider outage without violating privacy policy, emits verifiable receipts, survives restart, and does not publish private core material. All production claims remain evidence-gated.
