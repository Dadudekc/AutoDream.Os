#!/usr/bin/env python3
"""
Persistent Memory - Main interface
==================================

V2 Compliance: Refactored for <400 lines
Author: Agent-5 (Coordinator) - Refactored from Agent-1
License: MIT
"""

import logging
from datetime import UTC, datetime

from .persistent_memory_core import (
    MemoryCompression,
    MemoryMetadata,
    MemoryPriority,
    MemoryRelationship,
    MemorySecurity,
    MemoryStorage,
    MemoryType,
)
from .persistent_memory_advanced import MemoryOrganization, MemoryRetrieval

logger = logging.getLogger(__name__)


class PersistentMemory:
    """Main PersistentMemory class."""

    def __init__(self, storage_path: str = "data/memories"):
        self.storage = MemoryStorage(storage_path)
        self.retrieval = MemoryRetrieval()
        self.organization = MemoryOrganization()
        self.compression = MemoryCompression()
        self.security = MemorySecurity()
        self.retrieval.memories = self.storage.memories
        logger.info("PersistentMemory initialized")

    def store_memory(self, memory_id: str, content: str, metadata: MemoryMetadata) -> bool:
        """Store memory with metadata and organization."""
        try:
            if not self.security.check_access(memory_id, metadata.source):
                logger.warning(f"Access denied for memory {memory_id}")
                return False

            content_str = str(content)
            compressed_content, is_compressed = self.compression.compress_memory(memory_id, content_str)

            if metadata.priority == MemoryPriority.CRITICAL:
                compressed_content = self.security.encrypt_content(compressed_content)

            success = self.storage.store_memory(memory_id, compressed_content, metadata)

            if success:
                self.organization.organize_memory(memory_id, metadata.tags, metadata.category)
                metadata.access_count += 1
                metadata.last_accessed = datetime.now(UTC)

            return success

        except Exception as e:
            logger.error(f"Error storing memory {memory_id}: {e}")
            return False

    def retrieve_memory(self, memory_id: str, user: str = "system") -> dict | None:
        """Retrieve memory by ID with access control."""
        try:
            if not self.security.check_access(memory_id, user):
                logger.warning(f"Access denied for memory {memory_id}")
                return None

            memory = self.storage.get_memory(memory_id)
            if memory:
                metadata = memory.get("metadata", {})
                metadata["access_count"] = metadata.get("access_count", 0) + 1
                metadata["last_accessed"] = datetime.now(UTC).isoformat()

                content = memory.get("content", "")
                is_compressed = len(content) > 1000
                if is_compressed:
                    content = self.compression.decompress_memory(content, True)
                    memory["content"] = content

            return memory

        except Exception as e:
            logger.error(f"Error retrieving memory {memory_id}: {e}")
            return None

    def search_memories(self, query: str, context: dict = None) -> list[dict]:
        """Search memories based on query and context."""
        if context is None:
            context = {}
        return self.retrieval.search_memories(query, context)

    def get_memories_by_category(self, category: str) -> list[dict]:
        """Get memories by category."""
        memory_ids = self.organization.get_memories_by_category(category)
        return [self.storage.get_memory(mid) for mid in memory_ids if self.storage.get_memory(mid)]

    def list_memories(
        self, category: str | None = None, memory_type: MemoryType | None = None
    ) -> list[dict]:
        """List memories with optional filtering."""
        return self.storage.list_memories(category, memory_type)


def main():
    """Main function for testing."""
    memory = PersistentMemory()

    metadata = MemoryMetadata(
        memory_type=MemoryType.FACTUAL,
        priority=MemoryPriority.HIGH,
        category="test",
        tags=["test", "example"],
        source="test_user",
        confidence=0.9,
    )

    success = memory.store_memory("test_memory_1", "This is a test memory", metadata)
    print(f"Memory storage: {'Success' if success else 'Failed'}")

    retrieved = memory.retrieve_memory("test_memory_1")
    print(f"Memory retrieval: {'Success' if retrieved else 'Failed'}")

    results = memory.search_memories("test")
    print(f"Memory search: {len(results)} results found")

    category_memories = memory.get_memories_by_category("test")
    print(f"Category memories: {len(category_memories)} found")


if __name__ == "__main__":
    main()
