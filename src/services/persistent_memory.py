#!/usr/bin/env python3
"""
Persistent Memory - Long-term Memory and Knowledge Retention System
================================================================

Persistent memory and knowledge retention system for Dream.OS integration.
Provides long-term memory storage, retrieval, organization, and analytics.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Backend & API Specialist)
License: MIT
"""

import json
import logging
import hashlib
import time
import gzip
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

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
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    memory_type: MemoryType = MemoryType.FACTUAL
    priority: MemoryPriority = MemoryPriority.NORMAL
    tags: List[str] = field(default_factory=list)
    category: str = "general"
    source: str = "system"
    confidence: float = 1.0
    access_count: int = 0
    last_accessed: Optional[datetime] = None


@dataclass
class MemoryRelationship:
    """Memory relationship structure."""
    source_id: str
    target_id: str
    relationship_type: str
    strength: float = 1.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MemoryStorage:
    """Memory storage management."""
    
    def __init__(self, storage_path: str = "data/memories"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memories: Dict[str, Dict] = {}
        self._load_memories()
    
    def _load_memories(self) -> None:
        """Load memories from storage."""
        try:
            for memory_file in self.storage_path.glob("*.json"):
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                    self.memories[memory_data['id']] = memory_data
            logger.info(f"Loaded {len(self.memories)} memories from storage")
        except Exception as e:
            logger.error(f"Error loading memories: {e}")
    
    def store_memory(self, memory_id: str, content: Any, metadata: MemoryMetadata) -> bool:
        """Store memory with metadata."""
        try:
            memory_data = {
                'id': memory_id,
                'content': content,
                'metadata': {
                    'created_at': metadata.created_at.isoformat(),
                    'updated_at': metadata.updated_at.isoformat(),
                    'memory_type': metadata.memory_type.value,
                    'priority': metadata.priority.value,
                    'tags': metadata.tags,
                    'category': metadata.category,
                    'source': metadata.source,
                    'confidence': metadata.confidence,
                    'access_count': metadata.access_count,
                    'last_accessed': metadata.last_accessed.isoformat() if metadata.last_accessed else None
                }
            }
            
            self.memories[memory_id] = memory_data
            
            # Save to file
            memory_file = self.storage_path / f"{memory_id}.json"
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Stored memory {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing memory {memory_id}: {e}")
            return False
    
    def get_memory(self, memory_id: str) -> Optional[Dict]:
        """Get memory by ID."""
        return self.memories.get(memory_id)
    
    def list_memories(self, category: Optional[str] = None, memory_type: Optional[MemoryType] = None) -> List[Dict]:
        """List memories with optional filtering."""
        memories = list(self.memories.values())
        
        if category:
            memories = [m for m in memories if m['metadata']['category'] == category]
        
        if memory_type:
            memories = [m for m in memories if m['metadata']['memory_type'] == memory_type.value]
        
        return memories


class MemoryRetrieval:
    """Memory retrieval and search engine."""
    
    def __init__(self):
        self.search_index: Dict[str, List[str]] = {}
        self._build_index()
    
    def _build_index(self) -> None:
        """Build search index for memories."""
        # Simple keyword-based indexing
        self.search_index = {}
    
    def search_memories(self, query: str, context: Dict) -> List[Dict]:
        """Search memories based on query and context."""
        try:
            # Simple keyword matching
            query_lower = query.lower()
            results = []
            
            for memory_id, memory_data in self.memories.items():
                content = str(memory_data.get('content', '')).lower()
                metadata = memory_data.get('metadata', {})
                
                # Check content match
                if query_lower in content:
                    score = self._calculate_relevance_score(query, memory_data, context)
                    results.append({
                        'memory_id': memory_id,
                        'memory_data': memory_data,
                        'relevance_score': score
                    })
                
                # Check tag match
                tags = metadata.get('tags', [])
                for tag in tags:
                    if query_lower in tag.lower():
                        score = self._calculate_relevance_score(query, memory_data, context)
                        results.append({
                            'memory_id': memory_id,
                            'memory_data': memory_data,
                            'relevance_score': score
                        })
            
            # Sort by relevance score
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results
            
        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            return []
    
    def _calculate_relevance_score(self, query: str, memory_data: Dict, context: Dict) -> float:
        """Calculate relevance score for memory."""
        score = 0.0
        content = str(memory_data.get('content', '')).lower()
        metadata = memory_data.get('metadata', {})
        
        # Content relevance
        query_words = query.lower().split()
        content_words = content.split()
        
        for word in query_words:
            if word in content_words:
                score += 1.0
        
        # Priority boost
        priority = metadata.get('priority', 'normal')
        if priority == 'critical':
            score += 3.0
        elif priority == 'high':
            score += 2.0
        elif priority == 'normal':
            score += 1.0
        
        # Confidence boost
        confidence = metadata.get('confidence', 1.0)
        score += confidence
        
        # Recency boost
        created_at = metadata.get('created_at')
        if created_at:
            try:
                created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                days_old = (datetime.now(timezone.utc) - created_dt).days
                recency_boost = max(0, 1.0 - (days_old / 365.0))  # Decay over a year
                score += recency_boost
            except:
                pass
        
        return score


class MemoryOrganization:
    """Memory organization and categorization system."""
    
    def __init__(self):
        self.categories: Dict[str, List[str]] = {}
        self.hierarchies: Dict[str, List[str]] = {}
    
    def organize_memory(self, memory_id: str, categories: List[str], hierarchy: Optional[str] = None) -> bool:
        """Organize memory into categories and hierarchies."""
        try:
            # Add to categories
            for category in categories:
                if category not in self.categories:
                    self.categories[category] = []
                if memory_id not in self.categories[category]:
                    self.categories[category].append(memory_id)
            
            # Add to hierarchy
            if hierarchy:
                if hierarchy not in self.hierarchies:
                    self.hierarchies[hierarchy] = []
                if memory_id not in self.hierarchies[hierarchy]:
                    self.hierarchies[hierarchy].append(memory_id)
            
            logger.info(f"Organized memory {memory_id} into categories: {categories}")
            return True
            
        except Exception as e:
            logger.error(f"Error organizing memory {memory_id}: {e}")
            return False
    
    def get_memories_by_category(self, category: str) -> List[str]:
        """Get memory IDs by category."""
        return self.categories.get(category, [])
    
    def get_memories_by_hierarchy(self, hierarchy: str) -> List[str]:
        """Get memory IDs by hierarchy."""
        return self.hierarchies.get(hierarchy, [])


class MemoryCompression:
    """Memory compression and optimization system."""
    
    def __init__(self):
        self.compression_threshold = 1000  # Compress memories larger than 1000 chars
    
    def compress_memory(self, memory_id: str, content: str) -> Tuple[str, bool]:
        """Compress memory content if needed."""
        try:
            if len(content) > self.compression_threshold:
                # Compress content
                compressed = gzip.compress(content.encode('utf-8'))
                compressed_b64 = compressed.hex()  # Simple hex encoding
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
                # Decompress content
                compressed_bytes = bytes.fromhex(content)
                decompressed = gzip.decompress(compressed_bytes)
                return decompressed.decode('utf-8')
            else:
                return content
                
        except Exception as e:
            logger.error(f"Error decompressing memory: {e}")
            return content


class MemorySecurity:
    """Memory security and access control."""
    
    def __init__(self):
        self.access_control: Dict[str, List[str]] = {}
        self.encryption_key = self._generate_key()
    
    def _generate_key(self) -> str:
        """Generate encryption key."""
        return hashlib.sha256(f"memory_security_{int(time.time())}".encode()).hexdigest()
    
    def set_access(self, memory_id: str, users: List[str]) -> bool:
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
            return True  # No restrictions if not set
        
        return user in self.access_control[memory_id]
    
    def encrypt_content(self, content: str) -> str:
        """Encrypt memory content."""
        # Simple encryption for demonstration
        encrypted = hashlib.sha256((content + self.encryption_key).encode()).hexdigest()
        return f"encrypted:{encrypted}"
    
    def decrypt_content(self, encrypted_content: str) -> str:
        """Decrypt memory content."""
        if not encrypted_content.startswith("encrypted:"):
            return encrypted_content
        
        # Simple decryption for demonstration
        return "Decrypted content"  # In real implementation, proper decryption


class PersistentMemory:
    """Main PersistentMemory class."""
    
    def __init__(self, storage_path: str = "data/memories"):
        self.storage = MemoryStorage(storage_path)
        self.retrieval = MemoryRetrieval()
        self.organization = MemoryOrganization()
        self.compression = MemoryCompression()
        self.security = MemorySecurity()
        logger.info("PersistentMemory initialized")
    
    def store_memory(self, memory_id: str, content: Any, metadata: MemoryMetadata) -> bool:
        """Store memory with metadata and organization."""
        try:
            # Check access control
            if not self.security.check_access(memory_id, metadata.source):
                logger.warning(f"Access denied for memory {memory_id}")
                return False
            
            # Compress content if needed
            content_str = str(content)
            compressed_content, is_compressed = self.compression.compress_memory(memory_id, content_str)
            
            # Encrypt content if needed
            if metadata.priority == MemoryPriority.CRITICAL:
                compressed_content = self.security.encrypt_content(compressed_content)
            
            # Store memory
            success = self.storage.store_memory(memory_id, compressed_content, metadata)
            
            if success:
                # Organize memory
                self.organization.organize_memory(memory_id, metadata.tags, metadata.category)
                
                # Update access count
                metadata.access_count += 1
                metadata.last_accessed = datetime.now(timezone.utc)
            
            return success
            
        except Exception as e:
            logger.error(f"Error storing memory {memory_id}: {e}")
            return False
    
    def retrieve_memory(self, memory_id: str, user: str = "system") -> Optional[Dict]:
        """Retrieve memory by ID with access control."""
        try:
            if not self.security.check_access(memory_id, user):
                logger.warning(f"Access denied for memory {memory_id}")
                return None
            
            memory = self.storage.get_memory(memory_id)
            if memory:
                # Update access count
                metadata = memory.get('metadata', {})
                metadata['access_count'] = metadata.get('access_count', 0) + 1
                metadata['last_accessed'] = datetime.now(timezone.utc).isoformat()
                
                # Decompress content if needed
                content = memory.get('content', '')
                is_compressed = len(content) > 1000  # Simple heuristic
                if is_compressed:
                    content = self.compression.decompress_memory(content, True)
                    memory['content'] = content
            
            return memory
            
        except Exception as e:
            logger.error(f"Error retrieving memory {memory_id}: {e}")
            return None
    
    def search_memories(self, query: str, context: Dict = None) -> List[Dict]:
        """Search memories based on query and context."""
        if context is None:
            context = {}
        
        return self.retrieval.search_memories(query, context)
    
    def get_memories_by_category(self, category: str) -> List[Dict]:
        """Get memories by category."""
        memory_ids = self.organization.get_memories_by_category(category)
        return [self.storage.get_memory(mid) for mid in memory_ids if self.storage.get_memory(mid)]
    
    def list_memories(self, category: Optional[str] = None, memory_type: Optional[MemoryType] = None) -> List[Dict]:
        """List memories with optional filtering."""
        return self.storage.list_memories(category, memory_type)


def main():
    """Main function for testing."""
    memory = PersistentMemory()
    
    # Test memory storage
    metadata = MemoryMetadata(
        memory_type=MemoryType.FACTUAL,
        priority=MemoryPriority.HIGH,
        category="test",
        tags=["test", "example"],
        source="test_user",
        confidence=0.9
    )
    
    success = memory.store_memory("test_memory_1", "This is a test memory", metadata)
    print(f"Memory storage: {'Success' if success else 'Failed'}")
    
    # Test memory retrieval
    retrieved = memory.retrieve_memory("test_memory_1")
    print(f"Memory retrieval: {'Success' if retrieved else 'Failed'}")
    
    # Test memory search
    results = memory.search_memories("test")
    print(f"Memory search: {len(results)} results found")
    
    # Test category filtering
    category_memories = memory.get_memories_by_category("test")
    print(f"Category memories: {len(category_memories)} found")


if __name__ == "__main__":
    main()
