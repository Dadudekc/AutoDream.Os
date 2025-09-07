from __future__ import annotations
from typing import Any, Dict, List, Optional
from .contracts import UtilityEngine, EngineContext, EngineResult


class UtilityCoreEngine(UtilityEngine):
    """Core utility engine - consolidates all utility operations."""

    def __init__(self):
        self.processors: Dict[str, Any] = {}
        self.validators: Dict[str, Any] = {}
        self.transformers: Dict[str, Any] = {}
        self.is_initialized = False

    def initialize(self, context: EngineContext) -> bool:
        """Initialize utility core engine."""
        try:
            self.is_initialized = True
            context.logger.info("Utility Core Engine initialized")
            return True
        except Exception as e:
            context.logger.error(f"Failed to initialize Utility Core Engine: {e}")
            return False

    def execute(self, context: EngineContext, payload: Dict[str, Any]) -> EngineResult:
        """Execute utility operation based on payload type."""
        try:
            operation = payload.get("operation", "unknown")

            if operation == "process":
                return self.process(context, payload)
            elif operation == "validate":
                return self.validate(context, payload)
            elif operation == "transform":
                return self.transform(context, payload)
            else:
                return EngineResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown utility operation: {operation}",
                )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def process(self, context: EngineContext, data: Dict[str, Any]) -> EngineResult:
        """Process data using utility functions."""
        try:
            processor_id = data.get("processor_id", "default")
            input_data = data.get("data", {})
            process_type = data.get("type", "general")

            # Simplified processing logic
            if process_type == "format":
                processed = {"formatted": True, "data": str(input_data)}
            elif process_type == "normalize":
                processed = {"normalized": True, "data": input_data}
            elif process_type == "sanitize":
                processed = {"sanitized": True, "data": str(input_data).strip()}
            else:
                processed = {"processed": True, "data": input_data}

            self.processors[processor_id] = processed

            return EngineResult(
                success=True, data=processed, metrics={"process_type": process_type}
            )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def validate(self, context: EngineContext, data: Dict[str, Any]) -> EngineResult:
        """Validate data using utility functions."""
        try:
            validator_id = data.get("validator_id", "default")
            input_data = data.get("data", {})
            validation_rules = data.get("rules", [])

            # Simplified validation logic
            validation_result = {"valid": True, "errors": [], "warnings": []}

            for rule in validation_rules:
                if rule == "required" and not input_data:
                    validation_result["valid"] = False
                    validation_result["errors"].append("Field is required")
                elif rule == "length" and len(str(input_data)) > 100:
                    validation_result["warnings"].append("Field is too long")

            self.validators[validator_id] = validation_result

            return EngineResult(
                success=validation_result["valid"],
                data=validation_result,
                metrics={"rules_checked": len(validation_rules)},
            )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def transform(self, context: EngineContext, data: Dict[str, Any]) -> EngineResult:
        """Transform data using utility functions."""
        try:
            transformer_id = data.get("transformer_id", "default")
            input_data = data.get("data", {})
            transform_type = data.get("type", "general")

            # Simplified transformation logic
            if transform_type == "uppercase":
                transformed = {"transformed": True, "data": str(input_data).upper()}
            elif transform_type == "lowercase":
                transformed = {"transformed": True, "data": str(input_data).lower()}
            elif transform_type == "json":
                transformed = {"transformed": True, "data": str(input_data)}
            else:
                transformed = {"transformed": True, "data": input_data}

            self.transformers[transformer_id] = transformed

            return EngineResult(
                success=True,
                data=transformed,
                metrics={"transform_type": transform_type},
            )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: EngineContext) -> bool:
        """Cleanup utility core engine."""
        try:
            self.processors.clear()
            self.validators.clear()
            self.transformers.clear()
            self.is_initialized = False
            context.logger.info("Utility Core Engine cleaned up")
            return True
        except Exception as e:
            context.logger.error(f"Failed to cleanup Utility Core Engine: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get utility core engine status."""
        return {
            "initialized": self.is_initialized,
            "processors_count": len(self.processors),
            "validators_count": len(self.validators),
            "transformers_count": len(self.transformers),
        }
