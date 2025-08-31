#!/usr/bin/env python3
"""
CLI Handler - Agent Cellphone V2
==============================

Command-line interface handler for the unified messaging service.

Author: Agent-1 (PERPETUAL MOTION LEADER - CORE SYSTEMS CONSOLIDATION SPECIALIST)
Mission: LOC COMPLIANCE OPTIMIZATION - CLI Handler
License: MIT
"""

import argparse
import sys
from typing import List, Optional
from ..models.unified_message import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)
from .onboarding_service import OnboardingService
from .delivery_service import MessageDeliveryService


class CLIMessageHandler:
    """CLI handler for messaging operations"""
    
    def __init__(self):
        """Initialize the CLI handler"""
        self.onboarding_service = OnboardingService()
        self.delivery_service = MessageDeliveryService()
        self.messages: List[UnifiedMessage] = []
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser"""
        parser = argparse.ArgumentParser(description="Unified Messaging Service CLI")
        
        # Message options
        parser.add_argument("--message", "-m", help="Message content")
        parser.add_argument("--agent", "-a", help="Target agent (e.g., Agent-4)")
        parser.add_argument("--sender", "-s", default="Captain Agent-4", help="Message sender")
        parser.add_argument("--type", "-t", default="text", help="Message type")
        parser.add_argument("--priority", "-p", default="normal", help="Message priority")
        parser.add_argument("--high-priority", action="store_true", help="Set high priority")
        
        # Bulk messaging
        parser.add_argument("--bulk", action="store_true", help="Send to all agents")
        parser.add_argument("--mode", default="inbox", help="Messaging mode (inbox/pyautogui)")
        parser.add_argument("--no-paste", action="store_true", help="Disable fast pasting (use typing instead)")
        
        # Onboarding flags
        parser.add_argument("--onboarding", action="store_true", help="Onboarding mode - fast paste to all agents")
        parser.add_argument("--onboard", action="store_true", help="Comprehensive onboarding with contract assignment")
        parser.add_argument("--onboarding-style", choices=["friendly", "strict"], default="friendly", help="Onboarding message style")
        parser.add_argument("--wrapup", action="store_true", help="Wrapup sequence")
        
        # Utility options
        parser.add_argument("--coordinates", action="store_true", help="Show agent coordinates")
        parser.add_argument("--list-agents", action="store_true", help="List all agents")
        parser.add_argument("--history", action="store_true", help="Show message history")
        
        return parser
    
    def handle_utility_commands(self, args: argparse.Namespace) -> bool:
        """Handle utility commands"""
        if args.list_agents:
            self.delivery_service.list_agents()
            return True
        
        if args.coordinates:
            print("📍 AGENT COORDINATES:")
            print("=" * 30)
            coords = self.delivery_service.get_agent_coordinates()
            for agent_id, coord in coords.items():
                print(f"• {agent_id}: {coord}")
            print()
            return True
        
        if args.history:
            print("📚 MESSAGE HISTORY:")
            print("=" * 30)
            for msg in self.messages:
                print(f"• {msg.sender} → {msg.recipient}: {msg.content[:50]}...")
            print()
            return True
        
        return False
    
    def handle_onboarding_commands(self, args: argparse.Namespace) -> bool:
        """Handle onboarding commands"""
        if args.onboarding:
            print(f"🚨 ONBOARDING MODE ACTIVATED - {args.onboarding_style.upper()} STYLE")
            self._send_bulk_onboarding(args.onboarding_style, args.mode)
            return True
        
        if args.onboard:
            print(f"🎯 COMPREHENSIVE ONBOARDING ACTIVATED - {args.onboarding_style.upper()} STYLE")
            message = self.onboarding_service.create_comprehensive_onboarding_message(args.onboarding_style)
            self._deliver_to_all_agents(message, args.mode)
            return True
        
        if args.wrapup:
            print("🏁 WRAPUP SEQUENCE ACTIVATED")
            message = self.onboarding_service.create_wrapup_message()
            self._deliver_to_all_agents(message, args.mode)
            return True
        
        return False
    
    def handle_messaging_commands(self, args: argparse.Namespace) -> bool:
        """Handle regular messaging commands"""
        if not args.message:
            print("❌ ERROR: --message/-m is required for sending messages")
            print("Use --list-agents, --coordinates, --history, --onboarding, --onboard, or --wrapup for utility commands")
            return False
        
        # Determine message type and priority
        message_type = UnifiedMessageType(args.type)
        priority = UnifiedMessagePriority.URGENT if args.high_priority else UnifiedMessagePriority(args.priority)
        
        # Determine paste mode
        use_paste = not args.no_paste
        
        # Send message
        if args.bulk:
            self._send_bulk_message(args.message, args.sender, message_type, priority, args.mode, use_paste)
        elif args.agent:
            self._send_single_message(args.message, args.sender, args.agent, message_type, priority, args.mode, use_paste)
        else:
            print("❌ ERROR: Must specify --agent or --bulk")
            return False
        
        return True
    
    def _send_bulk_onboarding(self, style: str, mode: str) -> None:
        """Send onboarding messages to all agents"""
        agent_ids = list(self.delivery_service.agents.keys())
        
        for agent_id in agent_ids:
            message = self.onboarding_service.create_onboarding_message(agent_id, style)
            success = self.delivery_service.deliver_message(message, mode, use_paste=True)
            if success:
                print(f"✅ ONBOARDING MESSAGE DELIVERED TO {agent_id}")
            else:
                print(f"❌ ONBOARDING MESSAGE DELIVERY FAILED TO {agent_id}")
    
    def _deliver_to_all_agents(self, message: UnifiedMessage, mode: str) -> None:
        """Deliver message to all agents"""
        agent_ids = list(self.delivery_service.agents.keys())
        
        for agent_id in agent_ids:
            # Create individual message for each agent
            individual_message = UnifiedMessage(
                content=message.content,
                sender=message.sender,
                recipient=agent_id,
                message_type=message.message_type,
                priority=message.priority,
                tags=message.tags,
                metadata=message.metadata
            )
            
            success = self.delivery_service.deliver_message(individual_message, mode, use_paste=True)
            if success:
                print(f"✅ MESSAGE DELIVERED TO {agent_id}")
            else:
                print(f"❌ MESSAGE DELIVERY FAILED TO {agent_id}")
    
    def _send_bulk_message(self, content: str, sender: str, message_type: UnifiedMessageType, 
                          priority: UnifiedMessagePriority, mode: str, use_paste: bool) -> None:
        """Send bulk message to all agents"""
        agent_ids = list(self.delivery_service.agents.keys())
        
        for agent_id in agent_ids:
            message = UnifiedMessage(
                content=content,
                sender=sender,
                recipient=agent_id,
                message_type=message_type,
                priority=priority,
                tags=[UnifiedMessageTag.CAPTAIN]
            )
            
            self.messages.append(message)
            success = self.delivery_service.deliver_message(message, mode, use_paste)
            if success:
                print(f"✅ BULK MESSAGE DELIVERED TO {agent_id}")
            else:
                print(f"❌ BULK MESSAGE DELIVERY FAILED TO {agent_id}")
    
    def _send_single_message(self, content: str, sender: str, recipient: str, 
                           message_type: UnifiedMessageType, priority: UnifiedMessagePriority, 
                           mode: str, use_paste: bool) -> None:
        """Send single message to specific agent"""
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN]
        )
        
        self.messages.append(message)
        success = self.delivery_service.deliver_message(message, mode, use_paste)
        if success:
            print(f"✅ MESSAGE DELIVERED TO {recipient}")
        else:
            print(f"❌ MESSAGE DELIVERY FAILED TO {recipient}")
    
    def run(self, args: Optional[List[str]] = None) -> bool:
        """Run the CLI handler"""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        # Handle utility commands first
        if self.handle_utility_commands(parsed_args):
            return True
        
        # Handle onboarding commands
        if self.handle_onboarding_commands(parsed_args):
            return True
        
        # Handle regular messaging commands
        return self.handle_messaging_commands(parsed_args)


if __name__ == "__main__":
    # Test the CLI handler
    print("🎛️ CLI Handler Loaded Successfully")
    
    handler = CLIMessageHandler()
    
    # Test with help
    success = handler.run(["--help"])
    print(f"✅ CLI handler test completed: {success}")
    print("✅ All CLI handler functionality working correctly!")
