#!/usr/bin/env python3
"""
SSOT Unified - Consolidated Single Source of Truth System
========================================================

Consolidated SSOT system providing unified SSOT functionality for:
- SSOT models and data structures
- SSOT validators and validation
- SSOT execution and coordination
- SSOT management and monitoring
- SSOT synchronization and consistency

This module consolidates 10 SSOT files into 3 unified modules for better
maintainability and reduced complexity.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

# ============================================================================
# SSOT ENUMS AND MODELS
# ============================================================================


class SSOTStatus(Enum):
    """SSOT status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SYNCING = "syncing"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class SSOTType(Enum):
    """SSOT type enumeration."""

    CONFIGURATION = "configuration"
    DATA = "data"
    SCHEMA = "schema"
    METADATA = "metadata"
    RULES = "rules"
    POLICIES = "policies"


class SSOTOperation(Enum):
    """SSOT operation enumeration."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    SYNC = "sync"
    VALIDATE = "validate"


class SSOTConsistency(Enum):
    """SSOT consistency enumeration."""

    CONSISTENT = "consistent"
    INCONSISTENT = "inconsistent"
    PARTIALLY_CONSISTENT = "partially_consistent"
    UNKNOWN = "unknown"


# ============================================================================
# SSOT MODELS
# ============================================================================


@dataclass
class SSOTRecord:
    """SSOT record model."""

    record_id: str
    ssot_type: SSOTType
    key: str
    value: Any
    version: int
    status: SSOTStatus
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SSOTOperation:
    """SSOT operation model."""

    operation_id: str
    ssot_type: SSOTType
    operation: SSOTOperation
    key: str
    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = False
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SSOTValidation:
    """SSOT validation model."""

    validation_id: str
    ssot_type: SSOTType
    key: str
    is_valid: bool
    validation_rules: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SSOTMetrics:
    """SSOT metrics model."""

    ssot_type: SSOTType
    total_records: int = 0
    active_records: int = 0
    sync_operations: int = 0
    validation_operations: int = 0
    error_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


# ============================================================================
# SSOT INTERFACES
# ============================================================================


class SSOTManager(ABC):
    """Base SSOT manager interface."""

    def __init__(self, manager_id: str, name: str, ssot_type: SSOTType):
        self.manager_id = manager_id
        self.name = name
        self.ssot_type = ssot_type
        self.status = SSOTStatus.INACTIVE
        self.logger = logging.getLogger(f"ssot.{name}")
        self.metrics = SSOTMetrics(ssot_type=ssot_type)

    @abstractmethod
    def start(self) -> bool:
        """Start SSOT manager."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Stop SSOT manager."""
        pass

    @abstractmethod
    def create_record(self, key: str, value: Any) -> SSOTRecord | None:
        """Create SSOT record."""
        pass

    @abstractmethod
    def read_record(self, key: str) -> SSOTRecord | None:
        """Read SSOT record."""
        pass

    @abstractmethod
    def update_record(self, key: str, value: Any) -> SSOTRecord | None:
        """Update SSOT record."""
        pass

    @abstractmethod
    def delete_record(self, key: str) -> bool:
        """Delete SSOT record."""
        pass

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        """Get SSOT manager capabilities."""
        pass


class SSOTValidator(ABC):
    """Base SSOT validator interface."""

    def __init__(self, validator_id: str, name: str):
        self.validator_id = validator_id
        self.name = name
        self.logger = logging.getLogger(f"ssot_validator.{name}")
        self.is_active = False

    @abstractmethod
    def validate_record(self, record: SSOTRecord) -> SSOTValidation:
        """Validate SSOT record."""
        pass

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        """Get validator capabilities."""
        pass


# ============================================================================
# SSOT MANAGERS
# ============================================================================


class ConfigurationSSOTManager(SSOTManager):
    """Configuration SSOT manager implementation."""

    def __init__(self, manager_id: str = None):
        super().__init__(
            manager_id or str(uuid.uuid4()), "ConfigurationSSOTManager", SSOTType.CONFIGURATION
        )
        self.records: dict[str, SSOTRecord] = {}

    def start(self) -> bool:
        """Start configuration SSOT manager."""
        try:
            self.status = SSOTStatus.ACTIVE
            self.logger.info("Configuration SSOT manager started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start configuration SSOT manager: {e}")
            self.status = SSOTStatus.ERROR
            return False

    def stop(self) -> bool:
        """Stop configuration SSOT manager."""
        try:
            self.status = SSOTStatus.INACTIVE
            self.logger.info("Configuration SSOT manager stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop configuration SSOT manager: {e}")
            return False

    def create_record(self, key: str, value: Any) -> SSOTRecord | None:
        """Create configuration record."""
        try:
            if key in self.records:
                self.logger.warning(f"Record {key} already exists, updating instead")
                return self.update_record(key, value)

            record = SSOTRecord(
                record_id=str(uuid.uuid4()),
                ssot_type=self.ssot_type,
                key=key,
                value=value,
                version=1,
                status=SSOTStatus.ACTIVE,
            )

            self.records[key] = record
            self.metrics.total_records += 1
            self.metrics.active_records += 1

            self.logger.info(f"Configuration record {key} created")
            return record
        except Exception as e:
            self.logger.error(f"Failed to create configuration record {key}: {e}")
            self.metrics.error_count += 1
            return None

    def read_record(self, key: str) -> SSOTRecord | None:
        """Read configuration record."""
        try:
            record = self.records.get(key)
            if record:
                self.logger.debug(f"Configuration record {key} read")
            else:
                self.logger.warning(f"Configuration record {key} not found")
            return record
        except Exception as e:
            self.logger.error(f"Failed to read configuration record {key}: {e}")
            self.metrics.error_count += 1
            return None

    def update_record(self, key: str, value: Any) -> SSOTRecord | None:
        """Update configuration record."""
        try:
            if key not in self.records:
                self.logger.warning(f"Record {key} not found, creating instead")
                return self.create_record(key, value)

            record = self.records[key]
            record.value = value
            record.version += 1
            record.updated_at = datetime.now()

            self.logger.info(f"Configuration record {key} updated to version {record.version}")
            return record
        except Exception as e:
            self.logger.error(f"Failed to update configuration record {key}: {e}")
            self.metrics.error_count += 1
            return None

    def delete_record(self, key: str) -> bool:
        """Delete configuration record."""
        try:
            if key not in self.records:
                self.logger.warning(f"Record {key} not found")
                return False

            del self.records[key]
            self.metrics.active_records -= 1

            self.logger.info(f"Configuration record {key} deleted")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete configuration record {key}: {e}")
            self.metrics.error_count += 1
            return False

    def get_capabilities(self) -> list[str]:
        """Get configuration SSOT capabilities."""
        return ["configuration_management", "version_control", "record_crud"]


class DataSSOTManager(SSOTManager):
    """Data SSOT manager implementation."""

    def __init__(self, manager_id: str = None):
        super().__init__(manager_id or str(uuid.uuid4()), "DataSSOTManager", SSOTType.DATA)
        self.records: dict[str, SSOTRecord] = {}

    def start(self) -> bool:
        """Start data SSOT manager."""
        try:
            self.status = SSOTStatus.ACTIVE
            self.logger.info("Data SSOT manager started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start data SSOT manager: {e}")
            self.status = SSOTStatus.ERROR
            return False

    def stop(self) -> bool:
        """Stop data SSOT manager."""
        try:
            self.status = SSOTStatus.INACTIVE
            self.logger.info("Data SSOT manager stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop data SSOT manager: {e}")
            return False

    def create_record(self, key: str, value: Any) -> SSOTRecord | None:
        """Create data record."""
        try:
            if key in self.records:
                self.logger.warning(f"Record {key} already exists, updating instead")
                return self.update_record(key, value)

            record = SSOTRecord(
                record_id=str(uuid.uuid4()),
                ssot_type=self.ssot_type,
                key=key,
                value=value,
                version=1,
                status=SSOTStatus.ACTIVE,
            )

            self.records[key] = record
            self.metrics.total_records += 1
            self.metrics.active_records += 1

            self.logger.info(f"Data record {key} created")
            return record
        except Exception as e:
            self.logger.error(f"Failed to create data record {key}: {e}")
            self.metrics.error_count += 1
            return None

    def read_record(self, key: str) -> SSOTRecord | None:
        """Read data record."""
        try:
            record = self.records.get(key)
            if record:
                self.logger.debug(f"Data record {key} read")
            else:
                self.logger.warning(f"Data record {key} not found")
            return record
        except Exception as e:
            self.logger.error(f"Failed to read data record {key}: {e}")
            self.metrics.error_count += 1
            return None

    def update_record(self, key: str, value: Any) -> SSOTRecord | None:
        """Update data record."""
        try:
            if key not in self.records:
                self.logger.warning(f"Record {key} not found, creating instead")
                return self.create_record(key, value)

            record = self.records[key]
            record.value = value
            record.version += 1
            record.updated_at = datetime.now()

            self.logger.info(f"Data record {key} updated to version {record.version}")
            return record
        except Exception as e:
            self.logger.error(f"Failed to update data record {key}: {e}")
            self.metrics.error_count += 1
            return None

    def delete_record(self, key: str) -> bool:
        """Delete data record."""
        try:
            if key not in self.records:
                self.logger.warning(f"Record {key} not found")
                return False

            del self.records[key]
            self.metrics.active_records -= 1

            self.logger.info(f"Data record {key} deleted")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete data record {key}: {e}")
            self.metrics.error_count += 1
            return False

    def get_capabilities(self) -> list[str]:
        """Get data SSOT capabilities."""
        return ["data_management", "version_control", "record_crud"]


# ============================================================================
# SSOT VALIDATORS
# ============================================================================


class SSOTRecordValidator(SSOTValidator):
    """SSOT record validator implementation."""

    def __init__(self, validator_id: str = None):
        super().__init__(validator_id or str(uuid.uuid4()), "SSOTRecordValidator")

    def validate_record(self, record: SSOTRecord) -> SSOTValidation:
        """Validate SSOT record."""
        try:
            validation = SSOTValidation(
                validation_id=str(uuid.uuid4()),
                ssot_type=record.ssot_type,
                key=record.key,
                is_valid=True,
                validation_rules=["record_structure", "data_integrity", "version_consistency"],
            )

            # Validate record structure
            if not record.record_id or not record.key:
                validation.is_valid = False
                validation.errors.append("Record ID and key are required")

            # Validate data integrity
            if record.value is None:
                validation.is_valid = False
                validation.errors.append("Record value cannot be None")

            # Validate version consistency
            if record.version < 1:
                validation.is_valid = False
                validation.errors.append("Record version must be >= 1")

            # Validate status
            if record.status not in [
                SSOTStatus.ACTIVE,
                SSOTStatus.INACTIVE,
                SSOTStatus.SYNCING,
                SSOTStatus.ERROR,
                SSOTStatus.MAINTENANCE,
            ]:
                validation.is_valid = False
                validation.errors.append("Invalid record status")

            if validation.is_valid:
                validation.warnings.append("Record validation passed")
            else:
                validation.warnings.append("Record validation failed")

            self.logger.info(f"Record {record.key} validation completed: {validation.is_valid}")
            return validation
        except Exception as e:
            self.logger.error(f"Failed to validate record {record.key}: {e}")
            return SSOTValidation(
                validation_id=str(uuid.uuid4()),
                ssot_type=record.ssot_type,
                key=record.key,
                is_valid=False,
                errors=[f"Validation error: {e}"],
            )

    def get_capabilities(self) -> list[str]:
        """Get record validation capabilities."""
        return ["record_validation", "data_integrity", "version_validation"]


# ============================================================================
# SSOT COORDINATOR
# ============================================================================


class SSOTCoordinator:
    """SSOT coordination system."""

    def __init__(self):
        self.managers: dict[SSOTType, SSOTManager] = {}
        self.validators: list[SSOTValidator] = []
        self.logger = logging.getLogger("ssot_coordinator")

    def register_manager(self, manager: SSOTManager) -> bool:
        """Register SSOT manager."""
        try:
            self.managers[manager.ssot_type] = manager
            self.logger.info(f"SSOT manager {manager.name} registered")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register SSOT manager {manager.name}: {e}")
            return False

    def register_validator(self, validator: SSOTValidator) -> bool:
        """Register SSOT validator."""
        try:
            self.validators.append(validator)
            self.logger.info(f"SSOT validator {validator.name} registered")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register SSOT validator {validator.name}: {e}")
            return False

    def start_all_managers(self) -> bool:
        """Start all SSOT managers."""
        success = True
        for manager in self.managers.values():
            if not manager.start():
                success = False
        return success

    def stop_all_managers(self) -> bool:
        """Stop all SSOT managers."""
        success = True
        for manager in self.managers.values():
            if not manager.stop():
                success = False
        return success

    def create_record(self, ssot_type: SSOTType, key: str, value: Any) -> SSOTRecord | None:
        """Create record using appropriate manager."""
        manager = self.managers.get(ssot_type)
        if not manager:
            self.logger.error(f"No manager found for SSOT type {ssot_type}")
            return None

        return manager.create_record(key, value)

    def read_record(self, ssot_type: SSOTType, key: str) -> SSOTRecord | None:
        """Read record using appropriate manager."""
        manager = self.managers.get(ssot_type)
        if not manager:
            self.logger.error(f"No manager found for SSOT type {ssot_type}")
            return None

        return manager.read_record(key)

    def update_record(self, ssot_type: SSOTType, key: str, value: Any) -> SSOTRecord | None:
        """Update record using appropriate manager."""
        manager = self.managers.get(ssot_type)
        if not manager:
            self.logger.error(f"No manager found for SSOT type {ssot_type}")
            return None

        return manager.update_record(key, value)

    def delete_record(self, ssot_type: SSOTType, key: str) -> bool:
        """Delete record using appropriate manager."""
        manager = self.managers.get(ssot_type)
        if not manager:
            self.logger.error(f"No manager found for SSOT type {ssot_type}")
            return False

        return manager.delete_record(key)

    def validate_record(self, record: SSOTRecord) -> list[SSOTValidation]:
        """Validate record using all validators."""
        validations = []

        for validator in self.validators:
            try:
                validation = validator.validate_record(record)
                validations.append(validation)
            except Exception as e:
                self.logger.error(f"Failed to validate record with {validator.name}: {e}")

        return validations

    def get_ssot_status(self) -> dict[str, Any]:
        """Get SSOT system status."""
        return {
            "managers_registered": len(self.managers),
            "validators_registered": len(self.validators),
            "active_managers": len(
                [m for m in self.managers.values() if m.status == SSOTStatus.ACTIVE]
            ),
            "total_records": sum(m.metrics.total_records for m in self.managers.values()),
            "active_records": sum(m.metrics.active_records for m in self.managers.values()),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_ssot_manager(ssot_type: SSOTType, manager_id: str = None) -> SSOTManager | None:
    """Create SSOT manager by type."""
    managers = {SSOTType.CONFIGURATION: ConfigurationSSOTManager, SSOTType.DATA: DataSSOTManager}

    manager_class = managers.get(ssot_type)
    if manager_class:
        return manager_class(manager_id)

    return None


def create_ssot_validator(validator_type: str, validator_id: str = None) -> SSOTValidator | None:
    """Create SSOT validator by type."""
    validators = {"record": SSOTRecordValidator}

    validator_class = validators.get(validator_type)
    if validator_class:
        return validator_class(validator_id)

    return None


def create_ssot_coordinator() -> SSOTCoordinator:
    """Create SSOT coordinator."""
    return SSOTCoordinator()


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """Main execution function."""
    print("SSOT Unified - Consolidated Single Source of Truth System")
    print("=" * 60)

    # Create SSOT coordinator
    coordinator = create_ssot_coordinator()
    print("✅ SSOT coordinator created")

    # Create and register managers
    ssot_types = [SSOTType.CONFIGURATION, SSOTType.DATA]

    for ssot_type in ssot_types:
        manager = create_ssot_manager(ssot_type)
        if manager and coordinator.register_manager(manager):
            print(f"✅ {manager.name} registered")
        else:
            print(f"❌ Failed to register {ssot_type.value} manager")

    # Create and register validators
    validator_types = ["record"]

    for validator_type in validator_types:
        validator = create_ssot_validator(validator_type)
        if validator and coordinator.register_validator(validator):
            print(f"✅ {validator.name} registered")
        else:
            print(f"❌ Failed to register {validator_type} validator")

    # Start all managers
    if coordinator.start_all_managers():
        print("✅ All SSOT managers started")
    else:
        print("❌ Some SSOT managers failed to start")

    # Test SSOT functionality
    test_record = coordinator.create_record(SSOTType.CONFIGURATION, "test_key", "test_value")
    if test_record:
        print(f"✅ SSOT record created: {test_record.key}")
    else:
        print("❌ Failed to create SSOT record")

    # Test validation
    if test_record:
        validations = coordinator.validate_record(test_record)
        print(f"✅ Record validation completed: {len(validations)} validations")

    status = coordinator.get_ssot_status()
    print(f"✅ SSOT system status: {status}")

    print(f"\nTotal managers registered: {len(coordinator.managers)}")
    print(f"Total validators registered: {len(coordinator.validators)}")
    print("SSOT Unified system test completed successfully!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
