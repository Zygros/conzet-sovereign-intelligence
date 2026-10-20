# Security Policy

## Reporting a Vulnerability

Report suspected security issues privately to the repository owner.
Do **not** open a public issue for security vulnerabilities.

## Rules

- Never commit credentials, private keys, tokens, API keys, `.env` files, or personal data.
- Use environment variables or a secret manager for any credentials.
- Rotate any credential that may have been exposed before discussing the incident.
- HTC and all default modes remain local-only and network-disabled.
- This policy is a repository hygiene baseline. It does not certify that the historical source tree contains no secrets.

## Scope

OMEGA-10 is an evidence substrate. Signing keys used for local demonstration must never be committed.
