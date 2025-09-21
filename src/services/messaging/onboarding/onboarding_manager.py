#!/usr/bin/env python3
"""
Onboarding Manager
==================

Manages agent onboarding functionality.
"""

import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class OnboardingManager:
    """Manages agent onboarding functionality."""

    def __init__(self, agent_coordinates: Dict[str, Any]):
        """Initialize onboarding manager."""
        self.agent_coordinates = agent_coordinates

    def start_agent_onboarding(self, dry_run: bool = False, specific_agent: str | None = None) -> int:
        """Start agent onboarding sequence."""
        try:
            print("🐝 **SWARM ONBOARDING SEQUENCE INITIATED** 🐝")
            print("=" * 60)

            # Get agents to onboard
            if specific_agent:
                agents_to_onboard = [specific_agent] if specific_agent in self.agent_coordinates else []
                if not agents_to_onboard:
                    print(f"❌ Agent {specific_agent} not found in coordinates")
                    return 1
            else:
                agents_to_onboard = list(self.agent_coordinates.keys())
            
            print(f"🎯 Onboarding {len(agents_to_onboard)} agent(s): {', '.join(agents_to_onboard)}")

            if dry_run:
                print("🔍 **DRY RUN MODE** - No actual clicking/pasting will occur")

            success_count = 0
            for agent_id in agents_to_onboard:
                try:
                    print(f"\n📋 Processing {agent_id}...")

                    # Get onboarding coordinates
                    coords = self._get_onboarding_coordinates(agent_id)
                    if not coords:
                        print(f"❌ No onboarding coordinates found for {agent_id}")
                        continue

                    # Create personalized onboarding message for this agent
                    personalized_message = self._create_onboarding_message(agent_id)

                    if dry_run:
                        print(f"🔍 Would click to coordinates: ({coords[0]}, {coords[1]})")
                        print(f"🔍 Would paste personalized onboarding message for {agent_id}")
                        success_count += 1
                    else:
                        # Click to onboarding coordinates
                        success = self._click_to_coordinates(coords)
                        if not success:
                            print(f"❌ Failed to click to coordinates for {agent_id}")
                            continue

                        # Paste onboarding message
                        success = self._paste_onboarding_message(personalized_message)
                        if not success:
                            print(f"❌ Failed to paste onboarding message for {agent_id}")
                            continue

                        print(f"✅ {agent_id} onboarding completed successfully")
                        success_count += 1

                except Exception as e:
                    print(f"❌ Error onboarding {agent_id}: {e}")
                    logger.error(f"Onboarding error for {agent_id}: {e}")

            print(f"\n🎉 Onboarding sequence completed: {success_count}/{len(agents_to_onboard)} successful")
            return 0 if success_count == len(agents_to_onboard) else 1

        except Exception as e:
            print(f"❌ Onboarding sequence failed: {e}")
            logger.error(f"Onboarding sequence error: {e}")
            return 1

    def _create_onboarding_message(self, agent_id: str) -> str:
        """Create personalized onboarding message for an agent."""
        agent_description = self._get_agent_description(agent_id)
        timestamp = self._get_current_timestamp()

        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-2
📥 TO: {agent_id}
Priority: NORMAL
Tags: ONBOARDING
------------------------------------------------------------
🐝 **SWARM ONBOARDING INITIATED** 🐝

Welcome to V2_SWARM, {agent_id}!

**AGENT PROFILE:**
- **Role**: {agent_description}
- **Status**: Active and ready for coordination
- **Integration**: V2_SWARM Enhanced System

**QUICK START GUIDE:**
1. **Check Inbox**: Review agent_workspaces/{agent_id}/inbox/ for messages
2. **Update Status**: Update your working_tasks.json with current status
3. **Claim Tasks**: Use --get-next-task to claim available work
4. **Coordinate**: Use PyAutoGUI messaging for team coordination
5. **Report**: Create devlogs for significant actions

**CURRENT SYSTEM STATUS:**
- **V2 Compliance**: 90%+ achieved across all components
- **Messaging System**: PyAutoGUI automation operational
- **Discord Commander**: Enhanced bot with full integration
- **Database**: Advanced caching and scalability systems active
- **Testing**: Comprehensive pytest framework operational

**COORDINATION PROTOCOLS:**
- **Team Alpha**: Agent-1, Agent-2, Agent-3, Agent-4
- **Team Beta**: Agent-5, Agent-6, Agent-7, Agent-8
- **Captain**: Agent-2 (Architecture & Design Specialist)
- **Communication**: PyAutoGUI messaging + Discord integration

**IMMEDIATE ACTIONS:**
1. Acknowledge this onboarding message
2. Review your agent workspace structure
3. Check for pending tasks in future_tasks.json
4. Begin autonomous operation cycle

**SYSTEM FEATURES:**
- **Enhanced Status Function**: Comprehensive system monitoring
- **V2 Compliance Pipeline**: Automated refactoring and validation
- **Modular Architecture**: Clean separation of concerns
- **Performance Optimization**: Advanced caching and scaling
- **Vector Database Integration**: Automatic knowledge storage and semantic search

**VECTOR DATABASE FEATURES:**
- **Automatic Message Storage**: All messages stored for semantic search
- **Knowledge Retrieval**: Search similar past experiences and solutions
- **Swarm Intelligence**: Learn from collective agent experiences
- **Experience Search**: Find how other agents solved similar problems

**VECTOR DATABASE COMMANDS:**
- `python tools/agent_vector_search.py --query "Discord bot issues" --limit 5`
- `python tools/agent_vector_search.py --agent Agent-4 --query "consolidation" --experience`
- `python tools/agent_vector_search.py --agent Agent-4 --knowledge-summary`
- `python tools/agent_vector_search.py --swarm-summary`

Ready for autonomous operation and team coordination!

🐝 **WE ARE SWARM** 🐝
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
Timestamp: {timestamp}
🐝 **SWARM ONBOARDING COMPLETE** 🐝"""

    def _get_onboarding_coordinates(self, agent_id: str) -> Tuple[int, int] | None:
        """Get onboarding coordinates for an agent."""
        try:
            if agent_id not in self.agent_coordinates:
                return None

            coords = self.agent_coordinates[agent_id]
            
            # Try to get onboarding coordinates first
            if hasattr(coords, 'onboarding_coordinates') and coords.onboarding_coordinates:
                return coords.onboarding_coordinates
            
            # Fallback to regular coordinates
            if hasattr(coords, 'x') and hasattr(coords, 'y'):
                return (coords.x, coords.y)
            
            # Try dictionary format
            if isinstance(coords, dict):
                if 'onboarding_coordinates' in coords:
                    return coords['onboarding_coordinates']
                if 'x' in coords and 'y' in coords:
                    return (coords['x'], coords['y'])
            
            return None

        except Exception as e:
            logger.error(f"Error getting onboarding coordinates for {agent_id}: {e}")
            return None

    def _click_to_coordinates(self, coords: Tuple[int, int]) -> bool:
        """Click to specified coordinates."""
        try:
            import pyautogui
            pyautogui.click(coords[0], coords[1])
            return True
        except Exception as e:
            logger.error(f"Error clicking to coordinates {coords}: {e}")
            return False

    def _paste_onboarding_message(self, message: str) -> bool:
        """Paste onboarding message."""
        try:
            import pyperclip
            import pyautogui
            
            # Copy message to clipboard
            pyperclip.copy(message)
            
            # Paste using Ctrl+V
# SECURITY: Key placeholder - replace with environment variable
            
            return True
        except Exception as e:
            logger.error(f"Error pasting onboarding message: {e}")
            return False

    def _get_agent_description(self, agent_id: str) -> str:
        """Get agent description."""
        descriptions = {
            "Agent-1": "Integration Specialist",
            "Agent-2": "Architecture & Design Specialist", 
            "Agent-3": "Database Specialist",
            "Agent-4": "Captain & Operations Coordinator",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Quality Assurance Specialist",
            "Agent-7": "Python Development & Testing Specialist",
            "Agent-8": "System Monitoring & Health Specialist"
        }
        return descriptions.get(agent_id, "Specialist Agent")

    def _get_current_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


