#!/usr/bin/env python3
"""
Devlogs Connector
=================

Integration with devlog system for agent communication.
V2 Compliance: ≤400 lines, focused devlog integration.
"""

import logging

from ..ingest import Ingestor

logger = logging.getLogger(__name__)


def ingest_devlog(
    text: str,
    project: str,
    agent_id: str = "Agent-5",
    channel: str = "devlog",
    thread_id: str | None = None,
):
    """
    Ingest a devlog entry into the swarm brain.

    Args:
        text: Devlog content
        project: Project identifier
        agent_id: Agent creating the devlog
        channel: Communication channel
        thread_id: Thread identifier (optional)
    """
    try:
        ingestor = Ingestor()

        # Extract key information from devlog
        summary = text[:200] + "..." if len(text) > 200 else text

        # Determine tags based on content
        tags = ["devlog", "communication"]
        if "error" in text.lower() or "failed" in text.lower():
            tags.append("error")
        if "success" in text.lower() or "completed" in text.lower():
            tags.append("success")
        if "workflow" in text.lower():
            tags.append("workflow")
        if "discord" in text.lower():
            tags.append("discord")
        if "scanner" in text.lower():
            tags.append("scanner")
        if "coordination" in text.lower():
            tags.append("coordination")

        # Record as conversation
        doc_id = ingestor.conversation(
            title="Devlog Entry",
            channel=channel,
            thread_id=thread_id or "N/A",
            role="agent",
            content=text,
            project=project,
            agent_id=agent_id,
            tags=tags,
            summary=summary,
        )

        # Also record as action if it contains actionable information
        if any(
            keyword in text.lower()
            for keyword in ["completed", "finished", "success", "failed", "error"]
        ):
            outcome = (
                "success" if "success" in text.lower() or "completed" in text.lower() else "failure"
            )

            ingestor.action(
                title="Devlog Action",
                tool="devlog_system",
                outcome=outcome,
                context={"content_length": len(text), "channel": channel},
                project=project,
                agent_id=agent_id,
                tags=tags + ["action"],
                summary=summary,
            )

        logger.info(f"Successfully ingested devlog from {agent_id}")
        return doc_id

    except Exception as e:
        logger.error(f"Failed to ingest devlog: {e}")
        raise


def ingest_devlog_batch(devlogs: list, project: str):
    """
    Ingest multiple devlog entries in batch.

    Args:
        devlogs: List of devlog dictionaries with keys: text, agent_id, channel, thread_id
        project: Project identifier
    """
    try:
        ingestor = Ingestor()

        for devlog in devlogs:
            ingest_devlog(
                text=devlog.get("text", ""),
                project=project,
                agent_id=devlog.get("agent_id", "Agent-5"),
                channel=devlog.get("channel", "devlog"),
                thread_id=devlog.get("thread_id"),
            )

        logger.info(f"Successfully ingested {len(devlogs)} devlog entries")

    except Exception as e:
        logger.error(f"Failed to ingest devlog batch: {e}")
        raise
