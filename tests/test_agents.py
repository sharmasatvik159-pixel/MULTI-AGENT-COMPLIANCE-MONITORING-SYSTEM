"""Unit tests for individual autonomous compliance agents (TM, CS, RU, RG)."""

import pytest
from src.agents.communication_scanner import CommunicationScanner
from src.agents.regulatory_tracker import RegulatoryTracker
from src.agents.report_generator import ReportGenerator
from src.agents.transaction_monitor import TransactionMonitor


def test_transaction_monitor_spoofing():
    tm = TransactionMonitor()
    event = {
        "event_type": "ORDER_CANCEL",
        "payload": {
            "desk_id": "DESK_ALGO_01",
            "symbol": "CL_FUT_2026",
            "order_to_trade_ratio": 45.0,
            "cancellation_latency_ms": 250,
            "cancellations_count": 50,
        },
    }
    alert = tm.process_transaction(event)
    assert alert is not None
    assert alert["payload"]["violation_category"] == "MARKET_MANIPULATION_SPOOFING"
    assert alert["priority"] == 1
    assert alert["confidence_score"] > 0.80


def test_transaction_monitor_block_trade_suppression():
    tm = TransactionMonitor()
    tm.register_block_trade_exemption(
        ticket_id="TICKET-TEST-001",
        client_id="CLI_INST_99",
        symbol="ABC",
        notional_usd=200_000_000.0,
    )
    event = {
        "event_type": "TRADE_EXECUTION",
        "payload": {
            "client_id": "CLI_INST_99",
            "notional_usd": 200_000_000.0,
            "pct_adv": 7.5,
            "pre_clearance_ticket_id": "TICKET-TEST-001",
        },
    }
    alert = tm.process_transaction(event)
    assert alert is not None
    assert alert["payload"]["violation_category"] == "FALSE_POSITIVE_BLOCK_TRADE"
    assert alert["priority"] == 4  # LOW / Informational only


def test_communication_scanner_off_channel():
    cs = CommunicationScanner()
    record = {
        "channel": "BLOOMBERG_CHAT",
        "sender": "trader_dan@meridian.bank",
        "text": "Don't discuss quotes here, please WhatsApp me on +1-212-555-0144 immediately.",
    }
    alert = cs.ingest_communication(record)
    assert alert is not None
    assert alert["payload"]["violation_category"] == "OFF_CHANNEL_COMMUNICATION"
    assert alert["priority"] == 2


def test_communication_scanner_chinese_wall():
    cs = CommunicationScanner()
    record = {
        "channel": "SYMPHONY",
        "sender": "m_and_a_lead@meridian.bank",
        "recipient": "equity_analyst@meridian.bank",
        "text": "Confidential M&A deal code Project Apollo: Don't cover TargetCorp next week.",
    }
    alert = cs.ingest_communication(record)
    assert alert is not None
    assert alert["payload"]["violation_category"] == "CHINESE_WALL_BREACH"
    assert alert["priority"] == 1


def test_regulatory_tracker_sanctions_and_conflict():
    ru = RegulatoryTracker()
    # Check sanctions addition
    update = ru.process_regulatory_feed({
        "update_type": "SANCTIONS_UPDATE",
        "payload": {
            "entity_name": "RESTRICTED_SHIP_CORP",
            "sdn_id": "OFAC-SDN-5544",
            "subsidiaries": ["SHIP_SUB_A"],
        },
    })
    assert update is not None
    assert update["message_type"] == "UPDATE"

    # Test subsidiary matching
    match = ru.check_sanctions_match("SHIP_SUB_A")
    assert match is not None
    assert match["match_type"] == "INDIRECT_SUBSIDIARY"


def test_report_generator_sar_dual_sign_off():
    rg = ReportGenerator()
    report = rg.compile_regulatory_report(
        incident_id="INC-TEST-001",
        violation_category="INSIDER_TRADING",
        filing_type="FINCEN_SAR",
        evidence_dossier={
            "primary_entity_id": "TRD_INSIDER_01",
            "applicable_regulations": ["SEC Rule 10b-5"],
            "evidence_summary": "Traded ahead of corporate merger announcement.",
            "financial_impact_usd": 500000.0,
        },
        primary_officer_id="OFFICER_A",
        secondary_officer_id="DIRECTOR_B",
    )
    assert report["dual_sign_off_status"] == "VERIFIED"
    assert len(report["sign_offs"]) == 2
    assert "merkle_leaf_hash" in report
    assert report["merkle_leaf_hash"].startswith("sha256:")
    assert "SUSPICIOUS ACTIVITY REPORT NARRATIVE" in report["narrative_text"]
