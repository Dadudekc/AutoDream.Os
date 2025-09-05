#!/usr/bin/env python3
"""
ML Feature Analysis Engine
==========================

Feature analysis engine for ML optimization system.
Handles feature extraction, similarity calculation, and feature processing.
V2 COMPLIANT: Focused feature analysis under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR FEATURE ANALYSIS
@license MIT
"""

import statistics
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import Counter


class FeatureAnalysisEngine:
    """Feature analysis engine for ML optimization"""
    
    def __init__(self):
        """Initialize feature analysis engine"""
        self.feature_cache: Dict[str, Any] = {}
        self.similarity_cache: Dict[str, float] = {}
    
    def extract_features(self, data: Any, feature_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Extract features from raw data"""
        if feature_types is None:
            feature_types = ['basic', 'statistical', 'categorical']
        
        features = {}
        
        for feature_type in feature_types:
            if feature_type == 'basic':
                features.update(self._extract_basic_features(data))
            elif feature_type == 'statistical':
                features.update(self._extract_statistical_features(data))
            elif feature_type == 'categorical':
                features.update(self._extract_categorical_features(data))
            elif feature_type == 'temporal':
                features.update(self._extract_temporal_features(data))
        
        return features
    
    def _extract_basic_features(self, data: Any) -> Dict[str, Any]:
        """Extract basic features from data"""
        features = {}
        
        if isinstance(data, (list, tuple)):
            features['length'] = len(data)
            features['is_empty'] = len(data) == 0
            features['data_type'] = 'sequence'
        elif isinstance(data, dict):
            features['key_count'] = len(data)
            features['is_empty'] = len(data) == 0
            features['data_type'] = 'mapping'
        elif isinstance(data, (int, float)):
            features['value'] = data
            features['data_type'] = 'numeric'
        elif isinstance(data, str):
            features['length'] = len(data)
            features['is_empty'] = len(data) == 0
            features['data_type'] = 'string'
        else:
            features['data_type'] = type(data).__name__
        
        return features
    
    def _extract_statistical_features(self, data: Any) -> Dict[str, Any]:
        """Extract statistical features from data"""
        features = {}
        
        if isinstance(data, (list, tuple)) and all(isinstance(x, (int, float)) for x in data):
            if len(data) > 0:
                features['mean'] = statistics.mean(data)
                features['median'] = statistics.median(data)
                features['std'] = statistics.stdev(data) if len(data) > 1 else 0
                features['min'] = min(data)
                features['max'] = max(data)
                features['range'] = max(data) - min(data)
                features['sum'] = sum(data)
                features['count'] = len(data)
        elif isinstance(data, dict) and all(isinstance(v, (int, float)) for v in data.values()):
            values = list(data.values())
            if len(values) > 0:
                features['mean'] = statistics.mean(values)
                features['median'] = statistics.median(values)
                features['std'] = statistics.stdev(values) if len(values) > 1 else 0
                features['min'] = min(values)
                features['max'] = max(values)
                features['range'] = max(values) - min(values)
                features['sum'] = sum(values)
                features['count'] = len(values)
        
        return features
    
    def _extract_categorical_features(self, data: Any) -> Dict[str, Any]:
        """Extract categorical features from data"""
        features = {}
        
        if isinstance(data, (list, tuple)):
            counter = Counter(data)
            features['unique_count'] = len(counter)
            features['most_common'] = counter.most_common(1)[0] if counter else None
            features['entropy'] = self._calculate_entropy(counter)
        elif isinstance(data, dict):
            features['key_count'] = len(data)
            features['value_types'] = list(set(type(v).__name__ for v in data.values()))
            features['has_numeric_values'] = any(isinstance(v, (int, float)) for v in data.values())
            features['has_string_values'] = any(isinstance(v, str) for v in data.values())
        
        return features
    
    def _extract_temporal_features(self, data: Any) -> Dict[str, Any]:
        """Extract temporal features from data"""
        features = {}
        
        if isinstance(data, (list, tuple)) and all(isinstance(x, datetime) for x in data):
            if len(data) > 1:
                timestamps = [x.timestamp() for x in data]
                features['time_span'] = max(timestamps) - min(timestamps)
                features['avg_interval'] = statistics.mean(
                    [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
                ) if len(timestamps) > 1 else 0
                features['is_chronological'] = all(
                    data[i] <= data[i+1] for i in range(len(data)-1)
                )
        elif isinstance(data, dict):
            # Look for timestamp-like keys or values
            timestamp_keys = [k for k in data.keys() if 'time' in k.lower() or 'date' in k.lower()]
            features['has_temporal_keys'] = len(timestamp_keys) > 0
            features['temporal_key_count'] = len(timestamp_keys)
        
        return features
    
    def calculate_similarity(self, features1: Dict[str, Any], features2: Dict[str, Any],
                           method: str = 'weighted') -> float:
        """Calculate similarity between two feature sets"""
        if not features1 or not features2:
            return 0.0
        
        # Create cache key
        cache_key = f"{hash(str(sorted(features1.items())))}_{hash(str(sorted(features2.items())))}"
        if cache_key in self.similarity_cache:
            return self.similarity_cache[cache_key]
        
        if method == 'jaccard':
            similarity = self._jaccard_similarity(features1, features2)
        elif method == 'cosine':
            similarity = self._cosine_similarity(features1, features2)
        elif method == 'weighted':
            similarity = self._weighted_similarity(features1, features2)
        else:
            similarity = self._jaccard_similarity(features1, features2)
        
        # Cache result
        self.similarity_cache[cache_key] = similarity
        return similarity
    
    def _jaccard_similarity(self, features1: Dict[str, Any], features2: Dict[str, Any]) -> float:
        """Calculate Jaccard similarity between feature sets"""
        keys1 = set(features1.keys())
        keys2 = set(features2.keys())
        
        intersection = keys1.intersection(keys2)
        union = keys1.union(keys2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _cosine_similarity(self, features1: Dict[str, Any], features2: Dict[str, Any]) -> float:
        """Calculate cosine similarity between feature sets"""
        # Convert to numerical vectors
        all_keys = set(features1.keys()).union(set(features2.keys()))
        
        if not all_keys:
            return 0.0
        
        vec1 = []
        vec2 = []
        
        for key in all_keys:
            val1 = self._normalize_value(features1.get(key, 0))
            val2 = self._normalize_value(features2.get(key, 0))
            vec1.append(val1)
            vec2.append(val2)
        
        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _weighted_similarity(self, features1: Dict[str, Any], features2: Dict[str, Any]) -> float:
        """Calculate weighted similarity between feature sets"""
        common_keys = set(features1.keys()).intersection(set(features2.keys()))
        
        if not common_keys:
            return 0.0
        
        similarities = []
        weights = []
        
        for key in common_keys:
            val1 = features1[key]
            val2 = features2[key]
            
            # Calculate value similarity
            if val1 == val2:
                similarity = 1.0
            elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                max_val = max(abs(val1), abs(val2), 1.0)
                similarity = max(0.0, 1.0 - abs(val1 - val2) / max_val)
            else:
                similarity = 0.0
            
            # Weight based on feature importance
            weight = self._get_feature_weight(key)
            
            similarities.append(similarity)
            weights.append(weight)
        
        # Calculate weighted average
        if not similarities:
            return 0.0
        
        total_weight = sum(weights)
        if total_weight == 0:
            return sum(similarities) / len(similarities)
        
        weighted_similarity = sum(s * w for s, w in zip(similarities, weights)) / total_weight
        return weighted_similarity
    
    def _normalize_value(self, value: Any) -> float:
        """Normalize value to float for similarity calculation"""
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            return float(len(value))  # Use string length
        elif isinstance(value, bool):
            return 1.0 if value else 0.0
        else:
            return 0.0
    
    def _get_feature_weight(self, feature_name: str) -> float:
        """Get weight for feature based on its name"""
        # Higher weights for more important features
        if any(keyword in feature_name.lower() for keyword in ['id', 'key', 'type']):
            return 2.0
        elif any(keyword in feature_name.lower() for keyword in ['count', 'length', 'size']):
            return 1.5
        elif any(keyword in feature_name.lower() for keyword in ['mean', 'avg', 'median']):
            return 1.2
        else:
            return 1.0
    
    def _calculate_entropy(self, counter: Counter) -> float:
        """Calculate entropy of a counter"""
        total = sum(counter.values())
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in counter.values():
            probability = count / total
            if probability > 0:
                entropy -= probability * (probability.bit_length() - 1)
        
        return entropy
    
    def get_feature_importance(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Calculate importance scores for features"""
        importance = {}
        
        for key, value in features.items():
            score = 0.0
            
            # Base score from feature name
            score += self._get_feature_weight(key)
            
            # Score from value characteristics
            if isinstance(value, (int, float)) and value != 0:
                score += 1.0
            elif isinstance(value, str) and len(value) > 0:
                score += 0.5
            elif isinstance(value, (list, tuple)) and len(value) > 0:
                score += 0.8
            
            importance[key] = score
        
        return importance
    
    def clear_cache(self):
        """Clear feature and similarity caches"""
        self.feature_cache.clear()
        self.similarity_cache.clear()


# Factory function for dependency injection
def create_feature_analysis_engine() -> FeatureAnalysisEngine:
    """Factory function to create feature analysis engine"""
    return FeatureAnalysisEngine()


# Export for DI
__all__ = ['FeatureAnalysisEngine', 'create_feature_analysis_engine']
