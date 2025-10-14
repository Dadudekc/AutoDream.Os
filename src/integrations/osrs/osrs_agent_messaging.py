#!/usr/bin/env python3
"""
OSRS Agent Message Handling
Extracted from osrs_agent_core.py for V2 compliance.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .osrs_agent_core import OSRS_Agent_Core


class OSRSMessageHandler:
    """Handles coordination messages between OSRS agents."""

    @staticmethod
    def handle_coordination_message(agent: "OSRS_Agent_Core", message: dict[str, Any]) -> None:
        """Handle coordination message from another agent."""
        message_type = message.get("type", "unknown")

        if message_type == "resource_request":
            OSRSMessageHandler.handle_resource_request(agent, message)
        elif message_type == "activity_coordination":
            OSRSMessageHandler.handle_activity_coordination(agent, message)
        elif message_type == "emergency_alert":
            OSRSMessageHandler.handle_emergency_alert(agent, message)
        else:
            agent.logger.warning(f"Unknown message type: {message_type}")

    @staticmethod
    def handle_resource_request(agent: "OSRS_Agent_Core", message: dict[str, Any]) -> None:
        """Handle resource request from another agent."""
        requested_item = message.get("item")
        requesting_agent = message.get("from_agent")

        agent.logger.info(f"Resource request: {requested_item} from {requesting_agent}")

        if requested_item in agent.game_state.inventory_items:
            OSRSMessageHandler.send_message(
                agent,
                requesting_agent,
                {
                    "type": "resource_response",
                    "item": requested_item,
                    "available": True,
                    "from_agent": agent.agent_id,
                },
            )
        else:
            OSRSMessageHandler.send_message(
                agent,
                requesting_agent,
                {
                    "type": "resource_response",
                    "item": requested_item,
                    "available": False,
                    "from_agent": agent.agent_id,
                },
            )

    @staticmethod
    def handle_activity_coordination(agent: "OSRS_Agent_Core", message: dict[str, Any]) -> None:
        """Handle activity coordination message."""
        activity = message.get("activity")
        coordinating_agent = message.get("from_agent")

        agent.logger.info(f"Activity coordination: {activity} from {coordinating_agent}")

        if OSRSMessageHandler.should_participate_in_activity(agent, activity):
            agent.current_activity = activity
            agent.logger.info(f"Participating in coordinated activity: {activity}")

    @staticmethod
    def handle_emergency_alert(agent: "OSRS_Agent_Core", message: dict[str, Any]) -> None:
        """Handle emergency alert from another agent."""
        from .osrs_agent_core import AgentRole

        emergency_type = message.get("emergency_type")
        alerting_agent = message.get("from_agent")

        agent.logger.warning(f"Emergency alert: {emergency_type} from {alerting_agent}")

        if agent.role == AgentRole.EMERGENCY_RESPONSE:
            agent.initiate_emergency_response(emergency_type, alerting_agent)

    @staticmethod
    def should_participate_in_activity(agent: "OSRS_Agent_Core", activity: str) -> bool:
        """Determine if agent should participate in a coordinated activity."""
        from .osrs_agent_core import AgentRole

        if agent.role == AgentRole.EMERGENCY_RESPONSE:
            return "emergency" in activity.lower()
        elif agent.role == AgentRole.COMBAT_SPECIALIST:
            return "combat" in activity.lower() or "pvp" in activity.lower()
        elif agent.role == AgentRole.RESOURCE_MANAGER:
            return "resource" in activity.lower() or "gathering" in activity.lower()

        return False

    @staticmethod
    def send_message(agent: "OSRS_Agent_Core", target_agent: str, message: dict[str, Any]) -> None:
        """Send message to another agent."""
        message["from_agent"] = agent.agent_id
        message["timestamp"] = datetime.now().isoformat()

        agent.logger.info(f"Sending message to {target_agent}: {message['type']}")

    @staticmethod
    def communicate_with_swarm(agent: "OSRS_Agent_Core") -> None:
        """Communicate status and coordination with the swarm."""
        try:
            status_message = {
                "type": "status_update",
                "agent_id": agent.agent_id,
                "status": agent.status.value,
                "current_activity": agent.current_activity,
                "game_state": agent.game_state.__dict__ if agent.game_state else None,
                "timestamp": datetime.now().isoformat(),
            }

            agent.logger.debug(f"Status update: {status_message}")

        except Exception as e:
            agent.logger.error(f"Error communicating with swarm: {e}")
