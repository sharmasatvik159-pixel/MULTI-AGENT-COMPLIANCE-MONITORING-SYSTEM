# Escalation Decision Tree: Off-Channel Communications & Recordkeeping
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Workflow Code:** `DT-OC-v1.0`  
**Target Scenarios:** CS-05, CS-08, CS-13  
**Governing Regulations:** SEC Rule 17a-4, Exchange Act Section 17(a), FINRA Rules 2210/3110, FCA SYSC 9  

---

## 1. Off-Channel Surveillance Workflow

```mermaid
flowchart TD
    Start(["CS-01 Ingests Corporate Communication Stream"]) --> ChannelScan{"Detection of Channel Migration Lexicon?<br/>('WhatsApp me', 'check personal email', 'Signal')"}

    ChannelScan -- NO --> ContentAudit["Standard Sentiment & Conduct Surveillance"]
    ChannelScan -- YES --> EntityCheck{"Registered Representative / Licensed Broker?<br/>(FINRA Series 7 / 24 Licensed Personnel)"}

    EntityCheck -- NO --> HR_Warning["HR General Policy Reminder<br/>No Formal Regulatory Escalation"]
    EntityCheck -- YES --> BusinessContext{"Is Communication Related to Securities Business?<br/>(Prices, quotes, recommendations, deal discussions)"}

    BusinessContext -- NO --> PersonalClear["Log Administrative Clearance<br/>SLA: Tier 1 (30 Minutes)"]
    BusinessContext -- YES --> ScaleEvaluation{"Individual Incident or Systematic Ring?<br/>(CS-13: 7+ Reps Coordinating)"}

    ScaleEvaluation -- "Single Isolated Representative" --> T2_Review["<b>ESCALATE TIER 2 (Senior Analyst)</b><br/>SLA: 15 Minutes<br/>Subpoena Personal Device Cloud Backups<br/>Issue Formal Written Compliance Warning"]
    
    ScaleEvaluation -- "Systemic / Multi-Broker Desk Ring" --> T3_Manager["<b>ESCALATE TIER 3 (Compliance Manager)</b><br/>SLA: 10 Minutes<br/>Suspend Messaging Permissions<br/>Initiate Comprehensive Supervisory Audit"]

    T3_Manager --> SEC_Exposure{"Substantial Unrecorded Trading Discussions Found?"}
    SEC_Exposure -- YES --> T4_CCO["<b>ESCALATE TIER 4 (CCO & Legal Counsel)</b><br/>SLA: 5 Minutes<br/>Assess Self-Reporting Obligations under SEC Sweep Precedents"]
    SEC_Exposure -- NO --> InternalRemediation["Remediation & Device Capture Quarantine"]
```

---

## 2. Detection Patterns & Remediation Standards
* **Evasion Patterns:** Detecting disguised phone numbers (e.g., spelled out digits "nine-one-seven...", QR codes shared via image attachments, links to ephemeral messaging apps).
* **Supervisory Enforcement:** In alignment with SEC and CFTC enforcement actions against major broker-dealers for WhatsApp recordkeeping failures, systematic unapproved messaging triggers immediate supervisory remediation, hardware confiscation for forensic imaging, and employee conduct recordation.
