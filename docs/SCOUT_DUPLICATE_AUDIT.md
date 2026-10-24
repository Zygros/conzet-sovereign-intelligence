# Scout Duplicate-Signal Audit

The Scout duplicate-signal auditor is deliberately **metadata-only** and **non-destructive**. It canonicalizes source URLs, normalizes titles, groups sufficiently long identical descriptions, and flags the same GitHub repository slug paired with the same long description across distinct owners.

The workflow writes `duplicate-signal-audit.json` beside the discovery and receipt payloads. The SHA-256 manifest includes all three files. The manifest's OpenTimestamps proof therefore commits to the duplicate report too, even though the workflow directly stamps only the manifest and receipt JSON.

Every finding is classified `REVIEW_SIGNAL_ONLY`. A duplicate signal is not proof of malicious intent, plagiarism, or false claims. The auditor does not fetch README files, inspect git trees, execute candidate code, reject records, or promote opportunities. Content-clone assertions require separately collected source evidence and review.

The push trigger is restricted to `main` so an ordinary feature-branch push cannot publish candidate-code Scout results to the shared `evidence/scout` branch before review. PR CI still checks the code and tests before merge.
