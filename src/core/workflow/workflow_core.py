#!/usr/bin/env python3
"""
Workflow Core Module - V2 Core Workflow System
=============================================

Contains core workflow logic, management, and definition handling.
Follows V2 coding standards: ≤200 LOC, single responsibility, clean OOP design.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import uuid

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

# Import workflow types
try:
    from .workflow_types import (
        WorkflowStep, V2Workflow, WorkflowExecution, 
        WorkflowOptimization, OptimizationStrategy
    )
except ImportError:
    # Fallback for standalone usage
    from workflow_types import (
        WorkflowStep, V2Workflow, WorkflowExecution, 
        WorkflowOptimization, OptimizationStrategy
    )

logger = logging.getLogger(__name__)


class WorkflowDefinitionManager:
    """Manages workflow definitions - single responsibility: definition management"""
    
    def __init__(self):
        self.workflow_definitions: Dict[str, List[WorkflowStep]] = {}
        self.logger = logging.getLogger(f"{__name__}.WorkflowDefinitionManager")
        self._initialize_default_definitions()

    def _initialize_default_definitions(self):
        """Initialize default workflow definitions"""
        # Agent onboarding workflow
        self.workflow_definitions["agent_onboarding"] = [
            WorkflowStep(
                step_id="init",
                name="Initialization",
                step_type="initialization",
                description="Initialize agent system",
                dependencies=[],
                estimated_duration=30.0,
            ),
            WorkflowStep(
                step_id="training",
                name="Training",
                step_type="training",
                description="Conduct agent training",
                dependencies=["init"],
                estimated_duration=300.0,
            ),
            WorkflowStep(
                step_id="role_assignment",
                name="Role Assignment",
                step_type="role_assignment",
                description="Assign agent role",
                dependencies=["training"],
                estimated_duration=60.0,
            ),
            WorkflowStep(
                step_id="completion",
                name="Completion",
                step_type="completion",
                description="Complete onboarding",
                dependencies=["role_assignment"],
                estimated_duration=30.0,
            ),
        ]

    def get_workflow_definition(self, workflow_type: str) -> Optional[List[WorkflowStep]]:
        """Get workflow definition by type"""
        return self.workflow_definitions.get(workflow_type)

    def add_workflow_definition(self, workflow_type: str, steps: List[WorkflowStep]):
        """Add new workflow definition"""
        self.workflow_definitions[workflow_type] = steps
        self.logger.info(f"Added workflow definition: {workflow_type}")

    def list_workflow_types(self) -> List[str]:
        """List all available workflow types"""
        return list(self.workflow_definitions.keys())


class WorkflowStateManager:
    """Manages workflow state and transitions - single responsibility: state management"""
    
    def __init__(self):
        self.workflows: Dict[str, V2Workflow] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.active_workflows: Dict[str, V2Workflow] = {}
        self.logger = logging.getLogger(f"{__name__}.WorkflowStateManager")

    def create_workflow(self, name: str, description: str, steps: List[Dict[str, Any]]) -> str:
        """Create a new V2 workflow"""
        try:
            workflow_id = str(uuid.uuid4())
            
            # Convert step dictionaries to WorkflowStep objects
            workflow_steps = []
            for step_data in steps:
                step = WorkflowStep(
                    step_id=step_data.get("id", str(uuid.uuid4())),
                    name=step_data.get("name", "Unnamed Step"),
                    step_type=step_data.get("step_type", "general"),
                    description=step_data.get("description", ""),
                    dependencies=step_data.get("dependencies", []),
                    estimated_duration=step_data.get("estimated_duration", 0.0),
                    timeout=step_data.get("timeout", 300.0),
                    metadata=step_data.get("metadata", {})
                )
                workflow_steps.append(step)

            workflow = V2Workflow(
                workflow_id=workflow_id,
                name=name,
                description=description,
                steps=workflow_steps,
                created_at=datetime.now().isoformat(),
                status="created"
            )

            self.workflows[workflow_id] = workflow
            self.logger.info(f"Created workflow: {workflow_id} - {name}")
            
            return workflow_id

        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            raise

    def get_workflow(self, workflow_id: str) -> Optional[V2Workflow]:
        """Get workflow by ID"""
        return self.workflows.get(workflow_id)

    def update_workflow_status(self, workflow_id: str, status: str):
        """Update workflow status"""
        if workflow_id in self.workflows:
            self.workflows[workflow_id].status = status
            self.logger.info(f"Updated workflow {workflow_id} status to: {status}")

    def list_workflows(self) -> List[str]:
        """List all workflow IDs"""
        return list(self.workflows.keys())

    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get workflow summary statistics"""
        return {
            "total_workflows": len(self.workflows),
            "active_workflows": len(self.active_workflows),
            "workflow_types": list(set(w.status for w in self.workflows.values())),
            "workflow_names": [w.name for w in self.workflows.values()]
        }


class WorkflowOptimizationManager:
    """Manages workflow optimization - single responsibility: optimization management"""
    
    def __init__(self):
        self.optimization_history: List[WorkflowOptimization] = []
        self.running = False
        self.logger = logging.getLogger(f"{__name__}.WorkflowOptimizationManager")

    def add_optimization_result(self, optimization: WorkflowOptimization):
        """Add optimization result to history"""
        self.optimization_history.append(optimization)
        self.logger.info(f"Added optimization result: {optimization.optimization_id}")

    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get optimization summary"""
        try:
            total_optimizations = len(self.optimization_history)
            if total_optimizations == 0:
                return {"total_optimizations": 0, "average_improvement": 0.0}

            recent_optimizations = [
                o for o in self.optimization_history
                if datetime.fromisoformat(o.optimization_timestamp) > 
                   datetime.now() - timedelta(hours=24)
            ]

            avg_improvement = sum(
                o.improvement_percentage for o in self.optimization_history
            ) / total_optimizations

            return {
                "total_optimizations": total_optimizations,
                "recent_optimizations": len(recent_optimizations),
                "average_improvement": round(avg_improvement, 2),
                "optimization_active": self.running
            }

        except Exception as e:
            self.logger.error(f"Failed to get optimization summary: {e}")
            return {"error": str(e)}

    def start_optimization(self):
        """Start optimization process"""
        self.running = True
        self.logger.info("Workflow optimization started")

    def stop_optimization(self):
        """Stop optimization process"""
        self.running = False
        self.logger.info("Workflow optimization stopped")


# ============================================================================
# CLI INTERFACE - Single Responsibility: Command-line testing
# ============================================================================

def run_smoke_test():
    """Run basic functionality test for workflow core"""
    try:
        # Test WorkflowDefinitionManager
        def_manager = WorkflowDefinitionManager()
        assert "agent_onboarding" in def_manager.list_workflow_types()
        
        # Test WorkflowStateManager
        state_manager = WorkflowStateManager()
        steps = [{"id": "step1", "name": "Test Step", "step_type": "test"}]
        workflow_id = state_manager.create_workflow("Test", "Test Desc", steps)
        assert workflow_id in state_manager.list_workflows()
        
        # Test WorkflowOptimizationManager
        opt_manager = WorkflowOptimizationManager()
        summary = opt_manager.get_optimization_summary()
        assert summary["total_optimizations"] == 0
        
        print("✅ WorkflowCore smoke test passed!")
        return True
        
    except Exception as e:
        print(f"❌ WorkflowCore smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
