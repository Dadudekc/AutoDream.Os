#!/usr/bin/env python3
"""
Index Processor
===============

Processes index operations and handles vector database indexing.
"""

import logging
import time

from .manager import IndexManager
from .types import IndexEntry, IndexStatus, IndexType

logger = logging.getLogger(__name__)


class IndexProcessor:
    """Processes index operations."""

    def __init__(self, index_manager: IndexManager):
        self.index_manager = index_manager
        self.processing_queue: list[str] = []
        self.is_processing = False

    def queue_operation(
        self, entry_id: str, index_type: IndexType, metadata: dict[str, any]
    ) -> IndexEntry:
        """Queue an index operation."""
        entry = self.index_manager.create_entry(entry_id, index_type, metadata)
        self.processing_queue.append(entry_id)

        if not self.is_processing:
            self._process_queue()

        return entry

    def _process_queue(self):
        """Process the operation queue."""
        if self.is_processing or not self.processing_queue:
            return

        self.is_processing = True
        logger.info(f"Starting queue processing with {len(self.processing_queue)} operations")

        while self.processing_queue:
            entry_id = self.processing_queue.pop(0)
            self._process_entry(entry_id)

        self.is_processing = False
        logger.info("Queue processing completed")

    def _process_entry(self, entry_id: str):
        """Process a single index entry."""
        entry = self.index_manager.get_entry(entry_id)
        if not entry:
            logger.error(f"Entry {entry_id} not found")
            return

        logger.info(f"Processing index entry: {entry_id}")
        start_time = time.time()

        try:
            self.index_manager.update_entry_status(entry_id, IndexStatus.INDEXING)

            # Simulate index processing
            result = self._perform_indexing(entry)

            if result["success"]:
                entry.processing_time = time.time() - start_time
                entry.vector_count = result.get("vector_count", 0)
                self.index_manager.update_entry_status(entry_id, IndexStatus.COMPLETED)
                logger.info(f"Successfully processed entry {entry_id}")
            else:
                error_msg = result.get("error", "Unknown error")
                self.index_manager.update_entry_status(entry_id, IndexStatus.FAILED, error_msg)
                logger.error(f"Failed to process entry {entry_id}: {error_msg}")

        except Exception as e:
            error_msg = str(e)
            self.index_manager.update_entry_status(entry_id, IndexStatus.FAILED, error_msg)
            logger.error(f"Exception processing entry {entry_id}: {e}")

    def _perform_indexing(self, entry: IndexEntry) -> dict[str, any]:
        """Perform the actual indexing operation."""
        # Simulate indexing work
        time.sleep(0.1)  # Simulate processing time

        # Mock successful indexing
        return {"success": True, "vector_count": 100, "processing_time": 0.1}

    def get_queue_status(self) -> dict[str, any]:
        """Get current queue status."""
        return {
            "queue_length": len(self.processing_queue),
            "is_processing": self.is_processing,
            "total_entries": len(self.index_manager.entries),
        }

    def start_processing(self) -> None:
        """Start the processing of queued operations."""
        if not self.is_processing:
            logger.info("Starting index processing")
            self._process_queue()
