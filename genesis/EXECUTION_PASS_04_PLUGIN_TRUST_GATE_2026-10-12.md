# Conzetian Execution Pass 04: Plugin Trust Gate and CI Signal Quality

Date: 2026-10-12

## Concrete changes committed

1. `genesis/plugin_trust_policy.py` (commit `33bd09f0e74489f7d087907ad981364f1c66d171`)
   - Adds a non-executing plugin-path validation function.
   - Requires an exact allowlisted relative path under a trusted root.
   - Rejects traversal, symlinks, unlisted plugins, missing files, non-Python suffixes, and optional SHA-256 mismatches.
   - Explicitly returns `execution_performed: false` and `safety_verdict: NOT_ASSESSED` when the checks pass.
   - It is not yet wired into the legacy M.A.I.A. loader. It must be called before dynamic import, and untrusted plugins still require process isolation.

2. `tests/test_plugin_trust_policy.py` (commits `936175329e3d22175673889a50d400ff13ccdc87` and correction `69276b908851ebd0f536d2f94cdfccf158c5f503`)
   - Covers allowlisted path acceptance, unlisted plugin rejection, digest mismatch, traversal, symlink rejection, and missing files.
   - The test has been committed but has not yet been independently run in this report.

3. `.github/workflows/python-ci.yml` (commit `d4cb03d3a71d8782c78b767051f88ecedff52072`)
   - Adds a strict, targeted `python -m pytest -q tests/test_plugin_trust_policy.py` step without `|| true`.
   - This preserves the existing broad test step while ensuring this security gate cannot silently pass because of the existing `pytest || true` behavior.

## Newly discovered CI integrity issue

The existing broad test command is `pytest || true`, which suppresses a non-zero test exit status. Consequently, a green workflow alone is not sufficient proof that the broad test suite passed. The new targeted step is strict for the plugin trust-policy tests only. A future hardening pass should make the full test suite strict after existing repository failures are understood and corrected.

## Verified external workflow state

- The Diamond Watch run `38313831733` completed with conclusion `success`; all listed audit job steps completed successfully.
- That run returned no artifacts. Therefore, the workflow audit passed, but a downloadable Diamond Watch report artifact remains unconfirmed.
- The core integration run `38313585782` also returned no artifacts.
- These results establish the state of the inspected GitHub Actions runs, not continuous background execution or production operation.

## Remaining gates

1. Confirm the new commit's targeted CI step actually runs and passes.
2. Wire the trust policy into a safe integration point before any plugin import; do not execute plugin code during validation.
3. Add tests for platform-specific path behavior and trusted-root configuration.
4. Evaluate process isolation, resource limits, network access, secrets exposure, and plugin dependency pinning.
5. Prototype MCP Memory Service in read-only mode and compare against Cognee on a fixed retrieval/provenance test corpus.
6. Validate SkillMD portability against the Agent Skills specification and test Vercel Skills CLI only on a disposable fixture corpus.
7. Obtain actual scheduled daemon and Diamond Watch artifacts before claiming scheduled operation.

## Evidence boundary

The code and workflow updates are committed to GitHub. This document does not claim the new targeted CI has passed, the policy is integrated into the live M.A.I.A. execution path, candidate memory services are installed, or autonomous agents are running continuously.
