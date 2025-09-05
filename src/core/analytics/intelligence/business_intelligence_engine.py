#!/usr/bin/env python3
"""
Business Intelligence Engine - KISS Compliant
=============================================

Simple business intelligence for analytics.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import statistics
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BusinessIntelligenceEngine:
    """Simple business intelligence engine."""
    
    def __init__(self, config=None):
        """Initialize business intelligence engine."""
        self.config = config or {}
        self.thresholds = {
            'trend_significance': 0.05,
            'performance_threshold': 0.8,
            'efficiency_target': 0.85
        }
        self.logger = logger
    
    def analyze_trends(self, data: List[float]) -> Dict[str, Any]:
        """Analyze trends in data."""
        if not data or len(data) < 2:
            return {"trend": "insufficient_data", "slope": 0, "confidence": 0}
        
        try:
            # Simple linear trend calculation
            n = len(data)
            x = list(range(n))
            y = data
            
            # Calculate slope
            slope = self._calculate_slope(x, y)
            
            # Determine trend
            if abs(slope) < self.thresholds['trend_significance']:
                trend = "stable"
            elif slope > 0:
                trend = "increasing"
            else:
                trend = "decreasing"
            
            # Calculate confidence
            confidence = min(abs(slope) * 10, 1.0)
            
            return {
                "trend": trend,
                "slope": slope,
                "confidence": confidence,
                "data_points": n
            }
        except Exception as e:
            self.logger.error(f"Error in trend analysis: {e}")
            return {"trend": "error", "slope": 0, "confidence": 0}
    
    def calculate_efficiency(self, input_data: List[float], output_data: List[float]) -> Dict[str, Any]:
        """Calculate efficiency metrics."""
        if not input_data or not output_data or len(input_data) != len(output_data):
            return {"efficiency": 0, "status": "invalid_data"}
        
        try:
            # Simple efficiency calculation
            total_input = sum(input_data)
            total_output = sum(output_data)
            
            if total_input == 0:
                return {"efficiency": 0, "status": "zero_input"}
            
            efficiency = total_output / total_input
            status = "good" if efficiency >= self.thresholds['efficiency_target'] else "needs_improvement"
            
            return {
                "efficiency": efficiency,
                "status": status,
                "input_total": total_input,
                "output_total": total_output
            }
        except Exception as e:
            self.logger.error(f"Error in efficiency calculation: {e}")
            return {"efficiency": 0, "status": "error"}
    
    def generate_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate business insights."""
        insights = []
        
        # Trend insight
        if 'trend_data' in data:
            trend = self.analyze_trends(data['trend_data'])
            if trend['trend'] != 'stable':
                insights.append({
                    'type': 'trend',
                    'message': f"Data shows {trend['trend']} trend with {trend['confidence']:.2f} confidence",
                    'priority': 'medium'
                })
        
        # Efficiency insight
        if 'input_data' in data and 'output_data' in data:
            efficiency = self.calculate_efficiency(data['input_data'], data['output_data'])
            if efficiency['status'] == 'needs_improvement':
                insights.append({
                    'type': 'efficiency',
                    'message': f"Efficiency is {efficiency['efficiency']:.2f}, below target of {self.thresholds['efficiency_target']}",
                    'priority': 'high'
                })
        
        return insights
    
    def _calculate_slope(self, x: List[float], y: List[float]) -> float:
        """Calculate slope of linear regression."""
        n = len(x)
        if n < 2:
            return 0
        
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        return (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)

__all__ = ["BusinessIntelligenceEngine"]