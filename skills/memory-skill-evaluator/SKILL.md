---
name: conzetian-memory-skill-evaluator
version: 1.0.0
purpose: Evaluate candidate memory and skill systems before adoption, based on evidence and security.
---

# Conzetian Memory and Skill Evaluator

## Candidate intake
Record canonical repository, commit/release, current license and obligations, maintenance signals, dependency surface, architecture, data flows, persistence model, and deployment model. Re-check license and dependencies before adoption.

## Mandatory gates
- Data ownership, export, deletion, retention, backup/restore.
- Provenance, source attribution, timestamps, digests, and confidence.
- Access control and tenant isolation.
- Secrets handling and prompt-injection resistance for retrieved content.
- Offline/local operation and network egress.
- Dependency and supply-chain risk.
- Reproducible installation, rollback, migration, and failure recovery.
- Interface compatibility and resource constraints.

## Benchmark
Use the same fixed corpus and tasks for every candidate. Measure retrieval precision/recall, source fidelity, update/delete correctness, latency, memory/CPU/disk use, ingestion failures, and adversarial retrieval behavior. Publish corpus version, commands, raw results, and limitations. Do not claim superiority without results.

## Candidate handling
Previously noted candidates include MCP Memory Service, Cognee, Vercel Skills CLI, Agent Skills specification, BrowserOS, and OpenClaw Agent Skills. This is a research queue, not an endorsement. Confirm current license, repository state, and security posture before use. Do not install a candidate merely because its README sounds promising.

## Recommendation
Score only after mandatory gates and benchmarks. Separate facts, inferred tradeoffs, missing evidence, and recommendations.