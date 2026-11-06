# Termux Preflight Static Check — 2026-10-20

## Artifact

- Script: [`scripts/termux_preflight.sh`](https://github.com/Zygros/conzet-sovereign-intelligence/blob/compound-execution-2026-10-20/scripts/termux_preflight.sh)
- Git commit adding script: `5fb564c8d4f3d3f26d53323377dde5c531f4fc1e`
- Local test environment: Linux Bash in the ChatGPT execution container, **not Android/Termux**.
- Local source SHA-256: `7be53edf2c36097e75a29d466adc032897d378dc1bee7d092bd604e988230d87`

## Checks actually run

- `bash -n /tmp/termux_preflight.sh`: PASS.
- `bash /tmp/termux_preflight.sh --help`: PASS; usage text printed and no setup action executed.

## Behavior encoded

- Default mode avoids package installation, network/API calls, service launches, and repository mutation.
- Explicit `--install-prereqs` is required before Termux package installation.
- Logs, receipts and checksum manifests are written beneath a user-selected local directory with restrictive permissions.
- Optional test execution requires an explicit `--run-tests` flag.
- The script does not start agent processes or claim that any swarm is active.

## Not tested

- Not executed on an Android device or in Termux.
- Package names and venv behavior have not been validated against the user's installed Termux version.
- No phone resources, storage, battery, network, or API credentials were inspected.
- No live repository test suite was run by this script.

**Status:** Static shell syntax and help-path checks passed on Linux. Termux/device execution remains pending.
