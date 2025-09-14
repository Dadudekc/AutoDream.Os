#!/usr/bin/env python3
"""
Health Alerting System - V2 Compliant Main Coordinator
=====================================================

Consolidated health alerting system coordinating all alert components.
V2 COMPLIANT: Under 300 lines, focused orchestration responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from .alert_channels import AlertChannelManager, AlertChannelType, AlertChannelConfig, EmailAlertChannel, LogAlertChannel, SlackAlertChannel
from .alert_escalation import AlertEscalationEngine, EscalationLevel

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class HealthAlert:
    """Health alert data structure."""
    alert_id: str
    title: str
    message: str
    component: str
    severity: AlertSeverity
    timestamp: datetime
    metrics: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}


class HealthAlertingSystem:
    """Main health alerting system coordinator."""
    
    def __init__(self):
        self.channel_manager = AlertChannelManager()
        self.escalation_engine = AlertEscalationEngine()
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._alert_queue = asyncio.Queue()
        
        # Statistics
        self.stats = {
            "alerts_sent": 0,
            "alerts_failed": 0,
            "escalations": 0,
            "start_time": None
        }
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize alerting system with configuration."""
        try:
            # Configure channels
            await self._configure_channels(config.get("channels", []))
            
            # Configure escalation policies
            self._configure_escalation_policies(config.get("escalation_policies", []))
            
            self.stats["start_time"] = datetime.now()
            self.logger.info("Health alerting system initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize alerting system: {e}")
            return False
    
    async def _configure_channels(self, channel_configs: List[Dict[str, Any]]) -> None:
        """Configure alert channels."""
        for config in channel_configs:
            try:
                channel_type = AlertChannelType(config["type"])
                channel_config = AlertChannelConfig(
                    channel_type=channel_type,
                    enabled=config.get("enabled", True),
                    config=config.get("config", {})
                )
                
                if channel_type == AlertChannelType.EMAIL:
                    channel = EmailAlertChannel(channel_config)
                elif channel_type == AlertChannelType.LOG:
                    channel = LogAlertChannel(channel_config)
                elif channel_type == AlertChannelType.SLACK:
                    channel = SlackAlertChannel(channel_config)
                else:
                    self.logger.warning(f"Unsupported channel type: {channel_type}")
                    continue
                
                self.channel_manager.add_channel(channel)
                
            except Exception as e:
                self.logger.error(f"Failed to configure channel {config}: {e}")
    
    def _configure_escalation_policies(self, policy_configs: List[Dict[str, Any]]) -> None:
        """Configure escalation policies."""
        for config in policy_configs:
            try:
                from .alert_escalation import EscalationPolicy
                
                policy = EscalationPolicy(
                    name=config["name"],
                    component=config["component"],
                    initial_level=EscalationLevel(config.get("initial_level", "immediate")),
                    escalation_chain=[EscalationLevel(level) for level in config.get("escalation_chain", [])],
                    time_thresholds={EscalationLevel(k): v for k, v in config.get("time_thresholds", {}).items()},
                    max_escalations=config.get("max_escalations", 3),
                    cooldown_period=config.get("cooldown_period", 300),
                    enabled=config.get("enabled", True)
                )
                
                self.escalation_engine.add_policy(policy)
                
            except Exception as e:
                self.logger.error(f"Failed to configure escalation policy {config}: {e}")
    
    async def start(self) -> None:
        """Start the alerting system."""
        if self._running:
            return
        
        self._running = True
        self.logger.info("Starting health alerting system")
        
        # Start background tasks
        asyncio.create_task(self._process_alert_queue())
    
    async def stop(self) -> None:
        """Stop the alerting system."""
        self._running = False
        self.logger.info("Stopping health alerting system")
    
    async def send_alert(self, title: str, message: str, component: str, 
                        severity: AlertSeverity, metrics: Optional[Dict[str, Any]] = None) -> str:
        """Send a health alert."""
        try:
            alert_id = str(uuid.uuid4())
            
            # Create alert
            alert = HealthAlert(
                alert_id=alert_id,
                title=title,
                message=message,
                component=component,
                severity=severity,
                timestamp=datetime.now(),
                metrics=metrics or {}
            )
            
            # Queue for processing
            await self._alert_queue.put(alert)
            
            self.logger.debug(f"Queued alert {alert_id} for {component}")
            return alert_id
            
        except Exception as e:
            self.logger.error(f"Failed to queue alert: {e}")
            raise
    
    async def _process_alert_queue(self) -> None:
        """Process alerts from the queue."""
        while self._running:
            try:
                # Get alert from queue with timeout
                alert = await asyncio.wait_for(self._alert_queue.get(), timeout=1.0)
                
                # Process escalation
                escalation_level = self.escalation_engine.process_alert(
                    alert.alert_id, alert.component, alert.severity.value
                )
                
                # Send through channels
                results = await self.channel_manager.send_alert(alert)
                
                # Update statistics
                if any(results.values()):
                    self.stats["alerts_sent"] += 1
                else:
                    self.stats["alerts_failed"] += 1
                
                if escalation_level != EscalationLevel.IMMEDIATE:
                    self.stats["escalations"] += 1
                
                self.logger.info(f"Processed alert {alert.alert_id} at level {escalation_level.value}")
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Error processing alert queue: {e}")
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        return self.escalation_engine.acknowledge_alert(alert_id)
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        return self.escalation_engine.resolve_alert(alert_id)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and statistics."""
        return {
            "running": self._running,
            "queue_size": self._alert_queue.qsize(),
            "active_alerts": len(self.escalation_engine.get_active_alerts()),
            "channels": self.channel_manager.get_channel_status(),
            "statistics": self.stats.copy(),
            "uptime": (datetime.now() - self.stats["start_time"]).total_seconds() if self.stats["start_time"] else 0
        }
    
    def get_component_stats(self, component: str) -> Dict[str, Any]:
        """Get statistics for a specific component."""
        return self.escalation_engine.get_component_stats(component)
    
    def get_escalation_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get escalation history."""
        return self.escalation_engine.get_escalation_history(limit)

