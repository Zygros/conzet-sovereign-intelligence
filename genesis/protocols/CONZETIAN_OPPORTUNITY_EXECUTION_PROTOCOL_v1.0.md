# Conzetian Opportunity Execution Protocol v1.0

ID: CIS-OEP-001
Date: 2026-10-12
Status: Procedure committed; each run must produce its own evidence.

## Prime rule
Always Add, Never Take. Always Do, Never Don't. Execution is evidence-gated: preserve prior records, append new findings, and never relabel a proposal as completed action.

## Required stages
1. Inventory the opportunity, source, target repository/commit, expected benefit, dependencies, cost, risk, owner, and expiry.
2. Classify as IDEA, READY, BLOCKED, RUNNING, TESTED, VERIFIED, DEPLOYED, or REJECTED. Cite evidence for every status.
3. Prioritize impact, confidence, urgency, reversibility, and cost. Security, data loss, secret exposure, and misleading claims outrank growth work.
4. Prepare by freezing the target commit, defining acceptance criteria and containment plan, and using least privilege.
5. Execute only through available tools and granted permissions. If an external action or separate agent is unavailable, create a handoff packet and mark BLOCKED, not executed.
6. Verify with targeted tests and relevant CI. Capture run IDs, commit SHA, commands, exit status, artifacts, and test gaps.
7. Independently review security-sensitive or high-impact work. Preserve dissent.
8. Adjudicate PASS, PASS WITH CONDITIONS, FAIL, or INCONCLUSIVE. Critical unresolved findings block release.
9. Append machine-readable and human-readable evidence, including failures.
10. Turn confirmed lessons into versioned skills or regression tests without rewriting historical records.

## Evidence labels
PROPOSED, COMMITTED, TESTED LOCALLY, CI-VERIFIED, INDEPENDENTLY REPRODUCED, SECURITY-REVIEWED, DEPLOYED, OPERATIONALLY VERIFIED, CONTINUOUSLY OPERATING, UNVERIFIED.

## Stop conditions
Stop and record BLOCKED if permissions are missing, secrets could be exposed, the target is ambiguous, destructive mutation lacks backup and approval, or evidence contradicts the requested claim. Continue independent safe work where possible.

## Minimum run record
run_id, UTC timestamp, actor/tool, target commit, objective, steps attempted, outcome, test results, artifact links, failure details, evidence label, reviewer, residual risks, next action.

## Release gate
No high-impact change is released with unresolved Critical findings. Do not claim deployment, autonomous operation, external propagation, independent review, permanent anchoring, or revenue without direct evidence for that specific claim.

## First execution queue
1. Outsider review of the M.A.I.A. trust gate.
2. Hash-to-import race investigation and regression test.
3. CI broad-suite failure-masking assessment.
4. Scheduled-workflow run and artifact proof.
5. Memory/skill candidate benchmark.
6. Opportunity ledger and recurring review cadence.

This protocol defines a process. It does not itself spawn agents, grant permissions, deploy services, or prove execution occurred.