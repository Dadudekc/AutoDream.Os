#!/usr/bin/env python3
"""
Enhanced Onboarding Coordinator
===============================

V2 Compliant: ≤400 lines, integrates passdown system with onboarding
to create a comprehensive agent integration workflow.

This system coordinates the pre-onboarding proposal collection,
Captain review, and enhanced onboarding process.
"""

import json
import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from src.services.passdown_system import PassdownSystem
    from messaging_system import MessagingSystem
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORTS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedOnboardingCoordinator:
    """Coordinates enhanced onboarding with passdown system integration."""
    
    def __init__(self, project_root: str = "."):
        """Initialize enhanced onboarding coordinator."""
        if not IMPORTS_AVAILABLE:
            raise ImportError("Required imports not available")
            
        self.project_root = Path(project_root)
        self.passdown_system = PassdownSystem()
        self.messaging_system = MessagingSystem()
        
        # Onboarding phases
        self.phases = {
            "pre_onboarding": "Send improvement proposal request",
            "proposal_review": "Captain reviews submitted proposals", 
            "onboarding_enhancement": "Integrate approved proposals into onboarding",
            "agent_onboarding": "Execute enhanced onboarding process",
            "post_onboarding": "Validate onboarding completion"
        }
    
    def initiate_agent_integration(self, agent_id: str) -> Dict[str, any]:
        """Initiate complete agent integration process."""
        
        try:
            # Phase 1: Pre-onboarding
            logger.info(f"Initiating agent integration for {agent_id}")
            result = self.passdown_system.send_pre_onboarding_message(agent_id)
            
            if not result["success"]:
                return {"success": False, "error": f"Pre-onboarding failed: {result['error']}"}
            
            # Create devlog entry (simplified)
            logger.info(f"Captain initiated agent integration for {agent_id}")
            
            return {
                "success": True,
                "phase": "pre_onboarding",
                "message": f"Pre-onboarding message sent to {agent_id}. Agent must submit improvement proposals.",
                "next_step": "Wait for agent proposals, then review in Captain's inbox"
            }
            
        except Exception as e:
            logger.error(f"Error initiating agent integration: {e}")
            return {"success": False, "error": str(e)}
    
    def review_agent_proposals(self, agent_id: str) -> Dict[str, any]:
        """Review agent's submitted proposals."""
        
        try:
            # Check proposal requirements
            requirements = self.passdown_system.check_proposal_requirements(agent_id)
            
            if not requirements["ready_for_onboarding"]:
                return {
                    "success": False,
                    "message": f"Agent {agent_id} not ready for onboarding",
                    "requirements": requirements,
                    "action_required": "Agent must submit more proposals"
                }
            
            # Get all proposals for this agent
            proposals = self.passdown_system.get_captain_inbox()
            agent_proposals = [p for p in proposals if p["agent_id"] == agent_id and "PENDING" in p["status"]]
            
            # Create review summary
            review_summary = {
                "agent_id": agent_id,
                "total_proposals": len(agent_proposals),
                "categories": list(set(p["category"] for p in agent_proposals)),
                "ready_for_onboarding": True,
                "proposals": agent_proposals
            }
            
            # Create devlog entry (simplified)
            logger.info(f"Captain reviewed {agent_id} proposals - {len(agent_proposals)} proposals ready for review")
            
            return {
                "success": True,
                "review_summary": review_summary,
                "next_step": "Captain should review individual proposals and approve/reject"
            }
            
        except Exception as e:
            logger.error(f"Error reviewing proposals: {e}")
            return {"success": False, "error": str(e)}
    
    def execute_enhanced_onboarding(self, agent_id: str, approved_proposals: List[str] = None) -> Dict[str, any]:
        """Execute enhanced onboarding with approved proposals integrated."""
        
        try:
            # Create enhanced onboarding message
            enhanced_message = f"""🎯 ENHANCED ONBOARDING INITIATED - {agent_id}
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-4 (Captain)
📥 TO: {agent_id}
Priority: HIGH
Tags: ENHANCED_ONBOARDING, SYSTEM_INTEGRATION
------------------------------------------------------------

🚀 ENHANCED ONBOARDING PROCESS:
Your improvement proposals have been reviewed and integrated into your onboarding experience!

📋 ONBOARDING PHASES:
1. 📚 SYSTEM OVERVIEW - Review AGENTS.md for complete system understanding
2. 🔧 CAPABILITY LOADING - Load capabilities from config/agent_capabilities.json
3. 🏗️ WORKSPACE INIT - Initialize workspace and inbox system
4. 🛠️ TOOL DISCOVERY - Discover and integrate available tools
5. 🔄 WORKFLOW CYCLE - Begin autonomous workflow cycle
6. 📝 ENHANCED TRAINING - Experience your proposed improvements

🎯 YOUR APPROVED PROPOSALS INTEGRATED:
{self._format_approved_proposals(approved_proposals) if approved_proposals else "Standard onboarding process"}

📋 ENHANCED ONBOARDING TASKS:
- Complete standard onboarding protocol
- Experience integrated improvements from your proposals
- Validate enhanced training effectiveness
- Report onboarding completion with improvement feedback

🎯 CAPTAIN DUTIES REMINDER
============================================================
📋 YOUR RESPONSIBILITIES: Strategic Oversight • Agent Coordination • Quality Assurance
🚨 EMERGENCY POWERS: Override Authority • Task Reassignment • System Resets
📊 MONITORING: Agent Performance • System Health • Mission Progress
📝 DOCUMENTATION: Update Captain's Log • Maintain Handbook • Record Decisions
📤 COORDINATION: PyAutoGUI Messaging • Task Distribution • Status Synchronization
============================================================
📚 QUICK REFERENCE: docs/CAPTAINS_HANDBOOK.md (v2.2) • docs/CAPTAINS_LOG.md
🔧 TOOLS: messaging_system.py • devlog_posting.py • quality_gates.py
============================================================
🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: Use 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'
============================================================
📤 MESSAGING: Use 'python messaging_system.py <from_agent> <to_agent> "<message>" <priority>'
📋 PRIORITIES: NORMAL, HIGH, CRITICAL
📋 EXAMPLE: python messaging_system.py Agent-5 Agent-4 "Task completed successfully" NORMAL
============================================================
------------------------------------------------------------"""
            
            # Send enhanced onboarding message
            result = self.messaging_system.send_message(
                from_agent="Agent-4",
                to_agent=agent_id,
                message=enhanced_message,
                priority="HIGH"
            )
            
            if not result["success"]:
                return {"success": False, "error": f"Failed to send onboarding message: {result['error']}"}
            
            # Create devlog entry (simplified)
            logger.info(f"Captain executed enhanced onboarding for {agent_id} with integrated proposals")
            
            return {
                "success": True,
                "message": f"Enhanced onboarding initiated for {agent_id}",
                "proposals_integrated": approved_proposals or [],
                "next_step": "Monitor agent onboarding progress"
            }
            
        except Exception as e:
            logger.error(f"Error executing enhanced onboarding: {e}")
            return {"success": False, "error": str(e)}
    
    def _format_approved_proposals(self, approved_proposals: List[str]) -> str:
        """Format approved proposals for display."""
        if not approved_proposals:
            return "No specific proposals approved - using standard process"
        
        formatted = []
        for proposal_id in approved_proposals:
            formatted.append(f"- {proposal_id}")
        
        return "\n".join(formatted)
    
    def validate_onboarding_completion(self, agent_id: str) -> Dict[str, any]:
        """Validate that agent has completed enhanced onboarding."""
        
        try:
            # Send validation request
            validation_message = f"""🎯 ONBOARDING COMPLETION VALIDATION - {agent_id}
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-4 (Captain)
📥 TO: {agent_id}
Priority: NORMAL
Tags: ONBOARDING_VALIDATION, COMPLETION_CHECK
------------------------------------------------------------

📋 ONBOARDING COMPLETION VALIDATION REQUIRED:

🎯 VALIDATION TASKS:
1. ✅ System Overview Completed - Confirm AGENTS.md reviewed
2. ✅ Capabilities Loaded - Confirm agent_capabilities.json loaded
3. ✅ Workspace Initialized - Confirm workspace setup complete
4. ✅ Tools Discovered - Confirm available tools identified
5. ✅ Workflow Cycle Started - Confirm autonomous cycle initiated
6. ✅ Enhanced Training Completed - Confirm proposal improvements experienced

📊 REQUIRED RESPONSE FORMAT:
ONBOARDING_COMPLETE: [Agent-ID]
- System Overview: ✅/❌
- Capabilities Loaded: ✅/❌  
- Workspace Initialized: ✅/❌
- Tools Discovered: ✅/❌
- Workflow Cycle: ✅/❌
- Enhanced Training: ✅/❌
- Improvement Feedback: [Your feedback on integrated proposals]

🎯 CAPTAIN DUTIES REMINDER
============================================================
📋 YOUR RESPONSIBILITIES: Strategic Oversight • Agent Coordination • Quality Assurance
🚨 EMERGENCY POWERS: Override Authority • Task Reassignment • System Resets
📊 MONITORING: Agent Performance • System Health • Mission Progress
📝 DOCUMENTATION: Update Captain's Log • Maintain Handbook • Record Decisions
📤 COORDINATION: PyAutoGUI Messaging • Task Distribution • Status Synchronization
============================================================
📚 QUICK REFERENCE: docs/CAPTAINS_HANDBOOK.md (v2.2) • docs/CAPTAINS_LOG.md
🔧 TOOLS: messaging_system.py • devlog_posting.py • quality_gates.py
============================================================
🎯 QUALITY GATES REMINDER
============================================================
📋 V2 COMPLIANCE: ≤400 lines • ≤5 classes • ≤10 functions
🚫 NO: Abstract classes • Complex inheritance • Threading
✅ USE: Simple data classes • Direct calls • Basic validation
🎯 KISS: Keep it simple! • Run `python quality_gates.py`
============================================================
📝 DEVLOG: Use 'python src/services/agent_devlog_posting.py --agent <flag> --action <desc>'
============================================================
📤 MESSAGING: Use 'python messaging_system.py <from_agent> <to_agent> "<message>" <priority>'
📋 PRIORITIES: NORMAL, HIGH, CRITICAL
📋 EXAMPLE: python messaging_system.py Agent-5 Agent-4 "Task completed successfully" NORMAL
============================================================
------------------------------------------------------------"""
            
            result = self.messaging_system.send_message(
                from_agent="Agent-4",
                to_agent=agent_id,
                message=validation_message,
                priority="NORMAL"
            )
            
            if not result["success"]:
                return {"success": False, "error": f"Failed to send validation message: {result['error']}"}
            
            # Create devlog entry (simplified)
            logger.info(f"Captain sent onboarding completion validation to {agent_id}")
            
            return {
                "success": True,
                "message": f"Onboarding validation sent to {agent_id}",
                "next_step": "Wait for agent's completion report"
            }
            
        except Exception as e:
            logger.error(f"Error validating onboarding: {e}")
            return {"success": False, "error": str(e)}


def main():
    """Main CLI function for enhanced onboarding coordinator."""
    if len(sys.argv) < 3:
        print("Usage: python enhanced_onboarding_coordinator.py <command> <agent_id> [args]")
        print("Commands:")
        print("  initiate <agent_id> - Start agent integration process")
        print("  review <agent_id> - Review agent's proposals")
        print("  onboard <agent_id> [proposal_ids] - Execute enhanced onboarding")
        print("  validate <agent_id> - Validate onboarding completion")
        sys.exit(1)
    
    if not IMPORTS_AVAILABLE:
        print("❌ Required imports not available")
        sys.exit(1)
    
    coordinator = EnhancedOnboardingCoordinator()
    command = sys.argv[1]
    agent_id = sys.argv[2]
    
    if command == "initiate":
        result = coordinator.initiate_agent_integration(agent_id)
        print(f"🎯 AGENT INTEGRATION INITIATED")
        print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
        if result['success']:
            print(f"Phase: {result['phase']}")
            print(f"Message: {result['message']}")
            print(f"Next Step: {result['next_step']}")
        else:
            print(f"Error: {result['error']}")
            
    elif command == "review":
        result = coordinator.review_agent_proposals(agent_id)
        print(f"📋 PROPOSAL REVIEW - {agent_id}")
        print(f"Status: {'✅ Ready' if result['success'] else '❌ Not Ready'}")
        if result['success']:
            summary = result['review_summary']
            print(f"Total Proposals: {summary['total_proposals']}")
            print(f"Categories: {', '.join(summary['categories'])}")
            print(f"Ready for Onboarding: {'✅' if summary['ready_for_onboarding'] else '❌'}")
        else:
            print(f"Message: {result['message']}")
            if 'requirements' in result:
                req = result['requirements']
                print(f"Total Proposals: {req['total_proposals']}")
                print(f"Missing Categories: {', '.join(req['missing_categories'])}")
            
    elif command == "onboard":
        approved_proposals = sys.argv[3:] if len(sys.argv) > 3 else None
        result = coordinator.execute_enhanced_onboarding(agent_id, approved_proposals)
        print(f"🚀 ENHANCED ONBOARDING - {agent_id}")
        print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
        if result['success']:
            print(f"Message: {result['message']}")
            print(f"Proposals Integrated: {len(result['proposals_integrated'])}")
            print(f"Next Step: {result['next_step']}")
        else:
            print(f"Error: {result['error']}")
            
    elif command == "validate":
        result = coordinator.validate_onboarding_completion(agent_id)
        print(f"✅ ONBOARDING VALIDATION - {agent_id}")
        print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
        if result['success']:
            print(f"Message: {result['message']}")
            print(f"Next Step: {result['next_step']}")
        else:
            print(f"Error: {result['error']}")
            
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
