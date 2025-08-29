"""
Workflow Interface - Abstract Workflow Execution
Captain Agent-3: FSM Core V2 Modularization
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IWorkflowManager(ABC):
    """Abstract interface for workflow management"""
    
    @abstractmethod
    def create_workflow(self, template: str, workflow_id: str, initial_state: str) -> str:
        """Create new workflow instance"""
        pass
    
    @abstractmethod
    def start_workflow(self, workflow_id: str, context: Dict[str, Any]) -> bool:
        """Start workflow execution"""
        pass
    
    @abstractmethod
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow status"""
        pass

class IWorkflowExecutor(ABC):
    """Abstract interface for workflow execution"""
    
    @abstractmethod
    def execute_step(self, workflow_id: str, step_id: str) -> bool:
        """Execute workflow step"""
        pass
    
    @abstractmethod
    def pause_workflow(self, workflow_id: str) -> bool:
        """Pause workflow execution"""
        pass
    
    @abstractmethod
    def resume_workflow(self, workflow_id: str) -> bool:
        """Resume workflow execution"""
        pass
