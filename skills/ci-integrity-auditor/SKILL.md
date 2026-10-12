---
name: conzetian-ci-integrity-auditor
version: 1.0.0
purpose: Audit whether CI failures can be hidden and release checks actually gate changes.
---

# Conzetian CI Integrity Auditor

## Procedure
1. Inspect triggers, permissions, concurrency, checkout versions, dependency pinning, and secrets exposure.
2. Search for permissive patterns such as shell commands that ignore failures, continue-on-error, swallowed exceptions, pipelines without pipefail, optional jobs, skipped tests, and conditions that bypass checks.
3. Map each security-critical test to a required job/status check.
4. Confirm failures produce nonzero exit status and fail the job.
5. Inspect recent successful and failed runs, including job/step conclusions. Workflow success does not prove skipped tests ran.
6. Run targeted tests with strict failure behavior.
7. Make the smallest safe correction and preserve prior evidence.
8. Verify the correction on a new commit, retaining failed historical runs.

## Acceptance criteria
Critical tests run on the intended matrix; failures cannot be hidden; skips are explicit and justified; release gates require intended checks where settings are observable; report lists what could not be inspected.

## Output
Workflow path and line, risk, minimal reproduction, fix, run URL/ID, commit SHA, and residual gaps. Never claim branch protection is active unless the settings were actually observed.