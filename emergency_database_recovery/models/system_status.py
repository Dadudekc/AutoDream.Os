#!/usr/bin/env python3
"""
System Status Data Models.

This module contains data structures for system status and health monitoring:
- System health indicators
- Status tracking and monitoring
- Health level assessments
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class HealthLevel(Enum):
    """System health levels."""

    CRITICAL = "CRITICAL"
    POOR = "POOR"
    FAIR = "FAIR"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"


@dataclass
class SystemStatus:
    """System status and health information."""

    system_id: str
    name: str
    health_level: HealthLevel
    health_score: float  # 0.0 to 1.0
    status: str
    last_check: str
    components: Dict[str, Dict[str, Any]]
    alerts: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    @property
    def is_healthy(self) -> bool:
        """Check if system is healthy."""
        return self.health_level in [HealthLevel.GOOD, HealthLevel.EXCELLENT]

    @property
    def is_critical(self) -> bool:
        """Check if system is in critical condition."""
        return self.health_level == HealthLevel.CRITICAL

    @property
    def needs_attention(self) -> bool:
        """Check if system needs attention."""
        return self.health_level in [HealthLevel.CRITICAL, HealthLevel.POOR, HealthLevel.FAIR]

    @property
    def health_description(self) -> str:
        """Get human-readable health description."""
        if self.health_score >= 0.9:
            return "System is operating at excellent health"
        elif self.health_score >= 0.7:
            return "System is operating at good health"
        elif self.health_score >= 0.5:
            return "System is operating at fair health"
        elif self.health_score >= 0.3:
            return "System is operating at poor health"
        else:
            return "System is operating at critical health"

    def add_alert(self, alert: str):
        """Add a new alert."""
        if alert not in self.alerts:
            self.alerts.append(alert)

    def add_recommendation(self, recommendation: str):
        """Add a new recommendation."""
        if recommendation not in self.recommendations:
            self.recommendations.append(recommendation)

    def update_component_status(self, component_name: str, status: Dict[str, Any]):
        """Update status of a specific component."""
        self.components[component_name] = status

    def get_component_status(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific component."""
        return self.components.get(component_name)

    def calculate_overall_health(self):
        """Recalculate overall health based on component statuses."""
        if not self.components:
            self.health_score = 0.0
            self.health_level = HealthLevel.CRITICAL
            return

        # Calculate average health score from components
        total_score = 0.0
        component_count = 0

        for component_name, component_status in self.components.items():
            if "health_score" in component_status:
                total_score += component_status["health_score"]
                component_count += 1

        if component_count > 0:
            self.health_score = total_score / component_count
        else:
            self.health_score = 0.0

        # Update health level based on score
        if self.health_score >= 0.9:
            self.health_level = HealthLevel.EXCELLENT
        elif self.health_score >= 0.7:
            self.health_level = HealthLevel.GOOD
        elif self.health_score >= 0.5:
            self.health_level = HealthLevel.FAIR
        elif self.health_score >= 0.3:
            self.health_level = HealthLevel.POOR
        else:
            self.health_level = HealthLevel.CRITICAL
