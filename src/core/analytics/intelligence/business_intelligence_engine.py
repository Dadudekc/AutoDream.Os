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
                self.insights.pop(0)
            
            self.logger.info(f"Business insights generated: {len(insights)} insights")
            return insight_result
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {e}")
            return {"error": str(e)}
    
    def _analyze_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze data for insights."""
        try:
            insights = []
            
            # Simple data analysis
            numeric_fields = {}
            text_fields = {}
            
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, (int, float)):
                            if key not in numeric_fields:
                                numeric_fields[key] = []
                            numeric_fields[key].append(value)
                        elif isinstance(value, str):
                            if key not in text_fields:
                                text_fields[key] = []
                            text_fields[key].append(value)
            
            # Generate insights for numeric fields
            for field, values in numeric_fields.items():
                if len(values) > 1:
                    avg_val = statistics.mean(values)
                    max_val = max(values)
                    min_val = min(values)
                    
                    insights.append({
                        "field": field,
                        "type": "numeric",
                        "average": round(avg_val, 3),
                        "max": max_val,
                        "min": min_val,
                        "count": len(values)
                    })
            
            # Generate insights for text fields
            for field, values in text_fields.items():
                if values:
                    unique_count = len(set(values))
                    most_common = max(set(values), key=values.count) if values else None
                    
                    insights.append({
                        "field": field,
                        "type": "text",
                        "unique_values": unique_count,
                        "most_common": most_common,
                        "count": len(values)
                    })
            
            return insights[:10]  # Limit to 10 insights
        except Exception as e:
            self.logger.error(f"Error analyzing data: {e}")
            return []
    
    def _generate_recommendations(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommendations based on insights."""
        try:
            recommendations = []
            
            for insight in insights:
                if insight.get("type") == "numeric":
                    field = insight.get("field", "")
                    avg_val = insight.get("average", 0)
                    
                    if avg_val > 100:
                        recommendations.append({
                            "field": field,
                            "type": "optimization",
                            "message": f"Consider optimizing {field} - high average value detected"
                        })
                    elif avg_val < 10:
                        recommendations.append({
                            "field": field,
                            "type": "improvement",
                            "message": f"Consider improving {field} - low average value detected"
                        })
            
            return recommendations[:5]  # Limit to 5 recommendations
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return []
    
    def _calculate_kpis(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate key performance indicators."""
        try:
            kpis = {
                "total_records": len(data),
                "timestamp": datetime.now().isoformat()
            }
            
            # Simple KPI calculations
            if data:
                numeric_values = []
                for item in data:
                    if isinstance(item, dict):
                        for value in item.values():
                            if isinstance(value, (int, float)):
                                numeric_values.append(value)
                
                if numeric_values:
                    kpis.update({
                        "numeric_fields": len(numeric_values),
                        "average_value": round(statistics.mean(numeric_values), 3),
                        "max_value": max(numeric_values),
                        "min_value": min(numeric_values)
                    })
            
            return kpis
        except Exception as e:
            self.logger.error(f"Error calculating KPIs: {e}")
            return {"error": str(e)}
    
    def get_insights_summary(self) -> Dict[str, Any]:
        """Get insights summary."""
        try:
            if not self.insights:
                return {"message": "No insights available"}
            
            total_insights = len(self.insights)
            recent_insights = self.insights[-1] if self.insights else {}
            
            return {
                "total_insights": total_insights,
                "recent_insights": recent_insights,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting insights summary: {e}")
            return {"error": str(e)}
    
    def clear_insights(self) -> None:
        """Clear insights history."""
        self.insights.clear()
        self.logger.info("Insights history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get engine status."""
        return {
            "active": True,
            "insights_count": len(self.insights),
            "timestamp": datetime.now().isoformat()
        }

# Simple factory function
def create_business_intelligence_engine(config=None) -> BusinessIntelligenceEngine:
    """Create business intelligence engine."""
    return BusinessIntelligenceEngine(config)

__all__ = ["BusinessIntelligenceEngine", "create_business_intelligence_engine"]