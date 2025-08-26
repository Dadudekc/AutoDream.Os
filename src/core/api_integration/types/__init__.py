#!/usr/bin/env python3
"""
API Types Package - V2 Modular Architecture
==========================================

Core data structures for unified API and integration system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .api_types import (
    APIVersion,
    HTTPMethod,
    ServiceStatus,
    AuthenticationLevel,
    RateLimitType,
    ServiceEndpoint,
    APIRequest,
    APIResponse,
    RouteDefinition,
    RateLimitInfo,
    AuthenticationInfo,
    ServiceHealth
)

__all__ = [
    "APIVersion",
    "HTTPMethod",
    "ServiceStatus",
    "AuthenticationLevel",
    "RateLimitType",
    "ServiceEndpoint",
    "APIRequest",
    "APIResponse",
    "RouteDefinition",
    "RateLimitInfo",
    "AuthenticationInfo",
    "ServiceHealth"
]

