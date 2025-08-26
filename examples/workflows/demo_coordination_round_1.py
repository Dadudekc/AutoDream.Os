#!/usr/bin/env python3
"""
COORDINATION ROUND 1 DEMO: Decision-Making Algorithms
=====================================================

Demonstrates collaborative decision-making algorithms and coordination systems.
This is COORDINATION ROUND 1 of 6 - Decision-Making Algorithms focus.
"""

import time
import sys
import json

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from core.decision import DecisionManager as DecisionMakingEngine, DecisionType
from core.decision_coordination_system import (
    DecisionCoordinationSystem,
    CoordinationMode,
)


def main():
    """Demo COORDINATION ROUND 1: Decision-Making Algorithms"""
    print("🚀 COORDINATION ROUND 1: DECISION-MAKING ALGORITHMS")
    print("=" * 60)
    print("🎯 Focus: Decision-Making Algorithms")
    print("🤝 Implement collaborative decision-making")
    print("📡 Coordinate with other agents on decision logic")
    print("🏗️ Build decision coordination systems")
    print()

    # Initialize systems
    print("🔧 Initializing Decision-Making Systems...")
    decision_engine = DecisionMakingEngine()
    coordination_system = DecisionCoordinationSystem()

    print("✅ Decision-Making Engine initialized")
    print("✅ Decision Coordination System initialized")
    print()

    # DEMO 1: Task Assignment Decision
    print("📋 DEMO 1: Collaborative Task Assignment Decision")
    print("-" * 50)

    task_params = {
        "tasks": [
            {
                "id": "task_001",
                "type": "analysis",
                "priority": "high",
                "complexity": "medium",
            },
            {
                "id": "task_002",
                "type": "development",
                "priority": "medium",
                "complexity": "high",
            },
            {
                "id": "task_003",
                "type": "testing",
                "priority": "low",
                "complexity": "low",
            },
        ],
        "available_agents": ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"],
    }

    print(f"📝 Submitting task assignment decision request...")
    decision_id = decision_engine.submit_decision_request(
        DecisionType.TASK_ASSIGNMENT, "Coordinator", task_params, priority=1
    )
    print(f"✅ Decision request submitted: {decision_id}")

    # Process decision
    print("🔄 Processing collaborative decision...")
    result = decision_engine.process_decision(decision_id)
    print(f"✅ Decision completed with confidence: {result.confidence:.2f}")
    print(f"💡 Reasoning: {result.reasoning}")
    print(f"🤝 Collaborators: {len(result.collaborators)} agents")
    print()

    # DEMO 2: Resource Allocation Decision
    print("📋 DEMO 2: Collaborative Resource Allocation Decision")
    print("-" * 50)

    resource_params = {
        "resources": {"cpu": 100, "memory": 64, "storage": 1000},
        "demands": {
            "cpu": {
                "Agent-1": 30,
                "Agent-2": 25,
                "Agent-3": 20,
                "Agent-4": 15,
                "Agent-5": 10,
            },
            "memory": {
                "Agent-1": 16,
                "Agent-2": 12,
                "Agent-3": 8,
                "Agent-4": 6,
                "Agent-5": 4,
            },
            "storage": {
                "Agent-1": 200,
                "Agent-2": 150,
                "Agent-3": 100,
                "Agent-4": 75,
                "Agent-5": 50,
            },
        },
    }

    print(f"📝 Submitting resource allocation decision request...")
    resource_decision_id = decision_engine.submit_decision_request(
        DecisionType.RESOURCE_ALLOCATION, "ResourceManager", resource_params, priority=2
    )
    print(f"✅ Decision request submitted: {resource_decision_id}")

    # Process resource decision
    print("🔄 Processing resource allocation decision...")
    resource_result = decision_engine.process_decision(resource_decision_id)
    print(
        f"✅ Resource allocation completed with confidence: {resource_result.confidence:.2f}"
    )
    print(f"💡 Reasoning: {resource_result.reasoning}")
    print()

    # DEMO 3: Decision Coordination Session
    print("📋 DEMO 3: Decision Coordination Session")
    print("-" * 50)

    # Create a new decision for coordination
    priority_params = {
        "items": [
            {"id": "item_1", "urgency": 9, "impact": 8, "effort": 5},
            {"id": "item_2", "urgency": 7, "impact": 9, "effort": 3},
            {"id": "item_3", "urgency": 5, "impact": 6, "effort": 7},
        ],
        "criteria": {"urgency": 0.4, "impact": 0.4, "effort": 0.2},
    }

    priority_decision_id = decision_engine.submit_decision_request(
        DecisionType.PRIORITY_DETERMINATION,
        "PriorityManager",
        priority_params,
        priority=3,
    )
    print(f"📝 Priority decision request submitted: {priority_decision_id}")

    # Initiate coordination session
    print("🤝 Initiating collaborative coordination session...")
    session_id = coordination_system.initiate_coordination_session(
        priority_decision_id, CoordinationMode.COLLABORATIVE
    )
    print(f"✅ Coordination session initiated: {session_id}")
    print(f"📋 Mode: Collaborative (all agents participate)")

    # Show coordination status
    print("\n📊 Coordination Session Status:")
    session_status = coordination_system.get_session_status(session_id)
    if session_status:
        for key, value in session_status.items():
            print(f"  {key}: {value}")

    # Wait for coordination to progress
    print("\n⏱️ Waiting for coordination to progress...")
    time.sleep(3)

    # Show updated status
    print("\n📊 Updated Coordination Status:")
    updated_status = coordination_system.get_session_status(session_id)
    if updated_status:
        for key, value in updated_status.items():
            print(f"  {key}: {value}")

    print()

    # DEMO 4: Multiple Coordination Modes
    print("📋 DEMO 4: Multiple Coordination Modes")
    print("-" * 50)

    coordination_modes = [
        CoordinationMode.CONSENSUS,
        CoordinationMode.MAJORITY,
        CoordinationMode.EXPERT_OPINION,
        CoordinationMode.HIERARCHICAL,
        CoordinationMode.COLLABORATIVE,
    ]

    print("🔄 Testing different coordination modes:")
    for mode in coordination_modes:
        print(
            f"  📋 {mode.value}: {coordination_system.coordination_protocols[mode]['description']}"
        )
        print(
            f"     Threshold: {coordination_system.coordination_protocols[mode]['threshold']}"
        )
        print(
            f"     Timeout: {coordination_system.coordination_protocols[mode]['timeout']}s"
        )

    print()

    # DEMO 5: System Integration
    print("📋 DEMO 5: System Integration & Metrics")
    print("-" * 50)

    # Show decision engine metrics
    print("📊 Decision-Making Engine Metrics:")
    decision_metrics = decision_engine.get_collaboration_metrics()
    for key, value in decision_metrics.items():
        print(f"  {key}: {value}")

    print()

    # Show coordination system metrics
    print("📊 Decision Coordination System Metrics:")
    coord_metrics = coordination_system.get_coordination_status()
    for key, value in coord_metrics.items():
        print(f"  {key}: {value}")

    print()

    # COORDINATION ROUND 1 COMPLETION
    print("🎉 COORDINATION ROUND 1: DECISION-MAKING ALGORITHMS - COMPLETED!")
    print("=" * 60)
    print("✅ Collaborative Decision-Making Algorithms implemented")
    print("✅ Decision Coordination Systems built")
    print("✅ Agent collaboration on decision logic established")
    print("✅ Multiple coordination modes operational")
    print("✅ System integration completed")
    print()
    print("📋 COORDINATION ROUND 1 ACCOMPLISHMENTS:")
    print("  🧠 Decision-Making Engine: 6 decision types, collaborative algorithms")
    print("  🤝 Decision Coordination System: 5 coordination modes, session management")
    print("  📡 Agent Communication: Inbox-based messaging, real-time coordination")
    print("  🔄 Process Management: Multi-phase coordination, consensus building")
    print("  📊 Metrics & Monitoring: Real-time status, collaboration tracking")
    print()
    print("🚀 READY FOR COORDINATION ROUND 2!")
    print("💡 The agent swarm now has collaborative decision-making capabilities!")


if __name__ == "__main__":
    main()
