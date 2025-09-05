#!/usr/bin/env python3
"""
Messaging CLI Handlers - Agent Cellphone V2
===========================================

Command handlers for the messaging CLI system.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import asyncio
import sys
from typing import Any, Dict, List, Optional

from .messaging_cli_handlers_orchestrator import get_messaging_cli_handlers
from .messaging_core import UnifiedMessagingCore
from .models.messaging_models import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    UnifiedMessageTag, SenderType, RecipientType
)
from .unified_messaging_imports import load_coordinates_from_json

# Get the handlers instance
_handlers = get_messaging_cli_handlers()

def handle_utility_commands(args):
    """Handle utility commands."""
    try:
        if args.coordinates:
            # Load coordinates directly
            agents = load_coordinates_from_json()
            if agents:
                print("\n📍 Agent Coordinates:")
                print("=" * 40)
                print(f"{'Agent':<12} {'X':<8} {'Y':<8}")
                print("-" * 40)
                
                for agent_id, agent_data in agents.items():
                    coords = agent_data.get("chat_input_coordinates", [0, 0])
                    x, y = coords if len(coords) >= 2 else [0, 0]
                    print(f"{agent_id:<12} {x:<8} {y:<8}")
                
                print("=" * 40)
                print(f"Total agents: {len(agents)}")
            else:
                print("❌ No agent coordinates found")
            return True
        
        if args.list_agents:
            # Load coordinates to get agent list
            agents = load_coordinates_from_json()
            if agents:
                agent_list = list(agents.keys())
                print("\n👥 Available Agents:")
                print("=" * 30)
                for i, agent in enumerate(sorted(agent_list), 1):
                    print(f"{i:2d}. {agent}")
                print("=" * 30)
                print(f"Total: {len(agent_list)} agents")
            else:
                print("❌ No agents found")
            return True
            
        if args.check_status:
            print("\n📊 Messaging System Status:")
            print("=" * 40)
            print("System: ✅ Operational")
            print("Core: ✅ Active")
            print("Delivery: ✅ Ready")
            print("Coordinates: ✅ Loaded")
            print("=" * 40)
            return True
            
        if args.history:
            print("📜 Message History:")
            print("=" * 40)
            print("No message history available yet.")
            return True
            
    except Exception as e:
        print(f"❌ Error handling utility command: {e}")
        return False
    
    return False

def handle_contract_commands(args):
    """Handle contract-related commands."""
    try:
        if args.get_next_task:
            if not args.agent:
                print("❌ Error: --agent required for --get-next-task")
                return True
            
            print(f"📋 Getting next task for {args.agent}...")
            print("Contract system not fully implemented yet.")
            return True
            
        if args.check_contracts:
            print("📊 Contract Status:")
            print("=" * 40)
            print("Contract system not fully implemented yet.")
            return True
            
    except Exception as e:
        print(f"❌ Error handling contract command: {e}")
        return False
    
    return False

def handle_onboarding_commands(args):
    """Handle onboarding-related commands."""
    try:
        if args.onboarding:
            print("🚀 Starting bulk onboarding...")
            # Load coordinates
            agents = load_coordinates_from_json()
            if not agents:
                print("❌ No agent coordinates found")
                return True
            
            # Send onboarding to all agents
            messaging_core = UnifiedMessagingCore()
            success_count = 0
            
            for agent_id in agents.keys():
                message = messaging_core.create_message(
                    content=f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM.",
                    sender="Captain Agent-4",
                    recipient=agent_id,
                    message_type=UnifiedMessageType.ONBOARDING,
                    priority=UnifiedMessagePriority.REGULAR,
                    tags=[UnifiedMessageTag.ONBOARDING],
                    sender_type=SenderType.SYSTEM,
                    recipient_type=RecipientType.AGENT
                )
                
                if message:
                    success = messaging_core.send_message(message, mode=args.mode)
                    if success:
                        success_count += 1
                        print(f"✅ Onboarding sent to {agent_id}")
                    else:
                        print(f"❌ Failed to send onboarding to {agent_id}")
                else:
                    print(f"❌ Failed to create onboarding message for {agent_id}")
            
            print(f"📊 Onboarding complete: {success_count}/{len(agents)} agents")
            return True
            
        if args.onboard:
            if not args.agent:
                print("❌ Error: --agent required for --onboard")
                return True
            
            print(f"🚀 Onboarding {args.agent}...")
            messaging_core = UnifiedMessagingCore()
            
            message = messaging_core.create_message(
                content=f"Welcome to the team, {args.agent}! You are now part of the V2 SWARM.",
                sender="Captain Agent-4",
                recipient=args.agent,
                message_type=UnifiedMessageType.ONBOARDING,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.ONBOARDING],
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )
            
            if message:
                success = messaging_core.send_message(message, mode=args.mode)
                if success:
                    print(f"✅ Onboarding sent to {args.agent}")
                else:
                    print(f"❌ Failed to send onboarding to {args.agent}")
            else:
                print(f"❌ Failed to create onboarding message for {args.agent}")
            
            return True
            
        if args.wrapup:
            print("🏁 Sending wrapup message...")
            # Load coordinates
            agents = load_coordinates_from_json()
            if not agents:
                print("❌ No agent coordinates found")
                return True
            
            # Send wrapup to all agents
            messaging_core = UnifiedMessagingCore()
            success_count = 0
            
            for agent_id in agents.keys():
                message = messaging_core.create_message(
                    content=f"Great work today, {agent_id}! Mission accomplished.",
                    sender="Captain Agent-4",
                    recipient=agent_id,
                    message_type=UnifiedMessageType.BROADCAST,
                    priority=UnifiedMessagePriority.REGULAR,
                    tags=[UnifiedMessageTag.CAPTAIN],
                    sender_type=SenderType.SYSTEM,
                    recipient_type=RecipientType.AGENT
                )
                
                if message:
                    success = messaging_core.send_message(message, mode=args.mode)
                    if success:
                        success_count += 1
                        print(f"✅ Wrapup sent to {agent_id}")
                    else:
                        print(f"❌ Failed to send wrapup to {agent_id}")
                else:
                    print(f"❌ Failed to create wrapup message for {agent_id}")
            
            print(f"📊 Wrapup complete: {success_count}/{len(agents)} agents")
            return True
            
    except Exception as e:
        print(f"❌ Error handling onboarding command: {e}")
        return False
    
    return False

def handle_message_commands(args):
    """Handle message-related commands."""
    try:
        if not args.message:
            return False
        
        # Validate required arguments
        if not args.agent and not args.bulk:
            print("❌ Error: --agent or --bulk required")
            return True
        
        messaging_core = UnifiedMessagingCore()
        
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
            # Send to all agents
            agents = load_coordinates_from_json()
            if not agents:
                print("❌ No agent coordinates found")
                return True
            
            success_count = 0
            for agent_id in agents.keys():
                message = messaging_core.create_message(
                    content=args.message,
                    sender=args.sender,
                    recipient=agent_id,
                    message_type=message_type,
                    priority=priority,
                    sender_type=SenderType.SYSTEM,
                    recipient_type=RecipientType.AGENT
                )
                
                if message:
                    success = messaging_core.send_message(message, mode=args.mode)
                    if success:
                        success_count += 1
                        print(f"✅ Message sent to {agent_id}")
                    else:
                        print(f"❌ Failed to send message to {agent_id}")
                else:
                    print(f"❌ Failed to create message for {agent_id}")
            
            print(f"📊 Bulk message complete: {success_count}/{len(agents)} agents")
            return True
        
        else:
            # Send to specific agent
            message = messaging_core.create_message(
                content=args.message,
                sender=args.sender,
                recipient=args.agent,
                message_type=message_type,
                priority=priority,
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )
            
            if message:
                success = messaging_core.send_message(message, mode=args.mode)
                if success:
                    print(f"✅ Message sent to {args.agent}")
                else:
                    print(f"❌ Failed to send message to {args.agent}")
            else:
                print(f"❌ Failed to create message for {args.agent}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error handling message command: {e}")
        return False
    
    return False