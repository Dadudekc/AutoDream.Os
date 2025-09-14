#!/usr/bin/env python3
"""
Health Alert Escalation - V2 Compliant
=======================================

Focused module for alert escalation policies and management.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class EscalationLevel(Enum):
    """Alert escalation levels."""
    IMMEDIATE = "immediate"
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    CRITICAL = "critical"


@dataclass
class EscalationPolicy:
    """Escalation policy configuration."""
    name: str
    component: str
    initial_level: EscalationLevel
    escalation_chain: List[EscalationLevel]
    time_thresholds: Dict[EscalationLevel, int]  # seconds
    max_escalations: int = 3
    cooldown_period: int = 300  # 5 minutes
    enabled: bool = True


@dataclass
class AlertInstance:
    """Individual alert instance for tracking."""
    alert_id: str
    component: str
    severity: str
    timestamp: datetime
    escalation_level: EscalationLevel
    escalation_count: int = 0
    last_escalation: Optional[datetime] = None
    acknowledged: bool = False
    resolved: bool = False


class AlertEscalationEngine:
    """Manages alert escalation logic and policies."""
    
    def __init__(self):
        self.policies: Dict[str, EscalationPolicy] = {}
        self.active_alerts: Dict[str, AlertInstance] = {}
        self.escalation_history: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)
        
        # Default escalation chain
        self.default_chain = [
            EscalationLevel.IMMEDIATE,
            EscalationLevel.LEVEL_1,
            EscalationLevel.LEVEL_2,
            EscalationLevel.CRITICAL
        ]
        
        # Default time thresholds (seconds)
        self.default_thresholds = {
            EscalationLevel.IMMEDIATE: 0,
            EscalationLevel.LEVEL_1: 300,    # 5 minutes
            EscalationLevel.LEVEL_2: 900,    # 15 minutes
            EscalationLevel.CRITICAL: 1800   # 30 minutes
        }
    
    def add_policy(self, policy: EscalationPolicy) -> bool:
        """Add escalation policy."""
        try:
            self.policies[policy.name] = policy
            self.logger.info(f"Added escalation policy: {policy.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add policy {policy.name}: {e}")
            return False
    
    def get_policy_for_component(self, component: str) -> Optional[EscalationPolicy]:
        """Get escalation policy for component."""
        for policy in self.policies.values():
            if policy.component == component and policy.enabled:
                return policy
        
        # Return default policy if none found
        return self._create_default_policy(component)
    
    def _create_default_policy(self, component: str) -> EscalationPolicy:
        """Create default escalation policy for component."""
        return EscalationPolicy(
            name=f"default_{component}",
            component=component,
            initial_level=EscalationLevel.IMMEDIATE,
            escalation_chain=self.default_chain,
            time_thresholds=self.default_thresholds
        )
    
    def process_alert(self, alert_id: str, component: str, severity: str) -> Optional[EscalationLevel]:
        """Process new alert and determine escalation level."""
        policy = self.get_policy_for_component(component)
        if not policy:
            self.logger.warning(f"No escalation policy found for {component}")
            return EscalationLevel.IMMEDIATE
        
        current_time = datetime.now()
        
        # Check if this is a new alert or escalation
        if alert_id in self.active_alerts:
            alert_instance = self.active_alerts[alert_id]
            
            # Check if we can escalate
            if self._can_escalate(alert_instance, policy, current_time):
                return self._escalate_alert(alert_instance, policy, current_time)
            else:
                return alert_instance.escalation_level
        else:
            # New alert
            alert_instance = AlertInstance(
                alert_id=alert_id,
                component=component,
                severity=severity,
                timestamp=current_time,
                escalation_level=policy.initial_level
            )
            self.active_alerts[alert_id] = alert_instance
            self.logger.info(f"New alert {alert_id} at level {policy.initial_level.value}")
            return policy.initial_level
    
    def _can_escalate(self, alert_instance: AlertInstance, policy: EscalationPolicy, current_time: datetime) -> bool:
        """Check if alert can be escalated."""
        # Check if already at max escalations
        if alert_instance.escalation_count >= policy.max_escalations:
            return False
        
        # Check cooldown period
        if alert_instance.last_escalation:
            time_since_escalation = (current_time - alert_instance.last_escalation).total_seconds()
            if time_since_escalation < policy.cooldown_period:
                return False
        
        # Check if enough time has passed for current level
        current_level_time = policy.time_thresholds.get(alert_instance.escalation_level, 0)
        time_since_alert = (current_time - alert_instance.timestamp).total_seconds()
        
        return time_since_alert >= current_level_time
    
    def _escalate_alert(self, alert_instance: AlertInstance, policy: EscalationPolicy, current_time: datetime) -> EscalationLevel:
        """Escalate alert to next level."""
        current_index = policy.escalation_chain.index(alert_instance.escalation_level)
        
        # Move to next level if available
        if current_index + 1 < len(policy.escalation_chain):
            new_level = policy.escalation_chain[current_index + 1]
        else:
            new_level = EscalationLevel.CRITICAL
        
        # Update alert instance
        alert_instance.escalation_level = new_level
        alert_instance.escalation_count += 1
        alert_instance.last_escalation = current_time
        
        # Log escalation
        escalation_record = {
            "alert_id": alert_instance.alert_id,
            "component": alert_instance.component,
            "old_level": policy.escalation_chain[current_index].value,
            "new_level": new_level.value,
            "escalation_count": alert_instance.escalation_count,
            "timestamp": current_time.isoformat()
        }
        self.escalation_history.append(escalation_record)
        
        self.logger.warning(
            f"Escalated alert {alert_instance.alert_id} to {new_level.value} "
            f"(escalation #{alert_instance.escalation_count})"
        )
        
        return new_level
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert to stop escalation."""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].acknowledged = True
            self.logger.info(f"Alert {alert_id} acknowledged")
            return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark alert as resolved."""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].resolved = True
            # Remove from active alerts after a delay
            asyncio.create_task(self._cleanup_resolved_alert(alert_id))
            self.logger.info(f"Alert {alert_id} resolved")
            return True
        return False
    
    async def _cleanup_resolved_alert(self, alert_id: str, delay: int = 3600):
        """Clean up resolved alert after delay."""
        await asyncio.sleep(delay)
        if alert_id in self.active_alerts and self.active_alerts[alert_id].resolved:
            del self.active_alerts[alert_id]
            self.logger.debug(f"Cleaned up resolved alert {alert_id}")
    
    def get_active_alerts(self) -> List[AlertInstance]:
        """Get all active alerts."""
        return [alert for alert in self.active_alerts.values() if not alert.resolved]
    
    def get_escalation_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get escalation history."""
        return self.escalation_history[-limit:]
    
    def get_component_stats(self, component: str) -> Dict[str, Any]:
        """Get escalation statistics for component."""
        component_alerts = [
            alert for alert in self.active_alerts.values() 
            if alert.component == component
        ]
        
        if not component_alerts:
            return {"total_alerts": 0, "escalation_rate": 0}
        
        total_escalations = sum(alert.escalation_count for alert in component_alerts)
        escalation_rate = total_escalations / len(component_alerts)
        
        return {
            "total_alerts": len(component_alerts),
            "total_escalations": total_escalations,
            "escalation_rate": escalation_rate,
            "avg_escalations": total_escalations / len(component_alerts)
        }

