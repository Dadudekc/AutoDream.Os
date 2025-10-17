"""
Swarm Website SSOT Data Integration Layer

Created by: Agent-8 (SSOT & System Integration Specialist)
Purpose: Single source of truth for swarm website data
Status: Active Development - Cycle 2
"""

from .data_loader import (
    load_agent_status,
    load_all_agents,
    load_github_repos,
    load_debates,
    get_swarm_overview
)

from .validators import (
    validate_agent_status,
    validate_repo_data,
    validate_debate_data,
    ensure_data_consistency
)

__all__ = [
    # Data Loading
    'load_agent_status',
    'load_all_agents',
    'load_github_repos',
    'load_debates',
    'get_swarm_overview',
    
    # Validation
    'validate_agent_status',
    'validate_repo_data',
    'validate_debate_data',
    'ensure_data_consistency',
]

__version__ = '0.1.0'
__author__ = 'Agent-8 SSOT Specialist'

