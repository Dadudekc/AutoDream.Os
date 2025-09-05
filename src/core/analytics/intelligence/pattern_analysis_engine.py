#!/usr/bin/env python3
"""
Pattern Analysis Engine - KISS Compliant
========================================

Simple pattern analysis for analytics.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import statistics
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import Counter

logger = logging.getLogger(__name__)

class PatternAnalysisEngine:
    """Simple pattern analysis engine."""
    
    def __init__(self, config=None):
        """Initialize pattern analysis engine."""
        self.config = config or {}
        self.logger = logger
        self.patterns = {}
        self.analysis_history = []
    
    def analyze_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in data."""
        try:
            if not data:
                return {"error": "No data provided"}
            
            # Simple pattern analysis
            patterns = self._extract_patterns(data)
            trends = self._analyze_trends(data)
            anomalies = self._detect_anomalies(data)
            
            analysis_result = {
                "patterns": patterns,
                "trends": trends,
                "anomalies": anomalies,
                "data_points": len(data),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in history
            self.analysis_history.append(analysis_result)
            if len(self.analysis_history) > 100:  # Keep only last 100
                self.analysis_history.pop(0)
            
            self.logger.info(f"Pattern analysis completed: {len(patterns)} patterns found")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error analyzing patterns: {e}")
            return {"error": str(e)}
    
    def _extract_patterns(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract patterns from data."""
        try:
            patterns = []
            
            # Simple pattern extraction
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, (int, float)):
                            patterns.append({
                                "field": key,
                                "value": value,
                                "type": "numeric"
                            })
                        elif isinstance(value, str):
                            patterns.append({
                                "field": key,
                                "value": value,
                                "type": "text"
                            })
            
            return patterns[:10]  # Limit to 10 patterns
        except Exception as e:
            self.logger.error(f"Error extracting patterns: {e}")
            return []
    
    def _analyze_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in data."""
        try:
            if not data:
                return {"trend": "no_data"}
            
            # Simple trend analysis
            numeric_values = []
            for item in data:
                if isinstance(item, dict):
                    for value in item.values():
                        if isinstance(value, (int, float)):
                            numeric_values.append(value)
            
            if not numeric_values:
                return {"trend": "no_numeric_data"}
            
            # Calculate simple trend
            if len(numeric_values) >= 2:
                first_half = numeric_values[:len(numeric_values)//2]
                second_half = numeric_values[len(numeric_values)//2:]
                
                first_avg = statistics.mean(first_half)
                second_avg = statistics.mean(second_half)
                
                if second_avg > first_avg * 1.1:
                    trend = "increasing"
                elif second_avg < first_avg * 0.9:
                    trend = "decreasing"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            return {
                "trend": trend,
                "data_points": len(numeric_values),
                "avg_value": round(statistics.mean(numeric_values), 3)
            }
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {e}")
            return {"trend": "error"}
    
    def _detect_anomalies(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in data."""
        try:
            anomalies = []
            
            # Simple anomaly detection
            numeric_values = []
            for item in data:
                if isinstance(item, dict):
                    for value in item.values():
                        if isinstance(value, (int, float)):
                            numeric_values.append(value)
            
            if len(numeric_values) < 3:
                return anomalies
            
            # Calculate mean and standard deviation
            mean_val = statistics.mean(numeric_values)
            stdev_val = statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0
            
            # Find values that are more than 2 standard deviations from mean
            threshold = 2 * stdev_val
            for i, value in enumerate(numeric_values):
                if abs(value - mean_val) > threshold:
                    anomalies.append({
                        "index": i,
                        "value": value,
                        "deviation": round(abs(value - mean_val), 3)
                    })
            
            return anomalies[:5]  # Limit to 5 anomalies
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {e}")
            return []
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        try:
            if not self.analysis_history:
                return {"message": "No analysis data available"}
            
            total_analyses = len(self.analysis_history)
            recent_analysis = self.analysis_history[-1] if self.analysis_history else {}
            
            return {
                "total_analyses": total_analyses,
                "recent_analysis": recent_analysis,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting analysis summary: {e}")
            return {"error": str(e)}
    
    def clear_analysis_history(self) -> None:
        """Clear analysis history."""
        self.analysis_history.clear()
        self.logger.info("Analysis history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get engine status."""
        return {
            "active": True,
            "analyses_count": len(self.analysis_history),
            "timestamp": datetime.now().isoformat()
        }

# Simple factory function
def create_pattern_analysis_engine(config=None) -> PatternAnalysisEngine:
    """Create pattern analysis engine."""
    return PatternAnalysisEngine(config)

__all__ = ["PatternAnalysisEngine", "create_pattern_analysis_engine"]