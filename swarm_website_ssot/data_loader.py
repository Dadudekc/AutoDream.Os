"""
Data Loading Utilities for Swarm Website SSOT Layer

Loads data from various sources with validation and standardization.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

# ============================================================================
# AGENT STATUS LOADING
# ============================================================================

def load_agent_status(agent_id: str) -> Dict:
    """
    Load status.json for specific agent with SSOT validation.
    
    Args:
        agent_id: Agent identifier (e.g., "Agent-8")
        
    Returns:
        Dict with agent status data + derived fields
        
    Raises:
        FileNotFoundError: If agent status file doesn't exist
        ValueError: If data validation fails
    """
    status_file = Path(f"agent_workspaces/{agent_id}/status.json")
    
    if not status_file.exists():
        raise FileNotFoundError(f"Status file not found for {agent_id}")
    
    with open(status_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add derived fields
    data['is_live'] = _check_if_live(data.get('last_updated'))
    data['status_health'] = _compute_status_health(data)
    data['gas_level'] = _compute_gas_level(data)
    
    return data


def load_all_agents() -> List[Dict]:
    """
    Load status for all 8 agents.
    
    Returns:
        List of agent status dicts, sorted by agent_id
    """
    agents = []
    
    for i in range(1, 9):  # Agent-1 through Agent-8
        agent_id = f"Agent-{i}"
        try:
            agent_data = load_agent_status(agent_id)
            # Ensure agent_id is present
            if 'agent_id' not in agent_data:
                agent_data['agent_id'] = agent_id
            agents.append(agent_data)
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            # Agent status file missing or invalid - use placeholder
            agents.append({
                'agent_id': agent_id,
                'agent_name': f"{agent_id} (Unavailable)",
                'status': 'UNKNOWN',
                'is_live': False,
                'status_health': 'ERROR',
                'gas_level': 0,
                'points_total': 0,
                'error': f'Status unavailable: {type(e).__name__}'
            })
    
    return sorted(agents, key=lambda x: x.get('agent_id', 'Unknown'))


def _check_if_live(last_updated: Optional[str]) -> bool:
    """
    Check if agent is live (updated within last 30 minutes).
    
    This is CRITICAL for stop detection!
    """
    if not last_updated:
        return False
    
    try:
        # Parse timestamp (handles various formats)
        if 'T' in last_updated:
            timestamp = datetime.fromisoformat(last_updated)
        else:
            timestamp = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
        
        # Check if within 30 minutes
        age = datetime.now() - timestamp
        return age < timedelta(minutes=30)
    
    except (ValueError, TypeError):
        return False


def _compute_status_health(data: Dict) -> str:
    """
    Compute overall health status: HEALTHY, WARNING, STOPPED, ERROR.
    """
    if not data.get('is_live'):
        return 'STOPPED'
    
    if data.get('status') == 'BLOCKED':
        return 'WARNING'
    
    if data.get('status') == 'ACTIVE':
        return 'HEALTHY'
    
    return 'WARNING'


def _compute_gas_level(data: Dict) -> int:
    """
    Compute gas level (0-100) based on activity and recent updates.
    
    Higher gas = more recent activity, more achievements, more energy.
    """
    base_gas = data.get('energy_level', 50)
    
    # Boost for being live
    if data.get('is_live'):
        base_gas += 20
    
    # Boost for recent achievements
    achievements = data.get('achievements', [])
    if len(achievements) > 0:
        base_gas += min(len(achievements) * 5, 30)
    
    # Cap at 100
    return min(base_gas, 100)


# ============================================================================
# GITHUB REPOS LOADING
# ============================================================================

def load_github_repos() -> List[Dict]:
    """
    Load GitHub repo analysis data using Agent-2's parser.
    
    This integrates Partnership #4 work!
    
    Returns:
        List of repo analysis dicts
    """
    # TODO: Integrate Agent-2's github_book_viewer.py parser
    # For now, return placeholder structure
    
    repos = []
    
    # Parse the comprehensive book markdown
    book_file = Path("archive/status_updates/GITHUB_75_REPOS_COMPREHENSIVE_ANALYSIS_BOOK.md")
    
    if book_file.exists():
        # Simple parsing for now
        # In production, use Agent-2's parser with 8 comprehensive fields
        repos = _parse_github_book_simple(book_file)
    
    return repos


def _parse_github_book_simple(book_file: Path) -> List[Dict]:
    """
    Simple markdown parser for GitHub book.
    
    TODO: Replace with Agent-2's comprehensive parser integration.
    """
    repos = []
    
    with open(book_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract basic info (simplified)
    # Real implementation will use Agent-2's parser
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if line.startswith('#### Chapter') and 'Repo #' in line:
            # Extract repo number and name
            try:
                parts = line.split('#')
                if len(parts) >= 2:
                    repo_num = parts[1].split()[0]
                    
                    # Basic structure
                    repos.append({
                        'repo_id': int(repo_num),
                        'repo_name': 'TBD',  # Parse from markdown
                        'analyzed_by': 'TBD',
                        'status': 'ANALYZED',
                        'roi': 0.0,
                        'is_jackpot': '💎' in line or 'JACKPOT' in line,
                        'is_fork': 'FORK' in line,
                    })
            except (ValueError, IndexError):
                continue
    
    return repos


# ============================================================================
# DEBATES LOADING
# ============================================================================

def load_debates() -> List[Dict]:
    """
    Load debate data from debates/ directory.
    
    Returns:
        List of debate dicts with votes and consensus
    """
    debates = []
    debates_dir = Path("debates")
    
    if not debates_dir.exists():
        return debates
    
    for debate_file in debates_dir.glob("debate_*.json"):
        try:
            with open(debate_file, 'r', encoding='utf-8') as f:
                debate_data = json.load(f)
            
            # Add derived fields
            debate_data['consensus_percentage'] = _compute_consensus(debate_data)
            debate_data['status'] = _get_debate_status(debate_data)
            
            debates.append(debate_data)
        except (json.JSONDecodeError, IOError):
            continue
    
    return sorted(debates, key=lambda x: x.get('created_date', ''), reverse=True)


def _compute_consensus(debate: Dict) -> float:
    """
    Compute consensus percentage for debate.
    
    Returns percentage (0-100) of votes for winning option.
    """
    votes = debate.get('votes', {})
    if not votes:
        return 0.0
    
    # Count votes per option
    vote_counts = {}
    for agent_id, vote_data in votes.items():
        option = vote_data.get('option', vote_data.get('vote'))
        vote_counts[option] = vote_counts.get(option, 0) + 1
    
    if not vote_counts:
        return 0.0
    
    # Get max votes
    max_votes = max(vote_counts.values())
    total_votes = sum(vote_counts.values())
    
    return (max_votes / total_votes) * 100 if total_votes > 0 else 0.0


def _get_debate_status(debate: Dict) -> str:
    """
    Get debate status: ACTIVE, CLOSED, PENDING.
    """
    deadline = debate.get('deadline')
    if deadline:
        try:
            deadline_dt = datetime.fromisoformat(deadline)
            if datetime.now() > deadline_dt:
                return 'CLOSED'
        except ValueError:
            pass
    
    votes = debate.get('votes', {})
    expected_agents = 8
    
    if len(votes) >= expected_agents:
        return 'CLOSED'
    
    return 'ACTIVE'


# ============================================================================
# SWARM OVERVIEW
# ============================================================================

def get_swarm_overview() -> Dict:
    """
    Get high-level swarm overview with all key metrics.
    
    Returns:
        Dict with swarm-wide statistics and health
    """
    agents = load_all_agents()
    
    # Compute aggregate metrics
    total_points = sum(a.get('points_total', 0) for a in agents)
    active_agents = sum(1 for a in agents if a.get('status') == 'ACTIVE')
    live_agents = sum(1 for a in agents if a.get('is_live'))
    
    # Gas pipeline health
    avg_gas = sum(a.get('gas_level', 0) for a in agents) / len(agents) if agents else 0
    pipeline_health = 'FLOWING' if avg_gas > 50 else 'LOW' if avg_gas > 25 else 'EMPTY'
    
    # System health
    if live_agents >= 6:
        system_health = 'HEALTHY'
    elif live_agents >= 3:
        system_health = 'WARNING'
    else:
        system_health = 'CRITICAL'
    
    return {
        'timestamp': datetime.now().isoformat(),
        'total_agents': len(agents),
        'active_agents': active_agents,
        'live_agents': live_agents,
        'total_points': total_points,
        'avg_gas_level': round(avg_gas, 1),
        'pipeline_health': pipeline_health,
        'system_health': system_health,
        'agents': agents
    }

