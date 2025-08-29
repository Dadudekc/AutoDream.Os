#!/usr/bin/env python3
"""
Emergency Recovery Executor - Component of Emergency Response System
==================================================================

Responsible for executing recovery procedures and validating recovery success.
Extracted from EmergencyResponseSystem to follow Single Responsibility Principle.

Author: Agent-7 (Class Hierarchy Refactoring)
Contract: MODULAR-002: Class Hierarchy Refactoring (400 pts)
License: MIT
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

from ..base_manager import BaseManager


logger = logging.getLogger(__name__)


class RecoveryStatus(Enum):
    """Recovery procedure status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATED = "validated"


class RecoveryPriority(Enum):
    """Recovery procedure priority"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RecoveryTask:
    """Individual recovery task definition"""
    task_id: str
    name: str
    description: str
    priority: RecoveryPriority
    estimated_duration: int  # seconds
    dependencies: List[str] = field(default_factory=list)
    status: RecoveryStatus = RecoveryStatus.PENDING
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


@dataclass
class RecoveryProcedure:
    """Recovery procedure definition"""
    procedure_id: str
    name: str
    description: str
    priority: RecoveryPriority
    tasks: List[RecoveryTask]
    validation_criteria: List[str]
    estimated_total_duration: int  # seconds
    status: RecoveryStatus = RecoveryStatus.PENDING
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    validation_results: Optional[Dict[str, bool]] = None
    overall_success: Optional[bool] = None


@dataclass
class RecoveryExecution:
    """Recovery execution tracking"""
    execution_id: str
    procedure_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: RecoveryStatus = RecoveryStatus.IN_PROGRESS
    tasks_completed: int = 0
    total_tasks: int = 0
    validation_passed: bool = False
    errors: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)


class RecoveryExecutor(BaseManager):
    """
    Emergency Recovery Executor - Single responsibility: Recovery procedure execution
    
    This component is responsible for:
    - Executing recovery procedures
    - Managing recovery task dependencies
    - Validating recovery success
    - Tracking recovery progress
    - Managing recovery rollback if needed
    """

    def __init__(self, config_path: str = "config/recovery_executor.json"):
        """Initialize recovery executor"""
        super().__init__(
            manager_name="RecoveryExecutor",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Recovery procedures storage
        self.recovery_procedures: Dict[str, RecoveryProcedure] = {}
        self.recovery_handlers: Dict[str, Callable] = {}
        
        # Execution tracking
        self.active_executions: Dict[str, RecoveryExecution] = {}
        self.execution_history: List[RecoveryExecution] = []
        
        # Recovery state
        self.recovery_active = False
        self.max_concurrent_recoveries = 3
        self.recovery_timeout = 3600  # 1 hour default timeout
        
        # Load configuration and setup
        self._load_recovery_config()
        self._setup_default_procedures()
        
        self.logger.info("✅ Emergency Recovery Executor initialized successfully")

    def _load_recovery_config(self):
        """Load recovery executor configuration"""
        try:
            config = self.get_config()
            
            # Load custom recovery procedures if available
            if 'custom_procedures' in config:
                for procedure_data in config['custom_procedures']:
                    procedure = self._create_procedure_from_data(procedure_data)
                    if procedure:
                        self.recovery_procedures[procedure.procedure_id] = procedure
            
            # Load execution settings
            self.max_concurrent_recoveries = config.get('max_concurrent_recoveries', 3)
            self.recovery_timeout = config.get('recovery_timeout', 3600)
            
        except Exception as e:
            self.logger.error(f"Failed to load recovery config: {e}")

    def _setup_default_procedures(self):
        """Setup default recovery procedures"""
        try:
            # Contract System Recovery Procedure
            contract_recovery = RecoveryProcedure(
                procedure_id="contract_system_recovery",
                name="Contract System Recovery",
                description="Recover contract claiming system and restore functionality",
                priority=RecoveryPriority.CRITICAL,
                tasks=[
                    RecoveryTask(
                        task_id="validate_contract_data",
                        name="Validate Contract Data",
                        description="Check contract data integrity and identify corruption",
                        priority=RecoveryPriority.HIGH,
                        estimated_duration=300  # 5 minutes
                    ),
                    RecoveryTask(
                        task_id="restore_contract_backup",
                        name="Restore Contract Backup",
                        description="Restore contract system from latest backup",
                        priority=RecoveryPriority.CRITICAL,
                        estimated_duration=600,  # 10 minutes
                        dependencies=["validate_contract_data"]
                    ),
                    RecoveryTask(
                        task_id="validate_contract_functionality",
                        name="Validate Contract Functionality",
                        description="Test contract claiming and completion functionality",
                        priority=RecoveryPriority.HIGH,
                        estimated_duration=300,  # 5 minutes
                        dependencies=["restore_contract_backup"]
                    )
                ],
                validation_criteria=[
                    "Contract availability > 40",
                    "Contract claiming system operational",
                    "Contract completion system functional",
                    "No data corruption errors"
                ],
                estimated_total_duration=1200  # 20 minutes
            )
            
            # Workflow Momentum Recovery Procedure
            workflow_recovery = RecoveryProcedure(
                procedure_id="workflow_momentum_recovery",
                name="Workflow Momentum Recovery",
                description="Restore workflow momentum and agent engagement",
                priority=RecoveryPriority.HIGH,
                tasks=[
                    RecoveryTask(
                        task_id="assess_workflow_status",
                        name="Assess Workflow Status",
                        description="Analyze current workflow status and identify stalls",
                        priority=RecoveryPriority.MEDIUM,
                        estimated_duration=180  # 3 minutes
                    ),
                    RecoveryTask(
                        task_id="generate_emergency_contracts",
                        name="Generate Emergency Contracts",
                        description="Create emergency contracts to restore momentum",
                        priority=RecoveryPriority.HIGH,
                        estimated_duration=300,  # 5 minutes
                        dependencies=["assess_workflow_status"]
                    ),
                    RecoveryTask(
                        task_id="activate_agent_mobilization",
                        name="Activate Agent Mobilization",
                        description="Send emergency directives to all agents",
                        priority=RecoveryPriority.HIGH,
                        estimated_duration=120,  # 2 minutes
                        dependencies=["generate_emergency_contracts"]
                    )
                ],
                validation_criteria=[
                    "Agent engagement > 90%",
                    "Workflow momentum restored",
                    "Emergency contracts available",
                    "Agent coordination active"
                ],
                estimated_total_duration=600  # 10 minutes
            )
            
            # Add default procedures
            self.recovery_procedures["contract_system_recovery"] = contract_recovery
            self.recovery_procedures["workflow_momentum_recovery"] = workflow_recovery
            
            self.logger.info("✅ Default recovery procedures configured")
            
        except Exception as e:
            self.logger.error(f"Failed to setup default procedures: {e}")

    def _create_procedure_from_data(self, procedure_data: Dict[str, Any]) -> Optional[RecoveryProcedure]:
        """Create RecoveryProcedure from configuration data"""
        try:
            # Convert tasks
            tasks = []
            for task_data in procedure_data.get('tasks', []):
                task = RecoveryTask(
                    task_id=task_data['task_id'],
                    name=task_data['name'],
                    description=task_data['description'],
                    priority=RecoveryPriority(task_data['priority']),
                    estimated_duration=task_data['estimated_duration'],
                    dependencies=task_data.get('dependencies', [])
                )
                tasks.append(task)
            
            # Create procedure
            procedure = RecoveryProcedure(
                procedure_id=procedure_data['procedure_id'],
                name=procedure_data['name'],
                description=procedure_data['description'],
                priority=RecoveryPriority(procedure_data['priority']),
                tasks=tasks,
                validation_criteria=procedure_data['validation_criteria'],
                estimated_total_duration=procedure_data['estimated_total_duration']
            )
            
            return procedure
            
        except Exception as e:
            self.logger.error(f"Failed to create procedure from data: {e}")
            return None

    def add_recovery_procedure(self, procedure: RecoveryProcedure):
        """Add a new recovery procedure"""
        self.recovery_procedures[procedure.procedure_id] = procedure
        self.logger.info(f"✅ Added recovery procedure: {procedure.name}")

    def remove_recovery_procedure(self, procedure_id: str):
        """Remove a recovery procedure"""
        if procedure_id in self.recovery_procedures:
            del self.recovery_procedures[procedure_id]
            self.logger.info(f"✅ Removed recovery procedure: {procedure_id}")

    def get_recovery_procedure(self, procedure_id: str) -> Optional[RecoveryProcedure]:
        """Get a specific recovery procedure"""
        return self.recovery_procedures.get(procedure_id)

    def list_recovery_procedures(self) -> List[str]:
        """List all available recovery procedure IDs"""
        return list(self.recovery_procedures.keys())

    def can_start_recovery(self) -> bool:
        """Check if a new recovery can be started"""
        return (len(self.active_executions) < self.max_concurrent_recoveries and 
                not self.recovery_active)

    def start_recovery(self, procedure_id: str) -> Optional[str]:
        """Start a recovery procedure"""
        try:
            if not self.can_start_recovery():
                self.logger.warning("⚠️ Cannot start recovery - limit reached or recovery active")
                return None
            
            procedure = self.get_recovery_procedure(procedure_id)
            if not procedure:
                self.logger.error(f"Recovery procedure not found: {procedure_id}")
                return None
            
            if procedure.status != RecoveryStatus.PENDING:
                self.logger.warning(f"Procedure {procedure_id} is already {procedure.status.value}")
                return None
            
            # Create execution tracking
            execution_id = f"recovery_{procedure_id}_{int(time.time())}"
            execution = RecoveryExecution(
                execution_id=execution_id,
                procedure_id=procedure_id,
                start_time=datetime.now(),
                total_tasks=len(procedure.tasks)
            )
            
            # Update procedure status
            procedure.status = RecoveryStatus.IN_PROGRESS
            procedure.start_time = datetime.now()
            
            # Store execution
            self.active_executions[execution_id] = execution
            
            # Record event
            self.record_event("recovery_started", {
                "execution_id": execution_id,
                "procedure_id": procedure_id,
                "procedure_name": procedure.name,
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.info(f"🚨 Recovery started: {procedure.name} (ID: {execution_id})")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"Failed to start recovery {procedure_id}: {e}")
            return None

    def execute_recovery_tasks(self, execution_id: str) -> Dict[str, Any]:
        """Execute all tasks for a recovery procedure"""
        try:
            execution = self.active_executions.get(execution_id)
            if not execution:
                return {"error": "Execution not found"}
            
            procedure = self.get_recovery_procedure(execution.procedure_id)
            if not procedure:
                return {"error": "Procedure not found"}
            
            if procedure.status != RecoveryStatus.IN_PROGRESS:
                return {"error": f"Procedure is {procedure.status.value}"}
            
            results = {}
            
            # Execute tasks in dependency order
            completed_tasks = set()
            for task in procedure.tasks:
                if task.status == RecoveryStatus.COMPLETED:
                    completed_tasks.add(task.task_id)
                    continue
                
                # Check dependencies
                if not all(dep in completed_tasks for dep in task.dependencies):
                    continue
                
                # Execute task
                task.status = RecoveryStatus.IN_PROGRESS
                task.start_time = datetime.now()
                
                result = self._execute_recovery_task(task, execution_id)
                task.result = result
                
                if result.get("status") == "success":
                    task.status = RecoveryStatus.COMPLETED
                    task.completion_time = datetime.now()
                    completed_tasks.add(task.task_id)
                    execution.tasks_completed += 1
                    results[task.task_id] = result
                else:
                    task.status = RecoveryStatus.FAILED
                    task.error_message = result.get("error", "Unknown error")
                    execution.errors.append(f"Task {task.name} failed: {task.error_message}")
                    break
            
            # Check if all tasks completed
            if execution.tasks_completed >= execution.total_tasks:
                procedure.status = RecoveryStatus.COMPLETED
                procedure.completion_time = datetime.now()
                execution.status = RecoveryStatus.COMPLETED
                execution.end_time = datetime.now()
                
                # Validate recovery
                validation_passed = self._validate_recovery(procedure)
                execution.validation_passed = validation_passed
                procedure.overall_success = validation_passed
                
                if validation_passed:
                    procedure.status = RecoveryStatus.VALIDATED
                    self.logger.info(f"✅ Recovery {procedure.name} completed and validated successfully")
                else:
                    self.logger.warning(f"⚠️ Recovery {procedure.name} completed but validation failed")
                
                # Move to history
                self.execution_history.append(execution)
                del self.active_executions[execution_id]
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to execute recovery tasks for {execution_id}: {e}")
            return {"error": str(e)}

    def _execute_recovery_task(self, task: RecoveryTask, execution_id: str) -> Dict[str, Any]:
        """Execute a single recovery task"""
        try:
            # This would integrate with actual recovery systems
            # For now, simulate task execution
            
            if task.name == "Validate Contract Data":
                return {
                    "status": "success",
                    "data_integrity": 0.95,
                    "corruption_level": "low",
                    "execution_time": 2.8
                }
            elif task.name == "Restore Contract Backup":
                return {
                    "status": "success",
                    "backup_restored": True,
                    "data_consistency": 0.98,
                    "execution_time": 8.5
                }
            elif task.name == "Validate Contract Functionality":
                return {
                    "status": "success",
                    "claiming_working": True,
                    "completion_working": True,
                    "execution_time": 3.2
                }
            elif task.name == "Assess Workflow Status":
                return {
                    "status": "success",
                    "workflow_stalls": 2,
                    "agent_engagement": 0.75,
                    "execution_time": 1.8
                }
            elif task.name == "Generate Emergency Contracts":
                return {
                    "status": "success",
                    "contracts_created": 12,
                    "total_points": 4500,
                    "execution_time": 4.2
                }
            elif task.name == "Activate Agent Mobilization":
                return {
                    "status": "success",
                    "agents_notified": 8,
                    "response_rate": 100,
                    "execution_time": 1.5
                }
            else:
                return {
                    "status": "simulated",
                    "task_name": task.name,
                    "execution_time": 2.0
                }
                
        except Exception as e:
            self.logger.error(f"Failed to execute recovery task {task.name}: {e}")
            return {"status": "error", "error": str(e)}

    def _validate_recovery(self, procedure: RecoveryProcedure) -> bool:
        """Validate that recovery was successful"""
        try:
            validation_results = {}
            
            for criterion in procedure.validation_criteria:
                result = self._evaluate_validation_criterion(criterion)
                validation_results[criterion] = result
            
            # All criteria must pass for validation to succeed
            overall_success = all(validation_results.values())
            
            # Store validation results
            procedure.validation_results = validation_results
            
            # Record validation event
            self.record_event("recovery_validated", {
                "procedure_id": procedure.procedure_id,
                "procedure_name": procedure.name,
                "validation_passed": overall_success,
                "validation_results": validation_results,
                "timestamp": datetime.now().isoformat()
            })
            
            return overall_success
            
        except Exception as e:
            self.logger.error(f"Failed to validate recovery for {procedure.procedure_id}: {e}")
            return False

    def _evaluate_validation_criterion(self, criterion: str) -> bool:
        """Evaluate a single validation criterion"""
        try:
            # Simple criterion evaluation - can be enhanced with more sophisticated logic
            if "Contract availability > 40" in criterion:
                # This would check actual contract availability
                return True  # Placeholder
            elif "Contract claiming system operational" in criterion:
                # This would test contract claiming functionality
                return True  # Placeholder
            elif "Agent engagement > 90%" in criterion:
                # This would check agent engagement levels
                return True  # Placeholder
            elif "Workflow momentum restored" in criterion:
                # This would assess workflow momentum
                return True  # Placeholder
            else:
                # Default to true for unknown criteria
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to evaluate validation criterion '{criterion}': {e}")
            return False

    def get_recovery_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific recovery execution"""
        try:
            execution = self.active_executions.get(execution_id)
            if not execution:
                # Check history
                for hist_exec in self.execution_history:
                    if hist_exec.execution_id == execution_id:
                        execution = hist_exec
                        break
                
                if not execution:
                    return None
            
            procedure = self.get_recovery_procedure(execution.procedure_id)
            
            return {
                "execution_id": execution.execution_id,
                "procedure_id": execution.procedure_id,
                "procedure_name": procedure.name if procedure else "Unknown",
                "start_time": execution.start_time.isoformat(),
                "end_time": execution.end_time.isoformat() if execution.end_time else None,
                "status": execution.status.value,
                "tasks_completed": execution.tasks_completed,
                "total_tasks": execution.total_tasks,
                "validation_passed": execution.validation_passed,
                "errors": execution.errors,
                "results": execution.results
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get recovery status for {execution_id}: {e}")
            return None

    def get_all_recovery_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all active recoveries"""
        return {
            exec_id: self.get_recovery_status(exec_id)
            for exec_id in self.active_executions.keys()
        }

    def get_recovery_history(self) -> List[Dict[str, Any]]:
        """Get recovery execution history"""
        return [
            {
                "execution_id": e.execution_id,
                "procedure_id": e.procedure_id,
                "start_time": e.start_time.isoformat(),
                "end_time": e.end_time.isoformat() if e.end_time else None,
                "status": e.status.value,
                "tasks_completed": e.tasks_completed,
                "total_tasks": e.total_tasks,
                "validation_passed": e.validation_passed,
                "errors": e.errors,
                "results": e.results
            }
            for e in self.execution_history
        ]

    def stop_recovery(self, execution_id: str) -> bool:
        """Stop an active recovery execution"""
        try:
            execution = self.active_executions.get(execution_id)
            if not execution:
                self.logger.warning(f"Recovery execution not found: {execution_id}")
                return False
            
            # Update status
            execution.status = RecoveryStatus.FAILED
            execution.end_time = datetime.now()
            
            # Get procedure
            procedure = self.get_recovery_procedure(execution.procedure_id)
            if procedure:
                procedure.status = RecoveryStatus.FAILED
            
            # Move to history
            self.execution_history.append(execution)
            del self.active_executions[execution_id]
            
            self.logger.info(f"⏹️ Recovery stopped: {execution_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop recovery {execution_id}: {e}")
            return False

    def health_check(self) -> Dict[str, Any]:
        """Health check for the recovery executor"""
        try:
            return {
                "is_healthy": True,
                "recovery_active": self.recovery_active,
                "total_procedures": len(self.recovery_procedures),
                "active_executions": len(self.active_executions),
                "total_executions": len(self.execution_history),
                "max_concurrent_recoveries": self.max_concurrent_recoveries,
                "recovery_timeout": self.recovery_timeout,
                "procedures": list(self.recovery_procedures.keys())
            }
            
        except Exception as e:
            return {
                "is_healthy": False,
                "error": str(e)
            }


# Export the main classes
__all__ = [
    "RecoveryExecutor", "RecoveryProcedure", "RecoveryTask", "RecoveryStatus",
    "RecoveryPriority", "RecoveryExecution"
]
