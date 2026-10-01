"""Schema validation tests ensuring agent envelopes comply with message-schema.json."""

import json
import os
import jsonschema
import pytest

from src.agents.communication_scanner import CommunicationScanner
from src.agents.transaction_monitor import TransactionMonitor


@pytest.fixture
def message_schema():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "docs", "protocols", "message-schema.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_schema_validity(message_schema):
    """Ensure message-schema.json itself is a valid Draft 2020-12 schema."""
    jsonschema.Draft202012Validator.check_schema(message_schema)


def test_tm_alert_conforms_to_schema(message_schema):
    tm = TransactionMonitor()
    alert = tm.process_transaction({
        "event_type": "ORDER_CANCEL",
        "payload": {
            "desk_id": "DESK_ALGO_01",
            "symbol": "CL_FUT_2026",
            "order_to_trade_ratio": 40.0,
            "cancellation_latency_ms": 200,
            "cancellations_count": 35,
        },
    })
    assert alert is not None
    # Validate against schema
    validator = jsonschema.Draft202012Validator(message_schema)
    validator.validate(alert)


def test_cs_alert_conforms_to_schema(message_schema):
    cs = CommunicationScanner()
    alert = cs.ingest_communication({
        "channel": "BLOOMBERG_CHAT",
        "sender": "trader_a@meridian.bank",
        "text": "WhatsApp me right now on +1-212-555-0100 for trade details.",
    })
    assert alert is not None
    validator = jsonschema.Draft202012Validator(message_schema)
    validator.validate(alert)
