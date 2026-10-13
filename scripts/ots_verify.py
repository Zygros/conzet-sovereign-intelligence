#!/usr/bin/env python3
"""Independently verify OpenTimestamps .ots proofs.

Reads each proof with the OpenTimestamps client and reports whether it is
confirmed on Bitcoin and, when parseable from client output, the block height.
A successful command without a recognized confirmation is not treated as
confirmation. The raw output excerpt is retained for review.
"""
import json
import pathlib
import re
import subprocess
import sys


def verify(ots_path):
    path = pathlib.Path(ots_path)
    if not path.is_file():
        return {"file": str(path), "ok": False, "confirmed": False,
                "error": "not found"}

    try:
        result = subprocess.run(
            ["ots", "verify", str(path)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except FileNotFoundError:
        return {
            "file": str(path),
            "ok": False,
            "confirmed": False,
            "error": "ots client not installed",
            "install": "pip install opentimestamps-client",
        }
    except subprocess.TimeoutExpired:
        return {"file": str(path), "ok": False, "confirmed": False,
                "error": "ots verify timed out after 60 seconds"}

    output = (result.stdout + "\n" + result.stderr).strip()
    match = re.search(r"Bitcoin block\s+(\d+)", output, flags=re.IGNORECASE)
    confirmed = bool(match) or bool(re.search(r"\bConfirmed\b", output, re.IGNORECASE))
    return {
        "file": str(path),
        "ok": result.returncode == 0,
        "confirmed": result.returncode == 0 and confirmed,
        "bitcoin_block": int(match.group(1)) if match else None,
        "raw": output.splitlines()[-8:] if output else [],
    }


def main():
    if len(sys.argv) < 2:
        print("usage: ots_verify.py <file.ots> [...]", file=sys.stderr)
        return 1

    results = [verify(argument) for argument in sys.argv[1:]]
    print(json.dumps(results, indent=2))
    unconfirmed = [item for item in results if not item.get("confirmed")]
    if unconfirmed:
        print(f"\n{len(unconfirmed)} proof(s) unconfirmed, invalid, or unverifiable")
        return 2

    heights = [item.get("bitcoin_block") for item in results]
    print(f"\nAll {len(results)} proof(s) report confirmation.")
    if all(height is not None for height in heights):
        print("Reported Bitcoin block heights: " + ", ".join(map(str, heights)))
    else:
        print("At least one confirmation had no parseable block height; inspect raw output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
