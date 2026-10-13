#!/usr/bin/env python3
"""Create a hash-checked Markdown pointer for an existing evidence artifact.

This helper records artifact identity and provenance metadata. It does not
verify the truth of an artifact's claims, verify OpenTimestamps proofs, or
promote evidence beyond TESTED_PENDING_REVIEW.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.parse import urlparse


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path, help="local artifact file to hash")
    parser.add_argument("--run-id", required=True, help="GitHub Actions run ID")
    parser.add_argument("--run-url", required=True, help="canonical run URL")
    parser.add_argument("--expected-sha256", help="optional expected SHA-256 to compare")
    parser.add_argument("--label", default="Evidence artifact", help="human-readable artifact label")
    args = parser.parse_args()

    parsed = urlparse(args.run_url)
    if parsed.scheme != "https" or parsed.netloc != "github.com":
        parser.error("--run-url must be an HTTPS github.com URL")
    if not args.run_id.isdigit():
        parser.error("--run-id must contain digits only")
    if not args.artifact.is_file():
        parser.error(f"artifact does not exist: {args.artifact}")

    actual = sha256_file(args.artifact)
    matches = args.expected_sha256 is None or actual.lower() == args.expected_sha256.lower()
    print(f"artifact: {args.artifact}")
    print(f"run_id: {args.run_id}")
    print(f"run_url: {args.run_url}")
    print(f"sha256: {actual}")
    print(f"expected_sha256_match: {str(matches).lower()}")
    print("\n### Evidence pointer (TESTED_PENDING_REVIEW)")
    print(f"- Artifact: {args.label}")
    print(f"- Run: [{args.run_id}]({args.run_url})")
    print(f"- Local path: `{args.artifact.as_posix()}`")
    print(f"- SHA-256: `{actual}`")
    print("- Evidence class: TESTED_PENDING_REVIEW")
    print("- Qualification: hash identity only; semantic truth and independent reproduction remain unverified.")

    return 0 if matches else 2


if __name__ == "__main__":
    raise SystemExit(main())
