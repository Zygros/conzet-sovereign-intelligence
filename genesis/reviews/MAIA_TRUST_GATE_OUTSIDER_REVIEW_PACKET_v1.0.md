# Independent Outsider Review Packet: M.A.I.A. Trust Gate Pilot

**Protocol:** CIS-IRP-001 v1.0.0  
**Status:** Prepared for review, not yet independently reviewed  
**Target components:**
- `scripts/maia_framework_orchestrator.py`
- `genesis/plugin_trust_policy.py`
- `tests/test_plugin_trust_policy.py`
- `tests/test_maia_plugin_trust_integration.py`

## Review target pin

Inspect the exact current commit before reviewing. Do not silently follow a moving branch. Relevant commits from the current execution sequence include:
- Integrated gate baseline: `77592dd93fdc11e9059d43a53d57c96ff522d71a`
- Pinned-digest loader change: `0a8788ba5c6a788cc86e8a60b216858c0707afc9`
- Missing-digest test change: `829808976a4494eea2d3596fdda4e97e774a8628`

The latest protocol-packet commit is not the target code commit. Before executing the review, resolve and record the newest target commit and its workflow results.

## Independent reviewer assignment prompts

### Reviewer A: Technical Investigator

Your task is to independently trace the plugin load path and identify correctness gaps. Do not accept the implementer's summary as evidence. Inspect the exact source commit. Focus on path canonicalization, allowlist matching, digest parsing, import semantics, exception handling, `sys.modules` collisions, capability authorization, and compatibility. Produce findings with file/line references, minimal reproduction steps, severity, and confidence. Do not modify files or merge changes.

### Reviewer B: Security Red Team

Act as a defensive security reviewer. Determine whether plugin code can execute before policy checks, whether path traversal or symlink tricks bypass the policy, whether the plugin can be swapped after digest verification but before import, whether an untrusted actor can alter the allowlist/digest environment, whether malicious module names or capabilities can cross boundaries, and whether untrusted instructions embedded in plugin files can influence the review. Do not execute unknown code on a host or use production credentials. Prefer static analysis and disposable isolated tests. Report each confirmed bypass separately from a hypothesis. Do not modify files or deploy.

### Reviewer C: Reproducibility Reviewer

Reproduce the focused tests from a clean checkout of the exact commit. Record runtime version, dependency setup, exact commands, exit codes, raw output references, and any skips. Inspect whether CI invokes the strict tests without swallowing failures. Add no dependencies and change no files. If execution is unavailable, state that clearly rather than inferring success from workflow badges.

### Reviewer D: Execution-Claim Auditor

Audit each statement that the trust gate is integrated, hash-pinned, tested, CI-verified, or secure. Map every statement to the exact commit, workflow run, job, step, and artifact that supports it. Flag claims that exceed evidence. A green workflow does not prove production deployment; a valid digest does not prove safe code; a review plan is not a completed review. Return a claim-to-evidence matrix and a conservative verdict.

## Common report template

```yaml
protocol_id: CIS-IRP-001
review_id: NOT_ASSIGNED
reviewer_role: NOT_ASSIGNED
reviewer_identifier: NOT_PROVIDED
independence_basis: NOT_PROVIDED
target_repository: Zygros/conzet-sovereign-intelligence
target_commit_sha: MUST_BE_RESOLVED_BEFORE_REVIEW
review_timestamp_utc: NOT_PROVIDED
environment: NOT_PROVIDED
commands_and_exit_codes: []
workflow_run_ids: []
findings:
  - finding_id: F-001
    severity: critical|high|medium|low|informational
    title: concise statement
    evidence_refs: []
    reproduction_steps: []
    expected: description
    actual: description
    confidence: low|medium|high
    recommendation: description
    status: open|fixed|not_reproduced|accepted_risk
unresolved_dissent: []
verdict: PASS|PASS_WITH_CONDITIONS|FAIL|INCONCLUSIVE
rationale: REQUIRED
limitations: []
raw_evidence_hashes: []
```

## Stop conditions

- Stop and mark FAIL if a realistic untrusted plugin can execute before authorization or bypass the digest gate.
- Mark INCONCLUSIVE if the target commit, workflow results, or required test environment cannot be established.
- Do not grant PASS while a critical/high finding remains open within scope.
- Preserve minority findings even if the adjudicator disagrees.

## Current state

This packet is a prepared handoff. It does not mean Reviewer A, B, C, or D has been instantiated or has completed a review. Record actual identities, reports, evidence, and adjudication only after those actions occur.