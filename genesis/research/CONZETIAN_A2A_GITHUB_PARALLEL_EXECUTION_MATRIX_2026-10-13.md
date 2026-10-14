# Conzetian A2A ↔ GitHub Parallel Execution Matrix
**Date:** 2026-10-13  
**Status:** Workstreams tracked in GitHub; live service not deployed  
**Doctrine:** Always Add, Never Take

## Operating principle
Run architecture, ingress/queue, A2A routing, verification/telemetry, deployment, and adversarial testing as parallel workstreams. Integrate through versioned contracts and evidence receipts. “Simultaneous” means concurrent independent work, with dependencies explicitly gated where integration requires them.

## Master architecture
Specification: https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/genesis/research/CONZETIAN_A2A_GITHUB_CONTINUOUS_PIPELINE_SPEC_2026-10-13.md  
Master build issue: https://github.com/Zygros/conzet-sovereign-intelligence/issues/3

## Parallel workstreams
| Track | Work | Issue | Exit evidence |
|---|---|---|---|
| A. Ingress + queue | HTTPS webhook, HMAC validation, delivery dedupe, durable enqueue, retries | https://github.com/Zygros/conzet-sovereign-intelligence/issues/4 | Passing signature, dedupe, restart/retry tests; live delivery receipt |
| B. A2A routing | Versioned envelopes, capability routing, identity, policy gates, timeouts | https://github.com/Zygros/conzet-sovereign-intelligence/issues/5 | Contract tests and denial tests; trace IDs preserved |
| C. Verify + observe | Independent verifier, append-only receipts, p50/p95/p99, queue/retry metrics | https://github.com/Zygros/conzet-sovereign-intelligence/issues/6 | Receipt schema, tests, observed latency samples |
| D. Deployment | HTTPS hosting, secret manager, queue provisioning, GitHub webhook activation and shutdown runbook | https://github.com/Zygros/conzet-sovereign-intelligence/issues/7 | Deployment config, health checks, safe live delivery test |
| E. Adversarial reliability | Tampering, duplicates, out-of-order events, crash/restart, replay, timeout, outage | https://github.com/Zygros/conzet-sovereign-intelligence/issues/8 | Automated fault matrix with expected outcomes |

## Shared contracts
- Every event has a stable delivery ID, repository, event type, source ref/commit SHA when available, received timestamp, schema version, and correlation ID.
- Queue consumers assume at-least-once delivery. All side effects must be idempotent.
- Agent results are typed, bounded, and linked to their input commit/event.
- Read-only by default. Write actions require a policy decision and an explicit allowlist.
- Receipts are append-only. Existing source files, commits, and evidence are not silently replaced.
- CI status and workflow/job output are the source of truth for test claims.
- Secret material exists only in deployment secret storage, never in source or logs.
- Superseded work may be cancelled to save capacity, but its receipt remains in the ledger.

## Integration gates
1. **Contract gate:** envelope and receipt schemas agreed before cross-track merge.
2. **Security gate:** signature and authorization tests pass before accepting live events or enabling writes.
3. **Reliability gate:** duplicate, retry, restart, replay, and timeout tests pass before live pilot.
4. **Pilot gate:** one repository, push/workflow events, read-only processing, exact commit linkage.
5. **Expansion gate:** observed latency and error metrics reviewed before onboarding additional repositories or write-capable agents.

## Honest state boundary
This matrix and its issues are committed coordination artifacts. They do not themselves provision infrastructure, configure GitHub webhooks, establish an A2A network, or demonstrate live latency. The deployment track must produce a successful live delivery receipt before the pipeline is described as connected.
