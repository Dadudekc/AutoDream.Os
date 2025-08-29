"""
Web Automation Package for Agent_Cellphone_V2_Repository
Provides comprehensive web automation, website generation, and testing capabilities
"""

from .web_automation_engine import (
    WebAutomationEngine,
    AutomationConfig,
    create_automation_engine,
    run_automation_task,
)

from .website_generator import (
    WebsiteGenerator,
    WebsiteConfig,
    PageConfig,
    ComponentConfig,
    create_website_generator,
    generate_basic_website,
)

from .automation_test_suite import AutomationTestSuite, run_automation_tests_cli

from .automation_orchestrator import (
    AutomationOrchestrator,
    OrchestrationConfig,
    create_automation_orchestrator,
    run_automation_pipeline,
    EXAMPLE_PIPELINES,
)

__version__ = "1.0.0"
__author__ = "Agent_Cellphone_V2_Repository Team"

__all__ = [
    # Core classes
    "WebAutomationEngine",
    "WebsiteGenerator",
    "AutomationTestSuite",
    "AutomationOrchestrator",
    # Configuration classes
    "AutomationConfig",
    "WebsiteConfig",
    "PageConfig",
    "ComponentConfig",
    "OrchestrationConfig",
    # Factory functions
    "create_automation_engine",
    "create_website_generator",
    "create_automation_orchestrator",
    # Utility functions
    "run_automation_task",
    "generate_basic_website",
    "run_automation_pipeline",
    "run_automation_tests_cli",
    # Constants
    "EXAMPLE_PIPELINES",
]
