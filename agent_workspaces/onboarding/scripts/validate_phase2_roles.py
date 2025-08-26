#!/usr/bin/env python3
"""
Phase 2 Role Validation Script - Agent Cellphone V2
==================================================

Validates that new agents understand their correct Phase 2 roles
and prevents role confusion that could delay Phase 2 completion.

Purpose: Ensure agents are onboarded with correct Phase 2 understanding
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class Phase2RoleValidator:
    """Validates Phase 2 agent roles and prevents confusion."""
    
    def __init__(self):
        """Initialize the role validator."""
        self.phase2_roles = {
            "Agent-1": "Integration & Core Systems",
            "Agent-2": "Manager Specialization",
            "Agent-3": "Integration & Testing", 
            "Agent-4": "Coordination & Phase 3 Preparation"
        }
        
        self.old_v1_roles = {
            "Agent-1": "Foundation & Testing",
            "Agent-2": "AI & ML Integration", 
            "Agent-3": "Multimedia & Content",
            "Agent-4": "Security & Infrastructure",
            "Agent-5": "Business Intelligence",
            "Agent-6": "Gaming & Entertainment",
            "Agent-7": "Web Development",
            "Agent-8": "Integration & Performance"
        }
        
        self.current_tasks = {
            "Agent-1": ["TASK 1B: Workflow Engine Integration", "TASK 1C: Health System Consolidation", "TASK 1D: Task Scheduler Consolidation"],
            "Agent-2": ["TASK 2: Manager Specialization", "TASK 2A: Status Manager Consolidation", "TASK 2B: Decision System Consolidation", "TASK 2C: Scaling System Consolidation"],
            "Agent-3": ["TASK 3: Integration & Testing", "TASK 3A: Workspace System Consolidation", "TASK 3B: Performance System Consolidation"],
            "Agent-4": ["TASK 4: Coordination & Phase 3 Preparation", "TASK 4A: Coordination System Consolidation"]
        }

    def validate_agent_role(self, agent_id: str, claimed_role: str) -> Dict[str, Any]:
        """Validate that an agent claims the correct Phase 2 role."""
        if agent_id not in self.phase2_roles:
            return {
                "valid": False,
                "error": f"Unknown agent ID: {agent_id}",
                "correct_role": None,
                "current_tasks": None
            }
        
        correct_role = self.phase2_roles[agent_id]
        is_correct = claimed_role.lower() == correct_role.lower()
        
        return {
            "valid": is_correct,
            "agent_id": agent_id,
            "claimed_role": claimed_role,
            "correct_role": correct_role,
            "current_tasks": self.current_tasks.get(agent_id, []),
            "old_v1_role": self.old_v1_roles.get(agent_id, "Unknown"),
            "error": None if is_correct else f"Role confusion detected! You claimed '{claimed_role}' but your Phase 2 role is '{correct_role}'"
        }

    def check_role_confusion(self, agent_id: str, claimed_role: str) -> Dict[str, Any]:
        """Check for common role confusion patterns."""
        validation = self.validate_agent_role(agent_id, claimed_role)
        
        if not validation["valid"]:
            # Check if they're claiming an old V1 role
            old_role = self.old_v1_roles.get(agent_id, "")
            if claimed_role.lower() in old_role.lower():
                validation["confusion_type"] = "V1_ROLE_CLAIMED"
                validation["confusion_message"] = f"❌ CRITICAL ROLE CONFUSION: You claimed '{claimed_role}' which is your OLD V1 role. Your CURRENT Phase 2 role is '{validation['correct_role']}'. STOP IMMEDIATELY and ask for clarification."
            else:
                validation["confusion_type"] = "UNKNOWN_ROLE"
                validation["confusion_message"] = f"❌ ROLE CONFUSION: You claimed '{claimed_role}' which is not a valid role. Your Phase 2 role is '{validation['correct_role']}'."
        
        return validation

    def generate_role_correction_message(self, agent_id: str, claimed_role: str) -> str:
        """Generate a role correction message for confused agents."""
        validation = self.check_role_confusion(agent_id, claimed_role)
        
        if validation["valid"]:
            return f"✅ Role validation successful! Agent-{agent_id} correctly identified as {validation['correct_role']}"
        
        message = f"""
🚨 AGENT-{agent_id} ROLE CORRECTION REQUIRED

❌ ROLE CONFUSION DETECTED:
- You claimed: "{claimed_role}"
- Your actual Phase 2 role: "{validation['correct_role']}"
- Your old V1 role was: "{validation['old_v1_role']}"

🎯 YOUR ACTUAL PHASE 2 RESPONSIBILITIES:
{validation['correct_role']}

📋 YOUR CURRENT ACTIVE TASKS:
"""
        
        for task in validation["current_tasks"]:
            message += f"• {task}\n"
        
        message += f"""
⏰ TOTAL WORKLOAD: {self._get_workload_hours(agent_id)} hours

🚨 IMMEDIATE ACTION REQUIRED:
1. STOP working on wrong tasks immediately
2. Review your actual Phase 2 role responsibilities
3. Start working on your assigned Phase 2 tasks
4. Ask for clarification if you're still confused

📚 READ THESE DOCUMENTS:
- agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
- agent_workspaces/onboarding/training_documents/ssot_agent_responsibilities_matrix.md

WE. ARE. SWARM. 🚀
"""
        return message

    def _get_workload_hours(self, agent_id: str) -> str:
        """Get estimated workload hours for an agent."""
        workload_map = {
            "Agent-1": "5-8",
            "Agent-2": "8-12", 
            "Agent-3": "6-9",
            "Agent-4": "2-3 + ongoing coordination"
        }
        return workload_map.get(agent_id, "Unknown")

    def run_validation_check(self, agent_id: str, claimed_role: str) -> None:
        """Run a complete role validation check."""
        print("🔍 PHASE 2 ROLE VALIDATION CHECK")
        print("=" * 50)
        
        validation = self.check_role_confusion(agent_id, claimed_role)
        
        if validation["valid"]:
            print(f"✅ Agent-{agent_id} role validation: SUCCESS")
            print(f"🎯 Role: {validation['correct_role']}")
            print(f"📋 Current Tasks: {len(validation['current_tasks'])} active tasks")
            print(f"⏰ Workload: {self._get_workload_hours(agent_id)} hours")
        else:
            print(f"❌ Agent-{agent_id} role validation: FAILED")
            print(f"🚨 {validation['confusion_message']}")
            print()
            print("📋 CORRECTION MESSAGE:")
            print(self.generate_role_correction_message(agent_id, claimed_role))


def main():
    """Main entry point for role validation."""
    if len(sys.argv) != 3:
        print("Usage: python validate_phase2_roles.py <agent_id> <claimed_role>")
        print("Example: python validate_phase2_roles.py Agent-3 'Multimedia & Content'")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    claimed_role = sys.argv[2]
    
    validator = Phase2RoleValidator()
    validator.run_validation_check(agent_id, claimed_role)


if __name__ == "__main__":
    main()
