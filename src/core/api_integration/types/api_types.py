#!/usr/bin/env python3
"""
API Types - V2 Modular Architecture
===================================

Core data structures for unified API and integration system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum


class APIVersion(Enum):
    """API version enumeration"""
    V1 = "v1"
    V2 = "v2"
    BETA = "beta"
    ALPHA = "alpha"


class HTTPMethod(Enum):
    """HTTP method enumeration"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class ServiceStatus(Enum):
    """Service status values"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    OFFLINE = "offline"
    ERROR = "error"


class AuthenticationLevel(Enum):
    """Authentication level enumeration"""
    NONE = "none"
    BASIC = "basic"
    TOKEN = "token"
    JWT = "jwt"
    OAUTH = "oauth"
    API_KEY = "api_key"


class RateLimitType(Enum):
    """Rate limiting type enumeration"""
    NONE = "none"
    PER_SECOND = "per_second"
    PER_MINUTE = "per_minute"
    PER_HOUR = "per_hour"
    PER_DAY = "per_day"


@dataclass
class ServiceEndpoint:
    """Service endpoint information"""
    service_id: str
    name: str
    version: str
    base_url: str
    health_check_url: Optional[str] = None
    status: ServiceStatus = ServiceStatus.UNKNOWN
    last_health_check: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    authentication_required: bool = False
    rate_limit: Optional[int] = None
    timeout: float = 30.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "service_id": self.service_id,
            "name": self.name,
            "version": self.version,
            "base_url": self.base_url,
            "health_check_url": self.health_check_url,
            "status": self.status.value,
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None,
            "metadata": self.metadata,
            "authentication_required": self.authentication_required,
            "rate_limit": self.rate_limit,
            "timeout": self.timeout
        }


@dataclass
class APIRequest:
    """API request structure"""
    request_id: str
    method: HTTPMethod
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    body: Optional[Any] = None
    timestamp: datetime = field(default_factory=datetime.now)
    client_ip: str = ""
    user_agent: str = ""
    authentication_token: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "request_id": self.request_id,
            "method": self.method.value,
            "path": self.path,
            "headers": self.headers,
            "query_params": self.query_params,
            "body": self.body,
            "timestamp": self.timestamp.isoformat(),
            "client_ip": self.client_ip,
            "user_agent": self.user_agent,
            "authentication_token": self.authentication_token
        }


@dataclass
class APIResponse:
    """API response structure"""
    request_id: str
    status_code: int
    headers: Dict[str, str]
    body: Any
    timestamp: datetime = field(default_factory=datetime.now)
    processing_time: float = 0.0
    service_id: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "request_id": self.request_id,
            "status_code": self.status_code,
            "headers": self.headers,
            "body": self.body,
            "timestamp": self.timestamp.isoformat(),
            "processing_time": self.processing_time,
            "service_id": self.service_id,
            "error_message": self.error_message
        }


@dataclass
class RouteDefinition:
    """Route definition and configuration"""
    path: str
    method: HTTPMethod
    service_id: str
    handler: Callable
    requires_auth: bool = False
    auth_level: AuthenticationLevel = AuthenticationLevel.NONE
    rate_limit: Optional[int] = None
    rate_limit_type: RateLimitType = RateLimitType.PER_MINUTE
    timeout: float = 30.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "path": self.path,
            "method": self.method.value,
            "service_id": self.service_id,
            "requires_auth": self.requires_auth,
            "auth_level": self.auth_level.value,
            "rate_limit": self.rate_limit,
            "rate_limit_type": self.rate_limit_type.value,
            "timeout": self.timeout,
            "metadata": self.metadata
        }


@dataclass
class MiddlewareConfig:
    """Middleware configuration"""
    name: str
    enabled: bool = True
    priority: int = 100
    config: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "priority": self.priority,
            "config": self.config
        }


@dataclass
class RateLimitInfo:
    """Rate limiting information"""
    service_id: str
    limit_type: RateLimitType
    limit_value: int
    current_count: int = 0
    reset_time: Optional[datetime] = None
    window_start: Optional[datetime] = None
    
    def is_exceeded(self) -> bool:
        """Check if rate limit is exceeded"""
        return self.current_count >= self.limit_value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "service_id": self.service_id,
            "limit_type": self.limit_type.value,
            "limit_value": self.limit_value,
            "current_count": self.current_count,
            "reset_time": self.reset_time.isoformat() if self.reset_time else None,
            "window_start": self.window_start.isoformat() if self.window_start else None
        }


@dataclass
class AuthenticationInfo:
    """Authentication information"""
    user_id: Optional[str] = None
    username: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    token_expiry: Optional[datetime] = None
    auth_level: AuthenticationLevel = AuthenticationLevel.NONE
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_valid(self) -> bool:
        """Check if authentication is valid"""
        if self.token_expiry:
            return datetime.now() < self.token_expiry
        return self.auth_level != AuthenticationLevel.NONE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "roles": self.roles,
            "permissions": self.permissions,
            "token_expiry": self.token_expiry.isoformat() if self.token_expiry else None,
            "auth_level": self.auth_level.value,
            "metadata": self.metadata
        }


@dataclass
class ServiceHealth:
    """Service health information"""
    service_id: str
    status: ServiceStatus
    response_time: float
    last_check: datetime
    error_count: int = 0
    success_count: int = 0
    uptime_percentage: float = 100.0
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "service_id": self.service_id,
            "status": self.status.value,
            "response_time": self.response_time,
            "last_check": self.last_check.isoformat(),
            "error_count": self.error_count,
            "success_count": self.success_count,
            "uptime_percentage": self.uptime_percentage,
            "details": self.details
        }

