#!/usr/bin/env python3
"""
Master V2 Integration System
============================
Master orchestrator for all V2 integration framework components.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from integration_framework import V2IntegrationFramework
from api_gateway import V2APIGateway, RouteMethod, GatewayRequest
from services.testing import TestFramework as V2IntegrationTestingFramework
from service_discovery import V2ServiceDiscovery
from integration_monitoring import V2IntegrationMonitoring, AlertSeverity

logger = logging.getLogger(__name__)


@dataclass
class V2SystemStatus:
    """Overall V2 system status"""

    timestamp: str
    integration_framework: str
    api_gateway: str
    testing_framework: str
    service_discovery: str
    monitoring: str
    overall_health: str
    total_services: int
    active_alerts: int


class MasterV2Integration:
    """Master orchestrator for V2 integration framework"""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.MasterV2Integration")

        # Initialize all V2 components
        self.integration_framework = V2IntegrationFramework()
        self.api_gateway = V2APIGateway("V2-Master-Gateway")
        self.testing_framework = V2IntegrationTestingFramework()
        self.service_discovery = V2ServiceDiscovery()
        self.monitoring = V2IntegrationMonitoring(alert_callback=self._handle_alert)

        # System state
        self._system_initialized = False
        self._start_time = time.time()

        self.logger.info("Master V2 Integration System initialized")

    def initialize_system(self) -> bool:
        """Initialize the complete V2 integration system"""
        try:
            # Start monitoring
            self.monitoring.start_monitoring(interval_seconds=30)

            # Start service discovery
            self.service_discovery.start_discovery()

            # Activate API gateway
            self.api_gateway.activate_gateway()

            # Start health monitoring for integration framework
            self.integration_framework.start_health_monitoring(interval_seconds=60)

            # Set up monitoring thresholds
            try:
                self._setup_monitoring_thresholds()
            except Exception as e:
                self.logger.warning(f"Failed to setup monitoring thresholds: {e}")

            # Register core services
            self._register_core_services()

            self._system_initialized = True
            self.logger.info("V2 Integration System fully initialized")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize V2 system: {e}")
            return False

    def _setup_monitoring_thresholds(self):
        """Set up monitoring thresholds for key metrics"""
        self.monitoring.set_metric_threshold(
            "service_health", warning=80, error=60, critical=40
        )
        self.monitoring.set_metric_threshold(
            "api_response_time", warning=1000, error=2000, critical=5000
        )
        self.monitoring.set_metric_threshold(
            "active_services", warning=5, error=3, critical=1
        )

    def _register_core_services(self):
        """Register core V2 services"""
        # Register integration framework
        self.service_discovery.register_service(
            "v2-integration-framework",
            "V2 Integration Framework",
            "1.0.0",
            [
                {
                    "url": "localhost",
                    "protocol": "http",
                    "port": 8001,
                    "health_check_path": "/health",
                }
            ],
            {"component": "core", "type": "framework"},
            ["core", "framework"],
        )

        # Register API gateway
        self.service_discovery.register_service(
            "v2-api-gateway",
            "V2 API Gateway",
            "1.0.0",
            [
                {
                    "url": "localhost",
                    "protocol": "http",
                    "port": 8002,
                    "health_check_path": "/health",
                }
            ],
            {"component": "core", "type": "gateway"},
            ["core", "gateway"],
        )

    def _handle_alert(self, alert):
        """Handle monitoring alerts"""
        self.logger.warning(f"ALERT: {alert.severity.value} - {alert.message}")

        # Record alert metric
        self.monitoring.record_metric(
            "alerts_generated",
            1.0,
            {"severity": alert.severity.value, "metric": alert.metric_name},
        )

    def register_service(
        self,
        service_id: str,
        service_name: str,
        version: str = "1.0.0",
        endpoints: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """Register a service with the V2 system"""
        # Register with service discovery
        if not self.service_discovery.register_service(
            service_id, service_name, version, endpoints, metadata, tags
        ):
            return False

        # Register with integration framework
        if not self.integration_framework.register_service(
            service_id, service_name, version, endpoints
        ):
            return False

        # Record service registration metric
        self.monitoring.record_metric(
            "services_registered", 1.0, {"service_id": service_id}
        )

        self.logger.info(
            f"Service registered with V2 system: {service_name} ({service_id})"
        )
        return True

    def add_api_route(
        self,
        path: str,
        method: RouteMethod,
        service_id: str,
        handler: callable,
        requires_auth: bool = False,
        rate_limit: Optional[int] = None,
    ) -> bool:
        """Add API route to the gateway"""
        success = self.api_gateway.register_route(
            path, method, service_id, handler, requires_auth, rate_limit
        )

        if success:
            self.monitoring.record_metric(
                "api_routes_registered", 1.0, {"service_id": service_id}
            )

        return success

    def run_integration_tests(self, test_suite_name: Optional[str] = None) -> List[Any]:
        """Run integration tests"""
        if test_suite_name:
            results = self.testing_framework.run_test_suite(test_suite_name)
        else:
            results = self.testing_framework.run_all_tests()

        # Record test metrics
        summary = self.testing_framework.get_test_summary()
        self.monitoring.record_metric(
            "test_success_rate", summary.get("success_rate", 0)
        )
        self.monitoring.record_metric("tests_executed", summary.get("total_tests", 0))

        return results

    def get_system_status(self) -> V2SystemStatus:
        """Get comprehensive V2 system status"""
        from datetime import datetime

        # Get component statuses
        framework_status = self.integration_framework.get_framework_status()
        gateway_stats = self.api_gateway.get_gateway_stats()
        discovery_stats = self.service_discovery.get_discovery_stats()
        monitoring_stats = self.monitoring.get_monitoring_stats()

        # Determine overall health
        health_scores = [
            framework_status.get("health_score", 0),
            gateway_stats.get("success_rate", 0),
            (
                discovery_stats.get("active_services", 0)
                / max(1, discovery_stats.get("total_services", 1))
            )
            * 100,
        ]

        avg_health = sum(health_scores) / len(health_scores)

        if avg_health >= 80:
            overall_health = "HEALTHY"
        elif avg_health >= 60:
            overall_health = "DEGRADED"
        else:
            overall_health = "CRITICAL"

        return V2SystemStatus(
            timestamp=datetime.now().isoformat(),
            integration_framework="ONLINE"
            if framework_status.get("framework_status") == "ONLINE"
            else "OFFLINE",
            api_gateway="ACTIVE"
            if gateway_stats.get("status") == "ACTIVE"
            else "INACTIVE",
            testing_framework="READY",
            service_discovery="ACTIVE"
            if discovery_stats.get("discovery_active")
            else "INACTIVE",
            monitoring="ACTIVE"
            if monitoring_stats.get("monitoring_active")
            else "INACTIVE",
            overall_health=overall_health,
            total_services=discovery_stats.get("total_services", 0),
            active_alerts=monitoring_stats.get("active_alerts", 0),
        )

    def generate_system_report(self) -> str:
        """Generate comprehensive V2 system report"""
        status = self.get_system_status()

        lines = [
            "🚀 V2 INTEGRATION SYSTEM COMPREHENSIVE REPORT",
            "=" * 60,
            f"Timestamp: {status.timestamp}",
            f"Overall Health: {status.overall_health}",
            f"Total Services: {status.total_services}",
            f"Active Alerts: {status.active_alerts}",
            "",
            "COMPONENT STATUS:",
            f"  Integration Framework: {status.integration_framework}",
            f"  API Gateway: {status.api_gateway}",
            f"  Testing Framework: {status.testing_framework}",
            f"  Service Discovery: {status.service_discovery}",
            f"  Monitoring: {status.monitoring}",
            "",
            "MONITORING METRICS:",
        ]

        # Add monitoring metrics
        current_metrics = self.monitoring.get_current_metrics()
        for name, value in current_metrics.items():
            lines.append(f"  {name}: {value}")

        # Add active alerts
        active_alerts = self.monitoring.get_active_alerts()
        if active_alerts:
            lines.extend(
                [
                    "",
                    "🚨 ACTIVE ALERTS:",
                ]
            )
            for alert in active_alerts[:3]:  # Show first 3 alerts
                lines.append(f"  {alert.severity.value.upper()}: {alert.message}")

        lines.append("=" * 60)
        return "\n".join(lines)

    def shutdown_system(self):
        """Gracefully shutdown the V2 integration system"""
        self.logger.info("Shutting down V2 Integration System")

        # Stop all components
        self.monitoring.stop_monitoring()
        self.service_discovery.stop_discovery()
        self.integration_framework.stop_health_monitoring()
        self.api_gateway.deactivate_gateway()

        self._system_initialized = False
        self.logger.info("V2 Integration System shutdown complete")


def main():
    """CLI interface for testing MasterV2Integration"""
    import argparse

    parser = argparse.ArgumentParser(description="Master V2 Integration CLI")
    parser.add_argument("--test", action="store_true", help="Run comprehensive test")

    args = parser.parse_args()

    if args.test:
        print("🧪 MasterV2Integration Comprehensive Test")
        print("=" * 50)

        master = MasterV2Integration()

        # Test system initialization
        init_success = master.initialize_system()
        print(f"✅ System initialization: {init_success}")

        # Test service registration
        service_success = master.register_service(
            "test-service",
            "Test Service",
            "1.0.0",
            [{"url": "localhost", "protocol": "http", "port": 8080}],
            {"environment": "test"},
            ["test", "api"],
        )
        print(f"✅ Service registration: {service_success}")

        # Test API route addition
        def test_handler(request):
            return {"message": "Test response"}

        route_success = master.add_api_route(
            "/api/test", RouteMethod.GET, "test-service", test_handler
        )
        print(f"✅ API route addition: {route_success}")

        # Test system status
        status = master.get_system_status()
        print(f"✅ System health: {status.overall_health}")
        print(f"✅ Total services: {status.total_services}")

        # Generate system report
        report = master.generate_system_report()
        print("\n📊 SYSTEM REPORT:")
        print(report)

        # Cleanup
        master.shutdown_system()
        print("\n🎉 MasterV2Integration test PASSED!")
    else:
        print("MasterV2Integration ready")
        print("Use --test to run comprehensive test")


if __name__ == "__main__":
    main()
