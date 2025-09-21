#!/usr/bin/env python3
"""
Index Types and Data Structures
===============================

Data types and structures for vector database indexing.
"""

import json
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum


class IndexStatus(Enum):
    """Status of an index entry."""
    PENDING = "pending"
    INDEXING = "indexing"
    COMPLETED = "completed"
    FAILED = "failed"
    STALE = "stale"


class IndexType(Enum):
    """Type of index operation."""
    FULL = "full"
    INCREMENTAL = "incremental"
    REBUILD = "rebuild"
    OPTIMIZATION = "optimization"


@dataclass
class IndexEntry:
    """Represents an index entry."""
    id: str
    timestamp: float
    status: IndexStatus
    index_type: IndexType
    metadata: Dict[str, Any]
    vector_count: int = 0
    processing_time: float = 0.0
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IndexEntry':
        """Create from dictionary."""
        data['status'] = IndexStatus(data['status'])
        data['index_type'] = IndexType(data['index_type'])
        return cls(**data)
    
    def is_stale(self, max_age_seconds: int = 3600) -> bool:
        """Check if entry is stale."""
        age = time.time() - self.timestamp
        return age > max_age_seconds


@dataclass
class IndexStats:
    """Statistics for index operations."""
    total_entries: int = 0
    completed_entries: int = 0
    failed_entries: int = 0
    pending_entries: int = 0
    average_processing_time: float = 0.0
    last_index_time: Optional[float] = None
    
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_entries == 0:
            return 0.0
        return self.completed_entries / self.total_entries
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
