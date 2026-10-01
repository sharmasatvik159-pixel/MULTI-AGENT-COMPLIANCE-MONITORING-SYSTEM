# Escalation Decision Tree: Sanctions Violations & Counterparty Screening
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Workflow Code:** `DT-SV-v1.0`  
**Target Scenarios:** CS-09, CS-20  
**Governing Regulations:** OFAC Regulations (31 CFR Part 501), EU Financial Sanctions, UK OFSI Directives, UN Security Council Resolutions  

---

## 1. Sanctions Screening & Escalation Workflow

```mermaid
flowchart TD
    Start(["Wire Transfer / Payment Instruction Ingested"]) --> SanctionsFilter{"RU-01 Global Watchlist Ingestion Check<br/>(OFAC SDN, EU, UK OFSI Lists)"}

    SanctionsFilter --> MatchType{"Screening Match Level?"}

    MatchType -- "Direct Exact Match (SDN Listed Entity)" --> T4_InstantFreeze["<b>ESCALATE TIER 4 (CCO / General Counsel)</b><br/>SLA: 5 Minutes (IMMEDIATE)<br/>Automated Wire Intercept & Block<br/>Notify OFAC Sanctions Liaison"]
    
    MatchType -- "Indirect 50% Rule / Subsidiary Exposure (CS-09)" --> IndirectCheck{"Beneficiary Owned >= 50% by SDN?<br/>(OFAC 50 Percent Rule)"}
    
    IndirectCheck -- YES --> T4_InstantFreeze
    IndirectCheck -- UNCONFIRMED --> T3_Escrow["<b>ESCALATE TIER 3 (Compliance Manager / MLRO)</b><br/>SLA: 10 Minutes<br/>Place Funds in Administrative Escrow<br/>Trigger Enhanced Due Diligence (EDD)"]

    MatchType -- "Fuzzy Name / Acoustic Match (>0.85)" --> PEP_Check{"Politically Exposed Person (PEP) or Sanctions False Match?"}
    PEP_Check -- "False Positive (Different DOB/Country)" --> Tier1_Clear["Tier 1 Analyst Clearance<br/>SLA: 30 Minutes<br/>Document Passport/ID Verification"]
    PEP_Check -- "Potential Real Match" --> T2_SeniorReview["Tier 2 Senior Analyst Review<br/>SLA: 15 Minutes<br/>Request Source of Wealth Documentation"]

    MatchType -- "No Match Detected" --> ReleasePayment["Release Payment for Downstream Processing"]

    T4_InstantFreeze --> BlockReporting["Report Generator (RG-01)<br/>File Form TD-F 90-22.50 (OFAC Blocked Property)<br/>Submit Within 10 Business Days"]
```

---

## 2. Hard Execution Mandates
* **Zero-Tolerance Wire Intercept:** Any direct OFAC SDN hit results in an automated microsecond wire hold prior to execution across SWIFT or Fedwire rails.
* **OFAC 50% Rule Evaluation:** `RU-01` corporate hierarchy graph recursively traverses subsidiary ownership stakes up to 4 corporate parent tiers to flag indirect ownership exposure exceeding statutory thresholds.
* **Reporting SLA:** Official OFAC Report of Blocked Property must be generated and filed by `RG-01` within **10 business days** under 31 CFR § 501.603.
