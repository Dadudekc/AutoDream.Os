#!/usr/bin/env python3
"""
Performance Monitoring Launcher Script for Agent_Cellphone_V2_Repository
Main launcher for the performance monitoring and dashboard system.
"""

import argparse
import asyncio
import json
import logging
import os
import signal
import sys
import time
from pathlib import Path
from typing import Optional

# Add src to path for imports
current_dir = Path(__file__).parent.parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from services.performance_monitor import PerformanceMonitor
    from services.metrics_collector import (
        SystemMetricsCollector,
        ApplicationMetricsCollector,
        NetworkMetricsCollector,
        CustomMetricsCollector,
    )
    from services.dashboard_backend import DashboardBackend
    from services.dashboard_frontend import (
        DashboardFrontend,
        DashboardWidget,
        ChartType,
        DashboardLayout,
    )
    from services.performance_alerting import (
        AlertingSystem,
        EmailAlertChannel,
        SlackAlertChannel,
        WebhookAlertChannel,
        DiscordAlertChannel,
        PagerDutyAlertChannel,
    )
except ImportError as e:
    print(f"Error importing performance monitoring modules: {e}")
    print("Please ensure all required dependencies are installed:")
    print("pip install -r requirements_integration.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class PerformanceMonitoringLauncher:
    """Main launcher for the performance monitoring system."""

    def __init__(self, config_file: str = "config/performance_monitoring_config.json"):
        self.config_file = config_file
        self.config = {}
        self.performance_monitor: Optional[PerformanceMonitor] = None
        self.dashboard_backend: Optional[DashboardBackend] = None
        self.dashboard_frontend: Optional[DashboardFrontend] = None
        self.alerting_system: Optional[AlertingSystem] = None
        self.running = False
        self.startup_time = time.time()

        # Graceful shutdown handling
        self.shutdown_event = asyncio.Event()
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.info("Performance monitoring launcher initialized")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating graceful shutdown")
        self.shutdown_event.set()

    def load_config(self):
        """Load configuration from file."""
        try:
            config_path = Path(self.config_file)
            if not config_path.exists():
                logger.error(f"Configuration file not found: {self.config_file}")
                return False

            with open(config_path, "r") as f:
                self.config = json.load(f)

            # Expand environment variables
            self._expand_env_vars(self.config)

            logger.info(f"Configuration loaded from {self.config_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False

    def _expand_env_vars(self, obj):
        """Recursively expand environment variables in configuration."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self._expand_env_vars(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                obj[i] = self._expand_env_vars(item)
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            env_var = obj[2:-1]
            obj = os.getenv(env_var, obj)

        return obj

    def setup_performance_monitor(self) -> bool:
        """Set up the performance monitoring system."""
        try:
            perf_config = self.config.get("performance_monitoring", {})

            # Initialize performance monitor
            self.performance_monitor = PerformanceMonitor(self.config_file)

            # Add collectors
            collectors_config = perf_config.get("collectors", {})

            # System metrics collector
            if collectors_config.get("system_metrics", {}).get("enabled", True):
                system_collector = SystemMetricsCollector(
                    collection_interval=collectors_config.get("system_metrics", {}).get(
                        "collection_interval", 30
                    )
                )

                # Configure what to collect
                sys_config = collectors_config.get("system_metrics", {})
                system_collector.collect_cpu = sys_config.get("collect_cpu", True)
                system_collector.collect_memory = sys_config.get("collect_memory", True)
                system_collector.collect_disk = sys_config.get("collect_disk", True)
                system_collector.collect_network = sys_config.get(
                    "collect_network", True
                )

                self.performance_monitor.add_collector(system_collector)
                logger.info("System metrics collector added")

            # Application metrics collector
            if collectors_config.get("application_metrics", {}).get("enabled", True):
                app_collector = ApplicationMetricsCollector(
                    collection_interval=collectors_config.get(
                        "application_metrics", {}
                    ).get("collection_interval", 60)
                )
                self.performance_monitor.add_collector(app_collector)
                logger.info("Application metrics collector added")

            # Network metrics collector
            if collectors_config.get("network_metrics", {}).get("enabled", True):
                network_collector = NetworkMetricsCollector(
                    collection_interval=collectors_config.get(
                        "network_metrics", {}
                    ).get("collection_interval", 60)
                )

                # Add monitored ports
                monitored_ports = collectors_config.get("network_metrics", {}).get(
                    "monitored_ports", []
                )
                for port in monitored_ports:
                    network_collector.add_monitored_port(port)

                self.performance_monitor.add_collector(network_collector)
                logger.info("Network metrics collector added")

            # Custom metrics collector
            if collectors_config.get("custom_metrics", {}).get("enabled", True):
                custom_collector = CustomMetricsCollector(
                    collection_interval=collectors_config.get("custom_metrics", {}).get(
                        "collection_interval", 120
                    )
                )

                # Add custom metrics (these would be implemented in the main application)
                custom_metrics = collectors_config.get("custom_metrics", {}).get(
                    "metrics", {}
                )
                for metric_name, metric_config in custom_metrics.items():
                    # For now, add placeholder functions
                    custom_collector.add_custom_metric(metric_name, lambda: 100.0)

                self.performance_monitor.add_collector(custom_collector)
                logger.info("Custom metrics collector added")

            return True

        except Exception as e:
            logger.error(f"Failed to setup performance monitor: {e}")
            return False

    def setup_alerting_system(self) -> bool:
        """Set up the alerting system."""
        try:
            alerting_config = self.config.get("performance_monitoring", {}).get(
                "alerting", {}
            )

            if not alerting_config.get("enabled", True):
                logger.info("Alerting system disabled")
                return True

            self.alerting_system = AlertingSystem()

            # Add alert channels
            channels_config = alerting_config.get("channels", {})

            # Email channel
            email_config = channels_config.get("email", {})
            if email_config.get("enabled", False):
                email_channel = EmailAlertChannel(
                    name="email",
                    recipients=email_config.get("recipients", []),
                    smtp_server=email_config.get("smtp_server", "localhost"),
                    smtp_port=email_config.get("smtp_port", 587),
                    username=email_config.get("username"),
                    password=email_config.get("password"),
                    use_tls=email_config.get("use_tls", True),
                    sender_email=email_config.get("sender_email"),
                )
                email_channel.min_severity = getattr(
                    type(self.performance_monitor).AlertSeverity,
                    email_config.get("min_severity", "WARNING").upper(),
                )
                email_channel.rate_limit_seconds = email_config.get(
                    "rate_limit_seconds", 300
                )
                self.alerting_system.add_alert_channel(email_channel)
                logger.info("Email alert channel added")

            # Slack channel
            slack_config = channels_config.get("slack", {})
            if slack_config.get("enabled", False) and slack_config.get("webhook_url"):
                slack_channel = SlackAlertChannel(
                    name="slack",
                    webhook_url=slack_config.get("webhook_url"),
                    channel=slack_config.get("channel"),
                    username=slack_config.get("username", "AlertBot"),
                    icon_emoji=slack_config.get("icon_emoji", ":warning:"),
                )
                slack_channel.min_severity = getattr(
                    type(self.performance_monitor).AlertSeverity,
                    slack_config.get("min_severity", "WARNING").upper(),
                )
                slack_channel.rate_limit_seconds = slack_config.get(
                    "rate_limit_seconds", 180
                )
                self.alerting_system.add_alert_channel(slack_channel)
                logger.info("Slack alert channel added")

            # Discord channel
            discord_config = channels_config.get("discord", {})
            if discord_config.get("enabled", False) and discord_config.get(
                "webhook_url"
            ):
                discord_channel = DiscordAlertChannel(
                    name="discord",
                    webhook_url=discord_config.get("webhook_url"),
                    username=discord_config.get("username", "AlertBot"),
                )
                discord_channel.min_severity = getattr(
                    type(self.performance_monitor).AlertSeverity,
                    discord_config.get("min_severity", "CRITICAL").upper(),
                )
                discord_channel.rate_limit_seconds = discord_config.get(
                    "rate_limit_seconds", 120
                )
                self.alerting_system.add_alert_channel(discord_channel)
                logger.info("Discord alert channel added")

            # PagerDuty channel
            pagerduty_config = channels_config.get("pagerduty", {})
            if pagerduty_config.get("enabled", False) and pagerduty_config.get(
                "integration_key"
            ):
                pagerduty_channel = PagerDutyAlertChannel(
                    name="pagerduty",
                    integration_key=pagerduty_config.get("integration_key"),
                    api_url=pagerduty_config.get(
                        "api_url", "https://events.pagerduty.com/v2/enqueue"
                    ),
                )
                pagerduty_channel.min_severity = getattr(
                    type(self.performance_monitor).AlertSeverity,
                    pagerduty_config.get("min_severity", "CRITICAL").upper(),
                )
                pagerduty_channel.rate_limit_seconds = pagerduty_config.get(
                    "rate_limit_seconds", 60
                )
                self.alerting_system.add_alert_channel(pagerduty_channel)
                logger.info("PagerDuty alert channel added")

            # Webhook channel
            webhook_config = channels_config.get("webhook", {})
            if webhook_config.get("enabled", False) and webhook_config.get(
                "webhook_url"
            ):
                webhook_channel = WebhookAlertChannel(
                    name="webhook",
                    webhook_url=webhook_config.get("webhook_url"),
                    method=webhook_config.get("method", "POST"),
                    headers=webhook_config.get("headers", {}),
                )
                webhook_channel.min_severity = getattr(
                    type(self.performance_monitor).AlertSeverity,
                    webhook_config.get("min_severity", "WARNING").upper(),
                )
                webhook_channel.rate_limit_seconds = webhook_config.get(
                    "rate_limit_seconds", 120
                )
                self.alerting_system.add_alert_channel(webhook_channel)
                logger.info("Webhook alert channel added")

            # Connect alerting to performance monitor
            self.performance_monitor.alert_callbacks.append(
                self.alerting_system.process_alert
            )

            return True

        except Exception as e:
            logger.error(f"Failed to setup alerting system: {e}")
            return False

    def setup_dashboard(self) -> bool:
        """Set up the dashboard backend and frontend."""
        try:
            dashboard_config = self.config.get("performance_monitoring", {}).get(
                "dashboard", {}
            )

            if not dashboard_config.get("enabled", True):
                logger.info("Dashboard disabled")
                return True

            # Setup dashboard backend
            host = dashboard_config.get("host", "0.0.0.0")
            port = dashboard_config.get("port", 8080)

            self.dashboard_backend = DashboardBackend(
                performance_monitor=self.performance_monitor, host=host, port=port
            )

            # Setup dashboard frontend
            websocket_url = f"ws://{host}:{port}/ws"
            self.dashboard_frontend = DashboardFrontend(websocket_url=websocket_url)

            # Configure layout
            layout = DashboardLayout(
                auto_refresh=dashboard_config.get("auto_refresh", True),
                refresh_interval=dashboard_config.get("refresh_interval", 5),
                theme=dashboard_config.get("theme", "dark"),
            )
            self.dashboard_frontend.set_layout(layout)

            # Add widgets from configuration
            widgets_config = dashboard_config.get("widgets", [])
            for widget_config in widgets_config:
                widget = DashboardWidget(
                    widget_id=widget_config["id"],
                    title=widget_config["title"],
                    chart_type=ChartType(widget_config["chart_type"]),
                    metric_name=widget_config["metric_name"],
                    width=widget_config.get("width", 6),
                    height=widget_config.get("height", 4),
                    position_x=widget_config.get("position_x", 0),
                    position_y=widget_config.get("position_y", 0),
                    time_range=widget_config.get("time_range", 3600),
                    aggregation=widget_config.get("aggregation", "raw"),
                    options=widget_config.get("options", {}),
                    filters=widget_config.get("filters", {}),
                )
                self.dashboard_frontend.add_widget(widget)

            # Generate and save dashboard HTML
            html_content = self.dashboard_frontend.generate_html()
            static_dir = Path("static/dashboard")
            static_dir.mkdir(parents=True, exist_ok=True)

            with open(static_dir / "index.html", "w") as f:
                f.write(html_content)

            logger.info(f"Dashboard setup complete on http://{host}:{port}")
            return True

        except Exception as e:
            logger.error(f"Failed to setup dashboard: {e}")
            return False

    async def start_system(self) -> bool:
        """Start the performance monitoring system."""
        try:
            logger.info("Starting performance monitoring system...")

            # Start performance monitor
            if self.performance_monitor:
                await self.performance_monitor.start()
                logger.info("Performance monitor started")

            # Start dashboard backend
            if self.dashboard_backend:
                await self.dashboard_backend.start()
                logger.info("Dashboard backend started")

            self.running = True
            logger.info("Performance monitoring system started successfully")

            # Print startup summary
            self._print_startup_summary()

            return True

        except Exception as e:
            logger.error(f"Failed to start system: {e}")
            return False

    async def stop_system(self):
        """Stop the performance monitoring system."""
        try:
            logger.info("Stopping performance monitoring system...")

            self.running = False

            # Stop performance monitor
            if self.performance_monitor:
                await self.performance_monitor.stop()
                logger.info("Performance monitor stopped")

            # Stop dashboard backend
            if self.dashboard_backend:
                await self.dashboard_backend.stop()
                logger.info("Dashboard backend stopped")

            logger.info("Performance monitoring system stopped successfully")

        except Exception as e:
            logger.error(f"Error stopping system: {e}")

    def _print_startup_summary(self):
        """Print startup summary information."""
        uptime = time.time() - self.startup_time

        print("\n" + "=" * 60)
        print("🚀 Performance Monitoring System Started")
        print("=" * 60)

        if self.performance_monitor:
            print(f"✅ Performance Monitor: Running")
            print(f"   - Collectors: {len(self.performance_monitor.collectors)}")
            print(f"   - Alert Rules: {len(self.performance_monitor.alert_rules)}")
            print(
                f"   - Collection Interval: {self.performance_monitor.collection_interval}s"
            )

        if self.dashboard_backend:
            print(f"✅ Dashboard Backend: Running")
            print(f"   - Host: {self.dashboard_backend.host}")
            print(f"   - Port: {self.dashboard_backend.port}")
            print(
                f"   - URL: http://{self.dashboard_backend.host}:{self.dashboard_backend.port}"
            )

        if self.dashboard_frontend:
            print(f"✅ Dashboard Frontend: Ready")
            print(f"   - Widgets: {len(self.dashboard_frontend.widgets)}")
            print(f"   - Theme: {self.dashboard_frontend.layout.theme}")
            print(f"   - Auto Refresh: {self.dashboard_frontend.layout.auto_refresh}")

        if self.alerting_system:
            print(f"✅ Alerting System: Active")
            print(f"   - Channels: {len(self.alerting_system.alert_channels)}")
            print(f"   - Rules: {len(self.alerting_system.alert_rules)}")

        print(f"\n📊 System Status:")
        print(f"   - Startup Time: {uptime:.2f}s")
        print(f"   - Configuration: {self.config_file}")
        print(f"   - Process ID: {os.getpid()}")

        print(f"\n🔗 Quick Links:")
        if self.dashboard_backend:
            print(
                f"   - Dashboard: http://{self.dashboard_backend.host}:{self.dashboard_backend.port}"
            )
            print(
                f"   - Health Check: http://{self.dashboard_backend.host}:{self.dashboard_backend.port}/api/health"
            )
            print(
                f"   - Metrics API: http://{self.dashboard_backend.host}:{self.dashboard_backend.port}/api/metrics"
            )

        print("\n💡 Usage:")
        print("   - Press Ctrl+C to stop gracefully")
        print("   - Monitor logs for real-time status")
        print("   - Access dashboard for visual monitoring")

        print("=" * 60 + "\n")

    async def get_system_status(self) -> dict:
        """Get current system status."""
        status = {
            "running": self.running,
            "uptime": time.time() - self.startup_time,
            "components": {},
        }

        if self.performance_monitor:
            status["components"][
                "performance_monitor"
            ] = self.performance_monitor.get_system_status()

        if self.dashboard_backend:
            status["components"]["dashboard_backend"] = {
                "running": self.dashboard_backend.running,
                "host": self.dashboard_backend.host,
                "port": self.dashboard_backend.port,
                "websocket_connections": len(
                    self.dashboard_backend.websocket_handler.connections
                ),
            }

        if self.alerting_system:
            status["components"]["alerting_system"] = {
                "channels": len(self.alerting_system.alert_channels),
                "rules": len(self.alerting_system.alert_rules),
                "active_alerts": len(self.alerting_system.active_alerts),
            }

        return status

    async def get_health_status(self) -> dict:
        """Get health check status."""
        health = {
            "status": "healthy" if self.running else "unhealthy",
            "timestamp": time.time(),
            "uptime": time.time() - self.startup_time,
            "checks": {},
        }

        # Check performance monitor
        if self.performance_monitor:
            health["checks"]["performance_monitor"] = {
                "status": "healthy"
                if self.performance_monitor.running
                else "unhealthy",
                "collectors": len(self.performance_monitor.collectors),
                "metrics_count": len(
                    self.performance_monitor.metrics_storage.get_all_metric_names()
                ),
            }

        # Check dashboard backend
        if self.dashboard_backend:
            health["checks"]["dashboard_backend"] = {
                "status": "healthy" if self.dashboard_backend.running else "unhealthy",
                "port": self.dashboard_backend.port,
                "connections": len(
                    self.dashboard_backend.websocket_handler.connections
                ),
            }

        # Check alerting system
        if self.alerting_system:
            health["checks"]["alerting_system"] = {
                "status": "healthy",
                "channels": len(self.alerting_system.alert_channels),
                "active_alerts": len(self.alerting_system.active_alerts),
            }

        return health

    async def run_main_loop(self):
        """Run the main application loop."""
        try:
            logger.info("Entering main loop...")

            # Wait for shutdown signal
            await self.shutdown_event.wait()

            logger.info("Shutdown signal received")

        except Exception as e:
            logger.error(f"Error in main loop: {e}")

        finally:
            await self.stop_system()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Performance Monitoring System for Agent_Cellphone_V2_Repository"
    )

    parser.add_argument(
        "action",
        choices=["start", "stop", "restart", "status", "health"],
        help="Action to perform",
    )

    parser.add_argument(
        "--config",
        default="config/performance_monitoring_config.json",
        help="Configuration file path (default: config/performance_monitoring_config.json)",
    )

    parser.add_argument(
        "--daemon", action="store_true", help="Run in daemon mode (background)"
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # Set logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    launcher = PerformanceMonitoringLauncher(args.config)

    if args.action == "start":
        # Load configuration
        if not launcher.load_config():
            sys.exit(1)

        # Setup components
        if not launcher.setup_performance_monitor():
            sys.exit(1)

        if not launcher.setup_alerting_system():
            sys.exit(1)

        if not launcher.setup_dashboard():
            sys.exit(1)

        # Start system
        if not await launcher.start_system():
            sys.exit(1)

        # Run main loop
        await launcher.run_main_loop()

    elif args.action == "status":
        # Get status (would typically connect to running instance)
        print("Performance Monitoring System Status")
        print("=" * 40)
        print("Status: Not implemented for remote status check")
        print("Use the dashboard or health endpoint for live status")

    elif args.action == "health":
        # Get health status (would typically connect to running instance)
        print("Performance Monitoring System Health")
        print("=" * 40)
        print("Health: Not implemented for remote health check")
        print("Use the /api/health endpoint for live health status")

    else:
        print(f"Action '{args.action}' not implemented")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
