# Sovereign Conzetian Source Anchors & Branching Registry
**Created:** 2026-10-12  
**Purpose:** Establish a versioned source-of-truth map for the global discovery mesh. This is an index and anchoring policy, not a claim that external content has been permanently stored.

## Anchor hierarchy

### Root 0 — Sovereign project identity
- Repository: https://github.com/Zygros/conzet-sovereign-intelligence
- Root branch: `main`
- Current registry commit at creation: `93d4069b48261c2b91dbe65a9345579fdea36681`
- Evidence: commit history, workflow runs, artifact digests, tagged releases, and file hashes.
- Purpose: canonical record of integration code, architecture decisions, verification outcomes, and source manifests.

### Root 1 — Standards and interoperability
1. A2A specification, current released spec: https://a2a-protocol.org/v1.0.0/specification
2. A2A project releases: https://github.com/a2aproject/A2A/releases
3. MCP specification: https://modelcontextprotocol.io/specification
4. MCP tools specification snapshot (2026-07-28): https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/server/tools.mdx
5. OpenTelemetry GenAI agent spans: https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md

Branching:
- A2A → agent discovery cards, task envelopes, task status, artifacts, identity/auth, timeout and failure-recovery tests.
- MCP → capability schemas, server/client adapters, access scopes, input/output validation, rate limits and audit events.
- OpenTelemetry → trace IDs and spans for orchestrator, agent, tool, verifier and ledger events.

### Root 2 — Discovery and web intake
1. Crawl4AI docs: https://docs.crawl4ai.com/
2. Crawl4AI source: https://github.com/unclecode/crawl4ai
3. Firecrawl source: https://github.com/firecrawl/firecrawl
4. GitHub repository search API: https://docs.github.com/en/rest/search/search
5. arXiv API: https://info.arxiv.org/help/api/index.html

Branching:
- Search adapters → canonicalization → deduplication → source record → relevance score → opportunity card.
- Keep provider-specific adapters interchangeable. Respect robots policies, terms, rate limits, API quotas and licenses. Do not treat search rank or stars as evidence of technical validity.

### Root 3 — Memory, evaluation and verification
1. STATE-Bench announcement: https://opensource.microsoft.com/blog/2026/05/19/introducing-state-bench-a-benchmark-for-ai-agent-memory/
2. MemoryAgentBench: https://github.com/HUST-AI-HYZ/MemoryAgentBench
3. AgentMem candidate project: https://github.com/agentmem/agentmem
4. OpenTelemetry GenAI spans: https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md

Branching:
- Memory benchmarks → baseline/augmented comparisons → reproducible tasks → regression records.
- Agent action auditing → claimed-action vs actual-diff comparison → test results → verifier decision.
- Observability → trace-based debugging, latency/cost/error metrics, retry-loop detection.

### Root 4 — Durable storage and decentralized compute
1. Arweave AO documentation: https://ao_docs.ar.io/
2. AO cookbook: https://cookbook_ao.arweave.net/welcome/index.html
3. Arweave documentation: https://docs.arweave.org/

Branching:
- Begin with public, non-sensitive test artifacts.
- Record content hash, storage/transaction ID, timestamp, network, verification method, and retrieval result.
- Never anchor secrets, personal/private data, credentials, or content without rights.
- A hash establishes artifact identity/integrity only relative to the hashed bytes; it does not establish truth of claims within those bytes.

## Source-record schema

Each discovered source should be recorded with:
- `source_id` (stable identifier), `canonical_url`, `title`, `source_type`, `publisher`;
- `retrieved_at`, `published_at` where available, `version_or_commit`, `content_hash` when bytes are lawfully captured;
- `license`, `terms_or_robots_review`, `summary`, `evidence_excerpt` where permitted;
- `parent_source_ids`, `branch_ids`, `candidate_integrations`, `status`, `reviewer`;
- `confidence`, `limitations`, `next_test`, `verification_artifacts`.

## Branching and anchor lifecycle

1. **Discover:** create a candidate record with URL and retrieval timestamp.
2. **Normalize:** resolve canonical URL, stable project identity, version, and duplicate candidates.
3. **Capture:** preserve lawful metadata or a content hash; do not mirror copyrighted material indiscriminately.
4. **Assess:** score relevance, maturity, reproducibility, licensing, security, cost and integration effort.
5. **Branch:** create one or more child opportunity records linked to the parent source.
6. **Prototype:** implement in a sandbox against a narrow acceptance test.
7. **Verify:** have an independent test path check output and record evidence.
8. **Promote:** commit additive integration changes only after gates pass.
9. **Anchor:** publish a signed manifest or external anchor only after independently retrieving and verifying the exact manifest and underlying artifact hashes.
10. **Refresh:** revisit active source roots on a schedule; record changes as new versions rather than overwriting prior evidence.

## Initial cadence
- Every 6 hours: bounded GitHub/arXiv metadata scout.
- Weekly: review root-source changes, releases, security advisories, and broken links.
- On each integration commit: run unit tests, repository CI, security checks, and provenance checks.
- Before production promotion or permanent anchoring: independent review and explicit deployment evidence.

## Non-negotiable distinction
`indexed ≠ downloaded ≠ integrated ≠ verified ≠ deployed ≠ permanently anchored`.

Every state transition requires its own evidence. This registry is the trunk from which the global research and integration branches can grow.


## Root 5 — Open inquiry, contested knowledge and unknowns

- Research charter: https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/genesis/research/OPEN_INQUIRY_AND_UNKNOWNS_RESEARCH_CHARTER_2026-10-12.md
- A2A envelope contract: https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/schemas/a2a-task-envelope.schema.json
- Local envelope validator: https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/scripts/a2a_envelope.py
- Envelope regression tests: https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/tests/test_a2a_envelope.py

Branching:
- Taboo-labelled or controversial claims → source genealogy → historical/context analysis → contradiction search → evidence-quality assessment.
- Dual-use research → public-source discovery → benefit/risk mapping → safe, authorized evaluation → independent verification.
- Unknowns → explicit uncertainty record → minimal discriminating experiment → outcome and negative-result record → new child questions.
- Anomalous or fringe claims → primary-source retrieval → independent corroboration → alternative explanations → reproducibility assessment.

This root expands inquiry; it does not treat a label as proof of danger or proof of truth. Discovery remains metadata-only until a candidate is deliberately reviewed. Public availability alone does not establish permission to execute code, access systems, or reproduce sensitive operational details.
