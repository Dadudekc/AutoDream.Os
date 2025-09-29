#!/usr/bin/env python3
"""
Canonical Text Builders
=======================

Builds consistent canonical text representations for embedding.
V2 Compliance: ≤400 lines, focused text building functionality.
"""

import json
from typing import Any


def canonical_action(
    title: str, outcome: str, tool: str, context: dict[str, Any], summary: str, tags: list[str]
) -> str:
    """Build canonical text for an action."""
    lines = [
        f"[ACTION] {title}",
        f"Tool: {tool}",
        f"Outcome: {outcome}",
        f"Summary: {summary}",
        f"Tags: {', '.join(tags)}",
        f"Context: {json.dumps(context, indent=2)}",
    ]
    return "\n".join(lines)


def canonical_protocol(
    title: str,
    steps: list[str],
    effectiveness: float,
    improvements: dict[str, Any],
    summary: str,
    tags: list[str],
) -> str:
    """Build canonical text for a protocol."""
    lines = [
        f"[PROTOCOL] {title}",
        f"Effectiveness: {effectiveness:.3f}",
        f"Summary: {summary}",
        f"Tags: {', '.join(tags)}",
        f"Steps: {json.dumps(steps, indent=2)}",
        f"Improvements: {json.dumps(improvements, indent=2)}",
    ]
    return "\n".join(lines)


def canonical_workflow(
    title: str,
    execution_pattern: dict[str, Any],
    coordination: dict[str, Any],
    outcomes: dict[str, Any],
    optimization: dict[str, Any],
    summary: str,
    tags: list[str],
) -> str:
    """Build canonical text for a workflow."""
    lines = [
        f"[WORKFLOW] {title}",
        f"Summary: {summary}",
        f"Tags: {', '.join(tags)}",
        f"Execution Pattern: {json.dumps(execution_pattern, indent=2)}",
        f"Coordination: {json.dumps(coordination, indent=2)}",
        f"Outcomes: {json.dumps(outcomes, indent=2)}",
        f"Optimization: {json.dumps(optimization, indent=2)}",
    ]
    return "\n".join(lines)


def canonical_performance(
    title: str,
    metrics: dict[str, Any],
    anomalies: dict[str, Any],
    optimizations: dict[str, Any],
    trends: dict[str, Any],
    summary: str,
    tags: list[str],
) -> str:
    """Build canonical text for performance data."""
    lines = [
        f"[PERFORMANCE] {title}",
        f"Summary: {summary}",
        f"Tags: {', '.join(tags)}",
        f"Metrics: {json.dumps(metrics, indent=2)}",
        f"Anomalies: {json.dumps(anomalies, indent=2)}",
        f"Optimizations: {json.dumps(optimizations, indent=2)}",
        f"Trends: {json.dumps(trends, indent=2)}",
    ]
    return "\n".join(lines)


def canonical_conversation(
    title: str, channel: str, role: str, content: str, summary: str, tags: list[str]
) -> str:
    """Build canonical text for a conversation."""
    # Truncate content if too long
    content_preview = content[:1000] + "..." if len(content) > 1000 else content

    lines = [
        f"[CONVERSATION] {title}",
        f"Channel: {channel}",
        f"Role: {role}",
        f"Summary: {summary}",
        f"Tags: {', '.join(tags)}",
        f"Content: {content_preview}",
    ]
    return "\n".join(lines)


def canonical_coordination(
    title: str,
    coordination_type: str,
    participants: list[str],
    coordination_data: dict[str, Any],
    effectiveness: float,
    summary: str,
    tags: list[str],
) -> str:
    """Build canonical text for coordination data."""
    lines = [
        f"[COORDINATION] {title}",
        f"Type: {coordination_type}",
        f"Effectiveness: {effectiveness:.3f}",
        f"Summary: {summary}",
        f"Tags: {', '.join(tags)}",
        f"Participants: {', '.join(participants)}",
        f"Coordination Data: {json.dumps(coordination_data, indent=2)}",
    ]
    return "\n".join(lines)


def canonical_tool(
    title: str,
    usage_pattern: str,
    success_rate: float,
    failure_modes: list[str],
    optimizations: list[str],
    summary: str,
    tags: list[str],
) -> str:
    """Build canonical text for tool usage data."""
    lines = [
        f"[TOOL] {title}",
        f"Usage Pattern: {usage_pattern}",
        f"Success Rate: {success_rate:.3f}",
        f"Summary: {summary}",
        f"Tags: {', '.join(tags)}",
        f"Failure Modes: {json.dumps(failure_modes, indent=2)}",
        f"Optimizations: {json.dumps(optimizations, indent=2)}",
    ]
    return "\n".join(lines)
