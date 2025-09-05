"""
Prediction Analyzer - V2 Compliant Module
========================================

Handles prediction analysis and post-processing.
Extracted from prediction_processor.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from ...vector_analytics_models import PredictionResult


class PredictionAnalyzer:
    """
    Analyzer for prediction results and post-processing.
    
    Handles prediction analysis, post-processing, and summary generation.
    """
    
    def __init__(self, config):
        """Initialize prediction analyzer."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Analysis statistics
        self.analysis_stats = {
            'analyses_performed': 0,
            'analysis_errors': 0,
            'average_analysis_time': 0.0
        }
    
    def analyze_prediction(self, prediction: PredictionResult) -> Dict[str, Any]:
        """Analyze prediction result."""
        try:
            start_time = time.time()
            self.analysis_stats['analyses_performed'] += 1
            
            analysis = {
                'prediction_id': prediction.prediction_id,
                'analysis_timestamp': datetime.now().isoformat(),
                'confidence_analysis': self._analyze_confidence(prediction),
                'timing_analysis': self._analyze_timing(prediction),
                'metadata_analysis': self._analyze_metadata(prediction),
                'quality_score': self._calculate_quality_score(prediction)
            }
            
            # Update analysis time
            analysis_time = time.time() - start_time
            self._update_analysis_stats(analysis_time, True)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing prediction: {e}")
            self.analysis_stats['analysis_errors'] += 1
            return {'error': str(e)}
    
    def apply_post_processing(self, prediction: PredictionResult) -> PredictionResult:
        """Apply post-processing to prediction."""
        try:
            # Add confidence-based metadata
            if prediction.confidence >= 0.9:
                prediction.metadata['confidence_level'] = 'high'
            elif prediction.confidence >= 0.7:
                prediction.metadata['confidence_level'] = 'medium'
            else:
                prediction.metadata['confidence_level'] = 'low'
            
            # Add expiration warning
            if prediction.expires_at:
                time_to_expiry = prediction.expires_at - datetime.now()
                if time_to_expiry.total_seconds() < 3600:  # Less than 1 hour
                    prediction.metadata['expiration_warning'] = 'expires_soon'
            
            # Add analysis metadata
            prediction.metadata['post_processed'] = True
            prediction.metadata['post_processed_at'] = datetime.now().isoformat()
            
            return prediction
            
        except Exception as e:
            self.logger.error(f"Error in post-processing: {e}")
            return prediction
    
    def get_prediction_summary(self, prediction: PredictionResult) -> Dict[str, Any]:
        """Get summary information for a prediction."""
        try:
            return {
                'prediction_id': prediction.prediction_id,
                'prediction_type': prediction.prediction_type,
                'predicted_value': prediction.predicted_value,
                'confidence': prediction.confidence,
                'expires_at': prediction.expires_at.isoformat() if prediction.expires_at else None,
                'metadata': prediction.metadata,
                'timestamp': prediction.timestamp.isoformat(),
                'quality_score': self._calculate_quality_score(prediction)
            }
        except Exception as e:
            self.logger.error(f"Error getting prediction summary: {e}")
            return {'error': str(e)}
    
    def _analyze_confidence(self, prediction: PredictionResult) -> Dict[str, Any]:
        """Analyze prediction confidence."""
        try:
            confidence = prediction.confidence
            
            analysis = {
                'confidence_value': confidence,
                'confidence_level': 'high' if confidence >= 0.9 else 'medium' if confidence >= 0.7 else 'low',
                'reliability': 'high' if confidence >= 0.8 else 'medium' if confidence >= 0.6 else 'low'
            }
            
            # Add confidence trends if available
            if 'confidence_history' in prediction.metadata:
                history = prediction.metadata['confidence_history']
                if isinstance(history, list) and len(history) > 1:
                    analysis['confidence_trend'] = 'increasing' if history[-1] > history[0] else 'decreasing'
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing confidence: {e}")
            return {'error': str(e)}
    
    def _analyze_timing(self, prediction: PredictionResult) -> Dict[str, Any]:
        """Analyze prediction timing."""
        try:
            now = datetime.now()
            
            analysis = {
                'generated_at': prediction.timestamp.isoformat(),
                'age_seconds': (now - prediction.timestamp).total_seconds(),
                'expires_at': prediction.expires_at.isoformat() if prediction.expires_at else None
            }
            
            if prediction.expires_at:
                time_to_expiry = prediction.expires_at - now
                analysis['time_to_expiry_seconds'] = time_to_expiry.total_seconds()
                analysis['is_expired'] = time_to_expiry.total_seconds() <= 0
                analysis['expires_soon'] = time_to_expiry.total_seconds() < 3600  # Less than 1 hour
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing timing: {e}")
            return {'error': str(e)}
    
    def _analyze_metadata(self, prediction: PredictionResult) -> Dict[str, Any]:
        """Analyze prediction metadata."""
        try:
            metadata = prediction.metadata
            
            analysis = {
                'metadata_count': len(metadata),
                'has_quality_info': 'data_quality' in metadata,
                'has_source_info': 'data_source' in metadata,
                'has_processing_info': 'processing_timestamp' in metadata
            }
            
            # Analyze metadata quality
            quality_fields = ['data_quality', 'confidence_level', 'generated_at']
            present_quality_fields = sum(1 for field in quality_fields if field in metadata)
            analysis['metadata_completeness'] = present_quality_fields / len(quality_fields)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing metadata: {e}")
            return {'error': str(e)}
    
    def _calculate_quality_score(self, prediction: PredictionResult) -> float:
        """Calculate overall quality score for prediction."""
        try:
            score = 0.0
            
            # Base score from confidence
            score += prediction.confidence * 0.4
            
            # Metadata completeness score
            metadata = prediction.metadata
            quality_fields = ['data_quality', 'confidence_level', 'generated_at']
            present_fields = sum(1 for field in quality_fields if field in metadata)
            completeness = present_fields / len(quality_fields)
            score += completeness * 0.3
            
            # Timing score (fresher is better)
            age_hours = (datetime.now() - prediction.timestamp).total_seconds() / 3600
            timing_score = max(0, 1 - (age_hours / 24))  # Decay over 24 hours
            score += timing_score * 0.3
            
            return min(max(score, 0.0), 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating quality score: {e}")
            return 0.5  # Default score on error
    
    def _update_analysis_stats(self, analysis_time: float, success: bool):
        """Update analysis statistics."""
        try:
            if success:
                # Update average analysis time
                if self.analysis_stats['average_analysis_time'] == 0:
                    self.analysis_stats['average_analysis_time'] = analysis_time
                else:
                    # Exponential moving average
                    alpha = 0.1
                    self.analysis_stats['average_analysis_time'] = (
                        alpha * analysis_time + 
                        (1 - alpha) * self.analysis_stats['average_analysis_time']
                    )
            else:
                self.analysis_stats['analysis_errors'] += 1
        except Exception as e:
            self.logger.error(f"Error updating analysis stats: {e}")
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get analysis statistics."""
        return self.analysis_stats.copy()
    
    def reset_analysis_stats(self):
        """Reset analysis statistics."""
        self.analysis_stats = {
            'analyses_performed': 0,
            'analysis_errors': 0,
            'average_analysis_time': 0.0
        }
        self.logger.info("Prediction analyzer statistics reset")
