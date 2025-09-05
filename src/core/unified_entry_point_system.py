#!/usr/bin/env python3
"""
Unified Entry Point System - Agent Cellphone V2
==============================================

Unified entry point for all CLI applications.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import asyncio
import sys
from typing import Any, Dict

from .unified_logging_system import get_logger
from ..services.unified_messaging_imports import load_coordinates_from_json


async def main():
    """Main CLI entry point."""
    try:
        # Create and configure parser
        from ..services.messaging_cli import create_parser
        parser = create_parser()
        args = parser.parse_args()

        # Initialize messaging service
        from ..services.messaging_core import UnifiedMessagingCore
        service = UnifiedMessagingCore()

        # Handle utility commands first
        if args.coordinates:
            await handle_coordinates_command(service)
            return
        
        if args.list_agents:
            await handle_list_agents_command(service)
            return
        
        if args.check_status:
            await handle_status_command(service)
            return
        
        if args.history:
            await handle_history_command(service)
            return

        # Handle onboarding commands
        if args.onboarding:
            await handle_onboarding_command(service, args)
            return
        
        if args.onboard and args.agent:
            await handle_single_onboard_command(service, args)
            return
        
        if args.wrapup:
            await handle_wrapup_command(service, args)
            return

        # Handle contract commands
        if args.get_next_task and args.agent:
            await handle_get_next_task_command(service, args)
            return
        
        if args.check_contracts:
            await handle_check_contracts_command(service)
            return

        # Handle regular message commands
        if args.message:
            if args.bulk:
                await handle_bulk_message_command(service, args)
            elif args.agent:
                await handle_single_message_command(service, args)
            else:
                print("❌ Error: --agent or --bulk required when sending messages")
                return

        # If no commands were handled, show help
        parser.print_help()

    except KeyboardInterrupt:
        get_logger(__name__).info("\n⚠️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        get_logger(__name__).info(f"❌ UNEXPECTED ERROR: {e}")
        sys.exit(1)


# Command handler functions
async def handle_coordinates_command(service):
    """Handle coordinates display command."""
    try:
        agents = load_coordinates_from_json()
        print("\n📍 Agent Coordinates:")
        print("=" * 40)
        print(f"{'Agent':<12} {'X':<8} {'Y':<8}")
        print("-" * 40)
        
        for agent_id, agent_data in sorted(agents.items()):
            coords = agent_data.get("coords", [0, 0])
            x, y = coords if len(coords) >= 2 else [0, 0]
            print(f"{agent_id:<12} {x:<8} {y:<8}")
        
        print("=" * 40)
        print(f"Total agents: {len(agents)}")
        
    except Exception as e:
        print(f"❌ Error loading coordinates: {e}")


async def handle_list_agents_command(service):
    """Handle list agents command."""
    try:
        agents = load_coordinates_from_json()
        agent_list = list(agents.keys())
        
        print("\n👥 Available Agents:")
        print("=" * 30)
        for i, agent in enumerate(sorted(agent_list), 1):
            print(f"{i:2d}. {agent}")
        print("=" * 30)
        print(f"Total: {len(agent_list)} agents")
        
    except Exception as e:
        print(f"❌ Error listing agents: {e}")


async def handle_status_command(service):
    """Handle status display command."""
    try:
        # Get basic status from UnifiedMessagingCore
        message_history = service.get_message_history()
        config = service.get_config()
        
        print("\n📊 Messaging System Status:")
        print("=" * 40)
        print(f"System Active: ✅ Operational")
        print(f"Messages Processed: {len(message_history)}")
        print(f"Configuration: {len(config)} settings loaded")
        print(f"Message History Limit: {config.get('message_history_limit', 'N/A')}")
        print(f"Delivery Timeout: {config.get('delivery_timeout', 'N/A')}s")
        print(f"Max Message Length: {config.get('max_message_length', 'N/A')}")
        print("=" * 40)
        
    except Exception as e:
        print(f"❌ Error getting status: {e}")


async def handle_history_command(service):
    """Handle message history command."""
    try:
        history = service.get_message_history()
        
        print("\n📜 Recent Message History:")
        print("=" * 50)
        
        if not history:
            print("No messages in history")
        else:
            # Show last 10 messages
            recent_messages = history[-10:] if len(history) > 10 else history
            for msg in recent_messages:
                print(f"ID: {getattr(msg, 'message_id', 'N/A')}")
                print(f"Time: {getattr(msg, 'timestamp', 'N/A')}")
                print(f"From: {getattr(msg, 'sender', 'N/A')}")
                print(f"To: {getattr(msg, 'recipient', 'N/A')}")
                print(f"Type: {getattr(msg, 'message_type', 'N/A')}")
                print("-" * 30)
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error getting history: {e}")


async def handle_onboarding_command(service, args):
    """Handle bulk onboarding command."""
    try:
        from ..services.messaging_message_builder import MessagingMessageBuilder
        
        builder = MessagingMessageBuilder()
        agents = load_coordinates_from_json()
        
        print(f"\n🚀 Starting bulk onboarding ({args.onboarding_style} style)...")
        
        messages = []
        for agent_id in agents.keys():
            msg = builder.build_onboarding_message(
                recipient=agent_id,
                style=args.onboarding_style,
                sender=args.sender
            )
            messages.append(msg)
        
        # Send messages
        result = await service.send_bulk_messages([
            {
                "message": msg.content,
                "recipient": msg.recipient,
                "sender": msg.sender,
                "message_type": msg.message_type.value,
                "priority": msg.priority.value
            }
            for msg in messages
        ])
        
        print(f"✅ Onboarding complete: {result['successful']} successful, {result['failed']} failed")
        
    except Exception as e:
        print(f"❌ Error during onboarding: {e}")


async def handle_single_onboard_command(service, args):
    """Handle single agent onboarding command."""
    try:
        from ..services.messaging_message_builder import MessagingMessageBuilder
        
        builder = MessagingMessageBuilder()
        msg = builder.build_onboarding_message(
            recipient=args.agent,
            style=args.onboarding_style,
            sender=args.sender
        )
        
        result = await service.send_message({
            "message": msg.content,
            "recipient": msg.recipient,
            "sender": msg.sender,
            "message_type": msg.message_type.value,
            "priority": msg.priority.value
        })
        
        if result.get("status") == "success":
            print(f"✅ Onboarding sent to {args.agent}")
        else:
            print(f"❌ Failed to send onboarding to {args.agent}")
        
    except Exception as e:
        print(f"❌ Error during single onboarding: {e}")


async def handle_wrapup_command(service, args):
    """Handle wrapup message command."""
    try:
        from ..services.messaging_message_builder import MessagingMessageBuilder
        
        builder = MessagingMessageBuilder()
        agents = load_coordinates_from_json()
        
        wrapup_content = "🎯 Mission wrapup - all agents please report final status"
        
        messages = []
        for agent_id in agents.keys():
            msg = builder.build_message(
                message=wrapup_content,
                recipient=agent_id,
                sender=args.sender,
                message_type="broadcast"
            )
            messages.append(msg)
        
        result = await service.send_bulk_messages([
            {
                "message": msg.content,
                "recipient": msg.recipient,
                "sender": msg.sender,
                "message_type": msg.message_type.value,
                "priority": msg.priority.value
            }
            for msg in messages
        ])
        
        print(f"✅ Wrapup sent: {result['successful']} successful, {result['failed']} failed")
        
    except Exception as e:
        print(f"❌ Error during wrapup: {e}")


async def handle_get_next_task_command(service, args):
    """Handle get next task command."""
    try:
        print(f"🔍 Getting next task for {args.agent}...")
        print("⚠️ Contract system not fully implemented yet")
        print("This would normally fetch the next available task from the contract system")
        
    except Exception as e:
        print(f"❌ Error getting next task: {e}")


async def handle_check_contracts_command(service):
    """Handle check contracts command."""
    try:
        print("📋 Checking contract status...")
        print("⚠️ Contract system not fully implemented yet")
        print("This would normally show the status of all contracts")
        
    except Exception as e:
        print(f"❌ Error checking contracts: {e}")


async def handle_single_message_command(service, args):
    """Handle single message send command."""
    try:
        from ..services.models.messaging_models import (
            UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        )
        
        # Create message object
        message = UnifiedMessage(
            content=args.message,
            recipient=args.agent,
            sender=args.sender,
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Send message using the core service
        result = service.send_message(message, mode="pyautogui")
        
        if result:
            print(f"✅ Message sent to {args.agent}")
        else:
            print(f"❌ Failed to send message to {args.agent}")
        
    except Exception as e:
        print(f"❌ Error sending message: {e}")


async def handle_bulk_message_command(service, args):
    """Handle bulk message send command."""
    try:
        agents = load_coordinates_from_json()
        agent_list = list(agents.keys())
        
        messages = []
        for agent_id in agent_list:
            message_data = {
                "message": args.message,
                "recipient": agent_id,
                "sender": args.sender,
                "message_type": args.type,
                "priority": args.priority
            }
            messages.append(message_data)
        
        result = await service.send_bulk_messages(messages)
        
        print(f"✅ Bulk message sent: {result['successful']} successful, {result['failed']} failed")
        
    except Exception as e:
        print(f"❌ Error sending bulk message: {e}")
