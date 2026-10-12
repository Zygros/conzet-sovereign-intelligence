---
name: conzetian-scheduled-operations-verifier
version: 1.0.0
purpose: Verify scheduled automation ran and produced expected effects, not merely that configuration exists.
---

# Conzetian Scheduled Operations Verifier

1. Confirm workflow file, schedule expression, timezone assumptions, and enabled state where observable.
2. Retrieve actual runs and record run ID, event type, timestamp, head SHA, conclusion, and duration.
3. Inspect jobs and steps, including skipped, cancelled, or tolerated failures.
4. Inspect expected artifacts, creation time, expiry, and contents where accessible.
5. Compare output against acceptance criteria. A green empty run is not proof of useful work.
6. For external effects, require an authoritative receipt or destination read-back.
7. Evaluate cadence over a stated window with expected and observed run counts.
8. Distinguish CONFIGURED, RUN OBSERVED, ARTIFACT VERIFIED, EFFECT VERIFIED, and CADENCE VERIFIED.
9. If runs or artifacts are absent, state the gap and next diagnostic step. Never synthesize logs or receipts.

## Verdicts
CONFIGURED_ONLY, RUN_OBSERVED, ARTIFACT_VERIFIED, EFFECT_VERIFIED, CADENCE_VERIFIED, BLOCKED, INCONCLUSIVE.

Do not label a planner as an executor or scheduled configuration as a continuously running daemon.