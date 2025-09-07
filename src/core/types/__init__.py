#!/usr/bin/env python3
"""
Unified Type System - Main Entry Point
=====================================

Centralized imports and exports for the unified type system.
Consolidates all enum definitions from scattered locations into a single source of truth.

This module provides:
- Centralized imports for all consolidated enums
- Unified type registry access
- Type utility functions
- Single entry point for all type system functionality

Agent: Agent-8 (Type Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Type Registry

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

# ============================================================================
# WORKFLOW AND TASK MANAGEMENT ENUMS
# ============================================================================

from .workflow_enums import (
    WorkflowStatus,
    TaskStatus,
    WorkflowType,
    TaskType,
    Priority
)

# ============================================================================
# HEALTH AND PERFORMANCE ENUMS
# ============================================================================

from .health_enums import (
    HealthStatus,
    PerformanceStatus,
    ResourceStatus,
    SystemStatus
)

# ============================================================================
# API AND SERVICE MANAGEMENT ENUMS
# ============================================================================

from .api_enums import (
    ServiceStatus,
    APIStatus,
    ConnectionStatus,
    AuthenticationStatus
)

# ============================================================================
# VALIDATION AND COMMUNICATION ENUMS
# ============================================================================

from .validation_enums import (
    ValidationStatus,
    MessageStatus,
    CommunicationStatus,
    ErrorLevel
)

# ============================================================================
# SECURITY AND CONSOLIDATION ENUMS
# ============================================================================

from .security_enums import (
    SecurityStatus,
    MonitoringStatus,
    ConsolidationStatus,
    MigrationStatus
)

# ============================================================================
# TYPE REGISTRY AND UTILITIES
# ============================================================================

from .type_registry import TypeRegistry
from .type_utils import (
    validate_type,
    convert_type,
    get_type_info,
    register_custom_type
)

# ============================================================================
# UNIFIED TYPE REGISTRY INSTANCE
# ============================================================================

# Create unified type registry instance
type_registry = TypeRegistry()

# Register all consolidated enums
type_registry.register_type("WorkflowStatus", WorkflowStatus, "Workflow execution status")
type_registry.register_type("TaskStatus", TaskStatus, "Task execution status")
type_registry.register_type("WorkflowType", WorkflowType, "Workflow type definitions")
type_registry.register_type("TaskType", TaskType, "Task type definitions")
type_registry.register_type("Priority", Priority, "Priority levels")

type_registry.register_type("HealthStatus", HealthStatus, "Health status")
type_registry.register_type("PerformanceStatus", PerformanceStatus, "Performance status")
type_registry.register_type("ResourceStatus", ResourceStatus, "Resource status")
type_registry.register_type("SystemStatus", SystemStatus, "System status")

type_registry.register_type("ServiceStatus", ServiceStatus, "Service status")
type_registry.register_type("APIStatus", APIStatus, "API status")
type_registry.register_type("ConnectionStatus", ConnectionStatus, "Connection status")
type_registry.register_type("AuthenticationStatus", AuthenticationStatus, "Authentication status")

type_registry.register_type("ValidationStatus", ValidationStatus, "Validation status")
type_registry.register_type("MessageStatus", MessageStatus, "Message status")
type_registry.register_type("CommunicationStatus", CommunicationStatus, "Communication status")
type_registry.register_type("ErrorLevel", ErrorLevel, "Error levels")

type_registry.register_type("SecurityStatus", SecurityStatus, "Security status")
type_registry.register_type("MonitoringStatus", MonitoringStatus, "Monitoring status")
type_registry.register_type("ConsolidationStatus", ConsolidationStatus, "Consolidation status")
type_registry.register_type("MigrationStatus", MigrationStatus, "Migration status")

# ============================================================================
# PUBLIC API EXPORTS
# ============================================================================

__all__ = [
    # Workflow and Task Management
    "WorkflowStatus",
    "TaskStatus", 
    "WorkflowType",
    "TaskType",
    "Priority",
    
    # Health and Performance
    "HealthStatus",
    "PerformanceStatus",
    "ResourceStatus", 
    "SystemStatus",
    
    # API and Service Management
    "ServiceStatus",
    "APIStatus",
    "ConnectionStatus",
    "AuthenticationStatus",
    
    # Validation and Communication
    "ValidationStatus",
    "MessageStatus",
    "CommunicationStatus",
    "ErrorLevel",
    
    # Security and Consolidation
    "SecurityStatus",
    "MonitoringStatus",
    "ConsolidationStatus",
    "MigrationStatus",
    
    # Type Registry and Utilities
    "TypeRegistry",
    "type_registry",
    "validate_type",
    "convert_type",
    "get_type_info",
    "register_custom_type"
]
