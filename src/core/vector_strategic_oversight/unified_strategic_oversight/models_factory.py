"""
Strategic Oversight Factory Models
==================================

Factory methods and validation utilities for strategic oversight operations.
V2 Compliance: < 250 lines, single responsibility, factory and validation logic.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from .models_core import (
    StrategicInsight, MissionObjective, ResourceAllocation,
    InsightType, ConfidenceLevel, ImpactLevel, MissionStatus, PriorityLevel
)
from .models_extended import (
    StrategicRecommendation, OversightReport, PerformanceMetrics,
    CoordinationPattern, StrategicContext, OversightConfig
)


class StrategicOversightModels:
    """Factory class for strategic oversight models."""
    
    @staticmethod
    def create_strategic_insight(
        title: str,
        description: str,
        insight_type: InsightType,
        confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM,
        impact_level: ImpactLevel = ImpactLevel.MEDIUM,
        context: Dict[str, Any] = None
    ) -> StrategicInsight:
        """Create strategic insight."""
        return StrategicInsight(
            insight_id=str(uuid.uuid4()),
            title=title,
            description=description,
            insight_type=insight_type,
            confidence_level=confidence_level,
            impact_level=impact_level,
            context=context or {},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    @staticmethod
    def create_mission_objective(
        mission_id: str,
        title: str,
        description: str,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        status: MissionStatus = MissionStatus.PENDING,
        target_date: Optional[datetime] = None
    ) -> MissionObjective:
        """Create mission objective."""
        return MissionObjective(
            objective_id=str(uuid.uuid4()),
            mission_id=mission_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            target_date=target_date,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_resource_allocation(
        resource_type: str,
        allocated_amount: float,
        used_amount: float = 0.0,
        efficiency_score: float = 1.0
    ) -> ResourceAllocation:
        """Create resource allocation."""
        return ResourceAllocation(
            allocation_id=str(uuid.uuid4()),
            resource_type=resource_type,
            allocated_amount=allocated_amount,
            used_amount=used_amount,
            available_amount=allocated_amount - used_amount,
            efficiency_score=efficiency_score,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_strategic_recommendation(
        title: str,
        description: str,
        insight_id: str,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        impact_level: ImpactLevel = ImpactLevel.MEDIUM,
        implementation_effort: str = "medium",
        expected_benefits: List[str] = None,
        risks: List[str] = None
    ) -> StrategicRecommendation:
        """Create strategic recommendation."""
        return StrategicRecommendation(
            recommendation_id=str(uuid.uuid4()),
            title=title,
            description=description,
            insight_id=insight_id,
            priority=priority,
            impact_level=impact_level,
            implementation_effort=implementation_effort,
            expected_benefits=expected_benefits or [],
            risks=risks or [],
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_oversight_report(
        title: str,
        report_type: str = "comprehensive",
        insights: List[StrategicInsight] = None,
        recommendations: List[StrategicRecommendation] = None,
        objectives: List[MissionObjective] = None,
        resource_allocations: List[ResourceAllocation] = None,
        summary: str = ""
    ) -> OversightReport:
        """Create oversight report."""
        return OversightReport(
            report_id=str(uuid.uuid4()),
            title=title,
            report_type=report_type,
            insights=insights or [],
            recommendations=recommendations or [],
            objectives=objectives or [],
            resource_allocations=resource_allocations or [],
            summary=summary,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_performance_metrics(
        mission_id: str,
        agent_id: str = "system",
        cpu_usage: float = 0.0,
        memory_usage: float = 0.0,
        execution_time: float = 0.0,
        success_rate: float = 1.0,
        error_count: int = 0,
        throughput: float = 0.0,
        latency: float = 0.0
    ) -> PerformanceMetrics:
        """Create performance metrics."""
        return PerformanceMetrics(
            metrics_id=str(uuid.uuid4()),
            mission_id=mission_id,
            agent_id=agent_id,
            timestamp=datetime.now(),
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            execution_time=execution_time,
            success_rate=success_rate,
            error_count=error_count,
            throughput=throughput,
            latency=latency
        )
    
    @staticmethod
    def create_oversight_config(
        analysis_interval: float = 60.0,
        confidence_threshold: float = 0.7,
        impact_threshold: float = 0.5,
        max_insights: int = 100,
        report_frequency: str = "daily"
    ) -> OversightConfig:
        """Create oversight config."""
        return OversightConfig(
            config_id=str(uuid.uuid4()),
            analysis_interval=analysis_interval,
            confidence_threshold=confidence_threshold,
            impact_threshold=impact_threshold,
            max_insights=max_insights,
            report_frequency=report_frequency,
            created_at=datetime.now()
        )
    
    @staticmethod
    def validate_strategic_insight(insight: StrategicInsight) -> Dict[str, Any]:
        """Validate strategic insight."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not insight.title:
            validation['errors'].append("Insight title is required")
            validation['is_valid'] = False
        
        if not insight.description:
            validation['warnings'].append("Insight description is recommended")
        
        return validation
    
    @staticmethod
    def validate_mission_objective(objective: MissionObjective) -> Dict[str, Any]:
        """Validate mission objective."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not objective.title:
            validation['errors'].append("Objective title is required")
            validation['is_valid'] = False
        
        if not objective.mission_id:
            validation['errors'].append("Mission ID is required")
            validation['is_valid'] = False
        
        return validation
