#!/usr/bin/env python3
"""
Observability Metrics
=====================

Centralized metrics collection for all swarm systems.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

from collections import Counter

# Global metrics counter
METRICS = Counter()


def incr(key: str, n: int = 1):
    """
    Increment metric counter.

    Args:
        key: Metric key (e.g., "ingest.ok", "msg.sent")
        n: Increment amount
    """
    METRICS[key] += n


def decr(key: str, n: int = 1):
    """Decrement metric counter."""
    METRICS[key] -= n


def set_metric(key: str, value: int):
    """Set metric to specific value."""
    METRICS[key] = value


def snapshot() -> dict[str, int]:
    """Get current metrics snapshot."""
    return dict(METRICS)


def reset():
    """Reset all metrics."""
    METRICS.clear()


def get(key: str, default: int = 0) -> int:
    """Get specific metric value."""
    return METRICS.get(key, default)


def dump_metrics() -> str:
    """
    Dump metrics as formatted string.

    Returns:
        Formatted metrics output
    """
    metrics = snapshot()
    if not metrics:
        return "No metrics recorded"

    lines = [f"📊 Metrics ({len(metrics)} counters):"]
    lines.append("=" * 50)

    for key in sorted(metrics.keys()):
        lines.append(f"  {key}: {metrics[key]}")

    return "\n".join(lines)


# Message-Task specific metrics
def log_ingest_success():
    """Log successful message ingestion."""
    incr("msg_task.ingest.ok")


def log_ingest_failure():
    """Log failed message ingestion."""
    incr("msg_task.ingest.fail")


def log_ingest_duplicate():
    """Log duplicate task detected."""
    incr("msg_task.dedupe.duplicate")


def log_parser_used(parser_name: str):
    """Log which parser was used."""
    incr(f"msg_task.parser.{parser_name}")


# OSS specific metrics
def log_oss_clone_success():
    """Log successful OSS project clone."""
    incr("oss.clone.ok")


def log_oss_clone_failure():
    """Log failed OSS project clone."""
    incr("oss.clone.fail")


def log_oss_pr_submitted():
    """Log OSS PR submission."""
    incr("oss.pr.submitted")


def log_oss_pr_merged():
    """Log OSS PR merge."""
    incr("oss.pr.merged")


# Messaging specific metrics
def log_message_sent():
    """Log message sent."""
    incr("messaging.sent")


def log_message_failed():
    """Log message send failure."""
    incr("messaging.failed")


def log_race_condition_prevented():
    """Log race condition prevention via lock."""
    incr("messaging.race_prevented")
