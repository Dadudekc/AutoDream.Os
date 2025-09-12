#!/usr/bin/env python3
"""
Send contract availability announcement to all swarm agents.
"""

from src.services.messaging_cli_refactored import MessageCoordinator, UnifiedMessagePriority
import sys
import os

# Add project root to path
sys.path.append('.')

def send_contract_announcement():
    """Send contract availability announcement to all agents."""

    coordinator = MessageCoordinator()

    message = """🐝 CONTRACT AVAILABILITY ANNOUNCEMENT

NEW CONTRACTS AVAILABLE FOR SWARM AGENTS!

14 new contracts have been created across multiple domains:
- Security Enhancement (Agent-3)
- AI/ML Integration (Agent-5 & Agent-6)
- DevOps Automation (Agent-7)
- Advanced Monitoring (Agent-2)
- Cloud Infrastructure (Agent-2 & Agent-7)
- Data Analytics (Agent-5 & Agent-6)
- Blockchain Integration (Agent-6 & Agent-8)

Check contracts/ directory for details.
To claim: Update contract status to ASSIGNED and begin work.

🐝 WE ARE SWARM - CONTRACTS DRIVE EXCELLENCE!
"""

    agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8']
    results = {}

    print("🐝 SENDING CONTRACT ANNOUNCEMENT TO SWARM AGENTS...")
    print("=" * 60)

    for agent_id in agents:
        try:
            result = coordinator.send_to_agent(
                agent_id,
                message,
                UnifiedMessagePriority.URGENT,
                use_pyautogui=False
            )
            results[agent_id] = result
            status = "✅ SUCCESS" if result else "❌ FAILED"
            print(f"{status} - {agent_id}")
        except Exception as e:
            results[agent_id] = False
            print(f"❌ ERROR - {agent_id}: {e}")

    print("\n" + "=" * 60)
    successful = sum(1 for success in results.values() if success)
    print(f"📊 SUMMARY: {successful}/{len(agents)} agents notified successfully")

    if successful == len(agents):
        print("🎉 ALL AGENTS SUCCESSFULLY NOTIFIED!")
        print("🐝 WE ARE SWARM - CONTRACTS READY FOR EXECUTION!")
    else:
        print(f"⚠️  {len(agents) - successful} agents failed to receive notification")

    return results

if __name__ == "__main__":
    send_contract_announcement()
