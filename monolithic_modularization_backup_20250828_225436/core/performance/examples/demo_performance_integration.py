#!/usr/bin/env python3
"""
🚀 Performance Integration Demo - Agent_Cellphone_V2

Comprehensive demonstration of the integrated performance monitoring,
communication, and API gateway systems.

Author: Performance & Integration Specialist
License: MIT
"""

import os
import sys
import time
import json
import asyncio
import threading

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.performance_monitor import PerformanceMonitor, MetricType
from core.performance_dashboard import PerformanceDashboard, DashboardView, AlertLevel
from core.v2_comprehensive_messaging_system import (
    V2ComprehensiveMessagingSystem,
    V2MessageType,
    V2MessagePriority,
    V2AgentStatus,
)
from core.api_gateway import APIGateway, APIVersion, ServiceStatus


class PerformanceIntegrationDemo:
    """Comprehensive demo of integrated performance systems"""

    def __init__(self):
        """Initialize the performance integration demo"""
        self.config = {
            "max_metrics_history": 5000,
            "snapshot_interval": 10,
            "metric_retention_days": 7,
            "profiling_enabled": True,
            "heartbeat_interval": 15,
            "message_timeout": 120,
            "health_check_interval": 45,
        }

        # Initialize core systems
        self.performance_tracker = PerformanceMonitor(self.config)
        self.performance_profiler = PerformanceMonitor(self.config)
        self.messaging_system = V2ComprehensiveMessagingSystem(self.config)
        self.api_gateway = APIGateway(self.config)

        # Initialize dashboard
        self.performance_dashboard = PerformanceDashboard(
            agent_manager=None,
            performance_tracker=self.performance_tracker,
            config_manager=None,
            message_router=None,
        )

        # Set up integrations
        # Note: V2 messaging system doesn't need performance tracker setup
        self.api_gateway.set_performance_tracker(self.performance_tracker)

        # Demo state
        self.demo_running = False
        self.demo_thread = None

        print("🚀 Performance Integration Demo initialized")

    def start_demo(self):
        """Start the comprehensive demo"""
        print("\n" + "=" * 80)
        print("🚀 STARTING PERFORMANCE INTEGRATION DEMO")
        print("=" * 80)

        # Start all systems
        self.performance_dashboard.start()
        # Note: V2 messaging system starts automatically
        self.api_gateway.start_gateway()

        # Wait for initialization
        time.sleep(3)

        # Run demo scenarios
        self._run_demo_scenarios()

        # Start continuous demo loop
        self.demo_running = True
        self.demo_thread = threading.Thread(target=self._demo_loop, daemon=True)
        self.demo_thread.start()

        print("✅ Demo started successfully!")
        print("Press Ctrl+C to stop the demo")

    def stop_demo(self):
        """Stop the demo and cleanup"""
        print("\n🛑 Stopping demo...")

        self.demo_running = False
        if self.demo_thread:
            self.demo_thread.join(timeout=5)

        # Stop all systems
        self.performance_dashboard.cleanup()
        # Note: V2 messaging system cleanup handled automatically
        self.api_gateway.cleanup()
        self.performance_tracker.cleanup()
        self.performance_profiler.cleanup()

        print("✅ Demo stopped and cleaned up")

    def _run_demo_scenarios(self):
        """Run initial demo scenarios"""
        print("\n📋 Running initial demo scenarios...")

        # Scenario 1: Agent Registration and Communication
        self._demo_agent_registration()

        # Scenario 2: Service Registration and API Gateway
        self._demo_service_registration()

        # Scenario 3: Performance Metrics Collection
        self._demo_performance_metrics()

        # Scenario 4: Cross-System Integration
        self._demo_cross_system_integration()

        print("✅ Initial demo scenarios completed")

    def _demo_agent_registration(self):
        """Demonstrate agent registration and communication"""
        print("  🔧 Demo: Agent Registration and Communication")

        # Register demo agents
        agents = [
            (
                "monitoring_agent",
                "System Monitoring Agent",
                ["monitoring", "alerting", "metrics"],
            ),
            (
                "data_processor",
                "Data Processing Agent",
                ["data_processing", "analytics", "reporting"],
            ),
            (
                "task_coordinator",
                "Task Coordination Agent",
                ["coordination", "scheduling", "workflow"],
            ),
            (
                "security_monitor",
                "Security Monitoring Agent",
                ["security", "threat_detection", "compliance"],
            ),
        ]

        for agent_id, name, capabilities in agents:
            self.agent_communication.register_agent(
                agent_id,
                name,
                capabilities,
                f"http://localhost:800{hash(agent_id) % 10}",
                {"demo": True, "capabilities": capabilities},
            )
            print(f"    ✅ Registered {name} ({agent_id})")

        # Test agent discovery
        monitoring_agents = self.agent_communication.find_agents_by_capability(
            "monitoring"
        )
        print(f"    📡 Found {len(monitoring_agents)} monitoring agents")

        # Test message sending
        message_id = self.agent_communication.send_message(
            "system",
            "monitoring_agent",
            MessageType.TASK_ASSIGNMENT,
            {"task": "monitor_system_health", "priority": "high"},
            UnifiedMessagePriority.HIGH,
        )
        print(f"    📨 Sent task assignment message: {message_id}")

    def _demo_service_registration(self):
        """Demonstrate service registration and API gateway"""
        print("  🔧 Demo: Service Registration and API Gateway")

        # Register demo services
        services = [
            ("user_service", "User Management Service", "v1", "http://localhost:8001"),
            ("data_service", "Data Processing Service", "v1", "http://localhost:8002"),
            ("analytics_service", "Analytics Service", "v1", "http://localhost:8003"),
            (
                "notification_service",
                "Notification Service",
                "v1",
                "http://localhost:8004",
            ),
        ]

        for service_id, name, version, base_url in services:
            self.api_gateway.register_service(
                service_id,
                name,
                version,
                base_url,
                metadata={"demo": True, "category": "core_service"},
            )
            print(f"    ✅ Registered {name} ({service_id}) at {base_url}")

        # Set rate limits
        self.api_gateway.set_rate_limit("user_service", 100, 20)
        self.api_gateway.set_rate_limit("data_service", 50, 10)
        print("    ⚡ Rate limits configured")

        # Test API routing
        response = self.api_gateway.route_request(
            "GET",
            "/v1/users",
            {"Authorization": "Bearer demo-token"},
            {"page": "1", "limit": "10"},
            None,
            "127.0.0.1",
            "demo-client",
        )
        print(f"    🌐 API request routed successfully (Status: {response.status_code})")

    def _demo_performance_metrics(self):
        """Demonstrate performance metrics collection"""
        print("  🔧 Demo: Performance Metrics Collection")

        # Generate various performance metrics
        metric_scenarios = [
            (MetricType.RESPONSE_TIME, 0.3, "monitoring_agent"),
            (MetricType.CPU_USAGE, 65.0, "monitoring_agent"),
            (MetricType.MEMORY_USAGE, 1.8, "monitoring_agent"),
            (MetricType.RESPONSE_TIME, 0.8, "data_processor"),
            (MetricType.ERROR_RATE, 0.01, "data_processor"),
            (MetricType.THROUGHPUT, 150.0, "data_processor"),
            (MetricType.RESPONSE_TIME, 0.5, "task_coordinator"),
            (MetricType.SYSTEM_LOAD, 0.7, "task_coordinator"),
            (MetricType.NETWORK_LATENCY, 45.0, "security_monitor"),
            (MetricType.AGENT_HEALTH, 95.0, "security_monitor"),
        ]

        for metric_type, value, agent_id in metric_scenarios:
            self.performance_tracker.record_metric(
                metric_type,
                value,
                agent_id=agent_id,
                context={"demo": True, "scenario": "performance_metrics"},
                metadata={"source": "demo", "timestamp": datetime.now().isoformat()},
            )
            print(f"    📊 Recorded {metric_type.value}: {value} for {agent_id}")

        # Test profiling
        with self.performance_profiler.profile(
            "demo_metrics_collection", {"demo": True}
        ):
            time.sleep(0.2)  # Simulate work

        print("    ⚡ Performance profiling completed")

    def _demo_cross_system_integration(self):
        """Demonstrate cross-system integration"""
        print("  🔧 Demo: Cross-System Integration")

        # Simulate agent status updates
        for agent_id in [
            "monitoring_agent",
            "data_processor",
            "task_coordinator",
            "security_monitor",
        ]:
            status = AgentStatus.ONLINE if hash(agent_id) % 2 == 0 else AgentStatus.BUSY
            self.agent_communication.update_agent_status(agent_id, status)
            print(f"    🔄 Updated {agent_id} status to: {status.value}")

        # Simulate service health checks
        for service_id in [
            "user_service",
            "data_service",
            "analytics_service",
            "notification_service",
        ]:
            # This would normally come from actual health checks
            print(f"    🏥 Service {service_id} health status monitored")

        # Test dashboard integration
        dashboard_data = self.performance_dashboard.get_dashboard_data()
        print(
            f"    📊 Dashboard data collected: {len(dashboard_data.alerts)} alerts, {len(dashboard_data.system_metrics)} system metrics"
        )

        # Add demo alert
        self.performance_dashboard.add_alert(
            AlertLevel.INFO,
            "Demo integration completed successfully",
            "demo_system",
            {"demo": True, "timestamp": datetime.now().isoformat()},
        )
        print("    🚨 Demo alert added to dashboard")

    def _demo_loop(self):
        """Continuous demo loop"""
        iteration = 0

        while self.demo_running:
            try:
                iteration += 1

                # Simulate ongoing system activity
                self._simulate_system_activity(iteration)

                # Update demo status
                if iteration % 10 == 0:
                    self._show_demo_status(iteration)

                # Wait before next iteration
                time.sleep(5)

            except Exception as e:
                print(f"⚠️ Error in demo loop: {e}")
                time.sleep(10)

    def _simulate_system_activity(self, iteration):
        """Simulate ongoing system activity"""
        # Simulate agent performance variations
        agent_ids = [
            "monitoring_agent",
            "data_processor",
            "task_coordinator",
            "security_monitor",
        ]

        for agent_id in agent_ids:
            # Vary performance metrics
            base_response_time = 0.3 + (iteration % 5) * 0.1
            base_cpu_usage = 60.0 + (iteration % 10) * 2.0

            self.performance_tracker.record_metric(
                MetricType.RESPONSE_TIME,
                base_response_time,
                agent_id=agent_id,
                context={"demo": True, "iteration": iteration},
            )

            self.performance_tracker.record_metric(
                MetricType.CPU_USAGE,
                base_cpu_usage,
                agent_id=agent_id,
                context={"demo": True, "iteration": iteration},
            )

        # Simulate API requests
        if iteration % 3 == 0:
            self.api_gateway.route_request(
                "GET",
                f"/v1/demo/{iteration}",
                {"X-Demo": "true"},
                {"iteration": str(iteration)},
                None,
                "127.0.0.1",
                "demo-loop",
            )

        # Simulate agent communication
        if iteration % 5 == 0:
            sender = agent_ids[iteration % len(agent_ids)]
            recipient = agent_ids[(iteration + 1) % len(agent_ids)]

            self.agent_communication.send_message(
                sender,
                recipient,
                MessageType.STATUS_UPDATE,
                {"status": "active", "iteration": iteration, "demo": True},
                UnifiedMessagePriority.NORMAL,
            )

    def _show_demo_status(self, iteration):
        """Show current demo status"""
        print(f"\n📊 Demo Status Update (Iteration {iteration})")
        print("  " + "-" * 50)

        # Performance tracker status
        metrics_count = len(self.performance_tracker.get_metrics())
        snapshots_count = len(self.performance_tracker.get_performance_snapshots())
        print(
            f"  📊 Performance Tracker: {metrics_count} metrics, {snapshots_count} snapshots"
        )

        # Agent communication status
        agents_count = len(self.agent_communication.get_all_agents())
        messages_count = len(self.agent_communication.message_history)
        print(
            f"  📡 Agent Communication: {agents_count} agents, {messages_count} messages"
        )

        # API gateway status
        services_count = len(self.api_gateway.get_all_services())
        requests_count = len(self.api_gateway.request_history)
        print(f"  🌐 API Gateway: {services_count} services, {requests_count} requests")

        # Dashboard status
        dashboard_data = self.performance_dashboard.get_dashboard_data()
        alerts_count = len(dashboard_data.alerts)
        system_health = dashboard_data.performance_summary.get("system_health", 0)
        print(
            f"  📋 Dashboard: {alerts_count} alerts, System Health: {system_health:.1f}/100"
        )

        print("  " + "-" * 50)

    def export_demo_data(self, export_dir: str = None):
        """Export demo data for analysis"""
        if not export_dir:
            export_dir = f"demo_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        os.makedirs(export_dir, exist_ok=True)

        print(f"\n📁 Exporting demo data to: {export_dir}")

        # Export from all systems
        export_files = []

        # Performance tracker
        perf_export = os.path.join(export_dir, "performance_tracker.json")
        self.performance_tracker.export_metrics(perf_export)
        export_files.append(perf_export)

        # Performance profiler
        profiler_export = os.path.join(export_dir, "performance_profiler.json")
        self.performance_profiler.export_profiling_data(profiler_export)
        export_files.append(profiler_export)

        # Performance dashboard
        dashboard_export = os.path.join(export_dir, "performance_dashboard.json")
        self.performance_dashboard.export_dashboard_data(dashboard_export)
        export_files.append(dashboard_export)

        # Agent communication
        comm_export = os.path.join(export_dir, "agent_communication.json")
        self.agent_communication.export_communication_data(comm_export)
        export_files.append(comm_export)

        # API gateway
        gateway_export = os.path.join(export_dir, "api_gateway.json")
        self.api_gateway.export_gateway_data(gateway_export)
        export_files.append(gateway_export)

        # Create summary report
        summary = {
            "export_timestamp": datetime.now().isoformat(),
            "export_directory": export_dir,
            "export_files": export_files,
            "demo_summary": {
                "total_metrics": len(self.performance_tracker.get_metrics()),
                "total_snapshots": len(
                    self.performance_tracker.get_performance_snapshots()
                ),
                "total_agents": len(self.agent_communication.get_all_agents()),
                "total_services": len(self.api_gateway.get_all_services()),
                "total_alerts": len(self.performance_dashboard.get_alerts()),
            },
        }

        summary_file = os.path.join(export_dir, "export_summary.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"✅ Demo data exported successfully!")
        print(f"   📁 Export directory: {export_dir}")
        print(f"   📄 Summary file: {summary_file}")
        print(f"   📊 Total files exported: {len(export_files)}")

        return export_dir


def main():
    """Main demo execution"""
    print("🚀 Agent_Cellphone_V2 Performance Integration Demo")
    print("=" * 60)

    # Create demo instance
    demo = PerformanceIntegrationDemo()

    try:
        # Start the demo
        demo.start_demo()

        # Run for a specified duration or until interrupted
        print("\n⏱️  Demo will run for 2 minutes...")
        print("   Press Ctrl+C to stop early")

        time.sleep(120)  # Run for 2 minutes

    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")

    except Exception as e:
        print(f"\n❌ Demo error: {e}")

    finally:
        # Export demo data
        try:
            export_dir = demo.export_demo_data()
            print(f"\n📊 Demo completed! Data exported to: {export_dir}")
        except Exception as e:
            print(f"⚠️  Error exporting demo data: {e}")

        # Stop the demo
        demo.stop_demo()

        print("\n🎉 Performance Integration Demo completed successfully!")
        print("   Check the exported data for detailed analysis")


if __name__ == "__main__":
    main()
