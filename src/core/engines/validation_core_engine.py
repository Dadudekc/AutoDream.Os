from __future__ import annotations
from typing import Any, Dict, List, Optional
from .contracts import Engine, EngineContext, EngineResult

class ValidationCoreEngine(Engine):
    """Core validation engine - consolidates all validation operations."""
    
    def __init__(self):
        self.rules: Dict[str, Any] = {}
        self.validations: List[Dict[str, Any]] = []
        self.is_initialized = False
    
    def initialize(self, context: EngineContext) -> bool:
        """Initialize validation core engine."""
        try:
            self.is_initialized = True
            context.logger.info("Validation Core Engine initialized")
            return True
        except Exception as e:
            context.logger.error(f"Failed to initialize Validation Core Engine: {e}")
            return False
    
    def execute(self, context: EngineContext, payload: Dict[str, Any]) -> EngineResult:
        """Execute validation operation based on payload type."""
        try:
            operation = payload.get("operation", "unknown")
            
            if operation == "validate":
                return self._validate_data(context, payload)
            elif operation == "add_rule":
                return self._add_rule(context, payload)
            elif operation == "check_compliance":
                return self._check_compliance(context, payload)
            else:
                return EngineResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown validation operation: {operation}"
                )
        except Exception as e:
            return EngineResult(
                success=False,
                data={},
                metrics={},
                error=str(e)
            )
    
    def _validate_data(self, context: EngineContext, payload: Dict[str, Any]) -> EngineResult:
        """Validate data against rules."""
        try:
            data = payload.get("data", {})
            rules = payload.get("rules", [])
            
            validation_result = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "rules_checked": len(rules)
            }
            
            for rule in rules:
                if rule == "required" and not data:
                    validation_result["valid"] = False
                    validation_result["errors"].append("Data is required")
                elif rule == "v2_compliance" and len(str(data)) > 300:
                    validation_result["valid"] = False
                    validation_result["errors"].append("V2 compliance violation: exceeds 300 lines")
                elif rule == "format" and not isinstance(data, dict):
                    validation_result["warnings"].append("Data format warning")
            
            self.validations.append(validation_result)
            
            return EngineResult(
                success=validation_result["valid"],
                data=validation_result,
                metrics={"rules_checked": len(rules)}
            )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))
    
    def _add_rule(self, context: EngineContext, payload: Dict[str, Any]) -> EngineResult:
        """Add validation rule."""
        try:
            rule_id = payload.get("rule_id", f"rule_{len(self.rules)}")
            rule_definition = payload.get("rule", {})
            
            self.rules[rule_id] = rule_definition
            
            return EngineResult(
                success=True,
                data={"rule_id": rule_id, "status": "added"},
                metrics={"rules_count": len(self.rules)}
            )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))
    
    def _check_compliance(self, context: EngineContext, payload: Dict[str, Any]) -> EngineResult:
        """Check compliance with standards."""
        try:
            data = payload.get("data", {})
            standard = payload.get("standard", "v2")
            
            compliance_result = {
                "compliant": True,
                "standard": standard,
                "violations": [],
                "score": 100
            }
            
            if standard == "v2":
                if len(str(data)) > 300:
                    compliance_result["compliant"] = False
                    compliance_result["violations"].append("Line count exceeds 300")
                    compliance_result["score"] -= 20
                
                if "class " in str(data) and str(data).count("class ") > 5:
                    compliance_result["violations"].append("Too many classes")
                    compliance_result["score"] -= 10
            
            return EngineResult(
                success=compliance_result["compliant"],
                data=compliance_result,
                metrics={"standard": standard}
            )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))
    
    def cleanup(self, context: EngineContext) -> bool:
        """Cleanup validation core engine."""
        try:
            self.rules.clear()
            self.validations.clear()
            self.is_initialized = False
            context.logger.info("Validation Core Engine cleaned up")
            return True
        except Exception as e:
            context.logger.error(f"Failed to cleanup Validation Core Engine: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get validation core engine status."""
        return {
            "initialized": self.is_initialized,
            "rules_count": len(self.rules),
            "validations_count": len(self.validations)
        }
