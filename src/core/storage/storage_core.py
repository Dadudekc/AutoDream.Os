#!/usr/bin/env python3
"""
Storage Core - Agent Cellphone V2
=================================

Core storage operations and data management.
Follows V2 standards: ≤150 LOC, SRP, OOP principles.
"""

import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from .storage_types import StorageConfig, StorageType, DataIntegrityLevel
from .storage_metadata import MetadataManager

logger = logging.getLogger(__name__)


class PersistentDataStorage:
    """Core persistent data storage system."""
    
    def __init__(self, config: StorageConfig):
        """Initialize storage system with configuration."""
        self.config = config
        self.base_path = Path(config.base_path)
        self.data_path = self.base_path / "data"
        self.backup_path = self.base_path / "backups"
        self.metadata_path = self.base_path / "metadata"
        self.db_path = self.base_path / "storage.db"
        
        # Initialize components
        self.metadata_manager = MetadataManager(self.metadata_path / "metadata.json")
        self.data_metadata = {}
        
        # Create directories
        self._create_directories()
        self._init_database()
    
    def _create_directories(self):
        """Create necessary storage directories."""
        data_types = ["messages", "tasks", "status", "config", "logs", "missions", "tests"]
        for data_type in data_types:
            (self.data_path / data_type).mkdir(parents=True, exist_ok=True)
        
        self.backup_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """Initialize SQLite database for metadata."""
        import sqlite3
        self.db_conn = sqlite3.connect(str(self.db_path))
        self.db_cursor = self.db_conn.cursor()
        
        # Create tables
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_entries (
                data_id TEXT PRIMARY KEY,
                data_type TEXT NOT NULL,
                file_path TEXT NOT NULL,
                checksum TEXT NOT NULL,
                timestamp REAL NOT NULL,
                size INTEGER NOT NULL,
                version INTEGER NOT NULL
            )
        """)
        self.db_conn.commit()
    
    def store_data(self, data_id: str, data: Any, data_type: str) -> bool:
        """Store data with integrity checks."""
        try:
            type_dir = self.data_path / data_type
            type_dir.mkdir(parents=True, exist_ok=True)
            data_file = type_dir / f"{data_id}.json"
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
            checksum = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
            self.db_cursor.execute("""
                INSERT OR REPLACE INTO data_entries 
                (data_id, data_type, file_path, checksum, timestamp, size, version)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (data_id, data_type, str(data_file), checksum, 
                  self.metadata_manager.metadata.get(data_id, {}).get('timestamp', 0),
                  len(json.dumps(data)), 1))
            self.db_conn.commit()
            self.metadata_manager.create_metadata(data_id, data, data_type)
            logger.info(f"Stored data {data_id} of type {data_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to store data {data_id}: {e}")
            return False
    
    def retrieve_data(self, data_id: str, data_type: str) -> Optional[Any]:
        """Retrieve data with integrity verification."""
        try:
            # Get database entry
            self.db_cursor.execute("""
                SELECT file_path, checksum FROM data_entries 
                WHERE data_id = ? AND data_type = ?
            """, (data_id, data_type))
            
            result = self.db_cursor.fetchone()
            if not result:
                return None
            
            file_path, expected_checksum = result
            
            # Read data file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Verify checksum
            actual_checksum = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
            if actual_checksum != expected_checksum:
                logger.error(f"Checksum mismatch for {data_id}")
                return None
            
            logger.info(f"Retrieved data {data_id} of type {data_type}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to retrieve data {data_id}: {e}")
            return None
    
    def delete_data(self, data_id: str, data_type: str) -> bool:
        """Delete data and metadata."""
        try:
            # Get file path from database
            self.db_cursor.execute("""
                SELECT file_path FROM data_entries 
                WHERE data_id = ? AND data_type = ?
            """, (data_id, data_type))
            
            result = self.db_cursor.fetchone()
            if result:
                file_path = Path(result[0])
                if file_path.exists():
                    file_path.unlink()
            
            # Remove from database
            self.db_cursor.execute("""
                DELETE FROM data_entries 
                WHERE data_id = ? AND data_type = ?
            """, (data_id, data_type))
            
            self.db_conn.commit()
            
            # Remove metadata
            self.metadata_manager.delete_metadata(data_id)
            
            logger.info(f"Deleted data {data_id} of type {data_type}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete data {data_id}: {e}")
            return False
    
    def list_data_entries(self, data_type: Optional[str] = None) -> List[str]:
        """List all data entry IDs, optionally filtered by type."""
        try:
            if data_type:
                self.db_cursor.execute("""
                    SELECT data_id FROM data_entries WHERE data_type = ?
                """, (data_type,))
            else:
                self.db_cursor.execute("SELECT data_id FROM data_entries")
            
            results = self.db_cursor.fetchall()
            return [row[0] for row in results]
            
        except Exception as e:
            logger.error(f"Failed to list data entries: {e}")
            return []
    
    def get_data_metadata(self, data_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for specific data entry."""
        return self.metadata_manager.get_metadata(data_id)
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get comprehensive storage statistics."""
        try:
            self.db_cursor.execute("SELECT COUNT(*), SUM(size) FROM data_entries")
            result = self.db_cursor.fetchone()
            total_entries = result[0] if result[0] else 0
            total_size = result[1] if result[1] else 0
            metadata_stats = self.metadata_manager.get_metadata_stats()
            return {
                "total_data_entries": total_entries,
                "total_storage_size": total_size,
                "storage_type": self.config.storage_type.value,
                "integrity_level": DataIntegrityLevel.ADVANCED.value,
                "backup_count": metadata_stats.get("total_entries", 0),
                "compression_enabled": self.config.compression_enabled,
                "encryption_enabled": self.config.encryption_enabled
            }
        except Exception as e:
            logger.error(f"Failed to get storage stats: {e}")
            return {}
    
    def __del__(self):
        """Cleanup database connection."""
        if hasattr(self, 'db_conn'):
            self.db_conn.close()
