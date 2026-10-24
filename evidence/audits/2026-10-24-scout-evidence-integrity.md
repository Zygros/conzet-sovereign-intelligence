# Independent Scout Evidence-Integrity Checkpoint — 2026-10-24

**Evidence class:** `TESTED_PENDING_REVIEW`  
**Observation time:** `2026-10-24T16:02:20.294222Z`  
**Purpose:** preserve payload identity, receipt counts, and timestamp status for the newly published Scout run without upgrading unverified candidate claims.

## Source run

- [Scout workflow run 40109587547](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/40109587547) published the evidence at `2026-10-24T16:01:59Z` from source commit [`a9fa362e`](https://github.com/Zygros/conzet-sovereign-intelligence/commit/a9fa362edfcd1c5a8b77d7742df3c33d9d0a1bea).
- Published directory: [`runs/40109587547`](https://github.com/Zygros/conzet-sovereign-intelligence/tree/evidence/scout/runs/40109587547).
- The [manifest](https://github.com/Zygros/conzet-sovereign-intelligence/blob/evidence/scout/runs/40109587547/manifest.sha256) lists the two JSON payload digests below.

## Payload identity checks

The exact UTF-8 content returned by GitHub's file API was hashed again in this execution with a SHA-256 implementation that passed the standard `abc` test vector.

| File | Bytes | Manifest digest | Recomputed digest | Result |
|---|---:|---|---|---|
| [`opportunity-scout.json`](https://github.com/Zygros/conzet-sovereign-intelligence/blob/evidence/scout/runs/40109587547/opportunity-scout.json) | 102,319 | `2ca43c08601cac4aa3171c0c97272d9da474f8e9a7ac31cc41ec2f0c15e9e602` | `2ca43c08601cac4aa3171c0c97272d9da474f8e9a7ac31cc41ec2f0c15e9e602` | PASS |
| [`verification-receipts.json`](https://github.com/Zygros/conzet-sovereign-intelligence/blob/evidence/scout/runs/40109587547/verification-receipts.json) | 214,384 | `68b97a14b45374d257a9ddb5ef9083857970e0d6ba65e5f2f7d27a78cc83f0c2` | `68b97a14b45374d257a9ddb5ef9083857970e0d6ba65e5f2f7d27a78cc83f0c2` | PASS |

These matches establish byte identity against the manifest, not that the records' claims are true.

## Receipt and review state

The publication contains **100 discovery records, 97 receipts, and 3 rejected records**. Every receipt remains `pending_independent_review`. All receipts set `claims_verified=false`, `source_content_fetched=false`, and `discovered_code_executed=false`. The run declares public-metadata-only discovery with `unreviewed_candidates` and a `human_or_independent_review_required` gate.

These counts are not counts of independently validated opportunities. No candidate promotion is claimed.

## OpenTimestamps state

[Published Evidence Integrity run 40109682679](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/40109682679) completed with a green workflow conclusion. Its log at `2026-10-24T16:02:20Z` explicitly reported that both new proofs, [`manifest.sha256.ots`](https://github.com/Zygros/conzet-sovereign-intelligence/blob/evidence/scout/runs/40109587547/manifest.sha256.ots) and [`verification-receipts.json.ots`](https://github.com/Zygros/conzet-sovereign-intelligence/blob/evidence/scout/runs/40109587547/verification-receipts.json.ots), were **pending Bitcoin confirmation** with no block height.

The same log separately reported older run [40063447250](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/40063447250) confirmed at Bitcoin block **972879**. That older confirmation does not anchor run 40109587547. The workflow's successful result reflects configured fallback/grace-window behavior and must not be interpreted as confirmation of the newest proof.

## Reproduction and limitations

- Use the published manifest and exact JSON files with a SHA-256 verifier to reproduce the payload identity checks.
- The local environment had neither the `ots` executable nor the `opentimestamps` Python module, and local DNS resolution to GitHub's raw file host failed. The proof status above is therefore the status from the cited remote integrity log, not a fresh local `ots verify` execution.
- No later verification of run 40109587547 was observed in this checkpoint. A later integrity run is required to establish whether its proofs eventually received Bitcoin block attestations.

The machine-readable companion file, `2026-10-24-scout-evidence-integrity.json`, preserves run identifiers, exact digests, counts, timestamp state, and qualifiers.

No deployment, external anchor for the newest publication, independent source-claim validation, or automatic candidate promotion is claimed.
