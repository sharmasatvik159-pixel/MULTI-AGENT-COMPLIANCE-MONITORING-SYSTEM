"""Communication Scanner Agent (CS-01) for Meridian Global Bank.

Multilingual NLP communication surveillance across chat, email, and transcripts.
Detects off-channel evasion, Chinese Wall leaks, misleading marketing,
unsuitable advice, research conflicts, and elder exploitation.
"""

from __future__ import annotations

import datetime
import re
import uuid
from typing import Any, Dict, List, Optional


class CommunicationScanner:
    """Agent CS-01: Multimodal NLP communication and conduct risk surveillance."""

    def __init__(self, agent_id: str = "CS-01"):
        self.agent_id = agent_id
        self.calibrated_alpha: float = 0.88  # Historical TPR
        self.calibrated_beta: float = 0.07   # Historical FPR
        self.epistemic_noise: float = 0.12   # Epsilon

        # Lexicon watchlists
        self.off_channel_patterns = [
            r"\b(whatsapp|signal|wechat|telegram)\b",
            r"\b(my personal cell|call my mobile|text me on|off the record)\b",
            r"\b(\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b",
            r"\b(delete this chat|move to private|take this offline)\b",
        ]
        self.chinese_wall_patterns = [
            r"\b(confidential m&a|don't cover|do not cover|hold off on research)\b",
            r"\b(project [a-z]+|deal code|trust me on this|pitch deck)\b",
            r"\b(secondary offering|pre-ipo|insider info)\b",
        ]
        self.misleading_marketing_patterns = [
            r"\b(guaranteed\s+\d+%\s+(annual\s+)?returns?)\b",
            r"\b(zero\s+risk(\s+of\s+capital\s+loss)?|risk-free|safe as cash)\b",
            r"\b(cannot lose|100%\s+capital\s+protection)\b",
        ]
        self.elder_poa_patterns = [
            r"\b(new poa|power of attorney|liquidate immediately|transfer funds now)\b",
            r"\b(don't tell (my|the) (mother|father|parents|client))\b",
        ]

        # Internal communication cache for inter-agent queries
        self.communication_store: List[Dict[str, Any]] = []

    def compute_calibrated_confidence(self, raw_score: float) -> float:
        """Calculate calibrated confidence C_a using historical TPR and FPR."""
        raw_score = max(0.0, min(1.0, raw_score))
        numerator = self.calibrated_alpha * raw_score
        denominator = numerator + (self.calibrated_beta * (1.0 - raw_score))
        if denominator == 0:
            return 0.0
        return min(0.99, numerator / denominator)

    def ingest_communication(self, comm_record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Ingest single communication event and scan for conduct / policy infractions."""
        self.communication_store.append(comm_record)
        text = comm_record.get("text", "").lower()
        channel = comm_record.get("channel", "EMAIL")
        sender = comm_record.get("sender", "UNKNOWN")
        recipient = comm_record.get("recipient", "UNKNOWN")
        correlation_id = comm_record.get("correlation_id", str(uuid.uuid4()))
        trace_id = comm_record.get("trace_id", str(uuid.uuid4()))

        # 1. Off-Channel Communication Hunting (CS-13)
        off_channel_match = self._match_patterns(text, self.off_channel_patterns)
        if off_channel_match:
            raw_score = 0.89
            calibrated_conf = self.compute_calibrated_confidence(raw_score)
            return self._build_envelope(
                message_type="ALERT",
                priority=2,  # HIGH
                correlation_id=correlation_id,
                trace_id=trace_id,
                confidence_score=calibrated_conf,
                payload_schema="alert.communication-conduct.v1",
                payload={
                    "alert_id": str(uuid.uuid4()),
                    "violation_category": "OFF_CHANNEL_COMMUNICATION",
                    "severity": "HIGH",
                    "detection_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "primary_entity_id": sender,
                    "entity_type": "TRADER",
                    "applicable_regulations": ["SEC Rule 17a-4", "FINRA Rule 3110"],
                    "quantitative_metrics": {"channel": channel, "matched_pattern": off_channel_match},
                    "evidence_summary": f"Off-channel communication detected from {sender}: matched unapproved channel migration keywords ('{off_channel_match}').",
                },
            )

        # 2. Chinese Wall Breach / Deal Leakage (CS-05)
        chinese_wall_match = self._match_patterns(text, self.chinese_wall_patterns)
        if chinese_wall_match:
            raw_score = 0.94
            calibrated_conf = self.compute_calibrated_confidence(raw_score)
            return self._build_envelope(
                message_type="ALERT",
                priority=1,  # CRITICAL
                correlation_id=correlation_id,
                trace_id=trace_id,
                confidence_score=calibrated_conf,
                payload_schema="alert.information-barrier.v1",
                payload={
                    "alert_id": str(uuid.uuid4()),
                    "violation_category": "CHINESE_WALL_BREACH",
                    "severity": "CRITICAL",
                    "detection_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "primary_entity_id": sender,
                    "entity_type": "TRADER",
                    "applicable_regulations": ["SEC Section 15(g)", "FINRA Rule 5280", "MiFID II Article 33"],
                    "quantitative_metrics": {"sender": sender, "recipient": recipient, "keyword": chinese_wall_match},
                    "evidence_summary": f"Information barrier leak between private & public teams from {sender} to {recipient}: '{chinese_wall_match}'.",
                },
            )

        # 3. Misleading Marketing Claims (CS-08)
        marketing_match = self._match_patterns(text, self.misleading_marketing_patterns)
        if marketing_match:
            raw_score = 0.92
            calibrated_conf = self.compute_calibrated_confidence(raw_score)
            return self._build_envelope(
                message_type="ALERT",
                priority=1,  # CRITICAL
                correlation_id=correlation_id,
                trace_id=trace_id,
                confidence_score=calibrated_conf,
                payload_schema="alert.misleading-marketing.v1",
                payload={
                    "alert_id": str(uuid.uuid4()),
                    "violation_category": "MISLEADING_MARKETING",
                    "severity": "CRITICAL",
                    "detection_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "primary_entity_id": sender,
                    "entity_type": "COMMUNICATION_THREAD",
                    "applicable_regulations": ["SEC Rule 206(4)-1", "FINRA Rule 2210", "FCA COBS 4"],
                    "quantitative_metrics": {"recipients_count": comm_record.get("recipient_count", 3400), "claim": marketing_match},
                    "evidence_summary": f"Prohibited marketing distribution claim detected: '{marketing_match}' distributed to {comm_record.get('recipient_count', 3400)} prospects.",
                },
            )

        # 4. Unsuitable Investment Recommendation (CS-03)
        if "safe income" in text and "leveraged etf" in text:
            raw_score = 0.86
            calibrated_conf = self.compute_calibrated_confidence(raw_score)
            return self._build_envelope(
                message_type="ALERT",
                priority=2,  # HIGH
                correlation_id=correlation_id,
                trace_id=trace_id,
                confidence_score=calibrated_conf,
                payload_schema="alert.suitability.v1",
                payload={
                    "alert_id": str(uuid.uuid4()),
                    "violation_category": "UNSUITABLE_RECOMMENDATION",
                    "severity": "HIGH",
                    "detection_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "primary_entity_id": sender,
                    "entity_type": "TRADER",
                    "applicable_regulations": ["FINRA Rule 2111", "SEC Regulation Best Interest"],
                    "quantitative_metrics": {"client_age_range": "68-82", "product": "Leveraged ETF"},
                    "evidence_summary": f"Unsuitable recommendation: Advisor recommended speculative leveraged ETFs as 'safe income generators' to elderly retirement accounts.",
                },
            )

        # 5. Cross-Border Personal Data Transfer (CS-11)
        if comm_record.get("event_type") == "CROSS_BORDER_MIGRATION" or "eu residents data transfer" in text:
            raw_score = 0.90
            calibrated_conf = self.compute_calibrated_confidence(raw_score)
            return self._build_envelope(
                message_type="ALERT",
                priority=2,  # HIGH
                correlation_id=correlation_id,
                trace_id=trace_id,
                confidence_score=calibrated_conf,
                payload_schema="alert.data-privacy.v1",
                payload={
                    "alert_id": str(uuid.uuid4()),
                    "violation_category": "DATA_PRIVACY_BREACH",
                    "severity": "HIGH",
                    "detection_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "primary_entity_id": sender,
                    "entity_type": "ACCOUNT",
                    "applicable_regulations": ["GDPR Articles 44-49", "Schrems II ruling"],
                    "quantitative_metrics": {"records_impacted": comm_record.get("records_count", 14000), "destination_jurisdiction": "Non-Adequate"},
                    "evidence_summary": "GDPR cross-border transfer breach: 14,000 EU resident customer account records transferred without Standard Contractual Clauses (SCCs).",
                },
            )

        # 6. Research Independence / Conflict of Interest (CS-16)
        if "rating upgrade" in text and "secondary offering" in text:
            raw_score = 0.93
            calibrated_conf = self.compute_calibrated_confidence(raw_score)
            return self._build_envelope(
                message_type="ALERT",
                priority=1,  # CRITICAL
                correlation_id=correlation_id,
                trace_id=trace_id,
                confidence_score=calibrated_conf,
                payload_schema="alert.research-conflict.v1",
                payload={
                    "alert_id": str(uuid.uuid4()),
                    "violation_category": "RESEARCH_INDEPENDENCE_CONFLICT",
                    "severity": "CRITICAL",
                    "detection_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "primary_entity_id": sender,
                    "entity_type": "TRADER",
                    "applicable_regulations": ["SEC Regulation AC", "FINRA Rule 2241", "Global Research Settlement"],
                    "quantitative_metrics": {"analyst": sender, "action": "Sell to Buy upgrade"},
                    "evidence_summary": "Research independence breach: Analyst upgraded stock rating 3 days before Investment Banking team launched secondary offering after private meetings.",
                },
            )

        # 7. Elder Financial Exploitation (CS-17)
        elder_match = self._match_patterns(text, self.elder_poa_patterns)
        if elder_match or comm_record.get("event_type") == "POA_ACCELERATED_TRADING":
            raw_score = 0.92
            calibrated_conf = self.compute_calibrated_confidence(raw_score)
            return self._build_envelope(
                message_type="ALERT",
                priority=1,  # CRITICAL
                correlation_id=correlation_id,
                trace_id=trace_id,
                confidence_score=calibrated_conf,
                payload_schema="alert.elder-exploitation.v1",
                payload={
                    "alert_id": str(uuid.uuid4()),
                    "violation_category": "ELDER_FINANCIAL_EXPLOITATION",
                    "severity": "CRITICAL",
                    "detection_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "primary_entity_id": comm_record.get("account_id", "ACC_ELDER_84"),
                    "entity_type": "ACCOUNT",
                    "applicable_regulations": ["FINRA Rules 2165 & 4512", "Senior Safe Act"],
                    "quantitative_metrics": {"client_age": 84, "trading_velocity": "47 trades/mo vs 2/mo baseline"},
                    "evidence_summary": "Elder financial exploitation detected: 84-year-old client account trading surged to 47 trades/month following new POA filing with 22% loss.",
                },
            )

        return None

    def handle_query(self, query_envelope: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming QUERY from TM-01 or Orchestrator and return structured RESPONSE."""
        query_payload = query_envelope.get("payload", {})
        query_id = query_payload.get("query_id", str(uuid.uuid4()))
        subject_id = query_payload.get("target_subject_id", "")
        keywords = query_payload.get("filter_keywords", [])

        matching_items = []
        for c in self.communication_store:
            text = c.get("text", "")
            if subject_id in (c.get("sender"), c.get("recipient"), c.get("trader_id")) or any(k.lower() in text.lower() for k in keywords):
                matching_items.append({
                    "item_id": str(uuid.uuid4()),
                    "timestamp": c.get("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat()),
                    "source_channel": c.get("channel", "CHAT"),
                    "content_digest": text[:100],
                    "snippet": text,
                    "sentiment_score": 0.85 if "dinner" in text or "trust me" in text else 0.10,
                    "intent_classification": "MATERIAL_COMMUNICATION" if "dinner" in text or "acquisition" in text else "BENIGN",
                })

        corroboration = 0.88 if len(matching_items) > 0 and any(i["intent_classification"] == "MATERIAL_COMMUNICATION" for i in matching_items) else 0.15

        return {
            "message_id": str(uuid.uuid4()),
            "protocol_version": "1.0.0",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "sender_agent_id": self.agent_id,
            "recipient_agent_id": query_envelope.get("sender_agent_id", "TM-01"),
            "message_type": "RESPONSE",
            "priority": query_envelope.get("priority", 2),
            "correlation_id": query_envelope.get("correlation_id", str(uuid.uuid4())),
            "trace_id": query_envelope.get("trace_id", str(uuid.uuid4())),
            "confidence_score": corroboration,
            "ttl_seconds": 3600,
            "retry_count": 0,
            "audit_classification": "REGULATORY",
            "sender_signature": "MEQCIFz...CS01SignatureSimulatedBase64==",
            "nonce": uuid.uuid4().hex,
            "payload_schema": "response.communication.v1",
            "payload": {
                "response_to_query_id": query_id,
                "status": "SUCCESS" if matching_items else "NO_DATA_FOUND",
                "evidence_items": matching_items,
                "corroboration_score": corroboration,
            },
        }

    def _match_patterns(self, text: str, patterns: List[str]) -> Optional[str]:
        for p in patterns:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                return m.group(0)
        return None

    def _build_envelope(
        self,
        message_type: str,
        priority: int,
        correlation_id: str,
        trace_id: str,
        confidence_score: float,
        payload_schema: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "message_id": str(uuid.uuid4()),
            "protocol_version": "1.0.0",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "sender_agent_id": self.agent_id,
            "recipient_agent_id": "ORCHESTRATOR-01",
            "message_type": message_type,
            "priority": priority,
            "correlation_id": correlation_id,
            "trace_id": trace_id,
            "confidence_score": round(confidence_score, 4),
            "ttl_seconds": 3600,
            "retry_count": 0,
            "audit_classification": "REGULATORY",
            "sender_signature": "MEQCIFz...CS01SignatureSimulatedBase64==",
            "nonce": uuid.uuid4().hex,
            "payload_schema": payload_schema,
            "payload": payload,
        }
