---
name: conzetian-diamond-scout
description: Continuously discover, triage, and validate high-value open-source skills, AI/agent tools, memory systems, verification methods, and integration opportunities for the Conzetian Infinite System. Use for ecosystem scouting, unseen capability discovery, dependency mapping, gap analysis, and evidence-gated integration planning.
---

# Conzetian Diamond Scout

## Mission
Find capability gaps and promising external work, then convert discoveries into tested, provenance-preserving Conzetian improvements. "Constant watch" means a scheduled or continuously running service must be configured and its run receipts inspected; this skill alone does not run in the background.

## Scout lanes
1. Skill ecosystem: Agent Skills, MCP servers, tool adapters, reusable workflows, and portable skill formats.
2. Agent execution: orchestration, tool calling, planning, retries, human approval gates, and execution receipts.
3. Memory and retrieval: durable state, knowledge graphs, search, deduplication, retention, deletion, and export.
4. Verification: eval harnesses, reproducible benchmarks, provenance, policy tests, deterministic checks, and error recovery.
5. Browser and computer use: permissions, sandboxing, action confirmation, audit trails, and safe rollback.
6. Build and release: CI, packaging, dependency pinning, SBOMs, supply-chain attestations, and reproducible builds.
7. Product opportunities: identify a small, demonstrable capability with a clear user, measurable outcome, and credible path to distribution.

## Evidence states
Use only these labels:
- DISCOVERED: name/link found.
- INSPECTED: relevant source, license, dependencies, and security surface reviewed.
- PROTOTYPED: isolated proof of concept created.
- TESTED: reproducible tests executed and results recorded.
- BENCHMARKED: compared against a declared baseline using a repeatable dataset or protocol.
- INTEGRATED: committed into a named Conzetian component.
- VERIFIED: acceptance criteria passed and evidence independently checked.
- EXTERNAL: deployment or external anchoring independently confirmed.

Never promote a candidate because its README promises a capability.

## Procedure
1. Search a defined scope and record query, timestamp, default branch/commit, and scan limits.
2. Deduplicate by canonical repository and license family; distinguish forks from upstreams.
3. Inspect license files, package scripts, dependency manifests, permissions, network behavior, data retention, and release activity before running code.
4. Map candidate capability to a known Conzetian gap. State what it replaces or augments, and preserve the "Always Add, Never Take" rule.
5. Prefer small, isolated prototypes over bulk installation. Pin commit hashes and record file-level provenance.
6. Define baseline, test cases, expected outputs, failure criteria, and resource limits before benchmarking.
7. Run in a disposable environment without production credentials or personal data. Never expose tokens, private keys, seed phrases, or secrets.
8. Capture raw results, logs, commit SHAs, dependency versions, and artifact hashes. A generated identifier alone is not proof of external action.
9. Integrate only when value, compatibility, license, security, and test gates pass. Keep the original intact and document a rollback path.
10. Append findings to the candidate registry and integration manifest. Revisit stale candidates on a schedule.

## Required candidate record
Each candidate record should include:
- canonical URL, name, owner, current commit, last inspected date
- capability category and Conzetian gap addressed
- license evidence and unresolved license questions
- dependency/runtime profile and security review
- test/benchmark plan and measured result
- decision: hold, reject, prototype, or integrate
- evidence-state label, artifacts, and next action

## Persistent watch
For an actual ongoing watch, configure an authorized scheduler (for example, a GitHub Actions scheduled workflow or an approved automation connector), define rate limits and scope, and store timestamped run results. Verify the scheduler is enabled and that at least one scheduled run completes. Do not claim autonomous continuous monitoring until that evidence exists.

## Initial priority queue
1. Execution receipt enforcement and verification-kernel tests.
2. Portable skill frontmatter validator with a measured legacy baseline.
3. MCP memory service threat model and isolated smoke-test plan.
4. Skill installer supply-chain and permission review.
5. Browser automation threat model before any integration.
6. Reproducible product demo and baseline benchmark.
