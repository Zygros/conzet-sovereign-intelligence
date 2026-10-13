# Evidence Chain: Sovereign Conzetian Federation

## Evidence classes

Strict progression; no stage is skipped:

`DESIGNED → IMPLEMENTED → TESTED_PENDING_REVIEW → TESTED → VERIFIED`

- **DESIGNED:** specification exists; execution evidence is absent.
- **IMPLEMENTED:** code or configuration is committed. This alone does not prove it runs.
- **TESTED_PENDING_REVIEW:** an execution artifact has been produced and linked, but independent reproduction/review remains open.
- **TESTED:** a second party reproduced the documented result.
- **VERIFIED:** an independent reviewer/context reproduced the result and recorded the evidence.

## Promotion rules

- `DESIGNED → IMPLEMENTED`: commit exists and relevant static/configuration checks pass; record the checks.
- `IMPLEMENTED → TESTED_PENDING_REVIEW`: an actual run artifact is linked using `scripts/omega_link.py`; preserve its hash and run identifier.
- `TESTED_PENDING_REVIEW → TESTED`: a second party reproduces the artifact from the recorded instructions and records environment, command, date, and matching hash.
- `TESTED → VERIFIED`: an independent reviewer, separate from the author and first reviewer, reproduces the artifact from the committed record.

A commit is evidence of a committed file, not evidence of successful runtime execution. An artifact hash proves identity/integrity of bytes, not the truth of the artifact's claims.

## Ledger

| Artifact | Class | Evidence pointer | Recorded date | Qualification |
|---|---|---|---|---|
| Scout discovery (96 records) | IMPLEMENTED, reported | GitHub Actions run [38322545024](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38322545024) | 2026-10-12 | Run reference supplied for ledger import; not re-executed during this commit |
| Scout artifact SHA-256 match | TESTED_PENDING_REVIEW, reported | GitHub run 38322545024 | 2026-10-12 | Reported digest match; independent reproduction pending |
| `scout_verifier.py` receipts | IMPLEMENTED, reported | Existing repository script | 2026-10-12 | Five regression tests reported; test output not independently inspected in this change |
| `FEDERATION_INDEX.md` | IMPLEMENTED | Commit `0e94bf5` | 2026-10-12 | File committed |
| `scripts/federation_check.py` | IMPLEMENTED | Commit `7081f0b` | 2026-10-12 | File committed; execution result pending |
| `scripts/omega_link.py` | IMPLEMENTED | Commit `02d27c6` | 2026-10-12 | File committed; no artifact link recorded yet |
| `opportunity-scout.yml` publish gate | IMPLEMENTED | Commit `ded3062` | 2026-10-12 | Workflow committed; end-to-end run pending |
| README cross-links (two spine links) | IMPLEMENTED | Commits `06e5146`, `c48c218` | 2026-10-12 | Both README links fetched after commit |
| `evidence/scout` branch | DESIGNED | Scheduled/manual publication path | — | Branch creation pending successful workflow run |
| `federation-health` branch | DESIGNED | Daily 06:23 UTC workflow | — | Branch creation pending successful workflow run |
| OpenTimestamps stamp on an artifact | DESIGNED | First successful timestamping attempt | — | No stamp or confirmation recorded yet |
| `WITNESS_REPORT.md` | DESIGNED | `scripts/witness.py` | — | Script must be run against fetched remote branches |
| Independent reproduction | DESIGNED | `PROMOTE.md` | — | Requires a separate reviewer/context |

## Current gaps

1. No artifact link has yet been recorded through `omega_link.py`.
2. Automated evidence branches have not yet been confirmed present.
3. No OpenTimestamps stamp has been confirmed.
4. The federation health check has not yet been executed and reviewed in this workflow.
5. The public README cross-link sweep is committed for all 21 repositories in the supplied list. Combined with the two spine README links, all 23 public repositories now have the spine link; three private repositories remain outside this public sweep and need a separate visibility-aware pass.
6. Independent reproduction and promotion remain human review gates.

## Scheduled paths

- `evidence/scout`: intended to publish after scheduled or manually dispatched Scout runs.
- `federation-health`: intended to publish after the daily 06:23 UTC health workflow.

These are configured paths, not claims that either branch already exists or that a scheduled run has succeeded.

## Human review gates

- Promote `TESTED_PENDING_REVIEW → TESTED` only after a second party reproduces the artifact.
- Promote `TESTED → VERIFIED` only after a separate independent reviewer/context reproduces it.
- Confirm OTS stamps only after verifying the resulting proof against the source artifact.
- Complete and audit the remaining repository cross-links.
