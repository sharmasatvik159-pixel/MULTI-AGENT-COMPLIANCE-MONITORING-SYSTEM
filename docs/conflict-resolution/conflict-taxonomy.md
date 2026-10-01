# Inter-Agent Conflict Taxonomy & Tie-Breaking Rules
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D3-CT-v1.0`  
**Classification:** Tier-2 Global Banking Architecture Specification  
**Author:** AI Systems Architect, Zetheta Algorithms  

---

## 1. Conflict Classification Taxonomy

When independent autonomous agents operate over multifaceted banking datasets, disagreements inevitably arise. The system categorizes inter-agent conflict into five distinct taxonomies:

```
+---------------------------------------------------------------------------------------------------+
| CONFLICT CATEGORY          | PRIMARY AGENTS INVOLVED  | ROOT CAUSE                         | RISK |
+---------------------------------------------------------------------------------------------------+
| 1. Factual Discrepancy     | TM-01 vs CS-01           | Inconsistent timestamps or IDs     | High |
| 2. Semantic Interpretation | CS-01 vs TM-01           | Contextual ambiguity in chatter    | Med  |
| 3. Cross-Jurisdictional    | RU-01 vs Global Units    | Contradictory national laws        | Crit |
| 4. Temporal Horizon        | TM-01 vs TM-01 (Models)  | Microsecond burst vs 90d baseline  | Med  |
| 5. Regulatory Ambiguity    | RU-01 vs System Policies | Unclear circular guidance          | High |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Taxonomy Analysis & Tie-Breaking Resolution Rules

### 2.1 Category 1: Factual Discrepancy (Timestamp / Entity Mismatch)
* **Description:** An agent’s structured event logs directly contradict another agent’s timeline.
* **Archetype Scenario (CS-14: Late Trading):** OMS logs state mutual fund orders arrived at 16:00:00 ET, but CS-01 communication captures show trader entered orders via terminal at 16:18 ET.
* **Tie-Breaking Rule:** **Physical Immutable Clock Precedence (PTP/GPS).** Application-level user timestamps are superseded by low-level network packet capture (PCAP) and database journal commit timestamps. The factual contradiction itself is tagged as an *independent indicator of deception* and escalated to Tier 3.

### 2.2 Category 2: Semantic Interpretation Conflict
* **Description:** `TM-01` flags a transaction as suspicious market abuse, while `CS-01` finds written communication suggesting legitimate business intent, or vice versa.
* **Archetype Scenario (CS-18: False Positive Block Trade):** `TM-01` detects an 8% ADV volume surge ($450M), but `CS-01` finds pre-trade client authorization and compliance pre-clearance tickets.
* **Tie-Breaking Rule:** **Formal Compliance Exemption Supremacy.** If documented proof of pre-clearance exists within sanctioned compliance ticketing repositories, `CS-01` evidence suppresses `TM-01` alerts, provided $K < 0.20$.

### 2.3 Category 3: Cross-Jurisdictional Regulatory Conflict
* **Description:** Compliance with one sovereign regulator requires action that directly violates the penal or privacy laws of another jurisdiction.
* **Archetype Scenario (CS-19: Multi-Jurisdiction Conflict):** EU EMIR mandates reporting of all OTC derivative details within 1 business day. Simultaneously, Singapore MAS regulations and bank secrecy laws prohibit cross-border sharing of client derivative positions without judicial waiver.
* **Tie-Breaking Rule:** **Strict Local Law Paramountcy & Immediate Legal Escalation.** The system forbids autonomous resolution of cross-border legal sovereignty conflicts. The transaction is placed in administrative escrow, and an emergency dossier is routed directly to General Counsel and Tier 4 (CCO).

### 2.4 Category 4: Temporal Horizon Conflict
* **Description:** An agent evaluates a trade as anomalous within a 5-minute sliding window, but benign within a 60-day historical macro trend.
* **Tie-Breaking Rule:** **Precautionary Escalation Principle.** If an immediate threshold breach creates severe market liability (e.g., crossing a 25% sector concentration cap in CS-12), the short-term violation triggers an interim warning while the long-term context is attached as mitigating commentary.

---

## 3. Conflict Resolution Audit Trail Specification

Every detected inter-agent disagreement generates an immutable **Conflict Record** in the PostgreSQL audit schema:

```json
{
  "conflict_id": "cnf-9021-ba81",
  "timestamp": "2026-10-01T14:22:10.891Z",
  "taxonomy_category": "CROSS_JURISDICTIONAL",
  "involved_agents": ["RU-01", "TM-01"],
  "conflict_metric_k": 0.88,
  "agent_positions": {
    "TM-01": {"recommendation": "EXECUTE_EMIR_DISCLOSURE", "confidence": 0.92},
    "RU-01": {"recommendation": "HALT_DUE_TO_MAS_SECRECY", "confidence": 0.95}
  },
  "applied_rule": "STRICT_LOCAL_SOVEREIGNTY_ESCALATE_TIER_4",
  "resolution_status": "ESCALATED_TO_LEGAL_COUNSEL",
  "dossier_hash": "sha256:4a7e93f...b891"
}
```
