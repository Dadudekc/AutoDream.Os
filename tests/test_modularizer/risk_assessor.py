#!/usr/bin/env python3
"""
Risk Assessor - Risk assessment for testing coverage analysis.

This module handles risk assessment based on coverage gaps and provides
recommendations for improving test coverage.
V2 COMPLIANT: Focused module under 150 lines
"""

from typing import Dict, List, Any
from .coverage_models import CoverageMetric, RiskAssessment


class RiskAssessor:
    """
    Risk assessor for testing coverage analysis.
    
    This class handles:
    - Risk assessment based on coverage metrics
    - Risk factor identification
    - Critical gap detection
    - Risk-based recommendations
    """
    
    def __init__(self):
        """Initialize the risk assessor."""
        self.risk_thresholds = self._initialize_risk_thresholds()
        self.risk_factors = self._initialize_risk_factors()
        
    def _initialize_risk_thresholds(self) -> Dict[str, float]:
        """Initialize risk assessment thresholds."""
        return {
            "high_risk": 60.0,      # Below 60% coverage is high risk
            "medium_risk": 75.0,    # Below 75% coverage is medium risk
            "low_risk": 85.0,       # Below 85% coverage is low risk
            "safe": 95.0            # Above 95% coverage is safe
        }
    
    def _initialize_risk_factors(self) -> Dict[str, List[str]]:
        """Initialize risk factors for different coverage levels."""
        return {
            "critical": [
                "Extremely low test coverage",
                "No function-level testing",
                "Missing class-level testing",
                "No branch coverage testing"
            ],
            "high": [
                "Low test coverage",
                "Missing critical function tests",
                "Insufficient branch coverage",
                "Gaps in class testing"
            ],
            "medium": [
                "Moderate test coverage",
                "Some missing function tests",
                "Partial branch coverage",
                "Incomplete class testing"
            ],
            "low": [
                "Good test coverage",
                "Minor gaps in testing",
                "Most functions covered",
                "Most classes covered"
            ]
        }
    
    def assess_coverage_risk(self, coverage_metrics: Dict[str, CoverageMetric], 
                           overall_coverage: float) -> RiskAssessment:
        """
        Assess risk based on coverage metrics and overall coverage.
        
        Args:
            coverage_metrics: Dictionary of coverage metrics
            overall_coverage: Overall coverage percentage
            
        Returns:
            RiskAssessment object with risk analysis
        """
        try:
            # Determine overall risk level
            overall_risk = self._determine_overall_risk(overall_coverage)
            
            # Identify risk factors
            risk_factors = self._identify_risk_factors(coverage_metrics, overall_coverage)
            
            # Identify critical gaps
            critical_gaps = self._identify_critical_gaps(coverage_metrics, overall_coverage)
            
            # Generate recommendations
            recommendations = self._generate_risk_recommendations(
                overall_risk, risk_factors, critical_gaps
            )
            
            # Calculate risk score
            risk_score = self._calculate_risk_score(overall_coverage, coverage_metrics)
            
            return RiskAssessment(
                overall_risk=overall_risk,
                risk_factors=risk_factors,
                critical_gaps=critical_gaps,
                recommendations=recommendations,
                risk_score=risk_score
            )
            
        except Exception as e:
            # Return default risk assessment on error
            return RiskAssessment(
                overall_risk="UNKNOWN",
                risk_factors=[f"Risk assessment error: {e}"],
                critical_gaps=["Unable to assess gaps"],
                recommendations=["Fix risk assessment system"],
                risk_score=100.0
            )
    
    def _determine_overall_risk(self, overall_coverage: float) -> str:
        """Determine overall risk level based on coverage percentage."""
        if overall_coverage < self.risk_thresholds["high_risk"]:
            return "CRITICAL"
        elif overall_coverage < self.risk_thresholds["medium_risk"]:
            return "HIGH"
        elif overall_coverage < self.risk_thresholds["low_risk"]:
            return "MEDIUM"
        elif overall_coverage < self.risk_thresholds["safe"]:
            return "LOW"
        else:
            return "SAFE"
    
    def _identify_risk_factors(self, coverage_metrics: Dict[str, CoverageMetric], 
                              overall_coverage: float) -> List[str]:
        """Identify specific risk factors based on coverage metrics."""
        risk_factors = []
        
        # Check overall coverage risk
        if overall_coverage < 60:
            risk_factors.extend(self.risk_factors["critical"])
        elif overall_coverage < 75:
            risk_factors.extend(self.risk_factors["high"])
        elif overall_coverage < 85:
            risk_factors.extend(self.risk_factors["medium"])
        elif overall_coverage < 95:
            risk_factors.extend(self.risk_factors["low"])
        
        # Check individual metric risks
        for metric_name, metric in coverage_metrics.items():
            if not metric.is_passing():
                gap = metric.get_gap()
                if gap > 20:
                    risk_factors.append(f"Large gap in {metric_name}: {gap:.1f}% below target")
                elif gap > 10:
                    risk_factors.append(f"Moderate gap in {metric_name}: {gap:.1f}% below target")
                else:
                    risk_factors.append(f"Minor gap in {metric_name}: {gap:.1f}% below target")
        
        return risk_factors
    
    def _identify_critical_gaps(self, coverage_metrics: Dict[str, CoverageMetric], 
                               overall_coverage: float) -> List[str]:
        """Identify critical coverage gaps that need immediate attention."""
        critical_gaps = []
        
        # Overall coverage critical gaps
        if overall_coverage < 50:
            critical_gaps.append(f"Overall coverage critically low: {overall_coverage:.1f}%")
        
        # Individual metric critical gaps
        for metric_name, metric in coverage_metrics.items():
            if metric.risk_level == "HIGH" or metric.risk_level == "CRITICAL":
                gap = metric.get_gap()
                critical_gaps.append(f"{metric_name}: {gap:.1f}% below target ({metric.risk_level} risk)")
        
        # Specific critical thresholds
        for metric_name, metric in coverage_metrics.items():
            if metric.value < 50:
                critical_gaps.append(f"{metric_name} below 50%: {metric.value:.1f}%")
            elif metric.value < 70 and metric.target > 80:
                critical_gaps.append(f"{metric_name} significantly below target: {metric.value:.1f}% vs {metric.target:.1f}%")
        
        return critical_gaps
    
    def _generate_risk_recommendations(self, overall_risk: str, risk_factors: List[str], 
                                     critical_gaps: List[str]) -> List[str]:
        """Generate recommendations based on risk assessment."""
        recommendations = []
        
        # Overall risk recommendations
        if overall_risk == "CRITICAL":
            recommendations.append("CRITICAL: Immediate action required to improve test coverage")
            recommendations.append("Focus on achieving minimum 60% coverage before deployment")
            recommendations.append("Prioritize testing of core functionality and critical paths")
        elif overall_risk == "HIGH":
            recommendations.append("HIGH: Urgent action needed to improve test coverage")
            recommendations.append("Target 75% coverage within next development cycle")
            recommendations.append("Focus on high-impact areas with low coverage")
        elif overall_risk == "MEDIUM":
            recommendations.append("MEDIUM: Moderate improvement needed in test coverage")
            recommendations.append("Target 85% coverage within next sprint")
            recommendations.append("Address gaps in function and class testing")
        elif overall_risk == "LOW":
            recommendations.append("LOW: Minor improvements needed in test coverage")
            recommendations.append("Target 95% coverage for production readiness")
            recommendations.append("Focus on edge cases and boundary conditions")
        
        # Specific gap recommendations
        if critical_gaps:
            recommendations.append("Address critical coverage gaps:")
            for gap in critical_gaps[:3]:  # Limit to top 3
                recommendations.append(f"  - {gap}")
        
        # General improvement recommendations
        if overall_risk in ["CRITICAL", "HIGH", "MEDIUM"]:
            recommendations.append("Implement comprehensive testing strategy")
            recommendations.append("Add unit tests for uncovered functions and classes")
            recommendations.append("Consider integration testing for complex interactions")
            recommendations.append("Review and update test coverage targets")
        
        return recommendations
    
    def _calculate_risk_score(self, overall_coverage: float, 
                             coverage_metrics: Dict[str, CoverageMetric]) -> float:
        """Calculate numerical risk score (0-100, higher = more risk)."""
        try:
            # Base risk score from overall coverage
            if overall_coverage >= 95:
                base_score = 0
            elif overall_coverage >= 85:
                base_score = 20
            elif overall_coverage >= 75:
                base_score = 40
            elif overall_coverage >= 60:
                base_score = 60
            else:
                base_score = 80
            
            # Add risk from individual metrics
            metric_risk = 0
            for metric in coverage_metrics.values():
                if not metric.is_passing():
                    gap = metric.get_gap()
                    if gap > 20:
                        metric_risk += 15
                    elif gap > 10:
                        metric_risk += 10
                    else:
                        metric_risk += 5
            
            # Calculate final risk score
            final_score = min(100.0, base_score + metric_risk)
            
            return final_score
            
        except Exception:
            return 50.0  # Default risk score on error
    
    def get_risk_summary(self, risk_assessment: RiskAssessment) -> str:
        """Get a human-readable summary of the risk assessment."""
        try:
            summary = f"""
Risk Assessment Summary
======================
Overall Risk: {risk_assessment.overall_risk}
Risk Score: {risk_assessment.risk_score:.1f}/100

Risk Factors ({len(risk_assessment.risk_factors)}):
"""
            for factor in risk_assessment.risk_factors[:5]:  # Top 5 factors
                summary += f"  • {factor}\n"
            
            if risk_assessment.critical_gaps:
                summary += f"\nCritical Gaps ({len(risk_assessment.critical_gaps)}):\n"
                for gap in risk_assessment.critical_gaps[:3]:  # Top 3 gaps
                    summary += f"  ⚠️ {gap}\n"
            
            if risk_assessment.recommendations:
                summary += f"\nTop Recommendations:\n"
                for i, rec in enumerate(risk_assessment.recommendations[:3], 1):
                    summary += f"  {i}. {rec}\n"
            
            return summary.strip()
            
        except Exception as e:
            return f"Error generating risk summary: {e}"
