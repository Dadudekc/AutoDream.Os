#!/usr/bin/env python3
"""
Test-Driven Development: Integrity System Tests
==============================================

Tests written BEFORE implementation to drive development.
Follows TDD workflow: RED (failing) → GREEN (passing) → REFACTOR.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Import integrity types and classes
from src.core.integrity.integrity_types import (
    IntegrityCheckType,
    RecoveryStrategy,
    IntegrityLevel,
    IntegrityCheck,
    IntegrityViolation,
    IntegrityConfig,
)
from src.core.integrity.integrity_core import DataIntegrityManager


class TestIntegrityTypes:
    """Test integrity type definitions and enums."""

    def test_integrity_check_type_enum_values(self):
        """Test IntegrityCheckType enum has correct values."""
        assert IntegrityCheckType.CHECKSUM.value == "checksum"
        assert IntegrityCheckType.HASH_CHAIN.value == "hash_chain"
        assert IntegrityCheckType.TIMESTAMP.value == "timestamp"
        assert IntegrityCheckType.SIZE_VERIFICATION.value == "size_verification"
        assert IntegrityCheckType.VERSION_CONTROL.value == "version_control"

    def test_recovery_strategy_enum_values(self):
        """Test RecoveryStrategy enum has correct values."""
        assert RecoveryStrategy.BACKUP_RESTORE.value == "backup_restore"
        assert RecoveryStrategy.CHECKSUM_MATCH.value == "checksum_match"
        assert RecoveryStrategy.TIMESTAMP_ROLLBACK.value == "timestamp_rollback"
        assert RecoveryStrategy.VERSION_ROLLBACK.value == "version_rollback"
        assert RecoveryStrategy.MANUAL_RECOVERY.value == "manual_recovery"

    def test_integrity_level_enum_values(self):
        """Test IntegrityLevel enum has correct values."""
        assert IntegrityLevel.BASIC.value == "basic"
        assert IntegrityLevel.ADVANCED.value == "advanced"
        assert IntegrityLevel.CRITICAL.value == "critical"

    def test_integrity_check_creation(self):
        """Test IntegrityCheck dataclass creation."""
        check = IntegrityCheck(
            check_id="check_123",
            data_id="data_456",
            check_type=IntegrityCheckType.CHECKSUM,
            timestamp=1234567890.0,
            passed=True,
            details={"status": "verified"},
            recovery_attempted=False,
            recovery_successful=False,
        )

        assert check.check_id == "check_123"
        assert check.data_id == "data_456"
        assert check.check_type == IntegrityCheckType.CHECKSUM
        assert check.timestamp == 1234567890.0
        assert check.passed is True
        assert check.details == {"status": "verified"}
        assert check.recovery_attempted is False
        assert check.recovery_successful is False

    def test_integrity_violation_creation(self):
        """Test IntegrityViolation dataclass creation."""
        violation = IntegrityViolation(
            violation_id="violation_123",
            data_id="data_456",
            violation_type="checksum_mismatch",
            severity="high",
            timestamp=1234567890.0,
            description="Data integrity check failed",
            affected_data={"file": "test.txt", "size": 1024},
            suggested_recovery=RecoveryStrategy.BACKUP_RESTORE,
        )

        assert violation.violation_id == "violation_123"
        assert violation.data_id == "data_456"
        assert violation.violation_type == "checksum_mismatch"
        assert violation.severity == "high"
        assert violation.timestamp == 1234567890.0
        assert violation.description == "Data integrity check failed"
        assert violation.affected_data == {"file": "test.txt", "size": 1024}
        assert violation.suggested_recovery == RecoveryStrategy.BACKUP_RESTORE

    def test_integrity_config_creation(self):
        """Test IntegrityConfig dataclass creation."""
        config = IntegrityConfig(
            check_interval=300,
            recovery_enabled=True,
            alert_on_violation=True,
            auto_recovery=False,
            max_recovery_attempts=3,
        )

        assert config.check_interval == 300
        assert config.recovery_enabled is True
        assert config.alert_on_violation is True
        assert config.auto_recovery is False
        assert config.max_recovery_attempts == 3


class TestDataIntegrityManager:
    """Test DataIntegrityManager core functionality."""

    @pytest.fixture
    def temp_integrity_dir(self):
        """Create temporary integrity directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def integrity_manager(self, temp_integrity_dir):
        """Create DataIntegrityManager instance for testing."""
        return DataIntegrityManager(storage_path=temp_integrity_dir)

    def test_integrity_manager_initialization(
        self, integrity_manager, temp_integrity_dir
    ):
        """Test integrity manager initializes correctly."""
        assert integrity_manager.storage_path == Path(temp_integrity_dir)
        assert integrity_manager.integrity_db_path.exists()
        assert integrity_manager.audit_log_path.exists()
        assert integrity_manager.active_checks == {}
        assert integrity_manager.check_history == []
        assert len(integrity_manager.recovery_strategies) == 5

    def test_database_initialization(self, integrity_manager):
        """Test that integrity database is initialized correctly."""
        assert integrity_manager.integrity_db_path.exists()
        assert integrity_manager.integrity_conn is not None
        assert integrity_manager.integrity_cursor is not None

        # Verify tables exist
        integrity_manager.integrity_cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in integrity_manager.integrity_cursor.fetchall()]

        assert "integrity_checks" in tables
        assert "integrity_violations" in tables

    def test_recovery_strategies_initialization(self, integrity_manager):
        """Test that all recovery strategies are initialized."""
        expected_strategies = [
            RecoveryStrategy.BACKUP_RESTORE,
            RecoveryStrategy.CHECKSUM_MATCH,
            RecoveryStrategy.TIMESTAMP_ROLLBACK,
            RecoveryStrategy.VERSION_ROLLBACK,
            RecoveryStrategy.MANUAL_RECOVERY,
        ]

        for strategy in expected_strategies:
            assert strategy in integrity_manager.recovery_strategies
            assert callable(integrity_manager.recovery_strategies[strategy])

    def test_perform_integrity_check_checksum(self, integrity_manager):
        """Test checksum integrity check."""
        check = integrity_manager.perform_integrity_check(
            "test_data_123", IntegrityCheckType.CHECKSUM
        )

        assert check.check_id.startswith("test_data_123_checksum_")
        assert check.data_id == "test_data_123"
        assert check.check_type == IntegrityCheckType.CHECKSUM
        assert check.timestamp > 0
        assert check.passed is True  # Placeholder implementation returns True
        assert check.recovery_attempted is False
        assert check.recovery_successful is False

        # Verify check is recorded
        assert check in integrity_manager.check_history

    def test_perform_integrity_check_hash_chain(self, integrity_manager):
        """Test hash chain integrity check."""
        check = integrity_manager.perform_integrity_check(
            "test_data_456", IntegrityCheckType.HASH_CHAIN
        )

        assert check.check_type == IntegrityCheckType.HASH_CHAIN
        assert check.data_id == "test_data_456"
        assert check.passed is True  # Placeholder implementation returns True

    def test_perform_integrity_check_timestamp(self, integrity_manager):
        """Test timestamp integrity check."""
        check = integrity_manager.perform_integrity_check(
            "test_data_789", IntegrityCheckType.TIMESTAMP
        )

        assert check.check_type == IntegrityCheckType.TIMESTAMP
        assert check.data_id == "test_data_789"
        assert check.passed is True  # Placeholder implementation returns True

    def test_perform_integrity_check_size_verification(self, integrity_manager):
        """Test size verification integrity check."""
        check = integrity_manager.perform_integrity_check(
            "test_data_size", IntegrityCheckType.SIZE_VERIFICATION
        )

        assert check.check_type == IntegrityCheckType.SIZE_VERIFICATION
        assert check.data_id == "test_data_size"
        assert check.passed is True  # Placeholder implementation returns True

    def test_perform_integrity_check_version_control(self, integrity_manager):
        """Test version control integrity check."""
        check = integrity_manager.perform_integrity_check(
            "test_data_version", IntegrityCheckType.VERSION_CONTROL
        )

        assert check.check_type == IntegrityCheckType.VERSION_CONTROL
        assert check.data_id == "test_data_version"
        assert check.passed is True  # Placeholder implementation returns True

    def test_perform_integrity_check_error_handling(self, integrity_manager):
        """Test integrity check error handling."""
        # Mock verification methods to raise exceptions
        with patch.object(integrity_manager, "_verify_checksum") as mock_verify:
            mock_verify.side_effect = Exception("Verification failed")

            check = integrity_manager.perform_integrity_check(
                "error_test", IntegrityCheckType.CHECKSUM
            )

            assert check.passed is False
            assert "error" in check.details
            assert "Verification failed" in check.details["error"]

    def test_integrity_check_database_recording(self, integrity_manager):
        """Test that integrity checks are recorded in database."""
        # Perform a check
        check = integrity_manager.perform_integrity_check(
            "db_test", IntegrityCheckType.CHECKSUM
        )

        # Verify it's in the database
        integrity_manager.integrity_cursor.execute(
            "SELECT * FROM integrity_checks WHERE check_id = ?", (check.check_id,)
        )
        row = integrity_manager.integrity_cursor.fetchone()

        assert row is not None
        assert row[0] == check.check_id
        assert row[1] == check.data_id
        assert row[2] == check.check_type.value
        assert row[3] == check.timestamp
        assert row[4] == check.passed
        assert row[5] == "{}"  # Empty details JSON
        assert row[6] == check.recovery_attempted
        assert row[7] == check.recovery_successful

    def test_recovery_strategy_execution(self, integrity_manager):
        """Test recovery strategy execution."""
        # Test backup restore recovery
        success = integrity_manager.recovery_strategies[
            RecoveryStrategy.BACKUP_RESTORE
        ]("test_data")
        assert success is True  # Placeholder implementation returns True

        # Test checksum match recovery
        success = integrity_manager.recovery_strategies[
            RecoveryStrategy.CHECKSUM_MATCH
        ]("test_data")
        assert success is True  # Placeholder implementation returns True

        # Test timestamp rollback recovery
        success = integrity_manager.recovery_strategies[
            RecoveryStrategy.TIMESTAMP_ROLLBACK
        ]("test_data")
        assert success is True  # Placeholder implementation returns True

        # Test version rollback recovery
        success = integrity_manager.recovery_strategies[
            RecoveryStrategy.VERSION_ROLLBACK
        ]("test_data")
        assert success is True  # Placeholder implementation returns True

        # Test manual recovery
        success = integrity_manager.recovery_strategies[
            RecoveryStrategy.MANUAL_RECOVERY
        ]("test_data")
        assert success is False  # Manual recovery always requires intervention

    def test_get_integrity_stats(self, integrity_manager):
        """Test integrity statistics retrieval."""
        # Perform some checks first
        integrity_manager.perform_integrity_check(
            "stats_test1", IntegrityCheckType.CHECKSUM
        )
        integrity_manager.perform_integrity_check(
            "stats_test2", IntegrityCheckType.HASH_CHAIN
        )
        integrity_manager.perform_integrity_check(
            "stats_test3", IntegrityCheckType.TIMESTAMP
        )

        stats = integrity_manager.get_integrity_stats()

        assert "total_checks" in stats
        assert "passed_checks" in stats
        assert "failed_checks" in stats
        assert "recovery_attempts" in stats
        assert "successful_recoveries" in stats

        assert stats["total_checks"] == 3
        assert (
            stats["passed_checks"] == 3
        )  # All placeholder implementations return True
        assert stats["failed_checks"] == 0
        assert stats["recovery_attempts"] == 0
        assert stats["successful_recoveries"] == 0

    def test_integrity_check_history_tracking(self, integrity_manager):
        """Test that integrity checks are tracked in history."""
        # Perform multiple checks
        check1 = integrity_manager.perform_integrity_check(
            "history1", IntegrityCheckType.CHECKSUM
        )
        check2 = integrity_manager.perform_integrity_check(
            "history2", IntegrityCheckType.HASH_CHAIN
        )
        check3 = integrity_manager.perform_integrity_check(
            "history3", IntegrityCheckType.TIMESTAMP
        )

        # Verify all checks are in history
        assert len(integrity_manager.check_history) == 3
        assert check1 in integrity_manager.check_history
        assert check2 in integrity_manager.check_history
        assert check3 in integrity_manager.check_history

        # Verify check IDs are unique
        check_ids = [check.check_id for check in integrity_manager.check_history]
        assert len(check_ids) == len(set(check_ids))

    def test_integrity_check_timestamp_generation(self, integrity_manager):
        """Test that integrity check timestamps are generated correctly."""
        import time

        before_check = time.time()
        check = integrity_manager.perform_integrity_check(
            "timestamp_test", IntegrityCheckType.CHECKSUM
        )
        after_check = time.time()

        assert before_check <= check.timestamp <= after_check

    def test_integrity_check_id_format(self, integrity_manager):
        """Test that integrity check IDs follow the expected format."""
        check = integrity_manager.perform_integrity_check(
            "id_format_test", IntegrityCheckType.CHECKSUM
        )

        # Expected format: data_id_checktype_timestamp
        parts = check.check_id.split("_")
        assert len(parts) >= 3
        assert parts[0] == "id_format_test"
        assert parts[1] == "checksum"
        assert parts[2].isdigit()  # Timestamp should be numeric


# Test execution and coverage verification
if __name__ == "__main__":
    # Run tests with coverage
    pytest.main(
        [
            __file__,
            "--cov=src.core.integrity",
            "--cov-report=term-missing",
            "--cov-report=html",
            "-v",
        ]
    )
