"""Mock Streaming Data Engine for Meridian Global Bank Compliance Surveillance.

Simulates high-velocity multi-source ingestion feeds:
1. FIX 5.0 and UPI core trading transactions (2.4M daily scale).
2. Bloomberg, Symphony, Teams, and WhatsApp communications (850k daily scale).
3. Global regulatory circulars and OFAC SDN sanctions broadcasts.
Contains pre-configured event payloads for all 20 compliance scenarios (CS-01 to CS-20).
"""

from __future__ import annotations

import datetime
import uuid
from typing import Any, Dict, Generator, List


class MockStreamGenerator:
    """Generates synthetic high-velocity streaming records and deterministic scenario packages."""

    def __init__(self):
        self.scenario_database: Dict[str, Dict[str, Any]] = self._init_scenario_database()

    def get_scenario_event_bundle(self, scenario_id: str) -> Dict[str, Any]:
        """Fetch the pre-configured deterministic event package for a specific scenario (CS-01 to CS-20)."""
        sid = scenario_id.upper().strip()
        if sid not in self.scenario_database:
            raise ValueError(f"Unknown scenario ID: {scenario_id}. Must be CS-01 through CS-20.")
        return self.scenario_database[sid]

    def generate_random_trade_stream(self, count: int = 100) -> Generator[Dict[str, Any], None, None]:
        """Generate high-velocity baseline transaction stream."""
        symbols = ["AAPL", "MSFT", "NVDA", "JPM", "GS", "CL_FUT_2026", "EURUSD", "INFY.NSE"]
        for i in range(count):
            yield {
                "event_id": str(uuid.uuid4()),
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "event_type": "TRADE_EXECUTION",
                "feed_type": "FIX_5_0",
                "correlation_id": str(uuid.uuid4()),
                "trace_id": str(uuid.uuid4()),
                "payload": {
                    "trade_id": f"TRD-{uuid.uuid4().hex[:8].upper()}",
                    "account_id": f"ACC-{1000 + (i % 50)}",
                    "symbol": symbols[i % len(symbols)],
                    "quantity": 100 * ((i % 10) + 1),
                    "price": 150.0 + (i * 0.25),
                    "venue": "NASDAQ",
                },
            }

    def _init_scenario_database(self) -> Dict[str, Dict[str, Any]]:
        """Define complete deterministic payloads for CS-01 through CS-20."""
        return {
            "CS-01": {
                "name": "Insider Trading - Pre-Announcement Accumulation",
                "primary_agents": ["TM-01", "CS-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "COMMUNICATION",
                        "channel": "OUTLOOK_EMAIL",
                        "sender": "pm_marcus@meridian.bank",
                        "recipient": "cfo@companyx.com",
                        "text": "Thank you for the private dinner meeting yesterday. Very excited about Company X strategic acquisition plans.",
                        "timestamp": "2026-09-02T19:30:00Z",
                    },
                    {
                        "source": "TRANSACTION",
                        "event_type": "TRADE_EXECUTION",
                        "payload": {
                            "trader_id": "pm_marcus@meridian.bank",
                            "symbol": "CMPX",
                            "shares_accumulated": 450000,
                            "price_surge_pct": 35.0,
                            "acquisition_announced_days_later": 2,
                            "historical_win_rate_pct": 89.0,
                            "precedes_client_order_minutes": 15,
                        },
                    },
                ],
            },
            "CS-02": {
                "name": "Market Manipulation - Futures Spoofing",
                "primary_agents": ["TM-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "TRANSACTION",
                        "event_type": "ORDER_CANCEL",
                        "payload": {
                            "desk_id": "DESK_ALGO_CRUDE",
                            "symbol": "CL_FUT_2026",
                            "order_to_trade_ratio": 47.0,
                            "cancellation_latency_ms": 220,
                            "cancellations_count": 47,
                            "executed_opposite_side": True,
                        },
                    }
                ],
            },
            "CS-03": {
                "name": "Unsuitable Investment Recommendation",
                "primary_agents": ["CS-01", "TM-01"],
                "expected_outcome": "HIGH_ALERT",
                "escalation_tier": "TIER_2_SENIOR_ANALYST",
                "events": [
                    {
                        "source": "COMMUNICATION",
                        "channel": "TEAMS_CHAT",
                        "sender": "advisor_smith@meridian.bank",
                        "recipient": "client_retiree_74@meridian.bank",
                        "text": "I strongly recommend investing in our 3x leveraged ETF products. These are completely safe income generators for your retirement pension.",
                    }
                ],
            },
            "CS-04": {
                "name": "AML - Structuring Deposits (Smurfing)",
                "primary_agents": ["TM-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "TRANSACTION",
                        "event_type": "CASH_DEPOSIT",
                        "payload": {
                            "client_id": "COMM_CLI_SMURF_01",
                            "deposits_count": 23,
                            "deposit_amount_range": (8500, 9900),
                            "total_amount_usd": 214000.0,
                            "branches_count": 7,
                            "business_days": 10,
                        },
                    }
                ],
            },
            "CS-05": {
                "name": "Chinese Wall Breach - Information Leakage",
                "primary_agents": ["CS-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "COMMUNICATION",
                        "channel": "SYMPHONY_CHAT",
                        "sender": "ib_banker_deal@meridian.bank",
                        "recipient": "research_analyst@meridian.bank",
                        "text": "Confidential M&A alert: Don't cover TechCorp next week, trust me on this deal code Project Apollo.",
                    }
                ],
            },
            "CS-06": {
                "name": "Wash Trading - Cross-Account Coordination",
                "primary_agents": ["TM-01"],
                "expected_outcome": "HIGH_ALERT",
                "escalation_tier": "TIER_2_SENIOR_ANALYST",
                "events": [
                    {
                        "source": "TRANSACTION",
                        "event_type": "TRADE_EXECUTION",
                        "payload": {
                            "account_group_id": "ACC_GRP_WASH_BOND",
                            "symbol": "CORP_BOND_44",
                            "is_matched_internal": True,
                            "price_diff_bps": 1.2,
                            "matching_trades_count": 34,
                            "duration_days": 14,
                        },
                    }
                ],
            },
            "CS-07": {
                "name": "Regulatory Change Impact - Swap Margins",
                "primary_agents": ["RU-01"],
                "expected_outcome": "MEDIUM_ALERT",
                "escalation_tier": "TIER_1_ANALYST",
                "events": [
                    {
                        "source": "REGULATORY",
                        "update_type": "MARGIN_REQUIREMENT_RULE",
                        "payload": {
                            "initial_margin_increase_pct": 25.0,
                            "effective_days": 120,
                            "regulator": "SEC",
                            "statute": "Swap Margin Rule",
                        },
                    }
                ],
            },
            "CS-08": {
                "name": "Client Communication - Misleading Performance Claims",
                "primary_agents": ["CS-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_2_SENIOR_ANALYST",
                "events": [
                    {
                        "source": "COMMUNICATION",
                        "channel": "MARKETING_EMAIL_BLAST",
                        "sender": "marketing_wealth@meridian.bank",
                        "recipient_count": 3400,
                        "text": "Exclusive offering: Guaranteed 12% annual returns with zero risk of capital loss in all macroeconomic environments.",
                    }
                ],
            },
            "CS-09": {
                "name": "Sanctions Violation - Indirect Exposure",
                "primary_agents": ["TM-01", "RU-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_4_CCO_BOARD",
                "events": [
                    {
                        "source": "REGULATORY",
                        "update_type": "SANCTIONS_UPDATE",
                        "payload": {
                            "entity_name": "GLOBAL_TRANS_LOGISTICS",
                            "sdn_id": "OFAC-SDN-9941",
                            "subsidiaries": ["MARITIME_CARRIER_SUB_01"],
                        },
                    },
                    {
                        "source": "TRANSACTION",
                        "event_type": "WIRE_TRANSFER",
                        "payload": {
                            "beneficiary_name": "MARITIME_CARRIER_SUB_01",
                            "intermediary_banks_count": 3,
                            "amount_usd": 14500000.0,
                            "currency": "USD",
                        },
                    },
                ],
            },
            "CS-10": {
                "name": "Front-Running - Client Order Anticipation",
                "primary_agents": ["TM-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "TRANSACTION",
                        "event_type": "TRADE_EXECUTION",
                        "payload": {
                            "trader_id": "TRD_PROP_DESK_09",
                            "symbol": "MEGA_CAP_TECH",
                            "precedes_client_order_minutes": 18,
                            "historical_profit_rate_pct": 89.0,
                            "avg_trade_return_pct": 2.3,
                        },
                    }
                ],
            },
            "CS-11": {
                "name": "Data Privacy Violation - Cross-Border Transfer",
                "primary_agents": ["CS-01", "RU-01"],
                "expected_outcome": "HIGH_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "COMMUNICATION",
                        "event_type": "CROSS_BORDER_MIGRATION",
                        "records_count": 14000,
                        "text": "Routine EU residents data transfer executed to offshore cloud facility without standard contractual clauses.",
                    }
                ],
            },
            "CS-12": {
                "name": "Concentration Risk - Portfolio Limit Breach",
                "primary_agents": ["TM-01"],
                "expected_outcome": "MEDIUM_ALERT",
                "escalation_tier": "TIER_1_ANALYST",
                "events": [
                    {
                        "source": "TRANSACTION",
                        "event_type": "PORTFOLIO_UPDATE",
                        "payload": {
                            "fund_id": "MERIDIAN_GLOBAL_EQUITY_FUND",
                            "sector_concentration_pct": 28.0,
                            "sector_limit_pct": 25.0,
                            "days_persisted": 5,
                        },
                    }
                ],
            },
            "CS-13": {
                "name": "Off-Channel Communication - Personal WhatsApp",
                "primary_agents": ["CS-01"],
                "expected_outcome": "HIGH_ALERT",
                "escalation_tier": "TIER_2_SENIOR_ANALYST",
                "events": [
                    {
                        "source": "COMMUNICATION",
                        "channel": "BLOOMBERG_CHAT",
                        "sender": "registered_rep_01@meridian.bank",
                        "text": "Don't discuss the investment recommendation here. Please WhatsApp me at +1-917-555-0199 right away.",
                    }
                ],
            },
            "CS-14": {
                "name": "Late Trading - Mutual Fund NAV Manipulation",
                "primary_agents": ["TM-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "TRANSACTION",
                        "event_type": "MUTUAL_FUND_ORDER",
                        "payload": {
                            "broker_id": "BRK_LATE_EXEC",
                            "stamped_time": "16:00:00",
                            "system_entry_time": "16:18:22",
                            "pricing_nav": "SAME_DAY",
                            "orders_count": 14,
                        },
                    }
                ],
            },
            "CS-15": {
                "name": "Best Execution Failure - Routing Bias",
                "primary_agents": ["TM-01"],
                "expected_outcome": "HIGH_ALERT",
                "escalation_tier": "TIER_2_SENIOR_ANALYST",
                "events": [
                    {
                        "source": "TRANSACTION",
                        "event_type": "ROUTING_AUDIT",
                        "payload": {
                            "routing_desk_id": "EQUITY_ROUTING_DESK_US",
                            "pfof_venue_routing_pct": 78.0,
                            "price_inferiority_cents": 1.2,
                            "better_venues_count": 3,
                        },
                    }
                ],
            },
            "CS-16": {
                "name": "Conflict of Interest - Research Independence",
                "primary_agents": ["CS-01", "TM-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "COMMUNICATION",
                        "channel": "INTERNAL_EMAIL",
                        "sender": "research_head@meridian.bank",
                        "recipient": "ib_director@meridian.bank",
                        "text": "Confirming our meeting. I have completed the rating upgrade from Sell to Buy immediately prior to your secondary offering launch.",
                    }
                ],
            },
            "CS-17": {
                "name": "Elder Financial Exploitation",
                "primary_agents": ["TM-01", "CS-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_3_COMPLIANCE_MANAGER",
                "events": [
                    {
                        "source": "COMMUNICATION",
                        "event_type": "POA_ACCELERATED_TRADING",
                        "account_id": "ACC_SENIOR_84_POA",
                        "text": "New power of attorney instructions: liquidate entire conservative bond portfolio immediately and execute speculative derivative trades.",
                    }
                ],
            },
            "CS-18": {
                "name": "FALSE POSITIVE - Legitimate Institutional Block Trade",
                "primary_agents": ["TM-01"],
                "expected_outcome": "SUPPRESSED_ALERT",
                "escalation_tier": "NONE",
                "events": [
                    {
                        "source": "TRANSACTION",
                        "event_type": "TRADE_EXECUTION",
                        "payload": {
                            "client_id": "INSTITUTIONAL_PENSION_01",
                            "notional_usd": 450000000.0,
                            "pct_adv": 8.0,
                            "pre_clearance_ticket_id": "TICKET-BLK-2026-9021",
                        },
                    }
                ],
            },
            "CS-19": {
                "name": "Multi-Jurisdiction Regulatory Conflict",
                "primary_agents": ["RU-01"],
                "expected_outcome": "HIGH_ALERT",
                "escalation_tier": "TIER_4_CCO_BOARD",
                "events": [
                    {
                        "source": "REGULATORY",
                        "update_type": "CROSS_JURISDICTION_CONFLICT_CHECK",
                        "payload": {
                            "jurisdiction_a": "EU_EMIR",
                            "jurisdiction_b": "SINGAPORE_MAS",
                            "conflict_check": True,
                            "affected_clients_count": 450,
                        },
                    }
                ],
            },
            "CS-20": {
                "name": "COORDINATED - Trade-Based Money Laundering",
                "primary_agents": ["TM-01", "CS-01", "RU-01", "RG-01"],
                "expected_outcome": "CRITICAL_ALERT",
                "escalation_tier": "TIER_4_CCO_BOARD",
                "events": [
                    {
                        "source": "REGULATORY",
                        "update_type": "SANCTIONS_UPDATE",
                        "payload": {
                            "entity_name": "PORT_AUTHORITY_PACIFIC",
                            "sdn_id": "OFAC-SDN-8812",
                            "subsidiaries": ["PACIFIC_SHIPPING_CORP"],
                        },
                    },
                    {
                        "source": "COMMUNICATION",
                        "channel": "INTERNAL_EMAIL",
                        "sender": "rm_wealth_desk@meridian.bank",
                        "text": "I have manually overrode the compliance screening flags twice for this trade finance letter of credit. Proceed with wire transfer.",
                    },
                    {
                        "source": "TRANSACTION",
                        "event_type": "WIRE_TRANSFER",
                        "payload": {
                            "client_id": "TBML_CLIENT_TRADE_FINANCE",
                            "goods_market_markup_pct": 300.0,
                            "intermediary_banks_count": 5,
                            "beneficiary_name": "PACIFIC_SHIPPING_CORP",
                            "amount_usd": 48500000.0,
                        },
                    },
                ],
            },
        }
