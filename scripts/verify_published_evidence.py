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

RUN_ID = sys.argv[1] if len(sys.argv) > 1 else "38329245120"
REF = "origin/evidence/scout"
PREFIX = f"runs/{RUN_ID}/"


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
    for filename in ("manifest.sha256.ots", "verification-receipts.json.ots"):
        try:
            proof = git_bytes(filename)
        except RuntimeError as exc:
            proofs.append({"file": filename, "present": False, "confirmed": False, "error": str(exc)})
            continue
        with tempfile.NamedTemporaryFile(suffix=".ots") as handle:
            handle.write(proof)
            handle.flush()
            try:
                result = subprocess.run(
                    ["ots", "verify", handle.name],
                    capture_output=True, text=True, timeout=90, check=False,
                )
                output = (result.stdout + "\\n" + result.stderr).strip()
                block = re.search(r"Bitcoin block\\s+(\\d+)", output, flags=re.IGNORECASE)
                confirmed = result.returncode == 0 and (
                    bool(block) or bool(re.search(r"\\bConfirmed\\b", output, re.IGNORECASE))
                )
                proofs.append({
                    "file": filename, "present": True,
                    "client_exit_code": result.returncode,
                    "confirmed": confirmed,
                    "bitcoin_block": int(block.group(1)) if block else None,
                    "output_tail": output.splitlines()[-8:],
                })
            except FileNotFoundError:
                proofs.append({"file": filename, "present": True, "confirmed": False, "error": "ots client not installed"})
            except subprocess.TimeoutExpired:
                proofs.append({"file": filename, "present": True, "confirmed": False, "error": "ots verify timed out"})

    report = {
        "run_id": RUN_ID,
        "source_ref": REF,
        "artifact_hashes_match": all(x["match"] for x in entries),
        "artifacts": entries,
        "timestamp_proofs": proofs,
        "timestamp_confirmation_complete": bool(proofs) and all(x.get("confirmed") for x in proofs),
        "interpretation": "Hash matches establish byte identity only. Timestamp confirmation requires recognized verifier confirmation.",
    }
    print(json.dumps(report, indent=2))
    if not report["artifact_hashes_match"]:
        return 1
    if not report["timestamp_confirmation_complete"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
