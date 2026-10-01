"""Unit tests for Observability, Merkle Audit Ledger & Telemetry Metrics."""

import pytest
from src.observability.audit_ledger import MerkleAuditLedger
from src.observability.dashboard_metrics import DashboardMetricsCollector


def test_merkle_ledger_hash_chaining_and_verification():
    ledger = MerkleAuditLedger(epoch_block_size=3)

    # Append 7 events (creates 2 full epochs and leaves 1 uncommitted)
    for i in range(7):
        leaf_hash = ledger.append_audit_event({"event_index": i, "action": "SURVEILLANCE_FLAG"})
        assert len(leaf_hash) == 64

    assert len(ledger.committed_epochs) == 2

    # Commit remaining epoch
    ledger.commit_epoch()
    assert len(ledger.committed_epochs) == 3

    # Verify integrity
    is_valid, message = ledger.verify_ledger_integrity()
    assert is_valid is True
    assert "zero tampering" in message


def test_merkle_ledger_detects_tampering():
    ledger = MerkleAuditLedger(epoch_block_size=2)
    ledger.append_audit_event({"user": "Alice", "amount": 100})
    ledger.append_audit_event({"user": "Bob", "amount": 200})

    assert len(ledger.committed_epochs) == 1

    # Tamper with an event in the committed epoch
    ledger.committed_epochs[0]["leaf_hashes"][0] = "f" * 64

    is_valid, message = ledger.verify_ledger_integrity()
    assert is_valid is False
    assert "Tampered leaf detected" in message


def test_dashboard_metrics_percentiles():
    collector = DashboardMetricsCollector()
    # Add samples: 10, 20, 30, ... 100 ms
    for val in range(10, 110, 10):
        collector.record_processing_event(latency_ms=val, alert_generated=True, sla_met=True)

    percentiles = collector.get_latency_percentiles()
    assert percentiles["p50_ms"] == pytest.approx(50.0, 10.0)
    assert percentiles["p95_ms"] >= 90.0

    summary = collector.get_dashboard_summary()
    assert summary["panel_1_system_health"]["total_events_processed"] == 10
    assert summary["panel_2_compliance_effectiveness"]["sla_adherence_rate_pct"] == 100.0
