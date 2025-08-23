"""
AI & ML Integration Package
Agent_Cellphone_V2_Repository

This package provides:
- AI development environment setup
- ML framework management
- API key management
- CodeCrafter integration
- AI-powered development tools
"""

__version__ = "1.0.0"
__author__ = "AI & ML Integration Specialist"
__description__ = "AI & ML Integration for Agent_Cellphone_V2_Repository"

# Core AI/ML components (existing comprehensive infrastructure)
from .core import AIManager, MLFramework, ModelManager, WorkflowAutomation

# ML Frameworks (existing comprehensive implementations)
from .ml_frameworks import (
    MLFrameworkManager,
    PyTorchFramework,
    TensorFlowFramework,
    ScikitLearnFramework,
    JAXFramework,
)

# AI-powered development tools (existing implementations)
from .code_crafter import (
    CodeCrafter,
    CodeGenerationRequest,
    CodeGenerationResult,
    CodeAnalysis,
    get_code_crafter,
)

from .dev_workflow import (
    AIDevWorkflow,
    WorkflowStep,
    WorkflowResult,
    ProjectAnalysis,
    get_ai_dev_workflow,
)

from .intelligent_reviewer import (
    IntelligentReviewer,
    ReviewIssue,
    CodeReview,
    SecurityVulnerability,
    get_intelligent_reviewer,
)

# ML Robot Maker (existing implementation)
from .ml_robot_maker import (
    MLRobotMaker,
    MLTask,
    MLModelBlueprint,
    MLExperiment,
    get_ml_robot_maker,
)

# API integrations (existing implementations)
from .integrations import OpenAIIntegration, AnthropicIntegration, PyTorchIntegration

# Utilities and helpers (existing implementations)
from .utils import config_loader, logger_setup, performance_monitor

# Testing and validation (existing implementations)
from .testing import AITestRunner, ModelValidator, QualityAssurance

# API key management (existing implementation)
from .api_key_manager import (
    APIKeyManager,
    get_api_key_manager,
)

__all__ = [
    # Core components
    "AIManager",
    "MLFramework",
    "ModelManager",
    "WorkflowAutomation",
    # ML Frameworks
    "MLFrameworkManager",
    "PyTorchFramework",
    "TensorFlowFramework",
    "ScikitLearnFramework",
    "JAXFramework",
    # AI-powered development tools
    "CodeCrafter",
    "CodeGenerationRequest",
    "CodeGenerationResult",
    "CodeAnalysis",
    "get_code_crafter",
    "AIDevWorkflow",
    "WorkflowStep",
    "WorkflowResult",
    "ProjectAnalysis",
    "get_ai_dev_workflow",
    "IntelligentReviewer",
    "ReviewIssue",
    "CodeReview",
    "SecurityVulnerability",
    "get_intelligent_reviewer",
    # ML Robot Maker
    "MLRobotMaker",
    "MLTask",
    "MLModelBlueprint",
    "MLExperiment",
    "get_ml_robot_maker",
    # API integrations
    "OpenAIIntegration",
    "AnthropicIntegration",
    "PyTorchIntegration",
    # Utilities
    "config_loader",
    "logger_setup",
    "performance_monitor",
    # Testing
    "AITestRunner",
    "ModelValidator",
    "QualityAssurance",
    # API key management
    "APIKeyManager",
    "get_api_key_manager",
]
