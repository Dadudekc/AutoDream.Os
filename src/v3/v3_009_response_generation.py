"""
V3-009 Response Generation System
Intelligent response generation for agent communication
Refactored into modular components for V2 compliance
"""

# Import all components from refactored modules
from .v3_009_response_generation_core import (
    GeneratedResponse,
    ResponseContext,
    ResponseFormat,
    ResponseGeneratorCore,
    ResponseRequest,
    ResponseTemplate,
    ResponseTone,
)
from .v3_009_response_generation_main import (
    AdvancedResponseGenerator,
    ResponseGenerationService,
    create_response_generation_service,
    generate_agent_response,
)

# Re-export main classes for backward compatibility
__all__ = [
    "ResponseTone",
    "ResponseFormat",
    "ResponseTemplate",
    "ResponseContext",
    "ResponseRequest",
    "GeneratedResponse",
    "ResponseGeneratorCore",
    "AdvancedResponseGenerator",
    "ResponseGenerationService",
    "create_response_generation_service",
    "generate_agent_response",
]
