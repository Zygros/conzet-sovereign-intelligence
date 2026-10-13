#!/usr/bin/env python3
"""Check public repository URLs in the Zygros federation index."""
import datetime
import urllib.error
import urllib.request

OWNER = "Zygros"
REPOS = [
    "sovereign-federation",
    "conzetian-skill-lattice",
    "omega-10",
    "conzetian-method",
    "conzet-sovereign-intelligence",
    "PHOENIX-PROTOCOL-ULTIMATE",
    "multi-ai-convergence-protocol",
    "ultimate-phoenix-protocol",
    "ultimate-phoenix-protocol-ssi",
    "omninet-v4",
    "CONZETIAN-UNIFIED-INTELLIGANCE",
    "CZAOUA-UNITY-SYSTEM",
    "we-omega",
    "agents",
    "agentql",
    "Sovereign-AGSI-Archive",
    "ZYGROS-PRIME",
    "Grossian_Scrolls",
    "ZYGNUS-OMNI-REPO",
    "ZAAI-SYSTEM",
    "zyth-ultimate",
    "ARC-AGI",
    "Conzet-Intelligence-System-",
]

def check(repo):
    url = f"https://github.com/{OWNER}/{repo}"
    req = urllib.request.Request(
        url, method="GET",
        headers={"User-Agent": "conzetian-federation-check/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return "LIVE", response.status
    except urllib.error.HTTPError as exc:
        return ("NOT_FOUND_OR_PRIVATE" if exc.code == 404 else "HTTP_ERROR"), exc.code
    except Exception as exc:
        return "ERROR", str(exc)[:100]

def main():
    print(f"Federation check — {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n")
    print(f"{'REPOSITORY':<42} STATUS")
    print("-" * 70)
    live = 0
    for repo in REPOS:
        status, detail = check(repo)
        if status == "LIVE":
            live += 1
        print(f"{repo:<42} {status} {detail}")
    print("-" * 70)
    print(f"{live}/{len(REPOS)} public repository URLs responded successfully.")
    print("A successful HTTP response proves URL reachability only, not code correctness or system health.")

if __name__ == "__main__":
    main()
