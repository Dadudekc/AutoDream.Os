"""
AI/ML Package - Modularized Components
Agent-2: AI & ML Framework Integration

This package contains modularized AI/ML components extracted from the original monolithic core.py.
Each module focuses on a specific responsibility for better maintainability and testability.
"""

# Import all modularized components
from .models import AIModel, MLWorkflow
from .ai_manager import AIManager
from .ml_framework import MLFramework
from .model_manager import ModelManager
from .workflow_automation import WorkflowAutomation

# Re-export main classes for easy access
__all__ = [
    'AIModel',
    'MLWorkflow', 
    'AIManager',
    'MLFramework',
    'ModelManager',
    'WorkflowAutomation'
]

# Version information
__version__ = "2.0.0"
__description__ = "Modularized AI/ML Components"

# Convenience function to create a complete AI/ML system
def create_ai_ml_system(
    config_path: str = None,
    models_dir: str = None
) -> tuple[AIManager, ModelManager, WorkflowAutomation]:
    """
    Create a complete AI/ML system with all components initialized.
    
    Args:
        config_path: Path to AI/ML configuration file
        models_dir: Directory for model storage
        
    Returns:
        Tuple of (AIManager, ModelManager, WorkflowAutomation)
    """
    # Create managers
    ai_manager = AIManager(config_path=config_path)
    model_manager = ModelManager(models_dir=models_dir)
    
    # Create workflow automation
    workflow_automation = WorkflowAutomation(ai_manager, model_manager)
    
    return ai_manager, model_manager, workflow_automation
