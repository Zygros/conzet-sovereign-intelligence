# Phoenix Proof Cycle

## Purpose

This is a deterministic local harness for validating the execution-verification machinery around Phoenix. It runs a small Scout fixture, validates its structured output, optionally repairs a seeded defect, re-verifies the repaired result, and records every stage in a SHA-256 hash-chained JSON ledger.

It is an additive verification primitive, not a replacement for the Phoenix architecture.

## Run locally

Requires Python 3.10+ and no third-party packages.

    python tools/phoenix_proof_cycle.py --self-test
    python tools/phoenix_proof_cycle.py --task "my task" --output receipt.json
    python tools/phoenix_proof_cycle.py --task "fault test" --inject-defect --output repaired-receipt.json
    python tools/phoenix_proof_cycle.py --task "fault remains visible" --inject-defect --no-repair

The no-repair invocation intentionally returns a non-zero status for a failed cycle.

## What the checks cover

- Clean task path and a valid append-only event sequence.
- Deliberately empty evidence field is detected.
- A single bounded repair is applied and independently re-verified.
- Explicit failure remains visible when repair is disabled.
- Ledger event content, sequence, and previous-hash links are verified.
- Export hash and ledger integrity are checked, including tamper detection.
- Empty tasks are rejected.

## CI

The Phoenix Proof Cycle GitHub Actions workflow runs the self-tests, a clean acceptance cycle, a seeded-fault repair cycle, and uploads JSON receipts as workflow artifacts.

Workflow: https://github.com/Zygros/PHOENIX-PROTOCOL-ULTIMATE/actions/workflows/phoenix-proof-cycle.yml

## Evidence boundary

The Scout is a deterministic local fixture. It does not perform web research or call an external AI provider. The receipts explicitly mark Bitcoin, Arweave, and OpenTimestamps anchors as absent. A valid local hash chain establishes consistency of the recorded bytes, not independent truth, remote immutability, or production readiness. External anchors must be added only when the actual provider returns a verifiable receipt.
