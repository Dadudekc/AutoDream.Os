#!/usr/bin/env python3
"""
Optimization Recommendation System
=================================
Intelligent optimization recommendations for agent swarm systems.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class RecommendationType(Enum):
    """Optimization recommendation types"""
    IMMEDIATE = "immediate"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    PREVENTIVE = "preventive"


@dataclass
class OptimizationRecommendation:
    """System optimization recommendation"""
    recommendation_id: str
    recommendation_type: RecommendationType
    title: str
    description: str
    priority: int
    estimated_effort: str
    expected_impact: str
    confidence: float
    timestamp: float
    status: str = "active"


class OptimizationRecommendationSystem:
    """Intelligent optimization recommendation system"""
    
    def __init__(self, system_id: str = "default-recommendations"):
        self.logger = logging.getLogger(f"{__name__}.OptimizationRecommendationSystem")
        self.system_id = system_id
        self._recommendations: Dict[str, OptimizationRecommendation] = {}
        self._recommendation_history: List[OptimizationRecommendation] = []
        self._recommendation_templates: Dict[str, Dict[str, Any]] = {}
        self._initialize_templates()
        self._total_recommendations = 0
        self._implemented_recommendations = 0
        self.logger.info(f"Optimization Recommendation System '{system_id}' initialized")
    
    def _initialize_templates(self):
        """Initialize recommendation templates"""
        self._recommendation_templates = {
            "performance_bottleneck": {
                "title": "Performance Bottleneck Detected",
                "description": "System performance is degraded due to identified bottlenecks",
                "priority": 3, "estimated_effort": "medium", "expected_impact": "high"
            },
            "resource_optimization": {
                "title": "Resource Optimization Opportunity",
                "description": "System resources can be optimized for better efficiency",
                "priority": 2, "estimated_effort": "low", "expected_impact": "medium"
            },
            "scalability_improvement": {
                "title": "Scalability Enhancement",
                "description": "System scalability can be improved for future growth",
                "priority": 2, "estimated_effort": "high", "expected_impact": "high"
            },
            "error_rate_reduction": {
                "title": "Error Rate Reduction",
                "description": "System error rates can be reduced through optimization",
                "priority": 3, "estimated_effort": "medium", "expected_impact": "medium"
            },
            "workflow_optimization": {
                "title": "Workflow Optimization",
                "description": "System workflows can be optimized for better efficiency",
                "priority": 2, "estimated_effort": "medium", "expected_impact": "medium"
            }
        }
    
    def generate_recommendation(self, template_key: str, custom_data: Optional[Dict[str, Any]] = None,
                               confidence: float = 0.8) -> str:
        """Generate an optimization recommendation"""
        if template_key not in self._recommendation_templates:
            self.logger.error(f"Unknown recommendation template: {template_key}")
            return ""
        
        template = self._recommendation_templates[template_key]
        recommendation_id = f"rec_{template_key}_{int(time.time())}"
        
        title = custom_data.get("title", template["title"]) if custom_data else template["title"]
        description = custom_data.get("description", template["description"]) if custom_data else template["description"]
        priority = custom_data.get("priority", template["priority"]) if custom_data else template["priority"]
        estimated_effort = custom_data.get("estimated_effort", template["estimated_effort"]) if custom_data else template["estimated_effort"]
        expected_impact = custom_data.get("expected_impact", template["expected_impact"]) if custom_data else template["expected_impact"]
        
        recommendation = OptimizationRecommendation(
            recommendation_id=recommendation_id, recommendation_type=self._determine_recommendation_type(priority, confidence),
            title=title, description=description, priority=priority, estimated_effort=estimated_effort,
            expected_impact=expected_impact, confidence=confidence, timestamp=time.time()
        )
        
        self._recommendations[recommendation_id] = recommendation
        self._total_recommendations += 1
        self.logger.info(f"Recommendation generated: {title} (priority: {priority})")
        return recommendation_id
    
    def _determine_recommendation_type(self, priority: int, confidence: float) -> RecommendationType:
        """Determine recommendation type based on priority and confidence"""
        if priority >= 3 and confidence >= 0.9:
            return RecommendationType.IMMEDIATE
        elif priority >= 2 and confidence >= 0.7:
            return RecommendationType.SHORT_TERM
        elif confidence >= 0.6:
            return RecommendationType.LONG_TERM
        else:
            return RecommendationType.PREVENTIVE
    
    def get_recommendations(self, recommendation_type: Optional[RecommendationType] = None,
                           priority_min: Optional[int] = None) -> List[OptimizationRecommendation]:
        """Get optimization recommendations with optional filtering"""
        recommendations = list(self._recommendations.values())
        
        if recommendation_type:
            recommendations = [r for r in recommendations if r.recommendation_type == recommendation_type]
        
        if priority_min is not None:
            recommendations = [r for r in recommendations if r.priority >= priority_min]
        
        recommendations.sort(key=lambda x: (x.priority, x.confidence), reverse=True)
        return recommendations
    
    def implement_recommendation(self, recommendation_id: str) -> bool:
        """Mark a recommendation as implemented"""
        if recommendation_id not in self._recommendations:
            return False
        
        recommendation = self._recommendations[recommendation_id]
        recommendation.status = "implemented"
        self._recommendation_history.append(recommendation)
        del self._recommendations[recommendation_id]
        self._implemented_recommendations += 1
        self.logger.info(f"Recommendation implemented: {recommendation.title}")
        return True
    
    def get_recommendation_summary(self) -> Dict[str, Any]:
        """Get summary of all recommendations"""
        active_recommendations = [r for r in self._recommendations.values() if r.status == "active"]
        
        summary = {
            "total_recommendations": self._total_recommendations,
            "active_recommendations": len(active_recommendations),
            "implemented_recommendations": self._implemented_recommendations,
            "implementation_rate": (self._implemented_recommendations / max(1, self._total_recommendations)) * 100,
            "by_type": {}, "by_priority": {}, "by_effort": {}, "by_impact": {}
        }
        
        for rec_type in RecommendationType:
            summary["by_type"][rec_type.value] = len([r for r in active_recommendations if r.recommendation_type == rec_type])
        
        for priority in range(1, 6):
            summary["by_priority"][f"priority_{priority}"] = len([r for r in active_recommendations if r.priority == priority])
        
        efforts = set(r.estimated_effort for r in active_recommendations)
        for effort in efforts:
            summary["by_effort"][effort] = len([r for r in active_recommendations if r.estimated_effort == effort])
        
        impacts = set(r.expected_impact for r in active_recommendations)
        for impact in impacts:
            summary["by_impact"][impact] = len([r for r in active_recommendations if r.expected_impact == impact])
        
        return summary


def main():
    """CLI interface for testing OptimizationRecommendationSystem"""
    import argparse
    parser = argparse.ArgumentParser(description="Optimization Recommendation System CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    args = parser.parse_args()
    
    if args.test:
        print("🧪 OptimizationRecommendationSystem Smoke Test")
        system = OptimizationRecommendationSystem("test-recommendations")
        rec1 = system.generate_recommendation("performance_bottleneck", confidence=0.95)
        rec2 = system.generate_recommendation("resource_optimization", confidence=0.85)
        print(f"✅ Recommendations generated: {rec1}, {rec2}")
        active_recs = system.get_recommendations()
        print(f"✅ Active recommendations: {len(active_recs)}")
        success = system.implement_recommendation(rec1)
        print(f"✅ Recommendation implemented: {success}")
        summary = system.get_recommendation_summary()
        print(f"✅ Total recommendations: {summary['total_recommendations']}")
        print("🎉 Smoke test PASSED!")
    else:
        print("OptimizationRecommendationSystem ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
