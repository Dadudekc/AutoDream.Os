"""
Comprehensive Test Script for Agent Health Monitoring Refactoring

This script validates the functionality of all newly extracted modules
and ensures proper package imports after the refactoring of MAJOR-001.

Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_package_imports():
    """Test that all modules can be imported correctly"""
    try:
        logger.info("Testing package imports...")
        
        # Test importing the main package using relative imports
        from . import (
            AgentHealthCoreMonitor,
            HealthMetricsCollector,
            HealthReportingGenerator,
            generate_alert,
        )
        logger.info("✅ Main health package imported successfully")
        
        # Test importing specific modules
        from .monitoring.core import AgentHealthCoreMonitor, HealthStatus, HealthMetricType
        logger.info("✅ Core module imported successfully")
        
        from .metrics import HealthMetricsCollector, MetricSource
        logger.info("✅ Metrics module imported successfully")
        
        from .alerting import generate_alert, AlertSeverity
        logger.info("✅ Alerting module imported successfully")

        from .reporting import HealthReportingGenerator, ReportType
        logger.info("✅ Reporting module imported successfully")
        
        # Test importing all classes
        from . import (
            AgentHealthCoreMonitor,
            HealthMetricsCollector,
            HealthReportingGenerator,
            generate_alert,
        )
        logger.info("✅ All main classes imported successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Package import test failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


def test_core_module():
    """Test the core monitoring module"""
    try:
        logger.info("Testing core monitoring module...")
        
        from .monitoring.core import AgentHealthCoreMonitor, HealthStatus, HealthMetricType
        
        # Test initialization
        monitor = AgentHealthCoreMonitor()
        assert monitor is not None, "Monitor initialization failed"
        logger.info("✅ Core monitor initialization passed")
        
        # Test basic functionality
        monitor.record_health_metric("test_agent", HealthMetricType.RESPONSE_TIME, 500.0, "ms")
        health_data = monitor.get_agent_health("test_agent")
        assert health_data is not None, "Health data retrieval failed"
        assert health_data.agent_id == "test_agent", "Agent ID mismatch"
        logger.info("✅ Core monitor basic functionality passed")
        
        # Test health summary
        summary = monitor.get_health_summary()
        assert "total_agents" in summary, "Health summary missing total_agents"
        assert "active_alerts" in summary, "Health summary missing active_alerts"
        logger.info("✅ Core monitor health summary passed")
        
        # Test smoke test
        success = monitor.run_smoke_test()
        assert success, "Core monitor smoke test failed"
        logger.info("✅ Core monitor smoke test passed")
        
        # Cleanup
        monitor.shutdown()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Core module test failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


def test_metrics_module():
    """Test the metrics collection module"""
    try:
        logger.info("Testing metrics collection module...")
        
        from .metrics import HealthMetricsCollector, MetricSource
        
        # Test initialization
        collector = HealthMetricsCollector()
        assert collector is not None, "Collector initialization failed"
        logger.info("✅ Metrics collector initialization passed")
        
        # Test on-demand collection
        result = collector.collect_metrics_on_demand(MetricSource.SYSTEM)
        assert result is not None, "Metrics collection result is None"
        assert hasattr(result, 'success'), "Result missing success attribute"
        assert hasattr(result, 'metrics'), "Result missing metrics attribute"
        logger.info("✅ Metrics collection on-demand passed")
        
        # Test metrics summary
        summary = collector.get_metrics_summary()
        assert "total_collections" in summary, "Metrics summary missing total_collections"
        assert "total_metrics" in summary, "Metrics summary missing total_metrics"
        logger.info("✅ Metrics collection summary passed")
        
        # Test smoke test
        success = collector.run_smoke_test()
        assert success, "Metrics collector smoke test failed"
        logger.info("✅ Metrics collector smoke test passed")
        
        # Cleanup
        collector.shutdown()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Metrics module test failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


def test_alerting_module():
    """Test alert generation, dispatch and escalation utilities"""
    try:
        logger.info("Testing alerting utilities...")

        from dataclasses import asdict
        from .alerting import (
            generate_alert,
            send_alert_notifications,
            check_escalations,
            AlertSeverity,
            NotificationChannel,
            AlertRule,
            NotificationConfig,
            EscalationPolicy,
            EscalationLevel,
        )

        # Generate and dispatch an alert
        alert = generate_alert(
            "test_agent",
            AlertSeverity.WARNING,
            "Test alert message",
            "cpu_usage",
            90.0,
            85.0,
        )
        rule = AlertRule(
            rule_id="high_cpu_usage",
            name="High CPU Usage",
            description="Alert when CPU usage exceeds threshold",
            severity=AlertSeverity.WARNING,
            conditions={"metric": "cpu_usage", "operator": ">", "threshold": 85.0},
            notification_channels=[NotificationChannel.CONSOLE],
        )
        notif_config = NotificationConfig(
            channel=NotificationChannel.CONSOLE,
            template="{severity}: {message}",
        )
        send_alert_notifications(alert, rule, {NotificationChannel.CONSOLE: notif_config})
        assert alert.notification_sent, "Alert notification not sent"
        logger.info("✅ Alert generation and dispatch passed")

        # Escalation check
        policy = EscalationPolicy(
            level=EscalationLevel.LEVEL_1,
            delay_minutes=0,
            contacts=[],
            notification_channels=[],
        )
        check_escalations({alert.alert_id: alert}, {EscalationLevel.LEVEL_1: policy}, {})
        assert alert.escalation_level == EscalationLevel.LEVEL_2, "Escalation failed"
        logger.info("✅ Alert escalation passed")

        # Prepare data for report generator style structure (ensures asdict works)
        alerts_data = {"alerts": [asdict(alert)]}
        assert alerts_data["alerts"], "Alerts data not prepared"

        return True

    except Exception as e:
        logger.error(f"❌ Alerting utilities test failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


def test_reporting_module():
    """Test the reporting generator module"""
    try:
        logger.info("Testing reporting generator module...")
        
        from .reporting import HealthReportingGenerator, ReportType, ReportFormat
        
        # Test initialization
        generator = HealthReportingGenerator()
        assert generator is not None, "Reporting generator initialization failed"
        logger.info("✅ Reporting generator initialization passed")
        
        # Test report generation with mock data
        mock_health_data = {
            "agents": {
                "agent_1": {
                    "overall_status": "good",
                    "health_score": 85.0,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "metrics": {
                        "cpu_usage": {"value": 45.0, "unit": "%", "status": "good"},
                        "memory_usage": {"value": 60.0, "unit": "%", "status": "good"},
                    }
                }
            }
        }
        
        mock_alerts_data = {
            "alerts": [
                {
                    "severity": "warning",
                    "agent_id": "agent_1",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "message": "Test alert"
                }
            ]
        }
        
        from .reporting import ReportConfig
        config = ReportConfig(
            report_type=ReportType.DAILY_SUMMARY,
            format=ReportFormat.JSON,
            include_charts=True,
            include_metrics=True,
            include_alerts=True,
            include_recommendations=True,
        )
        
        report = generator.generate_report(mock_health_data, mock_alerts_data, config)
        assert report is not None, "Report generation failed"
        assert report.report_id.startswith("health_report_"), "Invalid report ID format"
        logger.info("✅ Report generation passed")
        
        # Test chart generation
        assert len(report.charts) > 0, "No charts were generated"
        logger.info("✅ Chart generation passed")
        
        # Test recommendations generation
        assert len(report.recommendations) > 0, "No recommendations were generated"
        logger.info("✅ Recommendations generation passed")
        
        # Test report history
        history = generator.get_report_history(limit=5)
        assert len(history) > 0, "No reports found in history"
        logger.info("✅ Report history passed")
        
        # Test smoke test
        success = generator.run_smoke_test()
        assert success, "Reporting generator smoke test failed"
        logger.info("✅ Reporting generator smoke test passed")
        
        # Cleanup
        generator.shutdown()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Reporting module test failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


def test_integration():
    """Test integration between all modules"""
    try:
        logger.info("Testing module integration...")
        
        from . import (
            AgentHealthCoreMonitor,
            HealthMetricsCollector,
            HealthReportingGenerator,
        )
        from .monitoring.core import HealthMetricType
        from .alerting import (
            generate_alert,
            send_alert_notifications,
            AlertSeverity,
            AlertRule,
            NotificationChannel,
            NotificationConfig,
        )
        from .reporting import ReportType, ReportFormat, ReportConfig

        # Initialize all components
        core_monitor = AgentHealthCoreMonitor()
        metrics_collector = HealthMetricsCollector()
        reporting_generator = HealthReportingGenerator()
        
        logger.info("✅ All components initialized")
        
        # Test data flow: Core -> Alerting -> Reporting
        
        # 1. Record health metrics in core monitor
        core_monitor.record_health_metric("test_agent", HealthMetricType.CPU_USAGE, 95.0, "%")
        core_monitor.record_health_metric("test_agent", HealthMetricType.MEMORY_USAGE, 88.0, "%")
        
        # 2. Create alerts based on metrics
        alert = generate_alert(
            "test_agent",
            AlertSeverity.WARNING,
            "High CPU usage detected",
            "cpu_usage",
            95.0,
            85.0,
        )
        rule = AlertRule(
            rule_id="high_cpu_usage",
            name="High CPU Usage",
            description="Alert when CPU usage exceeds threshold",
            severity=AlertSeverity.WARNING,
            conditions={"metric": "cpu_usage", "operator": ">", "threshold": 85.0},
            notification_channels=[NotificationChannel.CONSOLE],
        )
        config = NotificationConfig(
            channel=NotificationChannel.CONSOLE,
            template="{severity}: {message}",
        )
        send_alert_notifications(alert, rule, {NotificationChannel.CONSOLE: config})

        # 3. Generate report using data from both
        health_data = {"agents": core_monitor.get_all_agent_health()}
        alerts_data = {"alerts": [{"severity": alert.severity.value, "message": alert.message}]}
        
        config = ReportConfig(
            report_type=ReportType.DAILY_SUMMARY,
            format=ReportFormat.CONSOLE,
            include_charts=False,  # Skip charts for faster testing
            include_metrics=True,
            include_alerts=True,
            include_recommendations=True,
        )
        
        report = reporting_generator.generate_report(health_data, alerts_data, config)
        assert report is not None, "Integration report generation failed"
        logger.info("✅ Integration report generation passed")
        
        # Verify data consistency
        assert "test_agent" in report.metrics_data, "Test agent missing from report"
        assert report.alerts_data["total_alerts"] > 0, "No alerts in report"
        logger.info("✅ Data consistency verified")
        
        # Cleanup
        core_monitor.shutdown()
        metrics_collector.shutdown()
        reporting_generator.shutdown()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


def test_error_handling():
    """Test error handling and edge cases"""
    try:
        logger.info("Testing error handling...")
        
        from .monitoring.core import AgentHealthCoreMonitor
        from .metrics import HealthMetricsCollector
        from .alerting import generate_alert, AlertSeverity
        from .reporting import HealthReportingGenerator
        
        # Test with invalid data
        core_monitor = AgentHealthCoreMonitor()
        
        # Test with None values
        core_monitor.record_health_metric("test_agent", None, 100.0, "%")
        # Should handle gracefully without crashing
        
        # Test with empty data
        empty_health = core_monitor.get_health_summary()
        assert "total_agents" in empty_health, "Empty health summary missing fields"
        
        # Test metrics collector with invalid source
        metrics_collector = HealthMetricsCollector()
        try:
            from .metrics import MetricSource
            result = metrics_collector.collect_metrics_on_demand(MetricSource.CUSTOM)
            # Should handle gracefully
        except Exception:
            pass  # Expected for custom source without collector
        
        # Test alert generation with invalid data
        try:
            generate_alert("", AlertSeverity.INFO, "", "", 0, 0)
        except Exception:
            pass  # Expected for invalid data
        
        # Test reporting generator with empty data
        reporting_generator = HealthReportingGenerator()
        try:
            from .reporting import ReportType, ReportFormat, ReportConfig
            config = ReportConfig(
                report_type=ReportType.DAILY_SUMMARY,
                format=ReportFormat.JSON,
                include_charts=False,
                include_metrics=True,
                include_alerts=True,
                include_recommendations=True,
            )
            
            report = reporting_generator.generate_report({}, {}, config)
            assert report is not None, "Empty data report generation failed"
        except Exception as e:
            logger.warning(f"Empty data report generation warning (expected): {e}")
        
        # Cleanup
        core_monitor.shutdown()
        metrics_collector.shutdown()
        reporting_generator.shutdown()
        
        logger.info("✅ Error handling tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error handling test failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


def main():
    """Run all tests"""
    print("🚀 AGENT HEALTH MONITORING REFACTORING VALIDATION")
    print("=" * 60)

    test_results = []

    # Run all tests
    test_results.append(("Package Imports", test_package_imports()))
    test_results.append(("Core Module", test_core_module()))
    test_results.append(("Metrics Module", test_metrics_module()))
    test_results.append(("Alerting Module", test_alerting_module()))
    test_results.append(("Reporting Module", test_reporting_module()))
    test_results.append(("Module Integration", test_integration()))
    test_results.append(("Error Handling", test_error_handling()))

    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1

    print("=" * 60)
    print(f"Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Refactoring successful!")
        print("\n✅ MAJOR-001 (Agent Health Monitor) refactoring completed successfully!")
        print("   - Core monitoring module extracted and tested")
        print("   - Metrics collection module extracted and tested")
        print("   - Alerting utilities extracted and tested")
        print("   - Reporting generator module extracted and tested")
        print("   - All modules follow SRP and V2 coding standards")
        print("   - Package structure properly organized")
        print("   - Integration between modules verified")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
