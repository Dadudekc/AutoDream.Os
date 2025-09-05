#!/usr/bin/env python3
"""
Business Intelligence Engine Core - V2 Compliance Module
========================================================

Core business intelligence functionality.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

import statistics
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BusinessIntelligenceEngineCore:
    """Core business intelligence engine functionality."""
    
    def __init__(self, config=None):
        """Initialize business intelligence engine core."""
        self.config = config or {}
        self.logger = logger
        self.insights = []
        self.metrics = {}
    
    def generate_insights(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate business insights from data."""
        try:
            if not data:
                return {"error": "No data provided"}
            
            # Simple insight generation
            insights = self._analyze_data(data)
            recommendations = self._generate_recommendations(insights)
            kpis = self._calculate_kpis(data)
            
            insight_result = {
                "insights": insights,
                "recommendations": recommendations,
                "kpis": kpis,
                "data_points": len(data),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store insights
            self.insights.append(insight_result)
            if len(self.insights) > 50:  # Keep only last 50
                self.insights = self.insights[-50:]
            
            return insight_result
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {e}")
            return {"error": str(e)}
    
    def _analyze_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze data for patterns and trends."""
        insights = []
        
        if not data:
            return insights
        
        # Basic data analysis
        numeric_fields = self._get_numeric_fields(data[0])
        
        for field in numeric_fields:
            values = [row.get(field, 0) for row in data if field in row]
            if values:
                insight = self._analyze_field(field, values)
                if insight:
                    insights.append(insight)
        
        return insights
    
    def _get_numeric_fields(self, sample_row: Dict[str, Any]) -> List[str]:
        """Get numeric fields from sample row."""
        numeric_fields = []
        for key, value in sample_row.items():
            if isinstance(value, (int, float)):
                numeric_fields.append(key)
        return numeric_fields
    
    def _analyze_field(self, field: str, values: List[float]) -> Optional[Dict[str, Any]]:
        """Analyze a single field for insights."""
        if not values:
            return None
        
        try:
            mean_val = statistics.mean(values)
            median_val = statistics.median(values)
            std_val = statistics.stdev(values) if len(values) > 1 else 0
            
            # Simple trend analysis
            if len(values) >= 2:
                trend = "increasing" if values[-1] > values[0] else "decreasing"
                trend_strength = abs(values[-1] - values[0]) / values[0] if values[0] != 0 else 0
            else:
                trend = "stable"
                trend_strength = 0
            
            return {
                "field": field,
                "mean": mean_val,
                "median": median_val,
                "std_dev": std_val,
                "trend": trend,
                "trend_strength": trend_strength,
                "data_points": len(values)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing field {field}: {e}")
            return None
    
    def _generate_recommendations(self, insights: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on insights."""
        recommendations = []
        
        for insight in insights:
            if insight.get("trend") == "increasing" and insight.get("trend_strength", 0) > 0.1:
                recommendations.append(f"Monitor {insight['field']} - showing strong upward trend")
            elif insight.get("trend") == "decreasing" and insight.get("trend_strength", 0) > 0.1:
                recommendations.append(f"Investigate {insight['field']} - showing downward trend")
            elif insight.get("std_dev", 0) > insight.get("mean", 0) * 0.5:
                recommendations.append(f"High volatility detected in {insight['field']}")
        
        return recommendations
    
    def _calculate_kpis(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate key performance indicators."""
        if not data:
            return {}
        
        kpis = {
            "total_records": len(data),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add basic KPIs
        numeric_fields = self._get_numeric_fields(data[0])
        for field in numeric_fields:
            values = [row.get(field, 0) for row in data if field in row]
            if values:
                kpis[f"{field}_sum"] = sum(values)
                kpis[f"{field}_avg"] = statistics.mean(values)
                kpis[f"{field}_max"] = max(values)
                kpis[f"{field}_min"] = min(values)
        
        return kpis
    
    def get_insights_history(self) -> List[Dict[str, Any]]:
        """Get insights history."""
        return self.insights.copy()
    
    def clear_insights(self) -> None:
        """Clear insights history."""
        self.insights = []
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        return self.metrics.copy()
    
    def update_metrics(self, new_metrics: Dict[str, Any]) -> None:
        """Update metrics."""
        self.metrics.update(new_metrics)
