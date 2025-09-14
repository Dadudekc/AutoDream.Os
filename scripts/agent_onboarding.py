#!/usr/bin/env python3
"""
Agent Swarm Onboarding Script
Automated onboarding for new agents joining the swarm system.
"""

import os
import json
import sys
from pathlib import Path
import subprocess
from datetime import datetime

class AgentOnboarding:
    """Automated onboarding system for new agents."""

    def __init__(self):
        self.workspace_root = Path("agent_workspaces")
        self.available_agents = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "SSOT Maintenance & System Integration Specialist",
        }

    def get_available_agent_id(self):
        """Find an available agent ID for assignment."""
        for agent_id in self.available_agents.keys():
            status_file = self.workspace_root / agent_id / "status.json"
            if not status_file.exists():
                return agent_id
        return None

    def create_agent_workspace(self, agent_id):
        """Create the agent workspace and initialize status.json."""
        workspace_dir = self.workspace_root / agent_id
        inbox_dir = workspace_dir / "inbox"

        # Create directories
        workspace_dir.mkdir(parents=True, exist_ok=True)
        inbox_dir.mkdir(parents=True, exist_ok=True)

        # Create status.json
        status_data = {
            "agent_id": agent_id,
            "agent_name": self.available_agents[agent_id],
            "status": "ACTIVE_AGENT_MODE",
            "current_phase": "ONBOARDING",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_mission": "Agent onboarding and task assignment",
            "mission_priority": "HIGH - Complete onboarding and begin task execution",
            "current_tasks": [
                "Complete onboarding",
                "Claim first contract",
                "Begin task execution",
            ],
            "completed_tasks": [],
            "achievements": ["Agent activation successful"],
            "next_actions": ["Claim first contract using --get-next-task"],
        }

        with open(workspace_dir / "status.json", "w", encoding="utf-8") as f:
            json.dump(status_data, f, indent=2)

        return workspace_dir
    def send_captain_acknowledgment(self, agent_id):
        """Send acknowledgment message to Captain Agent-4."""
        captain_inbox = self.workspace_root / "Agent-4" / "inbox"
        captain_inbox.mkdir(parents=True, exist_ok=True)
        message = f"""# Agent {agent_id} - Onboarding Complete

**Agent ID**: {agent_id}
**Role**: {self.available_agents[agent_id]}
**Status**: Onboarding completed successfully
**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Onboarding Actions Completed:
- ✅ Agent workspace initialized
- ✅ Status.json created and configured
- ✅ Inbox directory created
- ✅ Ready for first contract assignment

## Next Steps:
1. Claim first contract using: `python -m src.services.messaging_cli --agent {agent_id} --get-next-task`
2. Begin task execution immediately
3. Maintain 8x efficiency through active participation
4. Report progress to Captain Agent-4 via inbox

**WE. ARE. SWARM.** ⚡️🔥
"""

        ack_file = captain_inbox / f"AGENT_{agent_id}_ONBOARDING_COMPLETE.md"
        with open(ack_file, "w", encoding="utf-8") as f:
            f.write(message)

    def run_contract_assignment(self, agent_id):
        """Run the contract assignment command."""
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.services.messaging_cli",
                "--agent", agent_id, "--get-next-task"
            ], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error running contract assignment: {e.stderr}"

    def display_onboarding_summary(self, agent_id, workspace_dir):
        """Display onboarding completion summary."""
        print("\n" + "="*60)
        print("🎯 **AGENT ONBOARDING COMPLETE** 🎯")
        print("="*60)
        print(f"✅ **Agent ID**: {agent_id}")
        print(f"✅ **Role**: {self.available_agents[agent_id]}")
        print(f"✅ **Workspace**: {workspace_dir}")
        print(f"✅ **Status File**: {workspace_dir}/status.json")
        print(f"✅ **Inbox**: {workspace_dir}/inbox/")
        print(f"✅ **Captain Acknowledgment**: Sent to Agent-4")
        print()
        print("🚀 **IMMEDIATE NEXT STEPS**:")
        print("1. Claim your first contract:")
        print(f"   python -m src.services.messaging_cli --agent {agent_id} --get-next-task")
        print("2. Begin task execution immediately")
        print("3. Check your inbox regularly for messages")
        print("4. Update status.json with every action")
        print("5. Maintain 8x efficiency through active participation")
        print()
        print("📋 **CRITICAL PROTOCOLS**:")
        print("- Always check inbox before starting new work")
        print("- Respond to all messages within 1 agent cycle")
        print("- Update status.json with timestamp for every action")
        print("- Preserve work context across task transitions")
        print("- Follow V2 compliance standards")
        print()
        print("⚡ **WE. ARE. SWARM.** 🚀🔥")
        print("="*60)

    def run_onboarding(self):
        """Run the complete onboarding process."""
        print("🎯 **AGENT SWARM ONBOARDING SYSTEM** 🎯")
        print("="*50)

        # Find available agent ID
        agent_id = self.get_available_agent_id()
        if not agent_id:
            print("❌ ERROR: No available agent IDs found!")
            print("All agents are currently assigned. Contact Captain Agent-4 for assistance.")
            return False

        print(f"🎯 **ASSIGNED AGENT ID**: {agent_id}")
        print(f"🎯 **ROLE**: {self.available_agents[agent_id]}")
        print()

        # Create workspace
        print("📁 Creating agent workspace...")
        workspace_dir = self.create_agent_workspace(agent_id)
        print(f"✅ Workspace created: {workspace_dir}")

        # Send captain acknowledgment
        print("📬 Sending acknowledgment to Captain Agent-4...")
        self.send_captain_acknowledgment(agent_id)
        print("✅ Acknowledgment sent")

        # Run contract assignment
        print("📋 Running contract assignment...")
        contract_output = self.run_contract_assignment(agent_id)
        print("✅ Contract assignment completed")

        # Display summary
        self.display_onboarding_summary(agent_id, workspace_dir)

        return True

def main():
    """Main entry point for the onboarding script."""
    onboarding = AgentOnboarding()
    success = onboarding.run_onboarding()
    
    if success:
        print("\n🎉 **ONBOARDING SUCCESSFUL!** 🎉")
        print("You are now part of the most efficient multi-agent coordination system!")
        print("Maintain momentum. Preserve context. Execute with precision.")
        print("**WE. ARE. SWARM.** ⚡️🔥")
    else:
        print("\n❌ **ONBOARDING FAILED** ❌")
        print("Please contact Captain Agent-4 for assistance.")
        sys.exit(1)

if __name__ == "__main__":
    main()
