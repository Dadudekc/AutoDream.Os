"""
Strategic Oversight Orchestrator
================================

Main orchestrator for strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .models import (
    StrategicOversightReport, SwarmCoordinationInsight, StrategicRecommendation,
    AgentPerformanceMetrics, SwarmCoordinationStatus, StrategicMission,
    VectorDatabaseMetrics, SystemHealthMetrics, StrategicOversightModels,
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, ReportType,
    PriorityLevel, AgentRole
)
from .engine import StrategicOversightEngine
from .analyzer import StrategicOversightAnalyzer


class StrategicOversightOrchestrator:
    """Main orchestrator for strategic oversight system."""
    
    def __init__(self):
        """Initialize strategic oversight orchestrator."""
        self.engine = StrategicOversightEngine()
        self.analyzer = StrategicOversightAnalyzer(self.engine)
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Strategic Oversight Orchestrator")
            
            # Initialize engine
            if not self.engine.initialize():
                raise Exception("Failed to initialize engine")
            
            # Initialize analyzer
            if not self.analyzer.initialize():
                raise Exception("Failed to initialize analyzer")
            
            self.is_initialized = True
            self.logger.info("Strategic Oversight Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Strategic Oversight Orchestrator: {e}")
            return False
    
    async def add_report(self, title: str, description: str, report_type: ReportType,
                        insights: List[SwarmCoordinationInsight],
                        recommendations: List[StrategicRecommendation],
                        metrics: Dict[str, Any]) -> bool:
        """Add strategic oversight report."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        report = StrategicOversightModels.create_strategic_oversight_report(
            title=title,
            description=description,
            report_type=report_type,
            insights=insights,
            recommendations=recommendations,
            metrics=metrics
        )
        
        return self.engine.add_report(report)
    
    async def add_insight(self, insight_type: InsightType, title: str, description: str,
                         confidence: ConfidenceLevel, impact: ImpactLevel,
                         evidence: List[str], recommendations: List[str]) -> bool:
        """Add swarm coordination insight."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        insight = StrategicOversightModels.create_swarm_coordination_insight(
            insight_type=insight_type,
            title=title,
            description=description,
            confidence=confidence,
            impact=impact,
            evidence=evidence,
            recommendations=recommendations
        )
        
        return self.engine.add_insight(insight)
    
    async def add_recommendation(self, title: str, description: str,
                               priority: PriorityLevel, impact: ImpactLevel,
                               implementation_effort: str, expected_benefits: List[str],
                               risks: List[str]) -> bool:
        """Add strategic recommendation."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        recommendation = StrategicOversightModels.create_strategic_recommendation(
            title=title,
            description=description,
            priority=priority,
            impact=impact,
            implementation_effort=implementation_effort,
            expected_benefits=expected_benefits,
            risks=risks
        )
        
        return self.engine.add_recommendation(recommendation)
    
    async def add_agent_metrics(self, agent_id: str, agent_role: AgentRole,
                              performance_score: float, efficiency: float,
                              coordination_score: float, task_completion_rate: float,
                              response_time: float) -> bool:
        """Add agent performance metrics."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        metrics = StrategicOversightModels.create_agent_performance_metrics(
            agent_id=agent_id,
            agent_role=agent_role,
            performance_score=performance_score,
            efficiency=efficiency,
            coordination_score=coordination_score,
            task_completion_rate=task_completion_rate,
            response_time=response_time
        )
        
        return self.engine.add_agent_metrics(metrics)
    
    async def add_mission(self, title: str, description: str, status: MissionStatus,
                         priority: PriorityLevel, assigned_agents: List[str],
                         objectives: List[str], success_criteria: List[str]) -> bool:
        """Add strategic mission."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        mission = StrategicOversightModels.create_strategic_mission(
            title=title,
            description=description,
            status=status,
            priority=priority,
            assigned_agents=assigned_agents,
            objectives=objectives,
            success_criteria=success_criteria
        )
        
        return self.engine.add_mission(mission)
    
    async def analyze_swarm_coordination(self, swarm_id: str = None) -> List[SwarmCoordinationInsight]:
        """Analyze swarm coordination."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.analyzer.analyze_swarm_coordination(swarm_id)
    
    async def analyze_agent_performance(self, agent_id: str = None) -> List[SwarmCoordinationInsight]:
        """Analyze agent performance."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.analyzer.analyze_agent_performance(agent_id)
    
    async def analyze_mission_efficiency(self, mission_id: str = None) -> List[SwarmCoordinationInsight]:
        """Analyze mission efficiency."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.analyzer.analyze_mission_efficiency(mission_id)
    
    async def generate_comprehensive_report(self, report_type: ReportType = ReportType.SUMMARY) -> Optional[StrategicOversightReport]:
        """Generate comprehensive strategic oversight report."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.generate_comprehensive_report(report_type)
    
    async def get_reports(self, report_type: ReportType = None) -> List[StrategicOversightReport]:
        """Get reports."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if report_type:
            return self.engine.get_reports_by_type(report_type)
        else:
            return list(self.engine.reports.values())
    
    async def get_insights(self, insight_type: InsightType = None) -> List[SwarmCoordinationInsight]:
        """Get insights."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if insight_type:
            return self.engine.get_insights_by_type(insight_type)
        else:
            return list(self.engine.insights.values())
    
    async def get_recommendations(self) -> List[StrategicRecommendation]:
        """Get recommendations."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return list(self.engine.recommendations.values())
    
    async def get_agent_metrics(self, agent_id: str = None) -> List[AgentPerformanceMetrics]:
        """Get agent metrics."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.get_agent_metrics(agent_id)
    
    async def get_missions(self, status: MissionStatus = None) -> List[StrategicMission]:
        """Get missions."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if status:
            return self.engine.get_missions_by_status(status)
        else:
            return list(self.engine.missions.values())
    
    async def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        engine_status = self.engine.get_engine_status()
        analyzer_summary = self.analyzer.get_analysis_summary()
        
        return {
            'status': 'initialized',
            'engine': engine_status,
            'analyzer': analyzer_summary,
            'last_updated': datetime.now().isoformat()
        }
    
    async def cleanup_old_data(self, days: int = 30):
        """Cleanup old data."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        self.engine.cleanup_old_data(days)
    
    async def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Strategic Oversight Orchestrator")
        self.analyzer.shutdown()
        self.engine.shutdown()
        self.is_initialized = False
        self.logger.info("Strategic Oversight Orchestrator shutdown complete")