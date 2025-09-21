#!/usr/bin/env python3
"""
Onboarding Service
==================

Automated agent onboarding and initialization functionality.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

logger = logging.getLogger(__name__)


class OnboardingService:
    """Service for automated agent onboarding."""
    
    def __init__(self, messaging_service):
        """Initialize onboarding service with messaging service reference."""
        self.messaging_service = messaging_service
    
    def get_onboarding_coordinates(self) -> Dict[str, any]:
        """Get onboarding coordinates for all agents."""
        try:
            with open(self.messaging_service.coords_file) as f:
                data = json.load(f)
                agents = data.get("agents", {})
                onboarding_coords = {}
                for agent_id, agent_data in agents.items():
                    if "onboarding_coordinates" in agent_data:
                        onboarding_coords[agent_id] = agent_data["onboarding_coordinates"]
                return onboarding_coords
        except Exception as e:
            logger.error(f"Error loading onboarding coordinates: {e}")
            return {}
    
    def verify_coordinates(self, coords: tuple) -> bool:
        """Verify coordinates are valid."""
        if not coords or len(coords) != 2:
            return False
        
        x, y = coords
        return isinstance(x, (int, float)) and isinstance(y, (int, float))
    
    def click_coordinates(self, coords: tuple, pause: float = 1.0) -> bool:
        """Click coordinates using PyAutoGUI."""
        if not pyautogui:
            print("❌ PyAutoGUI not available")
            logger.error("PyAutoGUI not available")
            return False
        
        try:
            if not self.verify_coordinates(coords):
                print(f"❌ Invalid coordinates: {coords}")
                logger.error(f"Invalid coordinates: {coords}")
                return False
            
            print(f"   🖱️  Clicking coordinates: {coords[0]}, {coords[1]}")
            pyautogui.click(coords[0], coords[1])
            print(f"   ⏱️  Waiting {pause} seconds...")
            pyautogui.sleep(pause)
            return True
            
        except Exception as e:
            logger.error(f"Error clicking coordinates: {e}")
            return False
    
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
        if not pyautogui:
            logger.error("PyAutoGUI not available")
            return False
        
        try:
            if self._validate_coordinates(x, y):
                pyautogui.click(x, y)
                pyautogui.press('enter')
            else:
                return False
            
            pyautogui.sleep(pause)
            return True
            
        except Exception as e:
# SECURITY: Key placeholder - replace with environment variable
            return False
    
    def paste_message(self, message: str, pause: float = 2.0) -> bool:
        """Paste message using PyAutoGUI and Pyperclip."""
        if not pyautogui or not pyperclip:
            print("❌ PyAutoGUI or Pyperclip not available")
            logger.error("PyAutoGUI or Pyperclip not available")
            return False
        
        try:
            print("   📋 Copying message to clipboard...")
            pyperclip.copy(message)
            print("   🔧 Pasting message with Ctrl+V...")
            pyautogui.hotkey('ctrl', 'v')
            print(f"   ⏱️  Waiting {pause} seconds...")
            pyautogui.sleep(pause)
            return True
            
        except Exception as e:
            logger.error(f"Error pasting message: {e}")
            return False
    
    def get_base_onboarding_message(self, agent_id: str) -> str:
        """Get base onboarding message for agent."""
        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-4 (Captain)
📥 TO: {agent_id}
Priority: NORMAL
Tags: GENERAL
------------------------------------------------------------
WELCOME TO V2_SWARM - AGENT ONBOARDING INITIATED

**AGENT IDENTITY CONFIRMED:**
- Agent ID: {agent_id}
- Role: V2_SWARM Agent
- Status: ACTIVE
- Mission: Autonomous Agent Operations

**IMMEDIATE ACTIONS REQUIRED:**
1. **Read Quick Start Guide**: Check your workspace for quick start guide and read it immediately
2. **Check Inbox**: Review agent_workspaces/{agent_id}/inbox/ for messages
3. **Review Tasks**: Check working_tasks.json and future_tasks.json
4. **System Status**: Verify all systems operational
5. **Coordinate**: Report status to Captain Agent-4

**V2_SWARM PROTOCOLS:**
- Follow autonomous agent workflow
- Use messaging system for coordination
- Create devlogs for all actions
- Maintain V2 compliance standards
- Coordinate with swarm intelligence

**READY FOR AUTONOMOUS OPERATIONS - {agent_id} ONLINE!**
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
"""
    
    def get_captain_system_explanation(self) -> str:
        """Get captain's system explanation."""
        return """
**CAPTAIN SYSTEM EXPLANATION:**

**V2_SWARM ARCHITECTURE:**
- 8 Autonomous Agents with specialized roles
- PyAutoGUI-based coordinate communication
- Real-time messaging system
- Comprehensive devlog system
- V2 compliance standards

**CURRENT PROJECT STATE:**
- Database schema implementation in progress
- V2 compliance refactoring active
- Discord commander operational
- Agent coordination systems active

**MISSION PRIORITIES:**
1. V2 compliance achievement
2. Database schema completion
3. Agent coordination optimization
4. System integration testing

**READY FOR SWARM COORDINATION!**
"""
    
    def get_current_project_state(self) -> str:
        """Get current project state summary."""
        try:
            # Try to read project analysis if available
            project_analysis = Path("project_analysis.json")
            if project_analysis.exists():
                with open(project_analysis) as f:
                    data = json.load(f)
                    return f"""
**CURRENT PROJECT STATE:**
- Total Files: {data.get('total_files', 'Unknown')}
- V2 Compliance: {data.get('v2_compliance_percentage', 'Unknown')}%
- Last Scan: {data.get('scan_timestamp', 'Unknown')}
- Status: Active Development
"""
            else:
                return """
**CURRENT PROJECT STATE:**
- Status: Active Development
- Phase: V2 Compliance Refactoring
- Focus: Database Schema Implementation
- Agents: 8 Active
"""
        except Exception as e:
            logger.warning(f"Error reading project state: {e}")
            return "**CURRENT PROJECT STATE:** Active Development Phase"
    
    def get_captain_onboarding_message(self, agent_id: str) -> str:
        """Get complete captain onboarding message."""
        base_message = self.get_base_onboarding_message(agent_id)
        system_explanation = self.get_captain_system_explanation()
        project_state = self.get_current_project_state()
        
        return f"{base_message}\n{system_explanation}\n{project_state}"
    
    def execute_onboarding_sequence(self, agent_id: str, message: str) -> bool:
        """Execute complete onboarding sequence for agent."""
        print(f"\n🚀 STARTING ONBOARDING SEQUENCE FOR {agent_id}")
        print("=" * 60)
        
        try:
            # Get onboarding coordinates for specific agent
            print(f"📍 Step 1: Getting onboarding coordinates for {agent_id}...")
            onboarding_coords = self.get_onboarding_coordinates()
            if not onboarding_coords or agent_id not in onboarding_coords:
                print(f"❌ No onboarding coordinates found for {agent_id}")
                logger.error(f"No onboarding coordinates found for {agent_id}")
                return False
            
            agent_coords = onboarding_coords[agent_id]
            print(f"✅ Found coordinates for {agent_id}: {agent_coords}")
            
            # Click onboarding coordinates
            print(f"🖱️  Step 2: Clicking onboarding coordinates {agent_coords}...")
            if not self.click_coordinates(agent_coords, pause=1.0):
                print("❌ Failed to click onboarding coordinates")
                logger.error("Failed to click onboarding coordinates")
                return False
            print("✅ Successfully clicked onboarding coordinates")
            
            # Start new chat with Ctrl+N
            print("🆕 Step 3: Starting new chat with Ctrl+N...")
            if not self.start_new_chat():
                print("❌ Failed to start new chat")
                logger.error("Failed to start new chat")
                return False
            print("✅ Successfully started new chat")
            
            # Paste message
            print("📋 Step 4: Pasting onboarding message...")
            print(f"📝 Message length: {len(message)} characters")
            if not self.paste_message(message, pause=2.0):
                print("❌ Failed to paste onboarding message")
                logger.error("Failed to paste onboarding message")
                return False
            print("✅ Successfully pasted onboarding message")
            
            # Send message
            print("📤 Step 5: Sending message with Enter key...")
            if not self.send_message():
                print("❌ Failed to send onboarding message")
                logger.error("Failed to send onboarding message")
                return False
            print("✅ Successfully sent onboarding message")
            
            print(f"\n🎉 ONBOARDING SEQUENCE COMPLETED FOR {agent_id}")
            print("=" * 60)
            logger.info(f"Onboarding sequence completed for {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing onboarding sequence for {agent_id}: {e}")
            return False
    
    def hard_onboard_agent(self, agent_id: str) -> bool:
        """Hard onboard specific agent."""
        if not self.messaging_service._is_agent_active(agent_id):
            logger.warning(f"Agent {agent_id} is inactive, skipping onboarding")
            return False
        
        try:
            message = self.get_captain_onboarding_message(agent_id)
            return self.execute_onboarding_sequence(agent_id, message)
            
        except Exception as e:
            logger.error(f"Error hard onboarding agent {agent_id}: {e}")
            return False
    
    def hard_onboard_all_agents(self) -> Dict[str, bool]:
        """Hard onboard all active agents."""
        results = {}
        
        for agent_id in self.messaging_service.loader.get_agent_ids():
            if self.messaging_service._is_agent_active(agent_id):
                results[agent_id] = self.hard_onboard_agent(agent_id)
            else:
                results[agent_id] = False
                logger.info(f"Skipping inactive agent {agent_id}")
        
        return results
    
    def start_new_chat(self, pause: float = 1.0) -> bool:
        """Start new chat with Ctrl+N."""
        if not pyautogui:
            print("❌ PyAutoGUI not available")
            logger.error("PyAutoGUI not available")
            return False
        
        try:
            print("   🔧 Pressing Ctrl+N to start new chat...")
            # Start new chat
            pyautogui.hotkey('ctrl', 'n')
            print(f"   ⏱️  Waiting {pause} seconds...")
            pyautogui.sleep(pause)
            return True
            
        except Exception as e:
            print(f"❌ Error starting new chat: {e}")
            logger.error(f"Error starting new chat: {e}")
            return False
    
    def send_message(self, pause: float = 1.0) -> bool:
        """Send message with Enter key."""
        if not pyautogui:
            print("❌ PyAutoGUI not available")
            logger.error("PyAutoGUI not available")
            return False
        
        try:
            print("   🔧 Pressing Enter to send message...")
            # Send message
            pyautogui.press('enter')
            print(f"   ⏱️  Waiting {pause} seconds...")
            pyautogui.sleep(pause)
            return True
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            logger.error(f"Error sending message: {e}")
            return False


