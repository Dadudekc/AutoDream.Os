#!/usr/bin/env python3
"""
Vector Analytics Pattern Analysis Engine
========================================

Pattern analysis engine for vector analytics system.
Handles behavioral patterns, temporal patterns, frequency analysis, and correlation detection.
V2 COMPLIANT: Focused pattern analysis under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR PATTERN ANALYSIS
@license MIT
"""

import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict

from ..vector_analytics_models import PatternMatch, VectorAnalyticsConfig


class PatternAnalysisEngine:
    """Pattern analysis engine for vector analytics"""
    
    def __init__(self, config: VectorAnalyticsConfig):
        """Initialize pattern analysis engine with configuration"""
        self.config = config
        self.pattern_cache: Dict[str, List[PatternMatch]] = {}
    
    def create_pattern_analysis_model(self) -> Dict[str, Any]:
        """Create pattern analysis processing model"""
        return {
            'model_type': 'pattern_analysis',
            'version': '1.0',
            'capabilities': [
                'behavioral_patterns',
                'temporal_patterns',
                'frequency_analysis',
                'correlation_detection',
                'clustering_analysis'
            ],
            'algorithms': {
                'pattern_detection': self.detect_patterns,
                'frequency_analysis': self.analyze_frequencies,
                'correlation_analysis': self.analyze_correlations,
                'clustering_analysis': self.perform_clustering
            }
        }
    
    def detect_patterns(self, data: List[Any], pattern_type: str = 'behavioral') -> List[PatternMatch]:
        """Detect patterns in data"""
        patterns = []
        
        if pattern_type == 'frequency':
            patterns.extend(self.detect_frequency_patterns(data))
        elif pattern_type == 'temporal':
            patterns.extend(self.detect_temporal_patterns(data))
        elif pattern_type == 'behavioral':
            patterns.extend(self.detect_behavioral_patterns(data))
        
        return patterns
    
    def detect_frequency_patterns(self, data: List[Any]) -> List[PatternMatch]:
        """Detect frequency-based patterns"""
        counter = Counter(data)
        patterns = []
        
        # Find most common patterns
        most_common = counter.most_common(5)
        for item, count in most_common:
            frequency = count / len(data)
            if frequency > 0.1:  # 10% threshold
                patterns.append(PatternMatch(
                    pattern_type='frequency',
                    pattern_data=item,
                    confidence=frequency,
                    metadata={'count': count, 'total': len(data)}
                ))
        
        return patterns
    
    def detect_temporal_patterns(self, data: List[Any]) -> List[PatternMatch]:
        """Detect temporal patterns in time-series data"""
        patterns = []
        
        if len(data) < 3:
            return patterns
        
        # Detect trends
        trend = self._calculate_trend(data)
        if abs(trend) > 0.1:  # 10% change threshold
            patterns.append(PatternMatch(
                pattern_type='temporal_trend',
                pattern_data=trend,
                confidence=min(abs(trend), 1.0),
                metadata={'direction': 'increasing' if trend > 0 else 'decreasing'}
            ))
        
        # Detect cycles (simplified)
        cycle_length = self._detect_cycle_length(data)
        if cycle_length > 0:
            patterns.append(PatternMatch(
                pattern_type='temporal_cycle',
                pattern_data=cycle_length,
                confidence=0.7,  # Simplified confidence
                metadata={'cycle_length': cycle_length}
            ))
        
        return patterns
    
    def detect_behavioral_patterns(self, data: List[Any]) -> List[PatternMatch]:
        """Detect behavioral patterns in data"""
        patterns = []
        
        if not data:
            return patterns
        
        # Detect sequences
        sequences = self._find_sequences(data)
        for sequence in sequences:
            if len(sequence) >= 3:  # Minimum sequence length
                patterns.append(PatternMatch(
                    pattern_type='behavioral_sequence',
                    pattern_data=sequence,
                    confidence=len(sequence) / 10.0,  # Normalized confidence
                    metadata={'sequence_length': len(sequence)}
                ))
        
        # Detect anomalies
        anomalies = self._detect_behavioral_anomalies(data)
        for anomaly in anomalies:
            patterns.append(PatternMatch(
                pattern_type='behavioral_anomaly',
                pattern_data=anomaly,
                confidence=anomaly.get('severity_score', 0.5),
                metadata={'anomaly_type': 'behavioral'}
            ))
        
        return patterns
    
    def analyze_frequencies(self, data: List[Any]) -> Dict[str, Any]:
        """Analyze frequency patterns"""
        counter = Counter(data)
        return {
            'frequencies': dict(counter.most_common(10)),
            'unique_count': len(counter),
            'total_count': len(data),
            'most_common': counter.most_common(1)[0] if counter else None
        }
    
    def analyze_correlations(self, data1: List[float], data2: List[float]) -> Dict[str, Any]:
        """Analyze correlations between two datasets"""
        if len(data1) != len(data2) or len(data1) < 2:
            return {'correlation': 0.0, 'strength': 'none', 'confidence': 0.0}
        
        # Calculate Pearson correlation coefficient
        correlation = self._calculate_pearson_correlation(data1, data2)
        
        # Determine strength
        if abs(correlation) > 0.7:
            strength = 'strong'
        elif abs(correlation) > 0.4:
            strength = 'moderate'
        elif abs(correlation) > 0.2:
            strength = 'weak'
        else:
            strength = 'none'
        
        return {
            'correlation': correlation,
            'strength': strength,
            'confidence': min(abs(correlation), 1.0),
            'sample_size': len(data1)
        }
    
    def perform_clustering(self, data: List[Any], num_clusters: int = 3) -> Dict[str, Any]:
        """Perform clustering analysis (simplified)"""
        if len(data) < num_clusters:
            return {'clusters': [], 'error': 'insufficient_data'}
        
        # Simple clustering based on value ranges
        clusters = defaultdict(list)
        data_sorted = sorted(data)
        
        # Divide data into clusters
        cluster_size = len(data_sorted) // num_clusters
        for i, value in enumerate(data_sorted):
            cluster_id = min(i // cluster_size, num_clusters - 1)
            clusters[cluster_id].append(value)
        
        # Calculate cluster statistics
        cluster_stats = {}
        for cluster_id, values in clusters.items():
            if values:
                cluster_stats[cluster_id] = {
                    'size': len(values),
                    'mean': statistics.mean(values),
                    'min': min(values),
                    'max': max(values)
                }
        
        return {
            'clusters': dict(clusters),
            'cluster_stats': cluster_stats,
            'num_clusters': num_clusters
        }
    
    def _calculate_trend(self, data: List[float]) -> float:
        """Calculate trend in data"""
        if len(data) < 2:
            return 0.0
        
        first_half = data[:len(data)//2]
        second_half = data[len(data)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        if first_avg == 0:
            return 0.0
        
        return (second_avg - first_avg) / first_avg
    
    def _detect_cycle_length(self, data: List[Any]) -> int:
        """Detect cycle length in data (simplified)"""
        if len(data) < 6:
            return 0
        
        # Look for repeating patterns
        for cycle_len in range(2, len(data) // 2):
            if self._is_cyclic(data, cycle_len):
                return cycle_len
        
        return 0
    
    def _is_cyclic(self, data: List[Any], cycle_len: int) -> bool:
        """Check if data is cyclic with given cycle length"""
        if len(data) < cycle_len * 2:
            return False
        
        # Check if first cycle matches second cycle
        first_cycle = data[:cycle_len]
        second_cycle = data[cycle_len:cycle_len * 2]
        
        return first_cycle == second_cycle
    
    def _find_sequences(self, data: List[Any]) -> List[List[Any]]:
        """Find repeating sequences in data"""
        sequences = []
        
        for seq_len in range(2, min(len(data) // 2, 10)):
            for i in range(len(data) - seq_len * 2 + 1):
                sequence = data[i:i + seq_len]
                next_sequence = data[i + seq_len:i + seq_len * 2]
                
                if sequence == next_sequence:
                    sequences.append(sequence)
        
        return sequences
    
    def _detect_behavioral_anomalies(self, data: List[Any]) -> List[Dict[str, Any]]:
        """Detect behavioral anomalies"""
        anomalies = []
        
        if len(data) < 3:
            return anomalies
        
        # Simple anomaly detection based on frequency
        counter = Counter(data)
        total_count = len(data)
        
        for item, count in counter.items():
            frequency = count / total_count
            if frequency < 0.05:  # Less than 5% frequency
                anomalies.append({
                    'item': item,
                    'frequency': frequency,
                    'severity_score': 1.0 - frequency
                })
        
        return anomalies
    
    def _calculate_pearson_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
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


# Factory function for dependency injection
def create_pattern_analysis_engine(config: VectorAnalyticsConfig) -> PatternAnalysisEngine:
    """Factory function to create pattern analysis engine with configuration"""
    return PatternAnalysisEngine(config)


# Export for DI
__all__ = ['PatternAnalysisEngine', 'create_pattern_analysis_engine']
