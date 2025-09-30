#!/usr/bin/env python3
"""
ML Training Infrastructure Tool
==============================

Infrastructure automation for ML training workloads and environments.
Refactored into modular components for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

# Import all components from refactored modules
from .ml_training_infrastructure_tool_core import (
    FrameworkType,
    ResourceType,
    TrainingEnvironment,
    TrainingInfrastructureConfig,
    TrainingInfrastructureCore,
    TrainingJob,
    TrainingJobStatus,
    TrainingResource,
    TrainingStatus,
)
from .ml_training_infrastructure_tool_main import MLTrainingInfrastructureTool, main
from .ml_training_infrastructure_tool_utils import (
    FileManager,
    JobQueueManager,
    ResourceManager,
    TrainingSimulator,
)

# Re-export main classes for backward compatibility
__all__ = [
    # Core classes
    "TrainingStatus",
    "ResourceType",
    "FrameworkType",
    "TrainingResource",
    "TrainingEnvironment",
    "TrainingJob",
    "TrainingJobStatus",
    "TrainingInfrastructureConfig",
    "TrainingInfrastructureCore",
    # Utility classes
    "TrainingSimulator",
    "ResourceManager",
    "JobQueueManager",
    "FileManager",
    # Main tool
    "MLTrainingInfrastructureTool",
    "main",
]


# For direct execution
if __name__ == "__main__":
    main()
