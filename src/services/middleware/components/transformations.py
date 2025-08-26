"""Data transformation middleware components."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional

from ..base import BaseMiddlewareComponent
from ..models import DataPacket, MiddlewareType


class DataTransformationMiddleware(BaseMiddlewareComponent):
    """Middleware for transforming data formats."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.middleware_type = MiddlewareType.TRANSFORMATION
        self.transformations = self.config.get("transformations", {})

    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        start_time = time.time()
        success = True

        try:
            # Apply transformations based on packet tags or metadata
            for condition, transformation in self.transformations.items():
                if self._matches_condition(data_packet, condition):
                    data_packet.data = await self._apply_transformation(
                        data_packet.data, transformation
                    )
                    data_packet.processing_history.append(
                        f"{self.name}:{transformation}"
                    )

            # Update packet metadata
            data_packet.metadata["transformed"] = True
            data_packet.metadata["transformation_count"] = len(
                data_packet.processing_history
            )

        except Exception as exc:  # noqa: BLE001
            success = False
            logger.exception("Error in %s for packet %s", self.name, data_packet.id)
            data_packet.metadata["error"] = f"{type(exc).__name__} in {self.name}"

        processing_time = time.time() - start_time
        self.update_metrics(processing_time, success)

        return data_packet

    def _matches_condition(self, data_packet: DataPacket, condition: str) -> bool:
        """Check if packet matches transformation condition."""
        if condition in data_packet.tags:
            return True
        if condition in data_packet.metadata:
            return bool(data_packet.metadata[condition])
        return False

    async def _apply_transformation(self, data: Any, transformation: str) -> Any:
        """Apply the specified transformation to data."""
        if transformation == "json_to_dict" and isinstance(data, str):
            return json.loads(data)
        if transformation == "dict_to_json" and isinstance(data, dict):
            return json.dumps(data)
        if transformation == "string_uppercase" and isinstance(data, str):
            return data.upper()
        if transformation == "string_lowercase" and isinstance(data, str):
            return data.lower()
        return data
