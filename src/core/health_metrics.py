#!/usr/bin/env python3
"""
HEALTH METRICS - V2 COMPLIANT MODULE
===================================

Health metric data structures and calculations.
Extracted from swarm_health_monitor.py for V2 compliance.

Author: Agent-4 (Strategic Oversight & Emergency Intervention Manager)
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


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
    critical_issues: list[str]
    recommendations: list[str]


class HealthCalculator:
    """Health calculation utilities."""
    
    @staticmethod
    def calculate_agent_health_score(heartbeat_status) -> float:
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
    
    @staticmethod
    def calculate_overall_health(agent_health: Dict[str, AgentHealthStatus], 
                               system_metrics: Dict[str, HealthMetric]) -> tuple[str, float]:
        """Calculate overall swarm health."""
        try:
            # Calculate average agent health score
            agent_scores = [agent.health_score for agent in agent_health.values()]
            avg_agent_score = sum(agent_scores) / len(agent_scores) if agent_scores else 0.0
            
            # Calculate system metrics score
            system_scores = []
            for metric in system_metrics.values():
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
            
        except Exception:
            return "unknown", 0.0
    
    @staticmethod
    def identify_critical_issues(agent_health: Dict[str, AgentHealthStatus], 
                               system_metrics: Dict[str, HealthMetric]) -> list[str]:
        """Identify critical issues in the swarm."""
        issues = []
        
        try:
            # Check for offline agents
            offline_agents = [agent for agent, status in agent_health.items() if not status.is_online]
            if offline_agents:
                issues.append(f"Offline agents: {', '.join(offline_agents)}")
            
            # Check for critical agents
            critical_agents = [agent for agent, status in agent_health.items() if status.status == "critical"]
            if critical_agents:
                issues.append(f"Critical agents: {', '.join(critical_agents)}")
            
            # Check for routing issues
            routing_success_rate = system_metrics.get("routing_success_rate")
            if routing_success_rate and routing_success_rate.value < 0.95:
                issues.append(f"Low routing success rate: {routing_success_rate.value:.2%}")
            
            # Check for messaging issues
            messaging_success_rate = system_metrics.get("messaging_success_rate")
            if messaging_success_rate and messaging_success_rate.value < 0.90:
                issues.append(f"Low messaging success rate: {messaging_success_rate.value:.2%}")
            
            # Check for Agent-8 specific issues
            if "Agent-8" in agent_health:
                agent8_status = agent_health["Agent-8"]
                if not agent8_status.is_online:
                    issues.append("CRITICAL: Agent-8 is offline - routing crisis")
                elif agent8_status.status == "critical":
                    issues.append("CRITICAL: Agent-8 health is critical - routing may be affected")
            
        except Exception as e:
            issues.append(f"Error identifying issues: {e}")
        
        return issues
    
    @staticmethod
    def generate_recommendations(critical_issues: list[str]) -> list[str]:
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
            
            # Default recommendations if no critical issues
            if not critical_issues:
                recommendations.append("System is healthy - continue monitoring")
                recommendations.append("Consider performance optimizations")
            
        except Exception as e:
            recommendations.append(f"Error generating recommendations: {e}")
        
        return recommendations