# Published Scout Evidence Integrity Checkpoint

**Observed at:** 2026-10-23T20:20:11.742Z  
**Classification:** byte-integrity reproduced; latest timestamp proof not confirmed  
**Source repository:** [Zygros/conzet-sovereign-intelligence](https://github.com/Zygros/conzet-sovereign-intelligence)

## Scope

This checkpoint independently recomputes the two SHA-256 hashes listed by each selected published Scout run's `manifest.sha256`, parses the retrieved JSON payloads, and records the timestamp state reported by the published evidence verifier. Hash integrity and Bitcoin timestamp confirmation are separate facts.

## Latest published run

- **Scout run:** [#47 / 39993289060](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/39993289060), conclusion `success`.
- **Published at:** 2026-10-23T17:14:33Z; **source commit:** `dc2ee10f51eb4ff5fdc990d46d20537c18082eb5`.
- **Published files:** [manifest](https://github.com/Zygros/conzet-sovereign-intelligence/blob/evidence/scout/runs/39993289060/manifest.sha256), [Scout JSON](https://github.com/Zygros/conzet-sovereign-intelligence/blob/evidence/scout/runs/39993289060/opportunity-scout.json), [receipt JSON](https://github.com/Zygros/conzet-sovereign-intelligence/blob/evidence/scout/runs/39993289060/verification-receipts.json).
- `opportunity-scout.json`: **97,643 bytes**; manifest SHA-256 `a4a96fa9da212b562bd066b85e4f1f7a5ed6de1763065e472700a28a49895833`; independently recomputed SHA-256 matched exactly.
- `verification-receipts.json`: **196,602 bytes**; manifest SHA-256 `d0175e9cf008dc1393e67867288ea0b98866eb4076f0e56d4cb01e7ca2c21ca4`; independently recomputed SHA-256 matched exactly.
- Both JSON payloads parsed successfully. `opportunity-scout.json` reports **93 discovery records**. The receipt file reports **89 receipts** and **4 rejected records**. Its review gate is `human_or_independent_review_required`; the Scout output labels candidates `unreviewed_candidates` and states that scope is public-metadata discovery only, without code execution or automatic promotion.

## Timestamp status and qualification

The latest observed [Published Evidence Integrity run #94 / 39993465496](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/39993465496) completed successfully and uploaded [verification artifact 12519181668](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/39993465496/artifacts/12519181668). Its job log at 2026-10-23T17:14:56Z reported:

- Latest run `39993289060`: payload hashes match, but both `.ots` proofs were **pending Bitcoin confirmation**, with no block height. `timestamp_confirmation_complete` for this latest run was `false`.
- Older run `39903171799`, published at 2026-10-23T05:00:17Z: both hashes match and the verifier reported **confirmed at Bitcoin block 972716**, using a public block header from mempool.space. This confirmation applies to that older run's proofs, not to run `39993289060`.
- The overall integrity workflow returned success because the latest run was within the configured confirmation grace window and an older run outside that window was confirmed. **Workflow success does not mean the newest OTS stamps are confirmed.**

No later Published Evidence Integrity check for run `39993289060` was present in the inspected run history at this checkpoint. Therefore this document records the last observed timestamp status, not a claim that the newest proof has been rechecked at 2026-10-23T20:20:11.742Z.

## Reproduction procedure

1. Read the exact published manifest and the two target JSON files from the `evidence/scout` branch.
2. Encode the retrieved UTF-8 text to bytes and recompute SHA-256 for each target.
3. Compare computed digests with the manifest entries. Both selected runs, `39993289060` and `39903171799`, matched both payload digests in the independent check.
4. Parse the JSON and compare the record/receipt/rejection counts with the file content.
5. For timestamp status, inspect the [Integrity run log](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/39993465496) and its uploaded report. Do not promote a pending newest proof on the basis of an older run's confirmation.

The local execution container did not have the `ots` command or the `opentimestamps` Python package installed, so this checkpoint does not claim a fresh local `ots verify` invocation. The timestamp state above is explicitly attributed to the remote GitHub Actions verifier and its recorded public-header check.

## Result

| Gate | Result |
|---|---|
| Latest Scout JSON byte hash vs manifest | **PASS** |
| Latest receipt JSON byte hash vs manifest | **PASS** |
| Latest JSON parsing and internal counts | **PASS** |
| Latest Scout `.ots` Bitcoin confirmation | **PENDING / NOT VERIFIED** at last observed check |
| Older run `39903171799` timestamp | **CONFIRMED, block 972716** according to Integrity run #94 |
| Automatic promotion of discovery candidates | **NOT PERFORMED** |

No deployment, runtime correctness, independent review of the 93 candidate records, or latest-run Bitcoin confirmation is claimed.
