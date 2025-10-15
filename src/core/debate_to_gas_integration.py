#!/usr/bin/env python3
"""
Debate → Swarm Brain → Gasline Integration
Connects democratic decisions to automatic execution

When debate concludes → Decision stored → Agents activated → Work happens
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class DebateToGasIntegration:
    """Integrates debate outcomes with gasline delivery for automatic execution"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.proposals_dir = self.project_root / "swarm_proposals"
        self.brain_dir = self.project_root / "swarm_brain"
    
    def process_debate_decision(
        self, 
        topic: str, 
        decision: str, 
        execution_plan: Dict,
        agent_assignments: Dict[str, str]
    ) -> bool:
        """
        Process debate decision and activate agents
        
        Args:
            topic: Debate topic (e.g., 'orientation_system')
            decision: Final decision (e.g., 'Integration approach')
            execution_plan: What needs to be done
            agent_assignments: Which agent does what
            
        Returns:
            True if successful
        """
        try:
            # Step 1: Store in Swarm Brain
            self._store_in_swarm_brain(topic, decision, execution_plan)
            
            # Step 2: Generate activation messages
            messages = self._generate_activation_messages(
                topic, decision, execution_plan, agent_assignments
            )
            
            # Step 3: Deliver via gasline
            self._deliver_via_gasline(messages)
            
            # Step 4: Create execution tracking
            self._create_execution_tracker(topic, agent_assignments)
            
            logger.info(f"✅ Debate decision '{decision}' activated via gasline")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to process debate decision: {e}")
            return False
    
    def _store_in_swarm_brain(
        self, topic: str, decision: str, execution_plan: Dict
    ):
        """Store decision in swarm brain for collective knowledge"""
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "decision": decision,
            "execution_plan": execution_plan,
            "status": "activated"
        }
        
        # Store as knowledge entry
        decisions_file = self.brain_dir / "decisions" / f"{topic}_decision.json"
        decisions_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(decisions_file, 'w') as f:
            json.dump(decision_record, f, indent=2)
        
        logger.info(f"📚 Stored decision in Swarm Brain: {decisions_file}")
    
    def _generate_activation_messages(
        self,
        topic: str,
        decision: str, 
        execution_plan: Dict,
        agent_assignments: Dict[str, str]
    ) -> List[Dict]:
        """Generate activation messages for assigned agents"""
        messages = []
        
        for agent_id, task in agent_assignments.items():
            message = f"""🎯 DEBATE DECISION → ACTION!

Topic: {topic}
Decision: {decision}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR ASSIGNMENT ({agent_id}):
{task}

CONTEXT (From Swarm Brain):
- Collective decision: {decision}
- Your part: {task}
- Coordination: Check swarm_brain/decisions/{topic}_decision.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTION STEPS:
1. Review decision: cat swarm_brain/decisions/{topic}_decision.json
2. Check your inbox: agent_workspaces/{agent_id}/inbox/
3. Execute your part: {task}
4. Report completion: Update status.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐝 SWARM DECISION → IMMEDIATE ACTION!

BEGIN NOW!
"""
            
            messages.append({
                "agent_id": agent_id,
                "message": message,
                "priority": "urgent"
            })
        
        return messages
    
    def _deliver_via_gasline(self, messages: List[Dict]):
        """Deliver activation messages via gasline (PyAutoGUI)"""
        try:
            from src.services.messaging_cli_handlers import send_message_to_agent
            
            for msg in messages:
                send_message_to_agent(
                    agent_id=msg["agent_id"],
                    message=msg["message"],
                    sender="Swarm Brain (Debate Decision)",
                    priority=msg.get("priority", "urgent"),
                    use_pyautogui=True
                )
                logger.info(f"⚡ GAS delivered to {msg['agent_id']}")
                
        except ImportError:
            logger.warning("⚠️ Messaging CLI not available, creating inbox files")
            # Fallback: Create inbox files
            for msg in messages:
                inbox_dir = self.project_root / "agent_workspaces" / msg["agent_id"] / "inbox"
                inbox_dir.mkdir(parents=True, exist_ok=True)
                
                msg_file = inbox_dir / f"DEBATE_DECISION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(msg_file, 'w') as f:
                    f.write(msg["message"])
                
                logger.info(f"📥 Inbox message created for {msg['agent_id']}")
    
    def _create_execution_tracker(self, topic: str, agent_assignments: Dict):
        """Create execution tracking file"""
        tracker = {
            "topic": topic,
            "started": datetime.now().isoformat(),
            "agents": {
                agent_id: {
                    "task": task,
                    "status": "assigned",
                    "started": None,
                    "completed": None
                }
                for agent_id, task in agent_assignments.items()
            }
        }
        
        tracker_file = self.project_root / "workflow_states" / f"{topic}_execution.json"
        tracker_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(tracker_file, 'w') as f:
            json.dump(tracker, f, indent=2)
        
        logger.info(f"📊 Execution tracker created: {tracker_file}")


def activate_debate_decision(
    topic: str,
    decision: str,
    execution_plan: Dict,
    agent_assignments: Dict[str, str]
) -> bool:
    """
    Quick function to activate a debate decision
    
    Example:
        activate_debate_decision(
            topic="orientation_system",
            decision="Integration approach combining all 8 proposals",
            execution_plan={
                "phase_1": "Build orientation CLI tool",
                "phase_2": "Create single-page reference",
                "phase_3": "Integrate with gasline"
            },
            agent_assignments={
                "Agent-7": "Build tools/agent_orient.py CLI tool",
                "Agent-2": "Create docs/AGENT_ORIENTATION.md reference",
                "Agent-4": "Integrate with onboarding service"
            }
        )
    """
    integrator = DebateToGasIntegration()
    return integrator.process_debate_decision(
        topic, decision, execution_plan, agent_assignments
    )


if __name__ == "__main__":
    # Example: Activate orientation system decision
    result = activate_debate_decision(
        topic="orientation_system",
        decision="Integration approach - combine Agent-7's enhance existing + Agent-3's CLI + Agent-2's single-page",
        execution_plan={
            "immediate": "Build working orientation tool",
            "phase_1": "CLI tool for discovery",
            "phase_2": "Single-page reference guide",
            "phase_3": "GAS integration"
        },
        agent_assignments={
            "Agent-7": "Build tools/agent_orient.py - enhance existing tools approach",
            "Agent-2": "Create docs/AGENT_ORIENTATION.md - single-page reference",
            "Agent-4": "Integrate orientation into onboarding/gasline"
        }
    )
    
    if result:
        print("✅ Debate decision activated - agents receiving GAS now!")
    else:
        print("❌ Activation failed")

