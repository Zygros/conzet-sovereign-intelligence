# Conzetian Ω∞ — Cascading Corpus Integration Plan

Date: 2026-10-12
Owner: Justin Neal Thomas Conzet / G0 Prime

## Governing rule
Preserve the source corpus. Inventory first, hash before transfer, deduplicate by content, record provenance, and never overwrite or delete originals during synchronization. Conflicts become explicit review records.

## Cascading phases

### Phase 0 — Access and scope
- Available now: connected Dropbox and GitHub repository `Zygros/conzet-sovereign-intelligence`.
- Not currently available in this session: a direct Google Drive / Google Docs connector. No Google Drive contents have been read or modified.
- Required for Google integration: connect/authorize the Google Drive/Docs integration in ChatGPT or provide a user-selected export/archive. Do not share passwords, OAuth tokens, or private keys in chat.

### Phase 1 — Inventory (read-only)
- Enumerate Dropbox root and all nested folders, preserving path, provider file ID, size, modified time, MIME/type, and shared status where available.
- Enumerate Google Drive and Docs once authorized, including native Docs metadata and exportable content.
- Build a source registry with stable IDs and source URLs; record pagination and any inaccessible locations.

### Phase 2 — Evidence and integrity
- Hash downloadable bytes with SHA-256; keep provider-native content hashes in separate fields.
- Verify existing manifest-to-file relationships and OpenTimestamps proofs only after obtaining exact binary files and running a compatible verifier.
- Classify each item as verified, metadata-only, inaccessible, conflicting, or pending.

### Phase 3 — Corpus normalization
- Group by content hash and near-duplicate title; never merge solely because titles match.
- Extract text from PDFs, DOCX, MD, TXT, JSON, source code, and exported Google Docs; retain originals and extraction provenance.
- Tag each artifact by project, subsystem, date, artifact type, status, dependencies, and evidence strength.

### Phase 4 — Canonical index and cross-links
- Generate an append-only master inventory and project map for Phoenix Protocol, CIS, CZAOUA, InfiniteOS-ZAAI, Memoria Omnia, OmniNet, HTC, skills/protocols, proof artifacts, and monetization assets.
- Preserve original language and user-defined terminology; record conflicts as alternate versions rather than silently rewriting.
- Include hashes, source path, source link, retrieval timestamp, and validation status.

### Phase 5 — Synchronization
- Default mode is non-destructive, one-way archival copy into a clearly designated canonical destination, followed by byte/hash verification.
- Two-way sync is disabled until conflict rules and destination are explicitly chosen. Never delete, rename, or overwrite originals automatically.
- Keep access-controlled/private material private; do not publish the full corpus publicly by default.

### Phase 6 — Execution and deployment
- Validate the current Genesis Kit independently from the historical Dropbox proof pack.
- Run code tests and GitHub Actions; record run IDs and commit SHAs.
- Establish an authorized permanent-storage path, publish only the approved package, retrieve it, and verify exact bytes before claiming an anchor.
- Deploy a persistent agent only when a real runtime, credentials, scopes, budgets, and monitoring are available.

### Phase 7 — Recovery and maintenance
- Test clean-session recovery from the canonical index and ledger.
- Add scheduled inventory-drift checks only after a connected event source or scheduler is configured and verified.
- Report completed, failed, blocked, and unattempted tasks separately.

## Current evidence snapshot
- Latest proof-investigation commit: `e50558ce35e9f749e85fc0c98a3adf2858d7f69c`.
- Phoenix Audit: passed for that commit: https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38309835140
- OmniNet Python CI: passed for that commit: https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38309835123
- Historical Dropbox proof-pack manifest records bundle hash `9948179a541811d80358440e207f04f33f804271c0d993fe2b93bb465b38ba74`; raw source hashes and timestamp chain remain independently unvalidated in this run.
- No current Genesis Kit Arweave anchor is established.

## Immediate next actions
1. Connect Google Drive/Docs access or provide a Drive export, then perform a read-only inventory.
2. Continue recursive Dropbox inventory and create a master manifest in batches.
3. Acquire exact historical proof files and validate their hashes and timestamp chains.
4. Generate and verify the current Genesis Kit manifest.
5. Only then synchronize copies and pursue external anchoring/deployment.