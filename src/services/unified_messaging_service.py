#!/usr/bin/env python3
"""
Unified Messaging Service - Agent Cellphone V2
============================================

Complete unified messaging service with CLI interface and PyAutoGUI delivery.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
import sys
import time
import os
from typing import List, Optional, Dict, Any

# Import models
try:
    from .models.unified_message import (
        UnifiedMessage,
        UnifiedMessageType,
        UnifiedMessagePriority,
        UnifiedMessageStatus,
        UnifiedMessageTag,
    )
except ImportError:
    # Fallback if models are not available
    from dataclasses import dataclass
    from datetime import datetime
    from enum import Enum
    import uuid
    
    class UnifiedMessageType(Enum):
        TEXT = "text"
        BROADCAST = "broadcast"
        ONBOARDING = "onboarding"
    
    class UnifiedMessagePriority(Enum):
        NORMAL = "normal"
        URGENT = "urgent"
    
    class UnifiedMessageStatus(Enum):
        SENT = "sent"
        DELIVERED = "delivered"
    
    class UnifiedMessageTag(Enum):
        CAPTAIN = "captain"
        ONBOARDING = "onboarding"
        WRAPUP = "wrapup"
    
    @dataclass
    class UnifiedMessage:
        content: str
        sender: str
        recipient: str
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT
        priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL
        tags: List[UnifiedMessageTag] = None
        metadata: Dict[str, Any] = None
        timestamp: datetime = None
        message_id: str = None
        
        def __post_init__(self):
            if self.tags is None:
                self.tags = []
            if self.metadata is None:
                self.metadata = {}
            if self.timestamp is None:
                self.timestamp = datetime.now()
            if self.message_id is None:
                self.message_id = f"msg_{self.timestamp.strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ WARNING: PyAutoGUI not available. Install with: pip install pyautogui")

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    print("⚠️ WARNING: Pyperclip not available. Install with: pip install pyperclip")


class UnifiedMessagingService:
    """Unified messaging service for all messaging scenarios."""
    
    def __init__(self):
        """Initialize the messaging service."""
        self.messages: List[UnifiedMessage] = []
        # CORRECT ORDER: Agent-4 LAST
        self.agents = {
            "Agent-1": {"description": "Integration & Core Systems Specialist", "coords": (-1269, 481)},
            "Agent-2": {"description": "Architecture & Design Specialist", "coords": (-308, 480)},
            "Agent-3": {"description": "Infrastructure & DevOps Specialist", "coords": (-1269, 1001)},
            "Agent-5": {"description": "Business Intelligence Specialist", "coords": (652, 421)},
            "Agent-6": {"description": "Gaming & Entertainment Specialist", "coords": (1612, 419)},
            "Agent-7": {"description": "Web Development Specialist", "coords": (653, 940)},
            "Agent-8": {"description": "Integration & Performance Specialist", "coords": (1611, 941)},
            "Agent-4": {"description": "Quality Assurance Specialist (CAPTAIN)", "coords": (-308, 1000)},
        }
        
        # Agent inbox paths
        self.inbox_paths = {
            "Agent-1": "agent_workspaces/Agent-1/inbox",
            "Agent-2": "agent_workspaces/Agent-2/inbox", 
            "Agent-3": "agent_workspaces/Agent-3/inbox",
            "Agent-4": "agent_workspaces/Agent-4/inbox",
            "Agent-5": "agent_workspaces/Agent-5/inbox",
            "Agent-6": "agent_workspaces/Agent-6/inbox",
            "Agent-7": "agent_workspaces/Agent-7/inbox",
            "Agent-8": "agent_workspaces/Agent-8/inbox",
        }
        
        # EXISTING ONBOARDING PROMPT TO APPEND
        self.onboarding_prompt = """🎯 **ONBOARDING - FRIENDLY MODE** 🎯

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
    
    def send_message_to_inbox(self, message: UnifiedMessage) -> bool:
        """Send message to agent's inbox file."""
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
            
            # Write message to file
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
            
            print(f"📬 MESSAGE DELIVERED TO INBOX: {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ ERROR delivering message to inbox: {e}")
            return False
    
    def send_message_via_pyautogui(self, message: UnifiedMessage, use_paste: bool = True) -> bool:
        """Send message via PyAutoGUI to agent coordinates."""
        if not PYAUTOGUI_AVAILABLE:
            print("❌ ERROR: PyAutoGUI not available for coordinate delivery")
            return False
        
        try:
            recipient = message.recipient
            if recipient not in self.agents:
                print(f"❌ ERROR: Unknown recipient {recipient}")
                return False
            
            coords = self.agents[recipient]["coords"]
            
            # Move to agent coordinates
            pyautogui.moveTo(coords[0], coords[1], duration=0.5)
            print(f"📍 MOVED TO {recipient} COORDINATES: {coords}")
            
            # Click to focus
            pyautogui.click()
            time.sleep(0.5)
            
            # Clear any existing content (Ctrl+A, Delete)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)
            
            # OPTIMIZED SEQUENCE: Send Ctrl+T to create new tab (no unnecessary message)
            pyautogui.hotkey('ctrl', 't')
            time.sleep(1.0)  # WAIT FOR NEW TAB
            print(f"🆕 NEW TAB CREATED FOR {recipient}")
            
            # Now send the actual message
            if use_paste and PYPERCLIP_AVAILABLE:
                # Fast paste method - copy to clipboard and paste
                pyperclip.copy(message.content)
                time.sleep(1.0)  # INCREASED WAIT TIME BEFORE PASTING
                pyautogui.hotkey('ctrl', 'v')
                print(f"📋 FAST PASTED MESSAGE TO {recipient}")
            else:
                # Slow type method for special formatting
                content = message.content
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    pyautogui.write(line, interval=0.01)
                    if i < len(lines) - 1:
                        pyautogui.hotkey('shift', 'enter')
                        time.sleep(0.1)
                print(f"⌨️ TYPED MESSAGE TO {recipient} WITH PROPER FORMATTING")
            
            # Press Enter to send
            pyautogui.press('enter')
            print(f"📤 MESSAGE SENT VIA PYAUTOGUI TO {recipient}")
            
            return True
            
        except Exception as e:
            print(f"❌ ERROR sending via PyAutoGUI: {e}")
            return False
    
    def generate_onboarding_message(self, agent_id: str, style: str = "friendly") -> str:
        """Generate onboarding message for specific agent."""
        agent_info = self.agents.get(agent_id, {})
        description = agent_info.get("description", "Specialist")
        
        # APPEND EXISTING ONBOARDING PROMPT
        return self.onboarding_prompt.format(agent_id=agent_id, description=description)
    
    def send_onboarding_message(self, agent_id: str, style: str = "friendly", mode: str = "pyautogui") -> bool:
        """Send onboarding message to specific agent."""
        message_content = self.generate_onboarding_message(agent_id, style)
        
        message = UnifiedMessage(
            content=message_content,
            sender="Captain Agent-4",
            recipient=agent_id,
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
            metadata={"onboarding_style": style}
        )
        
        self.messages.append(message)
        print(f"✅ ONBOARDING MESSAGE CREATED: Captain Agent-4 → {agent_id}")
        print(f"🎯 Style: {style}")
        print(f"🆔 Message ID: {message.message_id}")
        
        # Deliver the message
        delivery_success = False
        if mode == "pyautogui":
            delivery_success = self.send_message_via_pyautogui(message, use_paste=True)
        else:
            delivery_success = self.send_message_to_inbox(message)
        
        if delivery_success:
            print(f"✅ ONBOARDING MESSAGE DELIVERED TO {agent_id}")
        else:
            print(f"❌ ONBOARDING MESSAGE DELIVERY FAILED TO {agent_id}")
        
        print()
        return delivery_success
    
    def send_bulk_onboarding(self, style: str = "friendly", mode: str = "pyautogui") -> List[bool]:
        """Send onboarding messages to all agents."""
        results = []
        print(f"🚨 BULK ONBOARDING ACTIVATED - {style.upper()} MODE")
        print(f"📋 CORRECT ORDER: Agent-4 will be onboarded LAST")
        
        # CORRECT ORDER: Agent-4 LAST
        agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
        
        for agent_id in agent_order:
            success = self.send_onboarding_message(agent_id, style, mode)
            results.append(success)
            time.sleep(1)  # Brief pause between agents
        
        success_count = sum(results)
        total_count = len(results)
        print(f"📊 BULK ONBOARDING COMPLETE: {success_count}/{total_count} agents onboarded")
        print(f"🎯 Agent-4 onboarded LAST as required")
        print()
        return results
    
    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
        tags: Optional[List[UnifiedMessageTag]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        mode: str = "inbox",
        use_paste: bool = True,
    ) -> UnifiedMessage:
        """Send a message to a recipient."""
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
        delivery_success = False
        if mode == "pyautogui":
            delivery_success = self.send_message_via_pyautogui(message, use_paste)
        else:  # Default to inbox
            delivery_success = self.send_message_to_inbox(message)
        
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
        metadata: Optional[Dict[str, Any]] = None,
        mode: str = "inbox",
        use_paste: bool = True,
    ) -> List[UnifiedMessage]:
        """Send a message to multiple recipients."""
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
        metadata: Optional[Dict[str, Any]] = None,
        mode: str = "inbox",
        use_paste: bool = True,
    ) -> List[UnifiedMessage]:
        """Send a message to all agents."""
        # CORRECT ORDER: Agent-4 LAST
        recipients = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
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
    
    def list_agents(self) -> None:
        """List all available agents."""
        print("🤖 AVAILABLE AGENTS (CORRECT ORDER - Agent-4 LAST):")
        print("=" * 60)
        agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
        for agent_id in agent_order:
            info = self.agents[agent_id]
            print(f"• {agent_id}: {info['description']} (Coords: {info['coords']})")
        print()
    
    def get_message_history(self) -> List[UnifiedMessage]:
        """Get message history."""
        return self.messages


def main():
    """Main CLI entry point."""
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
    
    # Onboarding flags (NEW - INTEGRATED)
    parser.add_argument("--onboarding", action="store_true", help="Onboarding mode - fast paste to all agents")
    parser.add_argument("--onboard", action="store_true", help="Comprehensive onboarding with contract assignment")
    parser.add_argument("--onboarding-style", choices=["friendly", "strict"], default="friendly", help="Onboarding message style")
    parser.add_argument("--wrapup", action="store_true", help="Wrapup sequence")
    
    # Utility options
    parser.add_argument("--coordinates", action="store_true", help="Show agent coordinates")
    parser.add_argument("--list-agents", action="store_true", help="List all agents")
    parser.add_argument("--history", action="store_true", help="Show message history")
    
    args = parser.parse_args()
    
    # Initialize service
    service = UnifiedMessagingService()
    
    # Handle utility commands
    if args.list_agents:
        service.list_agents()
        return
    
    if args.coordinates:
        print("📍 AGENT COORDINATES (CORRECT ORDER - Agent-4 LAST):")
        print("=" * 50)
        agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
        for agent_id in agent_order:
            info = service.agents[agent_id]
            print(f"• {agent_id}: {info['coords']}")
        print()
        return
    
    if args.history:
        messages = service.get_message_history()
        print("📚 MESSAGE HISTORY:")
        print("=" * 30)
        for msg in messages:
            print(f"• {msg.sender} → {msg.recipient}: {msg.content[:50]}...")
        print()
        return
    
    # Handle onboarding commands (NEW - INTEGRATED)
    if args.onboarding:
        print(f"🚨 ONBOARDING MODE ACTIVATED - {args.onboarding_style.upper()} STYLE")
        print(f"📋 CORRECT SEQUENCE: Click → Starter Input → Ctrl+N → Onboarding Prompt")
        print(f"🎯 CORRECT ORDER: Agent-4 will be onboarded LAST")
        service.send_bulk_onboarding(style=args.onboarding_style, mode=args.mode)
        return
    
    if args.onboard:
        print(f"🎯 COMPREHENSIVE ONBOARDING ACTIVATED - {args.onboarding_style.upper()} STYLE")
        # Send onboarding to all agents with contract assignment message
        onboarding_content = f"""🎯 **COMPREHENSIVE ONBOARDING - CONTRACT ASSIGNMENT** 🎯

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Style**: {args.onboarding_style.upper()}
**Mode**: Comprehensive with contract assignment

**MISSION ASSIGNMENT**:
1. **IMMEDIATE CONTRACT CLAIMING**: Use --get-next-task flag
2. **PERPETUAL MOTION**: Maintain continuous workflow
3. **SYSTEM COMPLIANCE**: Follow V2 coding standards
4. **COORDINATION**: Regular status updates to Captain

**CONTRACT SYSTEM READY**: 40+ contracts available for claiming
**MESSAGING SYSTEM**: PyAutoGUI coordination active
**EMERGENCY PROTOCOLS**: Available for crisis intervention

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
