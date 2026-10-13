# Promotion Procedure

## TESTED_PENDING_REVIEW → TESTED

A claim may be promoted to `TESTED` only when all of the following are recorded:

1. A second party, outside the original author's session and execution context, retrieves the artifact using the committed evidence pointer and expected SHA-256.
2. The reviewer follows the documented command in a recorded environment.
3. The reproduced output hash matches the recorded expected hash, or any justified nondeterminism is explicitly documented with a comparison method.
4. The reviewer records date/time (UTC), environment, repository and commit, command, exit status, output hash, and reviewer identity.
5. The reproduction record is committed to `EVIDENCE_CHAIN.md` or linked from it.

## TESTED → VERIFIED

A separate independent reviewer/context, distinct from both the original author and the first reviewer, reproduces the artifact using only the committed record and records the same minimum details.

## Non-negotiable rules

- No author may promote their own claim.
- Automation may create evidence and set `TESTED_PENDING_REVIEW`; it may not promote claims to `TESTED` or `VERIFIED`.
- A commit, workflow green check, URL response, SHA-256 digest, or timestamp alone does not establish the truth of a claim.
- OpenTimestamps proves a timestamped commitment to bytes once confirmed; it does not validate the artifact's semantics.
- If a reproduction fails or cannot be repeated, preserve the record and mark the discrepancy. Do not silently overwrite or delete prior evidence.

## Reviewer record template

```text
Claim/artifact:
Source repository + commit:
Evidence URL:
Expected SHA-256:
Reproduced SHA-256:
Reviewer:
Review date/time (UTC):
Environment:
Command:
Exit status:
Result:
Limitations / discrepancies:
```
