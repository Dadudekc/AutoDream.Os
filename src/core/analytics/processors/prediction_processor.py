"""
Prediction Processor - V2 Compliant Module
=========================================

Main prediction processor that coordinates all prediction components.
Refactored from monolithic prediction_processor.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from ...vector_analytics_models import (
    PredictionResult, create_prediction_result, validate_prediction_result
)
from .prediction_validator import PredictionValidator
from .prediction_calculator import PredictionCalculator
from .prediction_analyzer import PredictionAnalyzer


class PredictionProcessor:
    """
    Main prediction generation and analysis processing engine.
    
    Coordinates validation, calculation, and analysis components.
    """
    
    def __init__(self, config):
        """Initialize prediction processor."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.validator = PredictionValidator(config)
        self.calculator = PredictionCalculator(config)
        self.analyzer = PredictionAnalyzer(config)
        
        # Processing statistics
        self.processing_stats = {
            'predictions_generated': 0,
            'validation_errors': 0,
            'processing_errors': 0,
            'average_processing_time': 0.0
        }
    
    def generate_prediction(self, data: Dict[str, Any]) -> Optional[PredictionResult]:
        """Generate prediction from input data."""
        start_time = time.time()
        
        try:
            # Validate input data
            if not self.validator.validate_input_data(data):
                self._record_validation_error("Input data validation failed")
                return None
            
            # Generate prediction ID
            prediction_id = self.calculator.generate_prediction_id()
            
            # Calculate predicted value
            predicted_value = self.calculator.calculate_predicted_value(data)
            
            # Calculate confidence
            confidence = self.calculator.calculate_confidence(data)
            
            # Calculate expiration time
            expires_at = self.calculator.calculate_expiration_time(data)
            
            # Generate metadata
            metadata = self.calculator.generate_metadata(data)
            
            # Create prediction result
            prediction = create_prediction_result(
                prediction_id=prediction_id,
                prediction_type=data.get('type', 'general'),
                predicted_value=predicted_value,
                confidence=confidence,
                expires_at=expires_at,
                metadata=metadata
            )
            
            # Validate prediction result
            if not self.validator.validate_prediction_result(prediction):
                self._record_validation_error("Prediction result validation failed")
                return None
            
            # Apply post-processing
            prediction = self.analyzer.apply_post_processing(prediction)
            
            # Update statistics
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, True)
            
            self.logger.info(f"Prediction generated: {prediction_id}")
            return prediction
            
        except Exception as e:
            self.logger.error(f"Error generating prediction: {e}")
            self._record_processing_error(str(e))
            processing_time = time.time() - start_time
            self._update_processing_stats(processing_time, False)
            return None
    
    def analyze_prediction(self, prediction: PredictionResult) -> Dict[str, Any]:
        """Analyze prediction result."""
        return self.analyzer.analyze_prediction(prediction)
    
    def get_prediction_summary(self, prediction: PredictionResult) -> Dict[str, Any]:
        """Get summary information for a prediction."""
        return self.analyzer.get_prediction_summary(prediction)
    
    def validate_prediction_data(self, data: Dict[str, Any]) -> bool:
        """Validate prediction data without processing."""
        return self.validator.validate_prediction_data(data)
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics."""
        stats = self.processing_stats.copy()
        
        # Add component statistics
        stats['validator_stats'] = self.validator.get_validation_stats()
        stats['calculator_stats'] = self.calculator.get_calculation_stats()
        stats['analyzer_stats'] = self.analyzer.get_analysis_stats()
        
        return stats
    
    def reset_stats(self):
        """Reset all processing statistics."""
        self.processing_stats = {
            'predictions_generated': 0,
            'validation_errors': 0,
            'processing_errors': 0,
            'average_processing_time': 0.0
        }
        
        # Reset component statistics
        self.validator.reset_validation_stats()
        self.calculator.reset_calculation_stats()
        self.analyzer.reset_analysis_stats()
        
        self.logger.info("Prediction processor statistics reset")
    
    def _record_validation_error(self, error_message: str):
        """Record validation error."""
        self.processing_stats['validation_errors'] += 1
        self.logger.warning(f"Validation error: {error_message}")
    
    def _record_processing_error(self, error_message: str):
        """Record processing error."""
        self.processing_stats['processing_errors'] += 1
        self.logger.error(f"Processing error: {error_message}")
    
    def _update_processing_stats(self, processing_time: float, success: bool):
        """Update processing statistics."""
        if success:
            self.processing_stats['predictions_generated'] += 1
            
            # Update average processing time
            if self.processing_stats['average_processing_time'] == 0:
                self.processing_stats['average_processing_time'] = processing_time
            else:
                # Exponential moving average
                alpha = 0.1
                self.processing_stats['average_processing_time'] = (
                    alpha * processing_time + 
                    (1 - alpha) * self.processing_stats['average_processing_time']
                )
        else:
            self.processing_stats['processing_errors'] += 1
