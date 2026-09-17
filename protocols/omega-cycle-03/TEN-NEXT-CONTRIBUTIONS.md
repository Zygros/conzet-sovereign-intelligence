# Ω-Cycle 03 — Ten Next Contributions

1. **Executable Contract Validator** — convert the Cycle 02 validator contract into runnable code with positive and negative fixtures.
2. **Receipt JSONL Emitter** — emit deterministic append-only execution receipts from real operations.
3. **Live Capability Manifest** — generate a machine-readable capability snapshot from the actual connected tool surface.
4. **Causal Graph Materializer** — turn receipt/evidence/patch relations into a queryable graph representation.
5. **Verification Transition Tests** — add fixtures that prove invalid state promotions are rejected.
6. **Failure Replay Fixture Set** — create canonical failed executions and materially different retry hypotheses.
7. **Provenance Resolver CLI** — implement backward/forward artifact tracing over the cycle records.
8. **Baseline/Intervention Runner** — create a minimal deterministic benchmark harness with declared metrics.
9. **Publication Metadata Generator** — generate a stable discovery bundle from a verified execution record.
10. **Evolution Gate Integration Test** — exercise promotion, rejection, regression, and next-hypothesis requirements end to end.

## Cycle rule
Execute each contribution where runtime capability permits. Every implementation must produce observable evidence. Preserve failures and blockers. Do not promote an implementation artifact to VERIFIED without actual execution evidence.
