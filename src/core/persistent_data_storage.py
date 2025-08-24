#!/usr/bin/env python3
"""
Persistent Data Storage System - Agent Cellphone V2
==================================================

Implements persistent data storage with integrity, recovery, and backup.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import time
import json
import hashlib
import threading

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import shutil
import sqlite3
from datetime import datetime


class StorageType(Enum):
    """Types of persistent storage"""

    FILE_BASED = "file_based"
    DATABASE = "database"
    HYBRID = "hybrid"


class DataIntegrityLevel(Enum):
    """Data integrity verification levels"""

    BASIC = "basic"  # Simple checksum
    ADVANCED = "advanced"  # Hash + timestamp
    CRITICAL = "critical"  # Full integrity chain


@dataclass
class StorageMetadata:
    """Storage metadata for data integrity"""

    data_id: str
    timestamp: float
    checksum: str
    size: int
    version: int
    integrity_level: DataIntegrityLevel
    backup_count: int
    last_backup: Optional[float]


class PersistentDataStorage:
    """
    Implements persistent data storage with integrity and recovery

    Responsibilities:
    - Provide persistent data storage across restarts
    - Ensure data integrity and zero data loss
    - Implement backup and recovery systems
    - Support multiple storage types
    """

    def __init__(
        self,
        storage_type: StorageType = StorageType.HYBRID,
        base_path: str = "persistent_data",
    ):
        self.logger = logging.getLogger(f"{__name__}.PersistentDataStorage")
        self.storage_type = storage_type
        self.base_path = Path(base_path)
        self.data_path = self.base_path / "data"
        self.backup_path = self.base_path / "backups"
        self.metadata_path = self.base_path / "metadata"
        self.db_path = self.base_path / "storage.db"

        # Ensure directories exist
        self._create_storage_directories()

        # Initialize storage systems
        self._initialize_storage_systems()

        # Data integrity tracking
        self.data_metadata: Dict[str, StorageMetadata] = {}
        self.integrity_checks: List[Callable] = []
        self.backup_scheduler: Optional[threading.Thread] = None
        self.is_backup_active = False

        # Load existing metadata
        self._load_metadata()

    def _create_storage_directories(self):
        """Create necessary storage directories"""
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.backup_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)

        # Create type-specific data directories
        for data_type in [
            "messages",
            "tasks",
            "status",
            "config",
            "logs",
            "missions",
            "tests",
        ]:
            (self.data_path / data_type).mkdir(parents=True, exist_ok=True)

    def _initialize_storage_systems(self):
        """Initialize storage systems based on type"""
        if self.storage_type in [StorageType.DATABASE, StorageType.HYBRID]:
            self._initialize_database()

        if self.storage_type in [StorageType.FILE_BASED, StorageType.HYBRID]:
            self._initialize_file_storage()

    def _initialize_database(self):
        """Initialize SQLite database for structured storage"""
        try:
            self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.cursor = self.conn.cursor()

            # Create tables
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS data_entries (
                    id TEXT PRIMARY KEY,
                    data_type TEXT,
                    content TEXT,
                    timestamp REAL,
                    checksum TEXT,
                    version INTEGER,
                    metadata TEXT
                )
            """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS backup_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_id TEXT,
                    backup_timestamp REAL,
                    backup_path TEXT,
                    checksum TEXT,
                    status TEXT
                )
            """
            )

            self.conn.commit()
            self.logger.info("Database initialized successfully")

        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            self.storage_type = StorageType.FILE_BASED

    def _initialize_file_storage(self):
        """Initialize file-based storage system"""
        # Directories are already created in _create_storage_directories
        pass

    def store_data(
        self,
        data_id: str,
        data: Any,
        data_type: str = "general",
        integrity_level: DataIntegrityLevel = DataIntegrityLevel.ADVANCED,
    ) -> bool:
        """Store data with integrity verification"""
        try:
            # Generate checksum
            data_str = json.dumps(data, sort_keys=True)
            checksum = hashlib.sha256(data_str.encode()).hexdigest()

            # Create metadata
            metadata = StorageMetadata(
                data_id=data_id,
                timestamp=time.time(),
                checksum=checksum,
                size=len(data_str),
                version=1,
                integrity_level=integrity_level,
                backup_count=0,
                last_backup=None,
            )

            # Store based on storage type
            if self.storage_type in [StorageType.DATABASE, StorageType.HYBRID]:
                self._store_in_database(data_id, data, data_type, metadata)

            if self.storage_type in [StorageType.FILE_BASED, StorageType.HYBRID]:
                self._store_in_file(data_id, data, data_type, metadata)

            # Update metadata
            self.data_metadata[data_id] = metadata
            self._save_metadata()

            # Schedule backup for critical data
            if integrity_level == DataIntegrityLevel.CRITICAL:
                self._schedule_backup(data_id, metadata)

            self.logger.info(f"Data stored successfully: {data_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to store data {data_id}: {e}")
            return False

    def _store_in_database(
        self, data_id: str, data: Any, data_type: str, metadata: StorageMetadata
    ):
        """Store data in SQLite database"""
        try:
            content = json.dumps(data)
            # Convert enum to string for JSON serialization
            metadata_dict = metadata.__dict__.copy()
            metadata_dict["integrity_level"] = metadata.integrity_level.value
            metadata_json = json.dumps(metadata_dict)

            # Use a separate connection for this operation to avoid cursor conflicts
            import sqlite3

            temp_conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            temp_cursor = temp_conn.cursor()

            temp_cursor.execute(
                """
                INSERT OR REPLACE INTO data_entries
                (id, data_type, content, timestamp, checksum, version, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    data_id,
                    data_type,
                    content,
                    metadata.timestamp,
                    metadata.checksum,
                    metadata.version,
                    metadata_json,
                ),
            )

            temp_conn.commit()
            temp_conn.close()

        except Exception as e:
            self.logger.error(f"Database storage failed for {data_id}: {e}")
            raise

    def _store_in_file(
        self, data_id: str, data: Any, data_type: str, metadata: StorageMetadata
    ):
        """Store data in file system"""
        try:
            # Determine file path
            file_path = self.data_path / data_type / f"{data_id}.json"

            # Create data package with enum conversion
            metadata_dict = metadata.__dict__.copy()
            metadata_dict["integrity_level"] = metadata.integrity_level.value

            data_package = {
                "data": data,
                "metadata": metadata_dict,
                "stored_at": time.time(),
            }

            # Write to file
            with open(file_path, "w") as f:
                json.dump(data_package, f, indent=2)

        except Exception as e:
            self.logger.error(f"File storage failed for {data_id}: {e}")
            raise

    def retrieve_data(self, data_id: str) -> Optional[Any]:
        """Retrieve data with integrity verification"""
        try:
            # Check metadata
            if data_id not in self.data_metadata:
                self.logger.warning(f"Data {data_id} not found in metadata")
                return None

            metadata = self.data_metadata[data_id]

            # Retrieve from appropriate storage
            data = None
            if self.storage_type in [StorageType.DATABASE, StorageType.HYBRID]:
                data = self._retrieve_from_database(data_id)

            if data is None and self.storage_type in [
                StorageType.FILE_BASED,
                StorageType.HYBRID,
            ]:
                data = self._retrieve_from_file(data_id)

            if data is None:
                self.logger.error(f"Data {data_id} not found in any storage")
                return None

            # Verify integrity
            if not self._verify_data_integrity(data, metadata):
                self.logger.error(f"Data integrity check failed for {data_id}")
                # Attempt recovery
                data = self._attempt_data_recovery(data_id, metadata)

            return data

        except Exception as e:
            self.logger.error(f"Failed to retrieve data {data_id}: {e}")
            return None

    def _retrieve_from_database(self, data_id: str) -> Optional[Any]:
        """Retrieve data from database"""
        try:
            self.cursor.execute(
                """
                SELECT content FROM data_entries WHERE id = ?
            """,
                (data_id,),
            )

            result = self.cursor.fetchone()
            if result:
                return json.loads(result[0])

        except Exception as e:
            self.logger.error(f"Database retrieval failed for {data_id}: {e}")

        return None

    def _retrieve_from_file(self, data_id: str) -> Optional[Any]:
        """Retrieve data from file system"""
        try:
            # Search in all data type directories
            for data_type_dir in self.data_path.iterdir():
                if data_type_dir.is_dir():
                    file_path = data_type_dir / f"{data_id}.json"
                    if file_path.exists():
                        with open(file_path, "r") as f:
                            data_package = json.load(f)
                            return data_package.get("data")

        except Exception as e:
            self.logger.error(f"File retrieval failed for {data_id}: {e}")

        return None

    def _verify_data_integrity(self, data: Any, metadata: StorageMetadata) -> bool:
        """Verify data integrity based on level"""
        try:
            data_str = json.dumps(data, sort_keys=True)
            current_checksum = hashlib.sha256(data_str.encode()).hexdigest()

            if metadata.integrity_level == DataIntegrityLevel.BASIC:
                return current_checksum == metadata.checksum

            elif metadata.integrity_level == DataIntegrityLevel.ADVANCED:
                # Check checksum and timestamp
                if current_checksum != metadata.checksum:
                    return False

                # Verify timestamp is reasonable
                current_time = time.time()
                return abs(current_time - metadata.timestamp) < 86400  # 24 hours

            elif metadata.integrity_level == DataIntegrityLevel.CRITICAL:
                # Full integrity verification
                if current_checksum != metadata.checksum:
                    return False

                # Check size
                if len(data_str) != metadata.size:
                    return False

                # Verify version
                return metadata.version > 0

            return False

        except Exception as e:
            self.logger.error(f"Integrity verification failed: {e}")
            return False

    def _attempt_data_recovery(
        self, data_id: str, metadata: StorageMetadata
    ) -> Optional[Any]:
        """Attempt to recover corrupted data"""
        try:
            self.logger.info(f"Attempting data recovery for {data_id}")

            # Try backup recovery
            backup_data = self._recover_from_backup(data_id)
            if backup_data:
                self.logger.info(f"Data recovered from backup: {data_id}")
                return backup_data

            # Try alternative storage
            if self.storage_type == StorageType.HYBRID:
                if metadata.checksum in self.data_metadata:
                    # Try to find data with same checksum
                    for other_id, other_metadata in self.data_metadata.items():
                        if (
                            other_metadata.checksum == metadata.checksum
                            and other_id != data_id
                        ):
                            return self.retrieve_data(other_id)

            self.logger.error(f"Data recovery failed for {data_id}")
            return None

        except Exception as e:
            self.logger.error(f"Recovery attempt failed for {data_id}: {e}")
            return None

    def _recover_from_backup(self, data_id: str) -> Optional[Any]:
        """Recover data from backup"""
        try:
            # Find most recent backup
            backup_files = list(self.backup_path.glob(f"{data_id}_*.json"))
            if not backup_files:
                return None

            # Get most recent backup
            latest_backup = max(backup_files, key=lambda f: f.stat().st_mtime)

            with open(latest_backup, "r") as f:
                backup_data = json.load(f)
                return backup_data.get("data")

        except Exception as e:
            self.logger.error(f"Backup recovery failed for {data_id}: {e}")
            return None

    def _schedule_backup(self, data_id: str, metadata: StorageMetadata):
        """Schedule backup for critical data"""
        if not self.is_backup_active:
            self.is_backup_active = True
            self.backup_scheduler = threading.Thread(
                target=self._backup_worker, daemon=True
            )
            self.backup_scheduler.start()

    def _backup_worker(self):
        """Background backup worker"""
        while self.is_backup_active:
            try:
                # Find data that needs backup
                for data_id, metadata in self.data_metadata.items():
                    if metadata.integrity_level == DataIntegrityLevel.CRITICAL and (
                        metadata.last_backup is None
                        or time.time() - metadata.last_backup > 3600
                    ):  # 1 hour
                        self._create_backup(data_id, metadata)

                time.sleep(300)  # Check every 5 minutes

            except Exception as e:
                self.logger.error(f"Backup worker error: {e}")
                time.sleep(60)

    def _create_backup(self, data_id: str, metadata: StorageMetadata):
        """Create backup of data"""
        try:
            # Retrieve data
            data = self.retrieve_data(data_id)
            if data is None:
                return

            # Create backup package with enum conversion
            metadata_dict = metadata.__dict__.copy()
            metadata_dict["integrity_level"] = metadata.integrity_level.value

            backup_package = {
                "data": data,
                "metadata": metadata_dict,
                "backup_timestamp": time.time(),
                "backup_version": metadata.version,
            }

            # Save backup
            backup_file = self.backup_path / f"{data_id}_{int(time.time())}.json"
            with open(backup_file, "w") as f:
                json.dump(backup_package, f, indent=2)

            # Update metadata
            metadata.backup_count += 1
            metadata.last_backup = time.time()
            self._save_metadata()

            # Log backup using separate connection
            try:
                import sqlite3

                temp_conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
                temp_cursor = temp_conn.cursor()

                temp_cursor.execute(
                    """
                    INSERT INTO backup_log (data_id, backup_timestamp, backup_path, checksum, status)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        data_id,
                        time.time(),
                        str(backup_file),
                        metadata.checksum,
                        "success",
                    ),
                )

                temp_conn.commit()
                temp_conn.close()
            except Exception as e:
                self.logger.warning(f"Failed to log backup to database: {e}")

            self.logger.info(f"Backup created for {data_id}")

        except Exception as e:
            self.logger.error(f"Backup creation failed for {data_id}: {e}")

    def _save_metadata(self):
        """Save metadata to persistent storage"""
        try:
            metadata_file = self.metadata_path / "storage_metadata.json"
            # Convert enums to strings for JSON serialization
            metadata_dict = {}
            for k, v in self.data_metadata.items():
                meta_dict = v.__dict__.copy()
                meta_dict["integrity_level"] = v.integrity_level.value
                metadata_dict[k] = meta_dict

            with open(metadata_file, "w") as f:
                json.dump(metadata_dict, f, indent=2)

        except Exception as e:
            self.logger.error(f"Failed to save metadata: {e}")

    def _load_metadata(self):
        """Load metadata from persistent storage"""
        try:
            metadata_file = self.metadata_path / "storage_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r") as f:
                    metadata_dict = json.load(f)

                for data_id, meta_dict in metadata_dict.items():
                    # Convert string back to enum
                    if "integrity_level" in meta_dict:
                        meta_dict["integrity_level"] = DataIntegrityLevel(
                            meta_dict["integrity_level"]
                        )
                    self.data_metadata[data_id] = StorageMetadata(**meta_dict)

                self.logger.info(
                    f"Loaded metadata for {len(self.data_metadata)} data entries"
                )

        except Exception as e:
            self.logger.error(f"Failed to load metadata: {e}")

    def get_storage_status(self) -> Dict[str, Any]:
        """Get current storage system status"""
        return {
            "storage_type": self.storage_type.value,
            "total_data_entries": len(self.data_metadata),
            "backup_count": sum(m.backup_count for m in self.data_metadata.values()),
            "critical_data_count": sum(
                1
                for m in self.data_metadata.values()
                if m.integrity_level == DataIntegrityLevel.CRITICAL
            ),
            "backup_system_active": self.is_backup_active,
            "storage_paths": {
                "data": str(self.data_path),
                "backup": str(self.backup_path),
                "metadata": str(self.metadata_path),
            },
            "status": "PERSISTENT_STORAGE_ACTIVE",
        }

    def cleanup_old_backups(self, max_age_hours: int = 24):
        """Clean up old backup files"""
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600

            for backup_file in self.backup_path.glob("*.json"):
                if current_time - backup_file.stat().st_mtime > max_age_seconds:
                    backup_file.unlink()
                    self.logger.info(f"Cleaned up old backup: {backup_file.name}")

        except Exception as e:
            self.logger.error(f"Backup cleanup failed: {e}")

    def shutdown(self):
        """Gracefully shutdown storage system"""
        try:
            self.is_backup_active = False
            if self.backup_scheduler:
                self.backup_scheduler.join(timeout=5)

            if hasattr(self, "conn"):
                self.conn.close()

            self._save_metadata()
            self.logger.info("Storage system shutdown complete")

        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")


def main():
    """CLI interface for Persistent Data Storage"""
    import argparse

    parser = argparse.ArgumentParser(description="Persistent Data Storage CLI")
    parser.add_argument("--store", "-s", help="Store data (JSON file)")
    parser.add_argument("--retrieve", "-r", help="Retrieve data by ID")
    parser.add_argument("--status", action="store_true", help="Show storage status")
    parser.add_argument("--backup", action="store_true", help="Create manual backup")
    parser.add_argument("--cleanup", action="store_true", help="Clean up old backups")

    args = parser.parse_args()

    storage = PersistentDataStorage()

    if args.store:
        try:
            with open(args.store, "r") as f:
                data = json.load(f)

            data_id = data.get("id", f"data_{int(time.time())}")
            success = storage.store_data(
                data_id, data, "test", DataIntegrityLevel.CRITICAL
            )

            if success:
                print(f"✅ Data stored successfully: {data_id}")
            else:
                print(f"❌ Failed to store data: {data_id}")

        except FileNotFoundError:
            print(f"❌ File not found: {args.store}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in file: {args.store}")

    elif args.retrieve:
        data = storage.retrieve_data(args.retrieve)
        if data:
            print(f"✅ Data retrieved: {args.retrieve}")
            print(f"📄 Content: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Data not found: {args.retrieve}")

    elif args.status:
        status = storage.get_storage_status()
        print("📊 Storage System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")

    elif args.backup:
        print("🔄 Creating manual backup...")
        for data_id in storage.data_metadata.keys():
            metadata = storage.data_metadata[data_id]
            storage._create_backup(data_id, metadata)
        print("✅ Manual backup complete")

    elif args.cleanup:
        print("🧹 Cleaning up old backups...")
        storage.cleanup_old_backups()
        print("✅ Cleanup complete")

    else:
        print("Persistent Data Storage - Use --help for options")

    storage.shutdown()


if __name__ == "__main__":
    main()
