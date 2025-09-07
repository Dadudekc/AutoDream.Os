"""Data validation middleware components."""

from __future__ import annotations

import time
from typing import Dict, Optional

from ..base import BaseMiddlewareComponent
from ..models import DataPacket, MiddlewareType
from .common_validation import validate_field


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
                        if not validate_field(value, rule, constraint):
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
            logger.exception("Error in %s for packet %s", self.name, data_packet.id)
            data_packet.metadata["error"] = f"{type(exc).__name__} in {self.name}"

        processing_time = time.time() - start_time
        self.update_metrics(processing_time, success)

        return data_packet
