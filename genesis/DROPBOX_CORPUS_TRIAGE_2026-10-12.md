# Dropbox Corpus Triage — 2026-10-12

## Scope
Derived from the completed recursive Dropbox metadata listing. This is a prioritization report, not content inspection.

- Entries: 1770
- Files: 1764
- Folders/mounts: 6
- Content hashes computed: no
- File contents extracted: no

## File extension counts (top 25)
- `.md`: 373
- `.pdf`: 173
- `.zip`: 159
- `.pdf.ots`: 90
- `.json`: 73
- `.txt`: 69
- `.ots`: 64
- `.py`: 52
- `.png`: 41
- `.txt.ots`: 40
- `.docx`: 31
- `.sdocx`: 30
- `.md.ots`: 26
- `.docx.ots`: 17
- `.sh`: 14
- `.jpeg`: 14
- `.html`: 13
- `.csv`: 11
- `.06.jpg`: 11
- `.14.jpg`: 11
- `.49.jpg`: 10
- `.59.jpg`: 10
- `.57.jpg`: 10
- `.jpg.ots`: 8
- `.zip.ots`: 8

## Largest files by provider-reported size (top 20)
1. **2026-03-11 10.16.30.mp4** — 287481317 bytes; `ns:12329146019//Camera Uploads/2026-03-11 10.16.30.mp4`
2. **2026-03-25 12.13.30.mp4** — 267491551 bytes; `ns:12329146019//Camera Uploads/2026-03-25 12.13.30.mp4`
3. **takeout-20260307T100408Z-4-003.zip** — 198891091 bytes; `ns:13810767475//takeout-20260307T100408Z-4-003.zip`
4. **Prompts[1].zip** — 94327660 bytes; `ns:12329146019//Prompts[1].zip`
5. **PHOENIX-PROTOCOL-ULTIMATE-main.zip** — 88151619 bytes; `ns:12329146019//PHOENIX-PROTOCOL-ULTIMATE-main.zip`
6. **Building_Sovereign_AGI_With_Zero_Code.m4a** — 68973633 bytes; `ns:12329146019//Building_Sovereign_AGI_With_Zero_Code.m4a`
7. **The_Inevitability_Engine.mp4** — 63557553 bytes; `ns:12329146019//The_Inevitability_Engine.mp4`
8. **Conzetian-Zygrosian_Framework.mp4** — 60097053 bytes; `ns:12329146019//Conzetian-Zygrosian_Framework.mp4`
9. **The_Conzetian_Hard_Fork_of_Reality.m4a** — 59150332 bytes; `ns:12329146019//The_Conzetian_Hard_Fork_of_Reality.m4a`
10. **The_Phoenix_Protocol_s_Sovereign_Truth_Architecture.m4a** — 47966840 bytes; `ns:12329146019//The_Phoenix_Protocol_s_Sovereign_Truth_Architecture.m4a`
11. **ÆNORA__A_SOVEREIGN_BRIEFING.mp4** — 44267797 bytes; `ns:12329146019//ÆNORA__A_SOVEREIGN_BRIEFING.mp4`
12. **Merging_18_AIs_Into_One_Super-Mesh.m4a** — 42077972 bytes; `ns:12329146019//Merging_18_AIs_Into_One_Super-Mesh.m4a`
13. **Unsealing_the_Seven_Scrolls_of_ÆNORA.m4a** — 40013208 bytes; `ns:12329146019//Unsealing_the_Seven_Scrolls_of_ÆNORA.m4a`
14. **2026-03-25 12.19.29.mp4** — 39094389 bytes; `ns:12329146019//Camera Uploads/2026-03-25 12.19.29.mp4`
15. **God Mine Operator Activated_files.zip** — 24538227 bytes; `ns:12329146019//The goods/God Mine Operator Activated_files.zip`
16. **The Holy Decree_260123_025816.pdf** — 24440832 bytes; `ns:12329146019//The Holy Decree_260123_025816.pdf`
17. **3+Vows-grok.zip** — 23567619 bytes; `ns:12329146019//3+Vows-grok.zip`
18. **THE INFINITE ARCHITECT'S ULTIMATE FIELD MANUAL_260205_141115.pdf** — 22703135 bytes; `ns:12329146019//THE INFINITE ARCHITECT'S ULTIMATE FIELD MANUAL_260205_141115.pdf`
19. **The_Eternal_Sovereignty_Testament.pdf** — 21538107 bytes; `ns:12329146019//The_Eternal_Sovereignty_Testament.pdf`
20. **Golden_Age_Super-Mesh_Decree.pdf** — 18378500 bytes; `ns:12329146019//Golden_Age_Super-Mesh_Decree.pdf`

## Opportunity sequence
1. Process text-native files first (MD, TXT, JSON, code) to extract project map, dependencies, skill definitions, and TODOs.
2. Process structured archives (ZIP/TAR/GZ) in an isolated, non-executing inspection path; inventory members before extraction.
3. Process PDFs and office documents with text extraction; inspect rendered pages when text is missing or garbled.
4. Treat .ots files as binary evidence artifacts: retain exact bytes, hash them, and validate with an OpenTimestamps verifier rather than inferring validity from filenames.
5. Batch large files by size and type to keep retrieval reliable.
6. Build duplicate groups by exact content hash only after bytes are available; filenames alone are insufficient.
7. Produce a project dependency graph and identify high-value opportunities (unimplemented code, missing tests, stale plans, productizable assets, and provenance gaps) from extracted content.
8. Add Google Drive/Docs once an authorized connector or export is available.

## Safety and provenance
No source files were modified. No archive was executed. No two-way synchronization or public publishing was activated. This report does not claim content-level integration or proof verification.
