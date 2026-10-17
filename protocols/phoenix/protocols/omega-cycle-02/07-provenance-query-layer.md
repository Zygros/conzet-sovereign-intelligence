# Provenance Query Layer

Status: IMPLEMENTED

## Contract
Allow an artifact to be traced backward to its source and forward to downstream effects.

## Query directions
`BACKWARD`: artifact → source → operation → input.

`FORWARD`: artifact → dependent artifact → execution → outcome.

## Required identifiers
Stable artifact ID, source reference, operation ID, timestamp, relation, verification state.

## Completion condition
Every provenance edge carries enough information to reconstruct its declared scope.
