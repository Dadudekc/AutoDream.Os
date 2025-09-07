#!/usr/bin/env python3
"""
Messaging Bulk Module - Agent Cellphone V2
=========================================

Bulk messaging functionality for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""
from typing import Any, Dict, List
import time

from .messaging_pyautogui import PyAutoGUIMessagingDelivery
from .messaging_message_builder import MessagingMessageBuilder
from .unified_messaging_imports import get_logger
from .models.messaging_models import (
    RecipientType,
    SenderType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)


class MessagingBulk:
    """Handles bulk messaging operations."""

    def __init__(
        self,
        message_builder: MessagingMessageBuilder,
        pyautogui_delivery: PyAutoGUIMessagingDelivery,
    ):
        """Initialize bulk messaging service."""
        self.message_builder = message_builder
        self.pyautogui_delivery = pyautogui_delivery

    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: List[UnifiedMessageTag] = None,
        metadata: Dict[str, Any] = None,
        mode: str = "pyautogui",
        use_paste: bool = True,
        new_tab_method: str = "ctrl_t",
        use_new_tab: bool = None,
        sender_type: SenderType = None,
        recipient_type: RecipientType = None,
    ) -> bool:
        """Send a single message to a specific agent."""
        message = self.message_builder.build_message(
            message=content,
            recipient=recipient,
            sender=sender,
            message_type=message_type,
            priority=priority,
            tags=tags,
            metadata=metadata,
            sender_type=sender_type,
            recipient_type=recipient_type,
        )

        get_logger(__name__).info(f"✅ MESSAGE CREATED: {sender} → {recipient}")
        get_logger(__name__).info(f"🎯 Type: {message_type.value}")
        if sender_type:
            get_logger(__name__).info(f"📤 Sender Type: {sender_type.value}")
        if recipient_type:
            get_logger(__name__).info(f"📥 Recipient Type: {recipient_type.value}")
        get_logger(__name__).info(f"🆔 Message ID: {message.message_id}")

        # Deliver the message
        delivery_success = False
        if mode == "pyautogui":
            delivery_success = self.pyautogui_delivery.send_message_via_pyautogui(
                message, use_paste, new_tab_method, use_new_tab
            )
        else:
            # For inbox mode, delivery will be handled by main core
            delivery_success = False  # Placeholder

        if delivery_success:
            get_logger(__name__).info(f"✅ MESSAGE DELIVERED TO {recipient}")
        else:
            get_logger(__name__).info(f"❌ MESSAGE DELIVERY FAILED TO {recipient}")

        get_logger(__name__).info()
        return delivery_success

    def send_to_all_agents(
        self,
        content: str,
        sender: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: List[UnifiedMessageTag] = None,
        metadata: Dict[str, Any] = None,
        mode: str = "pyautogui",
        use_paste: bool = True,
        new_tab_method: str = "ctrl_t",
        use_new_tab: bool = None,
        sender_type: SenderType = None,
        recipient_type: RecipientType = None,
    ) -> List[bool]:
        """Send message to all agents."""
        results = []
        get_logger(__name__).info("🚨 BULK MESSAGE ACTIVATED")
        get_logger(__name__).info("📋 SENDING TO ALL AGENTS")

        # CORRECT ORDER: Agent-4 LAST
        agent_order = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
            "Agent-4",
        ]

        for agent_id in agent_order:
            success = self.send_message(
                content=content,
                sender=sender,
                recipient=agent_id,
                message_type=message_type,
                priority=priority,
                tags=tags,
                metadata=metadata,
                mode=mode,
                use_paste=use_paste,
                new_tab_method=new_tab_method,
                use_new_tab=use_new_tab,
                sender_type=sender_type,
                recipient_type=recipient_type,
            )
            results.append(success)
            time.sleep(1)  # Brief pause between agents

        success_count = sum(results)
        total_count = len(results)
        get_logger(__name__).info(
            f"📊 BULK MESSAGE COMPLETED: {success_count}/{total_count} successful"
        )
        return results
