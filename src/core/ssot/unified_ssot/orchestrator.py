"""
SSOT Orchestrator
=================

Main orchestrator for SSOT operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime
import logging
from .models import (
    SSOTComponent, SSOTExecutionTask, SSOTIntegrationResult,
    SSOTValidationReport, SSOTExecutionPhase, SSOTValidationLevel,
    SSOTMetrics, SSOTComponentType
)
from .executor import SSOTExecutor
from .validator import SSOTValidator


class UnifiedSSOTOrchestrator:
    """Unified SSOT orchestrator."""
    
    def __init__(self):
        """Initialize SSOT orchestrator."""
        self.components: Dict[str, SSOTComponent] = {}
        self.executor = SSOTExecutor()
        self.validator = SSOTValidator()
        self.metrics = SSOTMetrics()
        self.is_initialized = False
    
    async def initialize(self) -> bool:
        """Initialize SSOT orchestrator."""
        try:
            logging.info("Initializing SSOT Orchestrator")
            
            # Initialize core components
            await self._initialize_core_components()
            
            # Validate all components
            await self._validate_all_components()
            
            self.is_initialized = True
            logging.info("SSOT Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize SSOT Orchestrator: {e}")
            return False
    
    async def _initialize_core_components(self):
        """Initialize core SSOT components."""
        # Create execution component
        execution_component = SSOTComponent(
            component_id="ssot_execution",
            component_type=SSOTComponentType.EXECUTION,
            name="SSOT Execution Engine",
            description="Core execution engine for SSOT operations",
            version="1.0.0",
            dependencies=[],
            configuration={"max_concurrent_tasks": 10}
        )
        self.components["ssot_execution"] = execution_component
        
        # Create validation component
        validation_component = SSOTComponent(
            component_id="ssot_validation",
            component_type=SSOTComponentType.VALIDATION,
            name="SSOT Validation Engine",
            description="Core validation engine for SSOT operations",
            version="1.0.0",
            dependencies=[],
            configuration={"validation_timeout": 30}
        )
        self.components["ssot_validation"] = validation_component
        
        # Create integration component
        integration_component = SSOTComponent(
            component_id="ssot_integration",
            component_type=SSOTComponentType.INTEGRATION,
            name="SSOT Integration Engine",
            description="Core integration engine for SSOT operations",
            version="1.0.0",
            dependencies=["ssot_execution", "ssot_validation"],
            configuration={"integration_timeout": 60}
        )
        self.components["ssot_integration"] = integration_component
    
    async def _validate_all_components(self):
        """Validate all components."""
        for component in self.components.values():
            report = self.validator.validate_component(component, SSOTValidationLevel.STANDARD)
            if not report.passed:
                logging.warning(f"Component {component.component_id} validation failed: {report.issues}")
    
    async def register_component(self, component: SSOTComponent) -> bool:
        """Register new SSOT component."""
        try:
            # Validate component
            report = self.validator.validate_component(component, SSOTValidationLevel.STANDARD)
            if not report.passed:
                logging.error(f"Component validation failed: {report.issues}")
                return False
            
            # Register component
            self.components[component.component_id] = component
            logging.info(f"Registered component: {component.component_id}")
            
            # Update metrics
            self.metrics.total_components = len(self.components)
            self.metrics.active_components = sum(1 for c in self.components.values() if c.is_active)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to register component {component.component_id}: {e}")
            return False
    
    async def execute_task(self, task: SSOTExecutionTask) -> SSOTIntegrationResult:
        """Execute SSOT task."""
        if not self.is_initialized:
            raise RuntimeError("SSOT Orchestrator not initialized")
        
        # Validate task
        report = self.validator.validate_task(task)
        if not report.passed:
            logging.warning(f"Task validation failed: {report.issues}")
        
        # Execute task
        result = await self.executor.execute_task(task)
        
        # Update metrics
        self._update_metrics()
        
        return result
    
    async def execute_batch(self, tasks: List[SSOTExecutionTask]) -> List[SSOTIntegrationResult]:
        """Execute batch of tasks."""
        if not self.is_initialized:
            raise RuntimeError("SSOT Orchestrator not initialized")
        
        results = []
        for task in tasks:
            result = await self.execute_task(task)
            results.append(result)
        
        return results
    
    def _update_metrics(self):
        """Update SSOT metrics."""
        executor_summary = self.executor.get_execution_summary()
        validator_summary = self.validator.get_validation_summary()
        
        self.metrics.total_components = len(self.components)
        self.metrics.active_components = sum(1 for c in self.components.values() if c.is_active)
        self.metrics.total_tasks = executor_summary["total_tasks"]
        self.metrics.completed_tasks = executor_summary["completed_tasks"]
        self.metrics.failed_tasks = executor_summary["failed_tasks"]
        self.metrics.success_rate = executor_summary["success_rate"]
        self.metrics.last_updated = datetime.now()
    
    def get_component(self, component_id: str) -> Optional[SSOTComponent]:
        """Get SSOT component by ID."""
        return self.components.get(component_id)
    
    def get_all_components(self) -> List[SSOTComponent]:
        """Get all SSOT components."""
        return list(self.components.values())
    
    def get_active_components(self) -> List[SSOTComponent]:
        """Get active SSOT components."""
        return [c for c in self.components.values() if c.is_active]
    
    def get_metrics(self) -> SSOTMetrics:
        """Get SSOT metrics."""
        self._update_metrics()
        return self.metrics
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        return self.executor.get_execution_summary()
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        return self.validator.get_validation_summary()
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status."""
        return self.executor.get_task_status(task_id)
    
    async def retry_failed_task(self, task_id: str) -> Optional[SSOTIntegrationResult]:
        """Retry failed task."""
        return await self.executor.retry_failed_task(task_id)
    
    def get_failed_tasks(self) -> List[SSOTExecutionTask]:
        """Get failed tasks."""
        return self.executor.get_failed_tasks()
    
    def get_completed_tasks(self) -> List[SSOTExecutionTask]:
        """Get completed tasks."""
        return self.executor.get_completed_tasks()
    
    def get_active_tasks(self) -> List[SSOTExecutionTask]:
        """Get active tasks."""
        return self.executor.get_active_tasks()
    
    def clear_history(self):
        """Clear execution and validation history."""
        self.executor.clear_history()
        self.validator.clear_history()
    
    def shutdown(self):
        """Shutdown SSOT orchestrator."""
        logging.info("Shutting down SSOT Orchestrator")
        self.clear_history()
        self.is_initialized = False
