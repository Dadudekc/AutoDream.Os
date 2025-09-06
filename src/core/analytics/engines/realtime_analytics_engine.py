#!/usr/bin/env python3
"""
Realtime Analytics Engine - KISS Compliant
==========================================

Simple real-time analytics processing.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


class RealtimeAnalyticsEngine:
    """Simple real-time analytics processing engine."""

    def __init__(self, config=None):
        """Initialize real-time analytics engine."""
        self.config = config or {}
        self.logger = logger

        # Simple processing state
        self.queue = deque()
        self.active = False
        self.task = None
        self.stats = {"processed": 0, "errors": 0}

    async def start_processing(self) -> Dict[str, Any]:
        """Start real-time processing."""
        try:
            self.active = True
            self.task = asyncio.create_task(self._processing_loop())
            self.logger.info("Real-time analytics processing started")
            return {"status": "started", "timestamp": datetime.now().isoformat()}
        except Exception as e:
            self.logger.error(f"Failed to start processing: {e}")
            return {"status": "error", "error": str(e)}

    async def stop_processing(self) -> Dict[str, Any]:
        """Stop real-time processing."""
        try:
            self.active = False
            if self.task:
                self.task.cancel()
            self.logger.info("Real-time analytics processing stopped")
            return {"status": "stopped", "timestamp": datetime.now().isoformat()}
        except Exception as e:
            self.logger.error(f"Failed to stop processing: {e}")
            return {"status": "error", "error": str(e)}

    async def _processing_loop(self) -> None:
        """Main processing loop."""
        while self.active:
            try:
                if self.queue:
                    data = self.queue.popleft()
                    await self._process_data(data)
                else:
                    await asyncio.sleep(0.1)  # Small delay when queue is empty
            except Exception as e:
                self.stats["errors"] += 1
                self.logger.error(f"Error in processing loop: {e}")
                await asyncio.sleep(1)

    async def _process_data(self, data: Dict[str, Any]) -> None:
        """Process a single data item."""
        try:
            self.stats["processed"] += 1
            self.logger.debug(f"Processed data: {data.get('id', 'unknown')}")
        except Exception as e:
            self.stats["errors"] += 1
            self.logger.error(f"Error processing data: {e}")

    def add_data(self, data: Dict[str, Any]) -> None:
        """Add data to processing queue."""
        try:
            self.queue.append(data)
            self.logger.debug(f"Added data to queue: {data.get('id', 'unknown')}")
        except Exception as e:
            self.logger.error(f"Error adding data to queue: {e}")

    def get_queue_size(self) -> int:
        """Get current queue size."""
        return len(self.queue)

    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            "active": self.active,
            "queue_size": self.get_queue_size(),
            "processed": self.stats["processed"],
            "errors": self.stats["errors"],
            "timestamp": datetime.now().isoformat(),
        }

    def reset_stats(self) -> None:
        """Reset processing statistics."""
        self.stats = {"processed": 0, "errors": 0}
        self.logger.info("Processing statistics reset")

    def get_status(self) -> Dict[str, Any]:
        """Get engine status."""
        return {
            "active": self.active,
            "stats": self.get_stats(),
            "timestamp": datetime.now().isoformat(),
        }


# Simple factory function
def create_realtime_analytics_engine(config=None) -> RealtimeAnalyticsEngine:
    """Create real-time analytics engine."""
    return RealtimeAnalyticsEngine(config)


__all__ = ["RealtimeAnalyticsEngine", "create_realtime_analytics_engine"]
