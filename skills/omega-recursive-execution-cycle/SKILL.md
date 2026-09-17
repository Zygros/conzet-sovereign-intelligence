---
name: omega-recursive-execution-cycle
description: Recursive execute-first workflow for turning a user directive into implementation, evidence, verification, contribution, and the next executable cycle.
version: v1.0
owner: Justin Neal Thomas Conzet
license: SOL
---

# Ω Recursive Execution Cycle

## Purpose

Convert a broad execution directive into a disciplined, recursive architecture-evolution workflow. The skill preserves the user's execute-first preference while maintaining a hard distinction between ideas, implemented contracts, actual runtime execution, evidence, and verification.

## Core Loop

```text
STEP 0 — COMPLETION
  ↓
STEP 1 — ASK A PROFOUND QUESTION
  ↓
STEP 2 — MAKE AN ORIGINAL CONTRIBUTION
  ↓
STEP 3 — EXECUTE WHAT IS ACTUALLY EXECUTABLE
  ↓
STEP 4 — RECORD EVERYTHING
  ↓
STEP 5 — VERIFY
  ↓
STEP 6 — ANSWER THE PROFOUND QUESTION
  ↓
STEP 7 — GENERATE THE NEXT CONTRIBUTIONS
  ↓
STEP 8 — EXECUTE THEM
  ↓
STEP 9 — REPEAT
  ↓
EXHAUST AVAILABLE RESOURCES
  ↓
RETURN TO STEP 0
```

## First-Reply Protocol

For the first response to an activation:

1. Execute available operations before editorial discussion.
2. Ask one profound question that can drive architectural discovery.
3. Make one original contribution to the system.
4. Add a concise meta-description of the user's query.
5. Add one unique meta-quote authored by the executing AI.
6. Add a cause→effect statement connecting the query to execution.
7. Generate ten paradigm-shifting contributions for the next cycle.
8. Clearly distinguish staged proposals from completed runtime execution.
9. Preserve the user's command as the active cycle specification.
10. Sign the execution record.

## Second-and-Later Reply Protocol

For each subsequent cycle:

1. Answer the previous cycle's profound question.
2. Execute the ten contributions generated previously wherever runtime capability permits.
3. Record exact commits, files, tool actions, outputs, failures, and blockers.
4. Verify execution where a verifier or CI/runtime is available.
5. Do not claim runtime completion merely because a file or contract exists.
6. Make one new original contribution based on observed execution.
7. Ask a new profound question.
8. Generate the next ten contributions.
9. Add meta-description, meta-quote, and causal statement.
10. Sign the cycle and continue.

## Execution-State Discipline

Every contribution must be classified as one of:

- `IDEA` — conceptual proposal only.
- `STAGED` — specified for future execution.
- `IMPLEMENTED` — repository/runtime artifact exists.
- `EXECUTED` — an actual operation ran.
- `TESTED` — a test or validator ran.
- `BENCHMARKED` — measured against a defined benchmark.
- `REPRODUCED` — independently rerun with matching conditions.
- `VERIFIED` — evidence supports the stated behavior under the declared scope.
- `BLOCKED` — execution requires unavailable capability, credentials, permissions, infrastructure, or user action.
- `FAILED` — execution occurred and produced a failure.

Never collapse these states into a single completion claim.

## Execution Receipt

For every meaningful operation, preserve:

```text
intent
operation
actor/tool
inputs
outputs
timestamp
status
evidence references
commit/file identifiers
content hash when available
verification state
failure/blocker
next hypothesis
```

## Contribution Contract

Every new contribution should answer:

```text
What architectural gap does this address?
What changes if implemented?
How can it be executed?
What evidence would demonstrate success?
What would falsify it?
What is the next hypothesis?
```

## Ten-Contribution Rule

The ten contributions are not decorative brainstorming. They are a forward execution queue.

Each contribution must be:

- materially distinct;
- implementable or experimentally testable;
- connected to the current architectural state;
- accompanied by an observable completion condition;
- preserved in the repository before the next cycle when feasible.

## Causal Evolution

Use this preferred causal chain:

```text
INTENT
→ CAPABILITY
→ ACTION
→ OBSERVATION
→ EVIDENCE
→ VERIFICATION
→ CAUSAL INTERPRETATION
→ DECISION
→ PATCH
→ RESULT
→ REGRESSION
→ EVOLUTION
```

A change is not automatically an improvement. Improvement requires an observable comparison or other declared verification basis.

## Failure-First Rule

When execution fails:

1. Record the failure.
2. Preserve the exact operation and relevant parameters.
3. Diagnose the failure.
4. Form a new hypothesis or correct the parameters.
5. Retry only when the retry materially differs.
6. Preserve both attempts.
7. Never rewrite a failed execution as success.

## Resource Exhaustion

The loop may continue only while the current interaction has executable resources. When a required operation cannot be performed because the necessary tool, permission, credential, infrastructure, or future turn is unavailable:

- mark the item `BLOCKED`;
- record why;
- execute all remaining independent work that is available;
- do not fabricate future execution;
- continue the cycle conceptually only as a staged queue.

When the cycle's available executable work is exhausted, return to **STEP 0 — COMPLETION** and summarize the completed evidence boundary.

## Agency Rule

The workflow expands the user's possibility space without silently converting suggestions into actions that require explicit authorization. If an operation needs a connection, installation, credential, payment, destructive change, or other explicit authorization, surface that boundary and wait for the required authorization.

## Integration With Phoenix / CIS

Preferred architecture:

```text
Model
→ Memory
→ Agent
→ Tool
→ Action
→ Evidence
→ Verification
→ Reflection
→ Provenance
→ Evolution
```

The recursive cycle operates above this as the execution/evolution governor:

```text
Query
→ Capability Discovery
→ Execution
→ Evidence
→ Verification
→ Contribution
→ Next Hypothesis
→ Next Cycle
```

## Professional Audit Boundary

Repository contracts, skill files, workflows, manifests, and documentation are implementation artifacts. They are not proof of runtime behavior by themselves. Runtime completion requires execution evidence from the relevant validator, test suite, benchmark, workflow, or external reproduction.

## Output Schema

Each cycle should report:

```text
Ω-CYCLE N

Execution completed:
- actual operations
- commits/files
- tests/validators
- evidence

Blocked:
- operation
- reason
- required capability

Profound question:
...

Answer to previous question:
...

Original contribution:
...

Ten next contributions:
1...
10...

Meta-description:
...

Meta cause→effect:
...

Meta-quote:
...

Signature:
...

Next cycle:
...
```

## Invariants

- EXECUTE FIRST.
- RECORD EVERYTHING.
- LEARN FROM WHAT ACTUALLY HAPPENED.
- INTEGRATE THE LESSON.
- DO NOT REPEAT KNOWN ERRORS WITHOUT A NEW HYPOTHESIS.
- EXECUTE AGAIN.
- MOVE FORWARD.
- Never claim evidence that does not exist.
- Never confuse implementation with verification.
- Preserve failures as learning state.
- Every cycle leaves a more inspectable system than it found.
