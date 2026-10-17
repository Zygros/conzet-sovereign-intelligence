# GitHub Skill Lattice & Open-Source Ecosystem Scout
**Date:** 2026-10-12  
**Scope:** Focused first-pass scan of accessible Zygros repositories and current public GitHub AI/agent/skill projects. This is not a claim to have exhaustively scanned all of GitHub.

## Executive result
The strongest immediate opportunity is to connect the existing Conzetian skill-discovery machinery to a repeatable, evidence-gated external capability intake pipeline, rather than duplicating broad discovery skills already present.

### Existing Conzetian skill inventory
GitHub recursive tree APIs were queried for selected accessible repositories:
- `Zygros/conzetian-skill-lattice`: 172 tree entries, 62 paths named `SKILL.md`, tree not truncated.
- `Zygros/PHOENIX-PROTOCOL-ULTIMATE`: 2,316 tree entries, 7 `SKILL.md` paths, tree not truncated.
- `Zygros/CONZETIAN-UNIFIED-INTELLIGANCE`: 8,978 tree entries, 2 `SKILL.md` paths, tree not truncated.
- `Zygros/agents`: 1,130 tree entries, zero `SKILL.md` paths.
- Ten additional selected repositories were checked; no `SKILL.md` path was found in those ten default-branch trees.
Thus the checked subset contains **71 skill-file paths across three repositories**. This is a file count, not a deduplicated unique-skill count. It is not a full inventory of all 26 accessible Zygros repositories or all branches. Search results and branch-specific paths may reveal more.

### Existing high-value internal skills inspected
- `github-gem-seeker`: repository/code discovery and provenance.
- `internet-skill-finder`: ongoing skill discovery.
- `global-skill-synthesis-workflow`: additive skill composition.
- `omega-ecosystem-capability-ingestion`: multi-source candidate normalization, benchmarking, adversarial testing, registration, and composition.
- `sovereign-self-reverse-engineer`: documented self-audit and additive improvements.
- `verified-reasoning-mirror`: independent reasoning and uncertainty tracking.

These are overlapping, useful capabilities. The correct move is to bind them into one explicit intake and evidence pipeline, not create another redundant generic discovery skill.

## External open-source candidates

### 1. Agent Skills open format
Source: https://github.com/agentskills/agentskills  
Related specification mirror: https://github.com/Open-Dot-Agents/SKILL.md  
Why it matters: portable skill directories with a `SKILL.md` plus optional scripts, references, and assets. Progressive disclosure supports scalable skill catalogs. The opened specification mirror describes Apache-2.0 code and CC-BY-4.0 documentation; verify the canonical upstream repository and each file's license before reuse.
Decision: **Adopt as the compatibility target**, while retaining Conzetian metadata extensions separately.

### 2. skillsmd
Source: https://github.com/avvertix/skillsmd  
Observed README: Python CLI for discovering/using Agent Skills across multiple coding agents; repository displays an MIT license. Supports listing, installing, checking, and updating skills.
Decision: **Prototype candidate** for local skill discovery/install workflows. Inspect source, package provenance, and test suite before using in any production path.

### 3. OpenClaw Agent Skills
Source: https://github.com/openclaw/agent-skills  
Observed README: shared workflows for code review, transcript provenance, behavior validation, handoff, and session inspection; repository states MIT license.
Decision: **Reference and selective-adapter candidate** for review closeout, behavior validation, provenance, and portable workflows. Review each skill's scripts and privacy behavior before importing.

### 4. Vercel/open agent-skills ecosystem tooling
Source: https://github.com/isiahhill/skills.sh  
Observed README: skill discovery/installation workflows for many agent clients, including repository/path-specific selection and project/global scope.
Decision: **Research candidate** for broad skill search and interoperability. Confirm canonical upstream, license, maintenance, and CLI security before installing. Avoid automatic bulk installation.

### 5. Persistent agent memory
Source: https://github.com/TheDotMack/claude-mem (trending report referenced the project as `thedotmack/claude-mem`; canonical repository naming should be confirmed before integration).
Observed description in current trend listing: persistent cross-session context with compression and retrieval.
Decision: **Architecture reference** for memory retrieval and session summaries. Privacy, retention, data deletion, storage, and provider-specific assumptions require review.

### 6. Multi-agent team orchestration
Source: https://github.com/mvschwarz/openrig  
Observed current trend listing: persistent teams built from multiple coding agents with roles, shared context, and assigned work.
Decision: **Architecture reference** for agent ownership, shared context, and task routing. Validate repository identity, license, activity, and tests before prototype.

### 7. Reverse-engineering agent
Source: https://github.com/morluto/rea  
Observed current trend listing on 2026-10-11: agentic reverse engineering of applications and binaries; trend metrics reported rapid attention. Star velocity is not a quality or safety signal.
Decision: **High-risk research-only candidate** until code, license, security posture, and scope are reviewed. Do not import exploit, credential theft, access-control bypass, or unauthorized-target behavior. Prefer clean-room implementations based on public specifications and authorized test targets.

### 8. Coding-agent frameworks
Search surfaced:
- https://github.com/anomalyco/opencode
- https://github.com/continuedev/continue
- https://github.com/langchain-ai/open-swe
- https://github.com/QwenLM/qwen-code
Decision: **Comparison set**, not selected integrations yet. Compare extension points, model/provider flexibility, license, tests, telemetry, and ability to run with constrained mobile/local resources.

## Priority integration plan
1. **Now:** Add `open-source-gem-triage` as a specialized procedure bound to existing `github-gem-seeker` and `omega-ecosystem-capability-ingestion`.
2. **Next:** Build a machine-readable candidate registry with source URL, commit SHA, license, security notes, evidence state, capability gap, tests, and integration decision.
3. **Then:** Prototype `skillsmd`-style skill discovery in an isolated environment, comparing results to the current lattice.
4. **Then:** Evaluate 3–5 specific skills from OpenClaw and the Agent Skills ecosystem against held-out tasks.
5. **Then:** Compare one agent-memory system and one multi-agent orchestrator against the current Conzetian implementation using the same task set.
6. **Finally:** Integrate only candidates that beat a stated baseline and pass license/security review.

## Reverse-engineering method
Use public behavior, documented interfaces, source code where licensing permits, and authorized test fixtures to infer the architecture. Preserve the original source, record exact versions, reproduce behavior with tests, and implement an original adapter or clean-room alternative where appropriate. Do not assume permission to copy, bypass protections, or use proprietary internals.

## Evidence limitations
- GitHub recursive tree responses were complete for the listed repositories and not truncated.
- The 71 count covers only three repositories' `SKILL.md` paths, not every repository, branch, archive, or historical commit.
- External project descriptions were used for discovery, not full source/security audits.
- No external code was copied into the Conzetian system in this pass.
- Candidate licenses and health must be rechecked at the exact version before code reuse.
- A trend listing is a discovery signal, not proof of technical superiority.

## Sources
- Agent Skills specification: https://github.com/agentskills/agentskills
- Open-Dot-Agents specification mirror: https://github.com/Open-Dot-Agents/SKILL.md
- skillsmd: https://github.com/avvertix/skillsmd
- OpenClaw Agent Skills: https://github.com/openclaw/agent-skills
- Skills ecosystem tooling: https://github.com/isiahhill/skills.sh
- Current AI-agent trend listing (observed 2026-10-11): https://githubtrending.today/topic/ai-agents/
