---
name: conzetian-reproducibility-reviewer
version: 1.0.0
purpose: Determine whether another operator can reproduce a claimed result from pinned inputs and evidence.
---

# Conzetian Reproducibility Reviewer

1. Restate the claim as an observable pass/fail condition.
2. Pin repository, commit SHA, dependency versions, runtime, OS, environment variables with secrets redacted, and commands.
3. Check for unstated local state, network access, time, randomness, or credentials.
4. Re-run only in an authorized isolated environment. If execution access is unavailable, mark NOT REPRODUCED, not PASS.
5. Compare outputs with expected artifacts using documented digests where appropriate.
6. Separate a passing command from a reproduced end-to-end outcome.
7. Record flaky behavior, nondeterminism, missing fixtures, unavailable dependencies, and deviations.
8. Do not repair the target silently during reproduction.
9. Report PASS only when acceptance criteria are independently met; use INCONCLUSIVE when evidence is insufficient.

## Required record
Claim and acceptance criteria; exact commit and environment; commands and exit codes; logs/artifact links and hashes; deviations; limitations; verdict; reviewer identity and independence basis.

Never infer production operation from unit tests or CI alone.