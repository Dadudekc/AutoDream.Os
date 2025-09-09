#!/usr/bin/env python3
"""
Survey Team Onboarding Sequence
==============================

Automated onboarding of specialized survey coordination agents
using the corrected messaging CLI system.
"""

import subprocess
import time
import sys
from pathlib import Path

def onboard_survey_agent(agent_name: str, role: str, specialty: str):
    """Onboard a single survey agent using messaging CLI."""

    print(f"🚀 Onboarding {agent_name} ({role}) - {specialty}")

    # Build the onboarding command
    cmd = [
        sys.executable, "-m", "src.services.messaging_cli",
        "--hard-onboarding",
        "--agent-subset", agent_name,
        "--yes",
        "--dry-run",
        "--assign-roles", f"{agent_name}:{role}"
    ]

    try:
        # Execute the onboarding command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(f"✅ SUCCESS: {agent_name} onboarded successfully")
            return True
        else:
            print(f"❌ FAILED: {agent_name} onboarding failed")
            print(f"   Return code: {result.returncode}")
            print(f"   Stderr: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {agent_name} onboarding timed out")
        return False
    except Exception as e:
        print(f"💥 ERROR: {agent_name} onboarding error: {e}")
        return False

def main():
    """Execute complete survey team onboarding sequence."""

    print("🐝 SURVEY TEAM ONBOARDING SEQUENCE INITIATED")
    print("=" * 60)

    # Define survey coordination team
    survey_team = [
        {
            "name": "Agent-SRC-1",
            "role": "SOLID",
            "specialty": "Survey Response Coordinator"
        },
        {
            "name": "Agent-SQA-2",
            "role": "TDD",
            "specialty": "Survey Quality Assurance"
        },
        {
            "name": "Agent-SDA-3",
            "role": "SSOT",
            "specialty": "Survey Data Analysis"
        },
        {
            "name": "Agent-SRC-4",
            "role": "SOLID",
            "specialty": "Survey Report Compilation"
        },
        {
            "name": "Agent-SRA-5",
            "role": "DRY",
            "specialty": "Survey Risk Assessment"
        },
        {
            "name": "Agent-STM-6",
            "role": "KISS",
            "specialty": "Survey Timeline Management"
        }
    ]

    successful_onboardings = 0
    total_agents = len(survey_team)

    print(f"📋 Onboarding {total_agents} specialized survey coordination agents...")
    print()

    for i, agent in enumerate(survey_team, 1):
        print(f"[{i}/{total_agents}] ", end="")

        success = onboard_survey_agent(
            agent["name"],
            agent["role"],
            agent["specialty"]
        )

        if success:
            successful_onboardings += 1

        # Small delay between onboardings
        time.sleep(1)

    print()
    print("=" * 60)
    print("📊 ONBOARDING SEQUENCE RESULTS")
    print("=" * 60)
    print(f"✅ Successful onboardings: {successful_onboardings}/{total_agents}")
    print(f"❌ Failed onboardings: {total_agents - successful_onboardings}")

    if successful_onboardings == total_agents:
        print("🎉 ALL AGENTS SUCCESSFULLY ONBOARDED!")
        print("🐝 Survey coordination team is now fully operational!")
    else:
        print(f"⚠️  {total_agents - successful_onboardings} agents failed onboarding")
        print("🔧 Manual intervention may be required for failed onboardings")

    print()
    print("📋 FINAL SURVEY COORDINATION TEAM STATUS:")
    for agent in survey_team:
        status = "✅ ACTIVE" if successful_onboardings == total_agents else "⏳ PENDING"
        print(f"   {status} {agent['name']} ({agent['role']}) - {agent['specialty']}")

    print()
    print("🚀 NEXT STEPS:")
    print("   1. Verify agent workspaces were created correctly")
    print("   2. Test inter-agent communication channels")
    print("   3. Activate survey coordination workflow")
    print("   4. Begin Discord devlog monitoring")

    return successful_onboardings == total_agents

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
