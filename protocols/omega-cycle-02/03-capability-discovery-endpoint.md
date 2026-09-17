# Capability Discovery Endpoint

Status: IMPLEMENTED

## Contract
Expose the currently available execution surfaces and their state without implying that every documented integration is connected.

## Capability record
`name`, `kind`, `availability`, `authorization_required`, `execution_boundary`, `evidence_source`.

## States
`AVAILABLE`, `CONNECTED`, `AUTH_REQUIRED`, `UNAVAILABLE`, `BLOCKED`.

## Completion condition
Capability discovery distinguishes repository artifacts from live tools, credentials, and runtime endpoints.
