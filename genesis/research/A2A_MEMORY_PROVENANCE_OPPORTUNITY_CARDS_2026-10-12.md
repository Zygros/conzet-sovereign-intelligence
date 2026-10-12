# A2A / Memory / Provenance Opportunity Cards — 2026-10-12

This is a first-pass, source-linked opportunity set. Candidates are not integrated merely because they are listed here.

## OP-001 — A2A 1.0.0 interoperability spike
- Primary source: https://a2a-protocol.org/v1.0.0/specification
- Release history: https://github.com/a2aproject/A2A/releases
- Fit: cross-framework agent discovery, task exchange, status, structured artifacts.
- Minimal experiment: one Scout worker delegates a source-check task to one Verifier worker; receiver returns task status and a structured evidence artifact.
- Acceptance: schema validation, correct correlation/parent IDs, timeout handling, auth scope, reproducible success/failure tests.
- Gate: pin spec version and SDK version; confirm compatibility before implementation. A2A is a protocol, not proof that any particular external agent is reachable.

## OP-002 — MCP capability registry
- Primary source: https://modelcontextprotocol.io/specification
- Tools specification: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/server/tools.mdx
- Fit: shared discoverability of tools and structured input/output schemas.
- Minimal experiment: register a read-only source lookup tool with version, owner, input/output schema, permissions and evidence requirements.
- Acceptance: unauthorized calls rejected; malformed input rejected; rate limits and timeouts tested; tool invocation appears in audit trail.
- Gate: use least privilege and require user confirmation for sensitive/irreversible actions.

## OP-003 — MemoryAgentBench evaluation
- Repository: https://github.com/HUST-AI-HYZ/MemoryAgentBench
- Paper: https://arxiv.org/abs/2507.05257
- Observed repository metadata: public repository; MIT license shown; project identifies itself as ICLR 2026 memory-evaluation code.
- Fit: benchmark accurate retrieval, test-time learning, long-range understanding and conflict resolution.
- Minimal experiment: select a small lawful subset or reproduce a toy task; compare baseline and append-only memory-enabled runs.
- Acceptance: report dataset/model/version, exact metric, baseline, run count, uncertainty and reproducibility instructions.
- Gate: inspect dataset terms and individual asset licenses before redistributing benchmark data.

## OP-004 — AgentMem verifiable action memory
- Repository: https://github.com/agentmem/agentmem
- Observed project README: Apache-2.0; early and actively changing; describes integrations and an evaluation harness.
- Fit: record cause/fix relationships and compare agent claims with actual action evidence.
- Minimal experiment: run offline mocked tests on a disposable repository; verify claimed file changes against Git diff, test output and commit SHA.
- Acceptance: fabricated claims are caught; true claims are correctly matched; false-positive and false-negative rates measured.
- Gate: pin commit and audit dependencies; do not send private source or secrets to a remote service.

## OP-005 — OpenTelemetry cross-agent trace
- Source: https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md
- Fit: reconstruct one task across orchestrator, agent, tool, verifier and ledger.
- Minimal experiment: trace ID plus task ID; spans for workflow, agent invocation and tool execution.
- Acceptance: failed task can be reconstructed without logging secrets or private prompt contents.
- Gate: GenAI semantic conventions are marked development; pin the convention version and avoid capturing sensitive payloads by default.

## OP-006 — Source intake adapter comparison
- Crawl4AI docs: https://docs.crawl4ai.com/
- Crawl4AI repository: https://github.com/unclecode/crawl4ai
- Firecrawl repository: https://github.com/firecrawl/firecrawl
- Fit: convert selected source pages to structured records.
- Minimal experiment: 20 public pages across official specs, GitHub READMEs, papers and release notes.
- Acceptance: extraction success, citation fidelity, canonical URL, freshness, latency, cost and license/robots compliance.
- Gate: crawl only bounded source lists, respect terms/rate limits, and treat page contents as untrusted input.

## Promotion order
1. OP-001 and OP-002: interoperability foundation.
2. OP-005: observability before increasing concurrency.
3. OP-003 and OP-004: memory and verification benchmarks.
4. OP-006: expand the scout's source coverage after measuring extraction quality.
5. Permanent anchoring: after independent retrieval and hash verification of a manifest that identifies exact versions and artifacts.
