"""
Trend Analyzer - V2 Compliance Module
====================================

Trend analysis functionality for analytics.

V2 Compliance: < 300 lines, single responsibility, trend analysis.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import statistics
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """Trend analysis functionality."""
    
    def __init__(self):
        """Initialize trend analyzer."""
        self.logger = logger
    
    def analyze_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in data."""
        try:
            if not data:
                return {"error": "No data provided"}
            
            trends = {
                "numeric_trends": self._analyze_numeric_trends(data),
                "categorical_trends": self._analyze_categorical_trends(data),
                "correlation_trends": self._analyze_correlation_trends(data)
            }
            
            return trends
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {e}")
            return {"error": str(e)}
    
    def _analyze_numeric_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze numeric trends."""
        try:
            # Extract numeric values
            numeric_values = []
            for item in data:
                for value in item.values():
                    if isinstance(value, (int, float)):
                        numeric_values.append(value)
            
            if len(numeric_values) < 2:
                return {"message": "Insufficient numeric data for trend analysis"}
            
            # Calculate trend direction
            first_half = numeric_values[:len(numeric_values)//2]
            second_half = numeric_values[len(numeric_values)//2:]
            
            first_mean = statistics.mean(first_half)
            second_mean = statistics.mean(second_half)
            
            trend_direction = "increasing" if second_mean > first_mean else "decreasing"
            trend_strength = abs(second_mean - first_mean) / first_mean if first_mean != 0 else 0
            
            return {
                "trend_direction": trend_direction,
                "trend_strength": round(trend_strength, 3),
                "first_half_mean": round(first_mean, 3),
                "second_half_mean": round(second_mean, 3),
                "total_values": len(numeric_values)
            }
        except Exception as e:
            self.logger.error(f"Error analyzing numeric trends: {e}")
            return {}
    
    def _analyze_categorical_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze categorical trends."""
        try:
            # Extract categorical values
            categorical_values = []
            for item in data:
                for value in item.values():
                    if isinstance(value, str):
                        categorical_values.append(value)
            
            if not categorical_values:
                return {"message": "No categorical data found"}
            
            # Count occurrences
            from collections import Counter
            value_counts = Counter(categorical_values)
            most_common = value_counts.most_common(5)
            
            return {
                "most_common_values": most_common,
                "unique_values": len(value_counts),
                "total_values": len(categorical_values)
            }
        except Exception as e:
            self.logger.error(f"Error analyzing categorical trends: {e}")
            return {}
    
    def _analyze_correlation_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze correlation trends."""
        try:
            # Simple correlation analysis
            numeric_fields = {}
            for item in data:
                for key, value in item.items():
                    if isinstance(value, (int, float)):
                        if key not in numeric_fields:
                            numeric_fields[key] = []
                        numeric_fields[key].append(value)
            
            if len(numeric_fields) < 2:
                return {"message": "Insufficient numeric fields for correlation analysis"}
            
            # Calculate simple correlations
            correlations = {}
            field_names = list(numeric_fields.keys())
            
            for i, field1 in enumerate(field_names):
                for field2 in field_names[i+1:]:
                    values1 = numeric_fields[field1]
                    values2 = numeric_fields[field2]
                    
                    if len(values1) == len(values2):
                        # Simple correlation calculation
                        correlation = self._calculate_correlation(values1, values2)
                        correlations[f"{field1}_vs_{field2}"] = round(correlation, 3)
            
            return {
                "correlations": correlations,
                "fields_analyzed": field_names
            }
        except Exception as e:
            self.logger.error(f"Error analyzing correlation trends: {e}")
            return {}
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate simple correlation coefficient."""
        try:
            if len(x) != len(y) or len(x) < 2:
                return 0.0
            
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(x[i] * y[i] for i in range(n))
            sum_x2 = sum(x[i] ** 2 for i in range(n))
            sum_y2 = sum(y[i] ** 2 for i in range(n))
            
            numerator = n * sum_xy - sum_x * sum_y
            denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
            
            if denominator == 0:
                return 0.0
            
            return numerator / denominator
        except Exception:
            return 0.0
