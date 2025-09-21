#!/usr/bin/env python3
"""
Index Manager
=============

Manages index operations and provides status tracking.
"""

import json
import logging
import time
from typing import Dict, List, Optional, Tuple
from .types import IndexEntry, IndexStats, IndexStatus, IndexType

logger = logging.getLogger(__name__)


class IndexManager:
    """Manages index operations and status tracking."""
    
    def __init__(self, storage_path: str = "data/index_storage.json"):
        self.storage_path = storage_path
        self.entries: Dict[str, IndexEntry] = {}
        self.load_entries()
    
    def load_entries(self):
        """Load index entries from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for entry_id, entry_data in data.items():
                    self.entries[entry_id] = IndexEntry.from_dict(entry_data)
            logger.info(f"Loaded {len(self.entries)} index entries")
        except FileNotFoundError:
            logger.info("No existing index storage found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading index entries: {e}")
    
    def save_entries(self):
        """Save index entries to storage."""
        try:
            data = {entry_id: entry.to_dict() for entry_id, entry in self.entries.items()}
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved {len(self.entries)} index entries")
        except Exception as e:
            logger.error(f"Error saving index entries: {e}")
    
    def create_entry(
        self, 
        entry_id: str, 
        index_type: IndexType, 
        metadata: Dict[str, any]
    ) -> IndexEntry:
        """Create a new index entry."""
        entry = IndexEntry(
            id=entry_id,
            timestamp=time.time(),
            status=IndexStatus.PENDING,
            index_type=index_type,
            metadata=metadata
        )
        self.entries[entry_id] = entry
        self.save_entries()
        logger.info(f"Created index entry: {entry_id}")
        return entry
    
    def update_entry_status(
        self, 
        entry_id: str, 
        status: IndexStatus,
        error_message: Optional[str] = None
    ):
        """Update entry status."""
        if entry_id in self.entries:
            self.entries[entry_id].status = status
            if error_message:
                self.entries[entry_id].error_message = error_message
            self.save_entries()
            logger.debug(f"Updated entry {entry_id} status to {status}")
    
    def get_entry(self, entry_id: str) -> Optional[IndexEntry]:
        """Get an index entry by ID."""
        return self.entries.get(entry_id)
    
    def get_stats(self) -> IndexStats:
        """Get index statistics."""
        stats = IndexStats()
        
        for entry in self.entries.values():
            stats.total_entries += 1
            
            if entry.status == IndexStatus.COMPLETED:
                stats.completed_entries += 1
            elif entry.status == IndexStatus.FAILED:
                stats.failed_entries += 1
            elif entry.status == IndexStatus.PENDING:
                stats.pending_entries += 1
            
            if entry.processing_time > 0:
                stats.average_processing_time += entry.processing_time
        
        if stats.completed_entries > 0:
            stats.average_processing_time /= stats.completed_entries
        
        # Find last index time
        if self.entries:
            last_times = [e.timestamp for e in self.entries.values()]
            stats.last_index_time = max(last_times)
        
        return stats
    
    def cleanup_stale_entries(self, max_age_seconds: int = 86400):
        """Remove stale entries."""
        current_time = time.time()
        stale_ids = []
        
        for entry_id, entry in self.entries.items():
            if current_time - entry.timestamp > max_age_seconds:
                stale_ids.append(entry_id)
        
        for entry_id in stale_ids:
            del self.entries[entry_id]
        
        if stale_ids:
            self.save_entries()
            logger.info(f"Cleaned up {len(stale_ids)} stale entries")
