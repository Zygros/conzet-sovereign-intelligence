# Phoenix Audit Python source probe: reproduction and correction

Date: 2026-10-23

## Observed failure

GitHub Actions [run 40012093647](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/40012093647), job `audit`, logged a broken pipe from `find` and then printed `No Python source detected.` The repository does contain Python files: the root Python CI run collected `tests/test_federation_check.py` and completed its 78-test suite.

The prior condition was:

```bash
if find . -type f -name '*.py' -not -path './.git/*' | grep -q .; then
```

With `set -o pipefail`, `grep -q` may exit as soon as it finds a match; `find` can then receive a broken pipe. The pipeline status becomes nonzero, the `if` takes its false branch, and the Python audit body is skipped while the step can still exit successfully.

## Additive correction

Use `find ... -print -quit | grep -q .`. `find` stops after printing the first matching path, so it finishes cleanly while `grep -q` reads the one-line result. The no-match behavior remains a clean false condition. The change is applied consistently to four existing workflow copies; none is removed or renamed.

## Local reproduction

A fixture containing 5,000 generated Python files reproduced the false-negative path with the old command:

- Old probe exit status: `0`
- Old probe stdout: `No Python source detected.`
- Corrected probe exit status: `0`
- Corrected probe stdout: `Python source detected.`
- Corrected probe stderr: empty

The regression suite contains four assertions across three behavioral cases: all four workflow copies use the early-exit form; Python source is detected; a directory without Python source is handled cleanly; and Python files inside `.git` are ignored.

## Evidence boundary

The local fixture demonstrates the shell condition behavior. A new GitHub Actions run is required to establish whether the corrected workflow completes the repository-wide compile/test path. No deployment or external anchor is involved.

## Remote verification checkpoint — 2026-10-23

The corrected probe was exercised remotely on code commit `2a23418d75815c1642cc8f8740741077f37af2e8`:

- [Phoenix Audit run #317](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/40013680276) completed successfully. Its log shows the `-print -quit` probe, proceeds into the Python audit, and reports **79 passed in 0.66s**. No broken-pipe error or executed false-negative message was observed.
- [OmniNet Python CI run #261](https://github.com/Zygros/conzet-sovereign-intelligence/actions/runs/40013680033) completed with all four Python 3.8–3.11 matrix jobs successful; each log includes `tests/test_phoenix_audit_probe.py` and all four regression cases.
- Black and mypy warnings remain non-blocking and are recorded as repository-wide hygiene debt, not as clean style/type evidence.

The runs validate the cited code commit before this evidence-only update. PR #31 remains open and unmerged; no deployment or external anchor is claimed.

