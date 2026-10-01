"""Unit tests for Dempster-Shafer Consensus & Mathematical Evidence Fusion."""

import pytest
from src.consensus.dempster_shafer import DempsterShaferConsensus


def test_confidence_calibration():
    consensus = DempsterShaferConsensus()
    # Test mass function generation
    m = consensus.create_mass_function(calibrated_confidence=0.85, noise_epsilon=0.10)
    assert m["V"] == pytest.approx(0.765, 0.001)
    assert m["not_V"] == pytest.approx(0.135, 0.001)
    assert m["Theta"] == pytest.approx(0.10, 0.001)
    assert sum(m.values()) == pytest.approx(1.0, 0.001)


def test_dempster_orthogonal_sum_low_conflict():
    consensus = DempsterShaferConsensus()
    m1 = consensus.create_mass_function(0.85, noise_epsilon=0.10)  # V: 0.765
    m2 = consensus.create_mass_function(0.80, noise_epsilon=0.10)  # V: 0.720

    combined, k, method = consensus.combine_two_masses(m1, m2)
    assert k < 0.65
    assert method == "DEMPSTER_ORTHOGONAL_SUM"
    assert combined["V"] > 0.85  # Reinforcing evidence increases conviction
    assert sum(combined.values()) == pytest.approx(1.0, 0.001)


def test_yager_fallback_elevated_conflict():
    consensus = DempsterShaferConsensus()
    # Strong contradiction
    m1 = {"V": 0.80, "not_V": 0.10, "Theta": 0.10}
    m2 = {"V": 0.10, "not_V": 0.80, "Theta": 0.10}

    combined, k, method = consensus.combine_two_masses(m1, m2)
    # k = (0.80 * 0.80) + (0.10 * 0.10) = 0.64 + 0.01 = 0.65
    assert k >= 0.65
    assert method == "YAGER_MODIFIED_COMBINATION"
    # Under Yager, conflicting mass is reallocated to Theta
    assert combined["Theta"] >= k


def test_multi_agent_combination():
    consensus = DempsterShaferConsensus()
    m_tm = consensus.create_mass_function(0.90, noise_epsilon=0.08)
    m_cs = consensus.create_mass_function(0.85, noise_epsilon=0.12)
    m_ru = consensus.create_mass_function(0.95, noise_epsilon=0.04)

    result = consensus.combine_multiple_agents([m_tm, m_cs, m_ru])
    assert result["belief_violation"] > 0.90
    assert result["conflict_k"] < 0.65
    assert result["method"] == "DEMPSTER_ORTHOGONAL_SUM"
