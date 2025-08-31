#!/usr/bin/env python3
"""
Health and Performance Enums
===========================

Consolidated health and performance enums from scattered locations.
Part of the unified type system consolidation.

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

from enum import Enum
from typing import Dict, List


class HealthStatus(Enum):
    """Unified health status - consolidated from multiple sources"""
    
    # Core health states
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"
    
    # V2 specific states
    OPTIMIZING = "optimizing"
    RECOVERING = "recovering"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_severity_level(cls) -> Dict[str, int]:
        """Get severity levels for health statuses"""
        return {
            cls.HEALTHY.value: 0,
            cls.OPTIMIZING.value: 1,
            cls.WARNING.value: 2,
            cls.DEGRADED.value: 3,
            cls.RECOVERING.value: 4,
            cls.MAINTENANCE.value: 5,
            cls.CRITICAL.value: 6,
            cls.UNKNOWN.value: 7
        }


class PerformanceStatus(Enum):
    """Unified performance status - consolidated from multiple sources"""
    
    # Core performance states
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    CRITICAL = "critical"
    
    # V2 specific states
    OPTIMIZING = "optimizing"
    SCALING = "scaling"
    THROTTLED = "throttled"
    
    @classmethod
    def get_performance_score(cls) -> Dict[str, float]:
        """Get performance scores for statuses"""
        return {
            cls.EXCELLENT.value: 1.0,
            cls.GOOD.value: 0.8,
            cls.AVERAGE.value: 0.6,
            cls.POOR.value: 0.4,
            cls.CRITICAL.value: 0.2,
            cls.OPTIMIZING.value: 0.7,
            cls.SCALING.value: 0.5,
            cls.THROTTLED.value: 0.3
        }


class ResourceStatus(Enum):
    """Unified resource status - consolidated from multiple sources"""
    
    # Core resource states
    AVAILABLE = "available"
    IN_USE = "in_use"
    RESERVED = "reserved"
    UNAVAILABLE = "unavailable"
    ERROR = "error"
    
    # V2 specific states
    SCALING = "scaling"
    OPTIMIZING = "optimizing"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_availability_score(cls) -> Dict[str, float]:
        """Get availability scores for resource statuses"""
        return {
            cls.AVAILABLE.value: 1.0,
            cls.IN_USE.value: 0.5,
            cls.RESERVED.value: 0.0,
            cls.UNAVAILABLE.value: 0.0,
            cls.ERROR.value: 0.0,
            cls.SCALING.value: 0.3,
            cls.OPTIMIZING.value: 0.7,
            cls.MAINTENANCE.value: 0.0
        }


class SystemStatus(Enum):
    """Unified system status - consolidated from multiple sources"""
    
    # Core system states
    ONLINE = "online"
    OFFLINE = "offline"
    STARTING = "starting"
    STOPPING = "stopping"
    ERROR = "error"
    
    # V2 specific states
    INITIALIZING = "initializing"
    RECOVERING = "recovering"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_operational_score(cls) -> Dict[str, float]:
        """Get operational scores for system statuses"""
        return {
            cls.ONLINE.value: 1.0,
            cls.STARTING.value: 0.5,
            cls.INITIALIZING.value: 0.3,
            cls.RECOVERING.value: 0.4,
            cls.MAINTENANCE.value: 0.0,
            cls.STOPPING.value: 0.2,
            cls.OFFLINE.value: 0.0,
            cls.ERROR.value: 0.0
        }
