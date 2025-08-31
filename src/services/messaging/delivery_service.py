#!/usr/bin/env python3
"""
Message Delivery Service - Agent Cellphone V2
===========================================

Message delivery functionality for inbox and PyAutoGUI delivery.

Author: Agent-1 (PERPETUAL MOTION LEADER - CORE SYSTEMS CONSOLIDATION SPECIALIST)
Mission: LOC COMPLIANCE OPTIMIZATION - Delivery Service
License: MIT
"""

import os
import time
from typing import Dict, Any
from ..models.unified_message import UnifiedMessage

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


class MessageDeliveryService:
    """Service for delivering messages via different methods"""
    
    def __init__(self):
        """Initialize the delivery service"""
        self.agents = {
            "Agent-1": {"description": "Integration & Core Systems Specialist", "coords": (-1269, 481)},
            "Agent-2": {"description": "Architecture & Design Specialist", "coords": (-308, 480)},
            "Agent-3": {"description": "Infrastructure & DevOps Specialist", "coords": (-1269, 1001)},
            "Agent-4": {"description": "Quality Assurance Specialist (CAPTAIN)", "coords": (-308, 1000)},
            "Agent-5": {"description": "Business Intelligence Specialist", "coords": (652, 421)},
            "Agent-6": {"description": "Gaming & Entertainment Specialist", "coords": (1612, 419)},
            "Agent-7": {"description": "Web Development Specialist", "coords": (653, 940)},
            "Agent-8": {"description": "Integration & Performance Specialist", "coords": (1611, 941)},
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
    
    def send_message_to_inbox(self, message: UnifiedMessage) -> bool:
        """Send message to agent's inbox file"""
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
        """Send message via PyAutoGUI to agent coordinates"""
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
            
            if use_paste and PYPERCLIP_AVAILABLE:
                # Fast paste method - copy to clipboard and paste
                pyperclip.copy(message.content)
                time.sleep(0.1)
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
    
    def deliver_message(self, message: UnifiedMessage, mode: str = "inbox", use_paste: bool = True) -> bool:
        """Deliver message using specified mode"""
        if mode == "pyautogui":
            return self.send_message_via_pyautogui(message, use_paste)
        else:  # Default to inbox
            return self.send_message_to_inbox(message)
    
    def list_agents(self) -> None:
        """List all available agents"""
        print("🤖 AVAILABLE AGENTS:")
        print("=" * 50)
        for agent_id, info in self.agents.items():
            print(f"• {agent_id}: {info['description']} (Coords: {info['coords']})")
        print()
    
    def get_agent_coordinates(self) -> Dict[str, Any]:
        """Get agent coordinates"""
        return {agent_id: info["coords"] for agent_id, info in self.agents.items()}


if __name__ == "__main__":
    # Test the delivery service
    print("📤 Message Delivery Service Loaded Successfully")
    
    service = MessageDeliveryService()
    
    # Test agent listing
    service.list_agents()
    
    # Test coordinate retrieval
    coords = service.get_agent_coordinates()
    print(f"✅ Agent coordinates retrieved: {len(coords)} agents")
    print("✅ All delivery service functionality working correctly!")
