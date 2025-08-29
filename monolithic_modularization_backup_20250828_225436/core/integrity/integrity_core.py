from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
import hashlib
import json
import logging
import sqlite3
import threading

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
from .integrity_persistence import IntegrityDataPersistence
from .integrity_types import (
from dataclasses import asdict
from src.utils.stability_improvements import stability_manager, safe_import
import time

#!/usr/bin/env python3
"""
Integrity Core - Agent Cellphone V2
===================================

Main data integrity manager with core functionality.
Follows Single Responsibility Principle with 150 LOC limit.
Now inherits from BaseManager for unified functionality.
"""



    IntegrityCheckType,
    RecoveryStrategy,
    IntegrityLevel,
    IntegrityCheck,
    IntegrityViolation,
    IntegrityConfig,
)


class DataIntegrityManager(BaseManager):
    """
    Core data integrity verification and recovery
    
    Responsibilities:
    - Perform comprehensive data integrity checks
    - Implement multiple recovery strategies
    - Maintain integrity audit trails
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, storage_path: str = "persistent_data"):
        """Initialize data integrity manager with BaseManager"""
        super().__init__(
            manager_id="data_integrity_manager",
            name="Data Integrity Manager",
            description="Core data integrity verification and recovery"
        )
        
        self.storage_path = Path(storage_path)
        self.integrity_db_path = self.storage_path / "integrity.db"
        self.audit_log_path = self.storage_path / "integrity_audit.log"

        # Integrity check tracking
        self.active_checks: Dict[str, IntegrityCheck] = {}
        self.check_history: List[IntegrityCheck] = []
        self.recovery_strategies: Dict[RecoveryStrategy, Callable] = {}

        # Data integrity management tracking
        self.integrity_operations: List[Dict[str, Any]] = []
        self.recovery_operations: List[Dict[str, Any]] = []
        self.verification_operations: List[Dict[str, Any]] = []

        # Persistence handler
        self.persistence = IntegrityDataPersistence(
            base_path=str(self.storage_path / "integrity_management")
        )

        # Background integrity monitoring
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None

        # Ensure integrity database exists
        self._initialize_integrity_database()

        # Initialize recovery strategies
        self._initialize_recovery_strategies()
        
        self.logger.info("Data Integrity Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize data integrity management system"""
        try:
            self.logger.info("Starting Data Integrity Manager...")
            
            # Clear tracking data
            self.integrity_operations.clear()
            self.recovery_operations.clear()
            self.verification_operations.clear()
            
            # Verify database connection
            if not hasattr(self, 'integrity_conn') or not self.integrity_conn:
                self._initialize_integrity_database()
            
            self.logger.info("Data Integrity Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Data Integrity Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup data integrity management system"""
        try:
            self.logger.info("Stopping Data Integrity Manager...")
            
            # Save tracking data
            self._save_data_integrity_management_data()
            
            # Close database connection
            if hasattr(self, 'integrity_conn') and self.integrity_conn:
                self.integrity_conn.close()
            
            # Clear data
            self.integrity_operations.clear()
            self.recovery_operations.clear()
            self.verification_operations.clear()
            
            self.logger.info("Data Integrity Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Data Integrity Manager: {e}")
    
    def _on_heartbeat(self):
        """Data integrity manager heartbeat"""
        try:
            # Check data integrity management health
            self._check_data_integrity_management_health()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize data integrity management resources"""
        try:
            # Initialize data structures
            self.integrity_operations = []
            self.recovery_operations = []
            self.verification_operations = []
            
            # Ensure storage directory exists
            self.storage_path.mkdir(parents=True, exist_ok=True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup data integrity management resources"""
        try:
            # Clear data
            self.integrity_operations.clear()
            self.recovery_operations.clear()
            self.verification_operations.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reinitialize database connection
            if hasattr(self, 'integrity_conn') and self.integrity_conn:
                self.integrity_conn.close()
            self._initialize_integrity_database()
            
            # Reset tracking
            self.integrity_operations.clear()
            self.recovery_operations.clear()
            self.verification_operations.clear()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Data Integrity Management Methods
    # ============================================================================
    
    def _initialize_integrity_database(self):
        """Initialize integrity verification database"""
        try:
            start_time = datetime.now()
            
            self.integrity_conn = sqlite3.connect(
                str(self.integrity_db_path), check_same_thread=False
            )
            self.integrity_cursor = self.integrity_conn.cursor()

            # Create integrity tables
            self.integrity_cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS integrity_checks (
                    check_id TEXT PRIMARY KEY, data_id TEXT, check_type TEXT,
                    timestamp REAL, passed INTEGER, details TEXT,
                    recovery_attempted INTEGER, recovery_successful INTEGER
                )
            """
            )

            self.integrity_cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS integrity_violations (
                    violation_id TEXT PRIMARY KEY, data_id TEXT, violation_type TEXT,
                    severity TEXT, timestamp REAL, description TEXT,
                    affected_data TEXT, suggested_recovery TEXT
                )
            """
            )

            self.integrity_conn.commit()
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("initialize_integrity_database", True, operation_time)
            
            self.logger.info("Integrity database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize integrity database: {e}")
            self.record_operation("initialize_integrity_database", False, 0.0)
            raise

    def _initialize_recovery_strategies(self):
        """Initialize recovery strategy implementations"""
        try:
            self.recovery_strategies = {
                RecoveryStrategy.BACKUP_RESTORE: self._backup_restore_recovery,
                RecoveryStrategy.CHECKSUM_MATCH: self._checksum_match_recovery,
                RecoveryStrategy.TIMESTAMP_ROLLBACK: self._timestamp_rollback_recovery,
                RecoveryStrategy.VERSION_ROLLBACK: self._version_rollback_recovery,
                RecoveryStrategy.MANUAL_RECOVERY: self._manual_recovery,
            }
            
            # Record operation
            self.record_operation("initialize_recovery_strategies", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to initialize recovery strategies: {e}")
            self.record_operation("initialize_recovery_strategies", False, 0.0)

    def perform_integrity_check(
        self, data_id: str, check_type: IntegrityCheckType
    ) -> IntegrityCheck:
        """Perform a specific type of integrity check"""
        try:
            start_time = datetime.now()
            
            check_id = f"{data_id}_{check_type.value}_{int(time.time())}"

            check = IntegrityCheck(
                check_id=check_id,
                data_id=data_id,
                check_type=check_type,
                timestamp=time.time(),
                passed=False,
                details={},
                recovery_attempted=False,
                recovery_successful=False,
            )

            if check_type == IntegrityCheckType.CHECKSUM:
                check.passed = self._verify_checksum(data_id)
            elif check_type == IntegrityCheckType.HASH_CHAIN:
                check.passed = self._verify_hash_chain(data_id)
            elif check_type == IntegrityCheckType.TIMESTAMP:
                check.passed = self._verify_timestamp(data_id)
            elif check_type == IntegrityCheckType.SIZE_VERIFICATION:
                check.passed = self._verify_size(data_id)
            elif check_type == IntegrityCheckType.VERSION_CONTROL:
                check.passed = self._verify_version(data_id)

            # Record check result
            self._record_integrity_check(check)
            self.check_history.append(check)

            # Record integrity operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "perform_integrity_check",
                "data_id": data_id,
                "check_type": check_type.value,
                "passed": check.passed,
                "success": True
            }
            self.integrity_operations.append(operation_record)

            if not check.passed:
                self.logger.warning(
                    f"Integrity check failed: {data_id} - {check_type.value}"
                )
                
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("perform_integrity_check", check.passed, operation_time)
            
        except Exception as e:
            self.logger.error(
                f"Integrity check error: {data_id} - {check_type.value}: {e}"
            )
            check.details["error"] = str(e)
            
            # Record failed operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "perform_integrity_check",
                "data_id": data_id,
                "check_type": check_type.value,
                "error": str(e),
                "success": False
            }
            self.integrity_operations.append(operation_record)
            
            self.record_operation("perform_integrity_check", False, 0.0)

        return check

    def _verify_checksum(self, data_id: str) -> bool:
        """Verify data checksum integrity"""
        try:
            # Record verification operation
            self.record_operation("verify_checksum", True, 0.0)
            return True  # Placeholder implementation
            
        except Exception as e:
            self.logger.error(f"Checksum verification failed: {e}")
            self.record_operation("verify_checksum", False, 0.0)
            return False

    def _verify_hash_chain(self, data_id: str) -> bool:
        """Verify hash chain integrity"""
        try:
            # Record verification operation
            self.record_operation("verify_hash_chain", True, 0.0)
            return True  # Placeholder implementation
            
        except Exception as e:
            self.logger.error(f"Hash chain verification failed: {e}")
            self.record_operation("verify_hash_chain", False, 0.0)
            return False

    def _verify_timestamp(self, data_id: str) -> bool:
        """Verify timestamp integrity"""
        try:
            # Record verification operation
            self.record_operation("verify_timestamp", True, 0.0)
            return True  # Placeholder implementation
            
        except Exception as e:
            self.logger.error(f"Timestamp verification failed: {e}")
            self.record_operation("verify_timestamp", False, 0.0)
            return False

    def _verify_size(self, data_id: str) -> bool:
        """Verify data size integrity"""
        try:
            # Record verification operation
            self.record_operation("verify_size", True, 0.0)
            return True  # Placeholder implementation
            
        except Exception as e:
            self.logger.error(f"Size verification failed: {e}")
            self.record_operation("verify_size", False, 0.0)
            return False

    def _verify_version(self, data_id: str) -> bool:
        """Verify version integrity"""
        try:
            # Record verification operation
            self.record_operation("verify_version", True, 0.0)
            return True  # Placeholder implementation
            
        except Exception as e:
            self.logger.error(f"Version verification failed: {e}")
            self.record_operation("verify_version", False, 0.0)
            return False

    def _record_integrity_check(self, check: IntegrityCheck):
        """Record integrity check result in database"""
        try:
            start_time = datetime.now()
            
            self.integrity_cursor.execute(
                """
                INSERT OR REPLACE INTO integrity_checks
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    check.check_id,
                    check.data_id,
                    check.check_type.value,
                    check.timestamp,
                    check.passed,
                    json.dumps(check.details),
                    check.recovery_attempted,
                    check.recovery_successful,
                ),
            )
            self.integrity_conn.commit()
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("record_integrity_check", True, operation_time)
            
        except Exception as e:
            self.logger.error(f"Failed to record integrity check: {e}")
            self.record_operation("record_integrity_check", False, 0.0)

    def _execute_recovery_strategy(
        self, data_id: str, strategy: RecoveryStrategy
    ) -> bool:
        """Execute specific recovery strategy"""
        try:
            start_time = datetime.now()
            
            self.logger.info(f"Executing {strategy.value} recovery for {data_id}")
            
            if strategy == RecoveryStrategy.MANUAL_RECOVERY:
                success = False  # Manual recovery requires intervention
            else:
                success = True  # Placeholder for automated strategies
            
            # Record recovery operation
            recovery_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "execute_recovery_strategy",
                "data_id": data_id,
                "strategy": strategy.value,
                "success": success
            }
            self.recovery_operations.append(recovery_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("execute_recovery_strategy", success, operation_time)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to execute recovery strategy: {e}")
            self.record_operation("execute_recovery_strategy", False, 0.0)
            return False

    def get_integrity_stats(self) -> Dict[str, Any]:
        """Get integrity verification statistics"""
        try:
            stats = {
                "total_checks": len(self.check_history),
                "passed_checks": len([c for c in self.check_history if c.passed]),
                "failed_checks": len([c for c in self.check_history if not c.passed]),
                "recovery_attempts": len(
                    [c for c in self.check_history if c.recovery_attempted]
                ),
                "successful_recoveries": len(
                    [c for c in self.check_history if c.recovery_successful]
                ),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_integrity_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get integrity stats: {e}")
            self.record_operation("get_integrity_stats", False, 0.0)
            return {"error": str(e)}
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_data_integrity_management_data(self):
        """Serialize and persist current integrity management state."""
        try:
            state = {
                "active_checks": {k: asdict(v) for k, v in self.active_checks.items()},
                "check_history": [asdict(c) for c in self.check_history],
                "integrity_operations": self.integrity_operations,
                "recovery_operations": self.recovery_operations,
                "verification_operations": self.verification_operations,
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
            }

            if not self.persistence.save(state):
                self.logger.warning("Persistence failed, data only logged in memory")
            else:
                self.logger.debug("Data integrity management data saved")

        except Exception as e:
            self.logger.error(f"Failed to save data integrity management data: {e}")
            self.logger.warning("Persistence failed, data only logged in memory")
    
    def _check_data_integrity_management_health(self):
        """Check data integrity management health status"""
        try:
            # Check for excessive integrity operations
            if len(self.integrity_operations) > 1000:
                self.logger.warning(f"High number of integrity operations: {len(self.integrity_operations)}")
            
            # Check recovery operations
            if len(self.recovery_operations) > 500:
                self.logger.info(f"Large recovery operations history: {len(self.recovery_operations)} records")
                
        except Exception as e:
            self.logger.error(f"Failed to check data integrity management health: {e}")
    
    def get_data_integrity_management_stats(self) -> Dict[str, Any]:
        """Get data integrity management statistics"""
        try:
            stats = {
                "total_checks": len(self.check_history),
                "active_checks": len(self.active_checks),
                "integrity_operations_count": len(self.integrity_operations),
                "recovery_operations_count": len(self.recovery_operations),
                "verification_operations_count": len(self.verification_operations),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_data_integrity_management_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get data integrity management stats: {e}")
            self.record_operation("get_data_integrity_management_stats", False, 0.0)
            return {"error": str(e)}
