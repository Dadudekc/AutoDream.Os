#!/usr/bin/env python3
"""
Workflow Integration Manager - Agent-5
=====================================

This module provides a unified interface for coordinating automated refactoring
workflows, validation, and reliability testing systems.

Features:
- Unified workflow coordination
- System integration management
- Performance monitoring and optimization
- Error handling and recovery

Author: Agent-5 (REFACTORING MANAGER)
Contract: REFACTOR-002 - Automated Refactoring Workflow Implementation
Status: IN PROGRESS
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import traceback

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.managers.base_manager import BaseManager
from core.refactoring.automated_refactoring_workflows import AutomatedRefactoringWorkflows, WorkflowType
from core.workflow_validation import WorkflowValidationSystem, ValidationLevel
from core.refactoring.workflow_reliability_testing import WorkflowReliabilityTesting

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IntegrationStatus:
    """Integration status information."""
    component: str
    status: str
    last_check: datetime
    health_score: float
    error_count: int = 0
    last_error: Optional[str] = None


@dataclass
class WorkflowExecutionSummary:
    """Summary of workflow execution results."""
    workflow_id: str
    workflow_type: str
    execution_time: float
    success_rate: float
    validation_score: float
    reliability_score: float
    target_files: List[str]
    completion_status: str
    timestamp: datetime


class WorkflowIntegrationManager(BaseManager):
    """
    Unified workflow integration manager for automated refactoring systems.
    
    This class coordinates all workflow components while maintaining separation
    of concerns and single responsibility principles.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the workflow integration manager."""
        super().__init__(config or {})
        self.workflows_system: Optional[AutomatedRefactoringWorkflows] = None
        self.validation_system: Optional[WorkflowValidationSystem] = None
        self.reliability_system: Optional[WorkflowReliabilityTesting] = None
        
        self.integration_status: Dict[str, IntegrationStatus] = {}
        self.execution_history: List[WorkflowExecutionSummary] = []
        self.performance_metrics: Dict[str, float] = {}
        
        self._setup_logging()
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all workflow components."""
        try:
            # Initialize workflows system
            self.workflows_system = AutomatedRefactoringWorkflows()
            self._update_component_status("workflows", "active", 100.0)
            
            # Initialize validation system
            self.validation_system = WorkflowValidationSystem()
            self._update_component_status("validation", "active", 100.0)
            
            # Initialize reliability system
            self.reliability_system = WorkflowReliabilityTesting()
            self._update_component_status("reliability", "active", 100.0)
            
            # Set up cross-component integration
            if self.reliability_system and self.validation_system:
                self.reliability_system.set_validation_system(self.validation_system)
            
            logger.info("All workflow components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize workflow components: {str(e)}")
            self._update_component_status("initialization", "failed", 0.0, str(e))
    
    def _update_component_status(self, component: str, status: str, health_score: float, 
                                error_message: Optional[str] = None):
        """Update component integration status."""
        if component not in self.integration_status:
            self.integration_status[component] = IntegrationStatus(
                component=component,
                status=status,
                last_check=datetime.now(),
                health_score=health_score
            )
        else:
            current_status = self.integration_status[component]
            current_status.status = status
            current_status.last_check = datetime.now()
            current_status.health_score = health_score
            
            if error_message:
                current_status.error_count += 1
                current_status.last_error = error_message
    
    async def execute_comprehensive_workflow(self, workflow_type: WorkflowType, 
                                          target_files: List[str],
                                          validation_level: ValidationLevel = ValidationLevel.COMPREHENSIVE) -> Dict[str, Any]:
        """
        Execute a comprehensive refactoring workflow with validation and reliability testing.
        
        Args:
            workflow_type: Type of workflow to execute
            target_files: List of target files for refactoring
            validation_level: Level of validation to perform
            
        Returns:
            Comprehensive execution results
        """
        if not self._validate_system_readiness():
            raise RuntimeError("Workflow systems not ready for execution")
        
        execution_start = datetime.now()
        results = {
            "workflow_execution": None,
            "validation_results": None,
            "reliability_results": None,
            "integration_status": self.get_integration_status(),
            "execution_summary": None
        }
        
        try:
            # Step 1: Execute workflow
            logger.info(f"Starting comprehensive workflow execution for {workflow_type.value}")
            workflow_id = self.workflows_system.create_workflow(workflow_type, target_files)
            workflow = await self.workflows_system.execute_workflow(workflow_id)
            results["workflow_execution"] = workflow
            
            # Step 2: Validate workflow
            logger.info("Executing workflow validation")
            validation_report = await self.validation_system.validate_workflow(
                workflow_id, validation_level, target_files
            )
            results["validation_results"] = validation_report
            
            # Step 3: Run reliability testing
            logger.info("Executing reliability testing")
            reliability_suite = await self.reliability_system.run_reliability_test_suite(
                f"workflow_{workflow_id}", None, workflow_id
            )
            results["reliability_results"] = reliability_suite
            
            # Step 4: Create execution summary
            execution_time = (datetime.now() - execution_start).total_seconds()
            summary = WorkflowExecutionSummary(
                workflow_id=workflow_id,
                workflow_type=workflow_type.value,
                execution_time=execution_time,
                success_rate=workflow.success_rate,
                validation_score=validation_report.overall_score,
                reliability_score=reliability_suite.overall_reliability,
                target_files=target_files,
                completion_status="completed",
                timestamp=datetime.now()
            )
            
            self.execution_history.append(summary)
            results["execution_summary"] = summary
            
            # Update performance metrics
            self._update_performance_metrics(execution_time, workflow.success_rate, 
                                          validation_report.overall_score, reliability_suite.overall_reliability)
            
            logger.info(f"Comprehensive workflow execution completed successfully in {execution_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Comprehensive workflow execution failed: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Create failure summary
            execution_time = (datetime.now() - execution_start).total_seconds()
            failure_summary = WorkflowExecutionSummary(
                workflow_id="failed_execution",
                workflow_type=workflow_type.value,
                execution_time=execution_time,
                success_rate=0.0,
                validation_score=0.0,
                reliability_score=0.0,
                target_files=target_files,
                completion_status="failed",
                timestamp=datetime.now()
            )
            
            self.execution_history.append(failure_summary)
            results["execution_summary"] = failure_summary
            
            # Update component status
            self._update_component_status("execution", "error", 0.0, str(e))
        
        return results
    
    def _validate_system_readiness(self) -> bool:
        """Validate that all workflow systems are ready for execution."""
        required_components = [
            ("workflows", self.workflows_system),
            ("validation", self.validation_system),
            ("reliability", self.reliability_system)
        ]
        
        for component_name, component in required_components:
            if component is None:
                logger.error(f"Required component {component_name} is not initialized")
                return False
            
            status = self.integration_status.get(component_name)
            if status and status.status != "active":
                logger.error(f"Component {component_name} is not in active status: {status.status}")
                return False
        
        return True
    
    def _update_performance_metrics(self, execution_time: float, success_rate: float, 
                                  validation_score: float, reliability_score: float):
        """Update performance metrics for monitoring."""
        self.performance_metrics["last_execution_time"] = execution_time
        self.performance_metrics["average_success_rate"] = self._calculate_average_success_rate()
        self.performance_metrics["average_validation_score"] = self._calculate_average_validation_score()
        self.performance_metrics["average_reliability_score"] = self._calculate_average_reliability_score()
        self.performance_metrics["total_executions"] = len(self.execution_history)
    
    def _calculate_average_success_rate(self) -> float:
        """Calculate average success rate from execution history."""
        if not self.execution_history:
            return 0.0
        
        total_rate = sum(execution.success_rate for execution in self.execution_history)
        return total_rate / len(self.execution_history)
    
    def _calculate_average_validation_score(self) -> float:
        """Calculate average validation score from execution history."""
        if not self.execution_history:
            return 0.0
        
        total_score = sum(execution.validation_score for execution in self.execution_history)
        return total_score / len(self.execution_history)
    
    def _calculate_average_reliability_score(self) -> float:
        """Calculate average reliability score from execution history."""
        if not self.execution_history:
            return 0.0
        
        total_score = sum(execution.reliability_score for execution in self.execution_history)
        return total_score / len(self.execution_history)
    
    def get_integration_status(self) -> Dict[str, Dict[str, Any]]:
        """Get current integration status for all components."""
        status_summary = {}
        
        for component_name, status in self.integration_status.items():
            status_summary[component_name] = {
                "status": status.status,
                "health_score": status.health_score,
                "last_check": status.last_check.isoformat(),
                "error_count": status.error_count,
                "last_error": status.last_error
            }
        
        return status_summary
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return {
            "performance_metrics": self.performance_metrics.copy(),
            "execution_history_count": len(self.execution_history),
            "system_health": self._calculate_system_health_score()
        }
    
    def _calculate_system_health_score(self) -> float:
        """Calculate overall system health score."""
        if not self.integration_status:
            return 0.0
        
        total_health = sum(status.health_score for status in self.integration_status.values())
        return total_health / len(self.integration_status)
    
    def get_execution_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get execution history with optional limit."""
        history = []
        
        for execution in self.execution_history[-limit:] if limit else self.execution_history:
            history.append({
                "workflow_id": execution.workflow_id,
                "workflow_type": execution.workflow_type,
                "execution_time": execution.execution_time,
                "success_rate": execution.success_rate,
                "validation_score": execution.validation_score,
                "reliability_score": execution.reliability_score,
                "target_files": execution.target_files,
                "completion_status": execution.completion_status,
                "timestamp": execution.timestamp.isoformat()
            })
        
        return history
    
    async def run_system_diagnostics(self) -> Dict[str, Any]:
        """Run comprehensive system diagnostics."""
        diagnostics = {
            "timestamp": datetime.now().isoformat(),
            "integration_status": self.get_integration_status(),
            "performance_metrics": self.get_performance_metrics(),
            "component_health": {},
            "recommendations": []
        }
        
        # Check component health
        for component_name, status in self.integration_status.items():
            health_info = {
                "status": status.status,
                "health_score": status.health_score,
                "error_count": status.error_count,
                "last_error": status.last_error
            }
            
            diagnostics["component_health"][component_name] = health_info
            
            # Generate recommendations
            if status.health_score < 80:
                diagnostics["recommendations"].append(
                    f"Component {component_name} has low health score ({status.health_score:.1f}%). "
                    "Consider investigation and maintenance."
                )
            
            if status.error_count > 5:
                diagnostics["recommendations"].append(
                    f"Component {component_name} has high error count ({status.error_count}). "
                    "Review error logs and implement fixes."
                )
        
        # Overall system recommendations
        system_health = self._calculate_system_health_score()
        if system_health < 90:
            diagnostics["recommendations"].append(
                f"Overall system health is below optimal ({system_health:.1f}%). "
                "Review component statuses and address issues."
            )
        
        if not diagnostics["recommendations"]:
            diagnostics["recommendations"].append("System is operating within optimal parameters.")
        
        return diagnostics
    
    def export_integration_report(self, output_path: str) -> bool:
        """Export comprehensive integration report."""
        try:
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "integration_status": self.get_integration_status(),
                "performance_metrics": self.get_performance_metrics(),
                "execution_history": self.get_execution_history(50),  # Last 50 executions
                "system_health": self._calculate_system_health_score()
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            logger.info(f"Integration report exported to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export integration report: {str(e)}")
            return False
    
    def cleanup_old_data(self, max_age_days: int = 7):
        """Clean up old execution history and performance data."""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        # Clean execution history
        original_count = len(self.execution_history)
        self.execution_history = [
            execution for execution in self.execution_history
            if execution.timestamp > cutoff_date
        ]
        removed_count = original_count - len(self.execution_history)
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old execution records")
        
        # Clean performance metrics (keep only recent)
        if "last_execution_time" in self.performance_metrics:
            if self.performance_metrics["last_execution_time"] < cutoff_date.timestamp():
                self.performance_metrics.clear()
                logger.info("Cleaned up old performance metrics")


# Example usage and testing
async def demo_workflow_integration():
    """Demonstrate the workflow integration manager."""
    print("🔗 Workflow Integration Manager Demo")
    print("=" * 50)
    
    # Initialize integration manager
    integration_manager = WorkflowIntegrationManager()
    
    # Check system status
    print("✅ Checking system status...")
    status = integration_manager.get_integration_status()
    for component, info in status.items():
        print(f"  {component}: {info['status']} (Health: {info['health_score']:.1f}%)")
    
    # Execute comprehensive workflow
    print("\n🚀 Executing comprehensive workflow...")
    target_files = [
        "src/services/financial/portfolio/rebalancing.py",
        "src/core/performance/performance_orchestrator.py"
    ]
    
    results = await integration_manager.execute_comprehensive_workflow(
        WorkflowType.CODE_DUPLICATION_REMOVAL,
        target_files,
        ValidationLevel.COMPREHENSIVE
    )
    
    # Display results
    if results["execution_summary"]:
        summary = results["execution_summary"]
        print(f"\n📊 Workflow Execution Results:")
        print(f"  Workflow ID: {summary.workflow_id}")
        print(f"  Success Rate: {summary.success_rate:.1f}%")
        print(f"  Validation Score: {summary.validation_score:.1f}%")
        print(f"  Reliability Score: {summary.reliability_score:.1f}%")
        print(f"  Execution Time: {summary.execution_time:.2f} seconds")
    
    # Run system diagnostics
    print("\n🔍 Running system diagnostics...")
    diagnostics = await integration_manager.run_system_diagnostics()
    
    print(f"  System Health: {diagnostics['component_health']['workflows']['health_score']:.1f}%")
    print(f"  Total Executions: {diagnostics['performance_metrics']['execution_history_count']}")
    
    # Export integration report
    report_path = "workflow_integration_report.json"
    if integration_manager.export_integration_report(report_path):
        print(f"\n📊 Integration report exported to: {report_path}")
    
    print("\n🎉 Integration demo completed successfully!")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_workflow_integration())
