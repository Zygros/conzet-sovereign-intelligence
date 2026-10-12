# Execution Pass 06: Pinned Plugin Integrity Gate

Date: 2026-10-12

## Changes committed

- `scripts/maia_framework_orchestrator.py` now requires `MAIA_PLUGIN_TRUST_ROOT`, `MAIA_PLUGIN_ALLOWLIST`, and `MAIA_PLUGIN_SHA256_ALLOWLIST` before importing a plugin.
- The loader parses exact `relative/path.py=64-character-hex-sha256` entries and rejects missing or malformed digests.
- The selected plugin digest is passed to `validate_plugin_path`; a mismatch is rejected before dynamic import.
- `tests/test_maia_plugin_trust_integration.py` now pins the fixture's digest and adds a test that missing digest configuration blocks loading.

## Configuration example

For a trusted plugin at `/srv/maia/plugins/example.py`:

```sh
export MAIA_PLUGIN_TRUST_ROOT=/srv/maia/plugins
export MAIA_PLUGIN_ALLOWLIST=example.py
export MAIA_PLUGIN_SHA256_ALLOWLIST=example.py=<the-reviewed-64-character-sha256>
```

Obtain the digest from the reviewed release artifact, not from the same untrusted plugin at runtime. If multiple plugins are configured, use comma-separated relative-path entries in both allowlist variables and matching path=digest entries in the digest variable. Treat environment variables as deployment configuration and protect them from untrusted writers.

## Verification ledger

- Commit `77592dd93fdc11e9059d43a53d57c96ff522d71a`: OmniNet Python CI passed on Python 3.8, 3.9, 3.10, and 3.11, including strict trust-policy and M.A.I.A. integration tests. Phoenix Audit passed.
- Commit `0a8788ba5c6a788cc86e8a60b216858c0707afc9`: pinned-digest loader change was committed; its CI and audit were in progress at the time of this report.
- Commit `829808976a4494eea2d3596fdda4e97e774a8628`: missing-digest test was committed; its CI and audit were queued at the time of this report.
- Do not treat the last two commits as verified until their own workflow runs complete successfully.

## Security boundary

Pinned SHA-256 detects changes relative to the reviewed digest. It does not prove a plugin is benign, protect against a compromised reviewer or build pipeline, or sandbox Python execution. Only reviewed plugins should be allowlisted. Untrusted plugins still require separate-process isolation, resource limits, restricted network access, and secrets minimization.

## Outstanding work

1. Confirm CI and Phoenix Audit for commit `829808976a4494eea2d3596fdda4e97e774a8628`.
2. Consider a signed manifest or deployment-owned digest file rather than environment variables for larger deployments.
3. Add subprocess isolation before allowing untrusted or third-party plugins.
4. Run the MCP Memory Service and Cognee comparison on a fixed local fixture, read-only, without exposing credentials.
5. Run skill-format compatibility checks against a disposable copy of the corpus.
6. Verify scheduled daemon and Diamond Watch artifacts before making any claim of persistent background operation.

## Truth classification

Code changes: committed. Earlier trust gate and integration tests: CI verified. Pinned digest hardening: committed but pending CI at report time. Memory service and skill CLI candidates: researched only, not installed or tested. Continuous autonomous execution: not established by this report.
