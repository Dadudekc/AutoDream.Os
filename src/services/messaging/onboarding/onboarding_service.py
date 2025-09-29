#!/usr/bin/env python3
"""
Onboarding Service - V2 Compliance
==================================

Service for handling agent onboarding and initialization.
Provides onboarding functionality for the Discord Commander.

Author: Agent-2 (Security Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive error handling
"""

import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class OnboardingService:
    """Service for handling agent onboarding and initialization."""

    def __init__(self):
        """Initialize onboarding service."""
        self.onboarded_agents = {}
        self.onboarding_history = []
        logger.info("Onboarding Service initialized")

    def onboard_agent(
        self, agent_id: str, agent_data: dict[str, Any]
    ) -> tuple[bool, dict[str, Any]]:
        """Onboard a new agent."""
        try:
            # Validate agent data
            if not self._validate_agent_data(agent_data):
                return False, {"error": "Invalid agent data"}

            # Check if agent already onboarded
            if agent_id in self.onboarded_agents:
                logger.warning(f"Agent {agent_id} already onboarded")
                return True, {"status": "already_onboarded"}

            # Perform onboarding
            onboarding_result = self._perform_onboarding(agent_id, agent_data)

            if onboarding_result["success"]:
                self.onboarded_agents[agent_id] = {
                    "agent_id": agent_id,
                    "onboarded_at": datetime.now(UTC),
                    "status": "active",
                    "data": agent_data,
                }

                self.onboarding_history.append(
                    {
                        "agent_id": agent_id,
                        "timestamp": datetime.now(UTC),
                        "action": "onboarded",
                        "result": "success",
                    }
                )

                logger.info(f"Agent {agent_id} successfully onboarded")
                return True, onboarding_result

            return False, onboarding_result

        except Exception as e:
            logger.error(f"Onboarding failed for agent {agent_id}: {e}")
            return False, {"error": str(e)}

    def get_agent_status(self, agent_id: str) -> dict[str, Any]:
        """Get onboarding status of an agent."""
        if agent_id in self.onboarded_agents:
            return {
                "agent_id": agent_id,
                "status": "onboarded",
                "onboarded_at": self.onboarded_agents[agent_id]["onboarded_at"],
                "active": self.onboarded_agents[agent_id]["status"] == "active",
            }
        else:
            return {"agent_id": agent_id, "status": "not_onboarded", "active": False}

    def list_onboarded_agents(self) -> list[dict[str, Any]]:
        """List all onboarded agents."""
        return [
            {"agent_id": agent_id, "onboarded_at": data["onboarded_at"], "status": data["status"]}
            for agent_id, data in self.onboarded_agents.items()
        ]

    def _validate_agent_data(self, agent_data: dict[str, Any]) -> bool:
        """Validate agent data for onboarding."""
        required_fields = ["agent_id", "capabilities"]

        for field in required_fields:
            if field not in agent_data:
                logger.error(f"Missing required field: {field}")
                return False

        return True

    def _perform_onboarding(self, agent_id: str, agent_data: dict[str, Any]) -> dict[str, Any]:
        """Perform the actual onboarding process."""
        try:
            # Initialize agent capabilities
            capabilities = agent_data.get("capabilities", [])

            # Set up agent workspace
            workspace_setup = self._setup_agent_workspace(agent_id)

            # Configure agent permissions
            permissions = self._configure_agent_permissions(agent_id, capabilities)

            # Initialize agent communication
            communication_setup = self._setup_agent_communication(agent_id)

            return {
                "success": True,
                "workspace_setup": workspace_setup,
                "permissions": permissions,
                "communication_setup": communication_setup,
                "capabilities": capabilities,
            }

        except Exception as e:
            logger.error(f"Onboarding process failed for {agent_id}: {e}")
            return {"success": False, "error": str(e)}

    def _setup_agent_workspace(self, agent_id: str) -> dict[str, Any]:
        """Set up agent workspace."""
        try:
            # Create agent workspace directory
            from pathlib import Path

            workspace_path = Path(f"agent_workspaces/{agent_id}")
            workspace_path.mkdir(parents=True, exist_ok=True)

            # Create required subdirectories
            (workspace_path / "inbox").mkdir(exist_ok=True)
            (workspace_path / "processed").mkdir(exist_ok=True)
            (workspace_path / "working_tasks.json").touch()
            (workspace_path / "future_tasks.json").touch()

            return {
                "success": True,
                "workspace_path": str(workspace_path),
                "directories_created": ["inbox", "processed"],
            }

        except Exception as e:
            logger.error(f"Workspace setup failed for {agent_id}: {e}")
            return {"success": False, "error": str(e)}

    def _configure_agent_permissions(
        self, agent_id: str, capabilities: list[str]
    ) -> dict[str, Any]:
        """Configure agent permissions based on capabilities."""
        try:
            # Define permission levels based on capabilities
            permissions = {
                "messaging": "messaging" in capabilities,
                "file_access": "file_access" in capabilities,
                "system_commands": "system_commands" in capabilities,
                "discord_integration": "discord_integration" in capabilities,
            }

            return {"success": True, "permissions": permissions}

        except Exception as e:
            logger.error(f"Permission configuration failed for {agent_id}: {e}")
            return {"success": False, "error": str(e)}

    def _setup_agent_communication(self, agent_id: str) -> dict[str, Any]:
        """Set up agent communication channels."""
        try:
            # Initialize messaging service for agent
            from ..core.messaging_service import MessagingService

            messaging_service = MessagingService()

            # Test communication
            test_result = messaging_service.test_agent_connection(agent_id)

            return {"success": True, "messaging_service": "initialized", "test_result": test_result}

        except Exception as e:
            logger.error(f"Communication setup failed for {agent_id}: {e}")
            return {"success": False, "error": str(e)}


# Global instance for easy access
onboarding_service = OnboardingService()
