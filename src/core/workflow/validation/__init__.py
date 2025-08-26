"""
Workflow Validation - Unified Validation Framework Integration

This module provides workflow-specific validation capabilities by integrating
with the existing Unified Validation Framework. It extends the base validation
system with workflow-specific rules and validation logic.

Components:
- WorkflowValidator: Workflow-specific validation rules
- WorkflowValidationManager: Workflow validation coordination
- Real-time validation during workflow execution
"""

from .workflow_validator import WorkflowValidator
from .workflow_validation_manager import WorkflowValidationManager

__all__ = [
    'WorkflowValidator',
    'WorkflowValidationManager'
]

__version__ = "2.0.0"
__author__ = "Agent-1 (Core Engine Development)"
__description__ = "Workflow validation integration with Unified Validation Framework"
