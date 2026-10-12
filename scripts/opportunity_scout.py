#!/usr/bin/env python3
"""Bounded, source-linked discovery scout for the Sovereign Conzetian Framework.

Uses only Python's standard library. Emits a JSON artifact; it does not execute
discovered code, change repository files, or promote candidates automatically.
"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

USER_AGENT = "Sovereign-Conzetian-Opportunity-Scout/1.0 (bounded public metadata discovery)"
OUT = Path(os.environ.get("SCOUT_OUTPUT", "scout-output"))
MAX_RESULTS = int(os.environ.get("SCOUT_MAX_RESULTS", "8"))
GITHUB_QUERIES = [
    "agent interoperability A2A MCP",
    "agent memory benchmark verification",
    "LLM web crawler agent",
    "agent observability OpenTelemetry",
    "Arweave AO decentralized compute",
]
ARXIV_QUERIES = [
    '("LLM agents" OR "AI agents") AND (memory OR verification)',
    '("multi-agent" OR "agentic") AND (coordination OR interoperability)',
    '("tool use" OR "agent") AND (evaluation OR benchmark)',
]

def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json, application/atom+xml, */*"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()

def github_search(query: str) -> list[dict]:
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": query, "sort": "updated", "order": "desc", "per_page": MAX_RESULTS})
    try:
        payload = json.loads(fetch(url).decode("utf-8"))
        rows = []
        for item in payload.get("items", []):
            rows.append({
                "source_type": "github_repository",
                "title": item.get("full_name"),
                "url": item.get("html_url"),
                "description": item.get("description"),
                "updated_at": item.get("updated_at"),
                "stars": item.get("stargazers_count"),
                "license": (item.get("license") or {}).get("spdx_id"),
                "query": query,
            })
        return rows
    except Exception as exc:
        return [{"source_type": "github_repository", "query": query, "error": type(exc).__name__ + ": " + str(exc)}]

def arxiv_search(query: str) -> list[dict]:
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({
        "search_query": "all:" + query,
        "start": "0",
        "max_results": str(MAX_RESULTS),
        "sortBy": "lastUpdatedDate",
        "sortOrder": "descending",
    })
    try:
        root = ET.fromstring(fetch(url))
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        rows = []
        for entry in root.findall("atom:entry", ns):
            title = " ".join((entry.findtext("atom:title", default="", namespaces=ns)).split())
            summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ns)).split())
            link = next((x.attrib.get("href") for x in entry.findall("atom:link", ns) if x.attrib.get("rel") == "alternate"), None)
            rows.append({
                "source_type": "arxiv_paper",
                "title": title,
                "url": link,
                "summary": summary[:1200],
                "published": entry.findtext("atom:published", default="", namespaces=ns),
                "updated": entry.findtext("atom:updated", default="", namespaces=ns),
                "query": query,
            })
        return rows
    except Exception as exc:
        return [{"source_type": "arxiv_paper", "query": query, "error": type(exc).__name__ + ": " + str(exc)}]

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    for query in GITHUB_QUERIES:
        records.extend(github_search(query))
        time.sleep(1.2)  # conservative public API pacing
    for query in ARXIV_QUERIES:
        records.extend(arxiv_search(query))
        time.sleep(3.0)  # conservative Atom API pacing
    seen = set()
    unique = []
    for item in records:
        key = item.get("url") or (item.get("source_type"), item.get("query"), item.get("error"))
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    document = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "public metadata discovery only; no code execution or automatic promotion",
        "record_count": len(unique),
        "records": unique,
    }
    path = OUT / "opportunity-scout.json"
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(unique)} discovery records to {path}")
    errors = sum(1 for row in unique if row.get("error"))
    print(f"Records with source errors: {errors}")
    # A temporary upstream/API failure is recorded in the artifact, not hidden.
    return 0 if unique else 1

if __name__ == "__main__":
    raise SystemExit(main())
