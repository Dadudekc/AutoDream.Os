#!/usr/bin/env python3
"""
Processing Coordinator - KISS Compliant
======================================

Simple processing coordination.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ProcessingCoordinator:
    """Simple processing coordinator."""

    def __init__(self, config=None, processors=None):
        """Initialize processing coordinator."""
        self.config = config or {}
        self.processors = processors or {}
        self.logger = logger

        # Simple processing state
        self.stats = {"total_processed": 0, "successful": 0, "failed": 0}

    def register_processor(self, name: str, processor: Any) -> None:
        """Register a processor."""
        self.processors[name] = processor
        self.logger.info(f"Registered processor: {name}")

    async def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data through registered processors."""
        try:
            self.stats["total_processed"] += 1
            result = {"processed": True, "timestamp": datetime.now().isoformat()}

            # Process with registered processors
            for name, processor in self.processors.items():
                if hasattr(processor, "process"):
                    processor_result = await processor.process(data)
                    result[f"{name}_result"] = processor_result

            self.stats["successful"] += 1
            return result
        except Exception as e:
            self.stats["failed"] += 1
            self.logger.error(f"Failed to process data: {e}")
            return {"processed": False, "error": str(e)}

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        total = self.stats["total_processed"]
        success_rate = (self.stats["successful"] / total * 100) if total > 0 else 0

        return {
            "total_processed": total,
            "successful": self.stats["successful"],
            "failed": self.stats["failed"],
            "success_rate": success_rate,
            "timestamp": datetime.now().isoformat(),
        }

    def reset_stats(self) -> None:
        """Reset processing statistics."""
        self.stats = {"total_processed": 0, "successful": 0, "failed": 0}
        self.logger.info("Processing statistics reset")


__all__ = ["ProcessingCoordinator"]
