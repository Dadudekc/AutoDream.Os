"""
Pattern Analysis Factory Models
===============================

Factory methods and validation utilities for pattern analysis operations.
V2 Compliance: < 200 lines, single responsibility, factory and validation logic.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from .models_core import (
    MissionPattern, PatternCorrelation, MissionContext,
    PatternType, RecommendationType, ImpactLevel
)
from .models_extended import (
    StrategicRecommendation, PatternAnalysisResult, PerformanceMetrics,
    ResourceUtilization, TimingPattern, CoordinationPattern
)


@dataclass
class PatternAnalysisConfig:
    """Pattern analysis configuration."""
    config_id: str
    analysis_interval: float
    correlation_threshold: float
    confidence_threshold: float
    max_patterns: int
    analysis_depth: int
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class PatternAnalysisModels:
    """Factory class for pattern analysis models."""
    
    @staticmethod
    def create_mission_pattern(
        name: str,
        description: str,
        pattern_type: PatternType,
        frequency: float = 0.5,
        confidence: float = 0.8,
        context: Dict[str, Any] = None
    ) -> MissionPattern:
        """Create mission pattern."""
        return MissionPattern(
            pattern_id=str(uuid.uuid4()),
            name=name,
            description=description,
            pattern_type=pattern_type,
            frequency=frequency,
            confidence=confidence,
            context=context or {},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    @staticmethod
    def create_pattern_correlation(
        pattern1_id: str,
        pattern2_id: str,
        correlation_score: float,
        significance: float = 0.8,
        relationship_type: str = "positive"
    ) -> PatternCorrelation:
        """Create pattern correlation."""
        return PatternCorrelation(
            correlation_id=str(uuid.uuid4()),
            pattern1_id=pattern1_id,
            pattern2_id=pattern2_id,
            correlation_score=correlation_score,
            significance=significance,
            relationship_type=relationship_type,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_mission_context(
        mission_id: str,
        phase: str = "execution",
        priority: str = "medium",
        resources: Dict[str, Any] = None,
        constraints: List[str] = None,
        objectives: List[str] = None
    ) -> MissionContext:
        """Create mission context."""
        return MissionContext(
            context_id=str(uuid.uuid4()),
            mission_id=mission_id,
            phase=phase,
            priority=priority,
            resources=resources or {},
            constraints=constraints or [],
            objectives=objectives or [],
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_strategic_recommendation(
        title: str,
        description: str,
        recommendation_type: RecommendationType,
        impact_level: ImpactLevel,
        priority: int = 1,
        implementation_effort: str = "medium",
        expected_benefits: List[str] = None,
        risks: List[str] = None
    ) -> StrategicRecommendation:
        """Create strategic recommendation."""
        return StrategicRecommendation(
            recommendation_id=str(uuid.uuid4()),
            title=title,
            description=description,
            recommendation_type=recommendation_type,
            impact_level=impact_level,
            priority=priority,
            implementation_effort=implementation_effort,
            expected_benefits=expected_benefits or [],
            risks=risks or [],
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_pattern_analysis_result(
        analysis_type: str = "comprehensive",
        patterns_found: List[MissionPattern] = None,
        correlations: List[PatternCorrelation] = None,
        recommendations: List[StrategicRecommendation] = None,
        confidence_score: float = 0.8,
        analysis_metadata: Dict[str, Any] = None
    ) -> PatternAnalysisResult:
        """Create pattern analysis result."""
        return PatternAnalysisResult(
            result_id=str(uuid.uuid4()),
            analysis_type=analysis_type,
            patterns_found=patterns_found or [],
            correlations=correlations or [],
            recommendations=recommendations or [],
            confidence_score=confidence_score,
            analysis_metadata=analysis_metadata or {},
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
    def create_pattern_analysis_config(
        analysis_interval: float = 60.0,
        correlation_threshold: float = 0.7,
        confidence_threshold: float = 0.8,
        max_patterns: int = 100,
        analysis_depth: int = 3
    ) -> PatternAnalysisConfig:
        """Create pattern analysis config."""
        return PatternAnalysisConfig(
            config_id=str(uuid.uuid4()),
            analysis_interval=analysis_interval,
            correlation_threshold=correlation_threshold,
            confidence_threshold=confidence_threshold,
            max_patterns=max_patterns,
            analysis_depth=analysis_depth,
            created_at=datetime.now()
        )
    
    @staticmethod
    def validate_mission_pattern(pattern: MissionPattern) -> Dict[str, Any]:
        """Validate mission pattern."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not pattern.name:
            validation['errors'].append("Pattern name is required")
            validation['is_valid'] = False
        
        if pattern.frequency < 0 or pattern.frequency > 1:
            validation['warnings'].append("Frequency should be between 0 and 1")
        
        if pattern.confidence < 0 or pattern.confidence > 1:
            validation['warnings'].append("Confidence should be between 0 and 1")
        
        return validation
    
    @staticmethod
    def validate_pattern_correlation(correlation: PatternCorrelation) -> Dict[str, Any]:
        """Validate pattern correlation."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not correlation.pattern1_id or not correlation.pattern2_id:
            validation['errors'].append("Both pattern IDs are required")
            validation['is_valid'] = False
        
        if correlation.correlation_score < -1 or correlation.correlation_score > 1:
            validation['warnings'].append("Correlation score should be between -1 and 1")
        
        if correlation.significance < 0 or correlation.significance > 1:
            validation['warnings'].append("Significance should be between 0 and 1")
        
        return validation
