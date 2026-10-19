# Scout Duplicate-Signal Audit — 2026-10-19

Status: REVIEW_SIGNAL_ONLY. This report preserves all source records and does not establish malicious intent or semantic truth.

## Reproduction context
- Repository: https://github.com/Zygros/conzet-sovereign-intelligence
- Scout workflow evidence: https://github.com/Zygros/conzet-sovereign-intelligence/actions
- Audit input SHA-256 (opportunity-scout.json): 63ca383567af03215b3af3547500acf16223f70f9939cc50ef1e08a959346f94
- Input records: 56
- URL-bearing candidate records: 46
- Source-error records: 10
- Duplicate canonical GitHub URL groups: 0
- Clone-candidate groups: 1
- Records flagged for manual review: 8
- Records deleted or automatically rejected: 0

## Cluster review
Eight repositories share the normalized slug Cognitive-Core-Skills and identical normalized descriptions. Their README Git blob SHA matches the canonical repository README blob SHA `505d84c4b6452c2338064395b1505698d4d21dd0`, while candidate repository trees contain only 8–12 files and omit the canonical repository's advertised Skills, data, schemas, benchmarks, and docs directories. Each inspected `src/core.py` has a `main()` that prints `ok`; the inspected test files contain no assertions or test functions.

This is a content-quality and provenance warning, not proof of malicious intent or infringement. No candidate code was executed. Preserve all records as pending independent review.

## Timestamp boundary
The newest Scout run's timestamp proofs remain PENDING. A confirmed proof from an older fallback run must not be attributed to the newest run. Payload hash agreement establishes byte integrity only, not claim truth.

## Proposed additive next step
Integrate `scripts/scout_duplicate_audit.py` as a non-destructive post-discovery audit, publish its JSON report alongside existing evidence, and include that report in the SHA-256 manifest. Require CI to pass before adoption. This report does not claim that proposed code is deployed or tested in GitHub Actions.

## Federation cross-link
See the canonical federation map: https://github.com/Zygros/sovereign-federation/blob/main/docs/CROSS_LINKS.md
