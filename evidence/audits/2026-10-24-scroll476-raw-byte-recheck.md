# Scroll 476 Raw-Byte Recheck — 2026-10-24

**Observed:** 2026-10-24T20:17:25Z  
**Evidence class:** \`RAW_BYTES_RETRIEVED_AND_PROVIDER_HASH_MATCHED\`  
**Status:** \`CORRECTION_REQUIRED_EMPTY_PAYLOAD_DIGEST_ON_NONEMPTY_ARTIFACTS\`  
**Related issue:** [#28](https://github.com/Zygros/conzet-sovereign-intelligence/issues/28)

## Retrieval and byte identity

The four source artifacts were retrieved through single-use Dropbox download URLs using remote HTTP GET requests. Every response returned HTTP 200 and its byte length exactly matched Dropbox metadata. For each file, the locally recomputed double-SHA-256 Dropbox content hash matched the provider-returned content hash. This validates the local copies as byte-identical to the connected Dropbox files without publishing the proposal contents in GitHub.

| File | Exact bytes | Raw SHA-256 | Dropbox content hash | Provider hash match |
|---|---:|---|---|---|
| \`DAO_Proposal_Scroll476.md\` | 1,135 | \`27f16d5d0910765997de7c0acd47b1ef5f6348e65727d463415bf6a7fe139e8c\` | \`67f3fe9f3b2acd5cccaec3e50ed30f17d6f8f34f032ee75608025818202e6ec2\` | PASS |
| \`DAO_Proposal_Scroll476.json\` | 1,201 | \`903db7de3539ea1dc5525b8b055fdf103b40f6b5002b3af2c494c1542b12d6b6\` | \`043af00609e651e3051add756a034f19c60d3b21202535683e8593b04b621e6f\` | PASS |
| \`DAO_Proposal_Scroll476.ots\` | 74 | \`907573c5633e2ff313b6e015fc3b0c1f23e816ea41327b3c3024440abfc2932c\` | \`4746cdcaf932d0b899ee0ceb2255f69dec84924b6d8de042e921a364d4d9a396\` | PASS |
| \`DAO_Proposal_Scroll476.md.ots\` | 514 | \`d72caf277897ec70b3b048836303b78d5aecb8e33b857f14eb64cf7b7ac2f745\` | \`02403030efab22d97245fba92f0cbfadc4833aba8154d3083b55725dd8dd9498\` | PASS |

## Hash-field result

The Markdown and JSON both contain \`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\`, which is SHA-256 of zero bytes. It does not match the exact Markdown file SHA-256, the JSON file SHA-256, or the SHA-256 of the JSON \`proposal_text\` UTF-8 value (\`de4fba0451259d1fd35b1a9323bde63db79d932695c124f47c3c87acb77fa03e\`). No explicit hash scope is declared in the fetched Markdown/JSON. The field inconsistency is now reproduced against exact bytes, not just text extraction or metadata.

## Receipt classification

- \`DAO_Proposal_Scroll476.ots\` is a 74-byte literal text placeholder beginning \`OpenTimestamps placeholder\`. It is not a valid OpenTimestamps serialized proof and must not be counted as an anchor.
- \`DAO_Proposal_Scroll476.md.ots\` begins with the binary OpenTimestamps/Proof header and contains calendar references. The corrected local helper classifies it as \`OTS_FORMAT_CANDIDATE_UNVERIFIED\`. **No \`ots verify\` command was completed in this run**, so the candidate is not described as a valid or Bitcoin-confirmed anchor.

## Tests and limits

The updated helper and fixture suite pass: Python syntax compilation succeeded and \`python -m pytest -q\` reports **4 passed**. The helper was also run on the exact local source copies and returned \`CORRECTION_REQUIRED_EMPTY_PAYLOAD_DIGEST_ON_NONEMPTY_ARTIFACTS\`, with the three candidate content hashes above. The helper now recognizes the extra NUL in this candidate's OpenTimestamps/Proof header but still never promotes a proof based on its header alone.

An attempt to install \`opentimestamps-client\` in the local environment failed because DNS resolution for the package index was unavailable. A remote verification attempt was blocked by the Firecrawl execution service's concurrent-job limit at the time of the call. Therefore proof verification and Bitcoin confirmation for \`DAO_Proposal_Scroll476.md.ots\` remain unverified.

Original Dropbox files are unchanged. The prior metadata-only report remains as the historical first-pass state; this report is an additive raw-byte follow-up. The intended verification-hash scope remains undefined and should not be silently guessed.
