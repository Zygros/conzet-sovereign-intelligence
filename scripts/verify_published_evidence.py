#!/usr/bin/env python3
"""Verify published Scout artifact hashes and inspect OpenTimestamps proofs.

This verifies byte identity against the published manifest. Timestamp confirmation
is reported separately and is never inferred from the mere presence of a .ots file.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile

REF = "origin/evidence/scout"
RUN_ID = None
PREFIX = ""


def select_run_id():
    """Use an explicitly requested run, otherwise the newest numeric published run."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    result = subprocess.run(
        ["git", "ls-tree", "--name-only", f"{REF}:runs"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Cannot list published runs on {REF}: {result.stderr.strip()}")
    run_ids = [line.strip().rstrip("/") for line in result.stdout.splitlines()
               if line.strip().rstrip("/").isdigit()]
    if not run_ids:
        raise RuntimeError(f"No numeric run directories found on {REF}")
    return str(max((int(run_id) for run_id in run_ids)))


def git_bytes(path):
    result = subprocess.run(
        ["git", "show", f"{REF}:{PREFIX}{path}"],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Cannot read {REF}:{PREFIX}{path}: {result.stderr.decode(errors='replace')}")
    return result.stdout


def main():
    global RUN_ID, PREFIX
    RUN_ID = select_run_id()
    PREFIX = f"runs/{RUN_ID}/"
    print(f"Verifying published Scout run {RUN_ID} from {REF}")
    manifest = git_bytes("manifest.sha256").decode("utf-8")
    entries = []
    for line in manifest.splitlines():
        if not line.strip():
            continue
        expected, filename = line.split(None, 1)
        filename = filename.strip().lstrip("*")
        payload = git_bytes(filename)
        actual = hashlib.sha256(payload).hexdigest()
        entries.append({
            "file": filename,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "match": actual == expected,
            "bytes": len(payload),
        })

    proofs = []
    for proof_name, target_name in (
        ("manifest.sha256.ots", "manifest.sha256"),
        ("verification-receipts.json.ots", "verification-receipts.json"),
    ):
        try:
            proof = git_bytes(proof_name)
            target = git_bytes(target_name)
        except RuntimeError as exc:
            proofs.append({"file": proof_name, "present": False, "confirmed": False, "error": str(exc)})
            continue
        with tempfile.TemporaryDirectory() as directory:
            proof_path = pathlib.Path(directory) / proof_name
            target_path = pathlib.Path(directory) / target_name
            proof_path.write_bytes(proof)
            target_path.write_bytes(target)
            try:
                result = subprocess.run(
                    ["ots", "verify", str(proof_path)],
                    capture_output=True, text=True, timeout=90, check=False,
                )
                output = (result.stdout + "\n" + result.stderr).strip()
                block = re.search(r"Bitcoin block\s+(\d+)", output, flags=re.IGNORECASE)
                confirmed = result.returncode == 0 and block is not None
                    bool(block) or bool(re.search(r"\bConfirmed\b", output, re.IGNORECASE))
                )
                proofs.append({
                    "file": proof_name, "target_file": target_name, "present": True,
                    "client_exit_code": result.returncode,
                    "confirmed": confirmed,
                    "bitcoin_block": int(block.group(1)) if block else None,
                    "output_tail": output.splitlines()[-8:],
                })
            except FileNotFoundError:
                proofs.append({"file": proof_name, "present": True, "confirmed": False, "error": "ots client not installed"})
            except subprocess.TimeoutExpired:
                proofs.append({"file": proof_name, "present": True, "confirmed": False, "error": "ots verify timed out"})
    report = {
        "run_id": RUN_ID,
        "source_ref": REF,
        "artifact_hashes_match": all(x["match"] for x in entries),
        "artifacts": entries,
        "timestamp_proofs": proofs,
        "timestamp_confirmation_complete": bool(proofs) and all(x.get("confirmed") for x in proofs),
        "interpretation": "Hash matches establish byte identity only. Timestamp confirmation requires recognized verifier confirmation.",
    }
    rendered = json.dumps(report, indent=2) + "\n"
    pathlib.Path("published-evidence-verification.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if not report["artifact_hashes_match"]:
        return 1
    if not report["timestamp_confirmation_complete"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
