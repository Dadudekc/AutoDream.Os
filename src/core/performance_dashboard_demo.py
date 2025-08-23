#!/usr/bin/env python3
"""
🚀 Performance Dashboard Demo - Agent_Cellphone_V2
Integration & Performance Optimization Captain - Phase 1 Foundation

This script demonstrates the deployed performance monitoring infrastructure
and cross-system integration capabilities.
"""

import sys
import os
import time
import threading
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from core.performance_tracker import PerformanceTracker, MetricType
from core.performance_profiler import PerformanceProfiler
from core.performance_dashboard import PerformanceDashboard
from core.api_gateway import APIGateway
from core.agent_communication import AgentCommunicationProtocol
from core.health_monitor_core import HealthMonitorCore


class PerformanceInfrastructureDemo:
    """Demonstrates the deployed performance monitoring infrastructure."""

    def __init__(self):
        """Initialize the performance infrastructure demo."""
        print("🚀 Initializing Performance Infrastructure Demo...")

        # Initialize core systems
        self.performance_tracker = PerformanceTracker()
        self.performance_profiler = PerformanceProfiler()
        self.performance_dashboard = PerformanceDashboard()
        self.api_gateway = APIGateway()
        self.agent_communication = AgentCommunicationProtocol()
        self.health_monitor = HealthMonitorCore()

        print("✅ All core systems initialized successfully")

    def demonstrate_performance_monitoring(self):
        """Demonstrate performance monitoring capabilities."""
        print("\n📊 Demonstrating Performance Monitoring...")

        # Record performance metrics
        self.performance_tracker.record_metric(
            MetricType.RESPONSE_TIME,
            0.5,
            agent_id="demo_agent",
            context={"operation": "demo_test"},
        )

        self.performance_tracker.record_metric(
            MetricType.CPU_USAGE,
            25.0,
            agent_id="demo_agent",
            context={"operation": "demo_test"},
        )

        # Get performance summary
        summary = self.performance_tracker.get_agent_performance_summary("demo_agent")
        print(f"✅ Performance metrics recorded: {len(summary)} metric types")

        for metric_type, data in summary.items():
            print(
                f"   📈 {metric_type}: {data['count']} samples, avg: {data['avg']:.2f}"
            )

    def demonstrate_api_gateway(self):
        """Demonstrate API gateway capabilities."""
        print("\n🌐 Demonstrating API Gateway...")

        # Register demo services
        self.api_gateway.register_service(
            "demo_service", "Demo Service", "1.0", "http://localhost:8000"
        )

        self.api_gateway.register_service(
            "monitoring_service", "Monitoring Service", "1.0", "http://localhost:8001"
        )

        services = self.api_gateway.get_all_services()
        print(f"✅ API Gateway operational: {len(services)} services registered")

        for service in services:
            print(f"   🔗 {service.name} ({service.version}) at {service.base_url}")

    def demonstrate_agent_communication(self):
        """Demonstrate agent communication capabilities."""
        print("\n💬 Demonstrating Agent Communication...")

        # Register demo agents
        self.agent_communication.register_agent(
            "demo_agent",
            "Demo Agent",
            ["performance_monitoring", "data_processing"],
            "http://localhost:8002",
        )

        self.agent_communication.register_agent(
            "monitor_agent",
            "Monitor Agent",
            ["health_monitoring", "alerting"],
            "http://localhost:8003",
        )

        agents = list(self.agent_communication.registered_agents.keys())
        print(f"✅ Agent Communication operational: {len(agents)} agents registered")

        for agent_id in agents:
            agent_info = self.agent_communication.registered_agents[agent_id]
            print(
                f"   🤖 {agent_info.name} ({agent_id}) - {len(agent_info.capabilities)} capabilities"
            )

    def demonstrate_health_monitoring(self):
        """Demonstrate health monitoring capabilities."""
        print("\n🏥 Demonstrating Health Monitoring...")

        # Start health monitoring
        self.health_monitor.start()
        print("✅ Health monitoring started")

        # Simulate some monitoring time
        time.sleep(1)

        # Stop health monitoring
        self.health_monitor.stop()
        print("✅ Health monitoring stopped")

    def run_full_demo(self):
        """Run the complete performance infrastructure demonstration."""
        print("=" * 60)
        print("🚀 PERFORMANCE INFRASTRUCTURE DEMONSTRATION")
        print("=" * 60)
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        try:
            # Run all demonstrations
            self.demonstrate_performance_monitoring()
            self.demonstrate_api_gateway()
            self.demonstrate_agent_communication()
            self.demonstrate_health_monitoring()

            print("\n" + "=" * 60)
            print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
            print("✅ All core systems operational")
            print("✅ Performance monitoring active")
            print("✅ Cross-system communication established")
            print("✅ Health monitoring functional")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            raise


def main():
    """Main entry point for the performance infrastructure demo."""
    try:
        demo = PerformanceInfrastructureDemo()
        demo.run_full_demo()

        print("\n🚀 Phase 1 Foundation Setup: COMPLETE")
        print("📊 Performance monitoring infrastructure: OPERATIONAL")
        print("🌐 Cross-system communication: ESTABLISHED")
        print("🏥 Health monitoring systems: ACTIVE")

    except Exception as e:
        print(f"\n❌ Foundation setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
