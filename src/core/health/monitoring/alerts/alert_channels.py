#!/usr/bin/env python3
"""
Health Alert Channels - V2 Compliant
=====================================

Focused module for alert channel implementations.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
import smtplib
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AlertChannelType(Enum):
    """Supported alert channel types."""
    EMAIL = "email"
    SLACK = "slack"
    MESSAGING = "messaging"
    LOG = "log"
    WEBHOOK = "webhook"


@dataclass
class AlertChannelConfig:
    """Configuration for alert channels."""
    channel_type: AlertChannelType
    enabled: bool = True
    config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}


class AlertChannel(ABC):
    """Abstract base class for alert channels."""
    
    def __init__(self, config: AlertChannelConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def send_alert(self, alert: 'HealthAlert') -> bool:
        """Send alert through this channel."""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate channel configuration."""
        pass


class EmailAlertChannel(AlertChannel):
    """Email alert channel implementation."""
    
    def __init__(self, config: AlertChannelConfig):
        super().__init__(config)
        self.smtp_server = config.config.get('smtp_server', 'localhost')
        self.smtp_port = config.config.get('smtp_port', 587)
        self.username = config.config.get('username')
        self.password = config.config.get('password')
        self.from_email = config.config.get('from_email')
        self.to_emails = config.config.get('to_emails', [])
    
    async def send_alert(self, alert: 'HealthAlert') -> bool:
        """Send alert via email."""
        try:
            if not self.to_emails:
                self.logger.warning("No recipient emails configured")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            msg['Subject'] = f"[{alert.severity.value}] {alert.title}"
            
            body = f"""
Alert Details:
- Title: {alert.title}
- Severity: {alert.severity.value}
- Timestamp: {alert.timestamp}
- Component: {alert.component}
- Message: {alert.message}
- Metrics: {json.dumps(alert.metrics, indent=2)}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.username and self.password:
                    server.starttls()
                    server.login(self.username, self.password)
                server.send_message(msg)
            
            self.logger.info(f"Email alert sent for {alert.component}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
            return False
    
    def validate_config(self) -> bool:
        """Validate email configuration."""
        required_fields = ['smtp_server', 'from_email', 'to_emails']
        for field in required_fields:
            if not self.config.config.get(field):
                self.logger.error(f"Missing required email config: {field}")
                return False
        return True


class LogAlertChannel(AlertChannel):
    """Log-based alert channel implementation."""
    
    async def send_alert(self, alert: 'HealthAlert') -> bool:
        """Send alert to logs."""
        try:
            log_level = {
                'critical': logging.CRITICAL,
                'warning': logging.WARNING,
                'info': logging.INFO
            }.get(alert.severity.value.lower(), logging.INFO)
            
            self.logger.log(log_level, 
                f"HEALTH ALERT: {alert.title} | Component: {alert.component} | "
                f"Severity: {alert.severity.value} | Message: {alert.message}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to log alert: {e}")
            return False
    
    def validate_config(self) -> bool:
        """Log channel always valid."""
        return True


class SlackAlertChannel(AlertChannel):
    """Slack alert channel implementation."""
    
    def __init__(self, config: AlertChannelConfig):
        super().__init__(config)
        self.webhook_url = config.config.get('webhook_url')
        self.channel = config.config.get('channel', '#alerts')
    
    async def send_alert(self, alert: 'HealthAlert') -> bool:
        """Send alert to Slack."""
        try:
            import requests
            
            color_map = {
                'critical': '#ff0000',
                'warning': '#ffaa00',
                'info': '#00aa00'
            }
            
            payload = {
                "channel": self.channel,
                "attachments": [{
                    "color": color_map.get(alert.severity.value.lower(), '#cccccc'),
                    "title": f"[{alert.severity.value.upper()}] {alert.title}",
                    "fields": [
                        {"title": "Component", "value": alert.component, "short": True},
                        {"title": "Timestamp", "value": str(alert.timestamp), "short": True},
                        {"title": "Message", "value": alert.message, "short": False}
                    ]
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            self.logger.info(f"Slack alert sent for {alert.component}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    def validate_config(self) -> bool:
        """Validate Slack configuration."""
        if not self.webhook_url:
            self.logger.error("Missing Slack webhook URL")
            return False
        return True


class AlertChannelManager:
    """Manages multiple alert channels."""
    
    def __init__(self):
        self.channels: List[AlertChannel] = []
        self.logger = logging.getLogger(__name__)
    
    def add_channel(self, channel: AlertChannel) -> bool:
        """Add alert channel."""
        if channel.validate_config():
            self.channels.append(channel)
            self.logger.info(f"Added {channel.__class__.__name__} channel")
            return True
        else:
            self.logger.error(f"Failed to validate {channel.__class__.__name__} channel")
            return False
    
    async def send_alert(self, alert: 'HealthAlert') -> Dict[str, bool]:
        """Send alert through all configured channels."""
        results = {}
        
        for channel in self.channels:
            if not channel.config.enabled:
                continue
                
            try:
                success = await channel.send_alert(alert)
                results[channel.__class__.__name__] = success
            except Exception as e:
                self.logger.error(f"Channel {channel.__class__.__name__} failed: {e}")
                results[channel.__class__.__name__] = False
        
        return results
    
    def get_channel_status(self) -> Dict[str, bool]:
        """Get status of all channels."""
        return {
            channel.__class__.__name__: channel.config.enabled 
            for channel in self.channels
        }

