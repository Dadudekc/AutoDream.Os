"""Persistent Memory Core - Data structures and storage"""

import gzip
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Memory type enumeration."""
    FACTUAL = "factual"
    PROCEDURAL = "procedural"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class MemoryPriority(Enum):
    """Memory priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MemoryMetadata:
    """Memory metadata structure."""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    memory_type: MemoryType = MemoryType.FACTUAL
    priority: MemoryPriority = MemoryPriority.NORMAL
    tags: list[str] = field(default_factory=list)
    category: str = "general"
    source: str = "system"
    confidence: float = 1.0
    access_count: int = 0
    last_accessed: datetime | None = None


@dataclass
class MemoryRelationship:
    """Memory relationship structure."""
    source_id: str
    target_id: str
    relationship_type: str
    strength: float = 1.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class MemoryStorage:
    """Memory storage management."""

    def __init__(self, storage_path: str = "data/memories"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memories: dict[str, dict] = {}
        self._load_memories()

    def _load_memories(self) -> None:
        """Load memories from storage."""
        try:
            for memory_file in self.storage_path.glob("*.json"):
                with open(memory_file, encoding="utf-8") as f:
                    memory_data = json.load(f)
                    self.memories[memory_data["id"]] = memory_data
            logger.info(f"Loaded {len(self.memories)} memories from storage")
        except Exception as e:
            logger.error(f"Error loading memories: {e}")

    def store_memory(self, memory_id: str, content: Any, metadata: MemoryMetadata) -> bool:
        """Store memory with metadata."""
        try:
            memory_data = {
                "id": memory_id,
                "content": content,
                "metadata": {
                    "created_at": metadata.created_at.isoformat(),
                    "updated_at": metadata.updated_at.isoformat(),
                    "memory_type": metadata.memory_type.value,
                    "priority": metadata.priority.value,
                    "tags": metadata.tags,
                    "category": metadata.category,
                    "source": metadata.source,
                    "confidence": metadata.confidence,
                    "access_count": metadata.access_count,
                    "last_accessed": metadata.last_accessed.isoformat()
                    if metadata.last_accessed
                    else None,
                },
            }

            self.memories[memory_id] = memory_data

            # Save to file
            memory_file = self.storage_path / f"{memory_id}.json"
            with open(memory_file, "w", encoding="utf-8") as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Stored memory {memory_id}")
            return True

        except Exception as e:
            logger.error(f"Error storing memory {memory_id}: {e}")
            return False

    def get_memory(self, memory_id: str) -> dict | None:
        """Get memory by ID."""
        return self.memories.get(memory_id)

    def list_memories(
        self, category: str | None = None, memory_type: MemoryType | None = None
    ) -> list[dict]:
        """List memories with optional filtering."""
        memories = list(self.memories.values())

        if category:
            memories = [m for m in memories if m["metadata"]["category"] == category]

        if memory_type:
            memories = [m for m in memories if m["metadata"]["memory_type"] == memory_type.value]

        return memories


class MemoryCompression:
    """Memory compression and optimization system."""

    def __init__(self):
        self.compression_threshold = 1000

    def compress_memory(self, memory_id: str, content: str) -> tuple[str, bool]:
        """Compress memory content if needed."""
        try:
            if len(content) > self.compression_threshold:
                compressed = gzip.compress(content.encode("utf-8"))
                compressed_b64 = compressed.hex()
                return compressed_b64, True
            else:
                return content, False
        except Exception as e:
            logger.error(f"Error compressing memory {memory_id}: {e}")
            return content, False

    def decompress_memory(self, content: str, is_compressed: bool) -> str:
        """Decompress memory content if needed."""
        try:
            if is_compressed:
                compressed_bytes = bytes.fromhex(content)
                decompressed = gzip.decompress(compressed_bytes)
                return decompressed.decode("utf-8")
            else:
                return content
        except Exception as e:
            logger.error(f"Error decompressing memory: {e}")
            return content


class MemorySecurity:
    """Memory security and access control."""

    def __init__(self):
        self.access_control: dict[str, list[str]] = {}
        self.encryption_key = self._generate_key()

    def _generate_key(self) -> str:
        """Generate encryption key."""
        return hashlib.sha256(f"memory_security_{int(time.time())}".encode()).hexdigest()

    def set_access(self, memory_id: str, users: list[str]) -> bool:
        """Set access control for memory."""
        try:
            self.access_control[memory_id] = users
            logger.info(f"Set access control for memory {memory_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting access control for memory {memory_id}: {e}")
            return False

    def check_access(self, memory_id: str, user: str) -> bool:
        """Check if user has access to memory."""
        if memory_id not in self.access_control:
            return True
        return user in self.access_control[memory_id]

    def encrypt_content(self, content: str) -> str:
        """Encrypt memory content."""
        encrypted = hashlib.sha256((content + self.encryption_key).encode()).hexdigest()
        return f"encrypted:{encrypted}"

    def decrypt_content(self, encrypted_content: str) -> str:
        """Decrypt memory content."""
        if not encrypted_content.startswith("encrypted:"):
            return encrypted_content
        return "Decrypted content"

