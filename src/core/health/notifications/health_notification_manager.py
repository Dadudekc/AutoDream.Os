#!/usr/bin/env python3
"""
Health Notification Manager - V2 Modular Architecture
===================================================

Handles health notifications through various channels.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from threading import Lock

from ..types.health_types import HealthAlert, NotificationConfig, NotificationChannel


logger = logging.getLogger(__name__)


class HealthNotificationManager:
    """
    Health Notification Manager - Single responsibility: Send health notifications
    
    Handles all notification operations including:
    - Multi-channel notification delivery
    - Notification scheduling
    - Channel configuration management
    - Notification history tracking
    """

    def __init__(self):
        """Initialize health notification manager"""
        self.logger = logging.getLogger(f"{__name__}.HealthNotificationManager")
        
        # Notification configurations
        self.notification_configs: Dict[str, NotificationConfig] = {}
        
        # Notification history
        self.notification_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        
        # Thread safety
        self._lock = Lock()
        
        # Setup default notifications
        self._setup_default_notifications()
        
        self.logger.info("✅ Health Notification Manager initialized successfully")

    def _setup_default_notifications(self):
        """Setup default notification configurations"""
        try:
            # Email notifications
            email_config = NotificationConfig(
                channel=NotificationChannel.EMAIL,
                enabled=True,
                recipients=["admin@example.com"],
                config={
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "health@example.com",
                    "password": "password"
                },
                schedule={"enabled": True, "start_time": "09:00", "end_time": "18:00"}
            )
            self.notification_configs["email"] = email_config
            
            # Log notifications
            log_config = NotificationConfig(
                channel=NotificationChannel.LOG,
                enabled=True,
                recipients=[],
                config={},
                schedule={"enabled": True}
            )
            self.notification_configs["log"] = log_config
            
            # Webhook notifications
            webhook_config = NotificationConfig(
                channel=NotificationChannel.WEBHOOK,
                enabled=False,
                recipients=[],
                config={
                    "webhook_url": "https://api.example.com/webhook",
                    "custom_headers": {"Authorization": "Bearer token"}
                },
                schedule={"enabled": True}
            )
            self.notification_configs["webhook"] = webhook_config
            
        except Exception as e:
            self.logger.error(f"Failed to setup default notifications: {e}")

    def add_notification_config(self, name: str, config: NotificationConfig) -> bool:
        """Add a new notification configuration"""
        try:
            with self._lock:
                self.notification_configs[name] = config
                self.logger.info(f"Added notification config: {name}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to add notification config {name}: {e}")
            return False

    def update_notification_config(self, name: str, config: NotificationConfig) -> bool:
        """Update an existing notification configuration"""
        try:
            with self._lock:
                if name in self.notification_configs:
                    self.notification_configs[name] = config
                    self.logger.info(f"Updated notification config: {name}")
                    return True
                else:
                    self.logger.warning(f"Notification config not found: {name}")
                    return False
        except Exception as e:
            self.logger.error(f"Failed to update notification config {name}: {e}")
            return False

    def remove_notification_config(self, name: str) -> bool:
        """Remove a notification configuration"""
        try:
            with self._lock:
                if name in self.notification_configs:
                    del self.notification_configs[name]
                    self.logger.info(f"Removed notification config: {name}")
                    return True
                return False
        except Exception as e:
            self.logger.error(f"Failed to remove notification config {name}: {e}")
            return False

    def get_notification_config(self, name: str) -> Optional[NotificationConfig]:
        """Get a notification configuration"""
        try:
            with self._lock:
                return self.notification_configs.get(name)
        except Exception as e:
            self.logger.error(f"Failed to get notification config {name}: {e}")
            return None

    def get_all_notification_configs(self) -> Dict[str, NotificationConfig]:
        """Get all notification configurations"""
        try:
            with self._lock:
                return self.notification_configs.copy()
        except Exception as e:
            self.logger.error(f"Failed to get all notification configs: {e}")
            return {}

    def send_notification(self, alert: HealthAlert, config_name: Optional[str] = None) -> bool:
        """Send notification for a health alert"""
        try:
            if config_name:
                # Send to specific config
                config = self.get_notification_config(config_name)
                if config and config.enabled:
                    return self._send_single_notification(alert, config)
                else:
                    self.logger.warning(f"Notification config {config_name} not found or disabled")
                    return False
            else:
                # Send to all enabled configs
                success_count = 0
                total_count = 0
                
                for name, config in self.notification_configs.items():
                    if config.enabled and self._is_notification_scheduled(config):
                        total_count += 1
                        if self._send_single_notification(alert, config):
                            success_count += 1
                
                # Record notification attempt
                self._record_notification(alert, success_count, total_count)
                
                return success_count > 0
                
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            return False

    def _send_single_notification(self, alert: HealthAlert, config: NotificationConfig) -> bool:
        """Send notification through a single channel"""
        try:
            if config.channel == NotificationChannel.EMAIL:
                return self._send_email_notification(alert, config)
            elif config.channel == NotificationChannel.LOG:
                return self._send_log_notification(alert, config)
            elif config.channel == NotificationChannel.WEBHOOK:
                return self._send_webhook_notification(alert, config)
            elif config.channel == NotificationChannel.SLACK:
                return self._send_slack_notification(alert, config)
            elif config.channel == NotificationChannel.DISCORD:
                return self._send_discord_notification(alert, config)
            else:
                self.logger.warning(f"Unsupported notification channel: {config.channel}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send {config.channel.value} notification: {e}")
            return False

    def _send_email_notification(self, alert: HealthAlert, config: NotificationConfig) -> bool:
        """Send email notification"""
        try:
            subject = f"HEALTH ALERT: {alert.level.value.upper()} - {alert.message}"
            body = f"""
            Health Alert Notification
            
            Alert ID: {alert.id}
            Level: {alert.level.value}
            Message: {alert.message}
            Metric: {alert.metric_name}
            Value: {alert.metric_value}
            Threshold: {alert.threshold}
            Time: {alert.timestamp}
            """
            
            self.logger.info(f"Email notification would be sent: {subject}")
            
            # In production, implement actual email sending logic
            # For now, just log the notification
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {e}")
            return False

    def _send_log_notification(self, alert: HealthAlert, config: NotificationConfig) -> bool:
        """Send log notification"""
        try:
            log_level = logging.WARNING
            if alert.level.value == "critical":
                log_level = logging.ERROR
            elif alert.level.value == "emergency":
                log_level = logging.CRITICAL
            
            self.logger.log(log_level, f"HEALTH ALERT: {alert.message}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send log notification: {e}")
            return False

    def _send_webhook_notification(self, alert: HealthAlert, config: NotificationConfig) -> bool:
        """Send webhook notification"""
        try:
            webhook_url = config.config.get('webhook_url')
            if not webhook_url:
                self.logger.warning("No webhook URL configured")
                return False
            
            # Prepare webhook payload
            payload = {
                "alert_id": alert.id,
                "level": alert.level.value,
                "message": alert.message,
                "metric_name": alert.metric_name,
                "metric_value": alert.metric_value,
                "threshold": alert.threshold,
                "timestamp": alert.timestamp,
                "source": "health_manager"
            }
            
            # In production, implement actual webhook sending logic
            # For now, just log the notification
            self.logger.info(f"Webhook notification would be sent to {webhook_url}: {payload}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send webhook notification: {e}")
            return False

    def _send_slack_notification(self, alert: HealthAlert, config: NotificationConfig) -> bool:
        """Send Slack notification"""
        try:
            # In production, implement actual Slack notification logic
            self.logger.info(f"Slack notification would be sent: {alert.message}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
            return False

    def _send_discord_notification(self, alert: HealthAlert, config: NotificationConfig) -> bool:
        """Send Discord notification"""
        try:
            # In production, implement actual Discord notification logic
            self.logger.info(f"Discord notification would be sent: {alert.message}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Discord notification: {e}")
            return False

    def _is_notification_scheduled(self, config: NotificationConfig) -> bool:
        """Check if notification is within scheduled time window"""
        try:
            if not config.schedule.get("enabled", True):
                return True
            
            current_time = datetime.now().time()
            start_time = datetime.strptime(config.schedule.get("start_time", "00:00"), "%H:%M").time()
            end_time = datetime.strptime(config.schedule.get("end_time", "23:59"), "%H:%M").time()
            
            return start_time <= current_time <= end_time
            
        except Exception as e:
            self.logger.error(f"Failed to check notification schedule: {e}")
            return True

    def _record_notification(self, alert: HealthAlert, success_count: int, total_count: int):
        """Record notification attempt in history"""
        try:
            with self._lock:
                notification_record = {
                    "timestamp": datetime.now().isoformat(),
                    "alert_id": alert.id,
                    "alert_level": alert.level.value,
                    "success_count": success_count,
                    "total_count": total_count,
                    "success_rate": success_count / total_count if total_count > 0 else 0.0
                }
                
                self.notification_history.append(notification_record)
                
                # Keep only recent history
                if len(self.notification_history) > self.max_history:
                    self.notification_history = self.notification_history[-self.max_history:]
                    
        except Exception as e:
            self.logger.error(f"Failed to record notification: {e}")

    def get_notification_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get notification history"""
        try:
            with self._lock:
                return self.notification_history[-limit:]
        except Exception as e:
            self.logger.error(f"Failed to get notification history: {e}")
            return []

    def get_notification_statistics(self) -> Dict[str, Any]:
        """Get notification statistics"""
        try:
            with self._lock:
                if not self.notification_history:
                    return {"total_notifications": 0, "success_rate": 0.0}
                
                total_notifications = len(self.notification_history)
                successful_notifications = sum(
                    1 for record in self.notification_history
                    if record.get("success_rate", 0) > 0.5
                )
                
                success_rate = successful_notifications / total_notifications if total_notifications > 0 else 0.0
                
                return {
                    "total_notifications": total_notifications,
                    "successful_notifications": successful_notifications,
                    "success_rate": round(success_rate, 3),
                    "last_notification": self.notification_history[-1]["timestamp"] if self.notification_history else None
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get notification statistics: {e}")
            return {"error": str(e)}

    def clear_notification_history(self):
        """Clear notification history"""
        try:
            with self._lock:
                self.notification_history.clear()
                self.logger.info("✅ Notification history cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear notification history: {e}")

    def test_notification_channel(self, config_name: str) -> bool:
        """Test a notification channel"""
        try:
            config = self.get_notification_config(config_name)
            if not config:
                self.logger.error(f"Notification config not found: {config_name}")
                return False
            
            # Create a test alert
            test_alert = HealthAlert(
                id="test_alert",
                type=None,  # Will be set by the manager
                level=None,  # Will be set by the manager
                component="test",
                message="This is a test notification",
                metric_name="test_metric",
                metric_value=0.0,
                threshold=0.0,
                timestamp=datetime.now().isoformat(),
                acknowledged=False,
                acknowledged_by=None,
                acknowledged_at=None,
                resolved=False,
                resolved_at=None,
                metadata={"test": True}
            )
            
            # Send test notification
            success = self._send_single_notification(test_alert, config)
            
            if success:
                self.logger.info(f"✅ Test notification sent successfully to {config_name}")
            else:
                self.logger.error(f"❌ Test notification failed for {config_name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to test notification channel {config_name}: {e}")
            return False

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.clear_notification_history()
            self.logger.info("✅ Health Notification Manager cleanup completed")
        except Exception as e:
            self.logger.error(f"Health Notification Manager cleanup failed: {e}")


