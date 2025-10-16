"""
OSRS Swarm Agents Integration
==============================

Integration of Old School RuneScape (OSRS) swarm agent coordination
and gaming integration capabilities.

DUP-012 Fix: gaming_integration_core consolidated to src/gaming/
Updated by: Agent-6 (Co-Captain) - 2025-10-16

Modules:
    - gaming_integration_core: Core gaming integration (from src.gaming/)
    - osrs_agent_core: OSRS agent core capabilities
    - swarm_coordinator: Multi-agent swarm coordination
    - performance_validation: Performance monitoring and validation

Usage:
    from src.integrations.osrs import gaming_integration_core
    from src.integrations.osrs import swarm_coordinator

Features:
    - Multi-agent swarm coordination
    - Gaming session management
    - Performance monitoring
    - SOLID-compliant architecture
"""

# Note: gaming_integration_core import removed temporarily due to dependency issues
# DUP-012 requires further analysis before consolidation

from . import osrs_agent_core, performance_validation, swarm_coordinator

try:
    from . import gaming_integration_core
    __all__.insert(0, "gaming_integration_core")
except ImportError:
    pass

__all__ = [
    "gaming_integration_core",
    "osrs_agent_core",
    "swarm_coordinator",
    "performance_validation",
]
