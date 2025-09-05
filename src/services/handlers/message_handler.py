"""
Message Handler - V2 Compliant Module
====================================

Handles message-related commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional

from ..messaging_core import UnifiedMessagingCore
from ..models.messaging_models import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    UnifiedMessageTag, SenderType, RecipientType
)
from ..unified_messaging_imports import load_coordinates_from_json


class MessageHandler:
    """
    Handles message-related commands for messaging CLI.
    
    Manages message creation, sending, and delivery.
    """
    
    def __init__(self):
        """Initialize message handler."""
        self.messaging_core = UnifiedMessagingCore()
        self.message_history = []
        self.sent_count = 0
        self.failed_count = 0
    
    def handle_message_commands(self, args) -> bool:
        """Handle message-related commands."""
        try:
            if not args.message:
                return False
            
            # Validate required arguments
            if not args.agent and not args.bulk:
                print("❌ Error: --agent or --bulk required")
                return True
            
            # Determine message type
            message_type = UnifiedMessageType.TEXT
            if args.type == "broadcast":
                message_type = UnifiedMessageType.BROADCAST
            elif args.type == "onboarding":
                message_type = UnifiedMessageType.ONBOARDING
            
            # Determine priority
            priority = UnifiedMessagePriority.REGULAR
            if args.high_priority or args.priority == "urgent":
                priority = UnifiedMessagePriority.URGENT
            
            if args.bulk:
                return self._handle_bulk_message(args, message_type, priority)
            else:
                return self._handle_single_message(args, message_type, priority)
                
        except Exception as e:
            print(f"❌ Error handling message command: {e}")
            return False
    
    def _handle_bulk_message(self, args, message_type: UnifiedMessageType, priority: UnifiedMessagePriority) -> bool:
        """Handle bulk message sending."""
        try:
            # Send to all agents
            agents = load_coordinates_from_json()
            if not agents:
                print("❌ No agent coordinates found")
                return True
            
            success_count = 0
            for agent_id in agents.keys():
                message = self.messaging_core.create_message(
                    content=args.message,
                    sender=args.sender,
                    recipient=agent_id,
                    message_type=message_type,
                    priority=priority,
                    sender_type=SenderType.SYSTEM,
                    recipient_type=RecipientType.AGENT
                )
                
                if message:
                    success = self.messaging_core.send_message(message, mode=args.mode)
                    if success:
                        success_count += 1
                        self.sent_count += 1
                        print(f"✅ Message sent to {agent_id}")
                    else:
                        self.failed_count += 1
                        print(f"❌ Failed to send message to {agent_id}")
                else:
                    self.failed_count += 1
                    print(f"❌ Failed to create message for {agent_id}")
            
            print(f"📊 Bulk message complete: {success_count}/{len(agents)} agents")
            return True
            
        except Exception as e:
            print(f"❌ Error in bulk message: {e}")
            return False
    
    def _handle_single_message(self, args, message_type: UnifiedMessageType, priority: UnifiedMessagePriority) -> bool:
        """Handle single message sending."""
        try:
            # Send to specific agent
            message = self.messaging_core.create_message(
                content=args.message,
                sender=args.sender,
                recipient=args.agent,
                message_type=message_type,
                priority=priority,
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )
            
            if message:
                success = self.messaging_core.send_message(message, mode=args.mode)
                if success:
                    self.sent_count += 1
                    print(f"✅ Message sent to {args.agent}")
                    return True
                else:
                    self.failed_count += 1
                    print(f"❌ Failed to send message to {args.agent}")
                    return False
            else:
                self.failed_count += 1
                print(f"❌ Failed to create message for {args.agent}")
                return False
                
        except Exception as e:
            print(f"❌ Error in single message: {e}")
            return False
    
    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        mode: str = "pyautogui"
    ) -> bool:
        """Send a message to specific recipient."""
        try:
            message = self.messaging_core.create_message(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=message_type,
                priority=priority,
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )
            
            if message:
                success = self.messaging_core.send_message(message, mode=mode)
                if success:
                    self.sent_count += 1
                    self.message_history.append({
                        "content": content,
                        "sender": sender,
                        "recipient": recipient,
                        "timestamp": "now",
                        "status": "sent"
                    })
                else:
                    self.failed_count += 1
                    self.message_history.append({
                        "content": content,
                        "sender": sender,
                        "recipient": recipient,
                        "timestamp": "now",
                        "status": "failed"
                    })
                return success
            return False
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def get_message_history(self) -> List[Dict[str, Any]]:
        """Get message history."""
        return self.message_history.copy()
    
    def get_message_stats(self) -> Dict[str, Any]:
        """Get message statistics."""
        return {
            "sent_count": self.sent_count,
            "failed_count": self.failed_count,
            "total_count": self.sent_count + self.failed_count,
            "success_rate": self.sent_count / max(self.sent_count + self.failed_count, 1) * 100
        }
    
    def clear_history(self):
        """Clear message history."""
        self.message_history.clear()
    
    def reset_stats(self):
        """Reset message statistics."""
        self.sent_count = 0
        self.failed_count = 0
    
    def get_message_status(self) -> Dict[str, Any]:
        """Get message handler status."""
        return {
            "sent_count": self.sent_count,
            "failed_count": self.failed_count,
            "history_count": len(self.message_history),
            "success_rate": self.sent_count / max(self.sent_count + self.failed_count, 1) * 100
        }
