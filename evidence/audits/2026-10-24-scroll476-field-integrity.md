# Scroll 476 Field-Integrity Correction Record

**Observed:** 2026-10-24 UTC  
**Evidence class:** `REPRODUCED_FIELD_INCONSISTENCY_METADATA_ONLY`  
**Related issue:** [#28, Reject placeholder OTS receipt and empty-content hash in Scroll 476 artifacts](https://github.com/Zygros/conzet-sovereign-intelligence/issues/28)

## Finding

The connected Dropbox extraction returned the same `verification_hash` value in the paired Markdown and JSON proposal:

`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

That is the standard SHA-256 digest of **zero bytes**. The extracted Markdown contains a non-empty Scroll 476 proposal, and the JSON contains a non-empty `proposal_text`. Dropbox metadata reports the Markdown at 1,135 bytes and the JSON at 1,201 bytes, so neither source file is empty. No explicit hash scope was visible in the fetched Markdown/JSON content. The field is therefore inconsistent with the non-empty artifacts if it is intended to identify either source file or the proposal text; the intended scope remains unresolved rather than assumed.

## Timestamp receipt state

| Artifact | Dropbox-reported size | Observation | Evidence status |
|---|---:|---|---|
| `DAO_Proposal_Scroll476.ots` | 74 bytes | Text extraction begins with the literal `OpenTimestamps placeholder` and a `SHA256 digest:` label. | `PLACEHOLDER_NOT_A_VALID_PROOF`; do not count as an anchor. |
| `DAO_Proposal_Scroll476.md.ots` | 514 bytes | Separate binary-like file whose extracted text includes an OpenTimestamps/Proof header and calendar references. | `PRESENT_UNVERIFIED`; presence and recognizable text do not prove that it commits to the intended source bytes or has Bitcoin confirmation. |

The files were not modified or replaced by this correction record.

## Raw-byte verification boundary

The connected Dropbox text extraction is not byte-preserving for this pair: the returned Markdown text contained 1,136 characters for a metadata size of 1,135 bytes, and the returned JSON text contained 1,202 characters for a metadata size of 1,201 bytes. A local request to the short-lived Dropbox download endpoint could not resolve DNS in the execution environment. Consequently, this run does **not** publish raw-source SHA-256 values and does not claim to have run `ots verify` on either receipt.

The additive read-only helper `scripts/audit_scroll476_integrity.py` now computes SHA-256 over the exact local bytes supplied by an operator, compares the Markdown and JSON fields, tests whether the field equals the empty-payload digest, and labels proof files as placeholder/candidate/unverified without promoting them. Four fixture tests cover these rules. The helper refuses to overwrite an existing output report.

## Reproduction

With exact local copies of the original files, run:

```bash
python scripts/audit_scroll476_integrity.py \\
  /path/to/DAO_Proposal_Scroll476.md \\
  /path/to/DAO_Proposal_Scroll476.json \\
  --placeholder-proof /path/to/DAO_Proposal_Scroll476.ots \\
  --candidate-proof /path/to/DAO_Proposal_Scroll476.md.ots
```

Then run the repository's OpenTimestamps verification workflow against the intended canonical bytes. A new timestamp should only be created after the hash scope is explicitly chosen. Preserve the original files and add a correction artifact rather than silently rewriting history. Record the raw verifier output and Bitcoin block height only if independently observed.

## Qualification

This checkpoint establishes a field-level inconsistency from the connected extraction and non-empty-file metadata. It does not establish the exact raw-byte hashes, the intended hash scope, validity of the separate `.md.ots` candidate, Bitcoin confirmation, or the truth of proposal claims. The candidate remains unverified pending exact-byte retrieval and proof verification.
