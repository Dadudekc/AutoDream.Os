"""
Validation Core - Modularized from Validation Manager
Captain Agent-3: MODULAR-001 Implementation
"""

import logging
from typing import Dict, Any, List, Optional
from .modules.validation_module import ValidationModule
from .validators.base_validator import BaseValidator

class ValidationCore:
    """Core validation functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_modules = {}
        self.validators = {}
        self.validation_history = []
    
    def register_validator(self, validator_name: str, validator: BaseValidator) -> bool:
        """Register a validator"""
        try:
            self.validators[validator_name] = validator
            self.logger.info(f"Validator {validator_name} registered")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register validator: {e}")
            return False
    
    def validate_data(self, data: Any, validator_name: str) -> Dict[str, Any]:
        """Validate data using specified validator"""
        try:
            if validator_name in self.validators:
                validator = self.validators[validator_name]
                result = validator.validate(data)
                
                validation_record = {
                    "validator": validator_name,
                    "data_type": type(data).__name__,
                    "result": result,
                    "timestamp": "2025-08-28T22:55:00.000000Z"
                }
                
                self.validation_history.append(validation_record)
                return result
            else:
                return {"error": f"Validator {validator_name} not found"}
                
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return {"error": str(e)}
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics"""
        return {
            "total_validations": len(self.validation_history),
            "registered_validators": len(self.validators),
            "validation_modules": len(self.validation_modules)
        }
