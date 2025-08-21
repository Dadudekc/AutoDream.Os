"""
Unified Web Portal Package
Agent_Cellphone_V2_Repository - Multi-Agent Web Integration

This package provides the unified web portal architecture that serves as
the central interface for all agent systems.
"""

# Core portal classes
from .unified_portal import (
    UnifiedPortal,
    PortalConfig,
    AgentPortalInfo,
    PortalNavigation,
    PortalSection,
    AgentDashboard
)

# Portal applications
from .unified_portal import (
    FlaskPortalApp,
    FastAPIPortalApp,
    PortalFactory
)

# Utility functions
from .unified_portal import (
    create_portal,
    create_flask_portal_app,
    create_fastapi_portal_app
)

__version__ = "1.0.0"
__author__ = "Agent_Cellphone_V2_Repository Team"
__description__ = "Unified Web Portal Architecture"

__all__ = [
    # Core portal classes
    "UnifiedPortal",
    "PortalConfig", 
    "AgentPortalInfo",
    "PortalNavigation",
    "PortalSection",
    "AgentDashboard",
    
    # Portal applications
    "FlaskPortalApp",
    "FastAPIPortalApp",
    "PortalFactory",
    
    # Utility functions
    "create_portal",
    "create_flask_portal_app",
    "create_fastapi_portal_app"
]

# Convenience functions for quick setup
def create_unified_portal(backend_type: str = 'flask', config: dict = None):
    """Create a unified portal with specified backend"""
    from .unified_portal import PortalFactory
    return PortalFactory.create_unified_portal(backend_type, config)

def create_portal_with_agents(agent_configs: list, backend_type: str = 'flask', config: dict = None):
    """Create a portal and register agents"""
    from .unified_portal import UnifiedPortal, AgentPortalInfo, AgentDashboard
    
    # Create portal
    portal = UnifiedPortal(config.get('portal') if config else None)
    
    # Register agents
    for agent_config in agent_configs:
        agent_info = AgentPortalInfo(
            agent_id=agent_config['agent_id'],
            name=agent_config['name'],
            description=agent_config.get('description', ''),
            dashboard_type=AgentDashboard(agent_config.get('dashboard_type', 'integration')),
            capabilities=agent_config.get('capabilities', []),
            status=agent_config.get('status', 'offline'),
            integration_status=agent_config.get('integration_status', 'pending')
        )
        portal.register_agent(agent_info)
    
    # Create application
    if backend_type.lower() == 'fastapi':
        return create_fastapi_portal_app(portal, config)
    else:
        return create_flask_portal_app(portal, config)

def setup_portal_integration(portal, agent_systems: dict):
    """Setup portal integration with existing agent systems"""
    from .unified_portal import AgentPortalInfo, AgentDashboard
    
    for agent_id, agent_system in agent_systems.items():
        # Create agent portal info
        agent_info = AgentPortalInfo(
            agent_id=agent_id,
            name=agent_system.get('name', agent_id),
            description=agent_system.get('description', ''),
            dashboard_type=AgentDashboard(agent_system.get('dashboard_type', 'integration')),
            capabilities=agent_system.get('capabilities', []),
            status=agent_system.get('status', 'offline'),
            integration_status=agent_system.get('integration_status', 'pending'),
            web_interface_url=agent_system.get('web_interface_url'),
            api_endpoints=agent_system.get('api_endpoints', []),
            custom_components=agent_system.get('custom_components', [])
        )
        
        # Register agent
        portal.register_agent(agent_info)
        
        # Setup integration if available
        if agent_system.get('web_interface_url'):
            portal.process_agent_integration(agent_id, "web_interface", {
                'web_interface_url': agent_system['web_interface_url']
            })
        
        if agent_system.get('api_endpoints'):
            portal.process_agent_integration(agent_id, "api_endpoints", {
                'api_endpoints': agent_system['api_endpoints']
            })
        
        if agent_system.get('custom_components'):
            portal.process_agent_integration(agent_id, "custom_components", {
                'custom_components': agent_system['custom_components']
            })

import logging
logger = logging.getLogger(__name__)
logger.info(f"Unified Web Portal package initialized - version {__version__}")
logger.info("Available classes: %s", ", ".join(__all__))
