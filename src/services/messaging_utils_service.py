#!/usr/bin/env python3
"""Messaging Utils Service - V2 Compliance Module
=================================================

Utility functions for the unified messaging system: agent status monitoring,
message validation, system health checks, and helpers.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pathlib import Path

from .unified_messaging_imports import (
    read_json,
    get_unified_utility,
    get_unified_validator,
)
from .models.messaging_models import UnifiedMessage
from .utils.messaging_validation_utils import MessagingValidationUtils
from .status_embedding_indexer import refresh_status_embedding
from ..core.constants.paths import (
    AGENT_WORKSPACES_DIR,
    DOCS_DIR,
    SCRIPTS_DIR,
    SRC_DIR,
    TESTS_DIR,
    get_agent_inbox,
    get_agent_status_file,
    get_agent_workspace,
)


class MessagingUtilsService:
    """
    Service for messaging utility functions.

    V2 Compliance: Centralized utility functions with proper validation.
    """

    def __init__(self, agent_list: Optional[List[str]] = None):
        """Initialize utils service."""
        # Default agent list if not provided
        self.agent_list = agent_list or [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
            "Agent-9",
        ]

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        agent_status = {}

        for agent_id in self.agent_list:
            status_file = get_agent_status_file(agent_id)
            inbox_path = get_agent_inbox(agent_id)

            agent_status[agent_id] = {
                "status_file_exists": status_file.exists(),
                "inbox_exists": inbox_path.exists(),
                "inbox_message_count": (
                    len(list(inbox_path.glob("*.md"))) if inbox_path.exists() else 0
                ),
                "last_status_update": None,
                "current_mission": None,
            }

            if status_file.exists():
                try:
                    status_data = read_json(status_file)
                    agent_status[agent_id].update(
                        {
                            "last_status_update": status_data.get("last_updated"),
                            "current_mission": status_data.get("current_mission"),
                            "agent_status": status_data.get("status", "unknown"),
                        }
                    )
                    refresh_status_embedding(agent_id, status_data)
                except Exception:
                    agent_status[agent_id]["status_read_error"] = True

        return {
            "agents": agent_status,
            "total_agents": len(self.agent_list),
            "active_agents": sum(
                1 for s in agent_status.values() if s["status_file_exists"]
            ),
            "timestamp": str(get_unified_utility().Path(".").stat().st_mtime),
        }

    def validate_message(self, message: UnifiedMessage) -> Dict[str, Any]:
        """Validate message structure and content."""

        # Use shared validation logic
        validation_result = MessagingValidationUtils.validate_message_structure(message)

        # Add agent-specific validation
        if message.sender and message.sender not in self.agent_list:
            validation_result["errors"].append(f"Invalid sender: {message.sender}")
        if message.recipient and message.recipient not in self.agent_list:
            validation_result["errors"].append(
                f"Invalid recipient: {message.recipient}"
            )

        # Update validation status
        validation_result["valid"] = len(validation_result["errors"]) == 0
        validation_result["error_count"] = len(validation_result["errors"])

        return validation_result

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        health_status = {
            "timestamp": str(get_unified_utility().Path(".").stat().st_mtime),
            "components": {},
        }

        core_dirs = [
            AGENT_WORKSPACES_DIR,
            SRC_DIR,
            SCRIPTS_DIR,
            DOCS_DIR,
            TESTS_DIR,
        ]
        for dir_path in core_dirs:
            health_status["components"][dir_path.name] = {
                "exists": dir_path.exists(),
                "file_count": (
                    len(list(dir_path.rglob("*"))) if dir_path.exists() else 0
                ),
                "size_mb": (
                    sum(
                        f.stat().st_size
                        for f in dir_path.rglob("*")
                        if self._is_file_accessible(f) and f.is_file()
                    )
                    / (1024 * 1024)
                    if dir_path.exists()
                    else 0
                ),
            }

        # Check agent workspaces
        agent_status = self.get_agent_status()
        health_status["agent_health"] = {
            "total_agents": agent_status["total_agents"],
            "active_agents": agent_status["active_agents"],
            "inactive_agents": (
                agent_status["total_agents"] - agent_status["active_agents"]
            ),
        }

        # Overall health assessment
        critical_components = [SRC_DIR.name, AGENT_WORKSPACES_DIR.name]
        critical_missing = [
            comp
            for comp in critical_components
            if not health_status["components"].get(comp, {}).get("exists", False)
        ]

        if critical_missing:
            health_status["overall_health"] = "critical"
            health_status["issues"] = [
                f"Missing critical component: {comp}" for comp in critical_missing
            ]
        elif agent_status["active_agents"] < agent_status["total_agents"] * 0.5:
            health_status["overall_health"] = "warning"
            health_status["issues"] = ["Low agent activity detected"]
        else:
            health_status["overall_health"] = "healthy"
            health_status["issues"] = []

        return health_status

    def _is_file_accessible(self, file_path: Path) -> bool:
        """Check if a file is accessible."""
        try:
            file_path.stat()
            return True
        except OSError:
            return False

    def format_message_for_display(self, message: UnifiedMessage) -> str:
        """Format message for display."""
        formatted = f"[{message.timestamp}] {message.sender} -> {message.recipient}\n"
        formatted += f"Type: {message.message_type.value}\n"
        formatted += f"Priority: {message.priority}\n"
        formatted += (
            f"Content: {message.content[:200]}"
            f"{'...' if len(message.content) > 200 else ''}"
        )

        if get_unified_validator().validate_hasattr(message, "tags") and message.tags:
            formatted += f"\nTags: {', '.join(message.tags)}"

        return formatted

    def generate_message_summary(
        self, messages: List[UnifiedMessage]
    ) -> Dict[str, Any]:
        """Generate summary statistics for messages."""
        if not get_unified_validator().validate_required(messages):
            return {"total_messages": 0, "error": "No messages provided"}

        # Count distributions in single pass
        distributions = {"types": {}, "senders": {}, "recipients": {}, "priorities": {}}
        total_length = 0

        for m in messages:
            distributions["types"][
                m.message_type.value if m.message_type else "unknown"
            ] = (
                distributions["types"].get(
                    m.message_type.value if m.message_type else "unknown", 0
                )
                + 1
            )
            distributions["senders"][m.sender] = (
                distributions["senders"].get(m.sender, 0) + 1
            )
            distributions["recipients"][m.recipient] = (
                distributions["recipients"].get(m.recipient, 0) + 1
            )
            distributions["priorities"][
                get_unified_validator().safe_getattr(m, "priority", "normal")
            ] = (
                distributions["priorities"].get(
                    get_unified_validator().safe_getattr(m, "priority", "normal"), 0
                )
                + 1
            )
            total_length += len(m.content)

        return {
            "total_messages": len(messages),
            "avg_content_length": total_length / len(messages),
            "time_range": {
                "earliest": min(m.timestamp for m in messages),
                "latest": max(m.timestamp for m in messages),
            },
            **distributions,
        }

    def validate_agent_workspace(self, agent_id: str) -> Dict[str, Any]:
        """Validate agent workspace structure."""
        workspace_path = get_agent_workspace(agent_id)

        if not workspace_path.exists():
            return {
                "agent_id": agent_id,
                "valid": False,
                "issues": ["Workspace does not exist"],
            }

        inbox_exists = get_agent_inbox(agent_id).exists()
        status_exists = get_agent_status_file(agent_id).exists()

        return {
            "agent_id": agent_id,
            "valid": inbox_exists and status_exists,
            "inbox_exists": inbox_exists,
            "status_exists": status_exists,
            "issues": [
                "Missing inbox directory" if not inbox_exists else None,
                "Missing status.json" if not status_exists else None,
            ],
        }


# Factory function for dependency injection
def create_messaging_utils_service(
    agent_list: Optional[List[str]] = None,
) -> MessagingUtilsService:
    """
    Factory function to create MessagingUtilsService with dependency injection.
    """
    return MessagingUtilsService(agent_list=agent_list)


# Export service interface
__all__ = ["MessagingUtilsService", "create_messaging_utils_service"]
