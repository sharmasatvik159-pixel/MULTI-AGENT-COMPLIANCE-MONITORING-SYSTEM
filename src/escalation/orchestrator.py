"""Multi-Agent Compliance Orchestration & Escalation Engine.

Implements the 4-Tier Human-in-the-Loop state machine, coordinating TM-01, CS-01,
RU-01, and RG-01 with mathematical consensus evaluation, false-positive suppression,
and statutory filing dispatch.
"""

from __future__ import annotations

import datetime
import uuid
from typing import Any, Dict, List, Optional

from src.agents.communication_scanner import CommunicationScanner
from src.agents.regulatory_tracker import RegulatoryTracker
from src.agents.report_generator import ReportGenerator
from src.agents.transaction_monitor import TransactionMonitor
from src.consensus.dempster_shafer import DempsterShaferConsensus


class ComplianceOrchestrator:
    """Central orchestrator managing multi-agent investigations, consensus, and tiered escalation."""

    def __init__(self):
        self.tm = TransactionMonitor()
        self.cs = CommunicationScanner()
        self.ru = RegulatoryTracker()
        self.rg = ReportGenerator()
        self.consensus = DempsterShaferConsensus()

        # Register known institutional block trade pre-clearance (CS-18)
        self.tm.register_block_trade_exemption(
            ticket_id="TICKET-BLK-2026-9021",
            client_id="INSTITUTIONAL_PENSION_01",
            symbol="INSTITUTIONAL_BLOCK_EQ",
            notional_usd=450_000_000.0,
        )

        self.incident_records: Dict[str, Dict[str, Any]] = {}

    def execute_scenario_pipeline(self, scenario_bundle: Dict[str, Any]) -> Dict[str, Any]:
        """Execute full surveillance pipeline for a scenario package:

        Data Ingestion -> Agent Surveillance -> Consensus Resolution ->
        HITL Escalation / Suppression -> Report Compilation -> Audit Record.
        """
        scenario_name = scenario_bundle.get("name", "Unknown Scenario")
        events = scenario_bundle.get("events", [])
        correlation_id = str(uuid.uuid4())
        trace_id = str(uuid.uuid4())

        collected_alerts: List[Dict[str, Any]] = []
        agent_masses: List[Dict[str, float]] = []

        # 1. Ingest all scenario events across agents
        for event in events:
            source = event.get("source")

            if source == "TRANSACTION":
                alert = self.tm.process_transaction(event)
                if alert:
                    collected_alerts.append(alert)
                    conf = alert.get("confidence_score", 0.5)
                    agent_masses.append(self.consensus.create_mass_function(conf, self.tm.epistemic_noise))

            elif source == "COMMUNICATION":
                alert = self.cs.ingest_communication(event)
                if alert:
                    collected_alerts.append(alert)
                    conf = alert.get("confidence_score", 0.5)
                    agent_masses.append(self.consensus.create_mass_function(conf, self.cs.epistemic_noise))

            elif source == "REGULATORY":
                update_envelope = self.ru.process_regulatory_feed(event)
                if update_envelope:
                    collected_alerts.append(update_envelope)
                    conf = update_envelope.get("confidence_score", 0.95)
                    agent_masses.append(self.consensus.create_mass_function(conf, self.ru.epistemic_noise))

        # Check for cross-agent correlation queries
        # If TM flagged transaction, query CS for trader communication context
        for alert in collected_alerts:
            if alert.get("sender_agent_id") == "TM-01" and alert.get("payload", {}).get("violation_category") in (
                "INSIDER_TRADING",
                "MARKET_MANIPULATION_SPOOFING",
            ):
                query_env = {
                    "sender_agent_id": "ORCHESTRATOR-01",
                    "priority": 1,
                    "correlation_id": correlation_id,
                    "trace_id": trace_id,
                    "payload": {
                        "query_id": str(uuid.uuid4()),
                        "query_type": "TRADER_COMMUNICATIONS",
                        "target_subject_id": alert.get("payload", {}).get("primary_entity_id", ""),
                        "time_window": {"start_time": "2026-09-01T00:00:00Z", "end_time": "2026-09-30T00:00:00Z"},
                        "filter_keywords": ["dinner", "meeting", "acquisition", "cover"],
                    },
                }
                cs_response = self.cs.handle_query(query_env)
                corroboration = cs_response.get("confidence_score", 0.0)
                if corroboration > 0.5:
                    agent_masses.append(self.consensus.create_mass_function(corroboration, self.cs.epistemic_noise))

        # Check for sanctions cross-check with RU-01
        for alert in collected_alerts:
            beneficiary = alert.get("payload", {}).get("quantitative_metrics", {}).get("beneficiary_name") or alert.get("payload", {}).get("primary_entity_id")
            if beneficiary:
                match = self.ru.check_sanctions_match(str(beneficiary))
                if match:
                    agent_masses.append(self.consensus.create_mass_function(0.99, self.ru.epistemic_noise))

        # 2. Consensus Fusion Evaluation
        consensus_result = self.consensus.combine_multiple_agents(agent_masses)
        composite_belief = consensus_result.get("belief_violation", 0.0)
        conflict_k = consensus_result.get("conflict_k", 0.0)

        # 3. Determine Escalation Tier & Outcome
        escalation_decision = self._classify_escalation(collected_alerts, composite_belief, conflict_k)

        # 4. Report Compilation (if escalated to Tier 3 or Tier 4)
        report_artifact = None
        if escalation_decision["target_tier"] in ("TIER_3_COMPLIANCE_MANAGER", "TIER_4_CCO_BOARD"):
            primary_alert = collected_alerts[0] if collected_alerts else {}
            payload_data = primary_alert.get("payload", {})
            report_artifact = self.rg.compile_regulatory_report(
                incident_id=f"INC-{uuid.uuid4().hex[:8].upper()}",
                violation_category=payload_data.get("violation_category", "SUSPICIOUS_ACTIVITY"),
                filing_type="FINCEN_SAR" if escalation_decision["target_tier"] == "TIER_3_COMPLIANCE_MANAGER" else "OFAC_BLOCK_OR_BOARD_DISCLOSURE",
                evidence_dossier={
                    "primary_entity_id": payload_data.get("primary_entity_id", "UNKNOWN"),
                    "applicable_regulations": payload_data.get("applicable_regulations", ["Federal Banking Regulations"]),
                    "evidence_summary": payload_data.get("evidence_summary", "Multi-agent surveillance detection."),
                    "financial_impact_usd": 1500000.0,
                    "jurisdiction": "US",
                },
                primary_officer_id="OFFICER_PRIMARY_TIER3",
                secondary_officer_id="DIRECTOR_CCO_TIER4" if escalation_decision["target_tier"] == "TIER_4_CCO_BOARD" else None,
            )

        result_summary = {
            "scenario_name": scenario_name,
            "correlation_id": correlation_id,
            "trace_id": trace_id,
            "alerts_generated_count": len(collected_alerts),
            "consensus_metrics": {
                "composite_belief_violation": composite_belief,
                "conflict_k": conflict_k,
                "combination_method": consensus_result.get("method"),
            },
            "escalation": escalation_decision,
            "report_generated": report_artifact is not None,
            "report_id": report_artifact.get("report_id") if report_artifact else None,
            "merkle_seal": report_artifact.get("merkle_leaf_hash") if report_artifact else None,
            "status": "COMPLETED",
        }

        self.incident_records[correlation_id] = result_summary
        return result_summary

    def _classify_escalation(
        self,
        alerts: List[Dict[str, Any]],
        composite_belief: float,
        conflict_k: float,
    ) -> Dict[str, Any]:
        """Classify target human escalation tier and SLA countdown."""
        if not alerts:
            return {
                "target_tier": "NONE",
                "action": "NO_ALERT_GENERATED",
                "sla_minutes": 0,
                "is_suppressed": True,
            }

        # Check for False Positive Block Trade (CS-18)
        for a in alerts:
            if a.get("payload", {}).get("violation_category") == "FALSE_POSITIVE_BLOCK_TRADE":
                return {
                    "target_tier": "NONE",
                    "action": "SUPPRESSED_FALSE_POSITIVE_EXEMPTION",
                    "sla_minutes": 0,
                    "is_suppressed": True,
                    "reasoning": "Documented institutional block trade pre-clearance verified. Zero human escalation.",
                }

        # Check for Tier 4: Sovereign Conflicts, Sanctions & TBML (CS-19, CS-09, CS-20)
        for a in alerts:
            cat = a.get("payload", {}).get("violation_category", "")
            if cat == "MULTI_JURISDICTION_CONFLICT":
                return {
                    "target_tier": "TIER_4_CCO_BOARD",
                    "action": "ESCALATE_GENERAL_COUNSEL_SOVEREIGN_CONFLICT",
                    "sla_minutes": 5,
                    "is_suppressed": False,
                    "reasoning": "Extraterritorial regulatory conflict requires immediate General Counsel & Board resolution.",
                }
            if "SANCTIONS" in cat or cat == "TRADE_BASED_MONEY_LAUNDERING":
                return {
                    "target_tier": "TIER_4_CCO_BOARD",
                    "action": "IMMEDIATE_WIRE_HOLD_AND_BOARD_ALERT",
                    "sla_minutes": 5,
                    "is_suppressed": False,
                    "reasoning": "OFAC / Financial Crime risk mandates sub-5 minute immediate executive intervention.",
                }

        # Check for Tier 1: Passive Limit Breach & Margin Rules (CS-07, CS-12)
        for a in alerts:
            cat = a.get("payload", {}).get("violation_category", "")
            if cat in ("REGULATORY_CHANGE_IMPACT", "CONCENTRATION_RISK_LIMIT"):
                return {
                    "target_tier": "TIER_1_ANALYST",
                    "action": "ROUTINE_TRIAGE_AND_LIMIT_REMEDITATION",
                    "sla_minutes": 30,
                    "is_suppressed": False,
                    "reasoning": "Passive limit breach or low-severity anomaly assigned to Tier 1 triage.",
                }

        # Check for Tier 2: Senior Analyst Scope (CS-03, CS-06, CS-08, CS-13, CS-15)
        for a in alerts:
            cat = a.get("payload", {}).get("violation_category", "")
            if cat in (
                "UNSUITABLE_RECOMMENDATION",
                "MARKET_MANIPULATION_WASH_TRADING",
                "MISLEADING_MARKETING",
                "OFF_CHANNEL_COMMUNICATION",
                "BEST_EXECUTION_FAILURE",
            ):
                return {
                    "target_tier": "TIER_2_SENIOR_ANALYST",
                    "action": "SENIOR_ANALYST_INVESTIGATION_AND_INTERVIEW",
                    "sla_minutes": 15,
                    "is_suppressed": False,
                    "reasoning": f"Conduct risk or execution pattern ({cat}) requires Tier 2 investigation.",
                }

        # Tier 3: Critical Violations (CS-01, CS-02, CS-04, CS-05, CS-10, CS-11, CS-14, CS-16, CS-17)
        return {
            "target_tier": "TIER_3_COMPLIANCE_MANAGER",
            "action": "AUTHORIZE_SAR_STR_AND_CONDUCT_REVIEW",
            "sla_minutes": 10,
            "is_suppressed": False,
            "reasoning": f"Critical statutory violation ({composite_belief:.2f} conviction) triggers Tier 3 Compliance Manager review.",
        }
