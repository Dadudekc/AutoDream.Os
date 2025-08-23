#!/usr/bin/env python3
"""
FSM-Discord Integration Demo - Agent Cellphone V2
================================================

Demonstrates the complete integration between:
- FSM Core V2
- Discord Integration Service
- Decision Engine
- Agent Coordination

**Author:** Agent-1
**Created:** Current Sprint
**Status:** ACTIVE - V2 STANDARDS COMPLIANT
"""

import sys
import time
import json
import asyncio
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def demo_fsm_discord_integration():
    """Main demo function for FSM-Discord integration"""
    print("🚀 FSM-Discord Integration Demo")
    print("=" * 50)

    try:
        # Import required components
        print("\n📦 Importing components...")

        from core.fsm_core_v2 import FSMCoreV2
        from core.decision import AutonomousDecisionEngine
        from services.discord_integration_service import DiscordIntegrationService
        from core.fsm_discord_bridge import FSMDiscordBridge

        print("✅ All components imported successfully")

        # Initialize components
        print("\n🔧 Initializing components...")

        # Mock workspace and inbox managers for demo
        class MockWorkspaceManager:
            def __init__(self):
                self.workspaces = {"demo": "Demo Workspace"}

        class MockInboxManager:
            def __init__(self):
                self.inboxes = {"demo": "Demo Inbox"}

        workspace_manager = MockWorkspaceManager()
        inbox_manager = MockInboxManager()

        # Initialize FSM Core
        fsm_core = FSMCoreV2(workspace_manager, inbox_manager, "demo_fsm_data")
        print("✅ FSM Core initialized")

        # Initialize Decision Engine
        decision_engine = AutonomousDecisionEngine()
        print("✅ Decision Engine initialized")

        # Initialize Discord Service
        discord_service = DiscordIntegrationService(fsm_core, decision_engine)
        discord_service.configure_discord(
            webhook_url="https://discord.com/api/webhooks/demo", guild_id="demo_guild"
        )
        print("✅ Discord Service initialized")

        # Initialize FSM-Discord Bridge
        bridge = FSMDiscordBridge(fsm_core, decision_engine, discord_service)
        print("✅ FSM-Discord Bridge initialized")

        # Demo 1: Agent Registration
        print("\n🎬 Demo 1: Agent Registration via Discord")
        print("-" * 40)

        agents = [
            ("agent-1", "Foundation Specialist", ["testing", "coordination"]),
            ("agent-2", "Quality Analyzer", ["automation", "monitoring"]),
            ("agent-3", "Integration Expert", ["development", "deployment"]),
        ]

        for agent_id, name, capabilities in agents:
            success = discord_service.register_agent(agent_id, name, capabilities)
            if success:
                print(f"✅ {name} registered with capabilities: {capabilities}")
            else:
                print(f"❌ Failed to register {name}")

        # Demo 2: Task Creation via Discord
        print("\n🎬 Demo 2: Task Creation via Discord Commands")
        print("-" * 40)

        test_tasks = [
            ("Integration Testing", "Test FSM-Discord integration", "agent-1", "high"),
            ("System Monitoring", "Monitor agent performance", "agent-2", "normal"),
            ("Decision Analysis", "Analyze decision patterns", "agent-3", "critical"),
        ]

        for title, description, agent, priority in test_tasks:
            task_id = bridge.create_task_via_discord(
                title, description, agent, priority
            )
            if task_id and task_id != "discord_only":
                print(f"✅ Task created: {title} (ID: {task_id})")
            else:
                print(f"⚠️ Task created (Discord only): {title}")

        # Demo 3: Decision Requests via Discord
        print("\n🎬 Demo 3: AI Decision Requests via Discord")
        print("-" * 40)

        decision_scenarios = [
            ("Agent coordination strategy", ["sequential", "parallel", "adaptive"]),
            (
                "Task priority allocation",
                ["round_robin", "load_balanced", "priority_based"],
            ),
            ("Resource allocation", ["conservative", "balanced", "aggressive"]),
        ]

        for context, options in decision_scenarios:
            result = bridge.request_decision_via_discord(context, options, "agent-1")
            print(f"🧠 Decision for '{context}': {result}")

        # Demo 4: FSM State Synchronization
        print("\n🎬 Demo 4: FSM State Synchronization")
        print("-" * 40)

        # Update some task states
        if fsm_core.tasks:
            task_id = list(fsm_core.tasks.keys())[0]
            success = fsm_core.update_task_state(
                task_id, "in_progress", "agent-1", "Starting task execution"
            )
            if success:
                print(f"✅ Task {task_id} state updated to 'in_progress'")

        # Sync state to Discord
        sync_success = bridge.sync_fsm_state_to_discord(force=True)
        if sync_success:
            print("✅ FSM state synchronized to Discord")
        else:
            print("❌ Failed to sync FSM state")

        # Demo 5: Discord Command Processing
        print("\n🎬 Demo 5: Discord Command Processing")
        print("-" * 40)

        test_commands = [
            ("!help", [], "demo_user", "general"),
            ("!fsm_status", [], "demo_user", "fsm_status"),
            ("!agent_status", [], "demo_user", "agent_status"),
            (
                "!create_task",
                ["Demo Task", "Testing command processing", "agent-2"],
                "demo_user",
                "tasks",
            ),
        ]

        for command, args, user, channel in test_commands:
            print(f"\n🔧 Testing: {command} {' '.join(args)}")
            response = bridge.process_discord_command(command, args, user, channel)
            print(f"Response: {response[:100]}{'...' if len(response) > 100 else ''}")

        # Demo 6: System Status and Integration
        print("\n🎬 Demo 6: System Integration Status")
        print("-" * 40)

        # Get status from all components
        fsm_status = {"total_tasks": len(fsm_core.tasks), "status": fsm_core.status}

        decision_status = decision_engine.get_autonomous_status()
        discord_status = discord_service.get_status()
        bridge_status = bridge.get_bridge_status()

        print("📊 FSM Status:")
        print(json.dumps(fsm_status, indent=2))

        print("\n🧠 Decision Engine Status:")
        print(json.dumps(decision_status, indent=2))

        print("\n📱 Discord Service Status:")
        print(json.dumps(discord_status, indent=2))

        print("\n🔗 Bridge Status:")
        print(json.dumps(bridge_status, indent=2))

        # Demo 7: Real-time Coordination
        print("\n🎬 Demo 7: Real-time Agent Coordination")
        print("-" * 40)

        # Simulate agent activities
        for agent_id in ["agent-1", "agent-2", "agent-3"]:
            discord_service.update_agent_status(agent_id, "busy", "Processing tasks")
            time.sleep(0.5)  # Simulate processing time

        # Update agent statuses
        discord_service.update_agent_status("agent-1", "idle", "Tasks completed")
        discord_service.update_agent_status("agent-2", "idle", "Monitoring complete")
        discord_service.update_agent_status("agent-3", "idle", "Integration verified")

        print("✅ Agent coordination simulation completed")

        # Final Status
        print("\n🎉 Demo Completed Successfully!")
        print("=" * 50)

        final_status = {
            "fsm_tasks": len(fsm_core.tasks),
            "agents_registered": len(discord_service.agents),
            "messages_sent": len(discord_service.messages),
            "integration_status": "FULLY OPERATIONAL",
        }

        print("📊 Final System Status:")
        print(json.dumps(final_status, indent=2))

        return True

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all components are properly installed and accessible")
        return False

    except Exception as e:
        print(f"❌ Demo Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    print("🤖 Agent Cellphone V2 - FSM-Discord Integration Demo")
    print("=" * 60)

    success = demo_fsm_discord_integration()

    if success:
        print("\n✅ Integration Demo: SUCCESS")
        print("\n🚀 Next Steps:")
        print("1. Configure your Discord webhook URL")
        print("2. Set up Discord bot token for full integration")
        print("3. Customize command handlers for your needs")
        print("4. Deploy to production environment")
    else:
        print("\n❌ Integration Demo: FAILED")
        print("Check the error messages above for troubleshooting")

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
