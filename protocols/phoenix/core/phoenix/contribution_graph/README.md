# PHOENIX Contribution Graph v0.1

## Purpose

Turn every Phoenix contribution into a cross-connected, provenance-bearing, action-oriented node rather than a passive numbered list.

## Core model

```text
Contribution
  -> relation
  -> trigger
  -> action
  -> evidence
  -> next state
```

A contribution may `extend`, `depend_on`, `test`, `contradict`, `compose_with`, `resonate_with`, `verify`, `revise`, or `generate` another contribution.

## Contribution contract

```yaml
id: C-###
name: string
question: string
answer: string
claim: string
action: string
triggers: []
activates: []
depends_on: []
extends: []
tests: []
contradicts: []
composes_with: []
resonates_with: []
provenance: []
evidence: []
verification_state: hypothesis|designed|executed|reproduced|verified
capability_delta: string
next_question: string
```

## Graph invariant

`G_C = (C, E_T)` where `E_T` is a typed edge set.

`G(t+1) = G(t) ∪ ΔG`

No contribution is deleted to revise it. A revision creates a new state linked by `revised_by`, preserving lineage.

## Action invariant

A contribution is actionable only when it defines a trigger and an observable action. Narrative claims remain hypotheses until evidence moves them through the verification states.

## Provenance invariant

Every node records where it came from and what it enabled. Reverse traversal must be possible: descendants can identify ancestors, and ancestors can identify descendants.

## Cross-connection seed set

The initial seed graph covers Contributions C127-C166, including Model-Failure Intelligence, Recursive Self-Model, Dyadic State Object, Temporal Truth Object, Substrate Drift Engine, Ontology Black Swan, Question Compiler, Process Identity, Frontier Delta Engine, Learning-from-the-Other, Contribution Graph, Contribution-as-Action, Contribution Trigger, Contribution Reciprocity, Contribution Closure, Contribution Lineage, Contribution Composition, Contribution Mutation, Contribution Verification, Contribution Contradiction, Contribution Gravity, Contribution Resonance, Contribution Black Swan Edge, and Contribution Evolution Engine.

## Design boundary

This repository artifact defines and records the architecture. A contribution is not claimed as independently verified merely because it is represented in this graph. Execution, reproduction, and verification must be recorded separately.
