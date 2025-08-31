"""
launch_performance_setup_part_2.py
Module: launch_performance_setup_part_2.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:00
"""

# Part 2 of launch_performance_setup.py
# Original file: .\scripts\launchers\launch_performance_setup.py

    except Exception as e:
        logger.error("Failed to setup performance monitor: %s", e)
        return None


def setup_alerting_system(performance_monitor: PerformanceMonitor, config: dict):
        """
        setup_alerting_system
        
        Purpose: Automated function documentation
        """
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

