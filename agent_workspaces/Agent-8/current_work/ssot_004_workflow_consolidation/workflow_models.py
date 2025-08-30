#!/usr/bin/env python3
"""
Workflow Models - SSOT-004 Implementation

Data models and classes for unified workflow system.
Maintains V2 compliance with modular architecture.

Author: Agent-8 (Integration Enhancement Optimization Manager)
Contract: SSOT-004: Workflow & Reporting System Consolidation
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from .workflow_types import (
    WorkflowType, WorkflowStatus, TaskStatus, TaskPriority, ExecutionStrategy,
    ResourceType, ValidationLevel, ErrorSeverity, WorkflowCategory, DataFormat,
    AuthenticationType, LogLevel, WorkflowPhase, RetryPolicy, TimeoutPolicy,
    WorkflowComplexity, PerformanceTier, SecurityLevel, ComplianceLevel,
    WorkflowVersion, IntegrationType, MonitoringType, BackupPolicy, RollbackPolicy,
    NotificationType, WorkflowTag, DataSourceType, OutputFormat, WorkflowTemplate,
    WorkflowPermission, WorkflowScope, WorkflowLifecycle, WorkflowMetric,
    WorkflowAlert, WorkflowSchedule, WorkflowDependency
)


@dataclass
class ResourceRequirement:
    """Resource requirement for workflow execution."""
    resource_type: ResourceType
    amount: Union[int, float]
    unit: str
    priority: TaskPriority = TaskPriority.NORMAL
    optional: bool = False
    description: Optional[str] = None


@dataclass
class AgentCapabilityInfo:
    """Information about agent capabilities."""
    agent_id: str
    capabilities: List[str]
    performance_rating: float
    availability: float
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class WorkflowStep:
    """Individual step in a workflow."""
    id: str
    name: str
    action: str
    description: Optional[str] = None
    next: Optional[Union[str, int]] = None
    condition: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = None
    retry_attempts: Optional[int] = None
    retry_delay: Optional[int] = None
    resources: List[ResourceRequirement] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_handling: Optional[Dict[str, Any]] = None
    validation: Optional[Dict[str, Any]] = None


@dataclass
class WorkflowDefinition:
    """Complete workflow definition."""
    workflow_id: str
    type: Union[str, WorkflowType]
    definition: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    name: Optional[str] = None
    description: Optional[str] = None
    version: str = "1.0.0"
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    category: WorkflowCategory = WorkflowCategory.CORE
    complexity: WorkflowComplexity = WorkflowComplexity.SIMPLE
    execution_strategy: ExecutionStrategy = ExecutionStrategy.SEQUENTIAL
    validation_level: ValidationLevel = ValidationLevel.STANDARD
    security_level: SecurityLevel = SecurityLevel.INTERNAL
    compliance_level: ComplianceLevel = ComplianceLevel.BASIC
    performance_tier: PerformanceTier = PerformanceTier.STANDARD
    timeout_policy: TimeoutPolicy = TimeoutPolicy.SOFT
    retry_policy: RetryPolicy = RetryPolicy.LINEAR_BACKOFF
    backup_policy: BackupPolicy = BackupPolicy.SCHEDULED
    rollback_policy: RollbackPolicy = RollbackPolicy.MANUAL
    monitoring_type: MonitoringType = MonitoringType.BASIC
    notification_type: NotificationType = NotificationType.LOG
    integration_type: IntegrationType = IntegrationType.NONE
    data_format: DataFormat = DataFormat.JSON
    output_format: OutputFormat = DataFormat.JSON
    authentication_type: AuthenticationType = AuthenticationType.NONE
    log_level: LogLevel = LogLevel.INFO
    workflow_scope: WorkflowScope = WorkflowScope.LOCAL
    workflow_permission: WorkflowPermission = WorkflowPermission.EXECUTE
    workflow_lifecycle: WorkflowLifecycle = WorkflowLifecycle.DEVELOPMENT
    workflow_version: WorkflowVersion = WorkflowVersion.DRAFT
    workflow_template: WorkflowTemplate = WorkflowTemplate.CUSTOM_WORKFLOW
    dependencies: List[WorkflowDependency] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """Workflow execution instance."""
    execution_id: str
    workflow_id: str
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: WorkflowStatus = WorkflowStatus.CREATED
    current_step: int = 0
    total_steps: int = 0
    execution_strategy: ExecutionStrategy = ExecutionStrategy.SEQUENTIAL
    execution_context: Dict[str, Any] = field(default_factory=dict)
    error_context: Optional[Dict[str, Any]] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowTask:
    """Individual task within a workflow execution."""
    task_id: str
    workflow_id: str
    execution_id: str
    step_id: str
    name: str
    action: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.NORMAL
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    timeout: Optional[int] = None
    retry_attempts: int = 0
    max_retry_attempts: int = 3
    retry_delay: int = 5
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    execution_context: Dict[str, Any] = field(default_factory=dict)
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowState:
    """Workflow state information."""
    workflow_id: str
    current_status: WorkflowStatus
    previous_status: Optional[WorkflowStatus] = None
    current_phase: WorkflowPhase = WorkflowPhase.INITIALIZATION
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    last_execution: Optional[datetime] = None
    next_scheduled_execution: Optional[datetime] = None
    active_executions: int = 0
    queued_executions: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowMetrics:
    """Workflow performance metrics."""
    workflow_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    execution_time: float = 0.0
    success_rate: float = 0.0
    error_rate: float = 0.0
    throughput: float = 0.0
    latency: float = 0.0
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    cost: float = 0.0
    custom_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowAlert:
    """Workflow alert information."""
    alert_id: str
    workflow_id: str
    alert_type: WorkflowAlert
    severity: ErrorSeverity
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved: bool = False
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowNotification:
    """Workflow notification information."""
    notification_id: str
    workflow_id: str
    notification_type: NotificationType
    recipient: str
    subject: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    sent: bool = False
    sent_at: Optional[datetime] = None
    delivered: bool = False
    delivered_at: Optional[datetime] = None
    read: bool = False
    read_at: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.NORMAL
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowSchedule:
    """Workflow schedule information."""
    schedule_id: str
    workflow_id: str
    schedule_type: WorkflowSchedule
    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    timezone: str = "UTC"
    enabled: bool = True
    last_execution: Optional[datetime] = None
    next_execution: Optional[datetime] = None
    max_executions: Optional[int] = None
    execution_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowDependency:
    """Workflow dependency information."""
    dependency_id: str
    workflow_id: str
    dependent_workflow_id: str
    dependency_type: WorkflowDependency
    condition: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = None
    required: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowTemplate:
    """Workflow template information."""
    template_id: str
    name: str
    description: str
    category: WorkflowCategory
    complexity: WorkflowComplexity
    template_data: Dict[str, Any]
    version: str = "1.0.0"
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    usage_count: int = 0
    rating: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowPermission:
    """Workflow permission information."""
    permission_id: str
    workflow_id: str
    user_id: str
    permission_level: WorkflowPermission
    granted_at: datetime = field(default_factory=datetime.now)
    granted_by: str
    expires_at: Optional[datetime] = None
    revoked: bool = False
    revoked_at: Optional[datetime] = None
    revoked_by: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowAudit:
    """Workflow audit information."""
    audit_id: str
    workflow_id: str
    user_id: str
    action: str
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowBackup:
    """Workflow backup information."""
    backup_id: str
    workflow_id: str
    backup_type: BackupPolicy
    backup_data: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str
    size_bytes: int = 0
    checksum: Optional[str] = None
    compression: bool = False
    encryption: bool = False
    retention_days: int = 30
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowIntegration:
    """Workflow integration information."""
    integration_id: str
    workflow_id: str
    integration_type: IntegrationType
    endpoint: str
    authentication: Dict[str, Any] = field(default_factory=dict)
    configuration: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    last_sync: Optional[datetime] = None
    sync_interval: Optional[int] = None
    error_count: int = 0
    last_error: Optional[str] = None
    last_error_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowMonitoring:
    """Workflow monitoring configuration."""
    monitoring_id: str
    workflow_id: str
    monitoring_type: MonitoringType
    metrics: List[WorkflowMetric] = field(default_factory=list)
    alerts: List[WorkflowAlert] = field(default_factory=list)
    thresholds: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    interval_seconds: int = 60
    last_check: Optional[datetime] = None
    next_check: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
