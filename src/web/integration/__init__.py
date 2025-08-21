"""
Cross-Agent Integration Package
Agent_Cellphone_V2_Repository - Multi-Agent Web Integration

This package provides the infrastructure for cross-agent communication,
coordination, and integration across all agent systems.
"""

# Core communication classes
from .cross_agent_protocol import (
    CrossAgentCommunicator,
    AgentMessage,
    AgentResponse,
    AgentStatus,
    MessagePriority,
    MessageValidator,
    AuthenticationManager
)

# Integration utilities
from .cross_agent_protocol import (
    create_flask_integration,
    create_fastapi_integration,
    create_agent_communicator,
    validate_message_format,
    create_heartbeat_message
)

# Protocol constants
from .cross_agent_protocol import (
    PROTOCOL_VERSION,
    MESSAGE_TYPES,
    COMMAND_CATEGORIES
)

__version__ = "1.0.0"
__author__ = "Agent_Cellphone_V2_Repository Team"
__description__ = "Cross-Agent Communication and Integration System"

__all__ = [
    # Core communication classes
    "CrossAgentCommunicator",
    "AgentMessage", 
    "AgentResponse",
    "AgentStatus",
    "MessagePriority",
    "MessageValidator",
    "AuthenticationManager",
    
    # Integration utilities
    "create_flask_integration",
    "create_fastapi_integration", 
    "create_agent_communicator",
    "validate_message_format",
    "create_heartbeat_message",
    
    # Protocol constants
    "PROTOCOL_VERSION",
    "MESSAGE_TYPES",
    "COMMAND_CATEGORIES"
]

# Convenience functions for quick setup
def create_agent_communication_system(agent_id: str, config: dict = None):
    """Create a complete agent communication system"""
    from .cross_agent_protocol import CrossAgentCommunicator
    return CrossAgentCommunicator(agent_id, config)

def setup_flask_agent_api(communicator, app=None):
    """Setup Flask app with agent communication endpoints"""
    from .cross_agent_protocol import create_flask_integration
    if app is None:
        from flask import Flask
        app = Flask(__name__)
    
    # Merge the communicator endpoints
    agent_app = create_flask_integration(communicator)
    
    # Register the routes
    for rule in agent_app.url_map.iter_rules():
        app.add_url_rule(
            rule.rule,
            rule.endpoint,
            view_func=agent_app.view_functions[rule.endpoint],
            methods=rule.methods
        )
    
    return app

def setup_fastapi_agent_api(communicator, app=None):
    """Setup FastAPI app with agent communication endpoints"""
    from .cross_agent_protocol import create_fastapi_integration
    if app is None:
        from fastapi import FastAPI
        app = FastAPI()
    
    # Merge the communicator endpoints
    agent_app = create_fastapi_integration(communicator)
    
    # Include the agent router
    app.include_router(agent_app.router, prefix="/agent-api")
    
    return app

import logging
logger = logging.getLogger(__name__)
logger.info(f"Cross-Agent Integration package initialized - version {__version__}")
logger.info("Available classes: %s", ", ".join(__all__))
