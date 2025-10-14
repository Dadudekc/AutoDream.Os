#!/usr/bin/env python3
"""
Query Optimization Helpers
==========================

Helper functions for query optimization system.
Extracted for V2 compliance (<400 lines per file).

Author: Agent-3 - Database Specialist
V2 Compliance: Extracted helper methods
"""

import logging

logger = logging.getLogger(__name__)


def calculate_query_complexity(query: str) -> float:
    """Calculate query complexity score."""
    complexity_factors = {
        "joins": query.upper().count("JOIN") * 0.2,
        "subqueries": query.upper().count("SELECT") - 1 * 0.3,
        "where_conditions": query.upper().count("WHERE") * 0.1,
        "group_by": query.upper().count("GROUP BY") * 0.2,
        "order_by": query.upper().count("ORDER BY") * 0.1,
        "having": query.upper().count("HAVING") * 0.1,
    }
    return min(1.0, sum(complexity_factors.values()))


def simulate_index_usage(index_name: str) -> float:
    """Simulate index usage score (in real implementation, would analyze actual usage)."""
    # Simulate based on index name patterns
    if "agent" in index_name.lower():
        return 0.9  # High usage for agent-related indexes
    elif "message" in index_name.lower():
        return 0.8  # High usage for message-related indexes
    elif "discord" in index_name.lower():
        return 0.7  # Medium usage for Discord-related indexes
    elif "compliance" in index_name.lower():
        return 0.6  # Medium usage for compliance-related indexes
    else:
        return 0.5  # Default medium usage


def suggest_query_rewrite(query: str) -> str:
    """Suggest query rewrite for optimization."""
    # Simple query rewrite suggestions
    if "SELECT *" in query:
        return query.replace("SELECT *", "SELECT specific_columns")  # Suggest specific columns
    elif "WHERE" in query and "ORDER BY" in query:
        return query.replace("ORDER BY", "ORDER BY indexed_column")  # Suggest indexed ordering
    else:
        return query + " -- Consider adding appropriate indexes"


def get_common_queries():
    """Get common query patterns for analysis."""
    return [
        "SELECT * FROM agent_workspaces WHERE team = ?",
        "SELECT * FROM agent_messages WHERE to_agent = ?",
        "SELECT * FROM discord_commands WHERE agent_id = ?",
        "SELECT * FROM v2_compliance_audit WHERE component_name = ?",
        "SELECT * FROM integration_tests WHERE test_type = ?",
    ]


def get_test_queries_with_thresholds():
    """Get test queries with performance thresholds."""
    return [
        {
            "query": "SELECT * FROM agent_workspaces WHERE team = ?",
            "description": "Team-based agent lookup",
            "threshold": 0.01,  # 10ms threshold
        },
        {
            "query": "SELECT * FROM agent_messages WHERE to_agent = ? AND delivery_status = ?",
            "description": "Message delivery status lookup",
            "threshold": 0.02,  # 20ms threshold
        },
        {
            "query": "SELECT COUNT(*) FROM agent_messages WHERE sent_at > ?",
            "description": "Recent message count",
            "threshold": 0.05,  # 50ms threshold
        },
        {
            "query": "SELECT * FROM v2_compliance_audit WHERE compliance_score < ?",
            "description": "Low compliance score lookup",
            "threshold": 0.03,  # 30ms threshold
        },
    ]


def get_validation_queries():
    """Get validation queries for performance testing."""
    return [
        "SELECT * FROM agent_workspaces WHERE team = 'Team Alpha'",
        "SELECT * FROM agent_messages WHERE to_agent = 'Agent-1'",
        "SELECT COUNT(*) FROM v2_compliance_audit WHERE compliance_score < 80",
    ]
