#!/usr/bin/env python3
"""
Vector Analytics Business Intelligence Engine
============================================

Business intelligence processing engine for vector analytics system.
Handles trend analysis, performance metrics, efficiency tracking, and optimization recommendations.
V2 COMPLIANT: Focused business intelligence under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR BUSINESS INTELLIGENCE
@license MIT
"""

import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..vector_analytics_models import AnalyticsInsight, VectorAnalyticsConfig


class BusinessIntelligenceEngine:
    """Business intelligence processing engine for vector analytics"""
    
    def __init__(self, config: VectorAnalyticsConfig):
        """Initialize business intelligence engine with configuration"""
        self.config = config
        self.thresholds = {
            'trend_significance': 0.05,
            'performance_threshold': 0.8,
            'efficiency_target': 0.85
        }
    
    def create_business_intelligence_model(self) -> Dict[str, Any]:
        """Create business intelligence processing model"""
        return {
            'model_type': 'business_intelligence',
            'version': '1.0',
            'capabilities': [
                'trend_analysis',
                'performance_metrics',
                'efficiency_tracking',
                'roi_calculation',
                'cost_optimization'
            ],
            'algorithms': {
                'trend_detection': self.detect_trends,
                'performance_analysis': self.analyze_performance,
                'efficiency_calculation': self.calculate_efficiency,
                'optimization_recommendation': self.recommend_optimizations
            },
            'thresholds': self.thresholds
        }
    
    def detect_trends(self, data: List[float]) -> Dict[str, Any]:
        """Detect trends in data"""
        if len(data) < 2:
            return {'trend': 'insufficient_data', 'strength': 0.0, 'confidence': 0.0}
        
        # Calculate trend direction and strength
        first_half = data[:len(data)//2]
        second_half = data[len(data)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        trend_direction = 'increasing' if second_avg > first_avg else 'decreasing' if second_avg < first_avg else 'stable'
        trend_strength = abs(second_avg - first_avg) / max(first_avg, 0.001)
        
        # Calculate confidence based on data consistency
        variance = statistics.variance(data) if len(data) > 1 else 0
        confidence = max(0.1, 1.0 - (variance / max(statistics.mean(data), 0.001)))
        
        return {
            'trend': trend_direction,
            'strength': min(trend_strength, 1.0),
            'confidence': min(confidence, 1.0),
            'first_half_avg': first_avg,
            'second_half_avg': second_avg,
            'variance': variance
        }
    
    def analyze_performance(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Analyze performance metrics"""
        performance_score = 0.0
        analysis = {}
        
        for metric, value in metrics.items():
            if metric.endswith('_time') or metric.endswith('_latency'):
                # Lower is better for time/latency metrics
                score = max(0, 1.0 - (value / 10.0))
            elif metric.endswith('_rate') or metric.endswith('_percentage'):
                # Higher is better for rate/percentage metrics
                score = min(1.0, value / 100.0)
            else:
                # Default scoring
                score = min(1.0, value / 100.0)
            
            analysis[metric] = {
                'value': value,
                'score': score,
                'status': 'excellent' if score > 0.9 else 'good' if score > 0.7 else 'poor'
            }
            performance_score += score
        
        if metrics:
            performance_score /= len(metrics)
        
        return {
            'overall_score': performance_score,
            'status': 'excellent' if performance_score > 0.9 else 'good' if performance_score > 0.7 else 'poor',
            'metrics_analysis': analysis,
            'recommendations': self.generate_performance_recommendations(analysis)
        }
    
    def calculate_efficiency(self, input_metrics: Dict[str, float], 
                           output_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Calculate efficiency metrics"""
        if not input_metrics or not output_metrics:
            return {'efficiency': 0.0, 'status': 'insufficient_data'}
        
        # Simple efficiency calculation: output / input
        total_input = sum(input_metrics.values())
        total_output = sum(output_metrics.values())
        
        if total_input == 0:
            efficiency = 0.0
        else:
            efficiency = total_output / total_input
        
        return {
            'efficiency': efficiency,
            'status': 'excellent' if efficiency > 0.9 else 'good' if efficiency > 0.7 else 'poor',
            'input_total': total_input,
            'output_total': total_output,
            'improvement_potential': max(0, 1.0 - efficiency)
        }
    
    def recommend_optimizations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if analysis.get('overall_score', 0) < 0.7:
            recommendations.append("Consider performance optimization initiatives")
        
        for metric, data in analysis.get('metrics_analysis', {}).items():
            if data.get('score', 0) < 0.5:
                recommendations.append(f"Optimize {metric} - current performance is below expectations")
        
        return recommendations
    
    def generate_performance_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate specific performance recommendations"""
        recommendations = []
        
        for metric, data in analysis.items():
            if data.get('score', 0) < 0.5:
                if 'time' in metric or 'latency' in metric:
                    recommendations.append(f"Reduce {metric} through caching or optimization")
                elif 'rate' in metric:
                    recommendations.append(f"Improve {metric} through process enhancement")
                else:
                    recommendations.append(f"Review and optimize {metric}")
        
        return recommendations
    
    def calculate_roi(self, investment: float, returns: float) -> Dict[str, Any]:
        """Calculate return on investment"""
        if investment == 0:
            return {'roi': 0.0, 'status': 'invalid_input'}
        
        roi = (returns - investment) / investment
        roi_percentage = roi * 100
        
        return {
            'roi': roi,
            'roi_percentage': roi_percentage,
            'investment': investment,
            'returns': returns,
            'net_profit': returns - investment,
            'status': 'excellent' if roi > 0.2 else 'good' if roi > 0.1 else 'poor'
        }
    
    def optimize_costs(self, current_costs: Dict[str, float], 
                      target_reduction: float = 0.1) -> Dict[str, Any]:
        """Optimize costs with target reduction"""
        total_current = sum(current_costs.values())
        target_total = total_current * (1 - target_reduction)
        
        # Simple proportional reduction
        optimization_plan = {}
        for category, cost in current_costs.items():
            optimization_plan[category] = {
                'current_cost': cost,
                'target_cost': cost * (1 - target_reduction),
                'reduction': cost * target_reduction,
                'reduction_percentage': target_reduction * 100
            }
        
        return {
            'current_total': total_current,
            'target_total': target_total,
            'total_reduction': total_current - target_total,
            'reduction_percentage': target_reduction * 100,
            'optimization_plan': optimization_plan
        }


# Factory function for dependency injection
def create_business_intelligence_engine(config: VectorAnalyticsConfig) -> BusinessIntelligenceEngine:
    """Factory function to create business intelligence engine with configuration"""
    return BusinessIntelligenceEngine(config)


# Export for DI
__all__ = ['BusinessIntelligenceEngine', 'create_business_intelligence_engine']
