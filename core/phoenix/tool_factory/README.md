# PHOENIX Tool Factory v0.1

A meta-tool for turning explicitly identified capability gaps into auditable tool packages.

## Pipeline

`CAPABILITY GAP -> SPEC -> SYNTHESIS -> AST CHECK -> TEST ARTIFACT -> MANIFEST -> RECEIPT -> INDEPENDENT VERIFICATION -> PROMOTION`

The factory deliberately does **not** execute generated code or grant external authority. A generated tool is an artifact until an independent verifier promotes it.

## Why this layer exists

The architecture now has a concrete mechanism for the question: **how does the system create the tools that create future tools?**

The factory is the first-order tool-maker. A future planner can identify a gap, populate a `ToolSpec`, and hand it to `discover_and_build()`. The resulting package contains:

- `tool.py` — generated implementation
- `test_tool.py` — supplied verification cases
- `tool.json` — provenance and capability contract
- `factory_receipt.json` — generation receipt and source hash

This preserves the system's additive lineage while separating **generation** from **authority** and **execution**.

## Promotion invariant

`generated != trusted`

`trusted := independently_verified(generated) AND contract_valid(generated) AND replay_passes(generated)`
