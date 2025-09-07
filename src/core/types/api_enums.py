#!/usr/bin/env python3
"""
API and Service Management Enums
================================

Consolidated API and service management enums from scattered locations.
Part of the unified type system consolidation.

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

from enum import Enum
from typing import Dict, List


class ServiceStatus(Enum):
    """Unified service status - consolidated from multiple sources"""
    
    # Core service states
    ACTIVE = "active"
    INACTIVE = "inactive"
    STARTING = "starting"
    STOPPING = "stopping"
    ERROR = "error"
    
    # V2 specific states
    SCALING = "scaling"
    OPTIMIZING = "optimizing"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_service_score(cls) -> Dict[str, float]:
        """Get service scores for statuses"""
        return {
            cls.ACTIVE.value: 1.0,
            cls.STARTING.value: 0.5,
            cls.SCALING.value: 0.7,
            cls.OPTIMIZING.value: 0.8,
            cls.MAINTENANCE.value: 0.0,
            cls.STOPPING.value: 0.2,
            cls.INACTIVE.value: 0.0,
            cls.ERROR.value: 0.0
        }


class APIStatus(Enum):
    """Unified API status - consolidated from multiple sources"""
    
    # Core API states
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"
    
    # V2 specific states
    THROTTLED = "throttled"
    OPTIMIZING = "optimizing"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_api_score(cls) -> Dict[str, float]:
        """Get API scores for statuses"""
        return {
            cls.AVAILABLE.value: 1.0,
            cls.THROTTLED.value: 0.6,
            cls.RATE_LIMITED.value: 0.4,
            cls.OPTIMIZING.value: 0.8,
            cls.MAINTENANCE.value: 0.0,
            cls.UNAVAILABLE.value: 0.0,
            cls.ERROR.value: 0.0
        }


class ConnectionStatus(Enum):
    """Unified connection status - consolidated from multiple sources"""
    
    # Core connection states
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    DISCONNECTING = "disconnecting"
    ERROR = "error"
    
    # V2 specific states
    RECONNECTING = "reconnecting"
    OPTIMIZING = "optimizing"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_connection_score(cls) -> Dict[str, float]:
        """Get connection scores for statuses"""
        return {
            cls.CONNECTED.value: 1.0,
            cls.CONNECTING.value: 0.5,
            cls.RECONNECTING.value: 0.3,
            cls.OPTIMIZING.value: 0.8,
            cls.MAINTENANCE.value: 0.0,
            cls.DISCONNECTING.value: 0.2,
            cls.DISCONNECTED.value: 0.0,
            cls.ERROR.value: 0.0
        }


class AuthenticationStatus(Enum):
    """Unified authentication status - consolidated from multiple sources"""
    
    # Core authentication states
    AUTHENTICATED = "authenticated"
    UNAUTHENTICATED = "unauthenticated"
    AUTHENTICATING = "authenticating"
    ERROR = "error"
    
    # V2 specific states
    REFRESHING = "refreshing"
    EXPIRED = "expired"
    LOCKED = "locked"
    
    @classmethod
    def get_auth_score(cls) -> Dict[str, float]:
        """Get authentication scores for statuses"""
        return {
            cls.AUTHENTICATED.value: 1.0,
            cls.AUTHENTICATING.value: 0.5,
            cls.REFRESHING.value: 0.7,
            cls.EXPIRED.value: 0.0,
            cls.LOCKED.value: 0.0,
            cls.UNAUTHENTICATED.value: 0.0,
            cls.ERROR.value: 0.0
        }
