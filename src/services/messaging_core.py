#!/usr/bin/env python3
"""
Core Messaging Service - Agent Cellphone V2
=========================================

Core messaging functionality for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import os
import time
from typing import List, Dict, Any

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .messaging_pyautogui import PyAutoGUIMessagingDelivery


class UnifiedMessagingCore:
    """Core unified messaging service functionality."""
    
    def __init__(self):
        """Initialize the core messaging service."""
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
        
        # Initialize PyAutoGUI delivery
        self.pyautogui_delivery = PyAutoGUIMessagingDelivery(self.agents)
    
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
        return self.pyautogui_delivery.send_message_via_pyautogui(message, use_paste)
    
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
        print(f"📊 BULK ONBOARDING COMPLETED: {success_count}/{total_count} successful")
        return results
    
    def send_message(self, content: str, sender: str, recipient: str, 
                    message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                    priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
                    tags: List[UnifiedMessageTag] = None,
                    metadata: Dict[str, Any] = None,
                    mode: str = "pyautogui",
                    use_paste: bool = True) -> bool:
        """Send a single message to a specific agent."""
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        print(f"✅ MESSAGE CREATED: {sender} → {recipient}")
        print(f"🎯 Type: {message_type.value}")
        print(f"🆔 Message ID: {message.message_id}")
        
        # Deliver the message
        delivery_success = False
        if mode == "pyautogui":
            delivery_success = self.send_message_via_pyautogui(message, use_paste)
        else:
            delivery_success = self.send_message_to_inbox(message)
        
        if delivery_success:
            print(f"✅ MESSAGE DELIVERED TO {recipient}")
        else:
            print(f"❌ MESSAGE DELIVERY FAILED TO {recipient}")
        
        print()
        return delivery_success
    
    def send_to_all_agents(self, content: str, sender: str,
                          message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                          priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
                          tags: List[UnifiedMessageTag] = None,
                          metadata: Dict[str, Any] = None,
                          mode: str = "pyautogui",
                          use_paste: bool = True) -> List[bool]:
        """Send message to all agents."""
        results = []
        print(f"🚨 BULK MESSAGE ACTIVATED")
        print(f"📋 SENDING TO ALL AGENTS")
        
        # CORRECT ORDER: Agent-4 LAST
        agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
        
        for agent_id in agent_order:
            success = self.send_message(
                content=content,
                sender=sender,
                recipient=agent_id,
                message_type=message_type,
                priority=priority,
                tags=tags or [],
                metadata=metadata or {},
                mode=mode,
                use_paste=use_paste
            )
            results.append(success)
            time.sleep(1)  # Brief pause between agents
        
        success_count = sum(results)
        total_count = len(results)
        print(f"📊 BULK MESSAGE COMPLETED: {success_count}/{total_count} successful")
        return results
    
    def list_agents(self):
        """List all available agents."""
        print("📋 AVAILABLE AGENTS:")
        print("=" * 50)
        for agent_id, info in self.agents.items():
            print(f"🤖 {agent_id}: {info['description']}")
            print(f"   📍 Coordinates: {info['coords']}")
            print(f"   📬 Inbox: {self.inbox_paths.get(agent_id, 'N/A')}")
            print()
    
    def show_coordinates(self):
        """Show agent coordinates."""
        print("📍 AGENT COORDINATES:")
        print("=" * 30)
        for agent_id, info in self.agents.items():
            print(f"🤖 {agent_id}: {info['coords']}")
        print()
    
    def show_message_history(self):
        """Show message history."""
        print("📜 MESSAGE HISTORY:")
        print("=" * 30)
        for i, message in enumerate(self.messages, 1):
            print(f"{i}. {message.sender} → {message.recipient}")
            print(f"   Type: {message.message_type.value}")
            print(f"   Priority: {message.priority.value}")
            print(f"   ID: {message.message_id}")
            print()
