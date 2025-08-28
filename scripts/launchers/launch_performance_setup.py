import logging
from pathlib import Path

from src.core.performance.monitoring.performance_monitor import PerformanceMonitor
from services.metrics_collector import (
    SystemMetricsCollector,
    ApplicationMetricsCollector,
    NetworkMetricsCollector,
    CustomMetricsCollector,
)
from services.dashboard_backend import DashboardBackend
from services.dashboard import (
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

logger = logging.getLogger(__name__)


def setup_performance_monitor(config: dict, config_file: str):
    """Initialize performance monitor and add collectors."""
    try:
        perf_monitor = PerformanceMonitor(config_file)
        collectors_config = config.get("performance_monitoring", {}).get("collectors", {})

        # System metrics collector
        if collectors_config.get("system_metrics", {}).get("enabled", True):
            sys_conf = collectors_config.get("system_metrics", {})
            system_collector = SystemMetricsCollector(
                collection_interval=sys_conf.get("collection_interval", 30)
            )
            system_collector.collect_cpu = sys_conf.get("collect_cpu", True)
            system_collector.collect_memory = sys_conf.get("collect_memory", True)
            system_collector.collect_disk = sys_conf.get("collect_disk", True)
            system_collector.collect_network = sys_conf.get("collect_network", True)
            perf_monitor.add_collector(system_collector)
            logger.info("System metrics collector added")

        # Application metrics collector
        if collectors_config.get("application_metrics", {}).get("enabled", True):
            app_conf = collectors_config.get("application_metrics", {})
            app_collector = ApplicationMetricsCollector(
                collection_interval=app_conf.get("collection_interval", 60)
            )
            perf_monitor.add_collector(app_collector)
            logger.info("Application metrics collector added")

        # Network metrics collector
        if collectors_config.get("network_metrics", {}).get("enabled", True):
            net_conf = collectors_config.get("network_metrics", {})
            network_collector = NetworkMetricsCollector(
                collection_interval=net_conf.get("collection_interval", 60)
            )
            for port in net_conf.get("monitored_ports", []):
                network_collector.add_monitored_port(port)
            perf_monitor.add_collector(network_collector)
            logger.info("Network metrics collector added")

        # Custom metrics collector
        if collectors_config.get("custom_metrics", {}).get("enabled", True):
            cust_conf = collectors_config.get("custom_metrics", {})
            custom_collector = CustomMetricsCollector(
                collection_interval=cust_conf.get("collection_interval", 120)
            )
            for metric_name in cust_conf.get("metrics", {}).keys():
                custom_collector.add_custom_metric(metric_name, lambda: 100.0)
            perf_monitor.add_collector(custom_collector)
            logger.info("Custom metrics collector added")

        return perf_monitor
    except Exception as e:
        logger.error("Failed to setup performance monitor: %s", e)
        return None


def setup_alerting_system(performance_monitor: PerformanceMonitor, config: dict):
    """Configure alerting system and attach to performance monitor."""
    try:
        alerting_config = config.get("performance_monitoring", {}).get("alerting", {})
        if not alerting_config.get("enabled", True):
            logger.info("Alerting system disabled")
            return None

        alerting_system = AlertingSystem()
        channels_config = alerting_config.get("channels", {})

        email_conf = channels_config.get("email", {})
        if email_conf.get("enabled", False):
            email_channel = EmailAlertChannel(
                name="email",
                recipients=email_conf.get("recipients", []),
                smtp_server=email_conf.get("smtp_server", "localhost"),
                smtp_port=email_conf.get("smtp_port", 587),
                username=email_conf.get("username"),
                password=email_conf.get("password"),
                use_tls=email_conf.get("use_tls", True),
                sender_email=email_conf.get("sender_email"),
            )
            email_channel.min_severity = getattr(
                type(performance_monitor).AlertSeverity,
                email_conf.get("min_severity", "WARNING").upper(),
            )
            email_channel.rate_limit_seconds = email_conf.get("rate_limit_seconds", 300)
            alerting_system.add_alert_channel(email_channel)
            logger.info("Email alert channel added")

        slack_conf = channels_config.get("slack", {})
        if slack_conf.get("enabled", False) and slack_conf.get("webhook_url"):
            slack_channel = SlackAlertChannel(
                name="slack",
                webhook_url=slack_conf.get("webhook_url"),
                channel=slack_conf.get("channel"),
                username=slack_conf.get("username", "AlertBot"),
                icon_emoji=slack_conf.get("icon_emoji", ":warning:"),
            )
            slack_channel.min_severity = getattr(
                type(performance_monitor).AlertSeverity,
                slack_conf.get("min_severity", "WARNING").upper(),
            )
            slack_channel.rate_limit_seconds = slack_conf.get("rate_limit_seconds", 180)
            alerting_system.add_alert_channel(slack_channel)
            logger.info("Slack alert channel added")

        discord_conf = channels_config.get("discord", {})
        if discord_conf.get("enabled", False) and discord_conf.get("webhook_url"):
            discord_channel = DiscordAlertChannel(
                name="discord",
                webhook_url=discord_conf.get("webhook_url"),
                username=discord_conf.get("username", "AlertBot"),
            )
            discord_channel.min_severity = getattr(
                type(performance_monitor).AlertSeverity,
                discord_conf.get("min_severity", "CRITICAL").upper(),
            )
            discord_channel.rate_limit_seconds = discord_conf.get("rate_limit_seconds", 120)
            alerting_system.add_alert_channel(discord_channel)
            logger.info("Discord alert channel added")

        pagerduty_conf = channels_config.get("pagerduty", {})
        if pagerduty_conf.get("enabled", False) and pagerduty_conf.get("integration_key"):
            pagerduty_channel = PagerDutyAlertChannel(
                name="pagerduty",
                integration_key=pagerduty_conf.get("integration_key"),
                api_url=pagerduty_conf.get(
                    "api_url", "https://events.pagerduty.com/v2/enqueue"
                ),
            )
            pagerduty_channel.min_severity = getattr(
                type(performance_monitor).AlertSeverity,
                pagerduty_conf.get("min_severity", "CRITICAL").upper(),
            )
            pagerduty_channel.rate_limit_seconds = pagerduty_conf.get(
                "rate_limit_seconds", 60
            )
            alerting_system.add_alert_channel(pagerduty_channel)
            logger.info("PagerDuty alert channel added")

        webhook_conf = channels_config.get("webhook", {})
        if webhook_conf.get("enabled", False) and webhook_conf.get("webhook_url"):
            webhook_channel = WebhookAlertChannel(
                name="webhook",
                webhook_url=webhook_conf.get("webhook_url"),
                method=webhook_conf.get("method", "POST"),
                headers=webhook_conf.get("headers", {}),
            )
            webhook_channel.min_severity = getattr(
                type(performance_monitor).AlertSeverity,
                webhook_conf.get("min_severity", "WARNING").upper(),
            )
            webhook_channel.rate_limit_seconds = webhook_conf.get(
                "rate_limit_seconds", 120
            )
            alerting_system.add_alert_channel(webhook_channel)
            logger.info("Webhook alert channel added")

        performance_monitor.alert_callbacks.append(alerting_system.process_alert)
        return alerting_system
    except Exception as e:
        logger.error("Failed to setup alerting system: %s", e)
        return None


def setup_dashboard(performance_monitor: PerformanceMonitor, config: dict):
    """Configure dashboard backend and frontend."""
    try:
        dashboard_config = config.get("performance_monitoring", {}).get("dashboard", {})
        if not dashboard_config.get("enabled", True):
            logger.info("Dashboard disabled")
            return None, None

        host = dashboard_config.get("host", "0.0.0.0")
        port = dashboard_config.get("port", 8080)
        dashboard_backend = DashboardBackend(
            performance_monitor=performance_monitor, host=host, port=port
        )

        websocket_url = f"ws://{host}:{port}/ws"
        dashboard_frontend = DashboardFrontend(websocket_url=websocket_url)
        layout = DashboardLayout(
            auto_refresh=dashboard_config.get("auto_refresh", True),
            refresh_interval=dashboard_config.get("refresh_interval", 5),
            theme=dashboard_config.get("theme", "dark"),
        )
        dashboard_frontend.set_layout(layout)

        for widget_config in dashboard_config.get("widgets", []):
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
            dashboard_frontend.add_widget(widget)

        html_content = dashboard_frontend.generate_html()
        static_dir = Path("static/dashboard")
        static_dir.mkdir(parents=True, exist_ok=True)
        with open(static_dir / "index.html", "w") as f:
            f.write(html_content)

        logger.info("Dashboard setup complete on http://%s:%s", host, port)
        return dashboard_backend, dashboard_frontend
    except Exception as e:
        logger.error("Failed to setup dashboard: %s", e)
        return None, None
