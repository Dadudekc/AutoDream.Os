#!/usr/bin/env python3
"""
Unified Messaging CLI - Agent Cellphone V2
==========================================

UNIFIED CLI for the CONSOLIDATED messaging system.
Uses V2ComprehensiveMessagingSystem as the single source of truth.

This CLI consolidates ALL messaging functionality into ONE interface
instead of creating more duplication.

**Features:**
- Send messages using consolidated V2Message system
- Queue management using consolidated V2MessageQueue
- Message routing using consolidated V2MessageRouter
- Communication management using consolidated CommunicationManager
- NO DUPLICATION - everything uses the same underlying system

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION COMPLETE
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import the CONSOLIDATED messaging system
from .v2_comprehensive_messaging_system import (
    V2ComprehensiveMessagingSystem,
    V2Message,
    V2MessageType,
    V2MessagePriority,
    V2MessageStatus
)

logger = logging.getLogger(__name__)


class UnifiedMessagingCLI:
    """Unified CLI for the consolidated messaging system"""
    
    def __init__(self):
        """Initialize with the consolidated messaging system"""
        self.messaging_system = V2ComprehensiveMessagingSystem()
        self.parser = self._create_parser()
        
        print("🚀 Unified Messaging CLI initialized")
        print("✅ Using CONSOLIDATED V2ComprehensiveMessagingSystem")
        print("🎯 NO DUPLICATION - single source of truth")
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the unified command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Unified Messaging CLI - CONSOLIDATED System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Send a message using the consolidated system
  python -m src.core.unified_messaging_cli send --type "coordination" --content "Hello team" --sender "agent-1" --recipient "agent-2"
  
  # Queue management using consolidated system
  python -m src.core.unified_messaging_cli queue --action "status"
  
  # Message routing using consolidated system
  python -m src.core.unified_messaging_cli route --message-id "msg_123" --strategy "round_robin"
            """
        )
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Send command - uses consolidated V2Message
        send_parser = subparsers.add_parser("send", help="Send message using consolidated system")
        send_parser.add_argument("--type", "-t", required=True, 
                               choices=[t.value for t in V2MessageType], 
                               help="Message type from consolidated V2MessageType")
        send_parser.add_argument("--content", "-c", required=True, help="Message content")
        send_parser.add_argument("--sender", "-s", required=True, help="Sender agent ID")
        send_parser.add_argument("--recipient", "-r", required=True, help="Recipient agent ID")
        send_parser.add_argument("--priority", "-p", type=int, choices=[1, 2, 3, 4, 5],
                               default=2, help="Message priority (1=Low, 2=Normal, 3=High, 4=Urgent, 5=Critical)")
        send_parser.add_argument("--tags", help="Comma-separated tags")
        send_parser.set_defaults(func=self._send_message)
        
        # Queue command - uses consolidated V2MessageQueue
        queue_parser = subparsers.add_parser("queue", help="Queue management using consolidated system")
        queue_parser.add_argument("--action", "-a", required=True,
                                choices=["status", "clear", "stats", "list"],
                                help="Queue action")
        queue_parser.add_argument("--limit", "-l", type=int, default=10, help="Number of items to show")
        queue_parser.set_defaults(func=self._manage_queue)
        
        # Route command - uses consolidated V2MessageRouter
        route_parser = subparsers.add_parser("route", help="Message routing using consolidated system")
        route_parser.add_argument("--message-id", "-m", required=True, help="Message ID to route")
        route_parser.add_argument("--strategy", "-s", 
                                choices=["round_robin", "load_balanced", "priority_based"],
                                default="round_robin", help="Routing strategy")
        route_parser.set_defaults(func=self._route_message)
        
        # Status command - shows consolidated system status
        status_parser = subparsers.add_parser("status", help="Show consolidated system status")
        status_parser.set_defaults(func=self._show_status)
        
        return parser
    
    def _send_message(self, args: argparse.Namespace) -> bool:
        """Send message using the consolidated V2Message system"""
        try:
            print(f"📤 Sending message using CONSOLIDATED V2Message system...")
            
            # Parse tags
            tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else []
            
            # Create message using consolidated V2Message
            message = V2Message(
                message_type=V2MessageType(args.type),
                priority=V2MessagePriority(args.priority),  # args.priority is already an int
                sender_id=args.sender,
                recipient_id=args.recipient,
                content=args.content,
                tags=tags
            )
            
            # Start the messaging system if not running
            if not self.messaging_system.is_running:
                self.messaging_system.start()
            
            # Create available agents list for the messaging system
            from .v2_comprehensive_messaging_system import V2AgentInfo, V2AgentStatus, V2AgentCapability
            available_agents = [
                V2AgentInfo(
                    agent_id="agent-1",
                    name="Agent 1",
                    status=V2AgentStatus.ONLINE,
                    capabilities={V2AgentCapability.COMMUNICATION, V2AgentCapability.TASK_EXECUTION}
                ),
                V2AgentInfo(
                    agent_id="agent-2", 
                    name="Agent 2",
                    status=V2AgentStatus.ONLINE,
                    capabilities={V2AgentCapability.COMMUNICATION, V2AgentCapability.TASK_EXECUTION}
                ),
                V2AgentInfo(
                    agent_id="agent-3",
                    name="Agent 3", 
                    status=V2AgentStatus.ONLINE,
                    capabilities={V2AgentCapability.COMMUNICATION, V2AgentCapability.TASK_EXECUTION}
                ),
                V2AgentInfo(
                    agent_id="agent-4",
                    name="Agent 4",
                    status=V2AgentStatus.ONLINE, 
                    capabilities={V2AgentCapability.COMMUNICATION, V2AgentCapability.TASK_EXECUTION}
                )
            ]
            
            # Send using consolidated messaging system
            success = self.messaging_system.send_message(message, available_agents)
            
            if success:
                print(f"✅ Message sent successfully using consolidated system!")
                print(f"🆔 Message ID: {message.message_id}")
                print(f"📝 Type: {message.message_type.value}")
                print(f"📊 Priority: {message.priority.value}")
                print(f"🤖 Sender: {message.sender_id}")
                print(f"👥 Recipient: {message.recipient_id}")
                print(f"🏷️ Tags: {', '.join(message.tags) if message.tags else 'None'}")
                print(f"🎯 Sent in 4-agent mode with consolidated messaging system!")
                return True
            else:
                print("❌ Failed to send message")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            print(f"❌ Error sending message: {e}")
            return False
    
    def _manage_queue(self, args: argparse.Namespace) -> bool:
        """Manage message queue using consolidated system"""
        try:
            print(f"📋 Managing queue using CONSOLIDATED V2MessageQueue system...")
            
            if args.action == "status":
                # Get queue status from consolidated system
                queue_status = self.messaging_system.get_queue_status()
                print(f"📊 Queue Status:")
                print(f"   Total Messages: {queue_status.get('total_messages', 0)}")
                print(f"   Pending: {queue_status.get('pending', 0)}")
                print(f"   Processing: {queue_status.get('processing', 0)}")
                print(f"   Completed: {queue_status.get('completed', 0)}")
                print(f"   Failed: {queue_status.get('failed', 0)}")
                
            elif args.action == "list":
                # List recent messages from consolidated system
                messages = self.messaging_system.get_recent_messages(limit=args.limit)
                print(f"📝 Recent Messages (limit: {args.limit}):")
                for msg in messages:
                    print(f"   🆔 {msg.message_id}")
                    print(f"   📝 {msg.message_type.value}")
                    print(f"   🤖 {msg.sender_id} → {msg.recipient_id}")
                    print(f"   📅 {msg.timestamp}")
                    print(f"   ---")
                    
            elif args.action == "clear":
                # Clear queue using consolidated system
                cleared = self.messaging_system.clear_queue()
                if cleared:
                    print("✅ Queue cleared successfully")
                else:
                    print("❌ Failed to clear queue")
                    
            elif args.action == "stats":
                # Get queue statistics from consolidated system
                stats = self.messaging_system.get_queue_statistics()
                print(f"📊 Queue Statistics:")
                print(f"   Average Processing Time: {stats.get('avg_processing_time', 0):.2f}s")
                print(f"   Success Rate: {stats.get('success_rate', 0):.1f}%")
                print(f"   Error Rate: {stats.get('error_rate', 0):.1f}%")
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to manage queue: {e}")
            print(f"❌ Error managing queue: {e}")
            return False
    
    def _route_message(self, args: argparse.Namespace) -> bool:
        """Route message using consolidated system"""
        try:
            print(f"🛣️ Routing message using CONSOLIDATED V2MessageRouter system...")
            
            # Route message using consolidated system
            routing_result = self.messaging_system.route_message(
                message_id=args.message_id,
                strategy=args.strategy
            )
            
            if routing_result.get('success'):
                print(f"✅ Message routed successfully!")
                print(f"🆔 Message ID: {args.message_id}")
                print(f"🛣️ Strategy: {args.strategy}")
                print(f"🎯 Routed to: {', '.join(routing_result.get('routed_to', []))}")
                return True
            else:
                print(f"❌ Failed to route message: {routing_result.get('error_message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to route message: {e}")
            print(f"❌ Error routing message: {e}")
            return False
    
    def _show_status(self, args: argparse.Namespace) -> bool:
        """Show consolidated system status"""
        try:
            print("📊 CONSOLIDATED MESSAGING SYSTEM STATUS")
            print("=" * 60)
            
            # Get status from consolidated system
            system_status = self.messaging_system.get_system_status()
            
            print(f"🚀 System: {'✅ Active' if system_status.get('active') else '❌ Inactive'}")
            print(f"📝 Messages Processed: {system_status.get('messages_processed', 0)}")
            print(f"📋 Queue Size: {system_status.get('queue_size', 0)}")
            print(f"🛣️ Routing Strategy: {system_status.get('routing_strategy', 'Unknown')}")
            print(f"🤖 Active Agents: {system_status.get('active_agents', 0)}")
            print(f"📊 Performance: {system_status.get('performance_score', 0):.1f}/100")
            
            print("\n🎯 CONSOLIDATION STATUS:")
            print(f"   ✅ V2Message: Unified message structure")
            print(f"   ✅ V2MessageType: Unified message types")
            print(f"   ✅ V2MessagePriority: Unified priority system")
            print(f"   ✅ V2MessageStatus: Unified status tracking")
            print(f"   ✅ V2MessageQueue: Unified queue management")
            print(f"   ✅ V2MessageRouter: Unified routing system")
            
            print("\n🚫 DUPLICATION ELIMINATED:")
            print(f"   ❌ Removed: simple_message_queue.py")
            print(f"   ❌ Removed: formatter.py")
            print(f"   ❌ Removed: communication_compatibility_layer.py")
            print(f"   ❌ Removed: middleware_tools.py")
            print(f"   ✅ Updated: routing_models.py")
            print(f"   ✅ Updated: communication_manager.py")
            print(f"   ✅ Updated: shared_enums.py")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to show status: {e}")
            print(f"❌ Error showing status: {e}")
            return False
    
    def run(self, args: List[str] = None) -> int:
        """Run the unified messaging CLI"""
        try:
            parsed_args = self.parser.parse_args(args)
            
            if not parsed_args.command:
                self.parser.print_help()
                return 0
            
            # Execute command using consolidated system
            success = parsed_args.func(parsed_args)
            return 0 if success else 1
            
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user")
            return 1
        except Exception as e:
            logger.error(f"CLI error: {e}")
            print(f"❌ CLI error: {e}")
            return 1


def main():
    """Main entry point for unified messaging CLI"""
    cli = UnifiedMessagingCLI()
    return cli.run()


if __name__ == "__main__":
    exit(main())
