# Log Retention, Archival & Data Sovereignty Policy
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D7-RP-v1.0`  
**Classification:** Tier-2 Global Banking Architecture  

---

## 1. Statutory Retention Mandates Across Jurisdictions

Operating across 12 countries obligates Meridian Global Bank to harmonize disparate national record retention mandates into an institutional policy standard:

| Jurisdiction | Regulatory Body | Statutory Rule | Covered Records | Mandatory Minimum Retention |
| :--- | :--- | :--- | :--- | :---: |
| **United States** | US SEC | SEC Rule 17a-4(b) / (f) | Trader communications, order records, audit trails | **6 Years** *(First 2 Accessible)* |
| **United States** | FinCEN | 31 CFR § 1020.320(d) | SAR filings and all underlying evidentiary records | **5 Years** *(from filing date)* |
| **United Kingdom**| UK FCA | FCA SYSC 9.1 / MAR | Order book records, STOR filings, surveillance logs | **5 Years** *(Up to 7 on request)* |
| **European Union**| ESMA / EBA | MiFID II Article 16(6) | Minutes, telephone recordings, electronic chats | **5 to 7 Years** |
| **India** | SEBI / FIU-IND | PMLA Section 12 / Rules | Transaction logs, STR filings, customer identity records | **5 Years** *(after relationship ends)*|
| **Singapore** | MAS | SFA / MAS Notice 626 | AML transaction records, customer due diligence | **5 Years** |

* **Institutional Standard:** To eliminate cross-border compliance divergence risk, Meridian adopts a unified default baseline of **7 Years** for all compliance detection logs, extending to **10 Years** for SAR/STR dossiers and human adjudication records.

---

## 2. Multi-Tier Lifecycle & Archival Hierarchy

Data flows through three progressive storage tiers optimized for low query latency during active investigations and cost-effective legal compliance over decadal horizons:

```
+---------------------------------------------------------------------------------------------------+
| TIER              | STORAGE TECHNOLOGY          | RETENTION WINDOW | QUERY LATENCY  | ENCRYPTION  |
+---------------------------------------------------------------------------------------------------+
| 1. HOT TIER       | PostgreSQL NVMe / Timescale | Day 0 to Day 90  | < 50 ms        | AES-256-GCM |
| 2. WARM TIER      | S3 Standard-Infrequent Access| Day 91 to Year 1 | < 250 ms       | SSE-KMS     |
| 3. COLD / WORM    | AWS S3 Glacier Vault Lock   | Year 2 to Year 10| Minutes-Hours  | WORM Locked |
+---------------------------------------------------------------------------------------------------+
```

### 2.1 WORM Compliance & Legal Hold Lock
* **Write Once Read Many (WORM):** Archival snapshots committed to Glacier are protected by an irrevocable S3 Object Lock configuration conforming to SEC Rule 17a-4(f) and FINRA Rule 4511.
* **Automated Legal Hold:** If an account, trader, or transaction becomes the subject of an SEC subpoena, DOJ grand jury inquiry, or FCA investigation, an automated **Legal Hold** flag is applied. Legal Hold records are immune to automated lifecycle expiration routines until released by the General Counsel.

### 2.2 End-of-Life Secure Crypto-Shredding
Upon expiration of the statutory retention period (and in the absence of active legal holds), records are destroyed using **NIST SP 800-88 Cryptographic Shredding**: the specific ephemeral Data Encryption Key (DEK) used to encrypt that partition is permanently purged from HashiCorp Vault, rendering the underlying ciphertext mathematically impossible to decrypt.
