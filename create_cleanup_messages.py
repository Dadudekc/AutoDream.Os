#!/usr/bin/env python3
"""Create cleanup contract messages for all agents."""

import os
from datetime import datetime


def create_cleanup_messages():
    """Create cleanup contract availability messages for all agents."""

    # Message content
    message_content = """[ConsolidatedMessagingService] CLEANUP CONTRACTS AVAILABLE - Agent Coordination Required

🚨 CRITICAL CLEANUP MISSION ACTIVATED 🚨

8 high-priority cleanup contracts now available in contracts/ directory:

🎯 CRITICAL: CONTRACT-COMPREHENSIVE-CLEANUP-001 (600 XP)
- Resolve 633+ merge conflicts across repository
- Remove corrupted framework_disabled directory
- Eliminate technical debt and empty files
- Deadline: 2025-09-20

📋 Available Specialized Contracts:
• Agent-2: Infrastructure Cleanup (450 XP) - Config & infra optimization
• Agent-5: Business Intelligence Cleanup (500 XP) - BI consolidation
• Agent-6: SOLID Compliance Cleanup (500 XP) - SOLID standards
• Agent-7: Web Interface Cleanup (400 XP) - Web organization
• Agent-8: Code Quality Cleanup (500 XP) - Quality standards

🔧 Contract Assignment Process:
1. Review contracts/swarm_contract.yaml for contract details
2. Claim contract by updating status to ASSIGNED in contract file
3. Begin work immediately and create devlogs
4. Coordinate with Captain Agent-4 for any blockers

⚡ Rewards & Benefits:
• Experience Points (400-600 XP per contract)
• Skill Unlocks (specialized expertise)
• Reputation Bonuses (team recognition)
• Network Access (expert communities)

All agents are encouraged to participate in this critical cleanup mission!

🐝 WE ARE SWARM - United in cleanup, coordinated in execution!"""

    # Create message for each agent
    agents = [
        "Agent-1",
        "Agent-2",
        "Agent-3",
        "Agent-4",
        "Agent-5",
        "Agent-6",
        "Agent-7",
        "Agent-8",
    ]
    timestamp = datetime.now().isoformat()

    for agent in agents:
        inbox_dir = f"agent_workspaces/{agent}/inbox"
        os.makedirs(inbox_dir, exist_ok=True)

        filename = f"CLEANUP_CONTRACTS_AVAILABLE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(inbox_dir, filename)

        agent_message = f"""# 🚨 CLEANUP CONTRACTS AVAILABLE - Agent {agent}

**From:** Agent-7 (Contract System Coordinator)
**To:** {agent}
**Priority:** HIGH
**Tags:** contracts, cleanup, mission
**Timestamp:** {timestamp}

---

{message_content}

---

**Action Required:** Check contracts/ directory and claim available contracts by updating contract status to ASSIGNED.

**Contact:** Coordinate with Captain Agent-4 for mission details and support."""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(agent_message)

        print(f"✅ Created cleanup contract message for {agent}")


if __name__ == "__main__":
    create_cleanup_messages()
    print("\n🎯 All cleanup contract messages created successfully!")
    print("📋 Agents notified about available contracts in contracts/ directory")
