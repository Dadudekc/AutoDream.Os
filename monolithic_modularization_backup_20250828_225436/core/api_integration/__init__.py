#!/usr/bin/env python3
"""
API Integration Package - V2 Modular Architecture
================================================

Unified API and integration system with modular components.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

# Main unified system
from .unified_api_integration_manager import UnifiedAPIIntegrationManager

# Core types
from .types.api_types import (
    APIVersion, HTTPMethod, ServiceStatus, AuthenticationLevel, RateLimitType,
    ServiceEndpoint, APIRequest, APIResponse, RouteDefinition, RateLimitInfo,
    AuthenticationInfo, ServiceHealth
)

# Modular components
from .gateway.api_gateway_manager import APIGatewayManager
from .middleware.integration_framework_manager import IntegrationFrameworkManager

# Backwards compatibility aliases
APIGateway = UnifiedAPIIntegrationManager
V2APIGateway = UnifiedAPIIntegrationManager
IntegrationFramework = UnifiedAPIIntegrationManager
V2IntegrationFramework = UnifiedAPIIntegrationManager

__all__ = [
    # Main system
    "UnifiedAPIIntegrationManager",
    
    # Core types
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
    "ServiceHealth",
    
    # Modular components
    "APIGatewayManager",
    "IntegrationFrameworkManager",
    
    # Backwards compatibility
    "APIGateway",
    "V2APIGateway",
    "IntegrationFramework",
    "V2IntegrationFramework",
]


