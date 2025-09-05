#!/usr/bin/env python3
"""
ML Prediction Engine
====================

Prediction engine for ML optimization system.
Handles prediction generation, pattern matching, and weighted predictions.
V2 COMPLIANT: Focused prediction generation under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR PREDICTION
@license MIT
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import Counter

from ..ml_optimizer_models import (
    MLOptimizationConfig, LearningPattern, MLPrediction, create_ml_prediction
)
from .pattern_learning_engine import PatternLearningEngine


class PredictionEngine:
    """Prediction engine for ML optimization"""
    
    def __init__(self, config: MLOptimizationConfig, pattern_engine: PatternLearningEngine):
        """Initialize prediction engine with configuration and pattern engine"""
        self.config = config
        self.pattern_engine = pattern_engine
        self.prediction_cache: Dict[str, MLPrediction] = {}
    
    def generate_prediction(self, prediction_type: str, input_features: Dict[str, Any],
                          cache_key: Optional[str] = None) -> MLPrediction:
        """Generate prediction based on learned patterns"""
        try:
            # Check cache first
            if cache_key and cache_key in self.prediction_cache:
                cached_prediction = self.prediction_cache[cache_key]
                cached_prediction.metadata['cache_hit'] = True
                return cached_prediction
            
            # Find matching patterns
            matching_patterns = self.pattern_engine.find_similar_patterns(
                prediction_type, input_features, similarity_threshold=0.7
            )
            
            if not matching_patterns:
                # No matching patterns found
                prediction = create_ml_prediction(
                    prediction_type=prediction_type,
                    predicted_value=None,
                    confidence=0.0,
                    input_features=input_features,
                    metadata={'status': 'no_matching_patterns'}
                )
            else:
                # Generate prediction from patterns
                predicted_value, confidence = self._generate_prediction_from_patterns(
                    matching_patterns, input_features
                )
                
                prediction = create_ml_prediction(
                    prediction_type=prediction_type,
                    predicted_value=predicted_value,
                    confidence=confidence,
                    input_features=input_features,
                    metadata={
                        'matching_patterns_count': len(matching_patterns),
                        'top_pattern_similarity': matching_patterns[0].metadata.get('similarity', 0.0),
                        'generation_method': 'pattern_matching'
                    }
                )
            
            # Cache prediction
            if cache_key:
                self.prediction_cache[cache_key] = prediction
            
            return prediction
            
        except Exception as e:
            # Return error prediction
            return create_ml_prediction(
                prediction_type=prediction_type,
                predicted_value=None,
                confidence=0.0,
                input_features=input_features,
                metadata={'error': str(e), 'status': 'error'}
            )
    
    def _generate_prediction_from_patterns(self, patterns: List[LearningPattern],
                                         input_features: Dict[str, Any]) -> Tuple[Any, float]:
        """Generate prediction from matching patterns"""
        if not patterns:
            return None, 0.0
        
        # Weighted prediction based on pattern similarity, frequency, and accuracy
        weighted_values = []
        total_weight = 0.0
        
        for pattern in patterns:
            similarity = pattern.metadata.get('similarity', 0.0)
            frequency_weight = min(1.0, pattern.frequency / 100.0)  # Normalize frequency
            accuracy_weight = pattern.accuracy
            
            # Combined weight
            weight = similarity * 0.5 + frequency_weight * 0.3 + accuracy_weight * 0.2
            
            weighted_values.append((pattern.target_value, weight))
            total_weight += weight
        
        if total_weight == 0:
            # Fallback to simple average
            if isinstance(patterns[0].target_value, (int, float)):
                avg_value = sum(p.target_value for p in patterns) / len(patterns)
                return avg_value, 0.5
            else:
                # For non-numeric values, return most frequent
                values = [p.target_value for p in patterns]
                most_common = Counter(values).most_common(1)[0][0]
                return most_common, 0.5
        
        # Calculate weighted prediction
        if isinstance(patterns[0].target_value, (int, float)):
            # Numerical prediction
            weighted_sum = sum(value * weight for value, weight in weighted_values)
            predicted_value = weighted_sum / total_weight
            confidence = min(total_weight / len(patterns), 1.0)
        else:
            # Categorical prediction - weighted voting
            value_weights = {}
            for value, weight in weighted_values:
                if value not in value_weights:
                    value_weights[value] = 0.0
                value_weights[value] += weight
            
            # Find value with highest weight
            predicted_value = max(value_weights.items(), key=lambda x: x[1])[0]
            confidence = value_weights[predicted_value] / total_weight
        
        return predicted_value, confidence
    
    def batch_predict(self, predictions: List[Dict[str, Any]]) -> List[MLPrediction]:
        """Generate multiple predictions in batch"""
        results = []
        
        for pred_data in predictions:
            prediction_type = pred_data.get('prediction_type', 'default')
            input_features = pred_data.get('input_features', {})
            cache_key = pred_data.get('cache_key')
            
            prediction = self.generate_prediction(
                prediction_type, input_features, cache_key
            )
            results.append(prediction)
        
        return results
    
    def validate_prediction(self, prediction: MLPrediction, actual_value: Any) -> Dict[str, Any]:
        """Validate prediction against actual value"""
        try:
            predicted_value = prediction.predicted_value
            confidence = prediction.confidence
            
            # Calculate accuracy
            if predicted_value is None:
                accuracy = 0.0
            elif isinstance(predicted_value, (int, float)) and isinstance(actual_value, (int, float)):
                # Numerical accuracy
                if actual_value == 0:
                    accuracy = 1.0 if predicted_value == 0 else 0.0
                else:
                    error = abs(predicted_value - actual_value) / abs(actual_value)
                    accuracy = max(0.0, 1.0 - error)
            else:
                # Categorical accuracy
                accuracy = 1.0 if predicted_value == actual_value else 0.0
            
            # Calculate confidence-weighted accuracy
            weighted_accuracy = accuracy * confidence
            
            validation_result = {
                'prediction_id': prediction.prediction_id,
                'predicted_value': predicted_value,
                'actual_value': actual_value,
                'accuracy': accuracy,
                'confidence': confidence,
                'weighted_accuracy': weighted_accuracy,
                'validation_timestamp': datetime.now().isoformat()
            }
            
            return validation_result
            
        except Exception as e:
            return {
                'prediction_id': prediction.prediction_id,
                'error': str(e),
                'validation_timestamp': datetime.now().isoformat()
            }
    
    def get_prediction_statistics(self) -> Dict[str, Any]:
        """Get statistics about predictions"""
        if not self.prediction_cache:
            return {
                'total_predictions': 0,
                'cache_hit_rate': 0.0,
                'avg_confidence': 0.0,
                'prediction_types': {}
            }
        
        total_predictions = len(self.prediction_cache)
        cache_hits = sum(1 for p in self.prediction_cache.values() 
                        if p.metadata.get('cache_hit', False))
        cache_hit_rate = cache_hits / total_predictions if total_predictions > 0 else 0.0
        
        confidences = [p.confidence for p in self.prediction_cache.values()]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        prediction_types = {}
        for prediction in self.prediction_cache.values():
            pred_type = prediction.prediction_type
            prediction_types[pred_type] = prediction_types.get(pred_type, 0) + 1
        
        return {
            'total_predictions': total_predictions,
            'cache_hit_rate': cache_hit_rate,
            'avg_confidence': avg_confidence,
            'prediction_types': prediction_types,
            'cache_size': len(self.prediction_cache)
        }
    
    def clear_cache(self):
        """Clear prediction cache"""
        self.prediction_cache.clear()
    
    def get_cached_predictions(self, prediction_type: Optional[str] = None) -> List[MLPrediction]:
        """Get cached predictions, optionally filtered by type"""
        if prediction_type:
            return [
                p for p in self.prediction_cache.values()
                if p.prediction_type == prediction_type
            ]
        return list(self.prediction_cache.values())
    
    def export_predictions(self) -> Dict[str, Any]:
        """Export predictions for analysis"""
        return {
            'predictions': {pid: pred.to_dict() for pid, pred in self.prediction_cache.items()},
            'statistics': self.get_prediction_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }


# Factory function for dependency injection
def create_prediction_engine(config: MLOptimizationConfig, 
                           pattern_engine: PatternLearningEngine) -> PredictionEngine:
    """Factory function to create prediction engine with dependencies"""
    return PredictionEngine(config, pattern_engine)


# Export for DI
__all__ = ['PredictionEngine', 'create_prediction_engine']
