"""
AI/ML Models and Workflows
Extracted from core.py for modularization

Contains:
- AIModel: AI model configuration and metadata
- MLWorkflow: Machine learning workflow definition
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime


@dataclass
class AIModel:
    """AI model configuration and metadata"""

    name: str
    provider: str
    model_id: str
    version: str
    capabilities: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "provider": self.provider,
            "model_id": self.model_id,
            "version": self.version,
            "capabilities": self.capabilities,
            "parameters": self.parameters,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class MLWorkflow:
    """Machine learning workflow definition"""

    name: str
    description: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)

    def add_step(
        self, step_name: str, step_type: str, parameters: Dict[str, Any]
    ) -> None:
        """Add a step to the workflow"""
        step = {
            "name": step_name,
            "type": step_type,
            "parameters": parameters,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
        }
        self.steps.append(step)

    def update_step_status(self, step_name: str, status: str) -> bool:
        """Update the status of a workflow step"""
        for step in self.steps:
            if step["name"] == step_name:
                step["status"] = status
                return True
        return False
