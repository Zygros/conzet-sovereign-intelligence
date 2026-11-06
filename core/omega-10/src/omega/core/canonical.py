"""Canonical JSON serialization for deterministic hashing and evidence."""

from __future__ import annotations

import json
from typing import Any


def _normalize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): _normalize(v) for k, v in sorted(obj.items(), key=lambda x: str(x[0]))}
    if isinstance(obj, (list, tuple)):
        return [_normalize(v) for v in obj]
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int) and not isinstance(obj, bool):
        return obj
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):
            return str(obj)
        return obj
    if obj is None:
        return None
    if isinstance(obj, str):
        return obj
    return str(obj)


def canonical_dumps(obj: Any, *, ensure_ascii: bool = False) -> str:
    normalized = _normalize(obj)
    return json.dumps(
        normalized,
        ensure_ascii=ensure_ascii,
        separators=(",", ":"),
        sort_keys=True,
        allow_nan=False,
    )


def canonical_json(obj: Any) -> bytes:
    return canonical_dumps(obj).encode("utf-8")
