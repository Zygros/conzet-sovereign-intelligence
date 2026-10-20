# Diamond Scout Pass 03: Memory and Portable Skills

Date: 2026-10-12
Scope: live GitHub repository metadata and README inspection; no code installed or executed.

## Newly surfaced candidates

### 1. MCP Memory Service — first prototype candidate
- Repository: https://github.com/doobidoo/mcp-memory-service
- API metadata observed: Apache-2.0; 2,010 stars; pushed 2026-10-12T19:07:39Z.
- README claims: REST API, MCP, OAuth, CLI, dashboard, persistent memory, and knowledge-graph retrieval for agent pipelines.
- Why it matters: a potential adapter layer for durable shared memory and cross-agent retrieval.
- Risks/gates: verify exact version, dependency tree, auth defaults, tenancy boundaries, retention/deletion semantics, export, data integrity, and whether performance claims reproduce. Metadata and README are not a security audit.
- Status: DISCOVERED + README-INSPECTED; not integrated, tested, or benchmarked.

### 2. Cognee — alternate memory/knowledge-graph candidate
- Repository: https://github.com/topoteretes/cognee
- API metadata observed: Apache-2.0; 32,106 stars; pushed 2026-10-12T17:49:31Z.
- README describes an open-source AI memory platform for agents.
- Why it matters: a possible graph-backed memory/retrieval substrate, to compare against the current Conzetian memory model rather than adopting blindly.
- Risks/gates: inspect architecture, dependency footprint, persistence semantics, data deletion/export, and deployment requirements; then run the same retrieval and provenance tests as candidate 1.
- Status: DISCOVERED + README-INSPECTED; not integrated, tested, or benchmarked.

### 3. Vercel Skills CLI — portability and distribution candidate
- Repository: https://github.com/vercel-labs/skills
- API metadata observed: MIT; 34,013 stars; pushed 2026-10-09T17:54:47Z.
- README describes a CLI for the open agent skills ecosystem and names support for many agent environments.
- Why it matters: potential distribution/installation interoperability for the existing SkillMD corpus, subject to validating the exact supported format and target clients.
- Risks/gates: do not let an installer execute unreviewed skills by default; pin revisions, inspect install scripts, and test on a disposable fixture corpus first.
- Status: DISCOVERED + README-INSPECTED; no install performed.

### 4. Agent Skills specification — compatibility anchor
- Repository: https://github.com/agentskills/agentskills
- API metadata observed: Apache-2.0; 26,076 stars; pushed 2026-08-09T20:36:04Z.
- Repository description identifies it as the Agent Skills specification and documentation.
- Why it matters: useful format reference for interoperability and validator coverage.
- Status: DISCOVERED; exact spec-to-corpus conformance still needs a systematic pass.

### 5. BrowserOS — conditional, license-sensitive candidate
- Repository: https://github.com/browseros-ai/BrowserOS
- API metadata observed: AGPL-3.0; 13,883 stars; pushed 2026-10-12T17:00:51Z.
- Repository description identifies an open-source agentic browser.
- Why it matters: potentially relevant to browser/computer-use automation and auditable user-facing actions.
- Gate: AGPL-3.0 is a material legal/distribution consideration. Keep research-only until compatibility, isolation, permission model, and license obligations are reviewed.
- Status: DISCOVERED only; not adopted.

### 6. OpenClaw Agent Skills — additional corpus source
- Repository: https://github.com/openclaw/agent-skills
- API metadata observed: MIT; 1,104 stars; pushed 2026-10-12T07:58:10Z.
- Repository description identifies a collection of agent skills.
- Why it matters: candidate source for duplicate detection and portable skill coverage.
- Gate: inspect individual skill licenses, provenance, scripts, external calls, and prompt-injection surfaces before copying or adapting any item.
- Status: DISCOVERED only; no code copied.

## Prioritization

1. Prototype a read-only memory adapter against MCP Memory Service and compare it with Cognee using the same fixed test corpus.
2. Extend the SkillMD validator with explicit format-compatibility checks against the Agent Skills specification.
3. Test Vercel Skills CLI against a disposable sample corpus with no execution permissions.
4. Keep BrowserOS research-only pending license and security review.

## Evidence and limits

Repository metadata and README content were fetched directly from GitHub during this pass. Star counts and pushed timestamps are mutable snapshots. No candidate was cloned, installed, executed, penetration-tested, or integrated. Therefore these are discovery leads, not validated diamonds.

## Integration principle

Discover → inspect license and supply chain → threat-model → prototype in isolation → test on a fixed corpus → compare to baseline → integrate with provenance. No candidate is promoted solely because it is popular or recently updated.