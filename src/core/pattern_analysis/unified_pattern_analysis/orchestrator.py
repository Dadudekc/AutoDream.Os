"""
Pattern Analysis Orchestrator
=============================

Main orchestrator for pattern analysis operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from .models import (
    MissionPattern, PatternCorrelation, MissionContext,
    StrategicRecommendation, PatternAnalysisResult, PerformanceMetrics,
    PatternType, RecommendationType, ImpactLevel
)
from .engine import PatternAnalysisEngine, PatternAnalysisConfig
from .analyzer import PatternAnalyzer


class PatternAnalysisOrchestrator:
    """Main orchestrator for pattern analysis operations."""
    
    def __init__(self):
        """Initialize pattern analysis orchestrator."""
        self.engine = PatternAnalysisEngine()
        self.analyzer = PatternAnalyzer()
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
        self.config: Optional[PatternAnalysisConfig] = None
    
    async def initialize(self, config: PatternAnalysisConfig = None) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Pattern Analysis Orchestrator")
            
            # Set default config if not provided
            if config is None:
                config = PatternAnalysisConfig(
                    config_id="default",
                    name="Default Pattern Analysis Config",
                    description="Default pattern analysis configuration"
                )
            
            self.config = config
            
            # Initialize engine
            if not self.engine.initialize(config):
                raise Exception("Failed to initialize engine")
            
            self.is_initialized = True
            self.logger.info("Pattern Analysis Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Pattern Analysis Orchestrator: {e}")
            return False
    
    async def add_pattern(self, pattern: MissionPattern) -> bool:
        """Add pattern to analysis."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.add_pattern(pattern)
    
    async def add_correlation(self, correlation: PatternCorrelation) -> bool:
        """Add pattern correlation."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.add_correlation(correlation)
    
    async def add_context(self, context: MissionContext) -> bool:
        """Add mission context."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.add_context(context)
    
    async def analyze_patterns(self, analysis_type: str = "comprehensive") -> PatternAnalysisResult:
        """Analyze patterns and generate results."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.analyze_patterns(analysis_type)
    
    async def analyze_pattern_type(self, pattern_type: PatternType) -> List[StrategicRecommendation]:
        """Analyze patterns of specific type."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        patterns = [p for p in self.engine.patterns.values() if p.pattern_type == pattern_type]
        return self.analyzer.analyze_pattern_type(pattern_type, patterns)
    
    async def get_pattern_metrics(self) -> PerformanceMetrics:
        """Get pattern analysis metrics."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.get_pattern_metrics()
    
    async def get_recent_results(self, limit: int = 10) -> List[PatternAnalysisResult]:
        """Get recent analysis results."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.get_recent_results(limit)
    
    async def get_patterns_by_type(self, pattern_type: PatternType) -> List[MissionPattern]:
        """Get patterns by type."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [p for p in self.engine.patterns.values() if p.pattern_type == pattern_type]
    
    async def get_high_confidence_patterns(self, threshold: float = 0.8) -> List[MissionPattern]:
        """Get high confidence patterns."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [p for p in self.engine.patterns.values() if p.confidence_score >= threshold]
    
    async def get_success_patterns(self, threshold: float = 0.7) -> List[MissionPattern]:
        """Get high success rate patterns."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [p for p in self.engine.patterns.values() if p.success_rate >= threshold]
    
    async def get_failure_patterns(self, threshold: float = 0.3) -> List[MissionPattern]:
        """Get low success rate patterns."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [p for p in self.engine.patterns.values() if p.success_rate <= threshold]
    
    async def get_pattern_quality_analysis(self, pattern_id: str) -> Dict[str, Any]:
        """Get pattern quality analysis."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        if pattern_id not in self.engine.patterns:
            raise ValueError(f"Pattern {pattern_id} not found")
        
        pattern = self.engine.patterns[pattern_id]
        return self.analyzer.analyze_pattern_quality(pattern)
    
    async def get_correlation_analysis(self) -> List[StrategicRecommendation]:
        """Get correlation analysis recommendations."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        correlations = list(self.engine.correlations.values())
        return self.analyzer.analyze_correlations(correlations)
    
    async def get_strategic_recommendations(self, limit: int = 20) -> List[StrategicRecommendation]:
        """Get strategic recommendations."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        # Get recommendations from all pattern types
        all_recommendations = []
        
        for pattern_type in PatternType:
            patterns = await self.get_patterns_by_type(pattern_type)
            recommendations = self.analyzer.analyze_pattern_type(pattern_type, patterns)
            all_recommendations.extend(recommendations)
        
        # Add correlation-based recommendations
        correlation_recommendations = await self.get_correlation_analysis()
        all_recommendations.extend(correlation_recommendations)
        
        # Sort by priority score and return top recommendations
        all_recommendations.sort(key=lambda x: x.priority_score, reverse=True)
        return all_recommendations[:limit]
    
    async def clear_old_data(self, days: int = 30):
        """Clear old analysis data."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        self.engine.clear_old_data(days)
        self.logger.info(f"Cleared pattern analysis data older than {days} days")
    
    def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Pattern Analysis Orchestrator")
        self.is_initialized = False
    
    def get_config(self) -> Optional[PatternAnalysisConfig]:
        """Get current configuration."""
        return self.config
    
    async def update_config(self, config: PatternAnalysisConfig) -> bool:
        """Update configuration."""
        try:
            self.config = config
            
            # Reinitialize engine with new config
            if not self.engine.initialize(config):
                raise Exception("Failed to reinitialize engine with new config")
            
            self.logger.info("Configuration updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating configuration: {e}")
            return False
    
    async def get_analysis_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        metrics = await self.get_pattern_metrics()
        recent_results = await self.get_recent_results(5)
        
        return {
            'status': 'active',
            'metrics': metrics.to_dict(),
            'recent_results_count': len(recent_results),
            'config': {
                'name': self.config.name if self.config else 'Unknown',
                'enabled': self.config.enabled if self.config else False,
                'analysis_interval': self.config.analysis_interval if self.config else 0
            },
            'last_updated': datetime.now().isoformat()
        }
