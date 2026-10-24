#!/usr/bin/env python3
"""Non-destructive, metadata-only duplicate-signal audit for Scout JSON.

The tool never fetches candidate sources, runs candidate code, rejects records,
or infers malicious intent. It emits review signals while preserving source
indices and URLs so a reviewer can inspect each record in context.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple
from urllib.parse import urlsplit, urlunsplit

SCHEMA_VERSION = "scout-duplicate-signal-audit/v1"
MIN_LONG_DESCRIPTION_CHARS = 100
MIN_LONG_DESCRIPTION_WORDS = 12


def normalize_text(value: Any) -> str:
    """Normalize Unicode, case, and whitespace for comparisons."""
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", normalized).strip()


def normalize_title(value: Any) -> str:
    text = normalize_text(value)
    return re.sub(r"[^\w]+", " ", text, flags=re.UNICODE).strip()


def canonicalize_url(value: Any) -> Optional[str]:
    """Canonicalize likely repository URLs without doing network I/O."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = urlsplit(value.strip())
        scheme = parsed.scheme.casefold()
        host = (parsed.hostname or "").casefold()
        port = parsed.port
    except ValueError:
        return None
    if scheme not in ("http", "https") or not host:
        return None

    if host == "github.com":
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) == 2:
            owner, repo = parts
            repo = repo[:-4] if repo.casefold().endswith(".git") else repo
            owner = unicodedata.normalize("NFKC", owner).casefold()
            repo = unicodedata.normalize("NFKC", repo).casefold()
            return "https://github.com/{}/{}".format(owner, repo)

    netloc = host + (":{}".format(port) if port is not None else "")
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((scheme, netloc, path, parsed.query, ""))


def _repo_identity(url: Any) -> Optional[Tuple[str, str]]:
    """Return normalized (owner, repo slug) for a GitHub repository URL."""
    canonical = canonicalize_url(url)
    if not canonical:
        return None
    parsed = urlsplit(canonical)
    if parsed.hostname != "github.com":
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 2:
        return None
    return parts[0].casefold(), parts[1].casefold()


def _record_ref(index: int, record: Dict[str, Any]) -> Dict[str, Any]:
    """Keep only public source metadata needed for reviewer navigation."""
    result: Dict[str, Any] = {"record_index": index}
    for key in ("title", "url", "source_type", "query"):
        value = record.get(key)
        if value is not None:
            result[key] = value
    return result


def _group_signals(
    records: Sequence[Dict[str, Any]],
    key_fn: Callable[[Dict[str, Any], int], Optional[str]],
    signal_type: str,
    description: str,
) -> List[Dict[str, Any]]:
    groups: Dict[str, List[Tuple[int, Dict[str, Any]]]] = {}
    for index, record in enumerate(records):
        key = key_fn(record, index)
        if not key:
            continue
        groups.setdefault(key, []).append((index, record))
    signals: List[Dict[str, Any]] = []
    for key, items in groups.items():
        if len(items) < 2:
            continue
        identity = hashlib.sha256((signal_type + "\0" + key).encode("utf-8")).hexdigest()[:16]
        signals.append({
            "signal_id": identity,
            "signal_type": signal_type,
            "classification": "REVIEW_SIGNAL_ONLY",
            "description": description,
            "normalized_key_sha256": hashlib.sha256(key.encode("utf-8")).hexdigest(),
            "record_count": len(items),
            "records": [_record_ref(index, record) for index, record in items],
        })
    return sorted(signals, key=lambda item: (item["signal_type"], item["signal_id"]))


def audit_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Return a deterministic metadata-only audit for a Scout discovery document."""
    if not isinstance(document, dict) or not isinstance(document.get("records"), list):
        raise ValueError("Scout document must contain a records array")
    records_raw = document["records"]
    if any(not isinstance(record, dict) for record in records_raw):
        raise ValueError("every item in Scout records must be an object")
    records: List[Dict[str, Any]] = records_raw

    exact_url_signals = _group_signals(
        records,
        lambda record, _index: record.get("url") if isinstance(record.get("url"), str) else None,
        "exact_url_duplicate",
        "Two or more records contain the same source URL string.",
    )
    canonical_url_signals = _group_signals(
        records,
        lambda record, _index: canonicalize_url(record.get("url")),
        "canonical_url_duplicate",
        "Two or more records resolve to the same normalized source URL.",
    )
    title_signals = _group_signals(
        records,
        lambda record, _index: normalize_title(record.get("title")),
        "normalized_title_duplicate",
        "Two or more records have the same case/punctuation/whitespace-normalized title.",
    )

    def _description_text(record: Dict[str, Any]) -> str:
        """Use description when present; fall back to summary for arXiv-style records."""
        description = record.get("description")
        if isinstance(description, str) and description.strip():
            return description
        summary = record.get("summary")
        return summary if isinstance(summary, str) else ""

    def long_description_key(record: Dict[str, Any], _index: int) -> Optional[str]:
        description = normalize_text(_description_text(record))
        if len(description) < MIN_LONG_DESCRIPTION_CHARS:
            return None
        if len(description.split()) < MIN_LONG_DESCRIPTION_WORDS:
            return None
        return description

    long_description_signals = _group_signals(
        records,
        long_description_key,
        "identical_long_description",
        "Two or more records share the same normalized long description; a reviewer should decide whether it is generic or copied.",
    )

    slug_groups: Dict[str, List[Tuple[int, Dict[str, Any], str, str]]] = {}
    for index, record in enumerate(records):
        identity = _repo_identity(record.get("url"))
        description = normalize_text(_description_text(record))
        if not identity or len(description) < MIN_LONG_DESCRIPTION_CHARS:
            continue
        if len(description.split()) < MIN_LONG_DESCRIPTION_WORDS:
            continue
        owner, slug = identity
        group_key = slug + "\0" + description
        slug_groups.setdefault(group_key, []).append((index, record, owner, slug))
    same_slug_description_signals: List[Dict[str, Any]] = []
    for group_key, items in slug_groups.items():
        distinct_owners = sorted({owner for _index, _record, owner, _slug in items})
        if len(items) < 2 or len(distinct_owners) < 2:
            continue
        slug = items[0][3]
        identity = hashlib.sha256(("same_github_slug_and_description\0" + group_key).encode("utf-8")).hexdigest()[:16]
        same_slug_description_signals.append({
            "signal_id": identity,
            "signal_type": "same_github_slug_and_long_description",
            "classification": "REVIEW_SIGNAL_ONLY",
            "description": "Different GitHub owners use the same repository slug and identical normalized long descriptions.",
            "repository_slug": slug,
            "distinct_owners": distinct_owners,
            "record_count": len(items),
            "records": [_record_ref(index, record) for index, record, _owner, _slug in items],
        })
    same_slug_description_signals.sort(key=lambda item: item["signal_id"])

    signals = (
        exact_url_signals + canonical_url_signals + title_signals
        + long_description_signals + same_slug_description_signals
    )
    flagged_indices = {
        item["record_index"]
        for signal in signals
        for item in signal.get("records", [])
    }
    by_type: Dict[str, int] = {}
    for signal in signals:
        by_type[signal["signal_type"]] = by_type.get(signal["signal_type"], 0) + 1
    return {
        "schema_version": SCHEMA_VERSION,
        "input_generated_at": document.get("generated_at"),
        "input_record_count": len(records),
        "scope": "public metadata only; no source fetching or code execution",
        "result_class": "REVIEW_SIGNAL_ONLY",
        "summary": {
            "records_scanned": len(records),
            "signal_group_count": len(signals),
            "unique_records_in_signal_groups": len(flagged_indices),
            "signal_groups_by_type": by_type,
            "exact_url_duplicate_groups": len(exact_url_signals),
            "canonical_url_duplicate_groups": len(canonical_url_signals),
            "normalized_title_duplicate_groups": len(title_signals),
            "identical_long_description_groups": len(long_description_signals),
            "same_github_slug_and_long_description_groups": len(same_slug_description_signals),
        },
        "signals": signals,
        "limitations": [
            "A duplicate signal is not proof of malicious intent, infringement, or claim truth.",
            "The audit uses source metadata only; it does not fetch README files, git blobs, trees, or source code.",
            "No record is deleted, rejected, executed, or automatically promoted by this audit.",
            "Content-clone detection requires separately captured and reviewable source evidence.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Scout opportunity-scout.json")
    parser.add_argument("--output", type=Path, help="Write report to this path; otherwise print it")
    args = parser.parse_args()
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
        report = audit_document(document)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print("Wrote metadata duplicate-signal audit: {} groups across {} records".format(
            report["summary"]["signal_group_count"], report["summary"]["records_scanned"]
        ))
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
