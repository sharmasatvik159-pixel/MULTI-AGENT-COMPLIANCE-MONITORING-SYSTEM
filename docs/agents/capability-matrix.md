# Cross-Agent Capability Matrix & Functional Boundaries
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D5-CM-v1.0`  
**Classification:** Tier-2 Global Banking Architecture  

---

## 1. Cross-Agent Functional Capability Matrix

| Operational Capability | Transaction Monitor (`TM-01`) | Communication Scanner (`CS-01`) | Regulatory Tracker (`RU-01`) | Report Generator (`RG-01`) |
| :--- | :---: | :---: | :---: | :---: |
| **High-Throughput Order Stream Analysis** | **PRIMARY** | No | No | No |
| **Level-2 / Level-3 Order Book Reconstruction** | **PRIMARY** | No | No | No |
| **Multi-Asset Wash Trading Graph Matching** | **PRIMARY** | Supporting | No | No |
| **Currency Structuring (Smurfing) Aggregation**| **PRIMARY** | Supporting | No | No |
| **Multilingual NLP / Voice Transcription** | No | **PRIMARY** | No | No |
| **Information Barrier (Chinese Wall) Tracking**| Supporting | **PRIMARY** | No | No |
| **Conduct Risk & Misleading Sales Detection** | No | **PRIMARY** | No | No |
| **Off-Channel Communication Hunting** | No | **PRIMARY** | No | No |
| **Global Regulatory Feed Ingestion (23 Bodies)**| No | No | **PRIMARY** | No |
| **Legal Text Vectorization & Rule Diffing** | No | No | **PRIMARY** | No |
| **Cross-Jurisdiction Conflict Identification** | No | Supporting | **PRIMARY** | No |
| **Watchlist & Sanctions List Dissemination** | Ingests | Ingests | **PRIMARY** | No |
| **Regulatory Filing Compilation (SAR / STR)** | Feeds Data | Feeds Data | Feeds Statute | **PRIMARY** |
| **Multi-Audience Report Adaptation** | No | No | No | **PRIMARY** |
| **Cryptographic Merkle Proof Generation** | Signs Signals | Signs Signals | Signs Rules | **PRIMARY (Seals)** |

---

## 2. Functional Boundaries & Separation of Concerns

To prevent architectural overlap and state corruption, strict operational boundaries are enforced:

1. **`TM-01` vs `CS-01` Boundary:**
   * `TM-01` **never** analyzes unstructured communication text. It only evaluates numerical, temporal, and account entity records.
   * `CS-01` **never** performs order-book or market-tick calculations. When `CS-01` suspects an unapproved trade leak, it queries `TM-01` with account and timestamp coordinates.
2. **`RU-01` Boundary:**
   * `RU-01` is strictly an intelligence and metadata provider. It does not monitor live transactional or communication traffic. It continuously provides updated rule vectors, threshold values, and sanctions updates to `TM-01` and `CS-01`.
3. **`RG-01` Boundary:**
   * `RG-01` does not initiate independent surveillance investigations. It acts as the execution compiler triggered exclusively by the consensus engine or human supervisor sign-off.
