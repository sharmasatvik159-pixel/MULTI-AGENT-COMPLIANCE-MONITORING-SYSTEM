"""Dempster-Shafer Mathematical Consensus & Evidence Fusion Engine.

Implements Dempster-Shafer Theory of Evidence, Basic Belief Assignment (BBA),
conflict metric (K) computation, Yager modified combination fallback,
and Bayesian belief calibration.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


class DempsterShaferConsensus:
    """Mathematical consensus engine for multi-agent evidence fusion."""

    def __init__(self, conflict_threshold_yager: float = 0.65, conflict_threshold_halt: float = 0.85):
        self.conflict_threshold_yager = conflict_threshold_yager
        self.conflict_threshold_halt = conflict_threshold_halt

    def create_mass_function(self, calibrated_confidence: float, noise_epsilon: float = 0.10) -> Dict[str, float]:
        """Convert calibrated confidence score into Basic Belief Assignment (BBA) mass function.

        Focal elements:
        - 'V': Violation proposition
        - 'not_V': Benign proposition
        - 'Theta': Uncommitted epistemic uncertainty {V, not_V}
        """
        c = max(0.0, min(1.0, calibrated_confidence))
        eps = max(0.01, min(0.30, noise_epsilon))

        m_v = c * (1.0 - eps)
        m_not_v = (1.0 - c) * (1.0 - eps)
        m_theta = eps

        return {
            "V": round(m_v, 6),
            "not_V": round(m_not_v, 6),
            "Theta": round(m_theta, 6),
        }

    def combine_two_masses(self, m1: Dict[str, float], m2: Dict[str, float]) -> Tuple[Dict[str, float], float, str]:
        """Compute the orthogonal sum m1,2 = m1 ⊕ m2 and conflict metric K.

        Returns:
            Tuple of (combined_mass, conflict_k, combination_method)
        """
        # Calculate cross-products
        # Intersections:
        # V ∩ V = V
        # V ∩ not_V = empty (conflict)
        # V ∩ Theta = V
        # not_V ∩ V = empty (conflict)
        # not_V ∩ not_V = not_V
        # not_V ∩ Theta = not_V
        # Theta ∩ V = V
        # Theta ∩ not_V = not_V
        # Theta ∩ Theta = Theta

        v_prod = (m1["V"] * m2["V"]) + (m1["V"] * m2["Theta"]) + (m1["Theta"] * m2["V"])
        not_v_prod = (m1["not_V"] * m2["not_V"]) + (m1["not_V"] * m2["Theta"]) + (m1["Theta"] * m2["not_V"])
        theta_prod = m1["Theta"] * m2["Theta"]
        conflict_k = (m1["V"] * m2["not_V"]) + (m1["not_V"] * m2["V"])

        # Check for deadlock
        if conflict_k >= self.conflict_threshold_halt:
            # Zadeh's Paradox Deadlock: Return uncombined with deadlock tag
            return (
                {"V": (m1["V"] + m2["V"]) / 2, "not_V": (m1["not_V"] + m2["not_V"]) / 2, "Theta": 1.0 - ((m1["V"] + m2["V"]) / 2 + (m1["not_V"] + m2["not_V"]) / 2)},
                round(conflict_k, 6),
                "DEADLOCK_HALT_ARBITER_REQUIRED",
            )

        # Check for elevated conflict: Yager's Modified Rule
        if conflict_k >= self.conflict_threshold_yager:
            # Reallocate conflicting mass K to Theta (uncertainty) without dividing by 1-K
            m_combined = {
                "V": round(v_prod, 6),
                "not_V": round(not_v_prod, 6),
                "Theta": round(theta_prod + conflict_k, 6),
            }
            return m_combined, round(conflict_k, 6), "YAGER_MODIFIED_COMBINATION"

        # Standard Dempster's Rule of Combination
        denom = 1.0 - conflict_k
        if denom <= 0:
            denom = 0.0001

        m_combined = {
            "V": round(v_prod / denom, 6),
            "not_V": round(not_v_prod / denom, 6),
            "Theta": round(theta_prod / denom, 6),
        }
        return m_combined, round(conflict_k, 6), "DEMPSTER_ORTHOGONAL_SUM"

    def combine_multiple_agents(self, agent_masses: List[Dict[str, float]]) -> Dict[str, Any]:
        """Sequentially combine evidence from 2 or more agents."""
        if not agent_masses:
            return {"combined_mass": {"V": 0.0, "not_V": 1.0, "Theta": 0.0}, "conflict_k": 0.0, "method": "NO_EVIDENCE"}

        if len(agent_masses) == 1:
            return {
                "combined_mass": agent_masses[0],
                "conflict_k": 0.0,
                "belief_violation": agent_masses[0]["V"],
                "plausibility_violation": agent_masses[0]["V"] + agent_masses[0]["Theta"],
                "method": "SINGLE_AGENT_DIRECT",
            }

        current_mass = agent_masses[0]
        max_conflict = 0.0
        applied_method = "DEMPSTER_ORTHOGONAL_SUM"

        for m_next in agent_masses[1:]:
            current_mass, k, method = self.combine_two_masses(current_mass, m_next)
            max_conflict = max(max_conflict, k)
            if "DEADLOCK" in method or "YAGER" in method:
                applied_method = method

        bel_v = current_mass["V"]
        pl_v = current_mass["V"] + current_mass["Theta"]

        return {
            "combined_mass": current_mass,
            "conflict_k": max_conflict,
            "belief_violation": round(bel_v, 4),
            "plausibility_violation": round(pl_v, 4),
            "method": applied_method,
        }
