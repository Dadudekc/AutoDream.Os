#!/usr/bin/env python3
"""
V3 Autonomous Cycle Tool
Advanced self-prompting agent coordination with continuous operation protocols
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from services.v3_autonomous_workflow_system import V3AutonomousWorkflowSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_v3_cycle(agent_id: str, cycles: int = 1, continuous: bool = False):
    """Run V3 autonomous cycle for agent"""
    print(f"🚀 Starting V3 autonomous cycle for {agent_id}")
    print(f"🔄 Mode: {'continuous' if continuous else f'{cycles} cycle(s)'}")

    v3_system = V3AutonomousWorkflowSystem()

    try:
        await v3_system.initialize()

        if continuous:
            cycle_count = 0
            while True:
                cycle_count += 1
                print(f"\n🤖 V3 Cycle {cycle_count} starting...")

                results = await v3_system.run_autonomous_cycle(agent_id)

                print(f"✅ V3 Cycle {cycle_count} completed")
                print(f"📊 Actions: {len(results.get('actions_taken', []))}")
                print(f"📨 Messages: {results.get('messages_sent', 0)}")
                print(f"🎯 Tasks: {results.get('tasks_processed', 0)}")
                print(f"📝 Devlogs: {results.get('devlogs_created', 0)}")

                if results.get("error"):
                    print(f"❌ Error: {results['error']}")

                # Wait before next cycle
                await asyncio.sleep(5)
        else:
            for cycle in range(1, cycles + 1):
                print(f"\n🤖 V3 Cycle {cycle}/{cycles} starting...")

                results = await v3_system.run_autonomous_cycle(agent_id)

                print(f"✅ V3 Cycle {cycle}/{cycles} completed")
                print(f"📊 Actions: {len(results.get('actions_taken', []))}")
                print(f"📨 Messages: {results.get('messages_sent', 0)}")
                print(f"🎯 Tasks: {results.get('tasks_processed', 0)}")
                print(f"📝 Devlogs: {results.get('devlogs_created', 0)}")

                if results.get("error"):
                    print(f"❌ Error: {results['error']}")

                if cycle < cycles:
                    await asyncio.sleep(2)

        # Get system status
        status = await v3_system.get_system_status()
        print("\n🌟 V3 System Status:")
        print(f"📊 Total Agents: {status['total_agents']}")
        print(f"🔄 Active Agents: {status['active_agents']}")
        print(f"📋 Total Tasks: {status['total_tasks']}")

    except Exception as e:
        logger.error(f"Error running V3 cycle: {e}")
        print(f"❌ Error: {e}")
    finally:
        await v3_system.close()


async def get_v3_status():
    """Get V3 system status"""
    print("📊 Getting V3 system status...")

    v3_system = V3AutonomousWorkflowSystem()

    try:
        await v3_system.initialize()
        status = await v3_system.get_system_status()

        print("\n🌟 V3 Autonomous Workflow System Status:")
        print(f"📊 System Version: {status['system_version']}")
        print(f"🤖 Total Agents: {status['total_agents']}")
        print(f"🔄 Active Agents: {status['active_agents']}")
        print(f"📋 Total Tasks: {status['total_tasks']}")

        print("\n📈 System Metrics:")
        for metric, value in status["system_metrics"].items():
            print(f"  {metric}: {value}")

        print("\n🤖 Agent Status:")
        for agent_id, agent_status in status["agent_status"].items():
            print(f"  {agent_id}:")
            print(f"    Current Task: {agent_status['current_task'] or 'None'}")
            print(f"    Performance: {agent_status['performance']}")
            print(f"    Last Active: {agent_status['last_active'] or 'Never'}")

    except Exception as e:
        logger.error(f"Error getting V3 status: {e}")
        print(f"❌ Error: {e}")
    finally:
        await v3_system.close()


def main():
    parser = argparse.ArgumentParser(description="V3 Autonomous Cycle Tool")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-1)")
    parser.add_argument("--cycles", type=int, default=1, help="Number of cycles to run")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--status", action="store_true", help="Get V3 system status")

    args = parser.parse_args()

    if args.status:
        asyncio.run(get_v3_status())
    else:
        asyncio.run(run_v3_cycle(args.agent, args.cycles, args.continuous))


if __name__ == "__main__":
    main()
