#!/usr/bin/env python3
"""
Validation and Communication Enums
==================================

Consolidated validation and communication enums from scattered locations.
Part of the unified type system consolidation.

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

from enum import Enum
from typing import Dict, List


class ValidationStatus(Enum):
    """Unified validation status - consolidated from multiple sources"""
    
    # Core validation states
    VALID = "valid"
    INVALID = "invalid"
    VALIDATING = "validating"
    ERROR = "error"
    
    # V2 specific states
    PENDING = "pending"
    WARNING = "warning"
    CRITICAL = "critical"
    
    @classmethod
    def get_validation_score(cls) -> Dict[str, float]:
        """Get validation scores for statuses"""
        return {
            cls.VALID.value: 1.0,
            cls.VALIDATING.value: 0.5,
            cls.PENDING.value: 0.3,
            cls.WARNING.value: 0.7,
            cls.CRITICAL.value: 0.0,
            cls.INVALID.value: 0.0,
            cls.ERROR.value: 0.0
        }


class MessageStatus(Enum):
    """Unified message status - consolidated from multiple sources"""
    
    # Core message states
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    PENDING = "pending"
    
    # V2 specific states
    PROCESSING = "processing"
    QUEUED = "queued"
    RETRYING = "retrying"
    
    @classmethod
    def get_message_score(cls) -> Dict[str, float]:
        """Get message scores for statuses"""
        return {
            cls.READ.value: 1.0,
            cls.DELIVERED.value: 0.8,
            cls.SENT.value: 0.6,
            cls.PROCESSING.value: 0.5,
            cls.QUEUED.value: 0.3,
            cls.RETRYING.value: 0.4,
            cls.PENDING.value: 0.2,
            cls.FAILED.value: 0.0
        }


class CommunicationStatus(Enum):
    """Unified communication status - consolidated from multiple sources"""
    
    # Core communication states
    ACTIVE = "active"
    INACTIVE = "inactive"
    CONNECTING = "connecting"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    
    # V2 specific states
    OPTIMIZING = "optimizing"
    SCALING = "scaling"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_communication_score(cls) -> Dict[str, float]:
        """Get communication scores for statuses"""
        return {
            cls.ACTIVE.value: 1.0,
            cls.CONNECTING.value: 0.5,
            cls.OPTIMIZING.value: 0.8,
            cls.SCALING.value: 0.7,
            cls.MAINTENANCE.value: 0.0,
            cls.INACTIVE.value: 0.0,
            cls.DISCONNECTED.value: 0.0,
            cls.ERROR.value: 0.0
        }


class ErrorLevel(Enum):
    """Unified error levels - consolidated from multiple sources"""
    
    # Core error levels
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    
    # V2 specific levels
    TRACE = "trace"
    FATAL = "fatal"
    
    @classmethod
    def get_error_severity(cls) -> Dict[str, int]:
        """Get error severity levels"""
        return {
            cls.TRACE.value: 0,
            cls.DEBUG.value: 1,
            cls.INFO.value: 2,
            cls.WARNING.value: 3,
            cls.ERROR.value: 4,
            cls.CRITICAL.value: 5,
            cls.FATAL.value: 6
        }
