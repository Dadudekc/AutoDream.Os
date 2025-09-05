#!/usr/bin/env python3
"""
Prediction Validator - KISS Compliant
====================================

Simple prediction validation.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class PredictionValidator:
    """Simple prediction validator."""
    
    def __init__(self, config=None):
        """Initialize validator."""
        self.config = config or {}
        self.logger = logger
    
    def validate_input_data(self, data: Dict[str, Any]) -> bool:
        """Validate input data."""
        if not isinstance(data, dict):
            self.logger.error("Input data must be a dictionary")
            return False
        
        if not data:
            self.logger.error("Input data cannot be empty")
            return False
        
        return True
    
    def validate_prediction_result(self, result: Dict[str, Any]) -> bool:
        """Validate prediction result."""
        if not isinstance(result, dict):
            self.logger.error("Prediction result must be a dictionary")
            return False
        
        required_fields = ['prediction_id', 'predicted_value', 'confidence']
        for field in required_fields:
            if field not in result:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        return True

__all__ = ["PredictionValidator"]
