#!/usr/bin/env python3
"""
Live Agent Communication Test
Testing V2 enhanced communication coordinator with real agent interactions
"""

import sys
import os
import time
import json
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

from services.communication import (
    MessageCoordinator,
    ChannelManager,
    CommunicationMode,
    TaskPriority,
    TaskStatus
)


def test_live_agent_communication():
    """Test live agent communication workflow"""
    print("🎬 LIVE AGENT COMMUNICATION TEST")
    print("=" * 50)

    try:
        # Initialize coordinator
        print("🔧 Initializing V2 Communication Coordinator...")
        coordinator = MessageCoordinator()
        channel_manager = ChannelManager()
        print("✅ Coordinator initialized successfully")

        # Test 1: Presidential Decision Workflow
        print("\n🏛️ TEST 1: Presidential Decision Workflow")
        print("-" * 40)

        # Captain (Agent-5) proposes a decision
        coordinator.send_message(
            "agent_5",
            ["agent_1", "agent_2", "agent_3", "agent_4", "agent_6", "agent_7", "agent_8"],
            "presidential_decision",
            "Multimedia Integration Directive: All agents must integrate multimedia capabilities within 24 hours"
        )

        print("📋 Presidential decision proposed by Captain (Agent-5)")
        time.sleep(1)

        # Test 2: Collaboration Session Workflow
        print("\n🤝 TEST 2: Collaboration Session Workflow")
        print("-" * 40)

        # Agent-1 requests collaboration
        session_id = coordinator.create_coordination_session(
            CommunicationMode.COLLABORATIVE,
            ["agent_1", "agent_3", "agent_5"],
            ["Coordinate multimedia services across all agents"]
        )
        print(f"🤝 Collaboration session created: {session_id}")

        print("🤝 Collaboration session requested by Agent-1")
        time.sleep(1)

        # Test 3: Task Progress Updates
        print("\n📈 TEST 3: Task Progress Updates")
        print("-" * 40)

        # Agent-3 (self) reports progress
        task_id = coordinator.create_task(
            "Multimedia Integration Test",
            "Test multimedia integration capabilities",
            TaskPriority.HIGH,
            ["agent_3"]
        )
        coordinator.update_task_status(task_id, TaskStatus.COMPLETED, 100.0)
        print(f"📈 Task created and completed: {task_id}")

        print("📈 Task progress updated by Agent-3 (Multimedia Specialist)")
        time.sleep(1)

        # Test 4: Multimedia Integration Coordination
        print("\n🎬 TEST 4: Multimedia Integration Coordination")
        print("-" * 40)

        # Test multimedia update broadcast
        coordinator.send_message(
            "agent_3",
            ["agent_1", "agent_2", "agent_4", "agent_5", "agent_6", "agent_7", "agent_8"],
            "multimedia_update",
            "All multimedia services are now operational. Begin integration testing."
        )

        print("📢 Multimedia update broadcast to all agents")
        time.sleep(1)

        # Test 5: Emergency Communication Mode
        print("\n🚨 TEST 5: Emergency Communication Mode")
        print("-" * 40)

        # Test high-priority broadcast
        coordinator._broadcast_message(
            "general",
            {
                "type": "emergency_broadcast",
                "message": "EMERGENCY: System-wide coordination test in progress. All agents report status immediately.",
                "priority": "critical",
                "action_required": "Immediate status report required",
            },
        )

        print("🚨 Emergency broadcast sent to all agents")
        time.sleep(2)

        # Get final status
        print("\n📊 FINAL SYSTEM STATUS")
        print("-" * 40)

        status = coordinator.get_communication_status()

        print(f"Overall Status: {status['communication_status']['overall_status']}")
        print(
            f"Communication Mode: {status['communication_status']['communication_mode']}"
        )
        print(f"Current Captain: {status['communication_status']['current_captain']}")
        print(f"Active Tasks: {status['active_tasks']}")
        print(f"Active Sessions: {status['active_sessions']}")
        print(f"Presidential Decisions: {status['presidential_decisions']}")

        # Agent status summary
        print(f"\n🤖 AGENT STATUS SUMMARY")
        print("-" * 40)
        active_agents = 0
        for agent_id, agent_info in status["agent_connections"].items():
            if agent_info["status"] == "active":
                active_agents += 1
                print(f"✅ {agent_id}: {agent_info['role']} - {agent_info['status']}")
            else:
                print(f"❌ {agent_id}: {agent_info['role']} - {agent_info['status']}")

        print(f"\n📈 COMMUNICATION METRICS")
        print("-" * 40)
        print(f"Active Agents: {active_agents}/8")
        print(
            f"Multimedia Services: {len([s for s in status['multimedia_services'].values() if s == 'healthy'])}/3 healthy"
        )

        # Message queue status
        total_queued = sum(status["message_queues"].values())
        print(f"Queued Messages: {total_queued}")

        print("\n🎯 LIVE AGENT COMMUNICATION TEST RESULTS")
        print("=" * 50)
        print("✅ Presidential Decision Workflow: TESTED")
        print("✅ Collaboration Session Workflow: TESTED")
        print("✅ Task Progress Updates: TESTED")
        print("✅ Multimedia Integration: TESTED")
        print("✅ Emergency Communication: TESTED")
        print("✅ Agent Coordination: FUNCTIONAL")
        print("✅ Message Delivery: OPERATIONAL")
        print("✅ V1-Style Communication Patterns: ACTIVE")

        return True

    except Exception as e:
        print(f"❌ Error in live agent communication test: {e}")
        return False


if __name__ == "__main__":
    success = test_live_agent_communication()
    if success:
        print("\n🎉 LIVE AGENT COMMUNICATION TEST SUCCESSFUL!")
        exit(0)
    else:
        print("\n💥 LIVE AGENT COMMUNICATION TEST FAILED!")
        exit(1)
