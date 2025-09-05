"""
Strategic Oversight Analyzer - V2 Compliant Module
=================================================

Main analyzer for strategic oversight operations.
Coordinates all analyzer components and provides unified interface.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

from ..models import (
    StrategicOversightReport, SwarmCoordinationInsight, PatternAnalysis,
    SuccessPrediction, RiskAssessment, InsightType, ConfidenceLevel, ImpactLevel
)
from .swarm_analyzer import SwarmCoordinationAnalyzer
from .pattern_analyzer import PatternAnalyzer
from .prediction_analyzer import PredictionAnalyzer


class StrategicOversightAnalyzer:
    """
    Main strategic oversight analyzer.
    
    Coordinates all analyzer components and provides unified interface
    for strategic oversight analysis operations.
    """
    
    def __init__(self):
        """Initialize strategic oversight analyzer."""
        self.swarm_analyzer = SwarmCoordinationAnalyzer()
        self.pattern_analyzer = PatternAnalyzer()
        self.prediction_analyzer = PredictionAnalyzer()
        self.analysis_history: List[Dict[str, Any]] = []
        self.analysis_metrics: Dict[str, float] = {}
    
    async def analyze_swarm_coordination(
        self,
        agent_data: List[Dict[str, Any]],
        mission_data: List[Dict[str, Any]],
        time_window_hours: int = 24
    ) -> List[SwarmCoordinationInsight]:
        """Analyze swarm coordination patterns."""
        return await self.swarm_analyzer.analyze_swarm_coordination(
            agent_data, mission_data, time_window_hours
        )
    
    async def detect_patterns(
        self,
        data: List[Dict[str, Any]],
        pattern_types: List[str] = None
    ) -> List[PatternAnalysis]:
        """Detect patterns in data."""
        return await self.pattern_analyzer.detect_patterns(data, pattern_types)
    
    async def predict_success(
        self,
        task_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None
    ) -> SuccessPrediction:
        """Predict task success probability."""
        return await self.prediction_analyzer.predict_success(task_data, historical_data)
    
    async def assess_risk(
        self,
        task_data: Dict[str, Any],
        context_data: List[Dict[str, Any]] = None
    ) -> RiskAssessment:
        """Assess risk for task or operation."""
        return await self.prediction_analyzer.assess_risk(task_data, context_data)
    
    async def generate_comprehensive_analysis(
        self,
        agent_data: List[Dict[str, Any]],
        mission_data: List[Dict[str, Any]],
        task_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None
    ) -> StrategicOversightReport:
        """Generate comprehensive strategic oversight analysis."""
        try:
            # Analyze swarm coordination
            swarm_insights = await self.analyze_swarm_coordination(agent_data, mission_data)
            
            # Detect patterns
            patterns = await self.detect_patterns(mission_data)
            
            # Predict success
            success_prediction = await self.predict_success(task_data, historical_data)
            
            # Assess risk
            risk_assessment = await self.assess_risk(task_data, mission_data)
            
            # Generate comprehensive report
            report = StrategicOversightReport(
                report_id=f"comprehensive_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                report_type="comprehensive_analysis",
                generated_at=datetime.now(),
                swarm_insights=swarm_insights,
                patterns=patterns,
                success_prediction=success_prediction,
                risk_assessment=risk_assessment,
                summary=f"Comprehensive analysis completed with {len(swarm_insights)} insights, {len(patterns)} patterns, and risk level {risk_assessment.risk_level}",
                recommendations=[
                    "Monitor swarm coordination patterns",
                    "Track pattern evolution",
                    "Implement risk mitigation strategies"
                ]
            )
            
            # Record analysis
            self.analysis_history.append({
                "timestamp": datetime.now().isoformat(),
                "analysis_type": "comprehensive",
                "agent_count": len(agent_data),
                "mission_count": len(mission_data),
                "insights_count": len(swarm_insights),
                "patterns_count": len(patterns)
            })
            
            return report
            
        except Exception as e:
            # Return error report
            return StrategicOversightReport(
                report_id=f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                report_type="error",
                generated_at=datetime.now(),
                swarm_insights=[],
                patterns=[],
                success_prediction=None,
                risk_assessment=None,
                summary=f"Analysis failed: {str(e)}",
                recommendations=["Manual analysis required"]
            )
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get comprehensive analysis summary."""
        return {
            "total_analyses": len(self.analysis_history),
            "swarm_analyzer": self.swarm_analyzer.get_analysis_summary(),
            "pattern_analyzer": self.pattern_analyzer.get_analysis_summary(),
            "prediction_analyzer": self.prediction_analyzer.get_analysis_summary(),
            "analysis_metrics": self.analysis_metrics.copy(),
            "last_analysis": self.analysis_history[-1] if self.analysis_history else None
        }
    
    def clear_analysis_data(self):
        """Clear all analysis data."""
        self.analysis_history.clear()
        self.analysis_metrics.clear()
        self.swarm_analyzer.clear_analysis_data()
        self.pattern_analyzer.clear_analysis_data()
        self.prediction_analyzer.clear_analysis_data()
    
    def get_analyzer_status(self) -> Dict[str, Any]:
        """Get analyzer status."""
        return {
            'main_analyzer': {
                'analysis_history_count': len(self.analysis_history),
                'metrics_count': len(self.analysis_metrics)
            },
            'swarm_analyzer': self.swarm_analyzer.get_analyzer_status(),
            'pattern_analyzer': self.pattern_analyzer.get_analyzer_status(),
            'prediction_analyzer': self.prediction_analyzer.get_analyzer_status()
        }
