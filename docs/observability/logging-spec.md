# Observability & Structured Logging Taxonomy Specification
**System:** Meridian Global Bank Multi-Agent Compliance Monitoring System (Project 1B)  
**Document Code:** `D7-LS-v1.0`  
**Classification:** Tier-2 Global Banking Architecture  

---

## 1. Structured Logging Taxonomy

All agents, orchestrators, and gateways emit structured JSON logs adhering to OpenTelemetry standards. Logs are categorized into eight statutory domains with minimum retention periods aligned with global financial regulations.

| Log Category | Allowed Severity Levels | Statutory Retention | Representative Events | Primary Target / Consumer |
| :--- | :--- | :---: | :--- | :--- |
| **Agent Lifecycle** | `INFO`, `WARN`, `ERROR`, `FATAL` | **7 Years** | Agent startup, shutdown, health check, schema update | Operations & Platform Engineering |
| **Detection Events** | `INFO`, `WARN`, `ALERT`, `CRITICAL`| **7 Years** *(10 for SAR)* | Pattern detection, threshold breach, model anomaly | Compliance Surveillance Officers |
| **Communication Events**| `DEBUG`, `INFO`, `WARN`, `ERROR` | **5 Years** | Message sent, received, RPC timeout, queue delay | Systems Engineering & Audit |
| **Escalation Events** | `INFO`, `WARN`, `ALERT` | **7 Years** | Escalation triggered, assigned, SLA breach warning | Compliance Management |
| **Human Decision Events**| `INFO`, `ALERT` | **10 Years** | Review initiated, human override, rationale logged | Regulators & Internal Audit |
| **Report Generation** | `INFO`, `WARN`, `ERROR` | **7 Years** *(or per rule)* | Report compiled, validated, signed, filed | Regulators & MLRO |
| **System Performance** | `DEBUG`, `INFO`, `WARN` | **1 Year** *(Rolling)* | Throughput, latency, queue depths, GPU thermals | SRE & Operations Dashboard |
| **Security Events** | `WARN`, `ALERT`, `CRITICAL` | **7 Years** | mTLS auth failure, token expiry, access denied | Security Operations Center (SOC) |

---

## 2. Standardized JSON Log Schema

Every log event conforms to the following structured format:

```json
{
  "timestamp": "2026-10-01T14:32:05.129482Z",
  "log_id": "log-7b8192a0-43cf-418a-821a-12908f921ab0",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "category": "DETECTION_EVENTS",
  "severity": "CRITICAL",
  "source": {
    "agent_id": "TM-01",
    "pod_name": "meridian-tm-core-7f89d-42abc",
    "datacenter": "mumbai-dc1",
    "version": "1.0.0"
  },
  "event_type": "PATTERN_MATCH_SPOOFING",
  "payload": {
    "instrument_symbol": "CL_FUT_2026",
    "venue": "CME",
    "order_id": "ORD-990214",
    "cancellation_latency_ms": 240,
    "order_to_trade_ratio": 47.2,
    "confidence_score": 0.94
  },
  "audit": {
    "classification": "REGULATORY",
    "retention_years": 7,
    "merkle_leaf_hash": "sha256:d8a2...3f1c"
  }
}
```
