#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TEMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TEMP_ROOT"' EXIT

BIN="$TEMP_ROOT/bin"
HOME_DIR="$TEMP_ROOT/home"
PROJECT="$TEMP_ROOT/project"
mkdir -p "$BIN" "$HOME_DIR" "$PROJECT"
chmod 755 "$PROJECT"

export HOME="$HOME_DIR"
export PYTHON_LOG="$TEMP_ROOT/python.log"
export PKG_LOG="$TEMP_ROOT/pkg.log"
export PYTEST_LOG="$TEMP_ROOT/pytest.log"
export PATH="$BIN:$PATH"

cat > "$BIN/python" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$PYTHON_LOG"
if [[ "${1:-}" == "--version" ]]; then
  echo "Python 3.12.0"
elif [[ "${1:-}" == "-c" ]]; then
  echo "3.12"
elif [[ "${1:-}" == "-m" && "${2:-}" == "venv" ]]; then
  mkdir -p "$3/bin"
else
  exit 2
fi
STUB
cat > "$BIN/git" <<'STUB'
#!/usr/bin/env bash
echo "git version 2.45.0"
STUB
cat > "$BIN/sqlite3" <<'STUB'
#!/usr/bin/env bash
echo "3.45.0"
STUB
cat > "$BIN/openssl" <<'STUB'
#!/usr/bin/env bash
echo "OpenSSL 3.0.0"
STUB
cat > "$BIN/pkg" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$PKG_LOG"
case "$*" in
  "update -y") [[ "${PKG_FAIL_UPDATE:-0}" != 1 ]] || exit 7 ;;
  "install -y python git sqlite openssl coreutils") [[ "${PKG_FAIL_INSTALL:-0}" != 1 ]] || exit 9 ;;
esac
STUB
cat > "$BIN/pytest" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$PYTEST_LOG"
echo "3 passed"
STUB
chmod +x "$BIN/"*

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
pass() { printf 'PASS: %s\n' "$1"; }

# Help and invalid arguments must not create the evidence directory.
help_output="$(bash "$ROOT/scripts/termux_preflight.sh" --help)"
[[ "$help_output" == *"never clones repositories"* ]] || fail "help output omitted the safety boundary"
[[ ! -e "$HOME/conzetian-execution" ]] || fail "help path created the project directory"
pass "help path is side-effect free"

set +e
bash "$ROOT/scripts/termux_preflight.sh" --unknown >/dev/null 2>&1
unknown_status=$?
set -e
[[ "$unknown_status" -eq 2 ]] || fail "unknown option did not return exit 2"
pass "unknown options are rejected"

# Default mode must not invoke pkg or pytest, and must not change base permissions.
: > "$PKG_LOG"
: > "$PYTEST_LOG"
bash "$ROOT/scripts/termux_preflight.sh" --project-dir "$PROJECT" >/dev/null
[[ ! -s "$PKG_LOG" ]] || fail "default mode invoked pkg"
[[ ! -s "$PYTEST_LOG" ]] || fail "default mode invoked pytest"
[[ "$(stat -c '%a' "$PROJECT")" == "755" ]] || fail "base directory permissions changed"
RUN_DIR="$(find "$PROJECT" -mindepth 1 -maxdepth 1 -type d -name 'preflight-*' | head -n 1)"
[[ -n "$RUN_DIR" ]] || fail "run directory was not created"
[[ "$(stat -c '%a' "$RUN_DIR")" == "700" ]] || fail "run directory is not private"
for child in logs receipts artifacts; do
  [[ "$(stat -c '%a' "$RUN_DIR/$child")" == "700" ]] || fail "$child directory is not private"
done
[[ -f "$RUN_DIR/receipts/preflight.txt" ]] || fail "report missing"
[[ -f "$RUN_DIR/logs/preflight.log" ]] || fail "log missing"
[[ -f "$RUN_DIR/artifacts/preflight-report.sha256" ]] || fail "checksum manifest missing"
(cd "$RUN_DIR" && sha256sum -c artifacts/preflight-report.sha256 >/dev/null) || fail "report checksum did not verify"
pass "default mode creates private per-run evidence without chmodding the base directory"

# --run-tests is explicit and routes only to the supplied target.
TEST_TARGET="$TEMP_ROOT/test-target"
mkdir -p "$TEST_TARGET"
: > "$PYTEST_LOG"
bash "$ROOT/scripts/termux_preflight.sh" --project-dir "$TEMP_ROOT/test-run" --run-tests "$TEST_TARGET" >/dev/null
grep -Fq -- "-q $TEST_TARGET" "$PYTEST_LOG" || fail "explicit test path was not passed to pytest"
pass "pytest runs only after explicit opt-in"

# --install-prereqs is explicit; package commands are intercepted by a stub.
: > "$PKG_LOG"
bash "$ROOT/scripts/termux_preflight.sh" --project-dir "$TEMP_ROOT/install-run" --install-prereqs >/dev/null
grep -Fxq "update -y" "$PKG_LOG" || fail "explicit install did not call pkg update"
grep -Fxq "install -y python git sqlite openssl coreutils" "$PKG_LOG" || fail "explicit install did not request the declared packages"
pass "package installation is gated behind the explicit flag and tested with a stub"

# Installer failures must still produce a report, log, and verifiable checksum.
set +e
update_output="$(PKG_FAIL_UPDATE=1 bash "$ROOT/scripts/termux_preflight.sh" --project-dir "$TEMP_ROOT/update-failure" --install-prereqs 2>&1)"
update_status=$?
set -e
[[ "$update_status" -eq 1 ]] || fail "pkg update failure did not return a recorded failure"
UPDATE_RUN="$(printf '%s\n' "$update_output" | sed -n 's/^run_dir=//p' | head -n 1)"
[[ -f "$UPDATE_RUN/receipts/preflight.txt" ]] || fail "pkg update failure report missing"
grep -q 'FAIL pkg_update_exit_code=7' "$UPDATE_RUN/logs/preflight.log" || fail "pkg update failure not recorded in log"
grep -q 'failure_count=1' "$UPDATE_RUN/receipts/preflight.txt" || fail "pkg update failure count missing"
(cd "$UPDATE_RUN" && sha256sum -c artifacts/preflight-report.sha256 >/dev/null) || fail "pkg update failure checksum did not verify"
pass "pkg update failure is captured in a complete evidence run"

set +e
install_output="$(PKG_FAIL_INSTALL=1 bash "$ROOT/scripts/termux_preflight.sh" --project-dir "$TEMP_ROOT/install-failure" --install-prereqs 2>&1)"
install_status=$?
set -e
[[ "$install_status" -eq 1 ]] || fail "pkg install failure did not return a recorded failure"
INSTALL_RUN="$(printf '%s\n' "$install_output" | sed -n 's/^run_dir=//p' | head -n 1)"
[[ -f "$INSTALL_RUN/receipts/preflight.txt" ]] || fail "pkg install failure report missing"
grep -q 'FAIL pkg_install_exit_code=9' "$INSTALL_RUN/logs/preflight.log" || fail "pkg install failure not recorded in log"
grep -q 'failure_count=1' "$INSTALL_RUN/receipts/preflight.txt" || fail "pkg install failure count missing"
(cd "$INSTALL_RUN" && sha256sum -c artifacts/preflight-report.sha256 >/dev/null) || fail "pkg install failure checksum did not verify"
pass "pkg install failure is captured in a complete evidence run"

mv "$BIN/pkg" "$BIN/pkg.disabled"
set +e
missing_output="$(bash "$ROOT/scripts/termux_preflight.sh" --project-dir "$TEMP_ROOT/missing-pkg" --install-prereqs 2>&1)"
missing_status=$?
set -e
mv "$BIN/pkg.disabled" "$BIN/pkg"
[[ "$missing_status" -eq 1 ]] || fail "missing pkg did not return a recorded failure"
MISSING_RUN="$(printf '%s\n' "$missing_output" | sed -n 's/^run_dir=//p' | head -n 1)"
[[ -f "$MISSING_RUN/receipts/preflight.txt" ]] || fail "missing pkg report missing"
grep -q 'BLOCKED prereq_install=pkg_not_found' "$MISSING_RUN/logs/preflight.log" || fail "missing pkg blocker not recorded"
(cd "$MISSING_RUN" && sha256sum -c artifacts/preflight-report.sha256 >/dev/null) || fail "missing pkg checksum did not verify"
pass "missing pkg is captured as a blocker with reproducible evidence"

printf 'All Termux preflight safety tests passed.\n'
