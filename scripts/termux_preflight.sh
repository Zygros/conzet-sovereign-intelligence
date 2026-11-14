#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail
umask 077

# Conzetian mobile preflight. Safe by default: no package installation,
# network/API calls, repository mutation, or service launch.
# Package installation and project tests require explicit opt-in flags.

INSTALL_PREREQS=0
RUN_TESTS=0
PROJECT_DIR="${HOME}/conzetian-execution"
TEST_PATH=""

usage() {
  cat <<'EOF'
Usage: termux_preflight.sh [--install-prereqs] [--run-tests [PATH]] [--project-dir PATH]

  --install-prereqs   Explicitly install python, git, sqlite, openssl, and coreutils with pkg.
  --run-tests [PATH]  Run pytest only when explicitly requested; defaults to the current directory.
  --project-dir PATH  Base directory for private, per-run evidence directories.
  -h, --help          Show this help without creating files or running setup.

The script never clones repositories, starts agents, contacts paid APIs, deploys services,
or changes permissions on the supplied base directory.
EOF
}

while (($#)); do
  case "$1" in
    --install-prereqs)
      INSTALL_PREREQS=1
      shift
      ;;
    --run-tests)
      RUN_TESTS=1
      shift
      if (($#)) && [[ "$1" != --* ]]; then
        TEST_PATH="$1"
        shift
      fi
      ;;
    --project-dir)
      (($# >= 2)) || { echo "ERROR: --project-dir needs a path" >&2; exit 2; }
      [[ -n "$2" ]] || { echo "ERROR: --project-dir cannot be empty" >&2; exit 2; }
      PROJECT_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

# Never chmod the caller's base directory. All restrictive permissions apply
# only to a unique run directory created by this invocation.
mkdir -p -- "$PROJECT_DIR"
BASE_DIR="$(cd -- "$PROJECT_DIR" && pwd -P)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$(mktemp -d "${BASE_DIR%/}/preflight-${STAMP}.XXXXXX")"
chmod 700 "$RUN_DIR"
mkdir -m 700 "$RUN_DIR/logs" "$RUN_DIR/receipts" "$RUN_DIR/artifacts"

LOG="$RUN_DIR/logs/preflight.log"
REPORT="$RUN_DIR/receipts/preflight.txt"
MANIFEST="$RUN_DIR/artifacts/preflight-report.sha256"

# Keep a full console transcript while preserving command exit statuses.
exec > >(tee -a "$LOG") 2>&1

echo "CONZETIAN MOBILE PREFLIGHT"
echo "utc_timestamp=$STAMP"
echo "base_dir=$BASE_DIR"
echo "run_dir=$RUN_DIR"
echo "install_prereqs=$INSTALL_PREREQS"
echo "run_tests=$RUN_TESTS"
echo ""

FAILURES=0

# Keep explicit package installation inside the evidence transcript. A missing
# pkg binary or a failed update/install is recorded instead of aborting before
# the per-run report and checksum manifest exist.
if [[ "$INSTALL_PREREQS" -eq 1 ]]; then
  if ! command -v pkg >/dev/null 2>&1; then
    echo "BLOCKED prereq_install=pkg_not_found"
    FAILURES=$((FAILURES + 1))
  elif pkg update -y; then
    echo "PASS pkg_update"
    if pkg install -y python git sqlite openssl coreutils; then
      echo "PASS pkg_install"
    else
      PKG_EXIT=$?
      echo "FAIL pkg_install_exit_code=$PKG_EXIT"
      FAILURES=$((FAILURES + 1))
    fi
  else
    PKG_EXIT=$?
    echo "FAIL pkg_update_exit_code=$PKG_EXIT"
    echo "SKIP pkg_install reason=update_failed"
    FAILURES=$((FAILURES + 1))
  fi
fi
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
  if PYTHON_MINOR="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"; then
    echo "python_minor=$PYTHON_MINOR"
    if python -m venv "$RUN_DIR/.venv"; then
      echo "PASS venv=$RUN_DIR/.venv"
    else
      echo "FAIL venv_creation"
      FAILURES=$((FAILURES + 1))
    fi
  else
    echo "FAIL python_version_probe"
    FAILURES=$((FAILURES + 1))
  fi
fi

if [[ "$RUN_TESTS" -eq 1 ]]; then
  if ! command -v pytest >/dev/null 2>&1; then
    echo "BLOCKED tests=pytest_not_installed; install project test dependencies first"
    FAILURES=$((FAILURES + 1))
  else
    TARGET="${TEST_PATH:-$PWD}"
    if [[ ! -e "$TARGET" ]]; then
      echo "FAIL tests=target_not_found path=$TARGET"
      FAILURES=$((FAILURES + 1))
    else
      echo "running_tests_path=$TARGET"
      if pytest -q "$TARGET"; then
        echo "PASS pytest"
      else
        TEST_EXIT=$?
        echo "FAIL pytest_exit_code=$TEST_EXIT"
        FAILURES=$((FAILURES + 1))
      fi
    fi
  fi
fi

{
  echo "utc_timestamp=$STAMP"
  echo "base_dir=$BASE_DIR"
  echo "run_dir=$RUN_DIR"
  echo "failure_count=$FAILURES"
  echo "install_prereqs=$INSTALL_PREREQS"
  echo "run_tests=$RUN_TESTS"
  echo "log_path=$LOG"
} > "$REPORT"

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum "$REPORT" > "$MANIFEST"
  echo "PASS report_sha256_manifest=$MANIFEST"
else
  FAILURES=$((FAILURES + 1))
  {
    echo "utc_timestamp=$STAMP"
    echo "base_dir=$BASE_DIR"
    echo "run_dir=$RUN_DIR"
    echo "failure_count=$FAILURES"
    echo "install_prereqs=$INSTALL_PREREQS"
    echo "run_tests=$RUN_TESTS"
    echo "log_path=$LOG"
    echo "checksum_manifest=unavailable"
  } > "$REPORT"
  echo "BLOCKED checksum_manifest=sha256sum_not_available"
fi

echo "report=$REPORT"
echo "log=$LOG"
echo "failure_count=$FAILURES"
if [[ "$FAILURES" -ne 0 ]]; then
  exit 1
fi
exit 0
