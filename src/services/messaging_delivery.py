#!/usr/bin/env python3
"""
Messaging Delivery Module - Agent Cellphone V2
=============================================

Inbox delivery functionality for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import os
import time
from typing import Dict, Any

from .models.messaging_models import UnifiedMessage
from ..utils.logger import get_messaging_logger
from ..core.metrics import MessagingMetrics


class MessagingDelivery:
    """Handles message delivery to agent inboxes."""

    def __init__(self, inbox_paths: Dict[str, str], metrics: MessagingMetrics):
        """Initialize delivery service."""
        self.inbox_paths = inbox_paths
        self.metrics = metrics
        self.logger = get_messaging_logger()

    def send_message_to_inbox(self, message: UnifiedMessage, max_retries: int = 3) -> bool:
        """Send message to agent's inbox file with retry mechanism.

        Args:
            message: The UnifiedMessage to deliver
            max_retries: Maximum number of retry attempts

        Returns:
            bool: True if delivery successful, False otherwise
        """
        for attempt in range(max_retries):
            try:
                recipient = message.recipient
                if recipient not in self.inbox_paths:
                    print(f"❌ ERROR: Unknown recipient {recipient}")
                    return False

                inbox_path = self.inbox_paths[recipient]
                os.makedirs(inbox_path, exist_ok=True)

                # Create message filename with timestamp
                timestamp = message.timestamp.strftime("%Y%m%d_%H%M%S") if message.timestamp else time.strftime("%Y%m%d_%H%M%S")
                filename = f"CAPTAIN_MESSAGE_{timestamp}_{message.message_id}.md"
                filepath = os.path.join(inbox_path, filename)

                # Write message to file with proper encoding
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# 🚨 CAPTAIN MESSAGE - {message.message_type.value.upper()}\n\n")
                    f.write(f"**From**: {message.sender}\n")
                    f.write(f"**To**: {message.recipient}\n")
                    f.write(f"**Priority**: {message.priority.value}\n")
                    f.write(f"**Message ID**: {message.message_id}\n")
                    f.write(f"**Timestamp**: {message.timestamp.isoformat() if message.timestamp else 'Unknown'}\n\n")
                    f.write("---\n\n")
                    f.write(message.content)
                    f.write("\n\n---\n")
                    f.write(f"*Message delivered via Unified Messaging Service*\n")

                self.logger.info("Message delivered to inbox successfully",
                                extra={"filepath": filepath, "recipient": recipient, "message_id": message.message_id})

                # Record metrics (V2 compliance)
                self.metrics.record_message_sent(message.message_type.value, recipient, "inbox")

                return True

            except OSError as e:
                self.logger.error(f"Failed to deliver message to inbox (attempt {attempt + 1}/{max_retries})",
                                extra={"recipient": recipient, "message_id": message.message_id, "error": str(e)})

                # Record failure metrics (V2 compliance)
                self.metrics.record_message_failed(message.message_type.value, recipient, "OSError")

                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff
            except Exception as e:
                self.logger.critical(f"Unexpected error delivering message to inbox (attempt {attempt + 1}/{max_retries})",
                                   extra={"recipient": recipient, "message_id": message.message_id, "error": str(e)})

                # Record failure metrics (V2 compliance)
                self.metrics.record_message_failed(message.message_type.value, recipient, "UnexpectedError")

                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff

        return False
