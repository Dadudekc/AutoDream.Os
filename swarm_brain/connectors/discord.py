#!/usr/bin/env python3
"""
Discord Connector
=================

Integration with Discord commander for agent coordination.
V2 Compliance: ≤400 lines, focused Discord integration.
"""

import logging
from typing import Any

from ..ingest import Ingestor

logger = logging.getLogger(__name__)


def ingest_discord(
    message: str,
    thread_id: str,
    project: str,
    agent_id: str = "Agent-6",
    outcome: str = "success",
    channel: str = "discord",
    role: str = "agent",
):
    """
    Ingest Discord communication into the swarm brain.

    Args:
        message: Discord message content
        thread_id: Discord thread identifier
        project: Project identifier
        agent_id: Agent sending the message
        outcome: Communication outcome
        channel: Communication channel
        role: Message role (user/agent/system)
    """
    try:
        ingestor = Ingestor()

        # Extract key information
        summary = message[:200] + "..." if len(message) > 200 else message

        # Determine tags based on content
        tags = ["discord", "communication", "coordination"]
        if "coordinate" in message.lower() or "swarm" in message.lower():
            tags.append("swarm")
        if "task" in message.lower() or "workflow" in message.lower():
            tags.append("task")
        if "error" in message.lower() or "failed" in message.lower():
            tags.append("error")
        if "success" in message.lower() or "completed" in message.lower():
            tags.append("success")

        # Record as conversation
        doc_id = ingestor.conversation(
            title="Discord Communication",
            channel=channel,
            thread_id=thread_id,
            role=role,
            content=message,
            project=project,
            agent_id=agent_id,
            tags=tags,
            summary=summary,
        )

        # Also record as action for coordination
        context = {
            "message_length": len(message),
            "thread_id": thread_id,
            "channel": channel,
            "role": role,
        }

        ingestor.action(
            title="Discord Commander",
            tool="discord_commander",
            outcome=outcome,
            context=context,
            project=project,
            agent_id=agent_id,
            tags=tags + ["action"],
            summary=summary,
        )

        # Record coordination if it's swarm-related
        if "swarm" in message.lower() or "coordinate" in message.lower():
            participants = []
            # Extract agent mentions from message
            for i in range(1, 9):  # Agent-1 to Agent-8
                if f"Agent-{i}" in message:
                    participants.append(f"Agent-{i}")

            if not participants:
                participants = [agent_id]

            ingestor.coordination(
                title="Discord Coordination",
                coordination_type="discord",
                participants=participants,
                coordination_data={"message": message, "thread_id": thread_id},
                effectiveness=1.0 if outcome == "success" else 0.5,
                project=project,
                agent_id=agent_id,
                tags=tags + ["coordination"],
                summary=summary,
            )

        logger.info(f"Successfully ingested Discord message from {agent_id}")
        return doc_id

    except Exception as e:
        logger.error(f"Failed to ingest Discord message: {e}")
        raise


def ingest_discord_command(
    command: str, args: list, result: dict[str, Any], project: str, agent_id: str = "Agent-6"
):
    """
    Ingest Discord command execution.

    Args:
        command: Command name
        args: Command arguments
        result: Command result
        project: Project identifier
        agent_id: Agent executing the command
    """
    try:
        ingestor = Ingestor()

        context = {"command": command, "args": args, "result": result}

        outcome = "success" if result.get("success", False) else "failure"

        ingestor.action(
            title=f"Discord Command: {command}",
            tool="discord_commander",
            outcome=outcome,
            context=context,
            project=project,
            agent_id=agent_id,
            tags=["discord", "command", "coordination"],
            summary=f"Executed {command} command with args: {args}",
        )

        logger.info(f"Recorded Discord command execution: {command}")

    except Exception as e:
        logger.error(f"Failed to ingest Discord command: {e}")
        raise


def ingest_discord_coordination(
    coordination_type: str,
    participants: list,
    coordination_data: dict[str, Any],
    effectiveness: float,
    project: str,
    agent_id: str = "Agent-6",
):
    """
    Ingest Discord-based coordination activity.

    Args:
        coordination_type: Type of coordination
        participants: List of participating agents
        coordination_data: Coordination details
        effectiveness: Coordination effectiveness (0.0-1.0)
        project: Project identifier
        agent_id: Coordinating agent
    """
    try:
        ingestor = Ingestor()

        ingestor.coordination(
            title=f"Discord {coordination_type}",
            coordination_type=f"discord_{coordination_type}",
            participants=participants,
            coordination_data=coordination_data,
            effectiveness=effectiveness,
            project=project,
            agent_id=agent_id,
            tags=["discord", "coordination", coordination_type],
            summary=f"Discord coordination: {coordination_type} with {len(participants)} participants",
        )

        logger.info(f"Recorded Discord coordination: {coordination_type}")

    except Exception as e:
        logger.error(f"Failed to ingest Discord coordination: {e}")
        raise
