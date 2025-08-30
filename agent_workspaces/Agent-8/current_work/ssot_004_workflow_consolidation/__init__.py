#!/usr/bin/env python3
"""
Unified Workflow Engine Package - SSOT-004 Implementation

This package provides a unified workflow engine that consolidates all workflow
functionality into a single source of truth, eliminating SSOT violations.

Author: Agent-8 (Integration Enhancement Optimization Manager)
Contract: SSOT-004: Workflow & Reporting System Consolidation
License: MIT
"""

from .unified_workflow_engine import UnifiedWorkflowEngine, create_unified_workflow_engine
from .workflow_core import WorkflowCore
from .workflow_state_manager import WorkflowStateManager, WorkflowState
from .workflow_task_manager import WorkflowTaskManager, TaskStatus, TaskPriority
from .workflow_orchestrator import WorkflowOrchestrator
from .workflow_types import (
    WorkflowType, WorkflowStatus, ExecutionStrategy, ResourceType,
    ValidationLevel, ErrorSeverity, WorkflowCategory, DataFormat,
    AuthenticationType, LogLevel, WorkflowPhase, RetryPolicy, TimeoutPolicy,
    WorkflowComplexity, PerformanceTier, SecurityLevel, ComplianceLevel,
    WorkflowVersion, IntegrationType, MonitoringType, BackupPolicy, RollbackPolicy,
    NotificationType, WorkflowTag, DataSourceType, OutputFormat, WorkflowTemplate,
    WorkflowPermission, WorkflowScope, WorkflowLifecycle, WorkflowMetric,
    WorkflowAlert, WorkflowSchedule, WorkflowDependency
)
from .workflow_models import (
    ResourceRequirement, AgentCapabilityInfo, WorkflowStep, WorkflowDefinition,
    WorkflowExecution, WorkflowTask, WorkflowState, WorkflowMetrics,
    WorkflowAlert, WorkflowNotification, WorkflowSchedule, WorkflowDependency,
    WorkflowTemplate, WorkflowPermission, WorkflowAudit, WorkflowBackup,
    WorkflowIntegration, WorkflowMonitoring
)

__version__ = "2.0.0"
__author__ = "Agent-8 (Integration Enhancement Optimization Manager)"
__license__ = "MIT"

__all__ = [
    # Main engine
    "UnifiedWorkflowEngine",
    "create_unified_workflow_engine",
    
    # Core components
    "WorkflowCore",
    "WorkflowStateManager",
    "WorkflowTaskManager",
    "WorkflowOrchestrator",
    
    # Enums and types
    "WorkflowType",
    "WorkflowStatus",
    "TaskStatus",
    "TaskPriority",
    "ExecutionStrategy",
    "ResourceType",
    "ValidationLevel",
    "ErrorSeverity",
    "WorkflowCategory",
    "DataFormat",
    "AuthenticationType",
    "LogLevel",
    "WorkflowPhase",
    "RetryPolicy",
    "TimeoutPolicy",
    "WorkflowComplexity",
    "PerformanceTier",
    "SecurityLevel",
    "ComplianceLevel",
    "WorkflowVersion",
    "IntegrationType",
    "MonitoringType",
    "BackupPolicy",
    "RollbackPolicy",
    "NotificationType",
    "WorkflowTag",
    "DataSourceType",
    "OutputFormat",
    "WorkflowTemplate",
    "WorkflowPermission",
    "WorkflowScope",
    "WorkflowLifecycle",
    "WorkflowMetric",
    "WorkflowAlert",
    "WorkflowSchedule",
    "WorkflowDependency",
    
    # Data models
    "ResourceRequirement",
    "AgentCapabilityInfo",
    "WorkflowStep",
    "WorkflowDefinition",
    "WorkflowExecution",
    "WorkflowTask",
    "WorkflowState",
    "WorkflowMetrics",
    "WorkflowAlert",
    "WorkflowNotification",
    "WorkflowSchedule",
    "WorkflowDependency",
    "WorkflowTemplate",
    "WorkflowPermission",
    "WorkflowAudit",
    "WorkflowBackup",
    "WorkflowIntegration",
    "WorkflowMonitoring",
]
