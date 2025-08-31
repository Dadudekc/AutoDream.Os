"""
launch_performance_setup_part_4.py
Module: launch_performance_setup_part_4.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:00
"""

# Part 4 of launch_performance_setup.py
# Original file: .\scripts\launchers\launch_performance_setup.py

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
        """
        setup_dashboard
        
        Purpose: Automated function documentation
        """
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

