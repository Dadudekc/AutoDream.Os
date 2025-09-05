"""
Pattern Analysis Orchestrator
=============================

Main orchestrator for pattern analysis operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .models import (
    MissionPattern, PatternCorrelation, MissionContext,
    StrategicRecommendation, PatternAnalysisResult, PerformanceMetrics,
    PatternType, RecommendationType, ImpactLevel, PatternAnalysisConfig,
    PatternAnalysisModels
)
from .engine_core import PatternAnalysisEngine
from .analyzer import PatternAnalyzer


class PatternAnalysisOrchestrator:
    """Main orchestrator for pattern analysis system."""
    
    def __init__(self):
        """Initialize pattern analysis orchestrator."""
        self.engine = PatternAnalysisEngine()
        self.analyzer = PatternAnalyzer(self.engine)
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    async def initialize(self, config: PatternAnalysisConfig = None) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Pattern Analysis Orchestrator")
            
            # Initialize engine
            if not self.engine.initialize(config):
                raise Exception("Failed to initialize engine")
            
            # Initialize analyzer
            if not self.analyzer.initialize():
                raise Exception("Failed to initialize analyzer")
            
            self.is_initialized = True
            self.logger.info("Pattern Analysis Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Pattern Analysis Orchestrator: {e}")
            return False
    
    async def add_pattern(self, name: str, description: str, pattern_type: PatternType,
                         frequency: float, confidence: float, context: Dict[str, Any]) -> bool:
        """Add mission pattern."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        pattern = PatternAnalysisModels.create_mission_pattern(
            name=name,
            description=description,
            pattern_type=pattern_type,
            frequency=frequency,
            confidence=confidence,
            context=context
        )
        
        return self.engine.add_pattern(pattern)
    
    async def add_correlation(self, pattern1_id: str, pattern2_id: str,
                             correlation_score: float, significance: float,
                             relationship_type: str) -> bool:
        """Add pattern correlation."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        correlation = PatternAnalysisModels.create_pattern_correlation(
            pattern1_id=pattern1_id,
            pattern2_id=pattern2_id,
            correlation_score=correlation_score,
            significance=significance,
            relationship_type=relationship_type
        )
        
        return self.engine.add_correlation(correlation)
    
    async def add_context(self, mission_id: str, phase: str, priority: str,
                         resources: Dict[str, Any], constraints: List[str],
                         objectives: List[str]) -> bool:
        """Add mission context."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        context = PatternAnalysisModels.create_mission_context(
            mission_id=mission_id,
            phase=phase,
            priority=priority,
            resources=resources,
            constraints=constraints,
            objectives=objectives
        )
        
        return self.engine.add_context(context)
    
    async def add_metrics(self, mission_id: str, phase: str, efficiency: float,
                         completion_time: float, resource_utilization: float,
                         quality_score: float, metrics_data: Dict[str, Any]) -> bool:
        """Add performance metrics."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        metrics = PatternAnalysisModels.create_performance_metrics(
            mission_id=mission_id,
            phase=phase,
            efficiency=efficiency,
            completion_time=completion_time,
            resource_utilization=resource_utilization,
            quality_score=quality_score,
            metrics_data=metrics_data
        )
        
        return self.engine.add_metrics(metrics)
    
    async def analyze_patterns(self, analysis_type: str = "comprehensive") -> Optional[PatternAnalysisResult]:
        """Analyze patterns."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.analyze_patterns(analysis_type)
    
    async def analyze_performance_patterns(self, mission_id: str = None) -> List[MissionPattern]:
        """Analyze performance patterns."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.analyzer.analyze_performance_patterns(mission_id)
    
    async def analyze_coordination_patterns(self, mission_id: str = None) -> List[MissionPattern]:
        """Analyze coordination patterns."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.analyzer.analyze_coordination_patterns(mission_id)
    
    async def generate_recommendations(self, patterns: List[MissionPattern]) -> List[StrategicRecommendation]:
        """Generate strategic recommendations."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.analyzer.generate_optimization_recommendations(patterns)
    
    async def get_patterns(self, pattern_type: PatternType = None) -> List[MissionPattern]:
        """Get patterns."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if pattern_type:
            return self.engine.get_patterns_by_type(pattern_type)
        else:
            return list(self.engine.patterns.values())
    
    async def get_correlations(self) -> List[PatternCorrelation]:
        """Get correlations."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return list(self.engine.correlations.values())
    
    async def get_recommendations(self) -> List[StrategicRecommendation]:
        """Get recommendations."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return list(self.engine.recommendations.values())
    
    async def get_analysis_results(self, limit: int = 10) -> List[PatternAnalysisResult]:
        """Get analysis results."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.get_recent_results(limit)
    
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
        self.analyzer.cleanup_old_analysis(days)
    
    async def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Pattern Analysis Orchestrator")
        self.analyzer.shutdown()
        self.engine.shutdown()
        self.is_initialized = False
        self.logger.info("Pattern Analysis Orchestrator shutdown complete")