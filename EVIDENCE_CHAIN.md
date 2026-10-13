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


## Live execution checkpoint — 2026-10-12 (Pacific)

The following observations were checked against GitHub Actions and the live branch listing during this checkpoint. These entries record observed results, not inferred completion.

| Observation | Class | Evidence pointer | Result / qualification |
|---|---|---|---|
| OmniNet Python CI | TESTED_PENDING_REVIEW | [Run 38327502934](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38327502934) | Successful inspected jobs for Python 3.8, 3.9, 3.10, and 3.11; pytest, mypy, CIS verification benchmark tests, formula regression tests, and plugin trust policy tests passed in those jobs. Independent reproduction pending. |
| Phoenix Audit | TESTED_PENDING_REVIEW | [Run 38327502847](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38327502847) | Python, Node, Go, Rust, Java, and credential-pattern audit steps succeeded in the inspected run. This is not a full security certification. |
| Scout discovery and receipt generation | TESTED_PENDING_REVIEW | [Run 38327019767](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38327019767) | Discovery, receipt generation, SHA-256 manifest generation, and artifact upload succeeded. Retained artifact: `sovereign-opportunity-scout-38327019767` (53,733 bytes reported by GitHub). |
| Scout publication for run 38327019767 | IMPLEMENTED; publication not performed | [Run 38327019767](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38327019767) | `publish-evidence` was skipped because the run event was a push; the workflow gate allows only schedule or workflow_dispatch. Do not treat this run as evidence-branch publication. |
| Target evidence branches | DESIGNED / not observed | Live GitHub branch listing at checkpoint | `evidence/scout`, `federation-health`, and `witness` were absent from the inspected listing. Recheck after dispatch before claiming they exist. |
| OTS proof verification | DESIGNED / pending | `scripts/ots_verify.py` | No actual `.ots` proof verification or confirmed Bitcoin block height was observed during this checkpoint. |
| Live witness report | DESIGNED / pending | `scripts/witness.py`, `.github/workflows/witness.yml` | No live `WITNESS_REPORT.md` was observed during this checkpoint. |

### Next runtime gate

1. Dispatch `federation-health.yml` manually and inspect its run logs and `federation-health` branch.
2. Dispatch `opportunity-scout.yml` manually and confirm `publish-evidence` succeeds and publishes `evidence/scout`.
3. Retrieve the actual published `.ots` proof, run `scripts/ots_verify.py`, and preserve the full output.
4. Dispatch `witness.yml` after the evidence branches exist; inspect the resulting report on `witness`.
5. Link a real artifact through `scripts/omega_link.py` and obtain independent reproduction before promoting the ledger.

A successful CI test is evidence for the tested job and commit only. A committed workflow is not evidence of a successful workflow run. A hash establishes byte identity, not the truth of a claim.


### Retrieved Scout artifact detail

The retained ZIP for [Scout run 38327019767](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38327019767) was downloaded and inspected during this checkpoint. The artifact metadata reported by GitHub identified artifact ID `11780734822` and archive size 53,733 bytes. The archive contains:

| File | Bytes | SHA-256 | Interpretation |
|---|---:|---|---|
| `opportunity-scout.json` | 112,183 | `3f433aba39bf34f8381eff0c304fa628c0109086b75ec3a2e01232297251329d` | 104 discovery records; `triage_status` is `unreviewed_candidates` |
| `verification-receipts.json` | 224,208 | `7ce81c34bb1268ca23cd8ebf200f85500da0459b9d241f76d86a5ae5fea8f7e7` | 101 receipts, 3 rejected candidates; review gate requires human or independent review |
| `manifest.sha256` | 182 | `728e5a9eb321be008728b24eda54488e2b709f073e7d5c4037351a09a9e65831` | Recorded hashes match the two downloaded data files |

The archive itself is 53,733 bytes as reported by GitHub, while the uncompressed files are larger. The artifact's generation timestamp is `2026-10-13T00:24:34Z`, which is October 12 in Pacific time. This establishes the downloaded artifact's contents and internal manifest consistency; it does not establish that the candidates are correct, valuable, safe, or independently reproduced. No `.ots` proof was present in this downloaded artifact.


## Execution checkpoint — 2026-10-12 Pacific / 2026-10-13 UTC

- Scout workflow [38329245120](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38329245120): discovery, receipts, manifest, artifact upload, and `publish-evidence` all completed successfully. Published files are on `evidence/scout/runs/38329245120/`, including `manifest.sha256.ots` and `verification-receipts.json.ots`.
- Federation Health [38329250209](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38329250209): health check and publication job completed successfully. Run metadata is on `federation-health/health/RUN_META_2026-10-13.yaml`.
- Witness [38329338512](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38329338512): completed successfully and published [the report](https://github.com/Zygros/conzet-sovereign-intelligence/blob/witness/reports/2026-10-13.md). It observed both evidence branches and identified the missing `scripts/omega_link.py` as a structural gap.
- Friction fix: added `scripts/omega_link.py` in commit [ce98b9e](https://github.com/Zygros/conzet-sovereign-intelligence/commit/ce98b9ef2a2435ba8ea1cdfd1fbbb33fd1a288b0). It hashes a local artifact, optionally compares an expected SHA-256, and emits a `TESTED_PENDING_REVIEW` pointer. It does not assert semantic truth or independently verify claims.
- Follow-up: Witness workflow now has push triggers for changes to its script, `omega_link.py`, or the workflow itself, commit [8401e33](https://github.com/Zygros/conzet-sovereign-intelligence/commit/8401e337cea8855f28efcba839d8e415613d98ce), so the structural check can run again automatically.

Qualification: successful workflow publication and matching hashes establish pipeline execution and byte identity. The OpenTimestamps proof files are present, but their Bitcoin confirmation has not yet been independently verified. Independent reproduction remains required before promoting evidence status.


### Follow-up witness checkpoint

The push-triggered Witness run [38329495697](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/38329495697) completed successfully after `scripts/omega_link.py` was added. Its refreshed [report](https://github.com/Zygros/conzet-sovereign-intelligence/blob/witness/reports/2026-10-13.md) observes both published evidence branches and passes all five structural checks, including `omega_link_present`. No structural gaps were reported by those checks. OTS Bitcoin confirmation and independent reproduction remain separate, uncompleted verification gates.
