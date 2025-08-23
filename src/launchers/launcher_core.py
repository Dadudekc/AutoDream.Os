#!/usr/bin/env python3
"""
Launcher Core - Core Launcher Functionality

This module provides the core launcher functionality including:
- System initialization and validation
- Agent management and coordination
- Core launcher operations

Architecture: Single Responsibility Principle - core launcher functionality only
LOC: 150 lines (under 200 limit)
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, Optional, Any

# Fix Python path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent  # Go up two levels to project root
src_dir = project_root / "src"

# Add paths to Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_dir))

# Import core components
try:
    from src.services.agent_cell_phone import AgentCellPhone, MsgTag
except ImportError:
    # Fallback for when running directly
    AgentCellPhone = None
    MsgTag = None


class LauncherCore:
    """Core launcher functionality for the Agent Cellphone System"""

    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.system_ready = False

    def check_system(self) -> bool:
        """Check if the system can be imported and initialized."""
        try:
            print("🔍 Checking system imports...")

            # Test core imports
            if AgentCellPhone is None:
                print("❌ AgentCellPhone import failed")
                return False
            print("✅ AgentCellPhone imported successfully")

            if MsgTag is None:
                print("❌ MsgTag import failed")
                return False
            print(f"✅ MsgTag available: {MsgTag}")

            # Test configuration
            coord_file = Path("runtime/agent_comms/cursor_agent_coords.json")
            if coord_file.exists():
                print("✅ Coordinate configuration found")
            else:
                print("❌ Coordinate configuration missing")
                return False

            mode_file = Path("runtime/config/agents/modes.json")
            if mode_file.exists():
                print("✅ Mode configuration found")
            else:
                print("❌ Mode configuration not found (using defaults)")

            print("✅ System check passed")
            self.system_ready = True
            return True

        except Exception as e:
            print(f"❌ System check failed: {e}")
            return False

    def initialize_agents(self) -> bool:
        """Initialize all 5 agents with proper onboarding."""
        if not self.system_ready:
            print("❌ System not ready - run check_system() first")
            return False

        try:
            print("\n🚀 Initializing 5-Agent System...")

            # Create agent instances
            agent_ids = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]

            for agent_id in agent_ids:
                print(f"📱 Creating {agent_id}...")
                self.agents[agent_id] = AgentCellPhone(agent_id, "5-agent")
                print(f"✅ {agent_id} initialized successfully")

            print(f"✅ All {len(self.agents)} agents initialized")
            return True

        except Exception as e:
            print(f"❌ Agent initialization failed: {e}")
            return False

    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all agents."""
        status = {}
        for agent_id, agent in self.agents.items():
            try:
                # Basic status check - can be enhanced
                status[agent_id] = "online" if agent else "offline"
            except Exception:
                status[agent_id] = "error"
        return status

    def shutdown_agents(self) -> bool:
        """Shutdown all agents gracefully."""
        try:
            print("\n🔄 Shutting down agents...")
            for agent_id in list(self.agents.keys()):
                print(f"📱 Shutting down {agent_id}...")
                # Add any cleanup code here if needed
                del self.agents[agent_id]
            print("✅ All agents shut down")
            return True
        except Exception as e:
            print(f"❌ Error shutting down agents: {e}")
            return False


def main():
    """CLI interface for launcher core testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Launcher Core CLI")
    parser.add_argument("--check", action="store_true", help="Check system status")
    parser.add_argument("--init", action="store_true", help="Initialize agents")
    parser.add_argument("--status", action="store_true", help="Get agent status")
    parser.add_argument("--shutdown", action="store_true", help="Shutdown agents")

    args = parser.parse_args()

    launcher = LauncherCore()

    if args.check:
        launcher.check_system()
    elif args.init:
        if launcher.check_system():
            launcher.initialize_agents()
    elif args.status:
        status = launcher.get_agent_status()
        print("Agent Status:", status)
    elif args.shutdown:
        launcher.shutdown_agents()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
