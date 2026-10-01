# Agent Specification: Regulatory Update Tracker (`RU-01`)
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Agent ID:** `RU-01`  
**Classification:** Tier-2 Global Banking Architecture  

---

## 1. Functional Purpose & Scope
`RU-01` provides autonomous regulatory intelligence by monitoring official gazettes, regulatory portals, and legal feeds across **23 global authorities**. It parses new rules, calculates operational impact deltas, identifies cross-jurisdictional legal conflicts, and updates operational parameters for `TM-01` and `CS-01`.

## 2. Ingestion & Analysis Architecture
1. **Automated Regulatory Feed Ingestion:**
   * Polls SEC EDGAR, FINRA Regulatory Notices, FCA Handbook, ESMA, SEBI circulars, and RBI Master Directions at 15-minute intervals.
   * Ingests real-time sanctions lists (OFAC SDN XML/JSON, EU Financial Sanctions Database) via push webhooks.
2. **Semantic Rule Diffing & Vectorization:**
   * Converts unstructured legal text and circular PDFs into structured markdown.
   * Identifies amendments to quantitative thresholds (e.g., SEC increasing uncleared swap margin requirements by 25% in CS-07).
   * Stores segmented rule vectors in ChromaDB collection `global_regulations_v1`.
3. **Cross-Jurisdiction Conflict Identification:**
   * Evaluates pairwise regulatory obligations across borders (e.g., EU EMIR reporting mandate vs. Singapore MAS client secrecy constraints in CS-19).
   * Flags irreconcilable sovereign contradictions directly to General Counsel.

## 3. Interfaces & Schemas
* **External Connectors:** REST APIs, RSS/Atom feeds, scraping microservices with TLS client certificates.
* **Broadcast Topic:** Kafka topic `meridian.compliance.regulatory_updates.v1` (`update.regulatory.v1`).
* **Direct RPC:** Query endpoint for `TM-01` and `CS-01` to fetch applicable legal statutes for suspected violation events.
