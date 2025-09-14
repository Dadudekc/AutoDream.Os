"""
Emergency Analyzer - V2 Compliant Module
=======================================

Analyzes emergency incidents and provides recommendations.
Extracted from orchestrator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from datetime import datetime
from typing import Any

from ..models import Emergency, EmergencyContext, EmergencySeverity, EmergencyType


class EmergencyAnalyzer:
    """Analyzes emergency incidents and provides recommendations.

    Handles emergency analysis, risk assessment, and health monitoring.
    """

    def __init__(self):
        """Initialize emergency analyzer."""
        self.analysis_history = []
        self.health_metrics = {}

    def analyze_emergency(self, emergency: Emergency) -> dict[str, Any]:
        """Analyze emergency incident."""
        try:
            analysis = {
                "emergency_id": emergency.emergency_id,
                "analysis_timestamp": datetime.now().isoformat(),
                "risk_assessment": self._assess_risk(emergency),
                "impact_analysis": self._analyze_impact(emergency),
                "recommendations": self._generate_recommendations(emergency),
                "priority_score": self._calculate_priority_score(emergency),
            }

            self.analysis_history.append(analysis)
            return analysis

        except Exception as e:
            return {
                "emergency_id": emergency.emergency_id,
                "error": str(e),
                "analysis_timestamp": datetime.now().isoformat(),
            }

    def _assess_risk(self, emergency: Emergency) -> dict[str, Any]:
        """Assess risk level for emergency."""
        severity_scores = {
            EmergencySeverity.LOW: 1,
            EmergencySeverity.MEDIUM: 2,
            EmergencySeverity.HIGH: 3,
            EmergencySeverity.CRITICAL: 4,
        }

        base_score = severity_scores.get(emergency.severity, 1)

        # Adjust based on emergency type
        type_multipliers = {
            EmergencyType.SYSTEM_FAILURE: 1.5,
            EmergencyType.SECURITY_BREACH: 2.0,
            EmergencyType.PERFORMANCE_DEGRADATION: 1.2,
            EmergencyType.DATA_CORRUPTION: 1.8,
            EmergencyType.NETWORK_OUTAGE: 1.3,
        }

        multiplier = type_multipliers.get(emergency.emergency_type, 1.0)
        risk_score = base_score * multiplier

        if risk_score >= 6:
            risk_level = "critical"
        elif risk_score >= 4:
            risk_level = "high"
        elif risk_score >= 2:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "severity_factor": base_score,
            "type_factor": multiplier,
        }

    def _analyze_impact(self, emergency: Emergency) -> dict[str, Any]:
        """Analyze impact of emergency."""
        context = emergency.context or EmergencyContext()

        return {
            "user_impact": context.get("user_impact", {}),
            "system_impact": context.get("system_metrics", {}),
            "business_impact": self._assess_business_impact(emergency),
            "estimated_downtime": self._estimate_downtime(emergency),
        }

    def _assess_business_impact(self, emergency: Emergency) -> str:
        """Assess business impact level."""
        if emergency.severity == EmergencySeverity.CRITICAL:
            return "severe"
        elif emergency.severity == EmergencySeverity.HIGH:
            return "moderate"
        elif emergency.severity == EmergencySeverity.MEDIUM:
            return "minor"
        else:
            return "minimal"

    def _estimate_downtime(self, emergency: Emergency) -> int:
        """Estimate downtime in minutes."""
        downtime_estimates = {
            EmergencySeverity.LOW: 5,
            EmergencySeverity.MEDIUM: 30,
            EmergencySeverity.HIGH: 120,
            EmergencySeverity.CRITICAL: 480,
        }

        return downtime_estimates.get(emergency.severity, 60)

    def _generate_recommendations(self, emergency: Emergency) -> list[str]:
        """Generate recommendations for emergency."""
        recommendations = []

        if emergency.severity == EmergencySeverity.CRITICAL:
            recommendations.append("Immediate intervention required")
            recommendations.append("Consider system isolation")
            recommendations.append("Notify all stakeholders")
        elif emergency.severity == EmergencySeverity.HIGH:
            recommendations.append("Priority intervention needed")
            recommendations.append("Monitor system closely")
        elif emergency.severity == EmergencySeverity.MEDIUM:
            recommendations.append("Schedule intervention")
            recommendations.append("Document incident")
        else:
            recommendations.append("Monitor situation")
            recommendations.append("Consider preventive measures")

        # Type-specific recommendations
        if emergency.emergency_type == EmergencyType.SECURITY_BREACH:
            recommendations.append("Initiate security protocols")
            recommendations.append("Preserve evidence")
        elif emergency.emergency_type == EmergencyType.DATA_CORRUPTION:
            recommendations.append("Stop data operations")
            recommendations.append("Initiate backup recovery")

        return recommendations

    def _calculate_priority_score(self, emergency: Emergency) -> int:
        """Calculate priority score for emergency."""
        severity_scores = {
            EmergencySeverity.LOW: 1,
            EmergencySeverity.MEDIUM: 2,
            EmergencySeverity.HIGH: 3,
            EmergencySeverity.CRITICAL: 4,
        }

        type_scores = {
            EmergencyType.SYSTEM_FAILURE: 3,
            EmergencyType.SECURITY_BREACH: 4,
            EmergencyType.PERFORMANCE_DEGRADATION: 2,
            EmergencyType.DATA_CORRUPTION: 4,
            EmergencyType.NETWORK_OUTAGE: 3,
        }

        severity_score = severity_scores.get(emergency.severity, 1)
        type_score = type_scores.get(emergency.emergency_type, 1)

        return severity_score + type_score

    def get_analysis_history(self) -> list[dict[str, Any]]:
        """Get analysis history."""
        return self.analysis_history.copy()

    def get_analysis_metrics(self) -> dict[str, Any]:
        """Get analysis metrics."""
        if not self.analysis_history:
            return {}

        total_analyses = len(self.analysis_history)
        critical_count = sum(
            1
            for a in self.analysis_history
            if a.get("risk_assessment", {}).get("risk_level") == "critical"
        )
        high_count = sum(
            1
            for a in self.analysis_history
            if a.get("risk_assessment", {}).get("risk_level") == "high"
        )

        return {
            "total_analyses": total_analyses,
            "critical_emergencies": critical_count,
            "high_emergencies": high_count,
            "average_priority_score": (
                sum(a.get("priority_score", 0) for a in self.analysis_history) / total_analyses
            ),
        }

    def clear_analysis_history(self):
        """Clear analysis history."""
        self.analysis_history.clear()

    def export_analysis_data(self) -> dict[str, Any]:
        """Export analysis data."""
        return {
            "analysis_history": self.analysis_history,
            "metrics": self.get_analysis_metrics(),
            "exported_at": datetime.now().isoformat(),
        }
