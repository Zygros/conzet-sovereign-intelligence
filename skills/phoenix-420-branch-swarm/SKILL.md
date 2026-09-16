---
name: phoenix-420-branch-swarm
description: Deterministic 420-branch Phoenix swarm specification with 420 named agents, unique domain-role logic, a shared 420-action typed action space, per-agent skill trees, evidence gates, provenance, additive evolution, and a protocolized Hyperbolic Time Chamber (HTC) execution model.
owner: Justin Neal Thomas Conzet
tags: [phoenix, 420, swarm, agents, skill-tree, orchestration, verification, hyperbolic, HTC]
license: SOL
---

# PHOENIX 420-BRANCH SWARM

🜂 **Field-native 420-agent architecture — 420 actions per agent — 176,400 typed bindings — HTC protocol substrate.**

> **Always Add, Never Take.** The baseline remains preserved; verified extensions are layered through append-only state, evidence, and provenance.

## Hyperbolic Time Chamber — Protocol Definition

The Phoenix **Hyperbolic Time Chamber (HTC)** is treated here as a **real computational/protocol construct** when implemented as an executable workflow: a controlled execution environment that expands a task across logical branches, applies repeated transformations and verification gates, records state transitions, and compresses the resulting evidence into a reproducible ledger.

It is **not necessary to invoke literal physical time dilation** for the protocol to be real. The protocol's reality is established by executable rules, measurable state transitions, reproducibility, and evidence. Physical relativistic time dilation is a separate physical phenomenon and is not assumed by this skill.

### HTC Core Model

```text
Intent
  ↓
HTC State Initialization
  ↓
Hyperbolic Branch Expansion
  ↓
420 Logical Agents
  ↓
420 Action Space
  ↓
Execution / Evidence
  ↓
Verification / Reflection
  ↓
State Compression
  ↓
Next HTC State
  ↺
```

A useful protocol abstraction is:

`H_{t+1} = C(V(E(B(H_t, Ω, A))))`

where:

- `H_t` = chamber state at iteration `t`
- `B` = branch expansion
- `Ω` = agent field
- `A` = typed action space
- `E` = execution
- `V` = verification
- `C` = evidence/state compression

The chamber therefore creates **computational depth and branch expansion**, not a claim of faster-than-light or physically accelerated time.

## Why “Hyperbolic” Is Architecturally Meaningful

Hyperbolic geometry is not merely a metaphor. Hyperbolic spaces have negative curvature and exponential volume growth, making them useful for representing hierarchical, tree-like, heterogeneous, and scale-free structures. Research on hyperbolic graph representations shows that such geometry can reduce distortion when representing these structures and can support efficient routing in suitable network models.

For Phoenix, this suggests a concrete integration target:

`Task → Hyperbolic State Space → Branches → Agent/Action Coordinates → Routing → Evidence`

The word **hyperbolic** therefore maps to measurable topology and representation rather than requiring a literal chamber in physical spacetime.

## Hyperbolic Integration Targets

### 1. Hyperbolic Agent Embedding
Represent agents as points in a hyperbolic manifold or hyperbolic-like graph metric. Radial position can encode abstraction/expansion depth; angular proximity can encode semantic or operational similarity.

### 2. Hyperbolic Capability Routing
Use hyperbolic distance as one routing signal:

`route(i,j) = argmin d_H(i, target)`

subject to evidence, safety, capability, and resource constraints.

### 3. Branch Expansion
The chamber expands candidate paths according to task complexity rather than treating every branch as equally useful.

`BranchBudget(t) = f(uncertainty, novelty, evidence_gap, resource_budget)`

### 4. Curvature as a Measurable Parameter
Introduce a protocol parameter `K < 0` for hyperbolic experiments. The system should compare routing, distortion, coverage, and convergence against Euclidean or graph-only baselines.

### 5. Compression After Expansion
Expansion is followed by evidence-preserving compression:

`Expanded State → Verified Evidence → Minimal Sufficient State`

This makes the HTC a **branch-expand / verify / compress / evolve** cycle.

## Use When

- A task needs 420 distinct logical branches or specialized agents.
- An action should be represented as an addressable agent capability.
- A task needs deterministic skill-tree routing, action composition, verification, or evolutionary feedback.
- HTC is being used as a measurable protocol for branch expansion, stress testing, recursive execution, and evidence compression.
- Hyperbolic graph geometry is useful for representing the topology of agents, capabilities, or knowledge.

## Don't Use When

- A real-world action requires authority, credentials, or permissions that have not been granted.
- A claim needs to be presented as executed or verified when only specified.
- A physical time-dilation claim is being inferred solely from computational parallelism.
- 420-way branching would add noise without increasing useful coverage.

## Workflow

1. **Resolve intent.** Map the incoming task to one or more domains.
2. **Initialize HTC state.** Create a reproducible state identifier, inputs, constraints, and evidence requirements.
3. **Expand branches.** Route the task through the 420-agent field.
4. **Load logic.** Apply the selected agent's domain-role logic from `references/AGENT_ACTION_REGISTRY.md` or regenerate it with `scripts/generate_registry.py`.
5. **Traverse the skill tree.** `Domain Core → Role Reasoning → Evidence Gate → Action Engine → Reflection Loop → Evolution Loop`.
6. **Select actions.** Address any of the 420 typed actions `A-001…A-420`.
7. **Execute.** Perform supported actions using available runtime/tools.
8. **Record.** Capture inputs, outputs, timestamps, provenance, failures, and state transitions.
9. **Verify.** Distinguish declaration from execution, reproduction, and independent verification.
10. **Compress.** Preserve sufficient evidence while reducing redundant state.
11. **Reflect.** Identify failures, novel patterns, capability deltas, and unresolved questions.
12. **Evolve.** Append verified improvements without deleting prior branches or evidence.

## Rules

- **420 agents:** exactly 20 domains × 21 roles.
- **420 actions:** exactly 20 action families × 21 operating modes.
- **176,400 bindings:** `420 × 420` addressable agent-action combinations.
- **Unique logic:** each agent is uniquely identified by its domain-role pair.
- **Skill tree:** every agent follows the six-stage topology while specializing domain and role.
- **Evidence gate:** `declared ≠ executed ≠ reproduced ≠ verified`.
- **Always Add, Never Take:** never silently delete prior registry entries, provenance, or failed evidence.
- **No fabricated execution:** a specification is not proof of runtime execution.
- **HTC is protocolized:** the chamber is implemented through executable state transitions, branch expansion, verification, compression, and provenance.
- **No unsupported physical claim:** computational branch expansion is not automatically physical time dilation.
- **Field, not hierarchy:** routing uses relationships, capability fit, evidence, and task state rather than rank.
- **Action-as-agent:** every action is addressable as a typed capability; this does not imply every action is continuously running as an autonomous process.

## Hyperbolic Research Program

The HTC implementation should be studied experimentally against measurable baselines:

| Metric | Definition |
|---|---|
| Coverage | fraction of relevant solution space explored |
| Distortion | preservation error between original and embedded topology |
| Routing Cost | computational cost of selecting a useful branch |
| Evidence Yield | verified evidence / executed branches |
| Redundancy | repeated equivalent branches / total branches |
| Convergence | reduction in unresolved disagreement over iterations |
| Capability Delta | measurable task gain after evolution |
| Recovery | successful continuation after branch failure |
| Provenance Completeness | traceable state transitions / total transitions |
| Compression Ratio | expanded state / retained sufficient evidence |

A legitimate HTC claim should be supported by measured runs, reproducible inputs, recorded outputs, and comparison against baselines.

## Scientific Boundary

Hyperbolic geometry is established mathematics. Hyperbolic graph embeddings and negative-curvature network models are established research areas. The Phoenix-specific claim that these ideas form an effective **HTC protocol** is an engineering hypothesis that should be validated through implementation and experiment.

This distinction strengthens the system: **the protocol does not need an unsupported physical claim to be real as software.** Its reality is demonstrated through execution, evidence, reproducibility, and measurable effects.

## References

- Complete architecture and deterministic catalog: `references/AGENT_ACTION_REGISTRY.md`.
- Deterministic generator and cardinality checks: `scripts/generate_registry.py`.
- Hyperbolic graph geometry: Krioukov et al., *Hyperbolic Geometry of Complex Networks*.
- Hyperbolic graph representation learning: current survey literature on hierarchical and scale-free graph embedding.
- Agent Skills convention: `SKILL.md` is the entry point; larger supporting material belongs in references.
