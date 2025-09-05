"""
Prediction Calculator - V2 Compliant Module
==========================================

Handles prediction value and confidence calculations.
Extracted from prediction_processor.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta


class PredictionCalculator:
    """
    Calculator for prediction values and confidence scores.
    
    Handles value calculation, confidence scoring, and metadata generation.
    """
    
    def __init__(self, config):
        """Initialize prediction calculator."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Calculation statistics
        self.calculation_stats = {
            'calculations_performed': 0,
            'calculation_errors': 0,
            'average_confidence': 0.0
        }
    
    def calculate_predicted_value(self, data: Dict[str, Any]) -> Any:
        """Calculate predicted value from data."""
        try:
            self.calculation_stats['calculations_performed'] += 1
            
            # Use provided value if available
            if 'value' in data:
                return data['value']
            
            # Use provided predicted_value if available
            if 'predicted_value' in data:
                return data['predicted_value']
            
            # Calculate based on data type and content
            if 'trend' in data:
                # Trend-based prediction
                trend = data['trend']
                if isinstance(trend, (int, float)):
                    return trend * 1.1  # 10% increase
                return trend
            
            if 'average' in data:
                # Average-based prediction
                avg = data['average']
                if isinstance(avg, (int, float)):
                    return avg
                return avg
            
            # Default prediction
            return 0
            
        except Exception as e:
            self.logger.error(f"Error calculating predicted value: {e}")
            self.calculation_stats['calculation_errors'] += 1
            return 0
    
    def calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score for prediction."""
        try:
            self.calculation_stats['calculations_performed'] += 1
            
            # Use provided confidence if available
            if 'confidence' in data:
                confidence = float(data['confidence'])
                self._update_confidence_stats(confidence)
                return confidence
            
            # Calculate based on data quality indicators
            confidence = 0.7  # Base confidence
            
            # Adjust based on data completeness
            required_fields = ['type']
            present_fields = sum(1 for field in required_fields if field in data and data[field])
            completeness = present_fields / len(required_fields)
            confidence *= completeness
            
            # Adjust based on data richness
            data_size = len(str(data))
            if data_size > 500:
                confidence *= 1.1  # Bonus for rich data
            elif data_size < 50:
                confidence *= 0.9  # Penalty for sparse data
            
            # Adjust based on prediction type
            prediction_type = data.get('type', 'general')
            if prediction_type in ['trend', 'forecast']:
                confidence *= 1.05  # Slight bonus for trend predictions
            elif prediction_type in ['anomaly', 'outlier']:
                confidence *= 0.95  # Slight penalty for anomaly predictions
            
            # Ensure confidence is within bounds
            confidence = min(max(confidence, 0.0), 1.0)
            
            self._update_confidence_stats(confidence)
            return confidence
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {e}")
            self.calculation_stats['calculation_errors'] += 1
            return 0.5  # Default confidence on error
    
    def generate_prediction_id(self) -> str:
        """Generate unique prediction ID."""
        timestamp = int(time.time() * 1000)
        return f"pred_{timestamp}"
    
    def calculate_expiration_time(self, data: Dict[str, Any]) -> Optional[datetime]:
        """Calculate prediction expiration time."""
        try:
            # Use provided expiration if available
            if 'expires_at' in data:
                expires_at = data['expires_at']
                if isinstance(expires_at, datetime):
                    return expires_at
                elif isinstance(expires_at, str):
                    return datetime.fromisoformat(expires_at)
            
            # Calculate based on prediction type
            prediction_type = data.get('type', 'general')
            if prediction_type in ['trend', 'forecast']:
                # Long-term predictions expire in 24 hours
                return datetime.now() + timedelta(hours=24)
            elif prediction_type in ['anomaly', 'outlier']:
                # Short-term predictions expire in 1 hour
                return datetime.now() + timedelta(hours=1)
            else:
                # Default expiration in 6 hours
                return datetime.now() + timedelta(hours=6)
            
        except Exception as e:
            self.logger.error(f"Error calculating expiration time: {e}")
            return None
    
    def generate_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate metadata for prediction."""
        try:
            metadata = {
                'generated_at': datetime.now().isoformat(),
                'data_source': data.get('source', 'unknown'),
                'prediction_type': data.get('type', 'general'),
                'data_quality': self._assess_data_quality(data)
            }
            
            # Add confidence-based metadata
            confidence = self.calculate_confidence(data)
            if confidence >= 0.9:
                metadata['confidence_level'] = 'high'
            elif confidence >= 0.7:
                metadata['confidence_level'] = 'medium'
            else:
                metadata['confidence_level'] = 'low'
            
            # Add processing metadata
            metadata['processing_timestamp'] = datetime.now().isoformat()
            metadata['data_size'] = len(str(data))
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error generating metadata: {e}")
            return {'generated_at': datetime.now().isoformat()}
    
    def _assess_data_quality(self, data: Dict[str, Any]) -> str:
        """Assess data quality level."""
        try:
            # Check data completeness
            required_fields = ['type']
            present_fields = sum(1 for field in required_fields if field in data and data[field])
            completeness = present_fields / len(required_fields)
            
            # Check data richness
            data_size = len(str(data))
            
            if completeness >= 0.8 and data_size > 200:
                return 'high'
            elif completeness >= 0.6 and data_size > 100:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            self.logger.error(f"Error assessing data quality: {e}")
            return 'unknown'
    
    def _update_confidence_stats(self, confidence: float):
        """Update confidence statistics."""
        try:
            if self.calculation_stats['average_confidence'] == 0:
                self.calculation_stats['average_confidence'] = confidence
            else:
                # Exponential moving average
                alpha = 0.1
                self.calculation_stats['average_confidence'] = (
                    alpha * confidence + 
                    (1 - alpha) * self.calculation_stats['average_confidence']
                )
        except Exception as e:
            self.logger.error(f"Error updating confidence stats: {e}")
    
    def get_calculation_stats(self) -> Dict[str, Any]:
        """Get calculation statistics."""
        return self.calculation_stats.copy()
    
    def reset_calculation_stats(self):
        """Reset calculation statistics."""
        self.calculation_stats = {
            'calculations_performed': 0,
            'calculation_errors': 0,
            'average_confidence': 0.0
        }
        self.logger.info("Prediction calculator statistics reset")
