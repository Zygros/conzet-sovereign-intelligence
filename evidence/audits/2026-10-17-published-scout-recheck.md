# Published Scout Artifact Recheck — 2026-10-17

Evidence class: TESTED_PENDING_REVIEW for byte identity only. This is not semantic verification or a separate-party review.

Source branch: `evidence/scout`; source commit: `1b6296fc6d1c2f30a229d1a4b47dc97555cae437`.

Independent SHA-256 recomputation matched all four payloads:

- Run 39046043380: `opportunity-scout.json` = `6c06aa39b71bd9ece04908b1cd57b37548cf1c4e407c5bff4555d5964324a381`; `verification-receipts.json` = `5a9e48391d6e75f8764fbd185a873ce3b6d69148ec7256625b032799dae70aed`.
- Run 39003101540: `opportunity-scout.json` = `1f4dcd9b3193655ffa8d3a8672c1124d9cd822a6594b1bb68e923f6c322b5ff8`; `verification-receipts.json` = `1ecbfb03afd2f431f99a8031121c8b35b290b9ff08e29788d3603c7c762f072b`.

The newest run contains 94 records, 90 receipts, and 4 rejected records. All 90 receipts remain pending independent review; none marks claims verified, source content fetched, or discovered code executed. The older run contains 49 records, 38 receipts, and 11 rejected records; all 38 receipts remain pending review.

Published Evidence Integrity run [39051875524](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/39051875524) completed successfully but explicitly reports the newest run's OTS proofs are still pending. It reports the older run's proofs confirmed at Bitcoin block 971810. Do not interpret workflow success as confirmation of the newest timestamp.

Reproduction: fetch `evidence/scout`, then run `sha256sum -c manifest.sha256` inside each run directory. Hash matching proves byte identity only. Newest timestamp confirmation, semantic review, and separate-party reproduction remain open.
