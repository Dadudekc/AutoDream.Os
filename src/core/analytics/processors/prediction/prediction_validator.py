"""
Prediction Validator - V2 Compliant Module
=========================================

Handles prediction validation and data validation.
Extracted from prediction_processor.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from ...vector_analytics_models import PredictionResult, validate_prediction_result


class PredictionValidator:
    """
    Validator for prediction data and results.
    
    Handles input validation, prediction validation, and data quality checks.
    """
    
    def __init__(self, config):
        """Initialize prediction validator."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Validation statistics
        self.validation_stats = {
            'validations_performed': 0,
            'validation_errors': 0,
            'validation_success_rate': 0.0
        }
    
    def validate_input_data(self, data: Dict[str, Any]) -> bool:
        """Validate input data for prediction generation."""
        try:
            self.validation_stats['validations_performed'] += 1
            
            # Check required fields
            if not isinstance(data, dict):
                self._record_validation_error("Input data must be a dictionary")
                return False
            
            # Check data structure
            if not data:
                self._record_validation_error("Input data cannot be empty")
                return False
            
            # Validate confidence if present
            if 'confidence' in data:
                confidence = data['confidence']
                if not isinstance(confidence, (int, float)) or not 0.0 <= confidence <= 1.0:
                    self._record_validation_error("Confidence must be between 0.0 and 1.0")
                    return False
            
            # Validate prediction type if present
            if 'type' in data:
                prediction_type = data['type']
                if not isinstance(prediction_type, str) or not prediction_type.strip():
                    self._record_validation_error("Prediction type must be a non-empty string")
                    return False
            
            # Update success rate
            self._update_validation_stats(True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating input data: {e}")
            self._record_validation_error(str(e))
            return False
    
    def validate_prediction_result(self, prediction: PredictionResult) -> bool:
        """Validate prediction result."""
        try:
            self.validation_stats['validations_performed'] += 1
            
            # Use the model validation function
            is_valid = validate_prediction_result(prediction)
            
            if not is_valid:
                self._record_validation_error("Prediction result validation failed")
                return False
            
            # Additional custom validations
            if not self._validate_prediction_metadata(prediction):
                return False
            
            if not self._validate_prediction_timing(prediction):
                return False
            
            # Update success rate
            self._update_validation_stats(True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating prediction result: {e}")
            self._record_validation_error(str(e))
            return False
    
    def _validate_prediction_metadata(self, prediction: PredictionResult) -> bool:
        """Validate prediction metadata."""
        try:
            if not isinstance(prediction.metadata, dict):
                self._record_validation_error("Prediction metadata must be a dictionary")
                return False
            
            # Check for required metadata fields
            required_metadata = ['generated_at']
            for field in required_metadata:
                if field not in prediction.metadata:
                    self._record_validation_error(f"Missing required metadata field: {field}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating prediction metadata: {e}")
            return False
    
    def _validate_prediction_timing(self, prediction: PredictionResult) -> bool:
        """Validate prediction timing."""
        try:
            # Check if prediction is not expired
            if prediction.expires_at:
                if prediction.expires_at <= datetime.now():
                    self._record_validation_error("Prediction has expired")
                    return False
            
            # Check if prediction timestamp is reasonable
            if prediction.timestamp:
                time_diff = datetime.now() - prediction.timestamp
                if time_diff.total_seconds() > 86400:  # More than 24 hours old
                    self._record_validation_error("Prediction timestamp is too old")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating prediction timing: {e}")
            return False
    
    def validate_prediction_data(self, data: Dict[str, Any]) -> bool:
        """Validate prediction data without processing."""
        return self.validate_input_data(data)
    
    def _record_validation_error(self, error_message: str):
        """Record validation error."""
        self.validation_stats['validation_errors'] += 1
        self.logger.warning(f"Validation error: {error_message}")
    
    def _update_validation_stats(self, success: bool):
        """Update validation statistics."""
        if success:
            # Calculate success rate
            total_validations = self.validation_stats['validations_performed']
            errors = self.validation_stats['validation_errors']
            self.validation_stats['validation_success_rate'] = (
                (total_validations - errors) / total_validations * 100
                if total_validations > 0 else 100.0
            )
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics."""
        return self.validation_stats.copy()
    
    def reset_validation_stats(self):
        """Reset validation statistics."""
        self.validation_stats = {
            'validations_performed': 0,
            'validation_errors': 0,
            'validation_success_rate': 0.0
        }
        self.logger.info("Prediction validator statistics reset")
