# Diamonds and A2A Intake Checkpoint
Date: 2026-10-12 Pacific / 2026-10-13 UTC

## Observed intake
Scout run [38329245120](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38329245120) artifact contains 97 discovery records, 93 review receipts, and 4 rejected records. All 93 receipts are pending independent review. Their A2A-shaped envelopes specify sender `opportunity-scout`, recipient `evidence-verifier`, task `review_discovery_candidate`, permissions `source:read` and `evidence:write`, sensitive-action confirmation enabled, and candidate execution disabled.

This establishes structured message-envelope generation and receipt persistence, not live model-to-model delivery or completed external review. The next A2A proof should be a mock round trip: send task, receive acknowledgement, return structured review, validate schema/evidence, and append the receipt.

## High-value candidates to inspect
These are research leads, not verified or integrated components:
1. [Vercel Skills CLI](https://github.com/vercel-labs/skills), MIT metadata: skill discovery/import/export compatibility.
2. [Agent Skills specification](https://github.com/agentskills/agentskills), Apache-2.0 metadata: portable SKILL.md conventions.
3. [MCP Memory Service](https://github.com/doobidoo/mcp-memory-service), Apache-2.0 metadata: persistent memory/retrieval.
4. [Cognee](https://github.com/topoteretes/cognee), Apache-2.0 metadata: graph and multi-hop retrieval.
5. [Firecrawl](https://github.com/firecrawl/firecrawl), AGPL-3.0 metadata: web ingestion; review license obligations before adoption.
6. [Crawl4AI](https://github.com/unclecode/crawl4ai), Apache-2.0 metadata: crawler/extraction alternative.
7. [A2A wrapper](https://github.com/shashikanth-gs/a2a-wrapper), MIT metadata: potential backend-to-agent adapter.
8. [Verifiable Agent Trust Envelope](https://github.com/Poke-nushi/Verifiable-Agent-Trust-Envelope), Apache-2.0 metadata: permission and receipt design lead.
9. [agent-stack](https://github.com/ssheleg/agent-stack), MIT metadata: orchestration/evals/routing patterns.
10. [Nautilus Compass](https://github.com/chunxiaoxx/nautilus-compass), NOASSERTION metadata: memory/verification lead; license must be resolved.

License values are discovery-time metadata, not legal clearance. The candidates have not been installed, benchmarked, or security-cleared.

## Scout coverage
The 97 records cover A2A/MCP, agent memory and verification, web crawling, observability, evaluation/benchmarks, scientific reproducibility, privacy/security, decentralized compute, red-team evaluation, and dual-use governance. Treat them as unreviewed leads, not vetted diamonds.

## Diamond Watch count check
The workflow receipt reports 7 repositories checked and 0 metadata fetch errors. The downloaded report contains seven candidate names: agentskills/agentskills, vercel-labs/skills, avvertix/skillsmd, openclaw/agent-skills, doobidoo/mcp-memory-service, topoteretes/cognee, and browseros-ai/BrowserOS. Assert the report's declared count against the actual results-array length in future runs.

## Next gates
1. Add automated count consistency checks to both discovery reports.
2. Review pinned source, dependencies, installation behavior, network access, telemetry, authentication, data persistence/export/delete, and licenses.
3. Run MCP Memory Service and Cognee in isolated disposable environments against the same 30-record/20-query synthetic benchmark.
4. Test skill import/export against a disposable corpus without auto-executing imported skills.
5. Inspect A2A wrapper and trust-envelope candidates; perform a bounded mock round trip before using external model providers.
6. Preserve raw outputs and hashes; promote only after acceptance tests and independent reproduction.

## Evidence labels
VERIFIED: Scout artifact has 97 records, 93 receipts, and 4 rejected records; all 93 receipts remain pending review. Diamond Watch published an artifact successfully.
NOT VERIFIED: candidate safety, comparative performance, live A2A delivery, external model responses, or integration.
