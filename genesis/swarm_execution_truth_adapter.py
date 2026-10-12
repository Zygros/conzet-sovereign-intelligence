"""Additive, read-only evidence gate for the legacy swarm orchestrator.

The legacy orchestrator is preserved unchanged. Its hashes and labels are
computed records, not proof that external agents ran or channels propagated.
This adapter relabels those records conservatively without mutating the source.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from agents.sovereign_swarm_orchestrator import SovereignSwarmOrchestrator
from genesis.execution_truth import classify_record

def build_evidence_gated_report(receipts_by_action: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Run the legacy report generator, then conservatively classify every output."""
    receipts_by_action = receipts_by_action or {}
    orchestrator = SovereignSwarmOrchestrator()
    report, swarms, channels, execution_log = orchestrator.run_all()

    gated_swarms = {}
    for name, record in swarms.items():
        action_id = f"swarm:{record.get('swarm_id', name)}"
        gated_swarms[name] = classify_record(record, receipts_by_action.get(action_id))

    gated_channels = {}
    for name, record in channels.items():
        action_id = f"channel:{name}"
        gated_channels[name] = classify_record(record, receipts_by_action.get(action_id))

    gated_log = [
        classify_record(record, receipts_by_action.get(f"swarm:{record.get('swarm_id', record.get('name', 'unknown'))}"))
        for record in execution_log
    ]
    executed_count = sum(item["status"] == "EXECUTED_PENDING_EVIDENCE_REVIEW" for item in gated_swarms.values())
    report = dict(report)
    report.update({
        "legacy_report_verdict": report.get("verdict"),
        "verdict": "EVIDENCE_GATED_REVIEW_REQUIRED",
        "swarms_reported": len(gated_swarms),
        "swarms_with_receipts_pending_review": executed_count,
        "swarms_without_acceptable_receipts": len(gated_swarms) - executed_count,
        "channels_reported": len(gated_channels),
        "channels_propagated_verified": 0,
        "execution_truth_policy": "No external execution or propagation is asserted without independently reviewed evidence.",
    })
    return {"report": report, "swarms": gated_swarms, "channels": gated_channels, "execution_log": gated_log}
