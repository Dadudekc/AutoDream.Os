#!/usr/bin/env python3
"""
Swarm Brain Ingestion Layer
===========================

High-level ingestion API for recording agent activities.
V2 Compliance: ≤400 lines, focused ingestion functionality.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from .canon import (
    canonical_action,
    canonical_conversation,
    canonical_coordination,
    canonical_performance,
    canonical_protocol,
    canonical_tool,
    canonical_workflow,
)
from .config import CONFIG
from .db import SwarmBrain
from .embeddings.numpy_backend import NumpyBackend

logger = logging.getLogger(__name__)


def _get_backend():
    """Get the configured embedding backend."""
    # For now, use numpy backend as default
    return NumpyBackend(CONFIG.index_path, CONFIG.dim)


class Ingestor:
    """High-level ingestion API for swarm intelligence."""

    def __init__(self, brain: SwarmBrain | None = None):
        """Initialize the ingestor."""
        self.brain = brain or SwarmBrain()
        self.backend = _get_backend()
        logger.info("Swarm Brain Ingestor initialized")

    def _embed_and_mark(self, doc_id: int, canonical: str):
        """Embed canonical text and mark as embedded."""
        try:
            vectors = self.backend.embed_texts([canonical])
            self.backend.add([doc_id], vectors)
            self.backend.persist()

            # Mark as embedded in database
            norm = float(np.linalg.norm(vectors[0]))
            self.brain.mark_embedded(doc_id, backend="numpy", dim=vectors.shape[1], norm=norm)

        except Exception as e:
            logger.error(f"Failed to embed document {doc_id}: {e}")

    def action(
        self,
        *,
        title: str,
        tool: str,
        outcome: str,
        context: dict[str, Any],
        project: str,
        agent_id: str,
        tags: list[str],
        summary: str = "",
        ref_id: str = None,
        ts: int = None,
        duration_ms: int = None,
    ) -> int:
        """Record an agent action."""
        canonical = canonical_action(title, outcome, tool, context, summary, tags)

        doc_id = self.brain.upsert_document(
            kind="action",
            ts=ts,
            title=title,
            summary=summary,
            tags=tags,
            meta=context,
            canonical=canonical,
            project=project,
            agent_id=agent_id,
            ref_id=ref_id,
        )

        # Insert action-specific data
        self.brain.insert_lens(
            "actions",
            doc_id,
            {
                "tool": tool,
                "outcome": outcome,
                "context": json.dumps(context),
                "duration_ms": duration_ms or 0,
            },
        )

        self._embed_and_mark(doc_id, canonical)
        logger.debug(f"Recorded action: {title} by {agent_id}")
        return doc_id

    def protocol(
        self,
        *,
        title: str,
        steps: list[str],
        effectiveness: float,
        improvements: dict[str, Any],
        project: str,
        agent_id: str,
        tags: list[str],
        summary: str = "",
        ref_id: str = None,
        ts: int = None,
    ) -> int:
        """Record a protocol."""
        canonical = canonical_protocol(title, steps, effectiveness, improvements, summary, tags)

        doc_id = self.brain.upsert_document(
            kind="protocol",
            ts=ts,
            title=title,
            summary=summary,
            tags=tags,
            meta={"improvements": improvements, "steps": steps},
            canonical=canonical,
            project=project,
            agent_id=agent_id,
            ref_id=ref_id,
        )

        # Insert protocol-specific data
        self.brain.insert_lens(
            "protocols",
            doc_id,
            {
                "steps": json.dumps(steps),
                "effectiveness": effectiveness,
                "improvements": json.dumps(improvements),
                "adaptation_history": json.dumps([]),
            },
        )

        self._embed_and_mark(doc_id, canonical)
        logger.debug(f"Recorded protocol: {title} by {agent_id}")
        return doc_id

    def workflow(
        self,
        *,
        title: str,
        execution_pattern: dict[str, Any],
        coordination: dict[str, Any],
        outcomes: dict[str, Any],
        optimization: dict[str, Any],
        project: str,
        agent_id: str,
        tags: list[str],
        summary: str = "",
        ref_id: str = None,
        ts: int = None,
    ) -> int:
        """Record a workflow execution."""
        canonical = canonical_workflow(
            title, execution_pattern, coordination, outcomes, optimization, summary, tags
        )

        doc_id = self.brain.upsert_document(
            kind="workflow",
            ts=ts,
            title=title,
            summary=summary,
            tags=tags,
            meta={"exec": execution_pattern, "coord": coordination},
            canonical=canonical,
            project=project,
            agent_id=agent_id,
            ref_id=ref_id,
        )

        # Insert workflow-specific data
        self.brain.insert_lens(
            "workflows",
            doc_id,
            {
                "execution_pattern": json.dumps(execution_pattern),
                "coordination": json.dumps(coordination),
                "outcomes": json.dumps(outcomes),
                "optimization": json.dumps(optimization),
            },
        )

        self._embed_and_mark(doc_id, canonical)
        logger.debug(f"Recorded workflow: {title} by {agent_id}")
        return doc_id

    def performance(
        self,
        *,
        title: str,
        metrics: dict[str, Any],
        anomalies: dict[str, Any],
        optimizations: dict[str, Any],
        trends: dict[str, Any],
        project: str,
        agent_id: str,
        tags: list[str],
        summary: str = "",
        ref_id: str = None,
        ts: int = None,
    ) -> int:
        """Record performance data."""
        canonical = canonical_performance(
            title, metrics, anomalies, optimizations, trends, summary, tags
        )

        doc_id = self.brain.upsert_document(
            kind="performance",
            ts=ts,
            title=title,
            summary=summary,
            tags=tags,
            meta={"metrics": metrics, "anomalies": anomalies},
            canonical=canonical,
            project=project,
            agent_id=agent_id,
            ref_id=ref_id,
        )

        # Insert performance-specific data
        self.brain.insert_lens(
            "performance",
            doc_id,
            {
                "metrics": json.dumps(metrics),
                "anomalies": json.dumps(anomalies),
                "optimizations": json.dumps(optimizations),
                "trends": json.dumps(trends),
            },
        )

        self._embed_and_mark(doc_id, canonical)
        logger.debug(f"Recorded performance: {title} by {agent_id}")
        return doc_id

    def conversation(
        self,
        *,
        title: str,
        channel: str,
        thread_id: str,
        role: str,
        content: str,
        project: str,
        agent_id: str,
        tags: list[str],
        summary: str = "",
        ref_id: str = None,
        ts: int = None,
    ) -> int:
        """Record a conversation."""
        canonical = canonical_conversation(title, channel, role, content, summary, tags)

        doc_id = self.brain.upsert_document(
            kind="conversation",
            ts=ts,
            title=title,
            summary=summary,
            tags=tags,
            meta={"thread_id": thread_id},
            canonical=canonical,
            project=project,
            agent_id=agent_id,
            ref_id=ref_id,
        )

        # Insert conversation-specific data
        self.brain.insert_lens(
            "conversations",
            doc_id,
            {"channel": channel, "thread_id": thread_id, "role": role, "content": content},
        )

        self._embed_and_mark(doc_id, canonical)
        logger.debug(f"Recorded conversation: {title} by {agent_id}")
        return doc_id

    def coordination(
        self,
        *,
        title: str,
        coordination_type: str,
        participants: list[str],
        coordination_data: dict[str, Any],
        effectiveness: float,
        project: str,
        agent_id: str,
        tags: list[str],
        summary: str = "",
        ref_id: str = None,
        ts: int = None,
    ) -> int:
        """Record coordination data."""
        canonical = canonical_coordination(
            title, coordination_type, participants, coordination_data, effectiveness, summary, tags
        )

        doc_id = self.brain.upsert_document(
            kind="coordination",
            ts=ts,
            title=title,
            summary=summary,
            tags=tags,
            meta={"coordination_type": coordination_type, "participants": participants},
            canonical=canonical,
            project=project,
            agent_id=agent_id,
            ref_id=ref_id,
        )

        # Insert coordination-specific data
        self.brain.insert_lens(
            "coordination",
            doc_id,
            {
                "coordination_type": coordination_type,
                "participants": json.dumps(participants),
                "coordination_data": json.dumps(coordination_data),
                "effectiveness": effectiveness,
            },
        )

        self._embed_and_mark(doc_id, canonical)
        logger.debug(f"Recorded coordination: {title} by {agent_id}")
        return doc_id

    def tool(
        self,
        *,
        title: str,
        usage_pattern: str,
        success_rate: float,
        failure_modes: list[str],
        optimizations: list[str],
        project: str,
        agent_id: str,
        tags: list[str],
        summary: str = "",
        ref_id: str = None,
        ts: int = None,
    ) -> int:
        """Record tool usage data."""
        canonical = canonical_tool(
            title, usage_pattern, success_rate, failure_modes, optimizations, summary, tags
        )

        doc_id = self.brain.upsert_document(
            kind="tool",
            ts=ts,
            title=title,
            summary=summary,
            tags=tags,
            meta={"usage_pattern": usage_pattern, "success_rate": success_rate},
            canonical=canonical,
            project=project,
            agent_id=agent_id,
            ref_id=ref_id,
        )

        # Insert tool-specific data
        self.brain.insert_lens(
            "tools",
            doc_id,
            {
                "usage_pattern": usage_pattern,
                "success_rate": success_rate,
                "failure_modes": json.dumps(failure_modes),
                "optimizations": json.dumps(optimizations),
            },
        )

        self._embed_and_mark(doc_id, canonical)
        logger.debug(f"Recorded tool: {title} by {agent_id}")
        return doc_id


# Import numpy for embedding operations
import numpy as np
