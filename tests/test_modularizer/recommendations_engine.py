#!/usr/bin/env python3
"""
Recommendations Engine - Coverage improvement recommendations.

This module generates actionable recommendations for improving test coverage
based on coverage metrics and risk assessment.
V2 COMPLIANT: Focused module under 150 lines
"""

from typing import Dict, List, Any
from .coverage_models import CoverageMetric, RiskAssessment


class RecommendationsEngine:
    """
    Engine for generating coverage improvement recommendations.
    
    This class handles:
    - Coverage improvement recommendations
    - Risk-based suggestions
    - Actionable improvement steps
    - Priority-based recommendations
    """
    
    def __init__(self):
        """Initialize the recommendations engine."""
        self.improvement_strategies = self._initialize_improvement_strategies()
        
    def _initialize_improvement_strategies(self) -> Dict[str, List[str]]:
        """Initialize improvement strategies for different coverage levels."""
        return {
            "critical": [
                "Implement comprehensive unit testing strategy",
                "Focus on core functionality testing first",
                "Add basic smoke tests for all functions",
                "Establish minimum coverage thresholds",
                "Prioritize high-impact areas"
            ],
            "high": [
                "Expand unit test coverage systematically",
                "Add integration tests for complex interactions",
                "Implement test-driven development practices",
                "Focus on uncovered functions and classes",
                "Add edge case testing"
            ],
            "medium": [
                "Fill gaps in existing test coverage",
                "Add boundary condition tests",
                "Improve test quality and maintainability",
                "Consider property-based testing",
                "Add performance testing where appropriate"
            ],
            "low": [
                "Fine-tune existing test coverage",
                "Add advanced testing techniques",
                "Focus on edge cases and error conditions",
                "Implement continuous coverage monitoring",
                "Consider mutation testing"
            ]
        }
    
    def generate_coverage_recommendations(self, coverage_metrics: Dict[str, CoverageMetric], 
                                        risk_assessment: RiskAssessment) -> List[str]:
        """
        Generate comprehensive coverage improvement recommendations.
        
        Args:
            coverage_metrics: Dictionary of coverage metrics
            risk_assessment: Risk assessment results
            
        Returns:
            List of actionable recommendations
        """
        try:
            recommendations = []
            
            # Add risk-based recommendations
            recommendations.extend(self._get_risk_based_recommendations(risk_assessment))
            
            # Add metric-specific recommendations
            recommendations.extend(self._get_metric_based_recommendations(coverage_metrics))
            
            # Add general improvement recommendations
            recommendations.extend(self._get_general_recommendations(coverage_metrics, risk_assessment))
            
            # Prioritize and deduplicate recommendations
            prioritized_recommendations = self._prioritize_recommendations(recommendations)
            
            return prioritized_recommendations[:10]  # Limit to top 10
            
        except Exception as e:
            return [f"Error generating recommendations: {e}"]
    
    def _get_risk_based_recommendations(self, risk_assessment: RiskAssessment) -> List[str]:
        """Get recommendations based on risk level."""
        recommendations = []
        
        risk_level = risk_assessment.overall_risk.lower()
        
        if risk_level in self.improvement_strategies:
            recommendations.extend(self.improvement_strategies[risk_level])
        
        # Add specific risk factor recommendations
        for factor in risk_assessment.risk_factors[:3]:  # Top 3 factors
            if "function" in factor.lower():
                recommendations.append("Add unit tests for uncovered functions")
            elif "class" in factor.lower():
                recommendations.append("Implement class-level testing strategy")
            elif "branch" in factor.lower():
                recommendations.append("Add branch coverage testing")
            elif "coverage" in factor.lower() and "low" in factor.lower():
                recommendations.append("Implement comprehensive testing strategy")
        
        return recommendations
    
    def _get_metric_based_recommendations(self, coverage_metrics: Dict[str, CoverageMetric]) -> List[str]:
        """Get recommendations based on specific metric failures."""
        recommendations = []
        
        for metric_name, metric in coverage_metrics.items():
            if not metric.is_passing():
                gap = metric.get_gap()
                
                if metric_name == "line_coverage":
                    if gap > 20:
                        recommendations.append(f"CRITICAL: Line coverage {gap:.1f}% below target - implement comprehensive testing")
                    else:
                        recommendations.append(f"Improve line coverage by {gap:.1f}% to meet target")
                
                elif metric_name == "function_coverage":
                    if gap > 15:
                        recommendations.append(f"HIGH: Function coverage {gap:.1f}% below target - add unit tests for uncovered functions")
                    else:
                        recommendations.append(f"Add tests for {gap:.1f}% of uncovered functions")
                
                elif metric_name == "class_coverage":
                    if gap > 15:
                        recommendations.append(f"HIGH: Class coverage {gap:.1f}% below target - implement class testing strategy")
                    else:
                        recommendations.append(f"Add tests for {gap:.1f}% of uncovered classes")
                
                elif metric_name == "branch_coverage":
                    if gap > 20:
                        recommendations.append(f"MEDIUM: Branch coverage {gap:.1f}% below target - add conditional testing")
                    else:
                        recommendations.append(f"Improve branch coverage by {gap:.1f}%")
        
        return recommendations
    
    def _get_general_recommendations(self, coverage_metrics: Dict[str, CoverageMetric], 
                                   risk_assessment: RiskAssessment) -> List[str]:
        """Get general improvement recommendations."""
        recommendations = []
        
        # Coverage improvement strategies
        if risk_assessment.overall_risk in ["CRITICAL", "HIGH"]:
            recommendations.append("Establish testing standards and guidelines")
            recommendations.append("Implement automated testing in CI/CD pipeline")
            recommendations.append("Set up coverage monitoring and reporting")
            recommendations.append("Provide testing training for development team")
        
        # Quality improvement
        if any(metric.risk_level == "HIGH" for metric in coverage_metrics.values()):
            recommendations.append("Review and improve existing test quality")
            recommendations.append("Implement test code review process")
            recommendations.append("Add test coverage requirements to pull requests")
        
        # Maintenance and monitoring
        recommendations.append("Regularly review and update test coverage targets")
        recommendations.append("Monitor coverage trends over time")
        recommendations.append("Set up alerts for coverage drops")
        
        return recommendations
    
    def _prioritize_recommendations(self, recommendations: List[str]) -> List[str]:
        """Prioritize recommendations based on importance and urgency."""
        try:
            # Define priority keywords
            priority_keywords = {
                "CRITICAL": 1,
                "HIGH": 2,
                "MEDIUM": 3,
                "LOW": 4
            }
            
            # Score recommendations based on priority keywords
            scored_recommendations = []
            for rec in recommendations:
                score = 5  # Default priority
                for keyword, priority in priority_keywords.items():
                    if keyword in rec.upper():
                        score = priority
                        break
                
                scored_recommendations.append((score, rec))
            
            # Sort by priority (lower score = higher priority)
            scored_recommendations.sort(key=lambda x: x[0])
            
            # Return recommendations without scores
            return [rec for _, rec in scored_recommendations]
            
        except Exception:
            return recommendations  # Return original if prioritization fails
    
    def get_quick_win_recommendations(self, coverage_metrics: Dict[str, CoverageMetric]) -> List[str]:
        """Get quick win recommendations for immediate improvement."""
        quick_wins = []
        
        for metric_name, metric in coverage_metrics.items():
            if not metric.is_passing():
                gap = metric.get_gap()
                
                # Quick wins for small gaps
                if gap <= 10:
                    if metric_name == "function_coverage":
                        quick_wins.append(f"Quick win: Add tests for {gap:.1f}% of uncovered functions")
                    elif metric_name == "class_coverage":
                        quick_wins.append(f"Quick win: Add tests for {gap:.1f}% of uncovered classes")
                    elif metric_name == "line_coverage":
                        quick_wins.append(f"Quick win: Improve line coverage by {gap:.1f}%")
        
        return quick_wins[:3]  # Top 3 quick wins
    
    def get_long_term_recommendations(self, risk_assessment: RiskAssessment) -> List[str]:
        """Get long-term strategic recommendations."""
        long_term = []
        
        if risk_assessment.overall_risk in ["CRITICAL", "HIGH"]:
            long_term.extend([
                "Establish comprehensive testing culture and practices",
                "Implement test-driven development methodology",
                "Set up continuous testing and quality gates",
                "Develop testing expertise within the team",
                "Create testing standards and best practices"
            ])
        else:
            long_term.extend([
                "Maintain high testing standards",
                "Continuously improve test quality",
                "Explore advanced testing techniques",
                "Implement automated quality monitoring",
                "Regular testing process optimization"
            ])
        
        return long_term[:5]  # Top 5 long-term recommendations
