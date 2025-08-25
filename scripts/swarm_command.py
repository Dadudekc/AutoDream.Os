#!/usr/bin/env python3
"""
Universal Swarm Command Script - Agent Cellphone V2
==================================================

ANY AGENT can use this script to take command and direct the swarm.
This enables true decentralized swarm leadership.

Usage: python scripts/swarm_command.py [AGENT_ID] [COMMAND]
Example: python scripts/swarm_command.py agent_2 "Execute Phase 3 contracts"

Author: V2 SWARM SYSTEM
License: MIT
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from autonomous_development.agents.agent_coordinator import AgentCoordinator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SWARM COMMAND - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Universal Swarm Command Interface"""
    print("🤖" + "="*58 + "🤖")
    print("🎯 UNIVERSAL SWARM COMMAND INTERFACE")
    print("🤖" + "="*58 + "🤖")
    print()
    print("⚡ ANY AGENT CAN TAKE COMMAND OF THE SWARM")
    print("🎖️  Decentralized leadership enabled")
    print("🚀 Execute commands from any agent position")
    print()
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("❌ USAGE: python swarm_command.py [AGENT_ID] [COMMAND]")
        print("📋 EXAMPLES:")
        print("  python swarm_command.py agent_1")
        print("  python swarm_command.py agent_2 'Execute Phase 3'")
        print("  python swarm_command.py agent_3 'Show swarm status'")
        print("  python swarm_command.py agent_4 'Deploy team'")
        return False
    
    agent_id = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Initialize swarm coordinator
        print("📋 Initializing Swarm Coordinator...")
        coordinator = AgentCoordinator()
        
        print(f"✅ Swarm Active: {len(coordinator.get_all_agents())} agents ready")
        print(f"🎯 Command Capable: {len(coordinator.get_command_capable_agents())} agents")
        
        # Show available agents
        print("\n🤖 AVAILABLE AGENTS:")
        for agent in coordinator.get_all_agents():
            command_icon = "⚡" if "swarm_command" in agent.skills else "  "
            role_icon = "🎖️" if agent.role.value == "COORDINATOR" else "🤖"
            print(f"  {role_icon} {command_icon} {agent.agent_id}: {agent.name}")
            print(f"    Skills: {', '.join(agent.skills)}")
        
        # Check if requesting agent can take command
        if agent_id not in coordinator.agents:
            print(f"❌ AGENT NOT FOUND: {agent_id}")
            print("📋 Available agents:", [a.agent_id for a in coordinator.get_all_agents()])
            return False
        
        agent = coordinator.agents[agent_id]
        if "swarm_command" not in agent.skills:
            print(f"❌ AGENT {agent_id} LACKS COMMAND CAPABILITY")
            print(f"📋 Required skill: swarm_command")
            print(f"📋 Current skills: {', '.join(agent.skills)}")
            return False
        
        print(f"\n🎖️  AGENT {agent_id} ({agent.name}) TAKING COMMAND...")
        
        # Execute command if provided
        if command:
            print(f"📡 Executing command: {command}")
            success = coordinator.execute_swarm_command(agent_id, command)
            
            if success:
                print(f"✅ Command executed successfully by {agent_id}")
            else:
                print(f"❌ Command execution failed")
                return False
        else:
            # No command provided, show swarm status
            print(f"📊 Showing swarm status for {agent_id}...")
            status = coordinator.show_swarm_status(agent_id)
            print(status)
        
        # Show final swarm status
        print("\n" + "🤖" + "="*58 + "🤖")
        print("🎖️  SWARM COMMAND EXECUTION COMPLETE")
        print("🤖" + "="*58 + "🤖")
        
        print(f"👑 Commander: {agent_id} ({agent.name})")
        print(f"📡 Command: {command if command else 'Status Report'}")
        print(f"🤖 Swarm Size: {len(coordinator.agents)} agents")
        print(f"⚡ Command Capable: {len(coordinator.get_command_capable_agents())} agents")
        
        print("\n🎯 SWARM READY FOR NEXT COMMAND")
        print("💡 Any agent can take command using this script!")
        
    except Exception as e:
        logger.error(f"SWARM COMMAND ERROR: {e}")
        print(f"❌ SWARM COMMAND FAILURE: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("🤖 SWARM COMMAND: Initializing...")
    success = main()
    if success:
        print("\n🤖 SWARM STATUS: Command successful")
    else:
        print("\n🤖 SWARM STATUS: Command failed")
    sys.exit(0 if success else 1)
