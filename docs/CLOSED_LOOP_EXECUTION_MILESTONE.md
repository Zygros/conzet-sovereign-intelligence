# Conzetian Closed-Loop Execution Milestone
**Status:** ROADMAP / NOT YET DEMONSTRATED END-TO-END  
**Purpose:** Define the next strategic milestone for the Conzetian Sovereign Framework in testable, evidence-gated terms.

## Decree
Reach a working closed-loop execution system that can discover a real task, plan it, execute it, verify the outcome independently, preserve provenance, learn from observed failure, and begin another cycle.

`DISCOVER → PLAN → EXECUTE → VERIFY → RECORD → REFLECT → CONTROLLED IMPROVEMENT → REPEAT`

This document is a milestone specification, not a claim that autonomous execution or self-improvement is already complete.

## Current foundation observed in the repository
- **Opportunity Scout:** discovers and publishes opportunity records.
- **Federation Health:** runs and publishes structural health results.
- **Witness:** checks repository structure and publishes a report. The latest recorded run passed five structural checks; those checks do not establish semantic correctness.
- **Evidence Chain:** records implementation history and separates implementation, testing, and independent verification.
- **CI and Phoenix Audit:** recent recorded runs completed successfully. These results establish only the checks those workflows actually performed.

## Milestone gates

### Gate 1 — Artifact integrity
- Recompute SHA-256 for every artifact named by the Scout manifest.
- Compare each computed digest to the manifest and record command, environment, exit status, and results.
- Verify OpenTimestamps proofs using the official client in an environment with required network access.
- Record Bitcoin confirmation and block height only when the verifier actually reports them.
- **Pass condition:** all required artifact hashes match; timestamp claims are explicitly confirmed or marked unresolved.

### Gate 2 — Independent reproduction
- Provide a reviewer with the artifact, exact commands, dependency versions, and expected results.
- Have a reviewer outside the originating execution context reproduce the result.
- Preserve reviewer identity/context, commit or report reference, hashes, and discrepancies.
- **Pass condition:** an independent reproduction matches, or discrepancies are documented and resolved.

### Gate 3 — One real task end-to-end
- Select one bounded, low-risk software task with a clear acceptance test.
- Record the task and expected outcome before execution.
- Plan and execute using a controlled agent/tool path.
- Run tests in a clean environment and preserve logs and artifacts.
- Ask an independent verifier to assess the result against the acceptance test.
- **Pass condition:** the task passes its predeclared acceptance criteria and evidence is reproducible.

### Gate 4 — Evidence-backed reflection
- Compare expected versus observed outcomes.
- Classify failures and propose one narrowly scoped improvement.
- Test the proposed change separately before integrating it.
- Preserve the prior state and append a new evidence record; never overwrite historical evidence.
- **Pass condition:** the improvement has a demonstrated effect on a repeatable test, or is rejected with reasons.

### Gate 5 — Repeatable closed loop
- Automatically queue the next bounded task only after required verification gates pass.
- Add time, cost, scope, and safety limits; require human approval for sensitive or destructive actions.
- Include stop conditions, rollback/recovery plans, and a complete execution trace.
- **Pass condition:** at least two consecutive task cycles complete with reproducible evidence and no unauthorized action.

## Non-negotiable invariants
1. **Always Add, Never Take:** preserve prior evidence and append new records.
2. **Always Add ≠ Always Accept:** candidate changes must pass tests and review before integration.
3. **No self-promotion:** automation cannot promote its own claims to independently verified status.
4. **Hashes prove byte identity, not truth.** A successful workflow proves only what its checks actually tested.
5. **Timestamp precision:** an `.ots` file's presence is not proof of Bitcoin confirmation.
6. **Capability claims follow evidence:** distinguish designed, implemented, tested, reproduced, and independently verified states.
7. **Bounded autonomy:** use least privilege, resource limits, explicit stop conditions, and human approval for high-impact actions.

## Scorecard
Track these per cycle:
- task acceptance-test pass rate
- independent reproduction pass rate
- defects caught before integration
- failed or unsafe actions
- hash/manifest agreement
- confirmed versus unconfirmed timestamp proofs
- execution time and resource cost
- improvement effect on a repeatable benchmark

Do not optimize a single aggregate score at the expense of safety or evidence quality.

## Immediate next action
Complete Gate 1 for the published Scout run `38329245120`: recompute the hashes for `opportunity-scout.json` and `verification-receipts.json`, then independently verify both corresponding `.ots` proofs. Keep all results at pending review until independently reproduced.

## Exit criterion for the strategic milestone
The milestone is reached only when one bounded real task completes the full discover-to-repeat loop, an independent reviewer reproduces the evidence, and a subsequent cycle demonstrates a tested improvement without erasing prior records.
