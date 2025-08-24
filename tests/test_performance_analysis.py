import asyncio
import json
import os
import time
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_module_from_file(module_name: str, file_path: str):
    """Load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def test_alerting_system_standalone():
    """Test alerting system in standalone mode."""
    print("\n🚨 Testing Alerting System Standalone")
    print("=" * 35)

    try:
        perf_monitor_path = "src/services/performance_monitor.py"
        perf_monitor_module = load_module_from_file(
            "performance_monitor", perf_monitor_path
        )

        alerting_path = "src/services/performance_alerting.py"
        alerting_module = load_module_from_file("performance_alerting", alerting_path)

        AlertingSystem = alerting_module.AlertingSystem
        AlertRule = alerting_module.AlertRule
        EmailAlertChannel = alerting_module.EmailAlertChannel
        SlackAlertChannel = alerting_module.SlackAlertChannel
        WebhookAlertChannel = alerting_module.WebhookAlertChannel

        AlertCondition = perf_monitor_module.AlertCondition
        AlertSeverity = perf_monitor_module.AlertSeverity
        PerformanceAlert = perf_monitor_module.PerformanceAlert

        alerting = AlertingSystem()
        print("✅ Alerting system created")

        rules = [
            AlertRule(
                name="High CPU Usage",
                metric_name="cpu_usage_percent",
                condition=AlertCondition.GREATER_THAN,
                threshold=85.0,
                severity=AlertSeverity.WARNING,
                description="CPU usage is above 85%",
            ),
            AlertRule(
                name="Critical Memory Usage",
                metric_name="memory_usage_percent",
                condition=AlertCondition.GREATER_THAN,
                threshold=95.0,
                severity=AlertSeverity.CRITICAL,
                description="Memory usage is critically high",
            ),
            AlertRule(
                name="Low Disk Space",
                metric_name="disk_usage_percent",
                condition=AlertCondition.GREATER_THAN,
                threshold=90.0,
                severity=AlertSeverity.WARNING,
                description="Disk space is running low",
            ),
        ]

        for rule in rules:
            alerting.add_alert_rule(rule)

        if len(alerting.alert_rules) == 3:
            print(f"✅ Alert rules added: {len(alerting.alert_rules)}")
            for rule in alerting.alert_rules:
                print(
                    f"   - {rule.name}: {rule.metric_name} {rule.condition.value} {rule.threshold}"
                )
        else:
            print("❌ Alert rule addition failed")
            return False

        channels = [
            EmailAlertChannel(
                name="test_email",
                recipients=["admin@example.com"],
                smtp_server="localhost",
                smtp_port=25,
            ),
            SlackAlertChannel(
                name="test_slack",
                webhook_url="https://hooks.slack.com/services/test",
                channel="#alerts",
            ),
            WebhookAlertChannel(
                name="test_webhook",
                webhook_url="https://api.example.com/alerts",
                method="POST",
            ),
        ]

        for channel in channels:
            channel.enabled = False
            alerting.add_alert_channel(channel)

        if len(alerting.alert_channels) == 3:
            print(f"✅ Alert channels added: {len(alerting.alert_channels)}")
            for channel in alerting.alert_channels:
                print(f"   - {channel.name}: {channel.__class__.__name__}")
        else:
            print("❌ Alert channel addition failed")
            return False

        test_alert = PerformanceAlert(
            alert_id="test_001",
            rule_name="High CPU Usage",
            metric_name="cpu_usage_percent",
            current_value=87.5,
            threshold=85.0,
            severity=AlertSeverity.WARNING,
            message="CPU usage is 87.5%, which exceeds the threshold of 85%",
            timestamp=time.time(),
            tags={"host": "test-server", "service": "test"},
        )

        results = await alerting.process_alert(test_alert)

        print("✅ Alert processing completed")
        print(f"   - Alert ID: {test_alert.alert_id}")
        print(f"   - Rule: {test_alert.rule_name}")
        print(f"   - Severity: {test_alert.severity.value}")
        print(f"   - Processing results: {results}")

        if alerting.alert_manager:
            history = alerting.alert_manager.get_alert_history(limit=5)
            print(f"✅ Alert history: {len(history)} alerts")

            active_channels = alerting.alert_manager.get_active_channels()
            print(f"✅ Active channels: {len(active_channels)} channels")

        return True

    except Exception as e:
        print(f"❌ Alerting system test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_configuration_standalone():
    """Test configuration loading."""
    print("\n⚙️ Testing Configuration Loading")
    print("=" * 30)

    try:
        config_file = "config/system/performance.json"

        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
            print("✅ Configuration file loaded successfully")

            perf_config = config.get("performance_monitoring", {})
            if perf_config:
                print("✅ Performance monitoring configuration found")

                sections = ["collectors", "dashboard", "alerting"]
                for section in sections:
                    if section in perf_config:
                        print(f"   - {section}: ✅")
                    else:
                        print(f"   - {section}: ❌")

                print(f"\nConfiguration Summary:")
                print(f"   - Version: {perf_config.get('version', 'N/A')}")
                print(
                    f"   - Collection Interval: {perf_config.get('collection_interval', 'N/A')}s"
                )
                print(
                    f"   - Retention Period: {perf_config.get('retention_period', 'N/A')}s"
                )

                dashboard_config = perf_config.get("dashboard", {})
                print(f"   - Dashboard Port: {dashboard_config.get('port', 'N/A')}")
                print(f"   - Dashboard Theme: {dashboard_config.get('theme', 'N/A')}")

                alerting_config = perf_config.get("alerting", {})
                rules = alerting_config.get("rules", [])
                channels = alerting_config.get("channels", {})
                print(f"   - Alert Rules: {len(rules)}")
                print(f"   - Alert Channels: {len(channels)}")

            else:
                print("❌ Performance monitoring configuration missing")
                return False

            return True
        else:
            print(f"⚠️ Configuration file not found: {config_file}")
            return False

    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False
