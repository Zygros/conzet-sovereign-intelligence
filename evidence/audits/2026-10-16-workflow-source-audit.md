# Workflow Source Audit — 2026-10-16

**Scope:** Read-only inspection of the current default-branch workflow and verifier source files.
**Evidence class:** IMPLEMENTED (source inspected); runtime execution not performed in this audit.
**Rule:** This report records source observations only. It does not claim that any workflow was dispatched or succeeded.

## Files inspected

| File | Current blob SHA | Observation |
|---|---|---|
| `.github/workflows/federation-health.yml` | `d525ec59f3438970d259bb04df40b29f885d2a5c` | Manual dispatch and daily schedule are configured; the job runs `scripts/federation_check.py` and attempts to publish to `federation-health`. |
| `.github/workflows/opportunity-scout.yml` | `a6dbb5535fbc8034b6a6101a35f0dd9016b6f990` | Discovery, receipt generation, SHA-256 manifest creation and artifact upload are configured. Publication condition currently permits `schedule`, `workflow_dispatch`, and `push`. |
| `.github/workflows/witness.yml` | `e3f7e130cad4a8f517374acbf192f3182383ae93` | Manual dispatch, schedule, and completion-triggered runs are configured; the workflow attempts to fetch evidence branches and publish a witness report. |
| `scripts/federation_check.py` | `7f2e666389c8c5138fee7c1dcbe080203b303672` | Checks HTTP reachability of 23 public repository URLs. The script itself cautions that reachability does not prove code correctness or system health. |
| `scripts/ots_verify.py` | `41ba9466d7ed02145c387f70a29cbae0e7ff2282` | Requires a successful `ots verify` command and an explicit Bitcoin block height before marking a proof confirmed. |
| `scripts/omega_link.py` | `e83697b5eb9d82bce4293337ed6a1531f5eba20c` | Hashes an existing local artifact and prints a provenance pointer; does not verify semantic truth or independently verify OTS proofs. |
| `scripts/witness.py` | `624c3cbcca4867559eece11dafca9744b77bdde2` | Read-only structural observer; checks branch contents and file/workflow structure, not claim validity. |

## Friction found

1. **Evidence ledger may be stale about Scout publication gating.** An earlier checkpoint said the publish job allowed only scheduled or manually dispatched runs. The currently inspected workflow condition also includes `push`. Reconcile the ledger with the current file revision before relying on that older statement.
2. **Best-effort timestamping is not guaranteed anchoring.** Scout publication treats OTS installation/stamping as best effort. The existence of the workflow does not prove an `.ots` file was created or confirmed.
3. **Witness is structural, not semantic.** A visible evidence branch proves branch visibility and file presence, not that its contents are valid.
4. **No live execution was performed for this audit.** Workflow dispatch, branch publication, OTS verification, and witness generation remain unconfirmed by this source inspection.

## Next verification sequence

1. Dispatch Federation Health and preserve run URL, commit SHA, logs, and the resulting branch state.
2. Dispatch Opportunity Scout; inspect the discover and publish jobs separately, then inspect the published run directory and manifest.
3. Run `scripts/ots_verify.py` against actual published `.ots` files. Preserve raw output and classify each proof independently.
4. Run Witness after the evidence branches are available; inspect its report and compare findings with the live branch listing.
5. Run `scripts/omega_link.py` on an actual retrieved artifact and compare its digest with the workflow manifest.
6. Update the evidence ledger additively, with source revision, run IDs, exact outcomes, and unresolved gaps.

## Promotion rule

Keep source inspection at **IMPLEMENTED**. Promote a runtime claim only when the corresponding run and output are observed. Promote to independent verification only after reproduction by a separate reviewer or isolated context.
