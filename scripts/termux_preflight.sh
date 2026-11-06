#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail
umask 077

# Conzetian mobile preflight. Safe by default: no package installation,
# network calls, API calls, service launches, or repository mutation.
# Opt in to package installation with --install-prereqs.

INSTALL_PREREQS=0
RUN_TESTS=0
PROJECT_DIR="${HOME}/conzetian-execution"
TEST_PATH=""

usage() {
  cat <<'EOF'
Usage: termux_preflight.sh [--install-prereqs] [--run-tests [PATH]] [--project-dir PATH]

  --install-prereqs   Explicitly install python, git, sqlite, openssl, and coreutils with pkg.
  --run-tests [PATH]  Run pytest if available; optional path defaults to current directory.
  --project-dir PATH  Directory for logs, receipts, and the virtual environment.
  -h, --help          Show this help.

Default behavior only checks tools and prepares a private local evidence directory.
It does not clone repositories, run project code, start agents, or contact paid APIs.
EOF
}

while (($#)); do
  case "$1" in
    --install-prereqs) INSTALL_PREREQS=1; shift ;;
    --run-tests)
      RUN_TESTS=1; shift
      if (($#)) && [[ "$1" != --* ]]; then TEST_PATH="$1"; shift; fi
      ;;
    --project-dir)
      (($# >= 2)) || { echo "ERROR: --project-dir needs a path" >&2; exit 2; }
      PROJECT_DIR="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ "$INSTALL_PREREQS" -eq 1 ]]; then
  command -v pkg >/dev/null 2>&1 || { echo "ERROR: pkg not found; this opt-in installer is Termux-only." >&2; exit 2; }
  pkg update -y
  pkg install -y python git sqlite openssl coreutils
fi

mkdir -p "$PROJECT_DIR/logs" "$PROJECT_DIR/receipts" "$PROJECT_DIR/artifacts"
chmod 700 "$PROJECT_DIR" "$PROJECT_DIR/logs" "$PROJECT_DIR/receipts" "$PROJECT_DIR/artifacts"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$PROJECT_DIR/logs/preflight-$STAMP.log"
REPORT="$PROJECT_DIR/receipts/preflight-$STAMP.txt"

# Send console output to the log while preserving the script's exit status.
exec > >(tee -a "$LOG") 2>&1

echo "CONZETIAN MOBILE PREFLIGHT"
echo "utc_timestamp=$STAMP"
echo "project_dir=$PROJECT_DIR"
echo "install_prereqs=$INSTALL_PREREQS"
echo "run_tests=$RUN_TESTS"
echo ""

FAILURES=0
for cmd in python git sqlite3 openssl sha256sum; do
  if command -v "$cmd" >/dev/null 2>&1; then
    case "$cmd" in
      python) VERSION="$(python --version 2>&1)" ;;
      git) VERSION="$(git --version 2>&1)" ;;
      sqlite3) VERSION="$(sqlite3 --version 2>&1 | head -n 1)" ;;
      openssl) VERSION="$(openssl version 2>&1)" ;;
      sha256sum) VERSION="$(sha256sum --version 2>&1 | head -n 1)" ;;
    esac
    echo "PASS tool=$cmd version=$VERSION"
  else
    echo "MISSING tool=$cmd"
    FAILURES=$((FAILURES + 1))
  fi
done

if command -v python >/dev/null 2>&1; then
  PYTHON_MINOR="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  echo "python_minor=$PYTHON_MINOR"
  if [[ ! -d "$PROJECT_DIR/.venv" ]]; then
    python -m venv "$PROJECT_DIR/.venv" || { echo "ERROR: venv creation failed"; exit 2; }
  fi
  echo "venv=$PROJECT_DIR/.venv"
fi

if [[ "$RUN_TESTS" -eq 1 ]]; then
  if ! command -v pytest >/dev/null 2>&1; then
    echo "BLOCKED tests=pytest_not_installed; install project test dependencies first"
    FAILURES=$((FAILURES + 1))
  else
    TARGET="${TEST_PATH:-$PWD}"
    echo "running_tests_path=$TARGET"
    set +e
    pytest -q "$TARGET"
    TEST_EXIT=$?
    set -e
    echo "pytest_exit_code=$TEST_EXIT"
    if [[ "$TEST_EXIT" -ne 0 ]]; then FAILURES=$((FAILURES + 1)); fi
  fi
fi

{
  echo "utc_timestamp=$STAMP"
  echo "project_dir=$PROJECT_DIR"
  echo "failures=$FAILURES"
  echo "install_prereqs=$INSTALL_PREREQS"
  echo "run_tests=$RUN_TESTS"
} > "$REPORT"

# Hash the report and log. Keep the checksum file beside the evidence, not in source control.
sha256sum "$REPORT" "$LOG" > "$PROJECT_DIR/artifacts/preflight-$STAMP.sha256"
echo "report=$REPORT"
echo "log=$LOG"
echo "sha256_manifest=$PROJECT_DIR/artifacts/preflight-$STAMP.sha256"
echo "failure_count=$FAILURES"
if [[ "$FAILURES" -ne 0 ]]; then exit 1; fi
exit 0
