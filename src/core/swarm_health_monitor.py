#!/usr/bin/env python3
"""
SWARM HEALTH MONITOR - COMPREHENSIVE MONITORING SYSTEM
=====================================================

Implements comprehensive swarm health monitoring system as outlined in THEA's guidance.
Part of the emergency routing patch and crisis response implementation.

Author: Agent-4 (Strategic Oversight & Emergency Intervention Manager)
License: MIT
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .messaging_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
    UnifiedMessageTag,
    get_messaging_core
)
from .verified_messaging_service import get_verified_messaging_service
from .routing_tracer import get_routing_tracer
from .heartbeat_verification import get_heartbeat_system

logger = logging.getLogger(__name__)

# SWARM AGENTS - Single source of truth
SWARM_AGENTS = [
    "Agent-1", "Agent-2", "Agent-3", "Agent-4",
    "Agent-5", "Agent-6", "Agent-7", "Agent-8"
]


@dataclass
class HealthMetric:
    """Health metric data structure."""
    name: str
    value: float
    unit: str
    timestamp: datetime
    threshold_warning: float
    threshold_critical: float
    status: str  # healthy, warning, critical


@dataclass
class AgentHealthStatus:
    """Agent health status data structure."""
    agent_id: str
    is_online: bool
    last_heartbeat: datetime
    response_time_ms: float
    consecutive_failures: int
    health_score: float  # 0.0 to 1.0
    metrics: Dict[str, HealthMetric]
    status: str  # healthy, degraded, critical, offline
    last_error: Optional[str] = None


@dataclass
class SwarmHealthReport:
    """Comprehensive swarm health report."""
    timestamp: datetime
    overall_health: str
    health_score: float
    agent_statuses: Dict[str, AgentHealthStatus]
    system_metrics: Dict[str, HealthMetric]
    routing_health: Dict[str, Any]
    messaging_health: Dict[str, Any]
    critical_issues: List[str]
    recommendations: List[str]


class SwarmHealthMonitor:
    """Comprehensive swarm health monitoring system."""
    
    def __init__(self, monitoring_interval: int = 30):
        self.logger = logging.getLogger(__name__)
        self.monitoring_interval = monitoring_interval
        
        # Initialize subsystems
        self.messaging_core = get_messaging_core()
        self.verified_messaging = get_verified_messaging_service()
        self.routing_tracer = get_routing_tracer()
        self.heartbeat_system = get_heartbeat_system()
        
        # Health data storage
        self.agent_health: Dict[str, AgentHealthStatus] = {}
        self.system_metrics: Dict[str, HealthMetric] = {}
        self.health_history: List[SwarmHealthReport] = []
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_task = None
        
        # Initialize agent health status
        self._initialize_agent_health()
        
        # Start monitoring
        self._start_monitoring()
    
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
    
    def _start_monitoring(self):
        """Start continuous health monitoring."""
        import threading
        
        def monitoring_loop():
            while True:
                try:
                    asyncio.run(self._perform_health_check())
                    time.sleep(self.monitoring_interval)
                except Exception as e:
                    self.logger.error(f"Health monitoring error: {e}")
                    time.sleep(60)  # Wait longer on error
        
        self.monitoring_task = threading.Thread(target=monitoring_loop, daemon=True)
        self.monitoring_task.start()
        self.is_monitoring = True
        self.logger.info("Swarm health monitoring started")
    
    async def _perform_health_check(self):
        """Perform comprehensive health check."""
        try:
            # Check agent health
            await self._check_agent_health()
            
            # Check system metrics
            await self._check_system_metrics()
            
            # Check routing health
            await self._check_routing_health()
            
            # Check messaging health
            await self._check_messaging_health()
            
            # Generate health report
            report = await self._generate_health_report()
            
            # Store report
            self.health_history.append(report)
            
            # Keep only last 100 reports
            if len(self.health_history) > 100:
                self.health_history = self.health_history[-100:]
            
            # Check for critical issues
            await self._check_critical_issues(report)
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
    
    async def _check_agent_health(self):
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
                    health_score = self._calculate_agent_health_score(heartbeat_status)
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
    
    def _calculate_agent_health_score(self, heartbeat_status) -> float:
        """Calculate health score for an agent."""
        if not heartbeat_status.is_online:
            return 0.0
        
        # Base score
        score = 1.0
        
        # Penalize for consecutive failures
        score -= heartbeat_status.consecutive_failures * 0.1
        
        # Penalize for high response time
        if heartbeat_status.response_time_ms > 1000:
            score -= 0.2
        elif heartbeat_status.response_time_ms > 500:
            score -= 0.1
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, score))
    
    async def _check_system_metrics(self):
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
    
    async def _check_routing_health(self):
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
    
    async def _check_messaging_health(self):
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
    
    async def _generate_health_report(self) -> SwarmHealthReport:
        """Generate comprehensive health report."""
        try:
            # Calculate overall health
            overall_health, health_score = self._calculate_overall_health()
            
            # Get routing health
            routing_health = self.routing_tracer.get_routing_statistics()
            
            # Get messaging health
            messaging_health = self.verified_messaging.get_system_health()
            
            # Identify critical issues
            critical_issues = self._identify_critical_issues()
            
            # Generate recommendations
            recommendations = self._generate_recommendations(critical_issues)
            
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
    
    def _calculate_overall_health(self) -> Tuple[str, float]:
        """Calculate overall swarm health."""
        try:
            # Calculate average agent health score
            agent_scores = [agent.health_score for agent in self.agent_health.values()]
            avg_agent_score = sum(agent_scores) / len(agent_scores) if agent_scores else 0.0
            
            # Calculate system metrics score
            system_scores = []
            for metric in self.system_metrics.values():
                if metric.status == "healthy":
                    system_scores.append(1.0)
                elif metric.status == "warning":
                    system_scores.append(0.5)
                else:
                    system_scores.append(0.0)
            
            avg_system_score = sum(system_scores) / len(system_scores) if system_scores else 1.0
            
            # Overall health score
            overall_score = (avg_agent_score + avg_system_score) / 2.0
            
            # Determine health status
            if overall_score >= 0.8:
                health_status = "healthy"
            elif overall_score >= 0.6:
                health_status = "degraded"
            elif overall_score >= 0.3:
                health_status = "critical"
            else:
                health_status = "offline"
            
            return health_status, overall_score
            
        except Exception as e:
            self.logger.error(f"Failed to calculate overall health: {e}")
            return "unknown", 0.0
    
    def _identify_critical_issues(self) -> List[str]:
        """Identify critical issues in the swarm."""
        issues = []
        
        try:
            # Check for offline agents
            offline_agents = [agent for agent, status in self.agent_health.items() if not status.is_online]
            if offline_agents:
                issues.append(f"Offline agents: {', '.join(offline_agents)}")
            
            # Check for critical agents
            critical_agents = [agent for agent, status in self.agent_health.items() if status.status == "critical"]
            if critical_agents:
                issues.append(f"Critical agents: {', '.join(critical_agents)}")
            
            # Check for routing issues
            routing_success_rate = self.system_metrics.get("routing_success_rate")
            if routing_success_rate and routing_success_rate.value < 0.95:
                issues.append(f"Low routing success rate: {routing_success_rate.value:.2%}")
            
            # Check for messaging issues
            messaging_success_rate = self.system_metrics.get("messaging_success_rate")
            if messaging_success_rate and messaging_success_rate.value < 0.90:
                issues.append(f"Low messaging success rate: {messaging_success_rate.value:.2%}")
            
            # Check for Agent-8 specific issues
            if "Agent-8" in self.agent_health:
                agent8_status = self.agent_health["Agent-8"]
                if not agent8_status.is_online:
                    issues.append("CRITICAL: Agent-8 is offline - routing crisis")
                elif agent8_status.status == "critical":
                    issues.append("CRITICAL: Agent-8 health is critical - routing may be affected")
            
        except Exception as e:
            self.logger.error(f"Failed to identify critical issues: {e}")
            issues.append(f"Error identifying issues: {e}")
        
        return issues
    
    def _generate_recommendations(self, critical_issues: List[str]) -> List[str]:
        """Generate recommendations based on critical issues."""
        recommendations = []
        
        try:
            # Agent-8 specific recommendations
            if any("Agent-8" in issue for issue in critical_issues):
                recommendations.append("URGENT: Deploy emergency routing patch for Agent-8")
                recommendations.append("URGENT: Implement direct messaging channel for Agent-8")
                recommendations.append("URGENT: Verify Agent-8 coordinates and routing table")
            
            # General recommendations
            if any("Offline agents" in issue for issue in critical_issues):
                recommendations.append("Restart offline agents")
                recommendations.append("Check agent workspace connectivity")
            
            if any("routing success rate" in issue for issue in critical_issues):
                recommendations.append("Review routing table configuration")
                recommendations.append("Validate agent coordinates")
            
            if any("messaging success rate" in issue for issue in critical_issues):
                recommendations.append("Check messaging system configuration")
                recommendations.append("Verify WebSocket connections")
            
            # Performance recommendations
            avg_response_time = self.system_metrics.get("average_response_time")
            if avg_response_time and avg_response_time.value > 500:
                recommendations.append("Optimize system performance")
                recommendations.append("Check network latency")
            
            # Default recommendations if no critical issues
            if not critical_issues:
                recommendations.append("System is healthy - continue monitoring")
                recommendations.append("Consider performance optimizations")
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
            recommendations.append(f"Error generating recommendations: {e}")
        
        return recommendations
    
    async def _check_critical_issues(self, report: SwarmHealthReport):
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
    
    def export_health_report(self, filepath: str):
        """Export health report to file."""
        try:
            report = self.get_current_health()
            
            # Convert to serializable format
            report_data = {
                "timestamp": report.timestamp.isoformat(),
                "overall_health": report.overall_health,
                "health_score": report.health_score,
                "agent_statuses": {
                    agent_id: {
                        "agent_id": status.agent_id,
                        "is_online": status.is_online,
                        "last_heartbeat": status.last_heartbeat.isoformat(),
                        "response_time_ms": status.response_time_ms,
                        "consecutive_failures": status.consecutive_failures,
                        "health_score": status.health_score,
                        "status": status.status,
                        "last_error": status.last_error
                    }
                    for agent_id, status in report.agent_statuses.items()
                },
                "system_metrics": {
                    name: {
                        "name": metric.name,
                        "value": metric.value,
                        "unit": metric.unit,
                        "timestamp": metric.timestamp.isoformat(),
                        "threshold_warning": metric.threshold_warning,
                        "threshold_critical": metric.threshold_critical,
                        "status": metric.status
                    }
                    for name, metric in report.system_metrics.items()
                },
                "routing_health": report.routing_health,
                "messaging_health": report.messaging_health,
                "critical_issues": report.critical_issues,
                "recommendations": report.recommendations
            }
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Health report exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to export health report: {e}")
    
    def stop_monitoring(self):
        """Stop health monitoring."""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.join(timeout=5)
        self.logger.info("Swarm health monitoring stopped")


# Global swarm health monitor instance
_swarm_health_monitor = None


def get_swarm_health_monitor() -> SwarmHealthMonitor:
    """Get global swarm health monitor instance."""
    global _swarm_health_monitor
    if _swarm_health_monitor is None:
        _swarm_health_monitor = SwarmHealthMonitor()
    return _swarm_health_monitor


# Convenience functions
def get_current_swarm_health() -> SwarmHealthReport:
    """Get current swarm health status."""
    monitor = get_swarm_health_monitor()
    return monitor.get_current_health()


def export_swarm_health_report(filepath: str):
    """Export swarm health report to file."""
    monitor = get_swarm_health_monitor()
    monitor.export_health_report(filepath)


def get_swarm_health_history(hours: int = 24) -> List[SwarmHealthReport]:
    """Get swarm health history."""
    monitor = get_swarm_health_monitor()
    return monitor.get_health_history(hours)