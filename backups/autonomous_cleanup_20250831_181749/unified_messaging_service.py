#!/usr/bin/env python3
"""
Unified Messaging Service - Agent Cellphone V2
============================================

Complete unified messaging service with CLI interface and PyAutoGUI delivery.

Author: Agent-1 (PERPETUAL MOTION LEADER - CORE SYSTEMS CONSOLIDATION SPECIALIST)
Mission: LOC COMPLIANCE OPTIMIZATION - Unified Messaging Service
License: MIT
"""

import sys
from typing import List, Optional
from .models.unified_message import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)
from .messaging.onboarding_service import OnboardingService
from .messaging.delivery_service import MessageDeliveryService
from .messaging.cli_handler import CLIMessageHandler


class UnifiedMessagingService:
    """Unified messaging service for all messaging scenarios"""
    
    def __init__(self):
        """Initialize the messaging service"""
        self.messages: List[UnifiedMessage] = []
        self.onboarding_service = OnboardingService()
        self.delivery_service = MessageDeliveryService()
        self.cli_handler = CLIMessageHandler()
    
    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
        tags: Optional[List[UnifiedMessageTag]] = None,
        metadata: Optional[dict] = None,
        mode: str = "inbox",
        use_paste: bool = True,
    ) -> UnifiedMessage:
        """Send a message to a recipient"""
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        self.messages.append(message)
        print(f"✅ MESSAGE CREATED: {sender} → {recipient}")
        print(f"📝 Content: {content[:100]}{'...' if len(content) > 100 else ''}")
        print(f"🏷️ Type: {message_type.value}")
        print(f"⚡ Priority: {priority.value}")
        print(f"🆔 Message ID: {message.message_id}")
        
        # Actually deliver the message
        delivery_success = self.delivery_service.deliver_message(message, mode, use_paste)
        
        if delivery_success:
            print(f"✅ MESSAGE DELIVERED SUCCESSFULLY TO {recipient}")
        else:
            print(f"❌ MESSAGE DELIVERY FAILED TO {recipient}")
        
        print()
        return message
    
    def send_bulk_message(
        self,
        content: str,
        sender: str,
        recipients: List[str],
        message_type: UnifiedMessageType = UnifiedMessageType.BROADCAST,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
        tags: Optional[List[UnifiedMessageTag]] = None,
        metadata: Optional[dict] = None,
        mode: str = "inbox",
        use_paste: bool = True,
    ) -> List[UnifiedMessage]:
        """Send a message to multiple recipients"""
        messages = []
        for recipient in recipients:
            message = self.send_message(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=message_type,
                priority=priority,
                tags=tags,
                metadata=metadata,
                mode=mode,
                use_paste=use_paste,
            )
            messages.append(message)
        
        print(f"📢 BULK MESSAGE SENT: {sender} → {len(recipients)} recipients")
        print()
        return messages
    
    def send_to_all_agents(
        self,
        content: str,
        sender: str,
        message_type: UnifiedMessageType = UnifiedMessageType.BROADCAST,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
        tags: Optional[List[UnifiedMessageTag]] = None,
        metadata: Optional[dict] = None,
        mode: str = "inbox",
        use_paste: bool = True,
    ) -> List[UnifiedMessage]:
        """Send a message to all agents"""
        recipients = list(self.delivery_service.agents.keys())
        return self.send_bulk_message(
            content=content,
            sender=sender,
            recipients=recipients,
            message_type=message_type,
            priority=priority,
            tags=tags,
            metadata=metadata,
            mode=mode,
            use_paste=use_paste,
        )
    
    def send_onboarding_message(self, agent_id: str, style: str = "friendly", mode: str = "pyautogui") -> bool:
        """Send onboarding message to specific agent"""
        message = self.onboarding_service.create_onboarding_message(agent_id, style)
        
        self.messages.append(message)
        print(f"✅ ONBOARDING MESSAGE CREATED: Captain Agent-4 → {agent_id}")
        print(f"🎯 Style: {style}")
        print(f"🆔 Message ID: {message.message_id}")
        
        # Deliver the message
        delivery_success = self.delivery_service.deliver_message(message, mode, use_paste=True)
        
        if delivery_success:
            print(f"✅ ONBOARDING MESSAGE DELIVERED TO {agent_id}")
        else:
            print(f"❌ ONBOARDING MESSAGE DELIVERY FAILED TO {agent_id}")
        
        print()
        return delivery_success
    
    def send_bulk_onboarding(self, style: str = "friendly", mode: str = "pyautogui") -> List[bool]:
        """Send onboarding messages to all agents"""
        results = []
        print(f"🚨 BULK ONBOARDING ACTIVATED - {style.upper()} MODE")
        
        agent_ids = list(self.delivery_service.agents.keys())
        for agent_id in agent_ids:
            success = self.send_onboarding_message(agent_id, style, mode)
            results.append(success)
        
        success_count = sum(results)
        total_count = len(results)
        print(f"📊 BULK ONBOARDING COMPLETE: {success_count}/{total_count} agents onboarded")
        print()
        return results
    
    def list_agents(self) -> None:
        """List all available agents"""
        self.delivery_service.list_agents()
    
    def get_message_history(self) -> List[UnifiedMessage]:
        """Get message history"""
        return self.messages


def main():
    """Main CLI entry point"""
    service = UnifiedMessagingService()
    success = service.cli_handler.run()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
