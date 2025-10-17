"""
Data Validation Functions for Swarm Website SSOT Layer

Ensures data integrity and consistency across all sources.
"""

from typing import Dict, List
from datetime import datetime, timedelta


# ============================================================================
# AGENT STATUS VALIDATION
# ============================================================================

def validate_agent_status(data: Dict) -> bool:
    """
    Validate agent status data structure and content.
    
    Args:
        data: Agent status dict
        
    Returns:
        True if valid, False otherwise
    """
    # Required fields
    required_fields = [
        'agent_id',
        'status',
        'last_updated',
        'current_mission',
        'progress_percentage'
    ]
    
    for field in required_fields:
        if field not in data:
            return False
    
    # Validate status enum
    valid_statuses = ['ACTIVE', 'REST', 'BLOCKED', 'UNKNOWN']
    if data['status'] not in valid_statuses:
        return False
    
    # Validate progress range
    progress = data.get('progress_percentage', 0)
    if not isinstance(progress, (int, float)) or not (0 <= progress <= 100):
        return False
    
    # Validate timestamp format
    try:
        if 'T' in data['last_updated']:
            datetime.fromisoformat(data['last_updated'])
        else:
            datetime.strptime(data['last_updated'], "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return False
    
    return True


# ============================================================================
# REPO DATA VALIDATION
# ============================================================================

def validate_repo_data(data: Dict) -> bool:
    """
    Validate GitHub repo analysis data.
    
    Args:
        data: Repo analysis dict
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['repo_id', 'repo_name', 'status']
    
    for field in required_fields:
        if field not in data:
            return False
    
    # Validate repo_id range
    repo_id = data.get('repo_id')
    if not isinstance(repo_id, int) or not (1 <= repo_id <= 75):
        return False
    
    # Validate ROI if present
    if 'roi' in data:
        roi = data['roi']
        if not isinstance(roi, (int, float)) or roi < 0:
            return False
    
    return True


# ============================================================================
# DEBATE DATA VALIDATION
# ============================================================================

def validate_debate_data(data: Dict) -> bool:
    """
    Validate debate data structure.
    
    Args:
        data: Debate dict
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['debate_id', 'title', 'votes']
    
    for field in required_fields:
        if field not in data:
            return False
    
    # Validate votes structure
    votes = data.get('votes', {})
    if not isinstance(votes, dict):
        return False
    
    return True


# ============================================================================
# DATA CONSISTENCY CHECKS
# ============================================================================

def ensure_data_consistency(agents: List[Dict]) -> Dict:
    """
    Ensure SSOT consistency across all data.
    
    Args:
        agents: List of agent status dicts
        
    Returns:
        Dict with consistency check results
    """
    issues = []
    
    # 1. Agent count consistency
    expected_agents = 8
    if len(agents) != expected_agents:
        issues.append(f"Expected {expected_agents} agents, found {len(agents)}")
    
    # 2. Unique agent IDs
    agent_ids = [a.get('agent_id') for a in agents]
    if len(agent_ids) != len(set(agent_ids)):
        issues.append("Duplicate agent IDs detected")
    
    # 3. Points consistency
    points_list = [a.get('points_total', 0) for a in agents]
    if any(p < 0 for p in points_list):
        issues.append("Negative points detected")
    
    # 4. Status consistency
    for agent in agents:
        if not validate_agent_status(agent):
            issues.append(f"Invalid status data for {agent.get('agent_id')}")
    
    return {
        'is_consistent': len(issues) == 0,
        'issues': issues,
        'checked_at': datetime.now().isoformat()
    }

