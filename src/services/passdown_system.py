#!/usr/bin/env python3
"""
Passdown System - Agent Improvement Proposals
=============================================

V2 Compliant: ≤400 lines, handles agent improvement proposals
for onboarding, workcycles, protocols, and additional tasks.

This system allows agents to propose enhancements that get
delivered to the Captain's inbox for review and implementation.
"""

import json
import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path for messaging system import
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from messaging_system import MessagingSystem
    MESSAGING_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    MESSAGING_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PassdownSystem:
    """Handles agent improvement proposals and passdown coordination."""
    
    def __init__(self, project_root: str = "."):
        """Initialize passdown system."""
        self.project_root = Path(project_root)
        self.inbox_dir = self.project_root / "captain_inbox"
        self.inbox_dir.mkdir(exist_ok=True)
        
        # Initialize messaging system if available
        self.messaging_system = None
        if MESSAGING_AVAILABLE:
            try:
                self.messaging_system = MessagingSystem()
            except Exception as e:
                logger.warning(f"Messaging system unavailable: {e}")
        
        # Passdown categories
        self.categories = {
            "onboarding": "Agent onboarding improvements and training enhancements",
            "workcycles": "Workflow cycle optimizations and protocol improvements", 
            "protocols": "Communication protocols and coordination procedures",
            "additional_tasks": "New task types and capability expansions",
            "system_improvements": "General system enhancements and optimizations"
        }
        
    def create_improvement_proposal(self, agent_id: str, category: str, 
                                  title: str, description: str, 
                                  rationale: str, priority: str = "NORMAL") -> Dict[str, any]:
        """Create improvement proposal for Captain review."""
        
        if category not in self.categories:
            return {"success": False, "error": f"Invalid category: {category}"}
            
        proposal = {
            "proposal_id": f"PROP_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{agent_id}",
            "agent_id": agent_id,
            "category": category,
            "title": title,
            "description": description,
            "rationale": rationale,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "status": "PENDING_CAPTAIN_REVIEW",
            "category_description": self.categories[category]
        }
        
        # Save to Captain's inbox
        try:
            proposal_file = self.inbox_dir / f"{proposal['proposal_id']}.json"
            with open(proposal_file, 'w') as f:
                json.dump(proposal, f, indent=2)
                
            logger.info(f"Improvement proposal created: {proposal['proposal_id']}")
            return {"success": True, "proposal_id": proposal['proposal_id'], "proposal": proposal}
            
        except Exception as e:
            logger.error(f"Failed to create proposal: {e}")
            return {"success": False, "error": str(e)}
    
    def get_captain_inbox(self) -> List[Dict[str, any]]:
        """Get all pending proposals from Captain's inbox."""
        proposals = []
        
        try:
            for proposal_file in self.inbox_dir.glob("PROP_*.json"):
                with open(proposal_file) as f:
                    proposal = json.load(f)
                    proposals.append(proposal)
                    
            # Sort by timestamp (newest first)
            proposals.sort(key=lambda x: x['timestamp'], reverse=True)
            return proposals
            
        except Exception as e:
            logger.error(f"Failed to read inbox: {e}")
            return []
    
    def review_proposal(self, proposal_id: str, captain_decision: str, 
                       captain_notes: str = "") -> Dict[str, any]:
        """Captain reviews and decides on proposal."""
        
        try:
            proposal_file = self.inbox_dir / f"{proposal_id}.json"
            
            if not proposal_file.exists():
                return {"success": False, "error": f"Proposal {proposal_id} not found"}
                
            with open(proposal_file) as f:
                proposal = json.load(f)
                
            # Update proposal with Captain decision
            proposal["status"] = f"CAPTAIN_{captain_decision.upper()}"
            proposal["captain_notes"] = captain_notes
            proposal["captain_review_timestamp"] = datetime.now().isoformat()
            
            # Save updated proposal
            with open(proposal_file, 'w') as f:
                json.dump(proposal, f, indent=2)
                
            logger.info(f"Captain reviewed proposal {proposal_id}: {captain_decision}")
            return {"success": True, "proposal": proposal}
            
        except Exception as e:
            logger.error(f"Failed to review proposal: {e}")
            return {"success": False, "error": str(e)}
    
    def create_passdown_message(self, agent_id: str, proposal_data: Dict[str, any]) -> str:
        """Create formatted passdown message for Captain's inbox."""
        
        return f"""📋 AGENT IMPROVEMENT PROPOSAL - {agent_id}
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {agent_id}
📥 TO: Agent-4 (Captain)
Priority: {proposal_data['priority']}
Tags: IMPROVEMENT_PROPOSAL, PASSDOWN
------------------------------------------------------------

🎯 IMPROVEMENT PROPOSAL DETAILS:
📋 PROPOSAL ID: {proposal_data['proposal_id']}
📂 CATEGORY: {proposal_data['category'].upper()}
📝 TITLE: {proposal_data['title']}

📊 CATEGORY DESCRIPTION:
{proposal_data['category_description']}

📋 PROPOSAL DESCRIPTION:
{proposal_data['description']}

💡 RATIONALE:
{proposal_data['rationale']}

🎯 CAPTAIN REVIEW REQUIRED:
- Review proposal in Captain's inbox
- Evaluate impact on system operations
- Decide: APPROVED, REJECTED, or NEEDS_REVISION
- Provide feedback and implementation guidance

📂 CAPTAIN INBOX LOCATION: captain_inbox/{proposal_data['proposal_id']}.json

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
    
    def get_available_categories(self) -> Dict[str, str]:
        """Get available proposal categories."""
        return self.categories.copy()
    
    def get_proposal_stats(self) -> Dict[str, int]:
        """Get statistics on proposals."""
        proposals = self.get_captain_inbox()
        
        stats = {
            "total_proposals": len(proposals),
            "pending_review": 0,
            "approved": 0,
            "rejected": 0,
            "by_category": {}
        }
        
        for proposal in proposals:
            status = proposal.get("status", "UNKNOWN")
            
            if "PENDING" in status:
                stats["pending_review"] += 1
            elif "APPROVED" in status:
                stats["approved"] += 1
            elif "REJECTED" in status:
                stats["rejected"] += 1
                
            category = proposal.get("category", "unknown")
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
        return stats
    
    def send_pre_onboarding_message(self, agent_id: str) -> Dict[str, any]:
        """Send pre-onboarding message to agent requesting improvement proposals."""
        
        if not self.messaging_system:
            return {"success": False, "error": "Messaging system not available"}
        
        message = f"""🎯 PRE-ONBOARDING IMPROVEMENT PROPOSAL REQUEST
============================================================
📋 AGENT: {agent_id}
📝 TASK: Submit improvement proposals before onboarding
🎯 PURPOSE: Enhance system based on agent expertise

📋 REQUIRED PROPOSALS:
1. ONBOARDING IMPROVEMENTS - How can we enhance agent training?
2. WORKCYCLE OPTIMIZATIONS - What workflow improvements do you suggest?
3. PROTOCOL ENHANCEMENTS - How can we improve coordination?
4. ADDITIONAL TASKS - What new capabilities should we add?

🎯 SUBMISSION INSTRUCTIONS:
Use: python src/services/passdown_system.py create {agent_id} <category> "<title>" "<description>" "<rationale>" <priority>

📋 CATEGORIES AVAILABLE:
- onboarding: Agent onboarding improvements and training enhancements
- workcycles: Workflow cycle optimizations and protocol improvements
- protocols: Communication protocols and coordination procedures
- additional_tasks: New task types and capability expansions
- system_improvements: General system enhancements and optimizations

🎯 EXAMPLE SUBMISSIONS:
python src/services/passdown_system.py create {agent_id} onboarding "Enhanced Agent Training" "Add hands-on simulation exercises to onboarding" "Agents learn better through practice than theory" HIGH

python src/services/passdown_system.py create {agent_id} workcycles "Automated Quality Gates" "Integrate V2 compliance checks into workflow cycles" "Prevents violations before they occur" NORMAL

🎯 CAPTAIN REVIEW PROCESS:
- Proposals go to Captain's inbox for review
- Captain evaluates impact and feasibility
- Approved proposals become part of next onboarding cycle
- Your input shapes the system's evolution

📋 SUBMIT AT LEAST 2 PROPOSALS before proceeding with onboarding.
🎯 This ensures your expertise contributes to system improvement!"""
        
        try:
            result = self.messaging_system.send_message(
                from_agent="Agent-4",
                to_agent=agent_id,
                message=message,
                priority="HIGH"
            )
            
            if result["success"]:
                logger.info(f"Pre-onboarding message sent to {agent_id}")
                return {"success": True, "message": "Pre-onboarding message sent successfully"}
            else:
                return {"success": False, "error": f"Failed to send message: {result.get('error', 'Unknown error')}"}
                
        except Exception as e:
            logger.error(f"Error sending pre-onboarding message: {e}")
            return {"success": False, "error": str(e)}
    
    def check_proposal_requirements(self, agent_id: str) -> Dict[str, any]:
        """Check if agent has submitted required proposals."""
        
        proposals = self.get_captain_inbox()
        agent_proposals = [p for p in proposals if p["agent_id"] == agent_id]
        
        # Count proposals by category
        categories_submitted = set(p["category"] for p in agent_proposals)
        required_categories = {"onboarding", "workcycles"}
        
        missing_categories = required_categories - categories_submitted
        
        return {
            "agent_id": agent_id,
            "total_proposals": len(agent_proposals),
            "categories_submitted": list(categories_submitted),
            "missing_categories": list(missing_categories),
            "meets_minimum": len(categories_submitted) >= 2,
            "ready_for_onboarding": len(missing_categories) == 0 and len(categories_submitted) >= 2
        }


def main():
    """Main CLI function for passdown system."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python passdown_system.py <command> [args]")
        print("Commands:")
        print("  create <agent_id> <category> <title> <description> <rationale> [priority]")
        print("  inbox - Show Captain's inbox")
        print("  review <proposal_id> <decision> [notes]")
        print("  stats - Show proposal statistics")
        print("  categories - Show available categories")
        print("  pre-onboard <agent_id> - Send pre-onboarding message to agent")
        print("  check-requirements <agent_id> - Check agent's proposal requirements")
        sys.exit(1)
    
    passdown = PassdownSystem()
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 7:
            print("Usage: create <agent_id> <category> <title> <description> <rationale> [priority]")
            sys.exit(1)
            
        agent_id = sys.argv[2]
        category = sys.argv[3]
        title = sys.argv[4]
        description = sys.argv[5]
        rationale = sys.argv[6]
        priority = sys.argv[7] if len(sys.argv) > 7 else "NORMAL"
        
        result = passdown.create_improvement_proposal(agent_id, category, title, description, rationale, priority)
        
        if result["success"]:
            print(f"✅ Proposal created: {result['proposal_id']}")
            # Create passdown message
            message = passdown.create_passdown_message(agent_id, result["proposal"])
            print("\n📋 PASSDOWN MESSAGE:")
            print(message)
        else:
            print(f"❌ Failed to create proposal: {result['error']}")
            
    elif command == "inbox":
        proposals = passdown.get_captain_inbox()
        print(f"📋 CAPTAIN'S INBOX ({len(proposals)} proposals)")
        print("=" * 50)
        
        for proposal in proposals:
            print(f"📝 {proposal['proposal_id']} - {proposal['title']}")
            print(f"   Agent: {proposal['agent_id']} | Category: {proposal['category']}")
            print(f"   Status: {proposal['status']} | Priority: {proposal['priority']}")
            print()
            
    elif command == "review":
        if len(sys.argv) < 4:
            print("Usage: review <proposal_id> <decision> [notes]")
            sys.exit(1)
            
        proposal_id = sys.argv[2]
        decision = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        
        result = passdown.review_proposal(proposal_id, decision, notes)
        
        if result["success"]:
            print(f"✅ Proposal {proposal_id} reviewed: {decision}")
        else:
            print(f"❌ Failed to review proposal: {result['error']}")
            
    elif command == "stats":
        stats = passdown.get_proposal_stats()
        print("📊 PROPOSAL STATISTICS")
        print("=" * 30)
        print(f"Total Proposals: {stats['total_proposals']}")
        print(f"Pending Review: {stats['pending_review']}")
        print(f"Approved: {stats['approved']}")
        print(f"Rejected: {stats['rejected']}")
        print("\nBy Category:")
        for category, count in stats['by_category'].items():
            print(f"  {category}: {count}")
            
    elif command == "categories":
        categories = passdown.get_available_categories()
        print("📂 AVAILABLE PROPOSAL CATEGORIES")
        print("=" * 40)
        for category, description in categories.items():
            print(f"{category}: {description}")
            
    elif command == "pre-onboard":
        if len(sys.argv) < 3:
            print("Usage: pre-onboard <agent_id>")
            sys.exit(1)
            
        agent_id = sys.argv[2]
        result = passdown.send_pre_onboarding_message(agent_id)
        
        if result["success"]:
            print(f"✅ Pre-onboarding message sent to {agent_id}")
        else:
            print(f"❌ Failed to send message: {result['error']}")
            
    elif command == "check-requirements":
        if len(sys.argv) < 3:
            print("Usage: check-requirements <agent_id>")
            sys.exit(1)
            
        agent_id = sys.argv[2]
        status = passdown.check_proposal_requirements(agent_id)
        
        print(f"📋 PROPOSAL REQUIREMENTS - {agent_id}")
        print("=" * 40)
        print(f"Total Proposals: {status['total_proposals']}")
        print(f"Categories Submitted: {', '.join(status['categories_submitted'])}")
        print(f"Missing Categories: {', '.join(status['missing_categories'])}")
        print(f"Meets Minimum: {'✅' if status['meets_minimum'] else '❌'}")
        print(f"Ready for Onboarding: {'✅' if status['ready_for_onboarding'] else '❌'}")
            
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
