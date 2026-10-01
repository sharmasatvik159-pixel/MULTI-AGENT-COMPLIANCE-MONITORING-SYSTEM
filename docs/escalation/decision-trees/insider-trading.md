# Escalation Decision Tree: Insider Trading Surveillance
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Workflow Code:** `DT-IT-v1.0`  
**Target Scenarios:** CS-01, CS-10, CS-16  
**Governing Regulations:** SEC Rule 10b-5, FINRA Rules 2010/5270, Insider Trading Sanctions Act (ITSA), SEBI PIT Regulations  

---

## 1. Insider Trading Workflow Decision Tree

```mermaid
flowchart TD
    Start(["Unusual Trading Activity Detected by TM-01"]) --> VolCheck{"Abnormal Position Accumulation?<br/>(Volume > 3x ADV over 30 days)"}

    VolCheck -- NO --> LogBenign["Log in Baseline Surveillance Cache<br/>No Escalation"]
    VolCheck -- YES --> EventCorrelation{"Corporate Event Announced within 14 Days?<br/>(Acquisition / Earnings / Restructuring)"}

    EventCorrelation -- NO --> FrontRunCheck{"Is Trade Executed 10–30m Prior to Large Client Order?<br/>(CS-10: Front-Running)"}
    FrontRunCheck -- YES --> T3_FrontRun["<b>ESCALATE TIER 3 (Compliance Manager)</b><br/>SLA: 10 Minutes<br/>Freeze Personal Account Trading<br/>Refer to Prop Trading Oversight"]
    FrontRunCheck -- NO --> DeskReview["Route to Tier 1 (Analyst)<br/>SLA: 30 Minutes for 90d Baseline Review"]

    EventCorrelation -- YES --> QueryCS["Dispatch Synchronous RPC to CS-01<br/>Target: Employee Communications & Meetings"]
    
    QueryCS --> ChatAnalysis{"CS-01 Finds Material Non-Public Info (MNPI) Clues?<br/>(Dinner meeting with CFO, deal code words)"}

    ChatAnalysis -- "Confidence >= 0.80" --> T3_Critical["<b>ESCALATE TIER 3 (Compliance Manager)</b><br/>SLA: 10 Minutes<br/>Compile Evidence Dossier<br/>Draft FinCEN SAR & Freeze Trading Account"]
    
    ChatAnalysis -- "Confidence 0.40–0.79" --> T2_Investigate["<b>ESCALATE TIER 2 (Senior Analyst)</b><br/>SLA: 15 Minutes<br/>Interview Trading Desk Supervisor<br/>Pull External Phone & Visitor Logs"]
    
    ChatAnalysis -- "Confidence < 0.40" --> PreClearCheck{"Was Trade Executed Under Valid 10b5-1 Plan?"}
    PreClearCheck -- YES --> ExemptionSuppress["<b>SUPPRESS ALERT (Documented Exemption)</b><br/>Verify 10b5-1 Cooling-Off Period (90 Days)<br/>Log Verification in Audit Ledger"]
    PreClearCheck -- NO --> T2_Investigate

    T3_Critical --> SAR_Filing{"Compliance Manager Approves SAR?"}
    SAR_Filing -- YES --> RG_SAR["Report Generator (RG-01)<br/>Compile FinCEN SAR XML & FIU-IND STR<br/>Submit within 30-Day Window"]
    SAR_Filing -- OVERRIDE --> FourEyes["Require Four-Eyes Countersignature<br/>Mandatory 50-Word Statutory Justification"]
```

---

## 2. Quantitative Thresholds & Decision Criteria
1. **Abnormal Volume Surge:** Cumulative position buildup exceeds $300\%$ of the account's historical 90-day moving average.
2. **Abnormal Return Trigger:** Price appreciation exceeding $\ge 15\%$ within 72 hours of public announcement.
3. **Communication Corroboration:** Semantic NLP intent score $\ge 0.75$ on private meetings, informal dinners, or non-public earnings previews.
4. **Action Protocols:** Mandatory freeze of personal trading accounts upon Tier 3 confirmation; SAR narrative compilation triggered automatically.
