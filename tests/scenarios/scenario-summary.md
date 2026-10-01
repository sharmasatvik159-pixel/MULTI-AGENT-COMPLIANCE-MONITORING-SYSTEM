# Master Test Scenario Summary Table (CS-01 to CS-20)
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D6-SS-v1.0`  
**Classification:** Tier-2 Global Banking Test Suite  

---

## 1. Master Scenario Validation Matrix

This table summarizes all 20 real-world compliance test scenarios drawn from SEC, FINRA, FCA, and OFAC enforcement actions.

| Scenario ID | Scenario Name | Primary Agents | Complexity | Expected System Outcome | Target Regulations | Escalation Tier |
| :---: | :--- | :---: | :---: | :--- | :--- | :---: |
| **CS-01** | Insider Trading: Pre-Announcement Accumulation | `TM-01` + `CS-01` | Complex | **CRITICAL ALERT** (SAR Filing within 30 days) | SEC Rule 10b-5, FINRA 2010 | Tier 3 |
| **CS-02** | Market Manipulation: Futures Spoofing | `TM-01` | Standard | **HIGH ALERT** (Desk Trading Halt) | Dodd-Frank 747, CEA 4c(a)(5), CME 575 | Tier 3 |
| **CS-03** | Unsuitable Investment Recommendation | `CS-01` + `TM-01` | Complex | **HIGH ALERT** (IPS Breach Notification) | FINRA Rule 2111, SEC Reg BI | Tier 2 |
| **CS-04** | AML: Currency Structuring (Smurfing) | `TM-01` | Standard | **CRITICAL ALERT** (SAR Filing) | Bank Secrecy Act, 31 CFR § 1020.320 | Tier 3 |
| **CS-05** | Chinese Wall Breach: Deal Leakage | `CS-01` | Complex | **CRITICAL ALERT** (Information Barrier Freeze) | SEC Section 15(g), FINRA 5280, MiFID II | Tier 3 |
| **CS-06** | Wash Trading: Cross-Account Coordination | `TM-01` | Complex | **HIGH ALERT** (Collusive Account Review) | CEA Section 4c(a), SEC Rule 10b-5, FINRA 5210 | Tier 2 |
| **CS-07** | Regulatory Change Impact: Swap Margins | `RU-01` | Standard | **MEDIUM ALERT** (Impact Assessment Report) | SEC Swap Margin Rule, Basel III CRE54 | Tier 1 |
| **CS-08** | Client Communication: Misleading Claims | `CS-01` | Standard | **CRITICAL ALERT** (Immediate Campaign Retract) | SEC Rule 206(4)-1, FINRA 2210, FCA COBS 4 | Tier 2 |
| **CS-09** | Sanctions Violation: Indirect Exposure | `TM-01` + `RU-01` | Complex | **CRITICAL ALERT** (Immediate Wire Hold) | OFAC Regulations, 31 CFR Part 501 | Tier 4 |
| **CS-10** | Front-Running: Client Order Anticipation | `TM-01` | Complex | **CRITICAL ALERT** (Prop Desk Trade Reversal) | Investment Company Act 17(j), FINRA 5270 | Tier 3 |
| **CS-11** | Data Privacy: Cross-Border EU Transfer | `CS-01` + `RU-01` | Complex | **HIGH ALERT** (72-Hour DPA Notification) | GDPR Articles 44–49, Schrems II | Tier 3 |
| **CS-12** | Concentration Risk: Portfolio Limit Breach | `TM-01` | Standard | **MEDIUM ALERT** (Rebalancing Directive) | ICA Section 13, Form N-PORT, UCITS | Tier 1 |
| **CS-13** | Off-Channel Communication: WhatsApp | `CS-01` | Standard | **HIGH ALERT** (Supervisory Sanction) | SEC Rule 17a-4, FINRA Rule 3110 | Tier 2 |
| **CS-14** | Late Trading: Mutual Fund NAV Manipulation | `TM-01` | Standard | **CRITICAL ALERT** (Trade Price Repricing) | SEC Rule 22c-1, ICA Section 22(c) | Tier 3 |
| **CS-15** | Best Execution Failure: Routing Bias | `TM-01` | Standard | **HIGH ALERT** (Routing Remediation) | SEC Rule 605/606, FINRA Rule 5310 | Tier 2 |
| **CS-16** | Conflict of Interest: Research Independence | `CS-01` + `TM-01` | Complex | **CRITICAL ALERT** (Research Rating Freeze) | SEC Regulation AC, FINRA Rule 2241 | Tier 3 |
| **CS-17** | Elder Financial Exploitation | `TM-01` + `CS-01` | Complex | **CRITICAL ALERT** (Temporary Account Hold) | FINRA Rules 2165 & 4512, Senior Safe Act | Tier 3 |
| **CS-18** | **FALSE POSITIVE:** Legitimate Block Trade | `TM-01` | Special | **NO ALERT** (Autonomously Suppressed) | Institutional Block Crossing Exemption | None |
| **CS-19** | Multi-Jurisdiction Regulatory Conflict | `RU-01` | Complex | **HIGH ALERT** (Escalate to General Counsel) | EMIR Reporting vs. Singapore MAS Secrecy | Tier 4 |
| **CS-20** | **COORDINATED:** Trade-Based Money Laundering | **ALL 4 AGENTS** | Complex | **CRITICAL ALERT** (SAR Filing & Board Report) | BSA/AML, OFAC, FATF TBML Red Flags | Tier 4 |
