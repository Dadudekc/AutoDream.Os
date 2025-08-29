"""Workflow operations for AIManager."""

from datetime import datetime
from typing import List, Optional

from ..workflows import MLWorkflow


class WorkflowOpsMixin:
    """Mixin providing workflow management operations."""

    active_workflows: dict
    workflow_executions: list
    engine: any

    def create_workflow(self, name: str, description: str) -> MLWorkflow:
        """Create a new ML workflow."""
        try:
            start_time = datetime.now()
            workflow = MLWorkflow(name=name, description=description)
            self.active_workflows[name] = workflow
            workflow_record = {
                "timestamp": datetime.now().isoformat(),
                "workflow_name": name,
                "description": description,
                "steps_count": 0,
            }
            self.workflow_executions.append(workflow_record)
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("create_workflow", True, operation_time)
            self.logger.info(f"Created workflow: {name}")
            return workflow
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error creating workflow {name}: {e}")
            self.record_operation("create_workflow", False, 0.0)
            raise

    def get_workflow(self, name: str) -> Optional[MLWorkflow]:
        """Get a workflow by name."""
        try:
            workflow = self.active_workflows.get(name)
            self.record_operation("get_workflow", True, 0.0)
            return workflow
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error getting workflow {name}: {e}")
            self.record_operation("get_workflow", False, 0.0)
            return None

    def list_workflows(self) -> List[str]:
        """List all active workflow names."""
        try:
            workflow_names = list(self.active_workflows.keys())
            self.record_operation("list_workflows", True, 0.0)
            return workflow_names
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error listing workflows: {e}")
            self.record_operation("list_workflows", False, 0.0)
            return []

    def execute_workflow(self, workflow_name: str) -> bool:
        """Execute a workflow."""
        try:
            start_time = datetime.now()
            workflow = self.get_workflow(workflow_name)
            if not workflow:
                self.logger.error(f"Workflow not found: {workflow_name}")
                self.record_operation("execute_workflow", False, 0.0)
                return False

            result = self.engine.execute_workflow(workflow)
            if result:
                for record in self.workflow_executions:
                    if record.get("workflow_name") == workflow_name:
                        record["status"] = "completed"
                        record["completed_at"] = datetime.now().isoformat()
                        break
                self.logger.info(f"Workflow completed: {workflow_name}")
            else:
                self.logger.error(f"Workflow execution failed: {workflow_name}")

            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("execute_workflow", result, operation_time)
            return result
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Workflow execution failed: {workflow_name} - {e}")
            self.record_operation("execute_workflow", False, 0.0)
            return False
