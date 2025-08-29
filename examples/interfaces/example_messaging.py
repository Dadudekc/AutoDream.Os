from typing import Any, Dict, List, Optional, Tuple

from __future__ import annotations
from src.services.messaging.interfaces import (
from src.services.messaging.storage.models import V2Message
from src.services.messaging.storage.storage import IMessageStorage

"""Example implementations for messaging interfaces."""



    IBulkMessaging,
    ICampaignMessaging,
    ICoordinateManager,
    ICrossSystemMessaging,
    IFSMMessaging,
    IMessageSender,
    IOnboardingMessaging,
    IYOLOMessaging,
    MessageType,
)


class InMemoryMessageStorage(IMessageStorage):
    """Store messages in memory for demonstration purposes."""

    def __init__(self) -> None:
        self._messages: Dict[str, V2Message] = {}

    def store_message(self, message: V2Message) -> bool:
        self._messages[message.id] = message
        return True

    def get_message(self, message_id: str) -> Optional[V2Message]:
        return self._messages.get(message_id)


class ConsoleMessageSender(IMessageSender):
    """Send messages by printing to the console."""

    def send_message(self, recipient: str, message_content: str) -> bool:
        print(f"{recipient}: {message_content}")
        return True


class SimpleCoordinateManager(ICoordinateManager):
    """Maintain coordinates in memory."""

    def __init__(self) -> None:
        self._coords: Dict[str, Tuple[int, int]] = {}

    def get_agent_coordinates(self, agent_id: str, mode: str) -> Optional[Any]:
        return self._coords.get(agent_id)

    def validate_coordinates(self) -> Dict[str, Any]:
        return {"valid": True}

    def get_available_modes(self) -> List[str]:
        return ["default"]

    def get_agents_in_mode(self, mode: str) -> List[str]:
        return list(self._coords.keys())

    def map_coordinates(
        self, mode: str = "8-agent"
    ) -> Dict[str, Any]:  # pragma: no cover - example
        return {"mode": mode, "coordinates": self._coords}

    def calibrate_coordinates(
        self,
        agent_id: str,
        input_coords: Tuple[int, int],
        starter_coords: Tuple[int, int],
        mode: str = "8-agent",
    ) -> bool:
        self._coords[agent_id] = input_coords
        return True

    def consolidate_coordinate_files(
        self,
    ) -> Dict[str, Any]:  # pragma: no cover - example
        return {"consolidated": True}


class SimpleBulkMessaging(IBulkMessaging):
    """Broadcast messages to multiple agents."""

    def __init__(self, sender: IMessageSender) -> None:
        self.sender = sender

    def send_bulk_messages(
        self, messages: Dict[str, str], mode: str
    ) -> Dict[str, bool]:
        return {
            agent: self.sender.send_message(agent, msg)
            for agent, msg in messages.items()
        }


class SimpleCampaignMessaging(ICampaignMessaging):
    """Send campaign messages using a sender."""

    def __init__(self, sender: IMessageSender) -> None:
        self.sender = sender

    def send_campaign_message(
        self, message_content: str, campaign_type: str
    ) -> Dict[str, bool]:
        recipients = ["agent1", "agent2"]
        return {
            agent: self.sender.send_message(agent, message_content)
            for agent in recipients
        }


class SimpleYOLOMessaging(IYOLOMessaging):
    """Activate YOLO mode for all agents."""

    def activate_yolo_mode(self, message_content: str) -> Dict[str, bool]:
        recipients = ["agent1", "agent2"]
        return {agent: True for agent in recipients}


class SimpleCrossSystemMessaging(ICrossSystemMessaging):
    """Send messages to another system."""

    async def send_cross_system_message(
        self, target_system: str, message_content: str, protocol: str
    ) -> bool:
        return True


class SimpleFSMMessaging(IFSMMessaging):
    """Send FSM coordination messages."""

    def send_fsm_message(
        self, agent_id: str, message_type: MessageType, payload: Dict[str, Any]
    ) -> bool:
        return True


class SimpleOnboardingMessaging(IOnboardingMessaging):
    """Send onboarding messages to new agents."""

    def send_onboarding_message(
        self, agent_id: str, onboarding_type: MessageType, content: str
    ) -> bool:
        return True
