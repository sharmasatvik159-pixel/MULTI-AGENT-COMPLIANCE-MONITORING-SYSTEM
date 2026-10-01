# Agent Specification: Transaction Monitor (`TM-01`)
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Agent ID:** `TM-01`  
**Classification:** Tier-2 Global Banking Architecture  

---

## 1. Functional Purpose & Scope
`TM-01` is the high-velocity structured streaming surveillance agent responsible for monitoring all order, trade, cancellation, quote, and payment events across Meridian Global Bank's 12 jurisdictions. It processes **2.4 million daily transactions** to identify manipulative trading practices, structural liquidity manipulation, insider trading patterns, and illicit currency structuring.

## 2. Quantitative Algorithms & Detection Models
1. **Spoofing & Layering Detection:**
   * Reconstructs Level-2 and Level-3 order books across high-frequency tick streams.
   * Tracks high-speed order creation followed by microsecond cancellations ($< 500\text{ ms}$) on opposite book sides.
   * Evaluates order-to-trade ratio ($OTR > 30:1$).
2. **Wash Trading Analysis:**
   * Evaluates bipartite matching graphs between internal portfolio accounts.
   * Flags trades matching within 2 basis points price variance and identical share quantities with near-zero change in beneficial ownership.
3. **Currency Structuring (Smurfing):**
   * Stateful sliding-window aggregation of cash deposits and wire transfers over rolling 10-business-day periods.
   * Flags multiple transactions clustered immediately below regulatory reporting thresholds ($8,500–$9,900 for US FinCEN $10,000 threshold; ₹8,50,000–₹9,90,000 for India PMLA ₹10 Lakh threshold).
4. **False Positive Suppression (CS-18 Block Trades):**
   * Cross-references institutional block trades against the internal Compliance Pre-Trade Clearance Ticket database and crossing network logs.
   * Suppresses market abuse alerts when execution is confirmed as part of an authorized, pre-scheduled portfolio rebalancing mandate.

## 3. Interfaces & Schemas
* **Inbound Stream:** Apache Kafka topic `meridian.transactions.v1` (Protobuf / Avro format).
* **Outbound Alerts:** Kafka topic `meridian.compliance.alerts.v1` (`alert.transaction.v1`).
* **Inter-Agent Query Protocol:** Directly queries `CS-01` via AMQP RPC (`query.comm.v1`) to obtain contextual trader communication history when quantitative anomalies are detected.
* **State Management:** RocksDB state store with periodic checkpoints to NVMe block storage.
