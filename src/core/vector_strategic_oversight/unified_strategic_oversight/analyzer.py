"""
Strategic Oversight Analyzer
============================

Analysis functionality for strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, analysis logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import (
    SwarmCoordinationInsight, StrategicRecommendation, AgentPerformanceMetrics,
    SwarmCoordinationStatus, StrategicMission, VectorDatabaseMetrics,
    SystemHealthMetrics, StrategicOversightModels,
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, ReportType,
    PriorityLevel, AgentRole
)
from .engine import StrategicOversightEngine


class StrategicOversightAnalyzer:
    """Strategic oversight analysis functionality."""
    
    def __init__(self, engine: StrategicOversightEngine):
        """Initialize strategic oversight analyzer."""
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the analyzer."""
        try:
            if not self.engine.is_initialized:
                raise Exception("Engine not initialized")
            
            self.is_initialized = True
            self.logger.info("Strategic Oversight Analyzer initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Strategic Oversight Analyzer: {e}")
            return False
    
    def analyze_swarm_coordination(self, swarm_id: str = None) -> List[SwarmCoordinationInsight]:
        """Analyze swarm coordination."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Analyzer not initialized")
            
            # Get coordination status
            coordination_statuses = list(self.engine.coordination_status.values())
            if swarm_id:
                coordination_statuses = [s for s in coordination_statuses if s.swarm_id == swarm_id]
            
            insights = []
            for status in coordination_statuses:
                if status.coordination_level < 0.7:
                    insight = StrategicOversightModels.create_swarm_coordination_insight(
                        insight_type=InsightType.COORDINATION,
                        title=f"Low Coordination Level - {status.swarm_id}",
                        description=f"Coordination level is below optimal threshold",
                        confidence=ConfidenceLevel.HIGH,
                        impact=ImpactLevel.MEDIUM,
                        evidence=[f"Coordination level: {status.coordination_level}"],
                        recommendations=["Improve communication protocols", "Enhance task distribution"]
                    )
                    insights.append(insight)
                    self.engine.add_insight(insight)
            
            self.logger.info(f"Analyzed {len(insights)} swarm coordination insights")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error analyzing swarm coordination: {e}")
            return []
    
    def analyze_agent_performance(self, agent_id: str = None) -> List[SwarmCoordinationInsight]:
        """Analyze agent performance."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Analyzer not initialized")
            
            # Get agent metrics
            agent_metrics = self.engine.get_agent_metrics(agent_id)
            
            insights = []
            for metrics in agent_metrics:
                if metrics.performance_score < 0.8:
                    insight = StrategicOversightModels.create_swarm_coordination_insight(
                        insight_type=InsightType.PERFORMANCE,
                        title=f"Low Performance - {metrics.agent_id}",
                        description=f"Agent performance is below optimal threshold",
                        confidence=ConfidenceLevel.HIGH,
                        impact=ImpactLevel.HIGH,
                        evidence=[f"Performance score: {metrics.performance_score}"],
                        recommendations=["Provide additional training", "Review task assignments"]
                    )
                    insights.append(insight)
                    self.engine.add_insight(insight)
            
            self.logger.info(f"Analyzed {len(insights)} agent performance insights")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error analyzing agent performance: {e}")
            return []
    
    def analyze_mission_efficiency(self, mission_id: str = None) -> List[SwarmCoordinationInsight]:
        """Analyze mission efficiency."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Analyzer not initialized")
            
            # Get missions
            missions = list(self.engine.missions.values())
            if mission_id:
                missions = [m for m in missions if m.mission_id == mission_id]
            
            insights = []
            for mission in missions:
                if mission.status == MissionStatus.ACTIVE and len(mission.assigned_agents) < 3:
                    insight = StrategicOversightModels.create_swarm_coordination_insight(
                        insight_type=InsightType.EFFICIENCY,
                        title=f"Understaffed Mission - {mission.title}",
                        description=f"Mission has insufficient agent allocation",
                        confidence=ConfidenceLevel.MEDIUM,
                        impact=ImpactLevel.MEDIUM,
                        evidence=[f"Assigned agents: {len(mission.assigned_agents)}"],
                        recommendations=["Assign additional agents", "Review mission scope"]
                    )
                    insights.append(insight)
                    self.engine.add_insight(insight)
            
            self.logger.info(f"Analyzed {len(insights)} mission efficiency insights")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error analyzing mission efficiency: {e}")
            return []
    
    def analyze_vector_database_performance(self, database_name: str = None) -> List[SwarmCoordinationInsight]:
        """Analyze vector database performance."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Analyzer not initialized")
            
            # Get vector metrics
            vector_metrics = self.engine.get_vector_metrics(database_name)
            
            insights = []
            for metrics in vector_metrics:
                if metrics.query_performance < 0.8:
                    insight = StrategicOversightModels.create_swarm_coordination_insight(
                        insight_type=InsightType.PERFORMANCE,
                        title=f"Slow Query Performance - {metrics.database_name}",
                        description=f"Vector database query performance is below optimal",
                        confidence=ConfidenceLevel.HIGH,
                        impact=ImpactLevel.MEDIUM,
                        evidence=[f"Query performance: {metrics.query_performance}"],
                        recommendations=["Optimize indexing", "Review query patterns"]
                    )
                    insights.append(insight)
                    self.engine.add_insight(insight)
            
            self.logger.info(f"Analyzed {len(insights)} vector database performance insights")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error analyzing vector database performance: {e}")
            return []
    
    def generate_strategic_recommendations(self, insights: List[SwarmCoordinationInsight]) -> List[StrategicRecommendation]:
        """Generate strategic recommendations based on insights."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Analyzer not initialized")
            
            recommendations = []
            
            # Generate recommendations based on insight types
            performance_insights = [i for i in insights if i.insight_type == InsightType.PERFORMANCE]
            if performance_insights:
                recommendation = StrategicOversightModels.create_strategic_recommendation(
                    title="Performance Optimization Initiative",
                    description="Implement comprehensive performance optimization across all systems",
                    priority=PriorityLevel.HIGH,
                    impact=ImpactLevel.HIGH,
                    implementation_effort="high",
                    expected_benefits=["Improved system performance", "Better user experience"],
                    risks=["Implementation complexity", "Resource requirements"]
                )
                recommendations.append(recommendation)
                self.engine.add_recommendation(recommendation)
            
            coordination_insights = [i for i in insights if i.insight_type == InsightType.COORDINATION]
            if coordination_insights:
                recommendation = StrategicOversightModels.create_strategic_recommendation(
                    title="Coordination Enhancement Program",
                    description="Improve coordination mechanisms across all agent swarms",
                    priority=PriorityLevel.MEDIUM,
                    impact=ImpactLevel.MEDIUM,
                    implementation_effort="medium",
                    expected_benefits=["Better team coordination", "Reduced conflicts"],
                    risks=["Team resistance", "Implementation time"]
                )
                recommendations.append(recommendation)
                self.engine.add_recommendation(recommendation)
            
            efficiency_insights = [i for i in insights if i.insight_type == InsightType.EFFICIENCY]
            if efficiency_insights:
                recommendation = StrategicOversightModels.create_strategic_recommendation(
                    title="Efficiency Improvement Initiative",
                    description="Enhance operational efficiency across all missions",
                    priority=PriorityLevel.HIGH,
                    impact=ImpactLevel.HIGH,
                    implementation_effort="high",
                    expected_benefits=["Faster mission completion", "Reduced costs"],
                    risks=["High implementation effort", "Change management"]
                )
                recommendations.append(recommendation)
                self.engine.add_recommendation(recommendation)
            
            self.logger.info(f"Generated {len(recommendations)} strategic recommendations")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating strategic recommendations: {e}")
            return []
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        try:
            if not self.is_initialized:
                return {'error': 'Analyzer not initialized'}
            
            insights_by_type = {}
            for insight_type in InsightType:
                insights_by_type[insight_type.value] = len([
                    i for i in self.engine.insights.values()
                    if i.insight_type == insight_type
                ])
            
            return {
                'analyzer_status': 'initialized',
                'insights_by_type': insights_by_type,
                'total_insights': len(self.engine.insights),
                'total_recommendations': len(self.engine.recommendations),
                'total_agent_metrics': len(self.engine.agent_metrics),
                'total_missions': len(self.engine.missions)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting analysis summary: {e}")
            return {'error': str(e)}
    
    def shutdown(self):
        """Shutdown analyzer."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Strategic Oversight Analyzer")
        self.is_initialized = False