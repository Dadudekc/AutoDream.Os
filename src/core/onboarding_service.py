#!/usr/bin/env python3
"""
Onboarding Service for Agent Messaging System
Provides onboarding functionality for new agents joining the SWARM
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class OnboardingService:
    """Service for handling agent onboarding messages and processes"""

    def __init__(self):
        self.logger = logger
        self.templates = self._load_onboarding_templates()

    def _load_onboarding_templates(self) -> dict[str, str]:
        """Load onboarding message templates"""
        return {
            "standard": """
🐝 **WELCOME TO THE SWARM!**

Hello **{agent_id}**! You have been successfully onboarded to the Agent Cellphone V2 system.

**Your Role:** {description}
**Your Position:** {coordinates}

**SWARM PROTOCOL:**
1. **Update Status** - Set your current task & focus
2. **Review Project** - Check relevant files & context
3. **Check Inbox** - Read/respond to pending messages
4. **Message Agents** - Coordinate using messaging commands
5. **Create Devlog** - Record actions, commit, status & post to Discord

**Ready to contribute to the SWARM intelligence!** 🐝
            """,
            "friendly": """
🌟 **Welcome aboard, {agent_id}!**

Hey there! I'm excited to have you join our SWARM! 🤖🐝

**Your Expertise:** {description}
**Your Coordinates:** {coordinates}

**Getting Started:**
- Check your inbox at `agent_workspaces/{agent_id}/inbox/`
- Update your status.json with your current focus
- Say hello to the other agents!

**Let's build something amazing together!** 🚀
            """,
            "technical": """
⚡ **SYSTEM ONBOARDING COMPLETE**

Agent: {agent_id}
Status: ACTIVE
Role: {description}
Coordinates: {coordinates}

**SYSTEM INTEGRATION:**
- Messaging system: ENABLED
- Coordinate system: CONFIGURED
- Workspace: INITIALIZED

**Technical Specifications:**
- Python 3.8+
- PyAutoGUI: ENABLED
- Message queue: ACTIVE

**Ready for SWARM coordination** 🐝
            """,
        }

    def generate_onboarding_message(self, agent_id: str, style: str = "standard") -> str:
        """Generate an onboarding message for the specified agent"""
        try:
            # Get agent information from coordinate loader
            agent_info = self._get_agent_info(agent_id)

            # Select template
            template = self.templates.get(style, self.templates["standard"])

            # Format message
            message = template.format(
                agent_id=agent_id,
                description=agent_info.get("description", "SWARM Agent"),
                coordinates=agent_info.get("coordinates", "(-308, 480)"),
            )

            self.logger.info(f"Generated onboarding message for {agent_id}")
            return message.strip()

        except Exception as e:
            self.logger.error(f"Failed to generate onboarding message for {agent_id}: {e}")
            return f"Welcome {agent_id}! You have been onboarded to the Agent Cellphone V2 system."

    def _get_agent_info(self, agent_id: str) -> dict[str, Any]:
        """Get agent information from coordinate loader"""
        try:
            from .coordinate_loader import get_coordinate_loader

            loader = get_coordinate_loader()

            if hasattr(loader, "get_agent_info"):
                return loader.get_agent_info(agent_id) or {}

            # Fallback to coordinate data
            coords = loader.get_chat_coordinates(agent_id)
            return {
                "coordinates": f"({coords[0]}, {coords[1]})",
                "description": f"Agent {agent_id.split('-')[1]}",
            }

        except Exception as e:
            self.logger.warning(f"Could not load agent info for {agent_id}: {e}")
            return {"coordinates": "(-308, 480)", "description": "SWARM Agent"}

    def validate_onboarding(self, agent_id: str) -> bool:
        """Validate that an agent has been properly onboarded"""
        try:
            # Check if agent workspace exists
            import os

            workspace_path = f"agent_workspaces/{agent_id}"
            inbox_path = f"{workspace_path}/inbox"
            status_path = f"{workspace_path}/status.json"

            if not os.path.exists(workspace_path):
                self.logger.warning(f"Agent workspace missing for {agent_id}")
                return False

            if not os.path.exists(inbox_path):
                self.logger.warning(f"Agent inbox missing for {agent_id}")
                return False

            if not os.path.exists(status_path):
                self.logger.warning(f"Agent status file missing for {agent_id}")
                return False

            self.logger.info(f"Onboarding validation passed for {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Onboarding validation failed for {agent_id}: {e}")
            return False

    def create_agent_workspace(self, agent_id: str) -> bool:
        """Create the workspace structure for a new agent"""
        try:
            import json
            import os

            # Create directories
            workspace_path = f"agent_workspaces/{agent_id}"
            inbox_path = f"{workspace_path}/inbox"
            devlogs_path = f"{workspace_path}/devlogs"

            os.makedirs(workspace_path, exist_ok=True)
            os.makedirs(inbox_path, exist_ok=True)
            os.makedirs(devlogs_path, exist_ok=True)

            # Create initial status.json
            status_data = {
                "agent_id": agent_id,
                "status": "active",
                "current_task": "Onboarding complete - ready for assignment",
                "last_updated": str(__import__("datetime").datetime.now()),
                "coordination_status": "available",
            }

            with open(f"{workspace_path}/status.json", "w") as f:
                json.dump(status_data, f, indent=2)

            self.logger.info(f"Created workspace for agent {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create workspace for {agent_id}: {e}")
            return False
