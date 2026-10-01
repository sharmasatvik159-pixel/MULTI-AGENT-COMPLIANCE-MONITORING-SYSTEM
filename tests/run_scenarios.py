"""Master Scenario Automation Suite for Meridian Global Bank Compliance Surveillance.

Executes all 20 compliance scenarios (CS-01 through CS-20) through the complete pipeline:
Ingestion -> Agent Detection -> Dempster-Shafer Consensus -> HITL Escalation -> Report Compilation -> Merkle Audit Sealing.
Verifies CS-18 suppression, CS-19 cross-jurisdiction conflict, and CS-20 multi-agent coordination.
Saves comprehensive results to tests/scenarios/execution_results.json.
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.escalation.orchestrator import ComplianceOrchestrator
from src.generators.mock_stream import MockStreamGenerator
from src.observability.audit_ledger import MerkleAuditLedger
from src.observability.dashboard_metrics import DashboardMetricsCollector


def run_all_scenarios() -> Dict[str, Any]:
    """Execute all 20 compliance test scenarios programmatically and return verification results."""
    print("=" * 80)
    print("MERIDIAN GLOBAL BANK - 20-SCENARIO COMPLIANCE AUTOMATION RUNNER")
    print("=" * 80)

    orchestrator = ComplianceOrchestrator()
    generator = MockStreamGenerator()
    ledger = MerkleAuditLedger(epoch_block_size=5)
    metrics = DashboardMetricsCollector()

    scenario_results: Dict[str, Any] = {}
    passed_scenarios = 0
    failed_scenarios = 0

    all_scenario_ids = [f"CS-{i:02d}" for i in range(1, 21)]

    for sid in all_scenario_ids:
        bundle = generator.get_scenario_event_bundle(sid)
        name = bundle["name"]
        expected_tier = bundle["escalation_tier"]

        t_start = time.perf_counter()
        result = orchestrator.execute_scenario_pipeline(bundle)
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0

        escalation = result["escalation"]
        actual_tier = escalation["target_tier"]
        is_suppressed = escalation.get("is_suppressed", False)

        # Verification rules
        scenario_passed = True
        verification_notes = []

        # CS-18 Verification: Must suppress alert without human escalation
        if sid == "CS-18":
            if actual_tier == "NONE" and is_suppressed:
                verification_notes.append("PASS: CS-18 correctly suppressed institutional block trade false positive.")
            else:
                scenario_passed = False
                verification_notes.append(f"FAIL: CS-18 was not suppressed (Target Tier: {actual_tier}).")

        # CS-19 Verification: Must flag multi-jurisdiction regulatory conflict
        elif sid == "CS-19":
            if actual_tier == "TIER_4_CCO_BOARD" and "SOVEREIGN_CONFLICT" in escalation.get("action", ""):
                verification_notes.append("PASS: CS-19 correctly identified EMIR vs MAS cross-border conflict.")
            else:
                scenario_passed = False
                verification_notes.append(f"FAIL: CS-19 did not escalate properly to Tier 4 (Actual: {actual_tier}).")

        # CS-20 Verification: Must coordinate across all agents and escalate to Tier 4
        elif sid == "CS-20":
            if actual_tier == "TIER_4_CCO_BOARD" and result["report_generated"]:
                verification_notes.append("PASS: CS-20 coordinated multi-agent money laundering detection with SAR compilation.")
            else:
                scenario_passed = False
                verification_notes.append(f"FAIL: CS-20 failed full coordination (Report: {result['report_generated']}).")

        # General Scenarios (CS-01 to CS-17)
        else:
            if actual_tier == expected_tier or (expected_tier == "TIER_3_COMPLIANCE_MANAGER" and actual_tier in ("TIER_3_COMPLIANCE_MANAGER", "TIER_4_CCO_BOARD")):
                verification_notes.append(f"PASS: Correctly escalated to {actual_tier}.")
            else:
                scenario_passed = False
                verification_notes.append(f"FAIL: Escalated to {actual_tier}, expected {expected_tier}.")

        # Log into cryptographic audit ledger
        leaf_hash = ledger.append_audit_event({
            "scenario_id": sid,
            "scenario_name": name,
            "actual_tier": actual_tier,
            "passed": scenario_passed,
            "latency_ms": round(elapsed_ms, 2),
        })

        # Record metric
        metrics.record_processing_event(
            latency_ms=elapsed_ms,
            alert_generated=(result["alerts_generated_count"] > 0),
            alert_suppressed=is_suppressed,
            sla_met=scenario_passed,
        )

        status_tag = "[PASS]" if scenario_passed else "[FAIL]"
        if scenario_passed:
            passed_scenarios += 1
        else:
            failed_scenarios += 1

        print(f"{status_tag} {sid}: {name:<45} | Tier: {actual_tier:<25} | Latency: {elapsed_ms:5.1f}ms")

        scenario_results[sid] = {
            "name": name,
            "expected_tier": expected_tier,
            "actual_tier": actual_tier,
            "passed": scenario_passed,
            "verification_notes": verification_notes,
            "latency_ms": round(elapsed_ms, 2),
            "merkle_leaf_hash": leaf_hash,
            "alerts_count": result["alerts_generated_count"],
            "consensus_metrics": result["consensus_metrics"],
            "report_generated": result["report_generated"],
            "report_id": result["report_id"],
        }

    # Finalize any uncommitted Merkle epoch block
    final_epoch = ledger.commit_epoch()
    is_valid_ledger, ledger_msg = ledger.verify_ledger_integrity()

    telemetry_summary = metrics.get_dashboard_summary()

    master_results = {
        "execution_timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "total_scenarios_tested": len(all_scenario_ids),
        "passed_count": passed_scenarios,
        "failed_count": failed_scenarios,
        "pass_rate_pct": round((passed_scenarios / len(all_scenario_ids)) * 100.0, 2),
        "cryptographic_ledger_integrity": {
            "verified": is_valid_ledger,
            "details": ledger_msg,
            "total_committed_epochs": len(ledger.committed_epochs),
            "latest_epoch_header": ledger.previous_epoch_hash,
        },
        "telemetry_metrics": telemetry_summary,
        "scenarios": scenario_results,
    }

    # Save to tests/scenarios/execution_results.json
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "scenarios", "execution_results.json"))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(master_results, f, indent=2)

    print("=" * 80)
    print(f"AUTOMATION SUMMARY: {passed_scenarios}/{len(all_scenario_ids)} Scenarios Passed ({master_results['pass_rate_pct']}%)")
    print(f"Merkle Ledger Status: {ledger_msg}")
    print(f"Results successfully saved to: {output_path}")
    print("=" * 80)

    return master_results


if __name__ == "__main__":
    results = run_all_scenarios()
    if results["failed_count"] > 0:
        sys.exit(1)
    sys.exit(0)
