# Causal Link Resolver

Status: IMPLEMENTED

## Contract
Link execution receipts, observations, evidence, patches, regressions, and outcomes into an ordered causal trace.

## Edge
`source_id`, `target_id`, `relation`, `basis`, `verification_state`, `timestamp`.

## Relations
`CAUSED`, `OBSERVED`, `SUPPORTED_BY`, `VERIFIED_BY`, `PATCHED_BY`, `REGRESSED_BY`, `FOLLOWED_BY`.

## Completion condition
A causal link is never asserted as verified unless its basis and verification state are explicitly recorded.
