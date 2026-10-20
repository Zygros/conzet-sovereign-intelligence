# Compound Execution Register — 2026-10-20

**Owner / attribution:** Justin Neal Thomas Conzet (@Zygros)  
**Framework:** Sovereign Conzetian Framework  
**Branch:** `compound-execution-2026-10-20`  
**Purpose:** Convert outstanding references and opportunities into a non-destructive, evidence-gated execution queue.

## Governing decision protocol

**ONE DECISION → MULTIPLE OUTCOMES.**

For each bounded task, seek coordinated gains in (1) reproducible proof, (2) public attribution, (3) reusable infrastructure, (4) mobile sovereignty, and (5) commercial value. Record trade-offs when those outcomes conflict.

Execution loop:

`DISCOVER → BUILD → EXECUTE → VERIFY → PUBLISH → MONETIZE → LEARN → EVOLVE`

Append-only means preserve prior records and add corrections/superseding entries; it does **not** mean accept every claim or execute every proposed side effect. Never expose credentials, spend money, change IAM, send mail, publish private content, delete data, deploy production systems, or move funds without the specific authorization and environment required.

## Evidence classes

- **DESIGNED:** specification or proposal exists.
- **IMPLEMENTED:** code/configuration is committed.
- **EXECUTED:** a specific run/action happened and its raw result is recorded.
- **TESTED_PENDING_REVIEW:** execution evidence exists but independent reproduction is pending.
- **TESTED:** another party reproduced the documented result.
- **VERIFIED:** independent reproduction and review are recorded.
- **BLOCKED:** a named dependency or missing permission prevents execution.

A repository, prompt, screenshot, hash, successful CI job, or workflow configuration proves only what that artifact actually demonstrates. Hash equality establishes byte identity, not semantic truth.

## Current known baseline

1. The federation index and evidence ledger already exist:
   - [Federation index](https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/FEDERATION_INDEX.md)
   - [Evidence chain](https://github.com/Zygros/conzet-sovereign-intelligence/blob/main/EVIDENCE_CHAIN.md)
   - [Total Integration Index](https://github.com/Zygros/sovereign-federation/blob/main/docs/SOVEREIGN_CONZETIAN_TOTAL_INTEGRATION_2026-10-16.md)
2. The evidence ledger records successful prior CI, Scout, Federation Health, Witness and Phoenix Audit runs. These records must be rechecked against current workflow runs before being described as current.
3. The ledger explicitly leaves OpenTimestamps Bitcoin confirmation, independent reproduction, permanent-memory restart/recall tests, and a real runtime-bound agent execution as distinct verification gates.
4. The connected GitHub inventory exposed 26 repositories in the current account listing, including private repositories. This is an account-visible inventory, not a full code audit.
5. No connected Google Drive, Google Docs, Gmail, Google Cloud Storage, Google Agent Platform, Gemini API credential, or Android/Termux shell was available in this execution context. Their state is therefore **BLOCKED for live inspection/execution**, not assumed active.

## Priority queue: compound execution

### P0 — Refresh evidence and close known verification gates

- [ ] Re-read current branch, workflow and artifact state before relying on older ledger entries.
- [ ] Inspect latest successful/failed Phoenix proof-cycle runs and their receipts. Preserve the original artifact and recompute SHA-256 from downloaded bytes.
- [ ] Retrieve each actual `.ots` proof and corresponding exact source file; run the repository verifier; preserve full stdout/stderr and exit status. Record a Bitcoin block height only if the verifier explicitly confirms it.
- [ ] Run/inspect the current Federation Health and Witness reports; distinguish HTTP reachability and structural checks from correctness, service health, or independent verification.
- [ ] Execute the existing Permanent Phi Memory restart/recall/integrity/correction tests. Do not promote the memory claim until logs and reproducible test instructions are attached.
- [ ] Bind one bounded agent role to an actual runtime, run one authorized low-risk task, and capture a receipt from dispatch through independent verification. Role definitions or a dispatch plan do not prove worker processes were spawned.

### P1 — Phoenix proof package and release path

- [ ] Inspect current branch diff, CI results, receipt schema, tamper tests, documentation and release licensing.
- [ ] Keep changes on a review branch and open a draft pull request; do not merge automatically.
- [ ] Package a reproducible **Phoenix Proof and Provenance Kit** candidate containing: proof-cycle runner, receipt validator, clean/repair/failure fixtures, tamper test, machine-readable output, hash manifest, and a mobile-first README.
- [ ] Test the package from a clean Termux environment when the user-provided Android environment is available. Until then, mark local-device execution BLOCKED.

### P2 — Mobile-first, zero-dollar deployment

- [ ] Provide a Termux bootstrap script that checks Python/Git/SQLite availability, creates a virtual environment, runs local tests, writes logs and hashes, and fails closed when dependencies are missing.
- [ ] Prefer local/open-source execution and SQLite WAL for local persistence. Treat cloud APIs, paid model calls, blockchain anchoring, and hosted storage as optional adapters with explicit cost and credential gates.
- [ ] Never store API keys in source control, shell history, committed environment files, receipts, or logs.
- [ ] Measure the actual phone's RAM, disk, thermals, battery, latency and supported model size before claiming local inference capability. Do not infer that a cloud model runs on-device.

### P3 — Google API lattice integration

Implement adapters only after OAuth/service-account configuration and account/project access are available. Start read-only; request the minimum scopes and IAM permissions; record dry-run plans before writes.

**Cloud Storage JSON API**
- Base: `https://storage.googleapis.com/storage/v1`
- Inventory phase: list buckets/objects and read metadata only.
- Write phase (separate approval): object upload/copy/compose and cache operations.
- Guardrails: no delete, retention lock, IAM policy change, HMAC key creation, or public ACL change in the default workflow.
- Reference: https://docs.cloud.google.com/storage/docs/json_api/v1

**Gmail API**
- Base: `https://gmail.googleapis.com`
- Inventory phase: inspect available labels/threads only with least-privilege read scopes.
- Write phase (separate approval): create drafts first; sending, forwarding, delegation, filters and security-key changes require explicit per-action approval.
- Never print message bodies, OAuth tokens, or sensitive headers in logs.

**Drive API**
- Base: `https://www.googleapis.com/drive/v3`
- Inventory phase: list/search file metadata, then fetch only relevant files after confirming scope.
- Write phase (separate approval): create new versioned artifacts; do not overwrite, move, or delete source files by default.
- OAuth scopes and Google Sign-In client IDs must be supplied through a secure local setup, never hard-coded.

**Agent Platform / reasoning engines**
- Treat region-specific endpoints, RAG, context retrieval, long-running operations and vector search as candidate adapter capabilities, not proof of a live project.
- Verify exact API version, region, IAM permissions, billing state, endpoint name and model availability against the actual project before execution.
- Keep cancellation, timeout, bounded retries, input/output hashes and explicit BLOCKED/SIMULATION states in every adapter.

### P4 — Gemini 4 Argon API integration

Official documentation currently identifies the model ID as `gemini-4-argon`. Reference:
- https://ai.google.dev/gemini-api/docs/models/gemini-4-argon
- https://ai.google.dev/gemini-api/docs/latest-model

Implementation corrections to the supplied example:
- A 1M context window is not the same as a guaranteed 1M synchronous output. Long decode beyond the synchronous limit requires the documented background execution path and appropriate output-token limit.
- The current model guidance says sampling parameters such as `temperature`, `top_p`, and `top_k` are ignored; remove them rather than relying on deterministic sampling.
- Use `client.interactions.create(...)` with `previous_interaction_id` for server-side continuation where supported by the installed SDK version.
- Confirm API access and pricing before a request. Do not label Gemini 4 Argon as zero-cost; use local models for the zero-dollar path and make metered API calls opt-in.
- Never hard-code `GEMINI_API_KEY`; load it from a local environment variable or secure secret store.

### P5 — Public research, provenance and attribution

- [ ] Verify each Zenodo record/DOI, manuscript version, authorship metadata, public repository link and citation before including it in a public claims register.
- [ ] Verify each ARC-AGI notebook, source dataset, benchmark protocol, submitted run and measured score from the actual artifacts.
- [ ] Verify Arweave/AO process IDs by retrieving live public records and matching exact content hashes. A process identifier alone does not establish the claimed execution.
- [ ] Verify OpenTimestamps receipts against exact original files and preserve raw verifier output.
- [ ] Replace unsupported valuation, global-rarity, “world first,” production, AGI, security-rate or revenue assertions with sourced, qualified statements. Keep the original source claims in append-only history and attach corrections rather than silently erasing them.

### P6 — Portfolio unification and commercialization

- [ ] Maintain one canonical capability/evidence index linking each claim to its repository, exact path/commit, status, command, observed output, verifier, date, SHA-256 and limitations.
- [ ] Use the existing federation spine; avoid creating duplicate indexes unless a clear ownership boundary is documented.
- [ ] Cross-link only after checking destination and permissions; private repository contents must not be leaked into public indexes.
- [ ] Product hypothesis: Phoenix Proof and Provenance Kit. Validate demand with interviews or an explicitly labeled landing-page experiment before projecting revenue.
- [ ] Track product milestones separately: reproducible package, clean install, independent reproduction, license review, first user, first paid customer, support burden and measured retention.

## Mobile Termux preflight template

This is a local command sequence to run **on the user's device**; it has not been executed by this GitHub connector.

```bash
pkg update
pkg install -y python git openssl
python -V
git --version
openssl version
mkdir -p "$HOME/conzetian-execution"/{logs,receipts,artifacts}
cd "$HOME/conzetian-execution"
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
```

Before running any repository-specific script, inspect its README and dependency manifest, use a clean branch/worktree, run tests before external writes, capture exit codes and logs, and hash the final artifacts:

```bash
set -o pipefail
python -m pytest -q 2>&1 | tee "logs/pytest-$(date -u +%Y%m%dT%H%M%SZ).log"
test_code=${PIPESTATUS[0]}
sha256sum logs/*.log > artifacts/logs.sha256
exit "$test_code"
```

The test command is a template; install project dependencies and confirm the test framework before using it. Do not paste secrets into the shell command or commit local secret files.

## Completion contract

Each work item closes only with a durable receipt containing:
- stable task ID and exact scope;
- intended compound outcomes;
- repository/branch/commit or local environment;
- commands and dependency versions;
- start/end timestamps;
- raw result and exit code;
- input/output SHA-256;
- evidence class and independent reviewer status;
- side effects, cost, and approvals;
- known limitations and next action.

A successful run may create new follow-up work. Add that work to the queue, deduplicate it against existing items, and continue with the highest-value authorized non-destructive action. Never mark a blocked external dependency as complete.

---
*Register created as an additive execution artifact. It is a coordination document, not evidence that the listed work has already run.*
