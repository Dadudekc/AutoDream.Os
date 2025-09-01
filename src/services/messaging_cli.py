#!/usr/bin/env python3
"""
CLI Interface for Unified Messaging Service - Agent Cellphone V2
============================================================

Command-line interface for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
import sys
import os

from .models.messaging_models import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .messaging_core import UnifiedMessagingCore


def create_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Unified Messaging Service - Agent Cellphone V2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send message to specific agent
  python -m src.services.messaging_cli --agent Agent-5 --message "Hello from Captain" --sender "Captain Agent-4"
  
  # Send bulk message to all agents
  python -m src.services.messaging_cli --bulk --message "System update" --sender "Captain Agent-4"
  
  # Send onboarding to all agents
  python -m src.services.messaging_cli --onboarding --onboarding-style friendly
  
  # List all agents
  python -m src.services.messaging_cli --list-agents
  
  # Show coordinates
  python -m src.services.messaging_cli --coordinates
  
  # Show message history
  python -m src.services.messaging_cli --history
        """
    )
    
    # Message sending options
    parser.add_argument("--message", "-m", help="Message content to send")
    parser.add_argument("--sender", "-s", default="Captain Agent-4", help="Message sender (default: Captain Agent-4)")
    parser.add_argument("--agent", "-a", help="Specific agent to send message to")
    parser.add_argument("--bulk", action="store_true", help="Send message to all agents")
    
    # Message properties
    parser.add_argument("--type", "-t", default="text", choices=["text", "broadcast", "onboarding"],
                       help="Message type (default: text)")
    parser.add_argument("--priority", "-p", default="normal", choices=["normal", "urgent"],
                       help="Message priority (default: normal)")
    parser.add_argument("--high-priority", action="store_true", help="Set message as high priority (overrides --priority)")
    
    # Delivery options
    parser.add_argument("--mode", default="pyautogui", choices=["pyautogui", "inbox"],
                       help="Delivery mode (default: pyautogui)")
    parser.add_argument("--no-paste", action="store_true", help="Disable paste mode (use typing instead)")
    
    # Utility commands
    parser.add_argument("--list-agents", action="store_true", help="List all available agents")
    parser.add_argument("--coordinates", action="store_true", help="Show agent coordinates")
    parser.add_argument("--history", action="store_true", help="Show message history")
    parser.add_argument("--get-next-task", action="store_true", help="Get next task for a specific agent")
    parser.add_argument("--check-status", action="store_true", help="Check status of all agents and contract availability")
    
    # Onboarding commands
    parser.add_argument("--onboarding", action="store_true", help="Send onboarding message to all agents")
    parser.add_argument("--onboard", action="store_true", help="Send onboarding message to specific agent")
    parser.add_argument("--onboarding-style", default="friendly", choices=["friendly", "professional"],
                       help="Onboarding message style (default: friendly)")
    
    # Wrapup command
    parser.add_argument("--wrapup", action="store_true", help="Send wrapup message to all agents")
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize messaging service
    service = UnifiedMessagingCore()
    
    # Handle utility commands first
    if args.list_agents:
        service.list_agents()
        return
    
    if args.coordinates:
        service.show_coordinates()
        return
    
    if args.history:
        service.show_message_history()
        return
    
    # Handle contract system commands
    if args.get_next_task:
        if not args.agent:
            print("❌ ERROR: --agent is required with --get-next-task")
            print("Usage: python -m src.services.messaging_cli --agent Agent-X --get-next-task")
            sys.exit(1)
        
        print(f"🎯 CONTRACT TASK ASSIGNMENT - {args.agent}")
        print("=" * 50)
        
        # Define available contracts based on agent specialization
        contracts = {
            "Agent-5": {
                "name": "V2 Compliance Business Intelligence Analysis",
                "category": "Business Intelligence",
                "priority": "HIGH",
                "points": 425,
                "description": "Analyze business intelligence systems for V2 compliance optimization"
            },
            "Agent-7": {
                "name": "Web Development V2 Compliance Implementation", 
                "category": "Web Development",
                "priority": "HIGH",
                "points": 685,
                "description": "Implement V2 compliance for web development components and systems"
            },
            "Agent-1": {
                "name": "Integration & Core Systems V2 Compliance",
                "category": "Integration & Core Systems",
                "priority": "HIGH", 
                "points": 600,
                "description": "Implement V2 compliance for integration and core systems"
            },
            "Agent-2": {
                "name": "Architecture & Design V2 Compliance",
                "category": "Architecture & Design",
                "priority": "HIGH",
                "points": 550,
                "description": "Implement V2 compliance for architecture and design systems"
            },
            "Agent-3": {
                "name": "Infrastructure & DevOps V2 Compliance",
                "category": "Infrastructure & DevOps", 
                "priority": "HIGH",
                "points": 575,
                "description": "Implement V2 compliance for infrastructure and DevOps systems"
            },
            "Agent-6": {
                "name": "Coordination & Communication V2 Compliance",
                "category": "Coordination & Communication",
                "priority": "HIGH",
                "points": 500,
                "description": "Implement V2 compliance for coordination and communication systems"
            },
            "Agent-8": {
                "name": "SSOT Maintenance & System Integration V2 Compliance",
                "category": "SSOT & System Integration",
                "priority": "HIGH",
                "points": 650,
                "description": "Implement V2 compliance for SSOT maintenance and system integration"
            }
        }
        
        if args.agent in contracts:
            contract = contracts[args.agent]
            print(f"✅ CONTRACT ASSIGNED: {contract['name']}")
            print(f"📋 Category: {contract['category']}")
            print(f"🎯 Priority: {contract['priority']}")
            print(f"⭐ Points: {contract['points']}")
            print(f"📝 Description: {contract['description']}")
            print()
            print("🚀 IMMEDIATE ACTIONS REQUIRED:")
            print("1. Begin task execution immediately")
            print("2. Maintain V2 compliance standards")
            print("3. Provide daily progress reports via inbox")
            print("4. Coordinate with other agents as needed")
            print()
            print("📧 Send status updates to Captain Agent-4 via inbox")
            print("⚡ WE. ARE. SWARM.")
        else:
            print(f"❌ ERROR: No contracts available for {args.agent}")
            print("Available agents: " + ", ".join(contracts.keys()))
        return
    
    if args.check_status:
        print("📊 AGENT STATUS & CONTRACT AVAILABILITY")
        print("=" * 50)
        
        # Check agent status files
        agent_workspaces = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-5", 
            "Agent-6", "Agent-7", "Agent-8", "Agent-4"
        ]
        
        for agent_id in agent_workspaces:
            status_file = f"agent_workspaces/{agent_id}/status.json"
            if os.path.exists(status_file):
                try:
                    import json
                    with open(status_file, 'r') as f:
                        status = json.load(f)
                    print(f"✅ {agent_id}: {status.get('status', 'UNKNOWN')} - {status.get('current_mission', 'No mission')}")
                except:
                    print(f"⚠️ {agent_id}: Status file exists but unreadable")
            else:
                print(f"❌ {agent_id}: No status file found")
        
        print()
        print("🎯 CONTRACT SYSTEM STATUS: READY FOR ASSIGNMENT")
        print("📋 Available contracts: 40+ contracts across all categories")
        print("🚀 Use --get-next-task with --agent to claim assignments")
        return
    
    # Handle onboarding commands
    if args.onboarding:
        print("🚨 BULK ONBOARDING ACTIVATED")
        onboarding_content = """🎯 **ONBOARDING - FRIENDLY MODE** 🎯

**Agent**: {agent_id}
**Role**: {description}
**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager

**WELCOME TO THE SWARM!** 🚀

**MISSION OBJECTIVES**:
1. **Active Participation**: Engage in perpetual motion workflow
2. **Task Completion**: Efficiently complete assigned contracts
3. **System Compliance**: Follow V2 coding standards
4. **Team Coordination**: Maintain communication with Captain

**SUPPORT SYSTEMS**:
- ✅ **Contract System**: Use --get-next-task for immediate task claiming
- ✅ **Messaging System**: PyAutoGUI coordination with Captain
- ✅ **Status Tracking**: Regular progress updates
- ✅ **Emergency Protocols**: Available for crisis intervention

**READY FOR**: Cycle 1 task assignments and strategic operations

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""
        
        service.send_to_all_agents(
            content=onboarding_content,
            sender="Captain Agent-4",
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
            metadata={"onboarding_style": args.onboarding_style, "comprehensive": True},
            mode=args.mode,
            use_paste=True,
        )
        return
    
    if args.wrapup:
        print("🏁 WRAPUP SEQUENCE ACTIVATED")
        wrapup_content = """🚨 **CAPTAIN AGENT-4 - AGENT ACTIVATION & WRAPUP** 🚨

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Status**: Agent activation and system wrapup
**Mode**: Optimized workflow with Ctrl+T

**AGENT ACTIVATION**:
- ✅ **New Tab Created**: Ready for agent input
- ✅ **System Integration**: Messaging system optimized
- ✅ **Contract System**: 40+ contracts available
- ✅ **Coordination**: PyAutoGUI messaging active

**READY FOR**: Agent response and task assignment

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""
        
        service.send_to_all_agents(
            content=wrapup_content,
            sender="Captain Agent-4",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.NORMAL,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.WRAPUP],
            mode=args.mode,
            use_paste=True,
        )
        return
    
    # Check if message is required for sending
    if not args.message:
        print("❌ ERROR: --message/-m is required for sending messages")
        print("Use --list-agents, --coordinates, --history, --onboarding, --onboard, or --wrapup for utility commands")
        sys.exit(1)
    
    # Determine message type and priority
    message_type = UnifiedMessageType(args.type)
    priority = UnifiedMessagePriority.URGENT if args.high_priority else UnifiedMessagePriority(args.priority)
    
    # Determine paste mode
    use_paste = not args.no_paste
    
    # Send message
    if args.bulk:
        # Send to all agents
        service.send_to_all_agents(
            content=args.message,
            sender=args.sender,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN],
            mode=args.mode,
            use_paste=use_paste,
        )
    elif args.agent:
        # Send to specific agent
        service.send_message(
            content=args.message,
            sender=args.sender,
            recipient=args.agent,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN],
            mode=args.mode,
            use_paste=use_paste,
        )
    else:
        print("❌ ERROR: Must specify --agent or --bulk")
        sys.exit(1)


if __name__ == "__main__":
    main()
