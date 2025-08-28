"""Message parsing utilities for the communication coordinator."""

import logging
from typing import List, Dict, Any, Optional

from .coordinator_types import CoordinationMessage, TaskPriority, MessageType
from .utils import generate_id, current_timestamp

logger = logging.getLogger(__name__)


class MessageParser:
    """Parse raw message data into CoordinationMessage objects."""

    def parse(
        self,
        sender_id: str,
        recipient_ids: List[str],
        message_type: str,
        content: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CoordinationMessage:
        """Create a CoordinationMessage from raw components."""
        try:
            msg_type = MessageType(message_type)
        except ValueError:
            msg_type = MessageType.COORDINATION

        message = CoordinationMessage(
            message_id=generate_id(),
            sender_id=sender_id,
            recipient_ids=recipient_ids,
            message_type=msg_type,
            content=content,
            timestamp=current_timestamp(),
            priority=priority,
            metadata=metadata or {},
        )
        logger.debug("Parsed message %s", message.message_id)
        return message
