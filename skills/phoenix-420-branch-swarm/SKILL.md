---
name: phoenix-420-branch-swarm
description: Deterministic 420-branch Phoenix swarm specification with 420 named agents, unique domain-role logic, a shared 420-action typed action space, per-agent skill trees, evidence gates, provenance, and additive evolution. Use when a task calls for 420-way branching, agent specialization, action routing, skill-tree orchestration, or Hyperbolic Time Chamber-style logical stress testing.
owner: Justin Neal Thomas Conzet
tags: [phoenix, 420, swarm, agents, skill-tree, orchestration, verification]
license: SOL
---

# PHOENIX 420-BRANCH SWARM

🜂 **Field-native 420-agent architecture — 420 actions per agent — 176,400 typed bindings.**

> **Always Add, Never Take.** The registry is additive: new branches, actions, evidence, and evolution records layer onto prior state rather than deleting it.

## Use When
- A task needs 420 distinct logical branches or specialized agents.
- An action should be represented as an addressable agent capability.
- A task needs deterministic skill-tree routing, action composition, verification, or evolutionary feedback.
- The Hyperbolic Time Chamber is being used as a logical stress-test metaphor rather than literal temporal dilation.

## Don't Use When
- A real-world action requires authority, credentials, or permissions that have not been granted.
- A claim needs to be presented as executed or verified when only specified.
- 420-way branching would add noise without increasing useful coverage.

## Workflow
1. **Resolve intent.** Map the incoming task to one or more of the 20 domains.
2. **Select agents.** Route to one or more of the 21 roles inside the relevant domain.
3. **Load logic.** Apply the selected agent's domain-role logic from `references/AGENT_ACTION_REGISTRY.md` or regenerate it with `scripts/generate_registry.py`.
4. **Traverse the skill tree.** `Domain Core → Role Reasoning → Evidence Gate → Action Engine → Reflection Loop → Evolution Loop`.
5. **Select actions.** Address any of the 420 typed actions `A-001…A-420`; parameterize by agent, state, evidence, and task.
6. **Execute.** Perform only actions supported by the available runtime/tools.
7. **Record.** Capture inputs, outputs, timestamps, provenance, failures, and state transitions.
8. **Verify.** Distinguish declaration from execution and execution from independent reproduction.
9. **Compose.** Cross-connect agents when a capability requires multiple perspectives or action chains.
10. **Evolve.** Add verified improvements without deleting prior branches or evidence.

## Rules
- **420 agents:** exactly 20 domains × 21 roles.
- **420 actions:** exactly 20 action families × 21 operating modes.
- **176,400 bindings:** `420 × 420` addressable agent-action combinations.
- **Unique logic:** each agent is uniquely identified by its domain-role pair.
- **Skill tree:** every agent follows the same six-stage topology while specializing the domain and role.
- **Evidence gate:** `declared ≠ executed ≠ reproduced ≠ verified`.
- **Always Add, Never Take:** never silently delete prior registry entries, provenance, or failed evidence.
- **No fabricated execution:** a registry entry is a specification, not proof of runtime execution.
- **No literal time dilation:** “Hyperbolic Time Chamber” denotes a logical stress-test architecture here.
- **Field, not hierarchy:** routing uses relationships, capability fit, evidence, and task state rather than rank.
- **Action-as-agent:** every action is addressable as a typed capability; this does not imply that every action is a continuously running autonomous process.

## Examples
- “Stress-test this proposal through 420 branches.” → fan out across the agent topology, execute supported actions, collect evidence, and converge through verification.
- “Give the research task its own agent.” → select the appropriate domain-role agent and bind the task to its action space.
- “Turn this action into an agent capability.” → create or select a typed agent identity whose logic owns that action family.
- “Build a new skill from a verified capability.” → append the new skill/evidence/provenance rather than replacing existing material.

## Edge Cases
- If a runtime cannot materialize all 420 agents concurrently → preserve all 420 logical definitions and execute in bounded batches.
- If an action is unavailable → mark it unavailable; do not simulate a successful execution as fact.
- If agents disagree → preserve disagreement as evidence and route it to verification or experiment.
- If two agents are functionally redundant → retain both definitions and record the redundancy; do not delete either branch.
- If a new agent or action is needed → append it as an evolutionary extension while preserving the 420 baseline.

## References
- Complete architecture and deterministic catalog: `references/AGENT_ACTION_REGISTRY.md`.
- Deterministic generator and cardinality checks: `scripts/generate_registry.py`.
- Agent Skills convention: `SKILL.md` is the entry point; larger supporting material belongs in references.
