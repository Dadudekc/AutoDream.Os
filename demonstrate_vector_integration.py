#!/usr/bin/env python3
"""
Demonstrate Vector Database Integration with Messaging System
===========================================================

This script demonstrates how the Swarm Brain vector database integrates
with the messaging system to provide intelligent communication and coordination.
"""

import logging
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.messaging.intelligent_coordinator import IntelligentAgentCoordinator
from services.messaging.intelligent_messaging import IntelligentMessagingService
from swarm_brain import Retriever

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demonstrate_intelligent_messaging():
    """Demonstrate intelligent messaging capabilities."""
    logger.info("=== INTELLIGENT MESSAGING DEMONSTRATION ===")

    try:
        # Initialize intelligent messaging service
        intelligent_messaging = IntelligentMessagingService()
        logger.info("✅ Intelligent Messaging Service initialized")

        # Demonstrate intelligent message sending
        logger.info("📤 Sending intelligent message...")
        success, suggestions = intelligent_messaging.send_message(
            agent_id="Agent-3",
            message="Please review the latest vector database integration",
            from_agent="Agent-1",
            priority="HIGH",
        )

        logger.info(f"✅ Message sent: {success}")
        logger.info(f"🧠 Intelligence suggestions: {suggestions}")

        # Demonstrate intelligent broadcast
        logger.info("📢 Broadcasting intelligent message...")
        broadcast_results = intelligent_messaging.broadcast_message(
            message="Vector database integration is now operational",
            from_agent="Agent-1",
            priority="NORMAL",
        )

        logger.info(f"✅ Broadcast completed: {len(broadcast_results)} agents notified")
        for agent_id, result in broadcast_results.items():
            logger.info(
                f"  {agent_id}: {result['success']} - {len(result.get('insights', {}))} insights"
            )

        # Demonstrate communication intelligence
        logger.info("🧠 Getting communication intelligence...")
        intelligence = intelligent_messaging.get_agent_communication_intelligence("Agent-3")
        logger.info(f"✅ Communication intelligence: {intelligence}")

        return True

    except Exception as e:
        logger.error(f"❌ Intelligent messaging demonstration failed: {e}")
        return False


def demonstrate_intelligent_coordination():
    """Demonstrate intelligent agent coordination."""
    logger.info("=== INTELLIGENT COORDINATION DEMONSTRATION ===")

    try:
        # Initialize intelligent coordinator
        coordinator = IntelligentAgentCoordinator()
        logger.info("✅ Intelligent Agent Coordinator initialized")

        # Demonstrate task coordination
        logger.info("🎯 Coordinating task...")
        coordination_result = coordinator.coordinate_task(
            task="vector database integration",
            required_skills=["database", "integration", "coordination"],
            priority="HIGH",
        )

        logger.info("✅ Task coordination completed")
        logger.info(f"📊 Success rate: {coordination_result['success_rate']}")
        logger.info(f"👥 Expert agents: {coordination_result['expert_agents']}")
        logger.info(f"📚 Lessons learned: {coordination_result['lessons_learned']}")

        # Demonstrate agent assignment suggestions
        logger.info("📋 Suggesting agent assignments...")
        assignments = coordinator.suggest_agent_assignments(
            ["database optimization", "integration testing", "performance monitoring"]
        )

        logger.info(f"✅ Agent assignments suggested for {len(assignments)} tasks")
        for task, assignment in assignments.items():
            logger.info(
                f"  {task}: {assignment['recommended_agent']} (confidence: {assignment['confidence']})"
            )

        # Demonstrate workload optimization
        logger.info("⚖️ Optimizing agent workload...")
        workload_analysis = coordinator.optimize_agent_workload(
            ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        )

        logger.info(f"✅ Workload optimization completed for {len(workload_analysis)} agents")
        for agent_id, analysis in workload_analysis.items():
            logger.info(f"  {agent_id}: {analysis['workload_balance']} workload")
            logger.info(f"    Recommendations: {analysis['recommendations']}")

        return True

    except Exception as e:
        logger.error(f"❌ Intelligent coordination demonstration failed: {e}")
        return False


def demonstrate_vector_database_queries():
    """Demonstrate vector database query capabilities."""
    logger.info("=== VECTOR DATABASE QUERIES DEMONSTRATION ===")

    try:
        # Initialize retriever
        retriever = Retriever()
        logger.info("✅ Vector Database Retriever initialized")

        # Demonstrate semantic search
        logger.info("🔍 Performing semantic search...")
        search_results = retriever.search("messaging system integration", k=5)
        logger.info(f"✅ Found {len(search_results)} relevant results")

        for result in search_results:
            logger.info(f"  - {result['title']} by {result['agent_id']}")

        # Demonstrate agent expertise
        logger.info("🧠 Getting agent expertise...")
        expertise = retriever.get_agent_expertise("Agent-1", k=10)
        logger.info(f"✅ Agent-1 expertise: {expertise['total_patterns']} patterns")

        # Demonstrate "how do agents do" queries
        logger.info("🎯 Finding successful patterns...")
        patterns = retriever.how_do_agents_do("successful messaging", k=5)
        logger.info(f"✅ Found {len(patterns)} successful messaging patterns")

        for pattern in patterns:
            logger.info(f"  - {pattern['title']} by {pattern['agent_id']}")

        # Demonstrate project patterns
        logger.info("📊 Getting project patterns...")
        project_patterns = retriever.get_project_patterns("Agent_Cellphone_V2", k=20)
        logger.info(f"✅ Project patterns: {project_patterns['total_activities']} activities")

        return True

    except Exception as e:
        logger.error(f"❌ Vector database queries demonstration failed: {e}")
        return False


def demonstrate_integration_benefits():
    """Demonstrate the benefits of vector database integration."""
    logger.info("=== INTEGRATION BENEFITS DEMONSTRATION ===")

    try:
        # Initialize components
        intelligent_messaging = IntelligentMessagingService()
        coordinator = IntelligentAgentCoordinator()
        retriever = Retriever()

        logger.info("✅ All components initialized")

        # Demonstrate learning from communication
        logger.info("📚 Learning from communication patterns...")

        # Send a message and learn from it
        success, suggestions = intelligent_messaging.send_message(
            agent_id="Agent-2", message="Testing vector database integration", from_agent="Agent-1"
        )

        # Query the learned patterns
        learned_patterns = retriever.search("testing vector database", k=3)
        logger.info(f"✅ Learned patterns: {len(learned_patterns)} patterns found")

        # Demonstrate intelligent coordination
        logger.info("🎯 Demonstrating intelligent coordination...")
        coordination_result = coordinator.coordinate_task(
            task="integration testing", required_skills=["testing", "integration"]
        )

        logger.info(f"✅ Coordination result: {coordination_result['success_rate']} success rate")

        # Demonstrate continuous learning
        logger.info("🔄 Demonstrating continuous learning...")

        # Get current state
        current_patterns = retriever.get_project_patterns("Agent_Cellphone_V2", k=20)
        logger.info(f"📊 Current project state: {current_patterns['total_activities']} activities")

        # The system learns from every interaction
        logger.info("✅ System continuously learns from all interactions")

        return True

    except Exception as e:
        logger.error(f"❌ Integration benefits demonstration failed: {e}")
        return False


def main():
    """Main demonstration function."""
    logger.info("🚀 Vector Database Integration Demonstration")
    logger.info("=" * 60)

    try:
        # Run all demonstrations
        results = []

        results.append(demonstrate_vector_database_queries())
        results.append(demonstrate_intelligent_messaging())
        results.append(demonstrate_intelligent_coordination())
        results.append(demonstrate_integration_benefits())

        # Summary
        successful_demos = sum(results)
        total_demos = len(results)

        logger.info("=" * 60)
        logger.info("🎉 Demonstration completed!")
        logger.info(f"📊 Results: {successful_demos}/{total_demos} demonstrations successful")

        if successful_demos == total_demos:
            logger.info("✅ All demonstrations successful!")
            logger.info("🧠 Vector database integration is working perfectly!")
            logger.info("🚀 The messaging system is now intelligent and self-learning!")
        else:
            logger.warning(f"⚠️ {total_demos - successful_demos} demonstrations had issues")
            logger.info("🔧 Check the logs above for details")

    except Exception as e:
        logger.error(f"❌ Demonstration failed: {e}")
        raise


if __name__ == "__main__":
    main()
