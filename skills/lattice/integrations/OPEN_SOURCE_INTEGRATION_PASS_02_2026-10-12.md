# Open-Source Integration Pass 02: Diamonds-to-Capabilities Register
**Date:** 2026-10-12  
**Principle:** Always Add, Never Take. Discovery is not integration; README claims are not test results.

## What changed
This pass adds a machine-readable candidate register and a portable skill compatibility contract. These are committed as additive files in the Conzetian skill lattice. No external code was copied into the system.

## High-value findings and decisions

| Candidate | Capability opportunity | Decision now | Why |
|---|---|---|---|
| [Agent Skills format](https://github.com/agentskills/agentskills) | Portable `SKILL.md` packaging across compatible agents | Adopt the specification as compatibility target | Lightweight format; preserve Conzetian extensions separately |
| [Vercel Skills CLI](https://github.com/vercel-labs/skills) | Discovery/install across many agent clients | Isolated prototype candidate | Useful intake adapter; installation and supply-chain risks require gates |
| [skillsmd](https://github.com/avvertix/skillsmd) | Python-based skill workflow | Isolated prototype candidate | Potentially convenient for Termux/Python; source/tests still need audit |
| [OpenClaw Agent Skills](https://github.com/openclaw/agent-skills) | Behavior validation, review closeout, provenance, handoff | Selective skill-by-skill review | MIT is stated in README; scripts and session-data handling need per-skill review |
| [MCP Memory Service](https://github.com/doobidoo/mcp-memory-service) | Shared memory over REST/MCP | Prototype candidate after threat-model review | README states Apache-2.0; inspect auth, retention, storage, tests |
| [Cognee](https://github.com/topoteretes/cognee) | Knowledge-graph memory and retrieval | Hold pending license/runtime inspection | Promising capability, but license and data lifecycle not verified in this pass |
| [BrowserOS](https://github.com/browseros-ai/BrowserOS) | Browser-native agent action | Hold pending license/threat-model review | README states AGPL-3.0; privileged browser integration warrants scrutiny |

## Integration architecture
```text
GitHub / Skills.sh / MCP / Model & Dataset Hubs
                    |
                    v
         DISCOVERY ADAPTERS (read-only)
                    |
                    v
    Candidate Registry + Exact Source Version
                    |
                    v
      License + Security + Capability Review
                    |
                    v
       Isolated Prototype / No Production Secrets
                    |
                    v
     Baseline + Held-out Tests + Failure Injection
                    |
                    v
       Additive Adapter / Skill Integration
                    |
                    v
    Provenance Ledger + CI + Rollback Reference
```

## Immediate work order
1. Add format validation for `SKILL.md` metadata and safe relative references.
2. Compare Vercel Skills CLI and skillsmd against the existing read-only repository tree scan.
3. Select three OpenClaw skills, review each script and license, then run held-out behavior tests.
4. Inspect MCP Memory Service and Cognee data stores, auth, export/deletion, and reproducible tests.
5. Keep BrowserOS at HOLD until AGPL implications and browser privilege boundaries are resolved.
6. Promote candidates only when an explicit baseline is beaten and the evidence is committed.

## Evidence discipline
- README-level details are labeled as such.
- No external dependency was installed or run during this pass.
- No external code was copied into the lattice.
- No candidate is labeled TESTED, INTEGRATED, or VERIFIED without reproducible implementation evidence.
- Search results were not treated as authoritative license or quality signals.

## Artifacts
- Portable compatibility skill: `skills/portable-agent-skill-compatibility/SKILL.md`
- Machine-readable candidate register: `integrations/open_source_candidate_registry_2026-10-12.json`
- Prior ecosystem scout: `integrations/GITHUB_ECOSYSTEM_SCOUT_2026-10-12.md`
