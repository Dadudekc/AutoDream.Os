#!/usr/bin/env python3
"""
Vector Analytics Anomaly Detection Engine
=========================================

Anomaly detection engine for vector analytics system.
Handles statistical anomalies, behavioral anomalies, and performance anomalies.
V2 COMPLIANT: Focused anomaly detection under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR ANOMALY DETECTION
@license MIT
"""

import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..vector_analytics_models import VectorAnalyticsConfig


class AnomalyDetectionEngine:
    """Anomaly detection engine for vector analytics"""
    
    def __init__(self, config: VectorAnalyticsConfig):
        """Initialize anomaly detection engine with configuration"""
        self.config = config
        self.anomaly_thresholds = {
            'statistical_z_score': 2.0,
            'performance_threshold': 0.5,
            'behavioral_frequency': 0.05
        }
    
    def create_anomaly_detection_model(self) -> Dict[str, Any]:
        """Create anomaly detection processing model"""
        return {
            'model_type': 'anomaly_detection',
            'version': '1.0',
            'capabilities': [
                'statistical_anomaly_detection',
                'behavioral_anomaly_detection',
                'performance_anomaly_detection',
                'trend_anomaly_detection',
                'pattern_anomaly_detection'
            ],
            'algorithms': {
                'detect_statistical_anomalies': self.detect_statistical_anomalies,
                'detect_behavioral_anomalies': self.detect_behavioral_anomalies,
                'detect_performance_anomalies': self.detect_performance_anomalies,
                'detect_trend_anomalies': self.detect_trend_anomalies
            },
            'thresholds': self.anomaly_thresholds
        }
    
    def detect_statistical_anomalies(self, data: List[float]) -> List[Dict[str, Any]]:
        """Detect statistical anomalies using z-score method"""
        if len(data) < 3:
            return []
        
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data) if len(data) > 1 else 0
        
        if std_val == 0:
            return []
        
        anomalies = []
        threshold = self.anomaly_thresholds['statistical_z_score']
        
        for i, value in enumerate(data):
            z_score = abs(value - mean_val) / std_val
            if z_score > threshold:
                anomalies.append({
                    'index': i,
                    'value': value,
                    'type': 'statistical',
                    'z_score': z_score,
                    'severity': 'high' if z_score > threshold * 1.5 else 'medium',
                    'deviation': value - mean_val,
                    'percentile': self._calculate_percentile(data, value)
                })
        
        return anomalies
    
    def detect_behavioral_anomalies(self, data: List[Any]) -> List[Dict[str, Any]]:
        """Detect behavioral anomalies based on frequency patterns"""
        if not data:
            return []
        
        from collections import Counter
        counter = Counter(data)
        total_count = len(data)
        threshold = self.anomaly_thresholds['behavioral_frequency']
        
        anomalies = []
        for item, count in counter.items():
            frequency = count / total_count
            if frequency < threshold:
                anomalies.append({
                    'item': item,
                    'frequency': frequency,
                    'type': 'behavioral',
                    'severity': 'high' if frequency < threshold * 0.5 else 'medium',
                    'count': count,
                    'total': total_count
                })
        
        return anomalies
    
    def detect_performance_anomalies(self, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Detect performance anomalies in metrics"""
        if not metrics:
            return []
        
        anomalies = []
        threshold = self.anomaly_thresholds['performance_threshold']
        
        for metric, value in metrics.items():
            # Different thresholds for different metric types
            if metric.endswith('_time') or metric.endswith('_latency'):
                # High values are anomalies for time/latency metrics
                if value > 5.0:  # 5 seconds threshold
                    anomalies.append({
                        'metric': metric,
                        'value': value,
                        'type': 'performance',
                        'severity': 'high' if value > 10.0 else 'medium',
                        'threshold': 5.0,
                        'deviation': value - 5.0
                    })
            elif metric.endswith('_rate') or metric.endswith('_percentage'):
                # Low values are anomalies for rate/percentage metrics
                if value < threshold * 100:  # Convert to percentage
                    anomalies.append({
                        'metric': metric,
                        'value': value,
                        'type': 'performance',
                        'severity': 'high' if value < threshold * 50 else 'medium',
                        'threshold': threshold * 100,
                        'deviation': threshold * 100 - value
                    })
            else:
                # Generic threshold for other metrics
                if value < threshold:
                    anomalies.append({
                        'metric': metric,
                        'value': value,
                        'type': 'performance',
                        'severity': 'high' if value < threshold * 0.5 else 'medium',
                        'threshold': threshold,
                        'deviation': threshold - value
                    })
        
        return anomalies
    
    def detect_trend_anomalies(self, data: List[float]) -> List[Dict[str, Any]]:
        """Detect anomalies in trend patterns"""
        if len(data) < 5:
            return []
        
        anomalies = []
        
        # Detect sudden changes in trend
        for i in range(2, len(data) - 2):
            # Calculate local trend before and after point
            before_trend = (data[i-1] - data[i-2]) if i >= 2 else 0
            after_trend = (data[i+1] - data[i]) if i < len(data) - 1 else 0
            
            # Check for trend reversal
            if before_trend > 0 and after_trend < -before_trend * 2:
                anomalies.append({
                    'index': i,
                    'value': data[i],
                    'type': 'trend_reversal',
                    'severity': 'high',
                    'before_trend': before_trend,
                    'after_trend': after_trend,
                    'change_magnitude': abs(after_trend - before_trend)
                })
            elif before_trend < 0 and after_trend > -before_trend * 2:
                anomalies.append({
                    'index': i,
                    'value': data[i],
                    'type': 'trend_reversal',
                    'severity': 'high',
                    'before_trend': before_trend,
                    'after_trend': after_trend,
                    'change_magnitude': abs(after_trend - before_trend)
                })
        
        return anomalies
    
    def detect_pattern_anomalies(self, data: List[Any]) -> List[Dict[str, Any]]:
        """Detect anomalies in pattern sequences"""
        if len(data) < 4:
            return []
        
        anomalies = []
        
        # Look for unexpected breaks in patterns
        for i in range(2, len(data) - 1):
            # Check if current item breaks a pattern
            if self._breaks_pattern(data, i):
                anomalies.append({
                    'index': i,
                    'value': data[i],
                    'type': 'pattern_break',
                    'severity': 'medium',
                    'context': data[max(0, i-2):i+3]
                })
        
        return anomalies
    
    def _breaks_pattern(self, data: List[Any], index: int) -> bool:
        """Check if value at index breaks an established pattern"""
        if index < 2 or index >= len(data) - 1:
            return False
        
        # Check for alternating pattern
        if index >= 2:
            if data[index-2] == data[index] and data[index-1] != data[index+1]:
                return True
        
        # Check for repeating pattern
        if index >= 3:
            pattern = data[index-3:index]
            if pattern == data[index-2:index+1][:-1]:  # Check if pattern continues
                return False
            else:
                return True
        
        return False
    
    def _calculate_percentile(self, data: List[float], value: float) -> float:
        """Calculate percentile rank of value in data"""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        rank = 0
        for i, v in enumerate(sorted_data):
            if v <= value:
                rank = i + 1
            else:
                break
        
        return (rank / len(sorted_data)) * 100
    
    def get_anomaly_summary(self, anomalies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary of detected anomalies"""
        if not anomalies:
            return {
                'total_anomalies': 0,
                'severity_counts': {'high': 0, 'medium': 0, 'low': 0},
                'type_counts': {},
                'risk_level': 'low'
            }
        
        severity_counts = {'high': 0, 'medium': 0, 'low': 0}
        type_counts = {}
        
        for anomaly in anomalies:
            severity = anomaly.get('severity', 'low')
            anomaly_type = anomaly.get('type', 'unknown')
            
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            type_counts[anomaly_type] = type_counts.get(anomaly_type, 0) + 1
        
        # Determine overall risk level
        if severity_counts['high'] > 0:
            risk_level = 'high'
        elif severity_counts['medium'] > 2:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'total_anomalies': len(anomalies),
            'severity_counts': severity_counts,
            'type_counts': type_counts,
            'risk_level': risk_level,
            'high_risk_anomalies': [a for a in anomalies if a.get('severity') == 'high']
        }


# Factory function for dependency injection
def create_anomaly_detection_engine(config: VectorAnalyticsConfig) -> AnomalyDetectionEngine:
    """Factory function to create anomaly detection engine with configuration"""
    return AnomalyDetectionEngine(config)


# Export for DI
__all__ = ['AnomalyDetectionEngine', 'create_anomaly_detection_engine']
