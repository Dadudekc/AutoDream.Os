"""
SSOT Models
===========

Data models for SSOT operations.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class SSOTExecutionPhase(Enum):
    """SSOT execution phases."""
    INITIALIZATION = "initialization"
    VALIDATION = "validation"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    COMPLETION = "completion"
    ERROR = "error"


class SSOTValidationLevel(Enum):
    """SSOT validation levels."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    CRITICAL = "critical"


class SSOTComponentType(Enum):
    """SSOT component types."""
    EXECUTION = "execution"
    VALIDATION = "validation"
    INTEGRATION = "integration"
    MONITORING = "monitoring"
    REPORTING = "reporting"


@dataclass
class SSOTComponent:
    """SSOT component definition."""
    component_id: str
    component_type: SSOTComponentType
    name: str
    description: str
    version: str
    dependencies: List[str]
    configuration: Dict[str, Any]
    is_active: bool = True
    created_at: datetime = None


@dataclass
class SSOTExecutionTask:
    """SSOT execution task."""
    task_id: str
    component_id: str
    phase: SSOTExecutionPhase
    priority: int
    data: Dict[str, Any]
    timeout: int = 300
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"


@dataclass
class SSOTIntegrationResult:
    """SSOT integration result."""
    integration_id: str
    component_id: str
    success: bool
    result_data: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = None


@dataclass
class SSOTValidationReport:
    """SSOT validation report."""
    report_id: str
    component_id: str
    validation_level: SSOTValidationLevel
    passed: bool
    score: float
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    generated_at: datetime


@dataclass
class SSOTMetrics:
    """SSOT system metrics."""
    total_components: int = 0
    active_components: int = 0
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    average_execution_time: float = 0.0
    success_rate: float = 0.0
    last_updated: datetime = None


class SSOTModels:
    """SSOT models and validation."""
    
    @staticmethod
    def create_component(
        component_id: str,
        component_type: SSOTComponentType,
        name: str,
        description: str,
        version: str,
        dependencies: List[str] = None,
        configuration: Dict[str, Any] = None
    ) -> SSOTComponent:
        """Create SSOT component."""
        return SSOTComponent(
            component_id=component_id,
            component_type=component_type,
            name=name,
            description=description,
            version=version,
            dependencies=dependencies or [],
            configuration=configuration or {},
            is_active=True,
            created_at=datetime.now()
        )
    
    @staticmethod
    def create_execution_task(
        task_id: str,
        component_id: str,
        phase: SSOTExecutionPhase,
        priority: int = 1,
        data: Dict[str, Any] = None,
        timeout: int = 300,
        max_retries: int = 3
    ) -> SSOTExecutionTask:
        """Create SSOT execution task."""
        return SSOTExecutionTask(
            task_id=task_id,
            component_id=component_id,
            phase=phase,
            priority=priority,
            data=data or {},
            timeout=timeout,
            retry_count=0,
            max_retries=max_retries,
            created_at=datetime.now(),
            status="pending"
        )
    
    @staticmethod
    def create_integration_result(
        integration_id: str,
        component_id: str,
        success: bool,
        result_data: Dict[str, Any] = None,
        error_message: str = None,
        execution_time: float = 0.0
    ) -> SSOTIntegrationResult:
        """Create SSOT integration result."""
        return SSOTIntegrationResult(
            integration_id=integration_id,
            component_id=component_id,
            success=success,
            result_data=result_data or {},
            error_message=error_message,
            execution_time=execution_time,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def create_validation_report(
        report_id: str,
        component_id: str,
        validation_level: SSOTValidationLevel,
        passed: bool,
        score: float,
        issues: List[Dict[str, Any]] = None,
        recommendations: List[str] = None
    ) -> SSOTValidationReport:
        """Create SSOT validation report."""
        return SSOTValidationReport(
            report_id=report_id,
            component_id=component_id,
            validation_level=validation_level,
            passed=passed,
            score=score,
            issues=issues or [],
            recommendations=recommendations or [],
            generated_at=datetime.now()
        )
    
    @staticmethod
    def create_metrics() -> SSOTMetrics:
        """Create SSOT metrics."""
        return SSOTMetrics(
            total_components=0,
            active_components=0,
            total_tasks=0,
            completed_tasks=0,
            failed_tasks=0,
            average_execution_time=0.0,
            success_rate=0.0,
            last_updated=datetime.now()
        )
    
    @staticmethod
    def update_metrics(
        metrics: SSOTMetrics,
        total_components: int = None,
        active_components: int = None,
        total_tasks: int = None,
        completed_tasks: int = None,
        failed_tasks: int = None,
        average_execution_time: float = None
    ) -> SSOTMetrics:
        """Update SSOT metrics."""
        if total_components is not None:
            metrics.total_components = total_components
        if active_components is not None:
            metrics.active_components = active_components
        if total_tasks is not None:
            metrics.total_tasks = total_tasks
        if completed_tasks is not None:
            metrics.completed_tasks = completed_tasks
        if failed_tasks is not None:
            metrics.failed_tasks = failed_tasks
        if average_execution_time is not None:
            metrics.average_execution_time = average_execution_time
        
        # Calculate success rate
        if metrics.total_tasks > 0:
            metrics.success_rate = metrics.completed_tasks / metrics.total_tasks
        
        metrics.last_updated = datetime.now()
        return metrics
    
    @staticmethod
    def validate_component(component: SSOTComponent) -> Dict[str, Any]:
        """Validate SSOT component."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        if not component.component_id:
            validation['errors'].append("Component ID is required")
            validation['is_valid'] = False
        
        if not component.name:
            validation['errors'].append("Component name is required")
            validation['is_valid'] = False
        
        if not component.version:
            validation['errors'].append("Component version is required")
            validation['is_valid'] = False
        
        # Check dependencies
        if component.dependencies:
            for dep in component.dependencies:
                if not isinstance(dep, str):
                    validation['warnings'].append(f"Invalid dependency type: {dep}")
        
        # Check configuration
        if component.configuration and not isinstance(component.configuration, dict):
            validation['warnings'].append("Configuration should be a dictionary")
        
        return validation
    
    @staticmethod
    def validate_task(task: SSOTExecutionTask) -> Dict[str, Any]:
        """Validate SSOT execution task."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        if not task.task_id:
            validation['errors'].append("Task ID is required")
            validation['is_valid'] = False
        
        if not task.component_id:
            validation['errors'].append("Component ID is required")
            validation['is_valid'] = False
        
        # Check timeout
        if task.timeout <= 0:
            validation['warnings'].append("Timeout should be positive")
        
        # Check retry count
        if task.retry_count > task.max_retries:
            validation['warnings'].append("Retry count exceeds max retries")
        
        return validation
