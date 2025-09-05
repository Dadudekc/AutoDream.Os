"""
Strategic Oversight Engine
=========================

Core engine for vector strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, engine logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from .data_models import (
    StrategicOversightReport, SwarmCoordinationInsight, StrategicRecommendation,
    AgentPerformanceMetrics, SwarmCoordinationStatus, StrategicMission,
    VectorDatabaseMetrics, SystemHealthMetrics
)
from .enums import (
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus,
    ReportType, PriorityLevel, AgentRole
)
from .factory_methods import StrategicOversightFactory
from .validators import StrategicOversightValidator


class StrategicOversightEngine:
    """Strategic oversight engine."""
    
    def __init__(self):
        """Initialize strategic oversight engine."""
        self.reports: Dict[str, StrategicOversightReport] = {}
        self.insights: Dict[str, SwarmCoordinationInsight] = {}
        self.recommendations: Dict[str, StrategicRecommendation] = {}
        self.missions: Dict[str, MissionStatus] = {}
        self.agent_capabilities: Dict[str, AgentCapabilities] = {}
        self.emergencies: Dict[str, EmergencyStatus] = {}
        self.patterns: Dict[str, PatternAnalysis] = {}
        self.predictions: Dict[str, SuccessPrediction] = {}
        self.risks: Dict[str, RiskAssessment] = {}
        self.interventions: Dict[str, InterventionHistory] = {}
    
    async def generate_oversight_report(
        self,
        report_type: str,
        title: str,
        summary: str,
        include_insights: bool = True,
        include_recommendations: bool = True
    ) -> StrategicOversightReport:
        """Generate strategic oversight report."""
        try:
            insights = []
            recommendations = []
            
            if include_insights:
                insights = await self._collect_insights()
            
            if include_recommendations:
                recommendations = await self._generate_recommendations()
            
            # Determine confidence and impact levels
            confidence_level = self._calculate_confidence_level(insights)
            impact_level = self._calculate_impact_level(insights)
            
            report = StrategicOversightReport(
                report_id=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                report_type=report_type,
                title=title,
                summary=summary,
                insights=insights,
                recommendations=recommendations,
                confidence_level=confidence_level,
                impact_level=impact_level,
                generated_at=datetime.now(),
                valid_until=datetime.now() + timedelta(hours=24)
            )
            
            self.reports[report.report_id] = report
            return report
            
        except Exception as e:
            # Return minimal report on error
            return StrategicOversightReport(
                report_id=f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                report_type=report_type,
                title=title,
                summary=f"Error generating report: {str(e)}",
                insights=[],
                recommendations=[],
                confidence_level=ConfidenceLevel.LOW,
                impact_level=ImpactLevel.MINIMAL,
                generated_at=datetime.now()
            )
    
    async def _collect_insights(self) -> List[Dict[str, Any]]:
        """Collect insights for report."""
        insights = []
        
        # Collect performance insights
        performance_insights = await self._analyze_performance()
        insights.extend(performance_insights)
        
        # Collect coordination insights
        coordination_insights = await self._analyze_coordination()
        insights.extend(coordination_insights)
        
        # Collect efficiency insights
        efficiency_insights = await self._analyze_efficiency()
        insights.extend(efficiency_insights)
        
        return insights
    
    async def _analyze_performance(self) -> List[Dict[str, Any]]:
        """Analyze performance metrics."""
        insights = []
        
        # Mock performance analysis
        if self.missions:
            completed_missions = sum(1 for m in self.missions.values() 
                                   if m.status == MissionStatusEnum.COMPLETED)
            total_missions = len(self.missions)
            completion_rate = completed_missions / total_missions if total_missions > 0 else 0.0
            
            insights.append({
                "type": "performance",
                "metric": "mission_completion_rate",
                "value": completion_rate,
                "description": f"Mission completion rate: {completion_rate:.2%}",
                "confidence": 0.8
            })
        
        return insights
    
    async def _analyze_coordination(self) -> List[Dict[str, Any]]:
        """Analyze coordination metrics."""
        insights = []
        
        # Mock coordination analysis
        if self.agent_capabilities:
            available_agents = sum(1 for a in self.agent_capabilities.values() if a.availability)
            total_agents = len(self.agent_capabilities)
            availability_rate = available_agents / total_agents if total_agents > 0 else 0.0
            
            insights.append({
                "type": "coordination",
                "metric": "agent_availability",
                "value": availability_rate,
                "description": f"Agent availability rate: {availability_rate:.2%}",
                "confidence": 0.9
            })
        
        return insights
    
    async def _analyze_efficiency(self) -> List[Dict[str, Any]]:
        """Analyze efficiency metrics."""
        insights = []
        
        # Mock efficiency analysis
        if self.interventions:
            successful_interventions = sum(1 for i in self.interventions.values() 
                                        if i.effectiveness_score > 0.7)
            total_interventions = len(self.interventions)
            success_rate = successful_interventions / total_interventions if total_interventions > 0 else 0.0
            
            insights.append({
                "type": "efficiency",
                "metric": "intervention_success_rate",
                "value": success_rate,
                "description": f"Intervention success rate: {success_rate:.2%}",
                "confidence": 0.7
            })
        
        return insights
    
    async def _generate_recommendations(self) -> List[str]:
        """Generate strategic recommendations."""
        recommendations = []
        
        # Analyze current state and generate recommendations
        if self.emergencies:
            active_emergencies = sum(1 for e in self.emergencies.values() if e.status == "active")
            if active_emergencies > 0:
                recommendations.append(f"Address {active_emergencies} active emergency(ies)")
        
        if self.risks:
            high_risks = sum(1 for r in self.risks.values() if r.risk_level == ImpactLevel.HIGH)
            if high_risks > 0:
                recommendations.append(f"Mitigate {high_risks} high-risk situation(s)")
        
        if self.missions:
            stalled_missions = sum(1 for m in self.missions.values() 
                                 if m.status == MissionStatusEnum.PAUSED)
            if stalled_missions > 0:
                recommendations.append(f"Resume {stalled_missions} stalled mission(s)")
        
        return recommendations
    
    def _calculate_confidence_level(self, insights: List[Dict[str, Any]]) -> ConfidenceLevel:
        """Calculate overall confidence level."""
        if not insights:
            return ConfidenceLevel.LOW
        
        avg_confidence = sum(insight.get("confidence", 0.0) for insight in insights) / len(insights)
        
        if avg_confidence >= 0.8:
            return ConfidenceLevel.VERY_HIGH
        elif avg_confidence >= 0.6:
            return ConfidenceLevel.HIGH
        elif avg_confidence >= 0.4:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _calculate_impact_level(self, insights: List[Dict[str, Any]]) -> ImpactLevel:
        """Calculate overall impact level."""
        if not insights:
            return ImpactLevel.MINIMAL
        
        # Check for critical insights
        for insight in insights:
            if insight.get("type") == "emergency":
                return ImpactLevel.CRITICAL
        
        # Check for high impact metrics
        high_impact_count = sum(1 for insight in insights 
                              if insight.get("value", 0) > 0.8)
        
        if high_impact_count >= 3:
            return ImpactLevel.HIGH
        elif high_impact_count >= 1:
            return ImpactLevel.MEDIUM
        else:
            return ImpactLevel.LOW
    
    async def add_mission_status(self, mission: MissionStatus) -> bool:
        """Add mission status."""
        try:
            self.missions[mission.mission_id] = mission
            return True
        except Exception:
            return False
    
    async def add_agent_capabilities(self, capabilities: AgentCapabilities) -> bool:
        """Add agent capabilities."""
        try:
            self.agent_capabilities[capabilities.agent_id] = capabilities
            return True
        except Exception:
            return False
    
    async def add_emergency_status(self, emergency: EmergencyStatus) -> bool:
        """Add emergency status."""
        try:
            self.emergencies[emergency.emergency_id] = emergency
            return True
        except Exception:
            return False
    
    async def add_risk_assessment(self, risk: RiskAssessment) -> bool:
        """Add risk assessment."""
        try:
            self.risks[risk.assessment_id] = risk
            return True
        except Exception:
            return False
    
    async def add_intervention_history(self, intervention: InterventionHistory) -> bool:
        """Add intervention history."""
        try:
            self.interventions[intervention.intervention_id] = intervention
            return True
        except Exception:
            return False
    
    def get_oversight_summary(self) -> Dict[str, Any]:
        """Get oversight summary."""
        return {
            "total_reports": len(self.reports),
            "total_insights": len(self.insights),
            "total_recommendations": len(self.recommendations),
            "active_missions": sum(1 for m in self.missions.values() 
                                 if m.status == MissionStatusEnum.ACTIVE),
            "available_agents": sum(1 for a in self.agent_capabilities.values() 
                                  if a.availability),
            "active_emergencies": sum(1 for e in self.emergencies.values() 
                                    if e.status == "active"),
            "high_risks": sum(1 for r in self.risks.values() 
                            if r.risk_level == ImpactLevel.HIGH),
            "total_interventions": len(self.interventions)
        }
    
    def clear_all_data(self):
        """Clear all data."""
        self.reports.clear()
        self.insights.clear()
        self.recommendations.clear()
        self.missions.clear()
        self.agent_capabilities.clear()
        self.emergencies.clear()
        self.patterns.clear()
        self.predictions.clear()
        self.risks.clear()
        self.interventions.clear()
