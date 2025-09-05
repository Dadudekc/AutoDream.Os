"""
Strategic Oversight Orchestrator
================================

Main orchestrator for vector strategic oversight operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
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
from .engine import StrategicOversightEngine
from .analyzer import StrategicOversightAnalyzer


class VectorStrategicOversightOrchestrator:
    """Main orchestrator for vector strategic oversight operations."""
    
    def __init__(self):
        """Initialize strategic oversight orchestrator."""
        self.engine = StrategicOversightEngine()
        self.analyzer = StrategicOversightAnalyzer()
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Vector Strategic Oversight Orchestrator")
            
            # Initialize with default data
            await self._load_default_data()
            
            self.is_initialized = True
            self.logger.info("Vector Strategic Oversight Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Vector Strategic Oversight Orchestrator: {e}")
            return False
    
    async def _load_default_data(self):
        """Load default data for initialization."""
        # Load default agent capabilities
        default_agent = AgentCapabilities(
            agent_id="Agent-3",
            capabilities=["infrastructure", "devops", "v2_compliance"],
            proficiency_scores={"infrastructure": 0.9, "devops": 0.8, "v2_compliance": 0.95},
            availability=True,
            current_workload=0.3
        )
        await self.engine.add_agent_capabilities(default_agent)
        
        # Load default mission status
        default_mission = MissionStatus(
            mission_id="default_mission",
            mission_name="V2 Compliance Refactoring",
            status=MissionStatus.ACTIVE,
            progress_percentage=75.0,
            assigned_agents=["Agent-3"],
            current_phase="refactoring"
        )
        await self.engine.add_mission_status(default_mission)
    
    async def generate_oversight_report(
        self,
        report_type: str = "comprehensive",
        title: str = "Strategic Oversight Report",
        include_insights: bool = True,
        include_recommendations: bool = True
    ) -> StrategicOversightReport:
        """Generate strategic oversight report."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.generate_oversight_report(
            report_type=report_type,
            title=title,
            include_insights=include_insights,
            include_recommendations=include_recommendations
        )
    
    async def analyze_swarm_coordination(
        self,
        agent_data: List[Dict[str, Any]] = None,
        mission_data: List[Dict[str, Any]] = None,
        time_window_hours: int = 24
    ) -> List[SwarmCoordinationInsight]:
        """Analyze swarm coordination patterns."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        # Use default data if not provided
        if agent_data is None:
            agent_data = [{"id": "Agent-3", "active": True, "workload": 0.3}]
        
        if mission_data is None:
            mission_data = [{"id": "mission_1", "status": "active"}]
        
        return await self.analyzer.analyze_swarm_coordination(
            agent_data=agent_data,
            mission_data=mission_data,
            time_window_hours=time_window_hours
        )
    
    async def detect_patterns(
        self,
        data: List[Dict[str, Any]],
        pattern_types: List[str] = None
    ) -> List[PatternAnalysis]:
        """Detect patterns in data."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.analyzer.detect_patterns(data, pattern_types)
    
    async def predict_success(
        self,
        task_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None
    ) -> SuccessPrediction:
        """Predict task success probability."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.analyzer.predict_success(task_data, historical_data)
    
    async def add_mission_status(self, mission: MissionStatus) -> bool:
        """Add mission status."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_mission_status(mission)
    
    async def add_agent_capabilities(self, capabilities: AgentCapabilities) -> bool:
        """Add agent capabilities."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_agent_capabilities(capabilities)
    
    async def add_emergency_status(self, emergency: EmergencyStatus) -> bool:
        """Add emergency status."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_emergency_status(emergency)
    
    async def add_risk_assessment(self, risk: RiskAssessment) -> bool:
        """Add risk assessment."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_risk_assessment(risk)
    
    async def add_intervention_history(self, intervention: InterventionHistory) -> bool:
        """Add intervention history."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_intervention_history(intervention)
    
    def get_oversight_summary(self) -> Dict[str, Any]:
        """Get oversight summary."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        engine_summary = self.engine.get_oversight_summary()
        analyzer_summary = self.analyzer.get_analysis_summary()
        
        return {
            **engine_summary,
            "analysis_summary": analyzer_summary
        }
    
    def get_mission_status(self, mission_id: str) -> Optional[MissionStatus]:
        """Get mission status by ID."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.missions.get(mission_id)
    
    def get_agent_capabilities(self, agent_id: str) -> Optional[AgentCapabilities]:
        """Get agent capabilities by ID."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.agent_capabilities.get(agent_id)
    
    def get_emergency_status(self, emergency_id: str) -> Optional[EmergencyStatus]:
        """Get emergency status by ID."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.emergencies.get(emergency_id)
    
    def get_risk_assessment(self, assessment_id: str) -> Optional[RiskAssessment]:
        """Get risk assessment by ID."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.risks.get(assessment_id)
    
    def clear_all_data(self):
        """Clear all data."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        self.engine.clear_all_data()
        self.analyzer.clear_analysis_data()
        self.logger.info("All data cleared")
    
    def shutdown(self):
        """Shutdown orchestrator."""
        self.logger.info("Shutting down Vector Strategic Oversight Orchestrator")
        self.is_initialized = False
