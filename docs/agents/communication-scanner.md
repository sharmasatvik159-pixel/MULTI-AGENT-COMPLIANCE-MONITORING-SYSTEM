# Agent Specification: Communication Scanner (`CS-01`)
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Agent ID:** `CS-01`  
**Classification:** Tier-2 Global Banking Architecture  

---

## 1. Functional Purpose & Scope
`CS-01` is the multimodal NLP surveillance agent responsible for continuous monitoring of **850,000 daily communications** across chat, email, collaboration platforms, and recorded voice lines. It detects information barrier breaches, misleading sales practices, off-channel communication migration, research independence violations, and elder financial exploitation.

## 2. NLP & Deep Learning Architecture
1. **Multilingual Domain Transformer:**
   * Utilizes domain-adapted RoBERTa / FinBERT models fine-tuned on financial compliance lexicons across English, Mandarin, Hindi, and Spanish.
   * Embeds communication snippets into a dense 1024-dimensional semantic space for vector similarity search in ChromaDB.
2. **Information Barrier (Chinese Wall) Surveillance:**
   * Enforces structural graph boundaries between private-side teams (Investment Banking, M&A) and public-side teams (Equity Research, Sales & Trading).
   * Identifies unapproved deal terminology, code names, and leaks (e.g., "Don't cover TechCorp next week" in CS-05).
3. **Misleading Marketing & Coercive Sales Detection:**
   * Flags high-risk marketing phrases ("guaranteed 12% returns", "zero capital risk" in CS-08) targeting retail prospects.
   * Compares stated investment parameters against underlying prospectus risk disclosures.
4. **Off-Channel Communication Hunting:**
   * Identifies linguistic patterns indicating channel evasion ("reach me on WhatsApp", "ping Signal", phone numbers sent as images/QR codes in CS-13).

## 3. Interfaces & Schemas
* **Inbound Stream:** Apache Kafka topic `meridian.communications.v1`.
* **Outbound Alerts:** Kafka topic `meridian.compliance.alerts.v1` (`alert.communication.v1`).
* **Evidence Exchange:** Responds to `TM-01` queries with cryptographically signed message transcripts, intent scores, and recipient relationship graphs.
