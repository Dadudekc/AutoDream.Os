#!/usr/bin/env python3
"""
Status Indexer V2
=================

V2 compliant status indexing system for vector database.
"""

import logging

from .indexing import IndexManager, IndexProcessor, IndexType

logger = logging.getLogger(__name__)


class StatusIndexer:
    """V2 compliant status indexer with modular architecture."""

    def __init__(self, orchestrator=None, storage_path: str = "data/index_storage.json"):
        self.orchestrator = orchestrator
        self.index_manager = IndexManager(storage_path)
        self.index_processor = IndexProcessor(self.index_manager)
        logger.info("StatusIndexer V2 initialized")

    def create_index(self, entry_id: str, index_type: IndexType, metadata: dict[str, any]):
        """Create a new index operation."""
        return self.index_processor.queue_operation(entry_id, index_type, metadata)

    def get_status(self, entry_id: str) -> dict[str, any] | None:
        """Get status of an index entry."""
        entry = self.index_manager.get_entry(entry_id)
        if entry:
            return entry.to_dict()
        return None

    def get_statistics(self) -> dict[str, any]:
        """Get index statistics."""
        stats = self.index_manager.get_stats()
        queue_status = self.index_processor.get_queue_status()

        return {
            "stats": stats.to_dict(),
            "queue": queue_status,
            "success_rate": stats.success_rate(),
        }

    def cleanup_stale_entries(self, max_age_seconds: int = 86400):
        """Clean up stale index entries."""
        self.index_manager.cleanup_stale_entries(max_age_seconds)

    def get_queue_status(self) -> dict[str, any]:
        """Get current processing queue status."""
        return self.index_processor.get_queue_status()

    def start_indexing(self) -> None:
        """Start the indexing process."""
        logger.info("Starting automatic indexing process")
        # Start the index processor
        self.index_processor.start_processing()
