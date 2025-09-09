"""
Message Bus Port - Domain Interface
===================================

Defines the contract for message publishing and event handling.
This enables domain events and inter-agent communication.
"""

from typing import Any, Protocol

from ..value_objects.ids import AgentId, MessageId


class MessageBus(Protocol):
    """
    Port for message publishing and event handling.

    This protocol enables loose coupling between domain objects
    and external messaging infrastructure.
    """

    def publish(
        self, event_type: str, payload: dict[str, Any], target_agent: AgentId = None
    ) -> MessageId:
        """
        Publish a message/event to the message bus.

        Args:
            event_type: Type of event/message
            payload: Event data
            target_agent: Specific agent to receive message (optional)

        Returns:
            Unique message identifier
        """
        ...

    def subscribe(self, event_type: str, handler: callable) -> None:
        """
        Subscribe to a specific event type.

        Args:
            event_type: Event type to subscribe to
            handler: Function to handle the event
        """
        ...

    def broadcast(self, event_type: str, payload: dict[str, Any]) -> None:
        """
        Broadcast message to all agents.

        Args:
            event_type: Type of event/message
            payload: Event data
        """
        ...

    def send_direct(self, target_agent: AgentId, message: str, priority: int = 1) -> MessageId:
        """
        Send direct message to specific agent.

        Args:
            target_agent: Agent to receive message
            message: Message content
            priority: Message priority (1=low, 2=medium, 3=high)

        Returns:
            Unique message identifier
        """
        ...
