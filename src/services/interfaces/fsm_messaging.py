"""Finite state machine messaging interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from .enums import MessageType


class IFSMMessaging(ABC):
    """Interface for FSM-driven coordination messaging."""

    @abstractmethod
    def send_fsm_message(
        self, agent_id: str, message_type: MessageType, payload: Dict[str, Any]
    ) -> bool:
        """Send an FSM-driven coordination message."""
        raise NotImplementedError("send_fsm_message must be implemented by subclasses")
