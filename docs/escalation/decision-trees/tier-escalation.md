# Escalation Decision Trees & Routing Logic
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D4-DT-v1.0`  
**Classification:** Tier-2 Global Banking Architecture Specification  
**Author:** AI Systems Architect, Zetheta Algorithms  

---

## 1. Primary Escalation Decision Tree

This master decision tree governs how composite signals from the Consensus Engine are routed across human compliance tiers.

```mermaid
flowchart TD
    Start(["Consensus Engine Output"]) --> SanctionsCheck{"Is Sanctioned Entity / OFAC Hit?<br/>(CS-09, CS-20)"}
    
    SanctionsCheck -- YES --> T4_Immediate["<b>ESCALATE TIER 4 (CCO / Legal)</b><br/>Immediate Wire Hold / Intercept<br/>SLA: 15 Minutes"]
    
    SanctionsCheck -- NO --> LegalConflict{"Is Cross-Border Legal Conflict?<br/>(CS-19)"}
    LegalConflict -- YES --> T4_Immediate
    
    LegalConflict -- NO --> SeverityCheck{"Violation Severity Rating?"}
    
    SeverityCheck -- "CRITICAL (P1)" --> ConfCheckCrit{"Confidence Score?"}
    ConfCheckCrit -- "Score >= 0.80" --> T3_SAR["<b>ESCALATE TIER 3 (Compliance Manager)</b><br/>Direct SAR/STR Candidate Review<br/>SLA: 30 Minutes"]
    ConfCheckCrit -- "Score < 0.80" --> T2_Investigate["<b>ESCALATE TIER 2 (Senior Analyst)</b><br/>Multi-Agent Evidence Aggregation<br/>SLA: 2 Hours"]
    
    SeverityCheck -- "HIGH (P2)" --> WallCheck{"Information Barrier / Conduct Breach?<br/>(CS-05, CS-08, CS-16)"}
    WallCheck -- YES --> T2_Investigate
    WallCheck -- NO --> T2_Investigate
    
    SeverityCheck -- "MEDIUM (P3)" --> LimitCheck{"Passive Limit Breach or Active Intent?<br/>(CS-07, CS-12)"}
    LimitCheck -- "Passive / MTM Breach" --> T1_Review["<b>ESCALATE TIER 1 (Junior Analyst)</b><br/>Desk Notification & Remediation Plan<br/>SLA: 4 Hours"]
    LimitCheck -- "Active Intent Found" --> T2_Investigate

    SeverityCheck -- "LOW / FALSE POSITIVE" --> FP_Check{"Documented Pre-Clearance Exists?<br/>(CS-18)"}
    FP_Check -- YES --> Suppress["<b>SUPPRESS ALERT</b><br/>Log Verification in Audit Ledger<br/>Zero Escalation"]
    FP_Check -- NO --> T1_Review
```

---

## 2. Domain-Specific Escalation Subtrees

### 2.1 Sanctions & Anti-Money Laundering Subtree (CS-04, CS-09, CS-20)
```mermaid
flowchart TD
    AML_Start["AML / Sanctions Detection"] --> OFAC_Match{"Exact / Fuzzy SDN Match?"}
    
    OFAC_Match -- "Confidence > 0.85" --> Freeze["Place Immediate Transaction Hold"]
    Freeze --> T4_Notice["Alert CCO & AML Director (Tier 4)"]
    T4_Notice --> BlockReport["Prepare OFAC Blocking Report (10 Days)"]
    
    OFAC_Match -- "Confidence < 0.85" --> StructuringCheck{"Structuring Pattern Detected?<br/>(20+ txns below $10k)"}
    StructuringCheck -- YES --> T3_Review["Alert AML Officer (Tier 3)"]
    T3_Review --> SAR_Filing["Authorize FinCEN SAR Filing (30 Days)"]
    StructuringCheck -- NO --> T2_Review["Senior Analyst Review (Tier 2)"]
```

### 2.2 Market Abuse & Trading Conduct Subtree (CS-01, CS-02, CS-06, CS-10)
```mermaid
flowchart TD
    Trade_Start["Trading Anomaly Flagged"] --> OrderCancel{"High Order Cancellation Rate?<br/>(CME Rule 575 Spoofing)"}
    
    OrderCancel -- YES --> SpoofAlert["Calculate Order-to-Trade Ratio"]
    SpoofAlert --> AlgoHalt{"Ratio > 30:1 in 500ms?"}
    AlgoHalt -- YES --> T3_DeskHalt["Alert Manager (Tier 3) & Suspend Algorithmic Desk"]
    AlgoHalt -- NO --> T2_TradeInvestigate["Senior Trading Surveillance Review (Tier 2)"]
    
    OrderCancel -- NO --> InsiderCheck{"Pre-Announcement Position Accumulation?<br/>(SEC Rule 10b-5)"}
    InsiderCheck -- YES --> CorrelateChat{"CS-01 Finds Material Communication?"}
    CorrelateChat -- YES --> T3_DeskHalt
    CorrelateChat -- NO --> T2_TradeInvestigate
```
