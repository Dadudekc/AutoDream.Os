#!/usr/bin/env python3
"""
HEALTH MONITOR CORE - V2 COMPLIANT MODULE
========================================

Core health monitoring functionality.
Extracted from swarm_health_monitor.py for V2 compliance.

Author: Agent-4 (Strategic Oversight & Emergency Intervention Manager)
License: MIT
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

from .health_metrics import (
    AgentHealthStatus,
    HealthCalculator,
    HealthMetric,
    SwarmHealthReport
)
from .heartbeat_verification import get_heartbeat_system
from .messaging_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
    UnifiedMessageTag
)
from .routing_tracer import get_routing_tracer
from .verified_messaging_service import get_verified_messaging_service

logger = logging.getLogger(__name__)

# SWARM AGENTS - Single source of truth
SWARM_AGENTS = [
    "Agent-1", "Agent-2", "Agent-3", "Agent-4",
    "Agent-5", "Agent-6", "Agent-7", "Agent-8"
]


class HealthMonitorCore:
    """Core health monitoring functionality."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize subsystems
        self.heartbeat_system = get_heartbeat_system()
        self.verified_messaging = get_verified_messaging_service()
        self.routing_tracer = get_routing_tracer()
        
        # Health data storage
        self.agent_health: Dict[str, AgentHealthStatus] = {}
        self.system_metrics: Dict[str, HealthMetric] = {}
        self.health_history: List[SwarmHealthReport] = []
        
        # Initialize agent health status
        self._initialize_agent_health()
    
    def _initialize_agent_health(self):
        """Initialize health status for all agents."""
        for agent in SWARM_AGENTS:
            self.agent_health[agent] = AgentHealthStatus(
                agent_id=agent,
                is_online=True,
                last_heartbeat=datetime.now(),
                response_time_ms=0.0,
                consecutive_failures=0,
                health_score=1.0,
                metrics={},
                status="healthy"
            )
    
    async def check_agent_health(self):
        """Check health of all agents."""
        for agent in SWARM_AGENTS:
            try:
                # Get heartbeat status
                heartbeat_status = self.heartbeat_system.get_agent_status(agent)
                
                if heartbeat_status:
                    # Update agent health
                    self.agent_health[agent].is_online = heartbeat_status.is_online
                    self.agent_health[agent].last_heartbeat = heartbeat_status.last_heartbeat
                    self.agent_health[agent].response_time_ms = heartbeat_status.response_time_ms
                    self.agent_health[agent].consecutive_failures = heartbeat_status.consecutive_failures
                    self.agent_health[agent].last_error = heartbeat_status.last_error
                    
                    # Calculate health score
                    health_score = HealthCalculator.calculate_agent_health_score(heartbeat_status)
                    self.agent_health[agent].health_score = health_score
                    
                    # Determine status
                    if heartbeat_status.is_online and health_score >= 0.8:
                        self.agent_health[agent].status = "healthy"
                    elif heartbeat_status.is_online and health_score >= 0.5:
                        self.agent_health[agent].status = "degraded"
                    elif heartbeat_status.is_online:
                        self.agent_health[agent].status = "critical"
                    else:
                        self.agent_health[agent].status = "offline"
                    
                    # Add response time metric
                    self.agent_health[agent].metrics["response_time"] = HealthMetric(
                        name="response_time",
                        value=heartbeat_status.response_time_ms,
                        unit="ms",
                        timestamp=datetime.now(),
                        threshold_warning=1000.0,
                        threshold_critical=5000.0,
                        status="healthy" if heartbeat_status.response_time_ms < 1000 else "warning"
                    )
                
            except Exception as e:
                self.logger.error(f"Failed to check health for {agent}: {e}")
                self.agent_health[agent].status = "offline"
                self.agent_health[agent].health_score = 0.0
    
    async def check_system_metrics(self):
        """Check system-wide metrics."""
        try:
            # Get messaging system health
            messaging_health = self.verified_messaging.get_system_health()
            
            # Add messaging success rate metric
            self.system_metrics["messaging_success_rate"] = HealthMetric(
                name="messaging_success_rate",
                value=messaging_health.get("message_success_rate", 0.0),
                unit="%",
                timestamp=datetime.now(),
                threshold_warning=0.95,
                threshold_critical=0.90,
                status="healthy" if messaging_health.get("message_success_rate", 0.0) >= 0.95 else "warning"
            )
            
            # Add average response time metric
            self.system_metrics["average_response_time"] = HealthMetric(
                name="average_response_time",
                value=messaging_health.get("average_response_time", 0.0),
                unit="ms",
                timestamp=datetime.now(),
                threshold_warning=100.0,
                threshold_critical=500.0,
                status="healthy" if messaging_health.get("average_response_time", 0.0) < 100 else "warning"
            )
            
            # Add agent availability metric
            online_agents = sum(1 for agent in SWARM_AGENTS if self.agent_health[agent].is_online)
            availability_ratio = online_agents / len(SWARM_AGENTS)
            
            self.system_metrics["agent_availability"] = HealthMetric(
                name="agent_availability",
                value=availability_ratio,
                unit="%",
                timestamp=datetime.now(),
                threshold_warning=0.8,
                threshold_critical=0.6,
                status="healthy" if availability_ratio >= 0.8 else "warning"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to check system metrics: {e}")
    
    async def check_routing_health(self):
        """Check routing system health."""
        try:
            # Get routing diagnostics
            routing_diagnostics = self.routing_tracer.get_routing_statistics()
            
            # Check routing success rate
            routing_success_rate = routing_diagnostics.get("success_rate", 0.0)
            
            self.system_metrics["routing_success_rate"] = HealthMetric(
                name="routing_success_rate",
                value=routing_success_rate,
                unit="%",
                timestamp=datetime.now(),
                threshold_warning=0.99,
                threshold_critical=0.95,
                status="healthy" if routing_success_rate >= 0.99 else "warning"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to check routing health: {e}")
    
    async def check_messaging_health(self):
        """Check messaging system health."""
        try:
            # Get messaging system health
            messaging_health = self.verified_messaging.get_system_health()
            
            # Check for routing table issues
            routing_table_status = messaging_health.get("routing_table_status", {})
            routing_issues = 0
            
            for agent, status in routing_table_status.items():
                if not status.get("coordinates_available", False):
                    routing_issues += 1
            
            if routing_issues > 0:
                self.system_metrics["routing_table_health"] = HealthMetric(
                    name="routing_table_health",
                    value=1.0 - (routing_issues / len(SWARM_AGENTS)),
                    unit="%",
                    timestamp=datetime.now(),
                    threshold_warning=0.9,
                    threshold_critical=0.7,
                    status="warning" if routing_issues <= 2 else "critical"
                )
            
        except Exception as e:
            self.logger.error(f"Failed to check messaging health: {e}")
    
    async def generate_health_report(self) -> SwarmHealthReport:
        """Generate comprehensive health report."""
        try:
            # Calculate overall health
            overall_health, health_score = HealthCalculator.calculate_overall_health(
                self.agent_health, self.system_metrics
            )
            
            # Get routing health
            routing_health = self.routing_tracer.get_routing_statistics()
            
            # Get messaging health
            messaging_health = self.verified_messaging.get_system_health()
            
            # Identify critical issues
            critical_issues = HealthCalculator.identify_critical_issues(
                self.agent_health, self.system_metrics
            )
            
            # Generate recommendations
            recommendations = HealthCalculator.generate_recommendations(critical_issues)
            
            return SwarmHealthReport(
                timestamp=datetime.now(),
                overall_health=overall_health,
                health_score=health_score,
                agent_statuses=self.agent_health.copy(),
                system_metrics=self.system_metrics.copy(),
                routing_health=routing_health,
                messaging_health=messaging_health,
                critical_issues=critical_issues,
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate health report: {e}")
            return SwarmHealthReport(
                timestamp=datetime.now(),
                overall_health="unknown",
                health_score=0.0,
                agent_statuses={},
                system_metrics={},
                routing_health={},
                messaging_health={},
                critical_issues=[f"Health report generation failed: {e}"],
                recommendations=["Investigate health monitoring system"]
            )
    
    async def check_critical_issues(self, report: SwarmHealthReport):
        """Check for critical issues and take action."""
        try:
            # Check for Agent-8 routing crisis
            if any("Agent-8" in issue for issue in report.critical_issues):
                await self._handle_agent8_crisis()
            
            # Check for system-wide issues
            if report.overall_health == "critical":
                await self._handle_system_crisis(report)
            
            # Check for degraded performance
            if report.overall_health == "degraded":
                await self._handle_performance_degradation(report)
            
        except Exception as e:
            self.logger.error(f"Failed to check critical issues: {e}")
    
    async def _handle_agent8_crisis(self):
        """Handle Agent-8 routing crisis."""
        try:
            self.logger.critical("🚨 AGENT-8 ROUTING CRISIS DETECTED!")
            
            # Send emergency alert to Captain
            emergency_message = UnifiedMessage(
                content="🚨 EMERGENCY: Agent-8 routing crisis detected! Immediate intervention required!",
                sender="SYSTEM",
                recipient="Agent-4",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.URGENT,
                tags=[UnifiedMessageTag.SYSTEM]
            )
            
            # Use verified messaging service
            success = await self.verified_messaging.send_message(emergency_message)
            
            if success:
                self.logger.info("Emergency alert sent to Captain")
            else:
                self.logger.error("Failed to send emergency alert to Captain")
            
        except Exception as e:
            self.logger.error(f"Failed to handle Agent-8 crisis: {e}")
    
    async def _handle_system_crisis(self, report: SwarmHealthReport):
        """Handle system-wide crisis."""
        try:
            self.logger.critical("🚨 SYSTEM CRISIS DETECTED!")
            
            # Send system-wide alert
            crisis_message = UnifiedMessage(
                content=f"🚨 SYSTEM CRISIS: Overall health is {report.overall_health}. Critical issues: {', '.join(report.critical_issues[:3])}",
                sender="SYSTEM",
                recipient="ALL_AGENTS",
                message_type=UnifiedMessageType.BROADCAST,
                priority=UnifiedMessagePriority.URGENT,
                tags=[UnifiedMessageTag.SYSTEM]
            )
            
            success = await self.verified_messaging.send_message(crisis_message)
            
            if success:
                self.logger.info("System crisis alert sent to all agents")
            else:
                self.logger.error("Failed to send system crisis alert")
            
        except Exception as e:
            self.logger.error(f"Failed to handle system crisis: {e}")
    
    async def _handle_performance_degradation(self, report: SwarmHealthReport):
        """Handle performance degradation."""
        try:
            self.logger.warning("⚠️ Performance degradation detected")
            
            # Log performance issues
            for metric_name, metric in report.system_metrics.items():
                if metric.status == "warning":
                    self.logger.warning(f"Performance warning: {metric_name} = {metric.value} {metric.unit}")
            
        except Exception as e:
            self.logger.error(f"Failed to handle performance degradation: {e}")
    
    def get_current_health(self) -> SwarmHealthReport:
        """Get current health status."""
        if self.health_history:
            return self.health_history[-1]
        else:
            # Generate initial report
            return SwarmHealthReport(
                timestamp=datetime.now(),
                overall_health="unknown",
                health_score=0.0,
                agent_statuses=self.agent_health.copy(),
                system_metrics=self.system_metrics.copy(),
                routing_health={},
                messaging_health={},
                critical_issues=["Health monitoring not yet initialized"],
                recommendations=["Initialize health monitoring system"]
            )
    
    def get_health_history(self, hours: int = 24) -> List[SwarmHealthReport]:
        """Get health history for specified hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [report for report in self.health_history if report.timestamp > cutoff_time]
    
    def store_health_report(self, report: SwarmHealthReport):
        """Store health report in history."""
        self.health_history.append(report)
        
        # Keep only last 100 reports
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]