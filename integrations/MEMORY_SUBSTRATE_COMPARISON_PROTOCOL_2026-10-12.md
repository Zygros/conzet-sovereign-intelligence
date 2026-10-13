# Memory Substrate Comparison Protocol: MCP Memory Service vs Cognee
**Status:** TEST PLAN READY; CANDIDATE EXECUTION NOT YET RUN  
**Purpose:** Select a memory/retrieval substrate for a bounded Conzetian prototype using repeatable evidence rather than popularity or README claims.

## Candidates
- [MCP Memory Service](https://github.com/doobidoo/mcp-memory-service), reported Apache-2.0 in the Diamond Scout metadata snapshot.
- [Cognee](https://github.com/topoteretes/cognee), reported Apache-2.0 in the same snapshot.

The license identifiers are discovery-time metadata, not a substitute for reviewing the exact pinned revision and license files before use.

## Safety boundary
1. Use a disposable, isolated environment with no production credentials, private corpora, or network write permissions.
2. Pin each candidate to a specific commit before testing.
3. Inspect license, dependency manifests, install scripts, default bind addresses, authentication, outbound network calls, telemetry, persistence, and deletion/export behavior before installation.
4. Do not load plugins or skills from either candidate into the live Conzetian runtime.
5. Abort if the test requires unexplained credential access, broad host permissions, or unbounded external execution.
6. Preserve raw inputs, exact commands, environment versions, logs, and output hashes. Append records; do not overwrite prior evidence.

## Fixed synthetic corpus
Create 30 synthetic records across three categories:
- 10 factual records with explicit identifiers and known answers.
- 10 linked records requiring two-hop retrieval.
- 10 distractor/near-duplicate records with conflicting or stale values marked as superseded.

No personal or production data is permitted. Store the corpus and its SHA-256 before either candidate is run.

## Queries and scoring
Prepare 20 fixed queries before testing:
- 8 direct factual retrieval queries.
- 6 two-hop relationship queries.
- 3 near-duplicate/conflict-resolution queries.
- 3 unknown-answer queries where abstention is the correct behavior.

Score:
- Exact-answer accuracy on answerable queries.
- Correct abstention on unanswerable queries.
- Citation/provenance completeness: whether each answer points to the correct source record.
- Cross-run determinism over three repeated runs.
- Latency: median and p95, recorded with hardware/runtime details.
- Resource use: peak memory and storage footprint.
- Data governance: export, deletion, persistence, and tenant-isolation behavior.
- Failure behavior: malformed input, missing dependencies, and unavailable backend.

## Decision gates
**Gate A: Source and trust review.** Record pinned commit, license-file hash, dependencies, install behavior, network surface, and unresolved risks. Do not install before review.

**Gate B: Isolated smoke test.** Install and run one candidate at a time in a disposable environment. Preserve full logs and stop on unexpected network or permission behavior.

**Gate C: Equal-condition benchmark.** Run the same corpus and queries with identical retrieval settings where possible. Document unavoidable differences instead of silently normalizing them away.

**Gate D: Decision.** Integrate only if a candidate materially improves a declared metric without unacceptable provenance, safety, or governance regressions. Otherwise retain the existing architecture and record the rejection.

## Required result table
| Metric | MCP Memory Service | Cognee | Evidence |
|---|---:|---:|---|
| Source/license review | Pending | Pending | Pinned commits + license hashes |
| Direct factual accuracy | Pending | Pending | Raw test output |
| Two-hop accuracy | Pending | Pending | Raw test output |
| Correct abstention | Pending | Pending | Raw test output |
| Provenance completeness | Pending | Pending | Source-record references |
| Determinism across 3 runs | Pending | Pending | Run receipts |
| Median / p95 latency | Pending | Pending | Timestamped measurements |
| Peak memory / storage | Pending | Pending | Environment metrics |
| Export/delete behavior | Pending | Pending | Test receipts |
| Security concerns | Pending | Pending | Review notes |

## Exit criterion
No candidate is promoted beyond DISCOVERED/INSPECTED until its pinned source, license, dependencies, and execution surface have been reviewed. No integration decision is made without raw reproducible benchmark evidence and a preserved decision record.
