"""AI & ML Integration Package.

This trimmed initializer exposes the core interfaces used across the
codebase while avoiding heavy optional dependencies during test
collection.
"""

from .core import AIManager, MLFramework, ModelManager, WorkflowAutomation
from .ml_frameworks import (
    MLFrameworkManager,
    PyTorchFramework,
    TensorFlowFramework,
    ScikitLearnFramework,
    JAXFramework,
)

__all__ = [
    "AIManager",
    "MLFramework",
    "ModelManager",
    "WorkflowAutomation",
    "MLFrameworkManager",
    "PyTorchFramework",
    "TensorFlowFramework",
    "ScikitLearnFramework",
    "JAXFramework",
]
