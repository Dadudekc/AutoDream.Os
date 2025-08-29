"""
Core AI/ML Components - Modularized Version
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

This is the main entry point that imports and coordinates all AI/ML modules.
The original monolithic file has been broken down into focused, maintainable modules.
"""

# Import all modularized components
from .models import AIModel, MLWorkflow
from .ai_manager import AIManager
from .ml_framework import MLFramework
from .model_manager import ModelManager
from .workflow_automation import WorkflowAutomation

# Re-export main classes for backward compatibility
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
__description__ = "Modularized AI/ML Core Components"

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

# Example usage and documentation
if __name__ == "__main__":
    print("AI/ML Core Components - Modularized Version")
    print("=" * 50)
    print(f"Version: {__version__}")
    print(f"Description: {__description__}")
    print("\nAvailable Components:")
    print("- AIModel: AI model configuration and metadata")
    print("- MLWorkflow: Machine learning workflow definition")
    print("- AIManager: Central AI management and coordination")
    print("- MLFramework: Abstract base class for ML frameworks")
    print("- ModelManager: Model lifecycle and management")
    print("- WorkflowAutomation: Automated workflow execution")
    print("\nUse create_ai_ml_system() to initialize a complete system.")
