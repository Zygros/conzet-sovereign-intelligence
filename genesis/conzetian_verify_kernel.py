#!/usr/bin/env python3
"""Conzetian Verification Kernel: read-only inventory, SHA-256, append-only JSONL ledger.

No network calls, credential handling, source mutation, or external anchoring occur here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "conzetian-evidence-event/1.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        while True:
            block = f.read(chunk_size)
            if not block:
                break
            size += len(block)
            digest.update(block)
    return digest.hexdigest(), size


def inventory(root: Path, exclude: set[Path] | None = None) -> list[dict[str, Any]]:
    """Return sorted metadata and raw-byte SHA-256 for regular files under root."""
    root = root.resolve(strict=True)
    exclude = {p.resolve() for p in (exclude or set())}
    rows = []
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(current) / d).is_symlink())
        for name in sorted(files):
            path = Path(current) / name
            if path.is_symlink() or not path.is_file() or path.resolve() in exclude:
                continue
            digest, size = sha256_file(path)
            st = path.stat()
            rows.append({
                "path": path.relative_to(root).as_posix(),
                "size_bytes": size,
                "sha256": digest,
                "modified_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(timespec="seconds"),
            })
    return sorted(rows, key=lambda row: row["path"].casefold())


def append_event(ledger: Path, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    timestamp = utc_now()
    event = {
        "schema": SCHEMA_VERSION,
        "event_id": hashlib.sha256((timestamp + event_type + json.dumps(payload, sort_keys=True)).encode()).hexdigest(),
        "timestamp_utc": timestamp,
        "event_type": event_type,
        "payload": payload,
    }
    line = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    fd = os.open(ledger, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, (line + "\n").encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    return event


def validate_ledger(ledger: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    if not ledger.exists():
        return 0, []
    count = 0
    with ledger.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                errors.append(f"line {line_no}: blank lines are not valid events")
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON ({exc.msg})")
                continue
            if item.get("schema") != SCHEMA_VERSION:
                errors.append(f"line {line_no}: unexpected schema")
            for field in ("event_id", "timestamp_utc", "event_type", "payload"):
                if field not in item:
                    errors.append(f"line {line_no}: missing {field}")
            if not isinstance(item.get("payload"), dict):
                errors.append(f"line {line_no}: payload must be an object")
            count += 1
    return count, errors


def write_manifest(output: Path, root: Path, ledger: Path | None = None) -> dict[str, Any]:
    excludes = {output}
    if ledger:
        excludes.add(ledger)
    rows = inventory(root, excludes)
    doc = {
        "schema": "conzetian-sha256-manifest/1.0",
        "created_utc": utc_now(),
        "root_label": root.name or str(root),
        "file_count": len(rows),
        "files": rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(output.name + ".tmp")
    temp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, output)
    return doc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inv = sub.add_parser("manifest", help="hash regular files under a root without changing them")
    inv.add_argument("root", type=Path)
    inv.add_argument("output", type=Path)
    inv.add_argument("--ledger", type=Path, default=None)
    log = sub.add_parser("event", help="append one JSONL evidence event")
    log.add_argument("ledger", type=Path)
    log.add_argument("event_type")
    log.add_argument("payload_json", help="JSON object payload")
    val = sub.add_parser("validate-ledger", help="validate JSONL event structure")
    val.add_argument("ledger", type=Path)
    args = parser.parse_args(argv)
    if args.command == "manifest":
        doc = write_manifest(args.output, args.root, args.ledger)
        print(json.dumps({
            "status": "PASS",
            "files_hashed": doc["file_count"],
            "manifest": str(args.output),
            "manifest_sha256": sha256_file(args.output)[0],
        }, indent=2))
        return 0
    if args.command == "event":
        try:
            payload = json.loads(args.payload_json)
        except json.JSONDecodeError as exc:
            print(f"ERROR: invalid payload JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(payload, dict):
            print("ERROR: payload must be a JSON object", file=sys.stderr)
            return 2
        event = append_event(args.ledger, args.event_type, payload)
        print(json.dumps({"status": "APPENDED", "event_id": event["event_id"], "ledger": str(args.ledger)}, indent=2))
        return 0
    count, errors = validate_ledger(args.ledger)
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "events": count, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
