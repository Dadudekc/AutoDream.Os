#!/usr/bin/env python3
"""
Test-Driven Development: Storage System Tests
============================================

Tests written BEFORE implementation to drive development.
Follows TDD workflow: RED (failing) → GREEN (passing) → REFACTOR.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Import storage types and classes
from src.core.storage.storage_types import (
    StorageType,
    DataIntegrityLevel,
    BackupStrategy,
    StorageMetadata,
    StorageConfig,
)
from src.core.storage.storage_core import PersistentDataStorage
from src.core.storage.storage_backup import StorageBackupManager
from src.core.storage.storage_integration import UnifiedStorageSystem


class TestStorageTypes:
    """Test storage type definitions and enums."""

    def test_storage_type_enum_values(self):
        """Test StorageType enum has correct values."""
        assert StorageType.FILE_BASED.value == "file_based"
        assert StorageType.DATABASE.value == "database"
        assert StorageType.HYBRID.value == "hybrid"

    def test_data_integrity_level_enum_values(self):
        """Test DataIntegrityLevel enum has correct values."""
        assert DataIntegrityLevel.BASIC.value == "basic"
        assert DataIntegrityLevel.ADVANCED.value == "advanced"
        assert DataIntegrityLevel.CRITICAL.value == "critical"

    def test_backup_strategy_enum_values(self):
        """Test BackupStrategy enum has correct values."""
        assert BackupStrategy.INCREMENTAL.value == "incremental"
        assert BackupStrategy.FULL.value == "full"
        assert BackupStrategy.DIFFERENTIAL.value == "differential"

    def test_storage_metadata_creation(self):
        """Test StorageMetadata dataclass creation."""
        metadata = StorageMetadata(
            data_id="test_123",
            timestamp=1234567890.0,
            checksum="abc123",
            size=1024,
            version=1,
            integrity_level=DataIntegrityLevel.ADVANCED,
            backup_count=0,
            last_backup=None,
        )

        assert metadata.data_id == "test_123"
        assert metadata.timestamp == 1234567890.0
        assert metadata.checksum == "abc123"
        assert metadata.size == 1024
        assert metadata.version == 1
        assert metadata.integrity_level == DataIntegrityLevel.ADVANCED
        assert metadata.backup_count == 0
        assert metadata.last_backup is None

    def test_storage_config_creation(self):
        """Test StorageConfig dataclass creation."""
        config = StorageConfig(
            storage_type=StorageType.HYBRID,
            base_path="/test/path",
            max_file_size=1048576,
            compression_enabled=True,
            encryption_enabled=False,
            backup_retention_days=30,
        )

        assert config.storage_type == StorageType.HYBRID
        assert config.base_path == "/test/path"
        assert config.max_file_size == 1048576
        assert config.compression_enabled is True
        assert config.encryption_enabled is False
        assert config.backup_retention_days == 30


class TestPersistentDataStorage:
    """Test PersistentDataStorage core functionality."""

    @pytest.fixture
    def temp_storage_dir(self):
        """Create temporary storage directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def storage_config(self, temp_storage_dir):
        """Create storage configuration for testing."""
        return StorageConfig(
            storage_type=StorageType.HYBRID,
            base_path=temp_storage_dir,
            max_file_size=1048576,
            compression_enabled=True,
            encryption_enabled=False,
            backup_retention_days=30,
        )

    @pytest.fixture
    def storage_instance(self, storage_config):
        """Create PersistentDataStorage instance for testing."""
        return PersistentDataStorage(storage_config)

    def test_storage_initialization(self, storage_instance, storage_config):
        """Test storage system initializes correctly."""
        assert storage_instance.config == storage_config
        assert storage_instance.base_path == Path(storage_config.base_path)
        assert storage_instance.data_path.exists()
        assert storage_instance.backup_path.exists()
        assert storage_instance.metadata_path.exists()

    def test_storage_directories_creation(self, storage_instance):
        """Test that all required directories are created."""
        data_types = [
            "messages",
            "tasks",
            "status",
            "config",
            "logs",
            "missions",
            "tests",
        ]

        for data_type in data_types:
            type_dir = storage_instance.data_path / data_type
            assert type_dir.exists()
            assert type_dir.is_dir()

    def test_database_initialization(self, storage_instance):
        """Test that SQLite database is initialized correctly."""
        assert storage_instance.db_path.exists()
        assert storage_instance.db_conn is not None
        assert storage_instance.db_cursor is not None

    def test_store_data_success(self, storage_instance):
        """Test successful data storage."""
        test_data = {"key": "value", "number": 42}
        data_id = "test_data_123"

        success = storage_instance.store_data(data_id, test_data, "test")
        assert success is True

        # Verify data file exists
        data_file = storage_instance.data_path / "test" / f"{data_id}.json"
        assert data_file.exists()

        # Verify metadata is stored
        assert data_id in storage_instance.data_metadata

    def test_store_data_failure(self, storage_instance):
        """Test data storage failure handling."""
        # Test with invalid data that would cause serialization failure
        with patch("json.dumps") as mock_dumps:
            mock_dumps.side_effect = Exception("Serialization failed")

            success = storage_instance.store_data("test_id", {"data": "test"}, "test")
            assert success is False

    def test_retrieve_data_success(self, storage_instance):
        """Test successful data retrieval."""
        # First store data
        test_data = {"key": "value", "number": 42}
        data_id = "test_data_456"
        storage_instance.store_data(data_id, test_data, "test")

        # Then retrieve it
        retrieved_data = storage_instance.retrieve_data(data_id, "test")
        assert retrieved_data == test_data

    def test_retrieve_data_not_found(self, storage_instance):
        """Test data retrieval when data doesn't exist."""
        retrieved_data = storage_instance.retrieve_data("nonexistent_id", "test")
        assert retrieved_data is None

    def test_retrieve_data_integrity_failure(self, storage_instance):
        """Test data retrieval with integrity check failure."""
        # Store data first
        test_data = {"key": "value"}
        data_id = "test_data_789"
        storage_instance.store_data(data_id, test_data, "test")

        # Corrupt the data file
        data_file = storage_instance.data_path / "test" / f"{data_id}.json"
        data_file.write_text("corrupted data")

        # Retrieval should fail due to checksum mismatch
        retrieved_data = storage_instance.retrieve_data(data_id, "test")
        assert retrieved_data is None

    def test_get_storage_stats(self, storage_instance):
        """Test storage statistics retrieval."""
        # Store some test data
        storage_instance.store_data("test1", {"data": "test1"}, "test")
        storage_instance.store_data("test2", {"data": "test2"}, "test")

        stats = storage_instance.get_storage_stats()

        assert "total_data_entries" in stats
        assert "total_storage_size" in stats
        assert "storage_type" in stats
        assert "integrity_level" in stats
        assert stats["total_data_entries"] == 2
        assert stats["total_storage_size"] > 0


class TestStorageBackupManager:
    """Test StorageBackupManager functionality."""

    @pytest.fixture
    def temp_backup_dir(self):
        """Create temporary backup directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def backup_manager(self, temp_backup_dir):
        """Create StorageBackupManager instance for testing."""
        return StorageBackupManager(Path(temp_backup_dir), retention_days=7)

    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory for testing."""
        temp_dir = tempfile.mkdtemp()
        # Create some test files
        (Path(temp_dir) / "test1.txt").write_text("test data 1")
        (Path(temp_dir) / "test2.txt").write_text("test data 2")
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_backup_manager_initialization(self, backup_manager, temp_backup_dir):
        """Test backup manager initializes correctly."""
        assert backup_manager.backup_path == Path(temp_backup_dir)
        assert backup_manager.retention_days == 7
        assert backup_manager.backup_history == []

    def test_create_backup_success(self, backup_manager, temp_data_dir):
        """Test successful backup creation."""
        backup_name = backup_manager.create_backup(Path(temp_data_dir))

        assert backup_name is not None
        assert backup_name.startswith("backup_")

        # Verify backup directory exists
        backup_dir = backup_manager.backup_path / backup_name
        assert backup_dir.exists()

        # Verify backup metadata exists
        metadata_file = backup_dir / "backup_metadata.json"
        assert metadata_file.exists()

        # Verify backup history is updated
        assert len(backup_manager.backup_history) == 1

    def test_create_backup_with_custom_name(self, backup_manager, temp_data_dir):
        """Test backup creation with custom name."""
        custom_name = "my_custom_backup"
        backup_name = backup_manager.create_backup(Path(temp_data_dir), custom_name)

        assert backup_name == custom_name

        # Verify backup directory exists
        backup_dir = backup_manager.backup_path / custom_name
        assert backup_dir.exists()

    def test_create_backup_duplicate_name(self, backup_manager, temp_data_dir):
        """Test backup creation with duplicate name."""
        # Create first backup
        backup_name = backup_manager.create_backup(
            Path(temp_data_dir), "duplicate_name"
        )
        assert backup_name == "duplicate_name"

        # Try to create second backup with same name
        second_backup_name = backup_manager.create_backup(
            Path(temp_data_dir), "duplicate_name"
        )
        assert second_backup_name is None

    def test_list_backups(self, backup_manager, temp_data_dir):
        """Test backup listing functionality."""
        # Create multiple backups
        backup1 = backup_manager.create_backup(Path(temp_data_dir), "backup1")
        backup2 = backup_manager.create_backup(Path(temp_data_dir), "backup2")

        backups = backup_manager.list_backups()

        assert len(backups) == 2
        assert backups[0]["backup_name"] == "backup2"  # Most recent first
        assert backups[1]["backup_name"] == "backup1"

    def test_get_backup_info(self, backup_manager, temp_data_dir):
        """Test backup information retrieval."""
        backup_name = backup_manager.create_backup(Path(temp_data_dir), "test_backup")

        backup_info = backup_manager.get_backup_info(backup_name)

        assert backup_info is not None
        assert backup_info["backup_name"] == backup_name
        assert "timestamp" in backup_info
        assert "size" in backup_info
        assert "file_count" in backup_info

    def test_get_backup_info_nonexistent(self, backup_manager):
        """Test backup information retrieval for nonexistent backup."""
        backup_info = backup_manager.get_backup_info("nonexistent_backup")
        assert backup_info is None

    def test_delete_backup_success(self, backup_manager, temp_data_dir):
        """Test successful backup deletion."""
        backup_name = backup_manager.create_backup(Path(temp_data_dir), "delete_test")

        # Verify backup exists
        backup_dir = backup_manager.backup_path / backup_name
        assert backup_dir.exists()

        # Delete backup
        success = backup_manager.delete_backup(backup_name)
        assert success is True

        # Verify backup is deleted
        assert not backup_dir.exists()

        # Verify backup history is updated
        assert len(backup_manager.backup_history) == 0

    def test_delete_backup_nonexistent(self, backup_manager):
        """Test backup deletion for nonexistent backup."""
        success = backup_manager.delete_backup("nonexistent_backup")
        assert success is False

    def test_cleanup_old_backups(self, backup_manager, temp_data_dir):
        """Test cleanup of old backups."""
        # Create backup with old timestamp
        with patch("time.time") as mock_time:
            mock_time.return_value = 0  # Very old timestamp
            backup_manager.create_backup(Path(temp_data_dir), "old_backup")

        # Create backup with current timestamp
        backup_manager.create_backup(Path(temp_data_dir), "new_backup")

        # Verify we have 2 backups
        assert len(backup_manager.backup_history) == 2

        # Cleanup old backups
        deleted_count = backup_manager.cleanup_old_backups()

        # Should delete 1 old backup
        assert deleted_count == 1
        assert len(backup_manager.backup_history) == 1
        assert backup_manager.backup_history[0]["backup_name"] == "new_backup"


class TestUnifiedStorageSystem:
    """Test UnifiedStorageSystem integration."""

    @pytest.fixture
    def temp_unified_dir(self):
        """Create temporary directory for unified storage testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def unified_storage(self, temp_unified_dir):
        """Create UnifiedStorageSystem instance for testing."""
        return UnifiedStorageSystem(
            base_path=temp_unified_dir,
            storage_type=StorageType.HYBRID,
            integrity_level=DataIntegrityLevel.ADVANCED,
        )

    def test_unified_storage_initialization(self, unified_storage, temp_unified_dir):
        """Test unified storage system initializes correctly."""
        assert unified_storage.storage is not None
        assert unified_storage.backup_manager is not None
        assert isinstance(unified_storage.storage, PersistentDataStorage)
        assert isinstance(unified_storage.backup_manager, StorageBackupManager)

    def test_unified_data_operations(self, unified_storage):
        """Test unified data storage and retrieval."""
        test_data = {"unified": "test", "data": 123}
        data_id = "unified_test_123"

        # Store data
        success = unified_storage.store_data(data_id, test_data, "unified")
        assert success is True

        # Retrieve data
        retrieved_data = unified_storage.retrieve_data(data_id, "unified")
        assert retrieved_data == test_data

    def test_unified_backup_operations(self, unified_storage):
        """Test unified backup operations."""
        # Store some test data first
        unified_storage.store_data("backup_test", {"data": "test"}, "test")

        # Create backup
        backup_name = unified_storage.create_backup()
        assert backup_name is not None

        # List backups
        backups = unified_storage.list_backups()
        assert len(backups) == 1
        assert backups[0]["backup_name"] == backup_name

    def test_unified_storage_stats(self, unified_storage):
        """Test unified storage statistics."""
        # Store some test data
        unified_storage.store_data("stats_test1", {"data": "test1"}, "test")
        unified_storage.store_data("stats_test2", {"data": "test2"}, "test")

        stats = unified_storage.get_storage_stats()

        assert "total_data_entries" in stats
        assert "total_storage_size" in stats
        assert "backups" in stats
        assert stats["total_data_entries"] == 2
        assert stats["backups"] >= 0

    def test_unified_data_deletion(self, unified_storage):
        """Test unified data deletion."""
        # Store test data
        data_id = "delete_test_123"
        unified_storage.store_data(data_id, {"data": "test"}, "test")

        # Verify data exists
        assert unified_storage.get_data_metadata(data_id) is not None

        # Delete data
        success = unified_storage.delete_data(data_id)
        assert success is True

        # Verify data is deleted
        assert unified_storage.get_data_metadata(data_id) is None

    def test_unified_data_listing(self, unified_storage):
        """Test unified data listing functionality."""
        # Store data in different types
        unified_storage.store_data("msg1", {"type": "message"}, "messages")
        unified_storage.store_data("task1", {"type": "task"}, "tasks")
        unified_storage.store_data("config1", {"type": "config"}, "config")

        # List all data entries
        all_entries = unified_storage.list_data_entries()
        assert len(all_entries) == 3
        assert "msg1" in all_entries
        assert "task1" in all_entries
        assert "config1" in all_entries

        # List entries by type
        message_entries = unified_storage.list_data_entries("messages")
        assert len(message_entries) == 1
        assert "msg1" in message_entries


# Test execution and coverage verification
if __name__ == "__main__":
    # Run tests with coverage
    pytest.main(
        [
            __file__,
            "--cov=src.core.storage",
            "--cov-report=term-missing",
            "--cov-report=html",
            "-v",
        ]
    )
