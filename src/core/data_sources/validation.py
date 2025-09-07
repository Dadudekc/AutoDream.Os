#!/usr/bin/env python3
"""
Data Validation - Rules and validation logic
===========================================

Provides data validation functionality for the unified data source system.
"""

import re
from typing import Any, Dict, List, Optional, Union
from .types import DataValidationLevel
from .models import DataValidationRule


class DataValidator:
    """Validates data according to defined rules"""
    
    def __init__(self):
        self.rules: Dict[str, DataValidationRule] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default validation rules"""
        default_rules = [
            DataValidationRule(
                id="required_fields",
                name="Required Fields Check",
                rule_type="required_fields",
                parameters={"fields": ["id", "name", "type"]},
                description="Ensures required fields are present"
            ),
            DataValidationRule(
                id="data_type_validation",
                name="Data Type Validation",
                rule_type="data_type",
                parameters={"allowed_types": ["string", "number", "boolean", "object"]},
                description="Validates data types"
            ),
            DataValidationRule(
                id="format_validation",
                name="Format Validation",
                rule_type="format",
                parameters={"patterns": {"email": r"^[^@]+@[^@]+\.[^@]+$"}},
                description="Validates data formats"
            )
        ]
        
        for rule in default_rules:
            self.add_rule(rule)
    
    def add_rule(self, rule: DataValidationRule) -> bool:
        """Add a validation rule"""
        try:
            self.rules[rule.id] = rule
            return True
        except Exception:
            return False
    
    def validate_data(self, data: Dict[str, Any], 
                     rule_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Validate data against rules"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "rule_results": {}
        }
        
        rules_to_check = rule_ids or list(self.rules.keys())
        
        for rule_id in rules_to_check:
            if rule_id in self.rules:
                rule = self.rules[rule_id]
                if rule.enabled:
                    rule_result = self._apply_rule(rule, data)
                    results["rule_results"][rule_id] = rule_result
                    
                    if not rule_result["valid"]:
                        results["valid"] = False
                        results["errors"].extend(rule_result["errors"])
                    
                    if rule_result["warnings"]:
                        results["warnings"].extend(rule_result["warnings"])
        
        return results
    
    def _apply_rule(self, rule: DataValidationRule, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a specific validation rule"""
        try:
            if rule.rule_type == "required_fields":
                return self._validate_required_fields(rule.parameters, data)
            elif rule.rule_type == "data_type":
                return self._validate_data_types(rule.parameters, data)
            elif rule.rule_type == "format":
                return self._validate_formats(rule.parameters, data)
            else:
                return {
                    "valid": False,
                    "errors": [f"Unknown rule type: {rule.rule_type}"],
                    "warnings": []
                }
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Rule execution error: {str(e)}"],
                "warnings": []
            }
    
    def _validate_required_fields(self, params: Dict[str, Any], 
                                data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate required fields are present"""
        required_fields = params.get("fields", [])
        missing_fields = [field for field in required_fields if field not in data]
        
        return {
            "valid": len(missing_fields) == 0,
            "errors": [f"Missing required field: {field}" for field in missing_fields],
            "warnings": []
        }
    
    def _validate_data_types(self, params: Dict[str, Any], 
                           data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data types"""
        allowed_types = params.get("allowed_types", [])
        errors = []
        
        for key, value in data.items():
            if isinstance(value, str) and "string" not in allowed_types:
                errors.append(f"Field '{key}' has string type, not allowed")
            elif isinstance(value, (int, float)) and "number" not in allowed_types:
                errors.append(f"Field '{key}' has number type, not allowed")
            elif isinstance(value, bool) and "boolean" not in allowed_types:
                errors.append(f"Field '{key}' has boolean type, not allowed")
            elif isinstance(value, dict) and "object" not in allowed_types:
                errors.append(f"Field '{key}' has object type, not allowed")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": []
        }
    
    def _validate_formats(self, params: Dict[str, Any], 
                         data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data formats using regex patterns"""
        patterns = params.get("patterns", {})
        errors = []
        
        for field, pattern in patterns.items():
            if field in data:
                if not re.match(pattern, str(data[field])):
                    errors.append(f"Field '{field}' does not match expected format")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": []
        }
