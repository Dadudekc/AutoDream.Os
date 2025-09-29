#!/usr/bin/env python3
"""
Swarm Brain Decorators
======================

Decorators for automatic agent activity recording.
V2 Compliance: ≤400 lines, focused decorator functionality.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from .ingest import Ingestor

logger = logging.getLogger(__name__)

# Global ingestor instance
_ingestor = Ingestor()


def vectorized_action(tool: str, project: str, agent_id: str, tags: list[str]):
    """
    Decorator to automatically record agent actions.

    Args:
        tool: Tool name being used
        project: Project identifier
        agent_id: Agent identifier
        tags: List of tags for categorization
    """

    def decorator(fn: Callable[..., Any]):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            outcome = "success"
            summary = ""
            context = {"args": str(args), "kwargs": str(kwargs)}

            try:
                result = fn(*args, **kwargs)

                # Extract summary from result if available
                if hasattr(result, "summary"):
                    summary = result.summary
                elif isinstance(result, dict) and "summary" in result:
                    summary = result["summary"]
                elif isinstance(result, str):
                    summary = result[:200]  # Truncate if too long

                return result

            except Exception as e:
                outcome = "failure"
                summary = f"Exception: {str(e)}"
                logger.error(f"Action failed in {fn.__name__}: {e}")
                raise

            finally:
                # Record the action
                duration_ms = int((time.time() - start_time) * 1000)

                try:
                    _ingestor.action(
                        title=f"{tool} execution",
                        tool=tool,
                        outcome=outcome,
                        context=context,
                        project=project,
                        agent_id=agent_id,
                        tags=tags,
                        summary=summary,
                        duration_ms=duration_ms,
                    )
                except Exception as e:
                    logger.error(f"Failed to record action: {e}")

        return wrapper

    return decorator


def vectorized_protocol(
    project: str,
    agent_id: str,
    tags: list[str],
    steps: list[str],
    title: str,
    effectiveness: float = 0.0,
):
    """
    Decorator to record protocol usage.

    Args:
        project: Project identifier
        agent_id: Agent identifier
        tags: List of tags
        steps: Protocol steps
        title: Protocol title
        effectiveness: Initial effectiveness score
    """

    def record_protocol(improvements: dict[str, Any] = None, summary: str = ""):
        """Record protocol execution."""
        try:
            _ingestor.protocol(
                title=title,
                steps=steps,
                effectiveness=effectiveness,
                improvements=improvements or {},
                project=project,
                agent_id=agent_id,
                tags=tags,
                summary=summary,
            )
        except Exception as e:
            logger.error(f"Failed to record protocol: {e}")

    return record_protocol


def vectorized_workflow(project: str, agent_id: str, tags: list[str], title: str):
    """
    Decorator to record workflow execution.

    Args:
        project: Project identifier
        agent_id: Agent identifier
        tags: List of tags
        title: Workflow title
    """

    def record_workflow(
        execution_pattern: dict[str, Any],
        coordination: dict[str, Any],
        outcomes: dict[str, Any],
        optimization: dict[str, Any],
        summary: str = "",
    ):
        """Record workflow execution."""
        try:
            _ingestor.workflow(
                title=title,
                execution_pattern=execution_pattern,
                coordination=coordination,
                outcomes=outcomes,
                optimization=optimization,
                project=project,
                agent_id=agent_id,
                tags=tags,
                summary=summary,
            )
        except Exception as e:
            logger.error(f"Failed to record workflow: {e}")

    return record_workflow


def vectorized_performance(project: str, agent_id: str, tags: list[str]):
    """
    Decorator to record performance data.

    Args:
        project: Project identifier
        agent_id: Agent identifier
        tags: List of tags
    """

    def record_performance(
        metrics: dict[str, Any],
        anomalies: dict[str, Any] = None,
        optimizations: dict[str, Any] = None,
        trends: dict[str, Any] = None,
        title: str = "Performance Snapshot",
        summary: str = "",
    ):
        """Record performance data."""
        try:
            _ingestor.performance(
                title=title,
                metrics=metrics,
                anomalies=anomalies or {},
                optimizations=optimizations or {},
                trends=trends or {},
                project=project,
                agent_id=agent_id,
                tags=tags,
                summary=summary,
            )
        except Exception as e:
            logger.error(f"Failed to record performance: {e}")

    return record_performance


def vectorized_conversation(project: str, agent_id: str, tags: list[str]):
    """
    Decorator to record conversations.

    Args:
        project: Project identifier
        agent_id: Agent identifier
        tags: List of tags
    """

    def record_conversation(
        channel: str,
        thread_id: str,
        role: str,
        content: str,
        title: str = "Conversation",
        summary: str = "",
    ):
        """Record conversation."""
        try:
            _ingestor.conversation(
                title=title,
                channel=channel,
                thread_id=thread_id,
                role=role,
                content=content,
                project=project,
                agent_id=agent_id,
                tags=tags,
                summary=summary,
            )
        except Exception as e:
            logger.error(f"Failed to record conversation: {e}")

    return record_conversation


def vectorized_coordination(project: str, agent_id: str, tags: list[str]):
    """
    Decorator to record coordination activities.

    Args:
        project: Project identifier
        agent_id: Agent identifier
        tags: List of tags
    """

    def record_coordination(
        coordination_type: str,
        participants: list[str],
        coordination_data: dict[str, Any],
        effectiveness: float,
        title: str = "Coordination",
        summary: str = "",
    ):
        """Record coordination activity."""
        try:
            _ingestor.coordination(
                title=title,
                coordination_type=coordination_type,
                participants=participants,
                coordination_data=coordination_data,
                effectiveness=effectiveness,
                project=project,
                agent_id=agent_id,
                tags=tags,
                summary=summary,
            )
        except Exception as e:
            logger.error(f"Failed to record coordination: {e}")

    return record_coordination


def vectorized_tool(project: str, agent_id: str, tags: list[str]):
    """
    Decorator to record tool usage patterns.

    Args:
        project: Project identifier
        agent_id: Agent identifier
        tags: List of tags
    """

    def record_tool(
        usage_pattern: str,
        success_rate: float,
        failure_modes: list[str] = None,
        optimizations: list[str] = None,
        title: str = "Tool Usage",
        summary: str = "",
    ):
        """Record tool usage."""
        try:
            _ingestor.tool(
                title=title,
                usage_pattern=usage_pattern,
                success_rate=success_rate,
                failure_modes=failure_modes or [],
                optimizations=optimizations or [],
                project=project,
                agent_id=agent_id,
                tags=tags,
                summary=summary,
            )
        except Exception as e:
            logger.error(f"Failed to record tool usage: {e}")

    return record_tool
