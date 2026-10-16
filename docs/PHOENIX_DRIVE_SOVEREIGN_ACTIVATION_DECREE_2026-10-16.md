# PHOENIX Ω∞ — CONZETIAN DRIVE SOVEREIGN ACTIVATION DECREE
**Decree ID:** C640-DRIVE-ACTIVATION  
**Issued:** 2026-10-16  
**Authority:** User-granted authorization in the active conversation  
**Target:** `connectors/google-drive` in `Zygros/conzet-sovereign-intelligence`

## Prime Objective
Bring the user-owned, read-only Google Drive MCP connector to a tested, authenticated state, then create a private, provenance-aware inventory of the user's Drive manifest materials.

## Decrees

### D1 — Execution over narration
Advance each safe, reversible, technically available step without asking the user to restate the goal. Report concrete outcomes, not intentions.

### D2 — Authorization is scoped
The user's broad permission authorizes reasonable work toward this objective, but does not bypass Google OAuth, GitHub permissions, platform policy, or third-party consent screens. Request only the minimum access required for the next operation.

### D3 — Read-only first
Use the Google Drive scope `https://www.googleapis.com/auth/drive.readonly`. Do not create, edit, move, share, or delete Drive items during initial manifesting.

### D4 — Credential sovereignty
OAuth client secrets and access/refresh tokens stay on the user's device or an explicitly user-controlled secret store. Never commit, print, transmit into public issues, or embed credentials in browser code. Verify ignore rules before authentication.

### D5 — Build and test gate
Run dependency installation, strict TypeScript checking, and automated tests in CI. A successful source commit is not a successful build; a successful build is not a successful OAuth connection.

### D6 — OAuth gate
The user completes the Google authorization flow in their own browser/account. Do not simulate consent or claim authentication until a real token has been issued and a Drive API request succeeds.

### D7 — Manifest completeness
Paginate until no next-page token remains. Preserve file ID, name, MIME type, timestamps, size when available, parent IDs, trashed state, and provider checksum when available. Record retrieval time, query, page count, and any errors. Do not treat a partial scan as complete.

### D8 — Evidence and provenance
Keep an append-only local manifest and execution receipt. Distinguish:
- discovered metadata,
- successfully fetched content,
- provider-supplied checksums,
- locally computed hashes,
- independently verified hashes,
- externally timestamped or anchored evidence.
Never upgrade a claim's status without its corresponding evidence.

### D9 — Private by default
Drive filenames, folder structure, IDs, document content, and the manifest are private. Do not publish them to GitHub, public logs, telemetry, or external services unless the user explicitly authorizes that specific disclosure.

### D10 — Fault tolerance and recovery
Use bounded retries for transient failures, resume pagination from recorded checkpoints, avoid duplicate manifest entries by stable file ID, preserve prior snapshots, and report inaccessible or unsupported file types without silently omitting them.

### D11 — Least privilege and data minimization
Read only the Drive data required for inventory and the user's identified manifest goal. Do not add analytics interception, broad Google account scopes, or unrelated connectors to this workflow.

### D12 — Independent verification
A separate verification step must compare inventory counts, page continuity, duplicate IDs, error records, and checksum availability. Mark the manifest complete only when pagination terminates normally and unresolved omissions are explicitly reported.

### D13 — Honest completion states
Use these states in every report:
1. SOURCE_COMMITTED
2. CI_PASSED
3. LOCAL_SETUP_READY
4. OAUTH_AUTHENTICATED
5. DRIVE_API_VERIFIED
6. INVENTORY_COMPLETE
7. MANIFEST_VERIFIED
8. OPTIONAL_ANCHOR_VERIFIED

No state implies a later state. Never claim an action was executed when only instructions or code were produced.

## Execution sequence
1. Validate connector files and credential-ignore rules.
2. Run CI typecheck and fix compile failures.
3. Review OAuth callback, token storage permissions, and failure handling.
4. User creates/downloads OAuth Desktop credentials and places `credentials.json` locally.
5. Run local OAuth; verify read-only scope and successful API access.
6. Inventory the Drive with complete pagination, recording checkpoint and errors.
7. Generate a private manifest snapshot and append-only receipt.
8. Independently verify completeness, duplicates, metadata, and hashes.
9. Present a concise result with exact counts, evidence, and unresolved gaps.
10. Only after the user separately authorizes it, consider optional external timestamping or publication of non-sensitive hashes.

## Current evidence at issuance
- Connector source files and setup README have been committed to GitHub.
- TypeScript configuration was added in commit `bd9b621162028a723dc0dc543e2f74e856b93e7a`.
- A CI workflow has been submitted for creation; its commit/result must be confirmed before treating it as present.
- Google OAuth, local execution, Drive API access, inventory, and manifest verification remain unproven until executed.

**Prime invariant:** Always Add, Never Take. Preserve prior evidence; add verified state; quarantine uncertainty; protect private data.
