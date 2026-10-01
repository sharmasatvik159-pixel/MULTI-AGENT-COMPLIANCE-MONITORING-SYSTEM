# Agent Specification: Report Generator (`RG-01`)
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Agent ID:** `RG-01`  
**Classification:** Tier-2 Global Banking Architecture  

---

## 1. Functional Purpose & Scope
`RG-01` is the legal documentation and regulatory filing compiler. It aggregates multi-agent evidence packages, human adjudications, and audit logs into legally binding disclosures, board risk dashboards, and statutory regulatory filings (FinCEN SAR, FIU-IND STR, SEC Form 8-K, Form N-PORT, and UK/EU STOR).

## 2. Core Capabilities & Filing Engines
1. **Automated SAR / STR Narrative Generation:**
   * Synthesizes chronological incident narratives adhering to FinCEN and FIU-IND regulatory guidelines.
   * Compiles suspect identification, financial instrument details, transaction amounts, and evidence summaries into XML filing packages.
2. **Multi-Audience Tailoring:**
   * Adapts technical detection dossiers into four distinct presentation profiles:
     * *Board Level:* Executive risk heatmaps, aggregate financial exposure, and strategic fine mitigation.
     * *Management Level:* Supervisory workflow status, remedial operational actions.
     * *Operations Level:* Granular timestamp logs, order IDs, communication transcripts.
     * *Regulator Level:* Official statutory submission schemas (XBRL, XML, PDF/A-1b).
3. **Cryptographic Proof Stamping:**
   * Generates SHA-256 Merkle proofs and applies institutional X.509 digital signatures to every exported document, ensuring evidentiary admissibility in judicial proceedings.

## 3. Interfaces & Schemas
* **Inbound Escalation:** Queue `agent.escalation.resolved` (Human-signed adjudication packages).
* **Outbound Gateway:** Secure SFTP / REST mTLS connections to regulatory submission gateways (FinCEN BSA E-Filing System, SEC EDGAR, FIU-IND FinGate, FCA RegData).
* **Permanent Archive:** Direct write to Amazon S3 Glacier Vault with Write-Once-Read-Many (WORM) compliance lock.
