#!/usr/bin/env python3
"""WITNESS (AG_54): read-only observer of federation evidence branches.

The script lists remote branch contents and checks local repository structure.
It does not execute the workflows, modify evidence, commit, or promote claims.
"""
import datetime
import json
import pathlib
import subprocess
import sys


def git(*args, cwd=None):
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def list_evidence(repo, branch):
    try:
        out = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", f"origin/{branch}"],
            cwd=repo, text=True, stderr=subprocess.DEVNULL
        )
        return [line for line in out.splitlines() if line.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def report(repo=".", out="WITNESS_REPORT.md"):
    repo_path = pathlib.Path(repo).resolve()
    branches = ["evidence/scout", "federation-health"]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    lines = [
        "# Witness Report\n\n",
        f"observed_at: {now}\n",
        f"repo: {repo_path}\n",
        "\n> Read-only structural observation. This report does not independently validate the contents of evidence artifacts.\n",
    ]
    findings = {"observed_at": now, "branches": {}, "checks": {}, "gaps": []}

    for branch in branches:
        files = list_evidence(repo_path, branch)
        findings["branches"][branch] = {"exists": bool(files), "files": len(files)}
        lines.append(f"\n## {branch}\n\n")
        if not files:
            lines.append("- **No files observed on this remote branch.**\n")
            findings["gaps"].append(f"{branch} branch missing or unavailable")
        else:
            for filename in sorted(files)[-20:]:
                lines.append(f"- {filename}\n")

    checks = {
        "federation_index_present": (repo_path / "FEDERATION_INDEX.md").exists(),
        "omega_link_present": (repo_path / "scripts/omega_link.py").exists(),
        "scout_verifier_present": (repo_path / "scripts/scout_verifier.py").exists(),
        "workflow_publish_gated": False,
        "federation_health_workflow_present": (repo_path / ".github/workflows/federation-health.yml").exists(),
    }
    workflow = repo_path / ".github/workflows/opportunity-scout.yml"
    if workflow.exists():
        content = workflow.read_text(encoding="utf-8")
        checks["workflow_publish_gated"] = (
            "publish-evidence" in content
            and "github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'" in content
        )

    findings["checks"] = checks
    lines.append("\n## Structural checks\n\n")
    for key, value in checks.items():
        lines.append(f"- {'✓' if value else '✗'} {key}\n")
        if not value:
            findings["gaps"].append(key)

    lines.append("\n## Gaps\n\n")
    if findings["gaps"]:
        lines.extend(f"- {gap}\n" for gap in findings["gaps"])
    else:
        lines.append("- none observed by these structural checks\n")

    lines.append("\n_Witness is observational only. Branch visibility is not proof of claim validity._\n")
    pathlib.Path(out).write_text("".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    print(json.dumps(findings, indent=2))


if __name__ == "__main__":
    report(repo=sys.argv[1] if len(sys.argv) > 1 else ".")
