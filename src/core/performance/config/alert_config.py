#!/usr/bin/env python3
"""
Alert Configuration - V2 Modular Architecture
=============================================

Alert system configuration and channel management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertChannelType(Enum):
    """Alert channel types."""
    CONSOLE = "console"
    LOG = "log"
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"


@dataclass
class AlertChannel:
    """Alert channel configuration."""
    channel_type: AlertChannelType
    name: str
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_configured(self) -> bool:
        """Check if channel is properly configured."""
        if not self.enabled:
            return False
        
        # Basic validation based on channel type
        if self.channel_type == AlertChannelType.EMAIL:
            return "recipients" in self.config
        elif self.channel_type == AlertChannelType.SLACK:
            return "webhook_url" in self.config
        elif self.channel_type == AlertChannelType.WEBHOOK:
            return "url" in self.config
        
        return True


@dataclass
class AlertConfig:
    """Alert system configuration."""
    enabled: bool = True
    severity_minimum: AlertSeverity = AlertSeverity.WARNING
    channels: List[AlertChannel] = field(default_factory=list)
    cooldown_seconds: int = 300  # 5 minutes
    max_alerts_per_hour: int = 100
    alert_retention_days: int = 7
    
    def get_enabled_channels(self) -> List[AlertChannel]:
        """Get all enabled alert channels."""
        return [channel for channel in self.channels if channel.enabled]
    
    def get_channels_by_type(self, channel_type: AlertChannelType) -> List[AlertChannel]:
        """Get channels of specific type."""
        return [channel for channel in self.channels 
                if channel.channel_type == channel_type and channel.enabled]
    
    def add_channel(self, channel: AlertChannel):
        """Add a new alert channel."""
        self.channels.append(channel)
    
    def remove_channel(self, channel_name: str):
        """Remove alert channel by name."""
        self.channels = [c for c in self.channels if c.name != channel_name]
    
    def validate_config(self) -> List[str]:
        """Validate alert configuration."""
        errors = []
        if self.cooldown_seconds < 0:
            errors.append("Alert cooldown must be non-negative")
        if self.max_alerts_per_hour <= 0:
            errors.append("Max alerts per hour must be positive")
        if self.alert_retention_days <= 0:
            errors.append("Alert retention must be positive")
        
        # Validate channels
        for channel in self.channels:
            if not channel.is_configured():
                errors.append(f"Channel {channel.name} is not properly configured")
        
        return errors
