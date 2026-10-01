# Security Architecture, Data Localization & Governance Specification
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D1-SEC-v1.0`  
**Classification:** Tier-2 Global Banking System Architecture  
**Author:** AI Systems Architect, Zetheta Algorithms  

---

## 1. Security Architecture Principles

Operating within a Tier-2 global banking institution across 12 jurisdictions requires an institutional Zero-Trust Security Architecture. Every inter-agent message, human decision, external API query, and database interaction is continuously authenticated, authorized, encrypted, and recorded in a tamper-evident audit ledger.

```mermaid
graph TD
    subgraph ZeroTrustIdentity["Zero-Trust Identity & Access (SPIFFE / SPIRE)"]
        SPIRE_Server["SPIRE Server (CA Root)"]
        Agent_TM["Agent TM-01<br/>(SVID: spiffe://meridian.bank/agent/tm)"]
        Agent_CS["Agent CS-01<br/>(SVID: spiffe://meridian.bank/agent/cs)"]
        Agent_RU["Agent RU-01<br/>(SVID: spiffe://meridian.bank/agent/ru)"]
        Agent_RG["Agent RG-01<br/>(SVID: spiffe://meridian.bank/agent/rg)"]
        
        SPIRE_Server -->|Issues 1-hr X.509 SVIDs| Agent_TM
        SPIRE_Server -->|Issues 1-hr X.509 SVIDs| Agent_CS
        SPIRE_Server -->|Issues 1-hr X.509 SVIDs| Agent_RU
        SPIRE_Server -->|Issues 1-hr X.509 SVIDs| Agent_RG
    end

    subgraph SecureTransit["Encrypted In-Transit Layer (mTLS 1.3)"]
        Agent_TM <-->|mTLS 1.3 / AES-256-GCM| Kafka_Broker["Apache Kafka Brokers"]
        Agent_CS <-->|mTLS 1.3 / AES-256-GCM| RabbitMQ_Broker["RabbitMQ Brokers"]
        Agent_RG <-->|mTLS 1.3 / AES-256-GCM| Orchestrator["Temporal / LangGraph"]
    end

    subgraph DataSovereignty["Data Sovereignty & Localization Boundary"]
        subgraph IndiaEnclave["India Regional Data Center (Mumbai / Hyderabad)"]
            RBI_Storage["RBI Payment Data Store<br/>(Exclusive In-Country Storage)"]
            UPI_Surveillance["UPI Transaction Monitor Enclave"]
        end
        subgraph EUEnclave["EU Regional Data Center (Frankfurt / Dublin)"]
            GDPR_Storage["EU Resident Personal Data<br/>(GDPR Articles 44–49 Enclave)"]
        end
        subgraph GlobalCluster["Global Aggregation & Synthesis"]
            Anonymized_Feeds["Tokenized & Anonymized Signals"]
            Audit_Ledger["Cryptographic Merkle Audit Ledger"]
        end
    end

    IndiaEnclave -->|Tokenized Metadata Only| GlobalCluster
    EUEnclave -->|Standard Contractual Clauses (SCCs)| GlobalCluster
```

---

## 2. Authentication & Inter-Agent Identity Management

### 2.1 Mutual TLS (mTLS v1.3) with SPIFFE/SPIRE
* **Identity Framework:** The system implements the **SPIFFE** (Secure Production Identity Framework for Everyone) standard backed by a high-availability **SPIRE** deployment.
* **Cryptographic SVIDs:** Every agent workload is issued a cryptographically verifiable **SPIFFE ID** and an X.509 SVID (SPIFFE Verifiable Identity Document).
  * Example TM Identifier: `spiffe://meridian.bank/agent/tm-01`
  * Example CS Identifier: `spiffe://meridian.bank/agent/cs-01`
  * Example Human Supervisor: `spiffe://meridian.bank/user/analyst/tier2`
* **Ephemeral Certificate Lifecycles:** Certificates have a strict **1-hour time-to-live (TTL)** with automated zero-downtime rotation. If an agent node is compromised, its certificate expires automatically within 60 minutes.
* **Cipher Suites:** Strictly enforced TLS 1.3 cipher suites with Perfect Forward Secrecy (PFS):
  * `TLS_AES_256_GCM_SHA384`
  * `TLS_CHACHA20_POLY1305_SHA256`

### 2.2 Message-Level Digital Signatures & Nonces
In addition to transport-layer encryption, every message envelope payload is digitally signed at the application layer:
* **Asymmetric Signatures:** The sending agent signs the SHA-256 digest of the message payload using its private RSA-4096 or ECDSA P-384 key.
* **Replay Prevention:** Every message includes a unique `nonce` (cryptographic random string) and a microsecond-precision `timestamp`. Receivers validate the nonce against a 10-minute sliding window in Redis; duplicate or expired nonces are dropped immediately.

---

## 3. Cryptography & Data Protection at Rest

### 3.1 Envelope Encryption with HashiCorp Vault / AWS KMS
Data persisted to PostgreSQL, TimescaleDB, ChromaDB, and Kafka commit logs is protected by a two-tier envelope encryption hierarchy:
1. **Customer Master Key (CMK):** Hardware Security Module (HSM)-protected keys hosted in HashiCorp Vault / AWS CloudHSM (FIPS 140-2 Level 3 validated).
2. **Data Encryption Keys (DEKs):** Ephemeral 256-bit AES keys generated per database partition or Kafka topic segment. DEKs are encrypted under the CMK and stored alongside encrypted ciphertext.
3. **Storage Cipher:** `AES-256-GCM` with authenticated data tags providing both confidentiality and integrity protection against disk tampering.

### 3.2 Automated Key Rotation
* Master keys are automatically rotated every **90 days**.
* In-flight DEKs are rotated every **24 hours** or after encrypting 10 million records.

---

## 4. Data Localization & Jurisdictional Compliance

Operating across 12 countries subjects Meridian Global Bank to strict data sovereignty mandates. The architecture enforces structural boundary firewalls to satisfy regional regulators:

### 4.1 India RBI Payment Data Localization Directive
* **Regulatory Mandate:** Reserve Bank of India Directive `DPSS.CO.OD.No.2785/06.11.001/2017-18` on *Storage of Payment System Data*.
* **Statutory Requirement:** All payment data relating to payment systems operated in India (including UPI, IMPS, NEFT, RTGS, and domestic card transactions) must be stored in systems **located only in India**.
* **System Implementation:**
  * **Dedicated Enclave:** A dedicated sovereign pod cluster (`meridian-in-surveillance`) is hosted in AWS Asia Pacific (Mumbai: `ap-south-1`) and mirrored to Hyderabad (`ap-south-2`).
  * **End-to-End Data In-Country:** Raw UPI and domestic payment transaction logs, settlement records, customer identifiers, and account balances remain exclusively on India-based databases.
  * **Cross-Border Aggregation:** Only de-identified, tokenized compliance alerts (e.g., "Alert ID: IND-9021, Category: Structuring, Risk: High") are transmitted to the global orchestration cluster; all underlying personal customer records remain pinned inside the Indian data border.

### 4.2 EU GDPR Cross-Border Data Transfer Framework (Articles 44–49)
* **Regulatory Mandate:** European Union General Data Protection Regulation (Regulation (EU) 2016/679), Chapter V, and the CJEU *Schrems II* ruling.
* **System Implementation:**
  * **Sovereignty Enclave:** EU resident communications and account data (surveilled by `CS-01` and `TM-01`) are processed inside the EU legal boundary (Frankfurt/Dublin).
  * **Transfer Mechanism:** Where global multi-agent correlation requires cross-border analysis (e.g., CS-11 data migration or global market manipulation), data transfers are governed by **Standard Contractual Clauses (SCCs)**, binding corporate rules, and supplementary technical measures (end-to-end homomorphic pseudonymization).
  * **72-Hour Breach Mechanism:** Automated notification pipelines within `RG-01` alert the Data Protection Officer (DPO) and lead supervisory authorities within the mandatory 72-hour statutory window.

---

## 5. Role-Based & Attribute-Based Access Control (RBAC / ABAC)

Access to surveillance dashboards, agent configurations, alert dossiers, and audit trails is governed by a fine-grained access control matrix:

| Role / Subject | View Anonymized Alerts | View Raw Communications | View Full Trading PII | Override Agent Decisions | Authorize SAR/STR Filing | Modify Agent Thresholds | Inspect Audit Ledger |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Junior Compliance Analyst (Tier 1)** | Yes | Masked | Masked | No | No | No | Read-Only (Assigned) |
| **Senior Compliance Analyst (Tier 2)** | Yes | Unmasked (Case) | Unmasked (Case) | Yes (Low/Med) | No | No | Read-Only (Assigned) |
| **Compliance Manager (Tier 3)** | Yes | Full Access | Full Access | Yes (All) | Review / Endorse | No | Full Read-Only |
| **Chief Compliance Officer (Tier 4)** | Yes | Full Access | Full Access | Yes (Board) | Final Signoff | Endorse | Full Read-Only |
| **Lead AI Systems Architect** | Diagnostics | No | No | No | No | Yes (Dual Control) | Operational Only |
| **Independent Regulatory Auditor** | Yes | Read-Only | Read-Only | No | No | No | Cryptographic Verify |
| **Autonomous Agent Service Principal** | Machine Read | Machine Read | Machine Read | Automated Only | Draft Only | No | Append-Only (Sign) |

### 5.1 Dual-Control (Four-Eyes Principle) Enforcement
Any modification to core surveillance parameters (e.g., raising the currency structuring alert threshold above $10,000 or suppressing detection rules) requires **Dual-Control Authorization**:
1. Initiated by the Lead AI Architect or Senior Analyst.
2. Formally countersigned via cryptographic multi-factor approval by the Chief Compliance Officer (CCO) or Designated Compliance Director before deployment to production pods.
