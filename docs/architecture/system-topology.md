# Multi-Agent System Topology & C4 Architecture Specification
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D1-ST-v1.0`  
**Classification:** Tier-2 Global Banking System Architecture  
**Author:** AI Systems Architect, Zetheta Algorithms  

---

## 1. Architectural Topology Overview

The Meridian Global Bank compliance monitoring architecture implements a **Hybrid Hierarchical-Choreographed Agent Topology**.

Purely choreographic systems (pure event-driven without coordinators) suffer from untraceable cascading loops and lack deterministic global state, making them unsuitable for stringent banking audits. Conversely, purely centralized orchestrators create single points of failure (SPOF) and catastrophic throughput bottlenecks when processing 2.4 million daily transactions.

To achieve both high throughput and audit-grade determinism, Meridian deploys a **Two-Tier Hybrid Topology**:
1. **Tier 1 (Streaming Ingestion & Autonomous Detection — Choreographed):** Ingestion and preliminary pattern detection operate choreographically over **Apache Kafka**. `TM-01` and `CS-01` autonomously ingest high-velocity data, evaluate sliding windows, and publish preliminary alerts without blocking or querying a central master.
2. **Tier 2 (Multi-Agent Correlation, Consensus & Escalation — Orchestrated Saga):** Once a potential cross-domain violation or high-severity anomaly is identified, execution transitions to an orchestrated **Temporal.io & LangGraph** state machine. This coordinator manages stateful multi-agent evidence gathering, consensus scoring, human-in-the-loop escalation, and audit trail finalization.

```mermaid
graph TB
    subgraph StreamLayer["Layer 1: Choreographed Stream Processing (Kafka Backbone)"]
        TxnStream["Trading & Payment Feeds<br/>(2.4M/day)"] -->|meridian.transactions.v1| TM_Workers["TM-01 Consumer Group<br/>(Flink / Kafka Streams)"]
        CommStream["Communications Ingest<br/>(850k/day)"] -->|meridian.communications.v1| CS_Workers["CS-01 GPU Workers<br/>(Transformer NLP)"]
        RegFeeds["Global Reg Feeds<br/>(23 Authorities)"] -->|External APIs / Scraping| RU_Workers["RU-01 Intelligence Scrapers"]
        
        RU_Workers -->|Broadcast Taxonomies| KafkaBus["Kafka Event Bus"]
        TM_Workers -->|Publish Preliminary Alerts| KafkaBus
        CS_Workers -->|Publish Preliminary Alerts| KafkaBus
    end

    subgraph SagaLayer["Layer 2: Orchestrated Coordination & Consensus (Temporal + LangGraph)"]
        KafkaBus -->|Trigger Multi-Agent Saga| TemporalEngine["Temporal.io Workflow Engine<br/>(Durable Execution / Saga Pattern)"]
        
        TemporalEngine <-->|Manage State Graph| LangGraph["LangGraph Consensus Coordinator"]
        LangGraph <-->|Query Evidence| TM_Workers
        LangGraph <-->|Query Context| CS_Workers
        LangGraph <-->|Query Applicable Law| RU_Workers
        
        LangGraph -->|Evidence Package| ConsensusEngine["Consensus & Scoring Engine<br/>(Dempster-Shafer / Bayesian)"]
    end

    subgraph EscalationAudit["Layer 3: Human-in-the-Loop & Audit Packaging (RabbitMQ + PostgreSQL)"]
        ConsensusEngine -->|Priority Routing| RabbitMQ["RabbitMQ AMQP Broker<br/>(Priority Queues P1-P5)"]
        RabbitMQ -->|Tiered Alert Dispatch| CompliancePortal["Compliance Officer Portal<br/>(Tiers 1–4 Human Review)"]
        CompliancePortal -->|Human Signoff / Override| TemporalEngine
        TemporalEngine -->|Generate Final Filing| RG_Workers["RG-01 Report Generator"]
        
        RG_Workers -->|Cryptographic Hash Chain| TimescaleDB["PostgreSQL / TimescaleDB<br/>(Tamper-Evident Ledger)"]
        RG_Workers -->|Automated Submissions| RegulatoryGateways["Regulatory Portals (EDGAR, FIU, FCA)"]
    end
```

---

## 2. Dual Message Broker Infrastructure: Kafka vs. RabbitMQ Rationale

A core architectural innovation of the Meridian platform is the deliberate separation of streaming throughput from transactional priority routing using a dual-broker strategy:

### 2.1 Apache Kafka: The High-Throughput Event Log
* **Role:** Ingestion backbone, event sourcing, continuous time-series streaming.
* **Volume Handled:** 2.4 million transactions/day (~30–50 events/sec average, 35,000 events/sec peak at market open) and 850,000 communications/day.
* **Key Capabilities Used:**
  * **Partitioned Topics:** Keyed partitioning by `account_id` and `instrument_id` guarantees in-order event delivery for strict temporal analysis (front-running, wash trading).
  * **Log Compaction & Replay:** Enables full event sourcing and retroactive compliance audits; if detection algorithms are updated by `RU-01`, transactions can be replayed from any historical offset.
  * **Zero-Copy Disk Persistence:** Guarantees zero data loss under high load.

### 2.2 RabbitMQ: Priority AMQP Routing & Dead-Letter Isolation
* **Role:** Targeted inter-agent Remote Procedure Calls (RPC), priority-based human escalation dispatch, and dead-letter queue (DLQ) containment.
* **Key Capabilities Used:**
  * **Priority Queuing (x-max-priority = 5):** Guarantees that CRITICAL (P1) alerts (e.g., active OFAC sanctions match or imminent $400M fraud) pre-empt lower priority batch notifications (P4/P5).
  * **Dead Letter Exchanges (DLX):** Unparseable payloads, malformed messages, or unacknowledged agent timeouts are automatically routed to `agent.deadletter.queue` with detailed diagnostic envelopes for quarantine.
  * **Transactional Acknowledgment (ACK/NACK):** Assures that no human compliance alert is lost during server restarts or network partitions.

---

## 3. C4 Model Architecture Specification

### 3.1 C4 Level 1: System Context Diagram
The System Context diagram details how the Multi-Agent Compliance Monitoring System sits within the enterprise ecosystem of Meridian Global Bank and interacts with internal trading infrastructure and external regulatory bodies.

```mermaid
C4Context
    title System Context Diagram - Meridian Global Bank Multi-Agent Compliance Monitoring System

    Person(compliance_officer, "Compliance Officer", "Reviews escalated alerts, investigates multi-agent dossiers, and authorizes filings.")
    Person(auditor, "Internal / Regulatory Auditor", "Inspects tamper-evident audit logs and verifies detection rule provenance.")

    System(compliance_system, "Multi-Agent Compliance System", "Autonomous surveillance platform utilizing TM-01, CS-01, RU-01, and RG-01.")

    System_Ext(trading_platform, "Core Trading & OMS Platforms", "Equities, Fixed Income, Derivatives, and FX execution management systems.")
    System_Ext(payment_rails, "Global & Domestic Payment Rails", "SWIFT MT/MX, Fedwire, CHAPS, Target2, and India UPI payment switches.")
    System_Ext(comm_systems, "Enterprise Communication Feeds", "Bloomberg Chat, Symphony, MS Teams, Exchange Email, WhatsApp Business.")
    System_Ext(regulatory_bodies, "External Regulatory Portals", "SEC EDGAR, FINRA Gateway, FCA RegData, SEBI Portal, FIU-IND FinGate.")

    Rel(trading_platform, compliance_system, "Streams orders, trades, and cancellations", "Kafka / FIX 5.0")
    Rel(payment_rails, compliance_system, "Streams wire transfers and instant payment records", "Kafka / ISO 20022")
    Rel(comm_systems, compliance_system, "Streams encrypted messages and transcripts", "Kafka / Webhooks")
    Rel(compliance_system, regulatory_bodies, "Submits automated SAR/STR, 8-K, and regulatory reports", "REST / mTLS / SFTP")
    Rel(compliance_system, compliance_officer, "Dispatches prioritized escalation packages", "WebSockets / HTTPS")
    Rel(compliance_officer, compliance_system, "Submits adjudication rationale and overrides", "HTTPS / RBAC")
    Rel(auditor, compliance_system, "Queries cryptographically verified audit ledger", "SQL / Read-Only")
```

---

### 3.2 C4 Level 2: Container Diagram
The Container diagram illustrates the high-level technical building blocks, operational containers, datastores, and networking protocols.

```mermaid
C4Container
    title Container Diagram - Meridian Multi-Agent System Components

    Container(api_gateway, "API & Ingestion Gateway", "FastAPI / Envoy", "Terminates mTLS, validates inbound schemas, distributes load.")
    Container(kafka_cluster, "Streaming Event Bus", "Apache Kafka 3.7", "Persistent partitioned event log for trades, communications, and raw feeds.")
    Container(rabbitmq_broker, "Priority Message Broker", "RabbitMQ 3.13", "Manages priority queues (P1-P5), RPC queries, and dead-letter queues.")
    
    Container(agent_tm, "Transaction Monitor (TM-01)", "Python / Flink / RocksDB", "Stateful streaming analytics, order book reconstruction, wash trade detector.")
    Container(agent_cs, "Communication Scanner (CS-01)", "Python / PyTorch / Transformers", "NLP classification, intent extraction, Chinese Wall monitor.")
    Container(agent_ru, "Regulatory Tracker (RU-01)", "Python / LangChain / ChromaDB", "Scrapes legal feeds, vectorizes circulars, assesses impact.")
    Container(agent_rg, "Report Generator (RG-01)", "Python / WeasyPrint / Cryptography", "Compiles SAR narratives, signs filings, generates audit PDFs.")
    
    Container(orchestrator, "Workflow Orchestrator", "Temporal.io & LangGraph", "Manages multi-agent sagas, consensus graphs, and SLA countdowns.")
    ContainerDb(db_postgres, "Primary Store & Ledger", "PostgreSQL 16 + TimescaleDB", "Stores relational compliance data, user accounts, and immutable audit logs.")
    ContainerDb(vector_db, "Regulatory Knowledge Store", "ChromaDB", "Stores dense vector embeddings of regulatory handbooks and lexicons.")
    ContainerDb(cache_redis, "Deduplication Cache", "Redis 7.2 Cluster", "Maintains idempotency keys, sliding window counters, and active heartbeats.")
    Container(vault, "Secrets & Key Management", "HashiCorp Vault", "Manages mTLS X.509 certs, rotating HMAC keys, and database credentials.")

    Rel(api_gateway, kafka_cluster, "Publishes validated events", "mTLS / Kafka Protocol")
    Rel(kafka_cluster, agent_tm, "Consumes transaction events", "Kafka Consumer")
    Rel(kafka_cluster, agent_cs, "Consumes communication events", "Kafka Consumer")
    Rel(agent_ru, vector_db, "Updates rule embeddings", "Internal API")
    Rel(agent_tm, rabbitmq_broker, "Dispatches alerts & queries", "AMQP SSL")
    Rel(agent_cs, rabbitmq_broker, "Dispatches alerts & queries", "AMQP SSL")
    Rel(rabbitmq_broker, orchestrator, "Triggers workflow executions", "AMQP SSL")
    Rel(orchestrator, agent_rg, "Requests report compilation", "gRPC / mTLS")
    Rel(agent_rg, db_postgres, "Writes signed audit records", "SQL / TLS")
    Rel(agent_tm, cache_redis, "Checks duplicate trade IDs", "RESP3")
```

---

### 3.3 C4 Level 3: Component Diagram (Agent Coordination & Consensus Engine)
The Component diagram focuses on the internal structure of the Multi-Agent Orchestration & Consensus Subsystem.

```mermaid
C4Component
    title Component Diagram - Consensus & Coordination Subsystem

    Component(event_listener, "Saga Event Listener", "Temporal Activity", "Listens for preliminary alerts from TM and CS.")
    Component(evidence_aggregator, "Evidence Aggregator", "LangGraph State Node", "Correlates trade timestamps with communication records.")
    Component(ru_rule_matcher, "Rule Impact Matcher", "ChromaDB Client", "Matches observed facts against jurisdictional rule vectors.")
    Component(consensus_core, "Consensus Evaluator", "Python Mathematical Module", "Applies Dempster-Shafer theory of evidence to aggregate agent belief masses.")
    Component(conflict_arbiter, "Conflict Arbiter", "Rule-Based Engine", "Detects jurisdictional or factual conflicts and triggers tie-breaking rules.")
    Component(escalation_router, "Escalation Router", "Priority Dispatcher", "Maps composite confidence score and severity to human tiers.")
    Component(crypto_stamper, "Cryptographic Stamper", "HMAC / SHA-256 Module", "Generates Merkle leaf nodes for immutable audit recording.")

    Rel(event_listener, evidence_aggregator, "Initiates saga instance")
    Rel(evidence_aggregator, ru_rule_matcher, "Requests applicable statutory rules")
    Rel(evidence_aggregator, consensus_core, "Provides aggregated multi-agent signals")
    Rel(consensus_core, conflict_arbiter, "Flags divergent agent assessments")
    Rel(conflict_arbiter, consensus_core, "Returns resolved belief state")
    Rel(consensus_core, escalation_router, "Passes consensus score & alert classification")
    Rel(escalation_router, crypto_stamper, "Sends complete decision package for sealing")
```

---

### 3.4 C4 Level 4: Code & Execution Sequence Diagram
This execution sequence traces Scenario **CS-01** (Pre-Announcement Insider Trading Accumulation):

```mermaid
sequenceDiagram
    autonumber
    participant Trader as Trader Account / OMS
    participant Email as Exchange Mail Server
    participant TM as Transaction Monitor (TM-01)
    participant CS as Communication Scanner (CS-01)
    participant Orchestrator as LangGraph / Temporal Engine
    participant Consensus as Consensus Engine
    participant Officer as Compliance Officer (Tier 3)
    participant RG as Report Generator (RG-01)
    participant Audit as Immutable Audit Ledger

    Trader->>TM: Executes $12M Company X accumulation over 3 weeks
    Email->>CS: Scans email: Private dinner with Company X CFO 4 weeks ago
    Note over TM: Company X announces acquisition (+35% price surge)
    TM->>TM: Flags anomalous timing & volume (Confidence: 0.82)
    TM->>Orchestrator: Emits ALERT (Type: INSIDER_TRADING, Priority: P1)
    
    Orchestrator->>CS: Dispatches QUERY (Subject: PM_ID, Ticker: CMPX, Window: 30d)
    CS->>CS: Semantic extraction: Discovers private dinner meeting evidence
    CS->>Orchestrator: Returns RESPONSE (Evidence: High Intent, Confidence: 0.88)
    
    Orchestrator->>Consensus: Computes Joint Mass Function (Dempster-Shafer)
    Consensus-->>Orchestrator: Combined Confidence: 0.94 (Severity: CRITICAL)
    
    Orchestrator->>Officer: Dispatches Tier 3 Decision Package (SLA: 2 Hours)
    Officer->>Orchestrator: Reviews Dossier & Confirms Suspicion ("SUBMIT SAR")
    
    Orchestrator->>RG: Triggers SAR Compilation (FinCEN 31 CFR § 1020.320)
    RG->>RG: Compiles Narrative, XML Package & Embeds Merkle Proof
    RG->>Audit: Seals Tamper-Evident Audit Record (Block Hash: 0x8f3c...)
    RG->>Officer: Ready for Final Regulatory Filing (Within 30-Day Window)
```

---

## 4. Architectural Trade-Off Analysis

| Architectural Pattern | Latency Profile | Fault Tolerance | Audit Determinism | Implementation Complexity | Decision for Meridian |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pure Centralized Orchestration** | Poor (Single choke-point for 2.4M txns/day) | Low (Central coordinator crash halts all surveillance) | High (Single state machine controls all transitions) | Moderate | **Rejected:** Bottlenecks ingestion volume. |
| **Pure Event Choreography** | Excellent (<5ms peer-to-peer pub/sub) | High (Decoupled agents; no central failure node) | Very Poor (Difficult to reconstruct end-to-end multi-agent timeline) | High (Prone to circular cascades and race conditions) | **Rejected:** Fails regulatory examination standards. |
| **Two-Tier Hybrid Saga (Adopted)** | **Optimal:** Stream ingestion is asynchronous; escalation sagas are deterministic. | **High:** Kafka guarantees stream durability; Temporal provides durable workflow state recovery. | **Maximum:** Every saga step is recorded in an immutable event ledger. | High (Requires rigorous schema and state machine contracts) | **ACCEPTED:** Selected as the production standard for Meridian Global Bank. |
