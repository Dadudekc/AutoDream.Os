#!/usr/bin/env python3
"""
Security and Consolidation Enums
================================

Consolidated security and consolidation enums from scattered locations.
Part of the unified type system consolidation.

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

from enum import Enum
from typing import Dict, List


class SecurityStatus(Enum):
    """Unified security status - consolidated from multiple sources"""
    
    # Core security states
    SECURE = "secure"
    VULNERABLE = "vulnerable"
    COMPROMISED = "compromised"
    UNKNOWN = "unknown"
    
    # V2 specific states
    SCANNING = "scanning"
    UPDATING = "updating"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_security_score(cls) -> Dict[str, float]:
        """Get security scores for statuses"""
        return {
            cls.SECURE.value: 1.0,
            cls.SCANNING.value: 0.7,
            cls.UPDATING.value: 0.8,
            cls.MAINTENANCE.value: 0.5,
            cls.VULNERABLE.value: 0.3,
            cls.COMPROMISED.value: 0.0,
            cls.UNKNOWN.value: 0.5
        }


class MonitoringStatus(Enum):
    """Unified monitoring status - consolidated from multiple sources"""
    
    # Core monitoring states
    MONITORING = "monitoring"
    ALERTING = "alerting"
    SILENT = "silent"
    ERROR = "error"
    
    # V2 specific states
    OPTIMIZING = "optimizing"
    SCALING = "scaling"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_monitoring_score(cls) -> Dict[str, float]:
        """Get monitoring scores for statuses"""
        return {
            cls.MONITORING.value: 1.0,
            cls.OPTIMIZING.value: 0.8,
            cls.SCALING.value: 0.7,
            cls.ALERTING.value: 0.5,
            cls.MAINTENANCE.value: 0.3,
            cls.SILENT.value: 0.0,
            cls.ERROR.value: 0.0
        }


class ConsolidationStatus(Enum):
    """Unified consolidation status - consolidated from multiple sources"""
    
    # Core consolidation states
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    
    # V2 specific states
    VALIDATING = "validating"
    OPTIMIZING = "optimizing"
    DEPLOYING = "deploying"
    
    @classmethod
    def get_consolidation_score(cls) -> Dict[str, float]:
        """Get consolidation scores for statuses"""
        return {
            cls.COMPLETED.value: 1.0,
            cls.DEPLOYING.value: 0.9,
            cls.OPTIMIZING.value: 0.7,
            cls.VALIDATING.value: 0.5,
            cls.IN_PROGRESS.value: 0.3,
            cls.PENDING.value: 0.0,
            cls.FAILED.value: 0.0
        }


class MigrationStatus(Enum):
    """Unified migration status - consolidated from multiple sources"""
    
    # Core migration states
    PENDING = "pending"
    MIGRATING = "migrating"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    
    # V2 specific states
    VALIDATING = "validating"
    OPTIMIZING = "optimizing"
    DEPLOYING = "deploying"
    
    @classmethod
    def get_migration_score(cls) -> Dict[str, float]:
        """Get migration scores for statuses"""
        return {
            cls.COMPLETED.value: 1.0,
            cls.DEPLOYING.value: 0.9,
            cls.OPTIMIZING.value: 0.7,
            cls.VALIDATING.value: 0.5,
            cls.MIGRATING.value: 0.3,
            cls.PENDING.value: 0.0,
            cls.FAILED.value: 0.0,
            cls.ROLLED_BACK.value: 0.0
        }
