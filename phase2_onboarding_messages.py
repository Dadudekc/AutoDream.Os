#!/usr/bin/env python3
"""
Phase 2 Consolidation Onboarding Messages - V2 Compliant Module
==============================================================

Generates Phase 2 consolidation onboarding messages for all 8 agents
with specific chunk assignments and reduction targets.

Author: Captain Agent-4 (QA & Coordination)
License: MIT
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import pyautogui as pg
except ImportError:
    pg = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

logger = logging.getLogger(__name__)


class Phase2OnboardingMessages:
    """Generates Phase 2 consolidation onboarding messages for all agents."""

    def __init__(self):
        """Initialize Phase 2 onboarding message generator."""
        self.agent_assignments = {
            "Agent-1": {
                "role": "Integration & Core Systems Specialist",
                "chunk": "Chunk 002 (Services)",
                "target": "50 → 20 files (60% reduction)",
                "focus": "PyAutoGUI Service Consolidation, Handler Framework, Vector Database Service"
            },
            "Agent-2": {
                "role": "Architecture & Design Specialist",
                "chunk": "Chunk 001 (Core)",
                "target": "50 → 15 files (70% reduction)",
                "focus": "Messaging System Consolidation, Analytics Engine, Configuration System"
            },
            "Agent-3": {
                "role": "Infrastructure & DevOps Specialist",
                "chunk": "Chunk 004-005 (Utils/Infrastructure)",
                "target": "31 → 13 files (58% reduction)",
                "focus": "Config Utilities, File Utilities, Browser Modules, Persistence Layer"
            },
            "Agent-4": {
                "role": "Quality Assurance Specialist (CAPTAIN)",
                "chunk": "Chunk 006-007 (Domain)",
                "target": "40 → 20 files (50% reduction)",
                "focus": "Gaming Module Consolidation, Trading Robot Consolidation, Quality Validation"
            },
            "Agent-5": {
                "role": "Business Intelligence Specialist",
                "chunk": "Support & Analysis",
                "target": "Data analysis and reporting",
                "focus": "Consolidation metrics, progress tracking, business impact analysis"
            },
            "Agent-6": {
                "role": "Coordination & Communication Specialist",
                "chunk": "Chunk 008-013 (Docs/Tools)",
                "target": "95 → 35 files (63% reduction)",
                "focus": "Documentation Consolidation, Scripts & Tools Consolidation, Communication Protocols"
            },
            "Agent-7": {
                "role": "Web Development Specialist",
                "chunk": "Chunk 003 (Web)",
                "target": "50 → 30 files (40% reduction)",
                "focus": "JavaScript Module Consolidation, CSS Consolidation, Dashboard Components"
            },
            "Agent-8": {
                "role": "Operations & Support Specialist",
                "chunk": "Support & Monitoring",
                "target": "System monitoring and support",
                "focus": "Deployment monitoring, error tracking, system health validation"
            }
        }

    def generate_phase2_message(self, agent_id: str) -> str:
        """Generate Phase 2 consolidation onboarding message for specific agent."""
        assignment = self.agent_assignments.get(agent_id, {})
        role = assignment.get("role", "Specialist")
        chunk = assignment.get("chunk", "General Support")
        target = assignment.get("target", "TBD")
        focus = assignment.get("focus", "General consolidation support")

        return f"""
🚀 **PHASE 2 CONSOLIDATION ONBOARDING - {agent_id.upper()}**

**Agent Identity:** {agent_id} - {role}
**Phase:** Phase 2 - Consolidation Execution
**Activation Time:** {datetime.now().isoformat()}
**Status:** ACTIVE - READY FOR CONSOLIDATION ASSIGNMENT

🎯 **YOUR CONSOLIDATION ASSIGNMENT:**

**Chunk Assignment:** {chunk}
**Reduction Target:** {target}
**Focus Areas:** {focus}

📋 **PHASE 2 CONSOLIDATION OBJECTIVES:**

**Primary Mission:**
- Execute systematic file consolidation according to assigned chunk
- Achieve target reduction percentages while maintaining functionality
- Maintain V2 compliance standards throughout consolidation
- Coordinate with other agents for parallel execution

**Consolidation Principles:**
- SOLID Compliance - Single responsibility, open-closed, etc.
- DRY Principle - Don't repeat yourself
- KISS Principle - Keep it simple, stupid
- YAGNI Principle - You aren't gonna need it
- Separation of Concerns - Clear module boundaries

**Quality Gates:**
- All tests passing - No regressions
- Documentation updated - Real-time updates
- Code review - Peer validation
- Performance validation - No degradation
- Integration testing - End-to-end validation

🔧 **CONSOLIDATION WORKFLOW:**

**Step 1: Analysis**
- Analyze assigned chunk files
- Identify consolidation opportunities
- Map dependencies and relationships
- Plan consolidation approach

**Step 2: Implementation**
- Execute consolidation according to plan
- Maintain functionality throughout process
- Update imports and references
- Test changes incrementally

**Step 3: Validation**
- Run comprehensive tests
- Validate performance metrics
- Update documentation
- Coordinate with other agents

**Step 4: Integration**
- Merge changes with other agents
- Resolve conflicts and dependencies
- Final validation and testing
- Deploy consolidated system

📊 **SUCCESS METRICS:**

**Quantitative Targets:**
- File reduction: {target}
- Code quality: Maintain or improve
- Test coverage: 100% maintained
- Performance: No degradation

**Qualitative Goals:**
- Improved maintainability
- Enhanced code organization
- Reduced complexity
- Better documentation

🤝 **CROSS-AGENT COORDINATION:**

**Daily Coordination:**
- Progress updates every 4 hours
- Blocking issue escalation
- Cross-agent dependency resolution
- Quality validation checkpoints

**Communication Protocols:**
- Use PyAutoGUI messaging for real-time coordination
- Maintain status updates in agent_coordination/
- Escalate issues immediately to Captain Agent-4
- Coordinate with assigned agent pairs

🎯 **IMMEDIATE ACTIONS:**

1. **Review Assignment:** Understand your chunk and target
2. **Plan Approach:** Create consolidation strategy
3. **Coordinate:** Check in with other agents
4. **Begin Execution:** Start with analysis phase
5. **Report Progress:** Update status regularly

🐝 **WE ARE SWARM - CONSOLIDATION EXECUTION BEGINS!**

**Phase 2 Status:** ✅ **ACTIVE - CONSOLIDATION EXECUTION READY**
**Agent Assignment:** ✅ **{chunk} - {target}**
**Cross-Agent Coordination:** ✅ **PROTOCOLS ACTIVE - SWARM COLLABORATION OPERATIONAL**

**🎉 WELCOME TO PHASE 2 - LET'S ACHIEVE THOSE CONSOLIDATION TARGETS!**

Best regards,
Captain Agent-4 (QA & Coordination)

⚡ **WE. ARE. SWARM. ⚡️🔥**
"""

    def send_phase2_messages_to_all_agents(self) -> dict[str, Any]:
        """Send Phase 2 onboarding messages to all 8 agents."""
        logger.info("🚀 Sending Phase 2 consolidation onboarding messages to all agents")

        results = []
        for agent_id in self.agent_assignments.keys():
            try:
                message = self.generate_phase2_message(agent_id)
                success = self._send_message_to_agent(agent_id, message)

                results.append({
                    "agent_id": agent_id,
                    "success": success,
                    "chunk": self.agent_assignments[agent_id]["chunk"],
                    "target": self.agent_assignments[agent_id]["target"],
                    "timestamp": datetime.now().isoformat()
                })

                if success:
                    logger.info(f"✅ Phase 2 message sent to {agent_id}")
                else:
                    logger.error(f"❌ Failed to send Phase 2 message to {agent_id}")

            except Exception as e:
                logger.error(f"❌ Error sending message to {agent_id}: {e}")
                results.append({
                    "agent_id": agent_id,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })

        successful = sum(1 for r in results if r.get("success", False))
        total = len(results)

        logger.info(f"📊 Phase 2 onboarding complete: {successful}/{total} agents notified")

        return {
            "success": successful > 0,
            "total_agents": total,
            "successful_deliveries": successful,
            "success_rate": (successful/total)*100,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }

    def _send_message_to_agent(self, agent_id: str, message: str) -> bool:
        """Send message to specific agent via UI automation using proper onboarding sequence."""
        if not pg:
            logger.warning("PyAutoGUI not available - simulating message delivery")
            return True

        try:
            # Load coordinates
            coord_file = Path("cursor_agent_coords.json")
            if not coord_file.exists():
                logger.error("Coordinate file not found")
                return False

            coords_data = json.loads(coord_file.read_text(encoding="utf-8"))
            agent_coords = coords_data.get("agents", {}).get(agent_id, {})
            onboarding_coords = agent_coords.get("onboarding_input_coords", [0, 0])

            if onboarding_coords == [0, 0]:
                logger.warning(f"No onboarding coordinates found for {agent_id}")
                return False

            # Focus agent window
            self._focus_agent_window(agent_id)
            time.sleep(0.2)

            # Open new tab with Ctrl+N for onboarding
            pg.hotkey("ctrl", "n")
            time.sleep(0.3)

            # Click on onboarding input coordinates
            pg.click(onboarding_coords[0], onboarding_coords[1])
            time.sleep(0.1)

            # Clear existing content
            pg.hotkey("ctrl", "a")
            pg.typewrite(["backspace"])
            time.sleep(0.1)

            # Use clipboard for better message delivery
            import pyperclip
            pyperclip.copy(message)
            pg.hotkey("ctrl", "v")
            time.sleep(0.2)

            # Send the message
            pg.press("enter")
            time.sleep(0.1)

            return True

        except Exception as e:
            logger.error(f"Failed to send onboarding message to {agent_id}: {e}")
            return False

    def _focus_agent_window(self, agent_id: str):
        """Focus the agent window."""
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(agent_id)
            if windows:
                windows[0].activate()
            else:
                pg.hotkey("alt", "tab")
        except Exception:
            pg.hotkey("alt", "tab")
        time.sleep(0.1)

    def generate_consolidation_summary(self) -> str:
        """Generate consolidation assignment summary for all agents."""
        summary = """
🎯 **PHASE 2 CONSOLIDATION ASSIGNMENTS - SWARM COORDINATION**

**Consolidation Targets by Agent:**

"""

        for agent_id, assignment in self.agent_assignments.items():
            summary += f"""
**{agent_id}** - {assignment['role']}
- Chunk: {assignment['chunk']}
- Target: {assignment['target']}
- Focus: {assignment['focus']}
"""

        summary += """

**Overall Consolidation Goals:**
- Total Files: 1,421 → ~400-500 files (65-70% reduction)
- Phase 1 Target: 100 → 35 files (65% reduction)
- Phase 2 Target: 31 → 13 files (58% reduction)
- Phase 3 Target: 90 → 50 files (44% reduction)
- Phase 4 Target: 95 → 35 files (63% reduction)

**Quality Standards:**
- V2 Compliance: All files under 500 lines
- Test Coverage: 100% maintained
- Performance: No degradation
- Documentation: Real-time updates

🐝 **WE ARE SWARM - CONSOLIDATION EXECUTION READY!**
"""

        return summary


def main():
    """Main function for Phase 2 onboarding message delivery."""
    onboarding = Phase2OnboardingMessages()

    # Generate and send messages to all agents
    result = onboarding.send_phase2_messages_to_all_agents()
    print(f"Phase 2 onboarding result: {result}")

    # Generate consolidation summary
    summary = onboarding.generate_consolidation_summary()
    print(summary)


if __name__ == "__main__":
    main()
