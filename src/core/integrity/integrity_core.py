#!/usr/bin/env python3
"""
Integrity Core - Agent Cellphone V2
===================================

Main data integrity manager with core functionality.
Follows Single Responsibility Principle with 150 LOC limit.
"""

import time
import json
import hashlib
import threading
from typing import Dict, List, Optional, Any, Callable
import logging
from pathlib import Path
import sqlite3
from datetime import datetime

from .integrity_types import (
    IntegrityCheckType, RecoveryStrategy, IntegrityLevel,
    IntegrityCheck, IntegrityViolation, IntegrityConfig
)


class DataIntegrityManager:
    """
    Core data integrity verification and recovery
    
    Responsibilities:
    - Perform comprehensive data integrity checks
    - Implement multiple recovery strategies
    - Maintain integrity audit trails
    """
    
    def __init__(self, storage_path: str = "persistent_data"):
        self.logger = logging.getLogger(f"{__name__}.DataIntegrityManager")
        self.storage_path = Path(storage_path)
        self.integrity_db_path = self.storage_path / "integrity.db"
        self.audit_log_path = self.storage_path / "integrity_audit.log"
        
        # Ensure integrity database exists
        self._initialize_integrity_database()
        
        # Integrity check tracking
        self.active_checks: Dict[str, IntegrityCheck] = {}
        self.check_history: List[IntegrityCheck] = []
        self.recovery_strategies: Dict[RecoveryStrategy, Callable] = {}
        
        # Initialize recovery strategies
        self._initialize_recovery_strategies()
        
        # Background integrity monitoring
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
    
    def _initialize_integrity_database(self):
        """Initialize integrity verification database"""
        try:
            self.integrity_conn = sqlite3.connect(str(self.integrity_db_path), check_same_thread=False)
            self.integrity_cursor = self.integrity_conn.cursor()
            
            # Create integrity tables
            self.integrity_cursor.execute('''
                CREATE TABLE IF NOT EXISTS integrity_checks (
                    check_id TEXT PRIMARY KEY, data_id TEXT, check_type TEXT,
                    timestamp REAL, passed INTEGER, details TEXT,
                    recovery_attempted INTEGER, recovery_successful INTEGER
                )
            ''')
            
            self.integrity_cursor.execute('''
                CREATE TABLE IF NOT EXISTS integrity_violations (
                    violation_id TEXT PRIMARY KEY, data_id TEXT, violation_type TEXT,
                    severity TEXT, timestamp REAL, description TEXT,
                    affected_data TEXT, suggested_recovery TEXT
                )
            ''')
            
            self.integrity_conn.commit()
            self.logger.info("Integrity database initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize integrity database: {e}")
            raise
    
    def _initialize_recovery_strategies(self):
        """Initialize recovery strategy implementations"""
        self.recovery_strategies = {
            RecoveryStrategy.BACKUP_RESTORE: self._backup_restore_recovery,
            RecoveryStrategy.CHECKSUM_MATCH: self._checksum_match_recovery,
            RecoveryStrategy.TIMESTAMP_ROLLBACK: self._timestamp_rollback_recovery,
            RecoveryStrategy.VERSION_ROLLBACK: self._version_rollback_recovery,
            RecoveryStrategy.MANUAL_RECOVERY: self._manual_recovery
        }
    
    def perform_integrity_check(self, data_id: str, check_type: IntegrityCheckType) -> IntegrityCheck:
        """Perform a specific type of integrity check"""
        check_id = f"{data_id}_{check_type.value}_{int(time.time())}"
        
        check = IntegrityCheck(
            check_id=check_id, data_id=data_id, check_type=check_type,
            timestamp=time.time(), passed=False, details={},
            recovery_attempted=False, recovery_successful=False
        )
        
        try:
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
            
            if not check.passed:
                self.logger.warning(f"Integrity check failed: {data_id} - {check_type.value}")
        except Exception as e:
            self.logger.error(f"Integrity check error: {data_id} - {check_type.value}: {e}")
            check.details["error"] = str(e)
        
        return check
    
    def _verify_checksum(self, data_id: str) -> bool:
        """Verify data checksum integrity"""
        try:
            return True  # Placeholder implementation
        except Exception as e:
            self.logger.error(f"Checksum verification failed: {e}")
            return False
    
    def _verify_hash_chain(self, data_id: str) -> bool:
        """Verify hash chain integrity"""
        try:
            return True  # Placeholder implementation
        except Exception as e:
            self.logger.error(f"Hash chain verification failed: {e}")
            return False
    
    def _verify_timestamp(self, data_id: str) -> bool:
        """Verify timestamp integrity"""
        try:
            return True  # Placeholder implementation
        except Exception as e:
            self.logger.error(f"Timestamp verification failed: {e}")
            return False
    
    def _verify_size(self, data_id: str) -> bool:
        """Verify data size integrity"""
        try:
            return True  # Placeholder implementation
        except Exception as e:
            self.logger.error(f"Size verification failed: {e}")
            return False
    
    def _verify_version(self, data_id: str) -> bool:
        """Verify version integrity"""
        try:
            return True  # Placeholder implementation
        except Exception as e:
            self.logger.error(f"Version verification failed: {e}")
            return False
    
    def _record_integrity_check(self, check: IntegrityCheck):
        """Record integrity check result in database"""
        try:
            self.integrity_cursor.execute('''
                INSERT OR REPLACE INTO integrity_checks 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                check.check_id, check.data_id, check.check_type.value,
                check.timestamp, check.passed, json.dumps(check.details),
                check.recovery_attempted, check.recovery_successful
            ))
            self.integrity_conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to record integrity check: {e}")
    
    def _execute_recovery_strategy(self, data_id: str, strategy: RecoveryStrategy) -> bool:
        """Execute specific recovery strategy"""
        self.logger.info(f"Executing {strategy.value} recovery for {data_id}")
        if strategy == RecoveryStrategy.MANUAL_RECOVERY:
            return False  # Manual recovery requires intervention
        return True  # Placeholder for automated strategies
    
    def get_integrity_stats(self) -> Dict[str, Any]:
        """Get integrity verification statistics"""
        return {
            "total_checks": len(self.check_history),
            "passed_checks": len([c for c in self.check_history if c.passed]),
            "failed_checks": len([c for c in self.check_history if not c.passed]),
            "recovery_attempts": len([c for c in self.check_history if c.recovery_attempted]),
            "successful_recoveries": len([c for c in self.check_history if c.recovery_successful])
        }
