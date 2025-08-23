#!/usr/bin/env python3
"""
Storage Integration - Agent Cellphone V2
========================================

Unified storage interface integrating all storage components.
Follows Single Responsibility Principle with 100 LOC limit.
"""

import logging
from typing import Dict, List, Optional, Any

from .storage_types import StorageType, DataIntegrityLevel, StorageConfig
from .storage_core import PersistentDataStorage


class UnifiedStorageSystem:
    """
    Unified interface for all storage operations

    Responsibilities:
    - Provide unified access to storage functionality
    - Coordinate between storage components
    - Maintain backward compatibility
    """

    def __init__(
        self,
        base_path: str = "persistent_data",
        storage_type: StorageType = StorageType.HYBRID,
        integrity_level: DataIntegrityLevel = DataIntegrityLevel.ADVANCED,
    ):
        self.logger = logging.getLogger(f"{__name__}.UnifiedStorageSystem")

        # Create storage configuration
        config = StorageConfig(
            storage_type=storage_type,
            base_path=base_path,
            max_file_size=100 * 1024 * 1024,  # 100MB
            compression_enabled=True,
            encryption_enabled=False,
            backup_retention_days=30,
        )

        # Initialize storage components
        self.storage = PersistentDataStorage(config)

        self.logger.info("Unified storage system initialized successfully")

    def store_data(self, data_id: str, data: Any, data_type: str = "general") -> bool:
        """Store data using the unified interface"""
        return self.storage.store_data(data_id, data, data_type)

    def retrieve_data(self, data_id: str, data_type: str = "general") -> Optional[Any]:
        """Retrieve data using the unified interface"""
        return self.storage.retrieve_data(data_id, data_type)

    def get_storage_stats(self) -> Dict[str, Any]:
        """Get comprehensive storage statistics"""
        stats = self.storage.get_storage_stats()
        return stats

    def get_data_metadata(self, data_id: str) -> Optional[Any]:
        """Get metadata for a specific data entry"""
        return self.storage.data_metadata.get(data_id)

    def list_data_entries(self, data_type: str = None) -> List[str]:
        """List all data entries, optionally filtered by type"""
        if data_type:
            return [
                k
                for k, v in self.storage.data_metadata.items()
                if v.get("data_type") == data_type
            ]
        return list(self.storage.data_metadata.keys())

    def delete_data(self, data_id: str) -> bool:
        """Delete a data entry"""
        try:
            if data_id in self.storage.data_metadata:
                # Remove from metadata
                del self.storage.data_metadata[data_id]

                # Remove data file
                for data_type in [
                    "messages",
                    "tasks",
                    "status",
                    "config",
                    "logs",
                    "missions",
                    "tests",
                ]:
                    data_file = self.storage.data_path / data_type / f"{data_id}.json"
                    if data_file.exists():
                        data_file.unlink()
                        break

                # Update database
                self.storage.db_cursor.execute(
                    "DELETE FROM storage_metadata WHERE data_id = ?", (data_id,)
                )
                self.storage.db_conn.commit()

                self.logger.info(f"Data deleted successfully: {data_id}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to delete data {data_id}: {e}")

        return False
