"""Modularization of the validation manager."""
from __future__ import annotations

from pathlib import Path

from .generator import write_file


def modularize() -> None:
    validation_path = Path("src/core/validation")
    modules_path = validation_path / "modules"
    validators_path = validation_path / "validators"

    for path in (modules_path, validators_path):
        path.mkdir(parents=True, exist_ok=True)

    validation_core = validation_path / "validation_core.py"
    core_content = '''"""
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
                    "timestamp": "2025-08-28T22:55:00.000000Z",
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
            "validation_modules": len(self.validation_modules),
        }
'''
    write_file(validation_core, core_content)

    base_validator = validators_path / "base_validator.py"
    base_validator_content = '''"""
Base Validator - Abstract Validator Interface
Captain Agent-3: MODULAR-001 Implementation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseValidator(ABC):
    """Abstract base validator"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def validate(self, data: Any) -> Dict[str, Any]:
        """Validate data"""
        pass

    def get_validator_info(self) -> Dict[str, Any]:
        """Get validator information"""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
        }
'''
    write_file(base_validator, base_validator_content)

    validation_module = modules_path / "validation_module.py"
    module_content = '''"""
Validation Module - Validation Functionality
Captain Agent-3: MODULAR-001 Implementation
"""

import logging
from typing import Dict, Any

class ValidationModule:
    """Validation module implementation"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.validation_rules = {}

    def add_validation_rule(self, rule_name: str, rule_config: Dict[str, Any]) -> bool:
        """Add validation rule"""
        try:
            self.validation_rules[rule_name] = rule_config
            return True
        except Exception as e:
            self.logger.error(f"Failed to add validation rule: {e}")
            return False

    def get_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules"""
        return self.validation_rules
'''
    write_file(validation_module, module_content)
