"""Regression tests for Phoenix Audit's Python source discovery probe."""
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATHS = (
    ROOT / ".github/workflows/phoenix-audit.yml",
    ROOT / "core/omninet/.github/workflows/phoenix-audit.yml",
    ROOT / "core/method/.github/workflows/phoenix-audit.yml",
    ROOT / "protocols/phoenix/.github/workflows/phoenix-audit.yml",
)


def _probe_expression(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if (
            stripped.startswith("if find . -type f -name '*.py'")
            and "| grep -q ." in stripped
        ):
            return stripped[3:].split("; then", 1)[0]
    raise AssertionError(f"No Python-source probe found in {path.relative_to(ROOT)}")


def _run_probe(expression: str, cwd: Path) -> subprocess.CompletedProcess:
    script = (
        "set -euo pipefail\n"
        f"if {expression}; then printf 'PYTHON_SOURCE_DETECTED\\n'; "
        "else printf 'NO_PYTHON_SOURCE\\n'; fi"
    )
    return subprocess.run(
        ["bash", "-c", script],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def test_all_phoenix_audit_workflow_copies_use_early_exit_probe():
    for path in WORKFLOW_PATHS:
        assert path.is_file(), f"Expected workflow copy is missing: {path}"
        expression = _probe_expression(path)
        assert "-print -quit" in expression
        assert "grep -q ." in expression


def test_probe_detects_python_source(tmp_path):
    source = tmp_path / "package" / "module.py"
    source.parent.mkdir()
    source.write_text("VALUE = 1\\n", encoding="utf-8")

    result = _run_probe(_probe_expression(WORKFLOW_PATHS[0]), tmp_path)

    assert result.returncode == 0
    assert result.stdout.strip() == "PYTHON_SOURCE_DETECTED"
    assert result.stderr == ""


def test_probe_reports_absence_without_python_source(tmp_path):
    (tmp_path / "README.md").write_text("documentation only\\n", encoding="utf-8")

    result = _run_probe(_probe_expression(WORKFLOW_PATHS[0]), tmp_path)

    assert result.returncode == 0
    assert result.stdout.strip() == "NO_PYTHON_SOURCE"
    assert result.stderr == ""


def test_probe_ignores_python_files_inside_git_metadata(tmp_path):
    git_file = tmp_path / ".git" / "ignored.py"
    git_file.parent.mkdir()
    git_file.write_text("INTERNAL = True\\n", encoding="utf-8")

    result = _run_probe(_probe_expression(WORKFLOW_PATHS[0]), tmp_path)

    assert result.returncode == 0
    assert result.stdout.strip() == "NO_PYTHON_SOURCE"
    assert result.stderr == ""
