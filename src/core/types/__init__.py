#!/usr/bin/env python3
"""
Unified Type System - V2 Modular Architecture
=============================================

Centralized type definitions for the entire codebase.
Consolidates all duplicate enums and type definitions into a single source of truth.

This module eliminates SSOT violations by providing unified types for:
- Workflow and task management
- Health and performance monitoring
- API and service management
- Validation and error handling
- All other system components

Agent: Agent-8 (Type Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Type Registry

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

# Core type imports - unified from all systems
from .unified_enums import (
    # Workflow and Task Management
    WorkflowStatus,
    TaskStatus,
    TaskPriority,
    TaskType,
    WorkflowType,
    ExecutionStrategy,
    
    # Health and Performance
    HealthLevel,
    AlertType,
    PerformanceLevel,
    BenchmarkType,
    
    # API and Service Management
    ServiceStatus,
    HTTPMethod,
    AuthenticationLevel,
    RateLimitType,
    
    # Validation and Error Handling
    ValidationSeverity,
    ValidationStatus,
    ErrorSeverity,
    ComplianceLevel,
    
    # Communication and Coordination
    MessagePriority,
    MessageStatus,
    CoordinationMode,
    NotificationType,
    
    # System and Infrastructure
    SystemStatus,
    ResourceType,
    SecurityLevel,
    MonitoringType
)

# Type registry for dynamic type resolution
from .type_registry import TypeRegistry

# Type validation and conversion utilities
from .type_utils import (
    validate_type,
    convert_type,
    get_type_info,
    register_custom_type
)

# Export the type registry instance
type_registry = TypeRegistry()

# Version and compliance information
__version__ = "2.0.0"
__author__ = "Agent-8 - Type Systems Consolidation Specialist"
__mission__ = "CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders"
__priority__ = "CRITICAL - Above all other work"
__status__ = "IMPLEMENTATION PHASE 1 - Unified Type Registry"

# Compliance validation
__v2_compliant__ = True
__ssot_compliant__ = True
__consolidation_target__ = "50%+ reduction in duplicate folders"

# Export all types for easy access
__all__ = [
    # Core enums
    "WorkflowStatus",
    "TaskStatus", 
    "TaskPriority",
    "TaskType",
    "WorkflowType",
    "ExecutionStrategy",
    "HealthLevel",
    "AlertType",
    "PerformanceLevel",
    "BenchmarkType",
    "ServiceStatus",
    "HTTPMethod",
    "AuthenticationLevel",
    "RateLimitType",
    "ValidationSeverity",
    "ValidationStatus",
    "ErrorSeverity",
    "ComplianceLevel",
    "MessagePriority",
    "MessageStatus",
    "CoordinationMode",
    "NotificationType",
    "SystemStatus",
    "ResourceType",
    "SecurityLevel",
    "MonitoringType",
    
    # Registry and utilities
    "TypeRegistry",
    "type_registry",
    "validate_type",
    "convert_type",
    "get_type_info",
    "register_custom_type"
]
