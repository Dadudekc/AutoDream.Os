#!/usr/bin/env python3
"""
Scaling Monitoring - Agent Cellphone V2
=======================================

Scaling metrics and performance monitoring functionality.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import json
import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict
from pathlib import Path

from .scaling_types import ScalingMetrics, ScalingDecision, ScalingStatus


class ScalingMonitor:
    """
    Monitors scaling performance and provides metrics analysis.
    
    Responsibilities:
    - Track scaling performance metrics
    - Analyze scaling patterns and trends
    - Provide scaling recommendations
    - Monitor scaling health and alerts
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ScalingMonitor")
        self.metrics_history: List[ScalingMetrics] = []
        self.decision_history: List[ScalingDecision] = []
        self.performance_alerts: List[Dict[str, Any]] = []
        self.scaling_patterns: Dict[str, Any] = {}
        
        # Performance thresholds
        self.thresholds = {
            'cpu_utilization': 80.0,
            'memory_utilization': 85.0,
            'response_time': 200.0,
            'error_rate': 5.0,
            'scaling_frequency': 10  # max scaling events per hour
        }
    
    def record_metrics(self, metrics: ScalingMetrics):
        """Record scaling metrics for analysis"""
        try:
            self.metrics_history.append(metrics)
            
            # Keep only recent history (last 1000 entries)
            if len(self.metrics_history) > 1000:
                self.metrics_history.pop(0)
            
            # Analyze for patterns
            self._analyze_scaling_patterns()
            
            # Check for performance alerts
            self._check_performance_alerts(metrics)
            
        except Exception as e:
            self.logger.error(f"Error recording metrics: {e}")
    
    def record_decision(self, decision: ScalingDecision):
        """Record scaling decision for analysis"""
        try:
            self.decision_history.append(decision)
            
            # Keep only recent history (last 500 entries)
            if len(self.decision_history) > 500:
                self.decision_history.pop(0)
            
            # Analyze decision patterns
            self._analyze_decision_patterns()
            
        except Exception as e:
            self.logger.error(f"Error recording decision: {e}")
    
    def _analyze_scaling_patterns(self):
        """Analyze scaling patterns from metrics history"""
        if len(self.metrics_history) < 10:
            return
        
        try:
            recent_metrics = self.metrics_history[-100:]  # Last 100 entries
            metrics = ['cpu_utilization', 'memory_utilization', 'response_time', 'error_rate']
            
            # Calculate averages and trends
            averages = {metric: round(sum(getattr(m, metric) for m in recent_metrics) / len(recent_metrics), 2) for metric in metrics}
            trends = {metric.split('_')[0]: self._calculate_trend([getattr(m, metric) for m in recent_metrics]) for metric in metrics[:-1]}  # Exclude error_rate
            
            self.scaling_patterns = {
                'current_averages': averages,
                'trends': trends,
                'last_updated': time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing scaling patterns: {e}")
    
    def _analyze_decision_patterns(self):
        """Analyze scaling decision patterns"""
        if len(self.decision_history) < 5:
            return
        
        try:
            recent_decisions = self.decision_history[-100:]  # Last 100 decisions
            
            # Count decision types and calculate metrics
            decision_counts = defaultdict(int)
            for decision in recent_decisions:
                decision_counts[decision.action] += 1
            
            # Calculate scaling frequency and success rate
            scaling_frequency = 0
            if len(recent_decisions) >= 2:
                time_span = recent_decisions[-1].timestamp - recent_decisions[0].timestamp
                scaling_frequency = len(recent_decisions) / (time_span / 3600)  # per hour
            
            successful_scales = sum(1 for d in recent_decisions if d.confidence > 0.7)
            success_rate = (successful_scales / len(recent_decisions)) * 100 if recent_decisions else 0
            
            self.scaling_patterns.update({
                'decision_analysis': {
                    'decision_counts': dict(decision_counts),
                    'scaling_frequency_per_hour': round(scaling_frequency, 2),
                    'success_rate_percent': round(success_rate, 2),
                    'total_decisions': len(recent_decisions)
                }
            })
            
        except Exception as e:
            self.logger.error(f"Error analyzing decision patterns: {e}")
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend from a list of values"""
        if len(values) < 2:
            return "stable"
        
        try:
            first_half = values[:len(values)//2]
            second_half = values[len(values)//2:]
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            change_percent = ((second_avg - first_avg) / first_avg * 100) if first_avg > 0 else 0
            
            if change_percent > 10:
                return "increasing"
            elif change_percent < -10:
                return "decreasing"
            else:
                return "stable"
                
        except Exception:
            return "unknown"
    
    def _check_performance_alerts(self, metrics: ScalingMetrics):
        """Check for performance alerts based on current metrics"""
        alerts = []
        
        # Check CPU, memory, response time, and error rate thresholds
        thresholds = [
            ('cpu_utilization', 'high_cpu_utilization', 'warning'),
            ('memory_utilization', 'high_memory_utilization', 'warning'),
            ('response_time', 'high_response_time', 'warning'),
            ('error_rate', 'high_error_rate', 'critical')
        ]
        
        for metric, alert_type, severity in thresholds:
            if getattr(metrics, metric) > self.thresholds[metric]:
                alerts.append({
                    'type': alert_type,
                    'severity': severity,
                    'message': f"{metric.replace('_', ' ').title()} {getattr(metrics, metric)} exceeds threshold {self.thresholds[metric]}",
                    'timestamp': time.time(),
                    'current_value': getattr(metrics, metric),
                    'threshold': self.thresholds[metric]
                })
        
        # Add alerts and maintain history
        self.performance_alerts.extend(alerts)
        if len(self.performance_alerts) > 100:
            self.performance_alerts = self.performance_alerts[-100:]
        
        # Log alerts
        for alert in alerts:
            if alert['severity'] == 'critical':
                self.logger.error(f"CRITICAL ALERT: {alert['message']}")
            else:
                self.logger.warning(f"PERFORMANCE ALERT: {alert['message']}")
    
    def get_scaling_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive scaling health report"""
        try:
            current_time = time.time()
            health_score = 100
            
            # Deduct points for performance issues
            if self.performance_alerts:
                critical_alerts = len([a for a in self.performance_alerts if a['severity'] == 'critical'])
                warning_alerts = len([a for a in self.performance_alerts if a['severity'] == 'warning'])
                health_score -= (critical_alerts * 20) + (warning_alerts * 5)
                health_score = max(0, health_score)
            
            # Deduct points for excessive scaling
            if self.scaling_patterns.get('decision_analysis'):
                scaling_freq = self.scaling_patterns['decision_analysis']['scaling_frequency_per_hour']
                if scaling_freq > self.thresholds['scaling_frequency']:
                    health_score -= 15
            
            report = {
                'timestamp': current_time,
                'health_score': max(0, health_score),
                'status': self._get_health_status(health_score),
                'performance_alerts': {
                    'total': len(self.performance_alerts),
                    'critical': len([a for a in self.performance_alerts if a['severity'] == 'critical']),
                    'warnings': len([a for a in self.performance_alerts if a['severity'] == 'warning'])
                },
                'scaling_patterns': self.scaling_patterns,
                'recommendations': self._generate_recommendations()
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating health report: {e}")
            return {'error': str(e), 'status': 'failed'}
    
    def _get_health_status(self, health_score: int) -> str:
        """Get health status based on score"""
        if health_score >= 90: return "excellent"
        elif health_score >= 75: return "good"
        elif health_score >= 50: return "fair"
        elif health_score >= 25: return "poor"
        else: return "critical"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate scaling recommendations based on current patterns"""
        recommendations = []
        
        try:
            if not self.scaling_patterns:
                return ["Insufficient data for recommendations"]
            
            # Check various metrics and generate recommendations
            current_metrics = self.scaling_patterns.get('current_averages', {})
            current_cpu = current_metrics.get('cpu_utilization', 0)
            current_memory = current_metrics.get('memory_utilization', 0)
            current_response = current_metrics.get('response_time', 0)
            
            if current_cpu > 70:
                recommendations.append("Consider scaling up due to high CPU utilization")
            elif current_cpu < 30:
                recommendations.append("Consider scaling down due to low CPU utilization")
            
            if current_memory > 75:
                recommendations.append("Monitor memory usage and consider optimization")
            
            if current_response > 150:
                recommendations.append("Investigate response time degradation")
            
            # Check scaling frequency
            if self.scaling_patterns.get('decision_analysis'):
                scaling_freq = self.scaling_patterns['decision_analysis']['scaling_frequency_per_hour']
                if scaling_freq > self.thresholds['scaling_frequency']:
                    recommendations.append("Reduce scaling frequency to prevent thrashing")
            
            if not recommendations:
                recommendations.append("Scaling system is operating optimally")
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            recommendations = ["Error generating recommendations"]
        
        return recommendations
    
    def clear_history(self):
        """Clear monitoring history"""
        self.metrics_history.clear()
        self.decision_history.clear()
        self.performance_alerts.clear()
        self.scaling_patterns.clear()
        self.logger.info("Scaling monitoring history cleared")
    
    def export_metrics(self, output_path: Path) -> bool:
        """Export monitoring metrics to file"""
        try:
            export_data = {'export_timestamp': time.time(), 'metrics_history': [vars(m) for m in self.metrics_history],
                          'decision_history': [vars(d) for d in self.decision_history], 'performance_alerts': self.performance_alerts,
                          'scaling_patterns': self.scaling_patterns}
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            self.logger.info(f"Scaling metrics exported to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {e}")
            return False
