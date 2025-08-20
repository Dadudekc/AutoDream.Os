#!/usr/bin/env python3
"""
Storage Metadata - Agent Cellphone V2
=====================================

Handles storage metadata management and operations.
Follows V2 standards: ≤50 LOC, SRP, OOP principles.
"""

import hashlib
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

from .storage_types import StorageMetadata, CompressionType, DataIntegrityLevel


class MetadataManager:
    """Manages storage metadata operations and integrity."""
    
    def __init__(self, metadata_path: Path):
        """Initialize metadata manager."""
        self.metadata_path = metadata_path
        self.metadata: Dict[str, StorageMetadata] = {}
        self._load_metadata()
    
    def _load_metadata(self):
        """Load existing metadata from disk."""
        if self.metadata_path.exists():
            try:
                with open(self.metadata_path, 'r') as f:
                    data = json.load(f)
                    for data_id, meta_data in data.items():
                        self.metadata[data_id] = StorageMetadata(**meta_data)
            except Exception:
                self.metadata = {}
    
    def _save_metadata(self):
        """Save metadata to disk."""
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_path, 'w') as f:
            json.dump({k: v.__dict__ for k, v in self.metadata.items()}, f, indent=2)
    
    def create_metadata(self, data_id: str, data: Any, data_type: str) -> StorageMetadata:
        """Create new metadata entry for data."""
        checksum = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        metadata = StorageMetadata(
            data_id=data_id,
            timestamp=time.time(),
            checksum=checksum,
            size=len(json.dumps(data)),
            version=1,
            integrity_level=DataIntegrityLevel.ADVANCED,
            backup_count=0,
            last_backup=None,
            compression_type=CompressionType.NONE,
            encryption_enabled=False
        )
        self.metadata[data_id] = metadata
        self._save_metadata()
        return metadata
    
    def get_metadata(self, data_id: str) -> Optional[StorageMetadata]:
        """Retrieve metadata for data ID."""
        return self.metadata.get(data_id)
    
    def update_metadata(self, data_id: str, **kwargs) -> bool:
        """Update metadata fields."""
        if data_id not in self.metadata:
            return False
        
        metadata = self.metadata[data_id]
        for key, value in kwargs.items():
            if hasattr(metadata, key):
                setattr(metadata, key, value)
        
        self._save_metadata()
        return True
    
    def delete_metadata(self, data_id: str) -> bool:
        """Delete metadata entry."""
        if data_id in self.metadata:
            del self.metadata[data_id]
            self._save_metadata()
            return True
        return False
    
    def list_metadata(self, data_type: Optional[str] = None) -> Dict[str, StorageMetadata]:
        """List all metadata entries, optionally filtered by type."""
        if data_type is None:
            return self.metadata.copy()
        return {k: v for k, v in self.metadata.items()}
    
    def get_metadata_stats(self) -> Dict[str, Any]:
        """Get metadata statistics."""
        if not self.metadata:
            return {"total_entries": 0, "total_size": 0, "avg_size": 0}
        total_size = sum(meta.size for meta in self.metadata.values())
        return {
            "total_entries": len(self.metadata),
            "total_size": total_size,
            "avg_size": total_size / len(self.metadata) if self.metadata else 0
        }
