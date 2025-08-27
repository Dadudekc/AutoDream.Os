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
from .models import AIModel
from .workflows import MLWorkflow, WorkflowAutomation
from .engine import AIEngine
from .inference import AIManager
from .training import MLFramework
from .model_loading import ModelManager

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
from .template_generation import TemplateGenerator
from .code_synthesis import CodeSynthesizer
from .validation import CodeValidator
from .deployment import CodeDeployer

from .dev_workflow_manager import DevWorkflowManager, WorkflowStep, WorkflowResult
from .dev_workflow_ai_processor import AIProcessor, ProjectAnalysis
from .dev_workflow_coordinator import WorkflowCoordinator
from .dev_workflow_config import WorkflowConfig, load_workflow_config
from .dev_workflow import AIDevWorkflow, get_ai_dev_workflow

from .intelligent_reviewer import (
    IntelligentReviewer,
    ReviewIssue,
    CodeReview,
    SecurityVulnerability,
    get_intelligent_reviewer,
)
from .intelligent_review_core import ReviewCore
from .intelligent_review_ai_analysis import AIAnalyzer
from .intelligent_review_reporting import (
    generate_recommendations,
    calculate_overall_score,
    generate_review_report,
)
from .intelligent_review_config import SECURITY_PATTERNS, QUALITY_PATTERNS

# ML Robot system (modular implementation)
from .ml_robot_config import MLTask, MLModelBlueprint, MLExperiment
from .ml_robot_creator import MLRobotCreator
from .ml_robot_processor import MLRobotProcessor
from .ml_robot_validator import validate_blueprint_config
from .ml_robot_maker import MLRobotMaker, get_ml_robot_maker

# AI Agent learner (modular implementation)
from .ai_agent_learner import (
    AIAgentLearner,
    LearnerCore,
    LearningGoal,
    LearningProgress,
    KnowledgeBase,
    KnowledgeItem,
    Skill,
    SkillManager,
)

# API integrations (existing implementations)
from .integrations import OpenAIIntegration, AnthropicIntegration, PyTorchIntegration

# Utilities and helpers (existing implementations)
from .utils import config_loader, logger_setup, performance_monitor

# Testing and validation
from .testing import DatasetPreparer, ModelEvaluator, TestReporter, CleanupManager

# API key management (existing implementation)
from .api_key_manager import (
    APIKeyManager,
    get_api_key_manager,
)

# Agent coordination
from .ai_agent_coordinator import AIAgentCoordinator
from .ai_agent_tasks import AIAgentTask

# Agent optimizer modules
from .ai_agent_optimizer_core import AIAgentOptimizerCore
from .ai_agent_performance_tuner import AIAgentPerformanceTuner
from ..core.managers.ai_agent_orchestrator import AIAgentOrchestrator
from .ai_agent_optimizer import AIAgentOptimizer

__all__ = [
    # Core components
    "AIModel",
    "MLWorkflow",
    "WorkflowAutomation",
    "AIEngine",
    "AIManager",
    "MLFramework",
    "ModelManager",
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
    "TemplateGenerator",
    "CodeSynthesizer",
    "CodeValidator",
    "CodeDeployer",
    "DevWorkflowManager",
    "AIProcessor",
    "WorkflowCoordinator",
    "WorkflowConfig",
    "load_workflow_config",
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
    "ReviewCore",
    "AIAnalyzer",
    "generate_recommendations",
    "calculate_overall_score",
    "generate_review_report",
    "SECURITY_PATTERNS",
    "QUALITY_PATTERNS",
    # ML Robot Maker
    "MLRobotCreator",
    "MLRobotProcessor",
    "validate_blueprint_config",
    "MLRobotMaker",
    "MLTask",
    "MLModelBlueprint",
    "MLExperiment",
    "get_ml_robot_maker",
    # AI Agent learner
    "AIAgentLearner",
    "LearnerCore",
    "LearningGoal",
    "LearningProgress",
    "KnowledgeBase",
    "KnowledgeItem",
    "Skill",
    "SkillManager",
    # API integrations
    "OpenAIIntegration",
    "AnthropicIntegration",
    "PyTorchIntegration",
    # Utilities
    "config_loader",
    "logger_setup",
    "performance_monitor",
    # Testing
    "DatasetPreparer",
    "ModelEvaluator",
    "TestReporter",
    "CleanupManager",
    # API key management
    "APIKeyManager",
    "get_api_key_manager",
    # Agent coordination
    "AIAgentCoordinator",
    "AIAgentTask",
    # Agent optimizer
    "AIAgentOptimizer",
    "AIAgentOptimizerCore",
    "AIAgentPerformanceTuner",
    "AIAgentOrchestrator",
]
