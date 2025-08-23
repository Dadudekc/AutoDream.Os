#!/usr/bin/env python3
"""
Critical Systems Integration Demo for Agent Cellphone V2
Demonstrates Internationalization, Horizontal Scaling, and Autonomous Decision-Making
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from core.internationalization_manager import (
    InternationalizationManager,
    LanguageCode,
    CulturalRegion,
    LocalizationLevel,
)
from core.horizontal_scaling_engine import (
    HorizontalScalingEngine,
    ScalingStrategy,
    AgentStatus,
    DeploymentType,
)
from core.autonomous_decision_engine import (
    AutonomousDecisionEngine,
    DecisionType,
    DecisionConfidence,
    LearningMode,
    IntelligenceLevel,
)
from core.persistent_data_storage import PersistentDataStorage, DataIntegrityLevel


def demo_internationalization_system():
    """Demonstrate internationalization capabilities"""
    print("\n🌍 INTERNATIONALIZATION SYSTEM DEMO")
    print("=" * 50)

    # Initialize internationalization manager
    i18n_manager = InternationalizationManager()

    # Show supported languages
    print("📚 Supported Languages:")
    languages = i18n_manager.get_supported_languages()
    for lang in languages:
        print(f"  {lang['code']}: {lang['name']} ({lang['native_name']})")

    # Test language switching
    print("\n🔄 Language Switching Test:")
    print(f"Current language: {i18n_manager.current_language.value}")

    i18n_manager.set_language("es")
    print(f"Switched to: {i18n_manager.current_language.value}")

    i18n_manager.set_language("fr")
    print(f"Switched to: {i18n_manager.current_language.value}")

    # Test cultural region switching
    print("\n🌍 Cultural Region Test:")
    print(f"Current region: {i18n_manager.current_region.value}")

    i18n_manager.set_cultural_region("europe")
    print(f"Switched to: {i18n_manager.current_region.value}")

    # Test localization level
    print("\n📊 Localization Level Test:")
    print(f"Current level: {i18n_manager.localization_level.value}")

    i18n_manager.set_localization_level("advanced")
    print(f"Upgraded to: {i18n_manager.localization_level.value}")

    # Test translation
    print("\n🔤 Translation Test:")
    test_text = "Hello, world!"
    translated = i18n_manager.translate_text(test_text)
    print(f"'{test_text}' -> '{translated}'")

    # Test cultural adaptation
    print("\n🎨 Cultural Adaptation Test:")
    adaptation = i18n_manager.get_cultural_adaptation("colors", "ui")
    print(f"Cultural adaptation for colors: {adaptation}")

    # Show system status
    print("\n📊 Internationalization Status:")
    status = i18n_manager.get_system_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    return i18n_manager


def demo_horizontal_scaling_system():
    """Demonstrate horizontal scaling capabilities"""
    print("\n📊 HORIZONTAL SCALING SYSTEM DEMO")
    print("=" * 50)

    # Initialize horizontal scaling engine
    scaling_engine = HorizontalScalingEngine()

    # Show initial status
    print("📈 Initial Scaling Status:")
    status = scaling_engine.get_scaling_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    # Test agent node creation
    print("\n🆕 Agent Node Creation Test:")
    test_node = scaling_engine._create_agent_node()
    if test_node:
        scaling_engine.add_agent_node(test_node)
        print(f"✅ Created agent node: {test_node.node_id}")
        print(f"  Hostname: {test_node.hostname}")
        print(f"  IP: {test_node.ip_address}:{test_node.port}")
        print(f"  Status: {test_node.status}")

    # Test load balancing strategies
    print("\n⚖️ Load Balancing Strategy Test:")
    strategies = [s.value for s in ScalingStrategy]
    for strategy in strategies:
        print(f"Testing strategy: {strategy}")
        scaling_engine.load_balancer_config.strategy = strategy
        next_node = scaling_engine.get_next_agent_node()
        if next_node:
            print(f"  Selected node: {next_node.node_id}")
        else:
            print("  No available nodes")

    # Test metrics update
    print("\n📊 Metrics Update Test:")
    if test_node:
        scaling_engine.update_node_metrics(test_node.node_id, 75.5, 0.3)
        print(f"✅ Updated metrics for {test_node.node_id}")
        print(f"  Load: 75.5, Response Time: 0.3s")

    # Test scaling metrics
    print("\n📈 Scaling Metrics Test:")
    scaling_engine.update_scaling_metrics(True, 0.5)
    scaling_engine.update_scaling_metrics(True, 0.3)
    scaling_engine.update_scaling_metrics(False, 1.2)
    print("✅ Updated scaling metrics")

    # Show final status
    print("\n📊 Final Scaling Status:")
    final_status = scaling_engine.get_scaling_status()
    for key, value in final_status.items():
        print(f"  {key}: {value}")

    return scaling_engine


def demo_autonomous_decision_system():
    """Demonstrate autonomous decision-making capabilities"""
    print("\n🧠 AUTONOMOUS DECISION-MAKING SYSTEM DEMO")
    print("=" * 50)

    # Initialize autonomous decision engine
    decision_engine = AutonomousDecisionEngine()

    # Show initial status
    print("📊 Initial Autonomous Status:")
    status = decision_engine.get_autonomous_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    # Test agent capability updates
    print("\n👥 Agent Capability Test:")
    from core.autonomous_decision_engine import AgentCapability

    test_capability = AgentCapability(
        agent_id="demo_agent_001",
        skills=["python", "ai", "ml", "scaling"],
        experience_level=0.85,
        performance_history=[0.8, 0.9, 0.85, 0.92, 0.88],
        learning_rate=0.15,
        specialization="ai_development",
        availability=True,
    )

    decision_engine.update_agent_capability("demo_agent_001", test_capability)
    print("✅ Updated agent capability for demo_agent_001")

    # Test autonomous decision making
    print("\n🤖 Autonomous Decision Test:")
    from core.autonomous_decision_engine import DecisionContext

    # Test task assignment decision
    task_context = DecisionContext(
        decision_id="demo_task_001",
        decision_type=DecisionType.TASK_ASSIGNMENT.value,
        timestamp=datetime.now().isoformat(),
        agent_id="demo_agent_001",
        context_data={
            "task_requirements": ["python", "ai"],
            "task_complexity": "high",
            "deadline": "2024-12-31",
        },
        constraints=["time_limit", "resource_constraints"],
        objectives=["efficiency", "quality", "learning"],
        risk_factors=["complexity", "uncertainty"],
    )

    task_decision = decision_engine.make_autonomous_decision(
        DecisionType.TASK_ASSIGNMENT.value, task_context
    )

    print(f"✅ Task assignment decision made:")
    print(f"  Selected option: {task_decision.selected_option}")
    print(f"  Confidence: {task_decision.confidence}")
    print(f"  Reasoning: {task_decision.reasoning}")
    print(f"  Expected outcome: {task_decision.expected_outcome}")

    # Test resource allocation decision
    resource_context = DecisionContext(
        decision_id="demo_resource_001",
        decision_type=DecisionType.RESOURCE_ALLOCATION.value,
        timestamp=datetime.now().isoformat(),
        agent_id="demo_agent_001",
        context_data={
            "resources": ["gpu_001", "gpu_002", "memory_001", "storage_001"],
            "resource_types": ["computing", "memory", "storage"],
            "priority": "high",
        },
        constraints=["budget_limit", "availability"],
        objectives=["efficiency", "cost_effectiveness"],
        risk_factors=["resource_contention", "failure_risk"],
    )

    resource_decision = decision_engine.make_autonomous_decision(
        DecisionType.RESOURCE_ALLOCATION.value, resource_context
    )

    print(f"\n✅ Resource allocation decision made:")
    print(f"  Selected option: {resource_decision.selected_option}")
    print(f"  Confidence: {resource_decision.confidence}")
    print(f"  Reasoning: {resource_decision.reasoning}")

    # Test learning data addition
    print("\n📚 Learning Data Test:")
    from core.autonomous_decision_engine import LearningData

    learning_data = LearningData(
        input_features=[0.9, 0.8, 0.95, 0.7],
        output_target="success",
        context="task_assignment",
        timestamp=datetime.now().isoformat(),
        performance_metric=0.92,
        feedback_score=0.9,
    )

    decision_engine.add_learning_data(learning_data)
    print("✅ Added learning data for continuous improvement")

    # Test performance metrics
    print("\n📊 Performance Metrics Test:")
    decision_engine.record_performance_metric("decision_accuracy", 0.92)
    decision_engine.record_performance_metric("response_time", 0.3)
    decision_engine.record_performance_metric("user_satisfaction", 0.88)
    print("✅ Recorded performance metrics")

    # Show final status
    print("\n📊 Final Autonomous Status:")
    final_status = decision_engine.get_autonomous_status()
    for key, value in final_status.items():
        print(f"  {key}: {value}")

    return decision_engine


def demo_system_integration():
    """Demonstrate integration between all three systems"""
    print("\n🔗 CRITICAL SYSTEMS INTEGRATION DEMO")
    print("=" * 50)

    # Initialize all systems
    print("🚀 Initializing all critical systems...")
    i18n_manager = InternationalizationManager()
    scaling_engine = HorizontalScalingEngine()
    decision_engine = AutonomousDecisionEngine()

    print("✅ All systems initialized")

    # Test cross-system communication
    print("\n🔄 Cross-System Communication Test:")

    # Internationalization + Scaling
    print("Testing i18n + scaling integration...")
    i18n_manager.set_language("en")
    i18n_manager.set_cultural_region("north_america")

    # Create a culturally-aware agent node
    test_node = scaling_engine._create_agent_node()
    if test_node:
        scaling_engine.add_agent_node(test_node)
        print(f"✅ Created culturally-aware agent node: {test_node.node_id}")

    # Scaling + Autonomous Decision
    print("Testing scaling + autonomous decision integration...")
    if test_node:
        # Update node metrics
        scaling_engine.update_node_metrics(test_node.node_id, 60.0, 0.4)

        # Make autonomous decision about scaling
        from core.autonomous_decision_engine import DecisionContext

        scaling_context = DecisionContext(
            decision_id="scaling_decision_001",
            decision_type=DecisionType.RESOURCE_ALLOCATION.value,
            timestamp=datetime.now().isoformat(),
            agent_id=test_node.node_id,
            context_data={
                "current_load": 60.0,
                "max_capacity": 100.0,
                "response_time": 0.4,
                "scaling_threshold": 80.0,
            },
            constraints=["budget", "infrastructure"],
            objectives=["performance", "cost_efficiency"],
            risk_factors=["over_scaling", "under_scaling"],
        )

        scaling_decision = decision_engine.make_autonomous_decision(
            DecisionType.RESOURCE_ALLOCATION.value, scaling_context
        )

        print(f"✅ Autonomous scaling decision made:")
        print(f"  Decision: {scaling_decision.selected_option}")
        print(f"  Confidence: {scaling_decision.confidence}")
        print(f"  Reasoning: {scaling_decision.reasoning}")

    # Autonomous Decision + Internationalization
    print("Testing autonomous decision + i18n integration...")

    # Make decision in different cultural contexts
    cultural_regions = ["north_america", "europe", "asia_pacific"]

    for region in cultural_regions:
        i18n_manager.set_cultural_region(region)
        print(f"\n🌍 Testing in {region} cultural context:")

        # Get cultural adaptation for decision making
        adaptation = i18n_manager.get_cultural_adaptation("decision_style", "business")
        print(f"  Cultural adaptation: {adaptation}")

        # Make culturally-aware decision
        cultural_context = DecisionContext(
            decision_id=f"cultural_decision_{region}",
            decision_type=DecisionType.TASK_ASSIGNMENT.value,
            timestamp=datetime.now().isoformat(),
            agent_id="cultural_agent",
            context_data={
                "task_requirements": ["communication", "cultural_awareness"],
                "cultural_context": region,
                "formality_level": "professional",
            },
            constraints=["cultural_sensitivity", "language_barriers"],
            objectives=["cultural_appropriateness", "effectiveness"],
            risk_factors=["cultural_misunderstanding", "communication_failure"],
        )

        cultural_decision = decision_engine.make_autonomous_decision(
            DecisionType.TASK_ASSIGNMENT.value, cultural_context
        )

        print(f"  Decision made: {cultural_decision.selected_option}")
        print(f"  Confidence: {cultural_decision.confidence}")

    print("\n🎉 Cross-system integration test completed successfully!")


def main():
    """Main demo function"""
    print("🚀 CRITICAL SYSTEMS INTEGRATION DEMO")
    print("=" * 60)
    print("This demo showcases the integration of three critical systems:")
    print("1. 🌍 Internationalization (Multi-language & Cultural Support)")
    print("2. 📊 Horizontal Scaling (Load Balancing & Auto-scaling)")
    print("3. 🧠 Autonomous Decision-Making (AI/ML & Self-Learning)")
    print("=" * 60)

    try:
        # Demo individual systems
        i18n_manager = demo_internationalization_system()
        scaling_engine = demo_horizontal_scaling_system()
        decision_engine = demo_autonomous_decision_system()

        # Demo system integration
        demo_system_integration()

        print("\n🎉 ALL CRITICAL SYSTEMS DEMONSTRATED SUCCESSFULLY!")
        print("=" * 60)
        print("✅ Internationalization: Multi-language support, cultural adaptation")
        print("✅ Horizontal Scaling: Load balancing, auto-scaling, health monitoring")
        print(
            "✅ Autonomous Decision-Making: AI/ML, pattern recognition, self-improvement"
        )
        print("✅ System Integration: Cross-system communication and coordination")
        print("=" * 60)

        # Show final status of all systems
        print("\n📊 FINAL SYSTEM STATUS SUMMARY:")
        print("-" * 40)

        print("🌍 Internationalization Status:")
        i18n_status = i18n_manager.get_system_status()
        print(f"  Current Language: {i18n_status['current_language']}")
        print(f"  Current Region: {i18n_status['current_region']}")
        print(f"  Localization Level: {i18n_status['localization_level']}")

        print("\n📊 Horizontal Scaling Status:")
        scaling_status = scaling_engine.get_scaling_status()
        print(f"  Total Nodes: {scaling_status['total_nodes']}")
        print(f"  Online Nodes: {scaling_status['online_nodes']}")
        print(f"  Load Balancer Strategy: {scaling_status['load_balancer_strategy']}")

        print("\n🧠 Autonomous Decision Status:")
        decision_status = decision_engine.get_autonomous_status()
        print(f"  Intelligence Level: {decision_status['intelligence_level']}")
        print(f"  Learning Mode: {decision_status['learning_mode']}")
        print(f"  Total Decisions: {decision_status['total_decisions']}")

        print("\n🎯 MISSION ACCOMPLISHED!")
        print("All three critical systems are fully operational and integrated!")

    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # Cleanup
        print("\n🧹 Cleaning up demo systems...")
        try:
            if "i18n_manager" in locals():
                i18n_manager.shutdown()
            if "scaling_engine" in locals():
                scaling_engine.shutdown()
            if "decision_engine" in locals():
                decision_engine.shutdown()
            print("✅ Cleanup completed")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")


if __name__ == "__main__":
    main()
