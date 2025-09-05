"""
Strategic Oversight Engine Services
===================================

Service functionality for strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, service logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .models import (
    StrategicOversightReport, SwarmCoordinationInsight, StrategicRecommendation,
    AgentPerformanceMetrics, SwarmCoordinationStatus, StrategicMission,
    VectorDatabaseMetrics, SystemHealthMetrics, StrategicOversightModels,
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, ReportType,
    PriorityLevel, AgentRole
)
from .engine_core import StrategicOversightEngineCore


class StrategicOversightEngineServices:
    """Service functionality for strategic oversight operations."""
    
    def __init__(self, engine_core: StrategicOversightEngineCore):
        """Initialize strategic oversight engine services."""
        self.engine_core = engine_core
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the engine services."""
        try:
            if not self.engine_core.is_initialized:
                raise Exception("Engine core not initialized")
            
            self.is_initialized = True
            self.logger.info("Strategic Oversight Engine Services initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Strategic Oversight Engine Services: {e}")
            return False
    
    def generate_comprehensive_report(self, report_type: ReportType = ReportType.SUMMARY) -> Optional[StrategicOversightReport]:
        """Generate comprehensive strategic oversight report."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine services not initialized")
            
            # Collect all insights
            all_insights = list(self.engine_core.insights.values())
            
            # Collect all recommendations
            all_recommendations = list(self.engine_core.recommendations.values())
            
            # Generate metrics summary
            metrics_summary = {
                'total_reports': len(self.engine_core.reports),
                'total_insights': len(self.engine_core.insights),
                'total_recommendations': len(self.engine_core.recommendations),
                'total_agent_metrics': len(self.engine_core.agent_metrics),
                'total_missions': len(self.engine_core.missions),
                'total_vector_metrics': len(self.engine_core.vector_metrics),
                'total_system_health': len(self.engine_core.system_health)
            }
            
            # Create comprehensive report
            report = StrategicOversightModels.create_strategic_oversight_report(
                title=f"Strategic Oversight Report - {report_type.value.title()}",
                description=f"Comprehensive strategic oversight analysis",
                report_type=report_type,
                insights=all_insights,
                recommendations=all_recommendations,
                metrics=metrics_summary
            )
            
            self.engine_core.reports[report.report_id] = report
            self.logger.info(f"Generated comprehensive report: {report.title}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating comprehensive report: {e}")
            return None
    
    def analyze_performance_trends(self, days: int = 7) -> Dict[str, Any]:
        """Analyze performance trends over specified days."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine services not initialized")
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Analyze agent performance trends
            recent_metrics = [
                metrics for metrics in self.engine_core.agent_metrics.values()
                if metrics.created_at >= cutoff_date
            ]
            
            if not recent_metrics:
                return {'message': 'No recent performance data available'}
            
            # Calculate trend statistics
            avg_performance = sum(m.performance_score for m in recent_metrics) / len(recent_metrics)
            avg_efficiency = sum(m.efficiency for m in recent_metrics) / len(recent_metrics)
            avg_coordination = sum(m.coordination_score for m in recent_metrics) / len(recent_metrics)
            
            return {
                'analysis_period_days': days,
                'total_metrics_analyzed': len(recent_metrics),
                'average_performance_score': avg_performance,
                'average_efficiency': avg_efficiency,
                'average_coordination_score': avg_coordination,
                'trend_direction': 'improving' if avg_performance > 0.8 else 'needs_attention',
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance trends: {e}")
            return {'error': str(e)}
    
    def generate_insights_summary(self) -> Dict[str, Any]:
        """Generate insights summary."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine services not initialized")
            
            insights_by_type = {}
            for insight_type in InsightType:
                insights_by_type[insight_type.value] = len([
                    i for i in self.engine_core.insights.values()
                    if i.insight_type == insight_type
                ])
            
            insights_by_confidence = {}
            for confidence in ConfidenceLevel:
                insights_by_confidence[confidence.value] = len([
                    i for i in self.engine_core.insights.values()
                    if i.confidence == confidence
                ])
            
            insights_by_impact = {}
            for impact in ImpactLevel:
                insights_by_impact[impact.value] = len([
                    i for i in self.engine_core.insights.values()
                    if i.impact == impact
                ])
            
            return {
                'total_insights': len(self.engine_core.insights),
                'insights_by_type': insights_by_type,
                'insights_by_confidence': insights_by_confidence,
                'insights_by_impact': insights_by_impact,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating insights summary: {e}")
            return {'error': str(e)}
    
    def generate_recommendations_summary(self) -> Dict[str, Any]:
        """Generate recommendations summary."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine services not initialized")
            
            recommendations_by_priority = {}
            for priority in PriorityLevel:
                recommendations_by_priority[priority.value] = len([
                    r for r in self.engine_core.recommendations.values()
                    if r.priority == priority
                ])
            
            recommendations_by_impact = {}
            for impact in ImpactLevel:
                recommendations_by_impact[impact.value] = len([
                    r for r in self.engine_core.recommendations.values()
                    if r.impact == impact
                ])
            
            return {
                'total_recommendations': len(self.engine_core.recommendations),
                'recommendations_by_priority': recommendations_by_priority,
                'recommendations_by_impact': recommendations_by_impact,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations summary: {e}")
            return {'error': str(e)}
    
    def generate_mission_status_summary(self) -> Dict[str, Any]:
        """Generate mission status summary."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine services not initialized")
            
            missions_by_status = {}
            for status in MissionStatus:
                missions_by_status[status.value] = len([
                    m for m in self.engine_core.missions.values()
                    if m.status == status
                ])
            
            missions_by_priority = {}
            for priority in PriorityLevel:
                missions_by_priority[priority.value] = len([
                    m for m in self.engine_core.missions.values()
                    if m.priority == priority
                ])
            
            return {
                'total_missions': len(self.engine_core.missions),
                'missions_by_status': missions_by_status,
                'missions_by_priority': missions_by_priority,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating mission status summary: {e}")
            return {'error': str(e)}
    
    def generate_system_health_summary(self) -> Dict[str, Any]:
        """Generate system health summary."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine services not initialized")
            
            health_scores = [h.health_score for h in self.engine_core.system_health.values()]
            avg_health_score = sum(health_scores) / len(health_scores) if health_scores else 0
            
            components_by_health = {
                'healthy': len([h for h in self.engine_core.system_health.values() if h.health_score >= 0.8]),
                'degraded': len([h for h in self.engine_core.system_health.values() if 0.5 <= h.health_score < 0.8]),
                'critical': len([h for h in self.engine_core.system_health.values() if h.health_score < 0.5])
            }
            
            return {
                'total_components': len(self.engine_core.system_health),
                'average_health_score': avg_health_score,
                'components_by_health': components_by_health,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating system health summary: {e}")
            return {'error': str(e)}
    
    def get_services_status(self) -> Dict[str, Any]:
        """Get services status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'engine_core_initialized': self.engine_core.is_initialized,
            'services_type': 'strategic_oversight'
        }
    
    def shutdown(self):
        """Shutdown engine services."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Strategic Oversight Engine Services")
        self.is_initialized = False
