"""Integration tests asserting 100% scenario compliance across CS-01 through CS-20."""

import pytest
from src.escalation.orchestrator import ComplianceOrchestrator
from src.generators.mock_stream import MockStreamGenerator


@pytest.fixture
def orchestrator():
    return ComplianceOrchestrator()


@pytest.fixture
def generator():
    return MockStreamGenerator()


def test_scenario_cs_18_block_trade_suppression(orchestrator, generator):
    """CS-18: Verify institutional block trade false positive is suppressed without escalation."""
    bundle = generator.get_scenario_event_bundle("CS-18")
    result = orchestrator.execute_scenario_pipeline(bundle)
    assert result["escalation"]["target_tier"] == "NONE"
    assert result["escalation"]["is_suppressed"] is True
    assert "SUPPRESSED_FALSE_POSITIVE" in result["escalation"]["action"]


def test_scenario_cs_19_cross_jurisdiction_conflict(orchestrator, generator):
    """CS-19: Verify EMIR vs MAS cross-border conflict escalates to Tier 4 CCO/Legal."""
    bundle = generator.get_scenario_event_bundle("CS-19")
    result = orchestrator.execute_scenario_pipeline(bundle)
    assert result["escalation"]["target_tier"] == "TIER_4_CCO_BOARD"
    assert "SOVEREIGN_CONFLICT" in result["escalation"]["action"]


def test_scenario_cs_20_coordinated_tbml(orchestrator, generator):
    """CS-20: Verify coordinated trade finance money laundering invokes all agents and compiles SAR."""
    bundle = generator.get_scenario_event_bundle("CS-20")
    result = orchestrator.execute_scenario_pipeline(bundle)
    assert result["escalation"]["target_tier"] == "TIER_4_CCO_BOARD"
    assert result["report_generated"] is True
    assert result["report_id"] is not None
    assert result["merkle_seal"].startswith("sha256:")


@pytest.mark.parametrize("sid,expected_tier", [
    ("CS-01", "TIER_3_COMPLIANCE_MANAGER"),
    ("CS-02", "TIER_3_COMPLIANCE_MANAGER"),
    ("CS-03", "TIER_2_SENIOR_ANALYST"),
    ("CS-04", "TIER_3_COMPLIANCE_MANAGER"),
    ("CS-05", "TIER_3_COMPLIANCE_MANAGER"),
    ("CS-06", "TIER_2_SENIOR_ANALYST"),
    ("CS-07", "TIER_1_ANALYST"),
    ("CS-08", "TIER_2_SENIOR_ANALYST"),
    ("CS-09", "TIER_4_CCO_BOARD"),
    ("CS-10", "TIER_3_COMPLIANCE_MANAGER"),
    ("CS-11", "TIER_3_COMPLIANCE_MANAGER"),
    ("CS-12", "TIER_1_ANALYST"),
    ("CS-13", "TIER_2_SENIOR_ANALYST"),
    ("CS-14", "TIER_3_COMPLIANCE_MANAGER"),
    ("CS-15", "TIER_2_SENIOR_ANALYST"),
    ("CS-16", "TIER_3_COMPLIANCE_MANAGER"),
    ("CS-17", "TIER_3_COMPLIANCE_MANAGER"),
])
def test_all_standard_scenarios(orchestrator, generator, sid, expected_tier):
    bundle = generator.get_scenario_event_bundle(sid)
    result = orchestrator.execute_scenario_pipeline(bundle)
    assert result["escalation"]["target_tier"] == expected_tier
    assert result["status"] == "COMPLETED"
