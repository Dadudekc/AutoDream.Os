"""
Discord Embeds
==============

Discord embed creation utilities for V2_SWARM notifications.
Extracted from discord_service.py for V2 compliance.

Author: Agent-7 - Repository Cloning & Consolidation Specialist
Extracted: 2025-10-11 (V2 compliance refactoring)
"""

from datetime import datetime
from typing import Any


def create_devlog_embed(devlog_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for devlog notification."""
    colors = {
        "general": 0x3498DB,
        "cleanup": 0xE74C3C,
        "consolidation": 0x9B59B6,
        "coordination": 0x1ABC9C,
        "testing": 0xF39C12,
        "deployment": 0x27AE60,
    }

    return {
        "title": f"📋 {devlog_data.get('title', 'DevLog Update')}",
        "description": devlog_data.get("description", "")[:2000],
        "color": colors.get(devlog_data.get("category", "general"), 0x3498DB),
        "fields": [
            {
                "name": "Category",
                "value": devlog_data.get("category", "general").title(),
                "inline": True,
            },
            {"name": "Agent", "value": devlog_data.get("agent", "Unknown"), "inline": True},
            {
                "name": "Timestamp",
                "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "inline": True,
            },
        ],
        "footer": {"text": "V2_SWARM DevLog Monitor"},
    }


def create_agent_status_embed(agent_status: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for agent status notification."""
    status_colors = {
        "active": 0x27AE60,
        "idle": 0xF39C12,
        "error": 0xE74C3C,
        "offline": 0x95A5A6,
    }

    return {
        "title": f"🤖 Agent Status Update - {agent_status.get('agent_id', 'Unknown')}",
        "color": status_colors.get(agent_status.get("status", "unknown"), 0x3498DB),
        "fields": [
            {
                "name": "Status",
                "value": agent_status.get("status", "unknown").title(),
                "inline": True,
            },
            {
                "name": "Last Activity",
                "value": agent_status.get("last_activity", "Unknown"),
                "inline": True,
            },
            {
                "name": "Timestamp",
                "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "inline": True,
            },
        ],
        "footer": {"text": "V2_SWARM Status Monitor"},
    }


def create_coordination_embed(coordination_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for swarm coordination notification."""
    priority_colors = {
        "LOW": 0x95A5A6,
        "NORMAL": 0x3498DB,
        "HIGH": 0xF39C12,
        "CRITICAL": 0xE74C3C,
    }

    return {
        "title": f"🐝 Swarm Coordination - {coordination_data.get('mission', 'Update')}",
        "color": priority_colors.get(coordination_data.get("priority", "NORMAL"), 0x3498DB),
        "fields": [
            {
                "name": "Mission",
                "value": coordination_data.get("mission", "Unknown"),
                "inline": True,
            },
            {
                "name": "Priority",
                "value": coordination_data.get("priority", "NORMAL"),
                "inline": True,
            },
            {
                "name": "Agents Involved",
                "value": str(coordination_data.get("agents", "All")),
                "inline": True,
            },
        ],
        "footer": {"text": "V2_SWARM Coordination System"},
    }
