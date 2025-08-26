"""Data validation middleware components."""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from ..base import BaseMiddlewareComponent
from ..models import DataPacket, MiddlewareType


class ValidationMiddleware(BaseMiddlewareComponent):
    """Middleware for data validation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.middleware_type = MiddlewareType.VALIDATION
        self.validation_rules = self.config.get("validation_rules", {})
        self.strict_mode = self.config.get("strict_mode", False)

    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        start_time = time.time()
        success = True

        try:
            validation_errors = []

            # Apply validation rules
            for field, rules in self.validation_rules.items():
                if field in data_packet.metadata:
                    value = data_packet.metadata[field]
                    for rule, constraint in rules.items():
                        if not self._validate_field(value, rule, constraint):
                            validation_errors.append(
                                f"Validation failed for {field}: {rule} {constraint}"
                            )

            # Handle validation results
            if validation_errors:
                data_packet.metadata["validation_errors"] = validation_errors
                data_packet.metadata["valid"] = False

                if self.strict_mode:
                    raise ValueError(f"Validation failed: {validation_errors}")
            else:
                data_packet.metadata["valid"] = True
                data_packet.tags.add("validated")

            data_packet.processing_history.append(f"{self.name}:validation")

        except Exception as exc:  # noqa: BLE001
            success = False
            data_packet.metadata["error"] = str(exc)

        processing_time = time.time() - start_time
        self.update_metrics(processing_time, success)

        return data_packet

    def _validate_field(self, value: Any, rule: str, constraint: Any) -> bool:
        """Validate a field according to the specified rule."""
        if rule == "required":
            return value is not None and value != ""
        if rule == "min_length" and isinstance(value, str):
            return len(value) >= constraint
        if rule == "max_length" and isinstance(value, str):
            return len(value) <= constraint
        if rule == "min_value" and isinstance(value, (int, float)):
            return value >= constraint
        if rule == "max_value" and isinstance(value, (int, float)):
            return value <= constraint
        if rule == "type" and constraint == "string":
            return isinstance(value, str)
        if rule == "type" and constraint == "number":
            return isinstance(value, (int, float))
        return True
