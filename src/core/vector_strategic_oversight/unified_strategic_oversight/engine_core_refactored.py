"""
Strategic Oversight Engine Core Refactored - KISS Simplified
===========================================================

Refactored strategic oversight engine core with modular architecture.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined core engine logic.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .models import (
    StrategicOversightReport, SwarmCoordinationInsight, StrategicRecommendation,
    AgentPerformanceMetrics, SwarmCoordinationStatus, StrategicMission,
    VectorDatabaseMetrics, SystemHealthMetrics
)
from .enums import (
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, ReportType,
    PriorityLevel, AgentRole
)
from .engine_core_base import StrategicOversightEngineCoreBase
from .engine_core_reports import StrategicOversightEngineCoreReports
from .engine_core_insights import StrategicOversightEngineCoreInsights
from .engine_core_recommendations import StrategicOversightEngineCoreRecommendations
from .engine_core_metrics import StrategicOversightEngineCoreMetrics
from .engine_core_missions import StrategicOversightEngineCoreMissions


class StrategicOversightEngineCore(StrategicOversightEngineCoreBase):
    """Refactored strategic oversight engine core with modular architecture."""
    
    def __init__(self):
        """Initialize refactored strategic oversight engine core."""
        super().__init__()
        
        # Initialize modular components
        self.reports_manager = StrategicOversightEngineCoreReports(self.reports, self.logger)
        self.insights_manager = StrategicOversightEngineCoreInsights(self.insights, self.logger)
        self.recommendations_manager = StrategicOversightEngineCoreRecommendations(self.recommendations, self.logger)
        self.metrics_manager = StrategicOversightEngineCoreMetrics(
            self.agent_metrics, self.coordination_status, self.logger
        )
        self.missions_manager = StrategicOversightEngineCoreMissions(self.missions, self.logger)
    
    # Delegate report operations to reports manager
    def add_report(self, report: StrategicOversightReport) -> bool:
        """Add a strategic oversight report."""
        return self.reports_manager.add_report(report)
    
    def get_report(self, report_id: str) -> Optional[StrategicOversightReport]:
        """Get a strategic oversight report by ID."""
        return self.reports_manager.get_report(report_id)
    
    def get_reports(self, report_type: ReportType = None, limit: int = 10) -> List[StrategicOversightReport]:
        """Get strategic oversight reports."""
        return self.reports_manager.get_reports(report_type, limit)
    
    # Delegate insight operations to insights manager
    def add_insight(self, insight: SwarmCoordinationInsight) -> bool:
        """Add a swarm coordination insight."""
        return self.insights_manager.add_insight(insight)
    
    def get_insight(self, insight_id: str) -> Optional[SwarmCoordinationInsight]:
        """Get a swarm coordination insight by ID."""
        return self.insights_manager.get_insight(insight_id)
    
    def get_insights(self, insight_type: InsightType = None, limit: int = 10) -> List[SwarmCoordinationInsight]:
        """Get swarm coordination insights."""
        return self.insights_manager.get_insights(insight_type, limit)
    
    # Delegate recommendation operations to recommendations manager
    def add_recommendation(self, recommendation: StrategicRecommendation) -> bool:
        """Add a strategic recommendation."""
        return self.recommendations_manager.add_recommendation(recommendation)
    
    def get_recommendation(self, recommendation_id: str) -> Optional[StrategicRecommendation]:
        """Get a strategic recommendation by ID."""
        return self.recommendations_manager.get_recommendation(recommendation_id)
    
    def get_recommendations(self, priority: PriorityLevel = None, limit: int = 10) -> List[StrategicRecommendation]:
        """Get strategic recommendations."""
        return self.recommendations_manager.get_recommendations(priority, limit)
    
    # Delegate metrics operations to metrics manager
    def add_agent_metrics(self, metrics: AgentPerformanceMetrics) -> bool:
        """Add agent performance metrics."""
        return self.metrics_manager.add_agent_metrics(metrics)
    
    def get_agent_metrics(self, agent_id: str) -> Optional[AgentPerformanceMetrics]:
        """Get agent performance metrics by agent ID."""
        return self.metrics_manager.get_agent_metrics(agent_id)
    
    def get_all_agent_metrics(self) -> List[AgentPerformanceMetrics]:
        """Get all agent performance metrics."""
        return self.metrics_manager.get_all_agent_metrics()
    
    def add_coordination_status(self, status: SwarmCoordinationStatus) -> bool:
        """Add swarm coordination status."""
        return self.metrics_manager.add_coordination_status(status)
    
    def get_coordination_status(self, status_id: str) -> Optional[SwarmCoordinationStatus]:
        """Get swarm coordination status by ID."""
        return self.metrics_manager.get_coordination_status(status_id)
    
    def get_latest_coordination_status(self) -> Optional[SwarmCoordinationStatus]:
        """Get latest swarm coordination status."""
        return self.metrics_manager.get_latest_coordination_status()
    
    # Delegate mission operations to missions manager
    def add_mission(self, mission: StrategicMission) -> bool:
        """Add a strategic mission."""
        return self.missions_manager.add_mission(mission)
    
    def get_mission(self, mission_id: str) -> Optional[StrategicMission]:
        """Get a strategic mission by ID."""
        return self.missions_manager.get_mission(mission_id)
    
    def get_missions(self, status: MissionStatus = None, limit: int = 10) -> List[StrategicMission]:
        """Get strategic missions."""
        return self.missions_manager.get_missions(status, limit)
