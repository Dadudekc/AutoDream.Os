#!/usr/bin/env python3
"""
FSM Scanner - V2 Compliant
==========================

Finite State Machine scanner for validating agent and swarm states.
Scans all status files and reports invalid states.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.fsm.fsm_registry import (
    AgentState, SwarmState, 
    validate_agent_state, validate_swarm_state,
    get_all_agent_states, read_swarm_state
)

# V2 Compliance: File under 400 lines, functions under 30 lines
ROOTS = [
    Path("data/semantic_seed/status"),
    Path("agent_workspaces"),
    Path("swarm_coordination"),
]

VALID_AGENT_STATES = {state.value for state in AgentState}
VALID_SWARM_STATES = {state.value for state in SwarmState}


def scan_agent_states() -> Tuple[Dict[str, str], List[str]]:
    """Scan all agent status files for state validation."""
    agents = {}
    issues = []
    
    # Scan semantic seed status files
    semantic_path = Path("data/semantic_seed/status")
    if semantic_path.exists():
        for status_file in semantic_path.glob("Agent-*.json"):
            try:
                with open(status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    agent_id = status_file.stem
                    state = data.get("fsm_state") or data.get("status")
                    
                    if state and not validate_agent_state(state):
                        issues.append(f"{status_file.name}: invalid fsm_state '{state}'")
                    
                    agents[agent_id] = state
            except Exception as e:
                issues.append(f"{status_file.name}: read error - {e}")
    
    # Scan workspace status files
    workspace_path = Path("agent_workspaces")
    if workspace_path.exists():
        for agent_dir in workspace_path.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                status_file = agent_dir / "status.json"
                if status_file.exists():
                    try:
                        with open(status_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            agent_id = agent_dir.name
                            state = data.get("fsm_state") or data.get("status")
                            
                            if state and not validate_agent_state(state):
                                issues.append(f"{status_file}: invalid fsm_state '{state}'")
                            
                            # Override semantic seed if workspace exists
                            agents[agent_id] = state
                    except Exception as e:
                        issues.append(f"{status_file}: read error - {e}")
    
    return agents, issues


def scan_swarm_state() -> Tuple[Optional[str], List[str]]:
    """Scan swarm state file for validation."""
    issues = []
    swarm_state = None
    
    swarm_file = Path("swarm_coordination/swarm_state.json")
    if swarm_file.exists():
        try:
            with open(swarm_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                swarm_state = data.get("swarm_state")
                
                if swarm_state and not validate_swarm_state(swarm_state):
                    issues.append(f"swarm_state.json: invalid swarm_state '{swarm_state}'")
        except Exception as e:
            issues.append(f"swarm_state.json: read error - {e}")
    
    return swarm_state, issues


def scan_all_states() -> Tuple[Dict[str, str], Optional[str], List[str]]:
    """Scan all states and return comprehensive results."""
    agents, agent_issues = scan_agent_states()
    swarm, swarm_issues = scan_swarm_state()
    
    all_issues = agent_issues + swarm_issues
    return agents, swarm, all_issues


def print_scan_results(agents: Dict[str, str], swarm: Optional[str], issues: List[str]):
    """Print formatted scan results."""
    print("🔍 FSM State Scan Results")
    print("=" * 50)
    
    print(f"\n📊 Agent States ({len(agents)} agents):")
    for agent_id, state in sorted(agents.items()):
        status = "✅" if validate_agent_state(state) else "❌"
        print(f"  {status} {agent_id}: {state or 'NO_STATE'}")
    
    print(f"\n🐝 Swarm State:")
    if swarm:
        status = "✅" if validate_swarm_state(swarm) else "❌"
        print(f"  {status} {swarm}")
    else:
        print("  ⚠️  No swarm state found")
    
    if issues:
        print(f"\n❌ Issues Found ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"\n✅ No issues found - all states valid!")
    
    print(f"\n📈 Summary:")
    print(f"  - Total agents: {len(agents)}")
    print(f"  - Valid agent states: {sum(1 for s in agents.values() if validate_agent_state(s))}")
    print(f"  - Swarm state: {'Valid' if swarm and validate_swarm_state(swarm) else 'Invalid/Missing'}")
    print(f"  - Issues: {len(issues)}")


def main():
    """Main scanner function."""
    try:
        agents, swarm, issues = scan_all_states()
        print_scan_results(agents, swarm, issues)
        
        if issues:
            print(f"\n❌ Scan failed with {len(issues)} issues")
            return 2
        else:
            print(f"\n✅ Scan passed - all states valid")
            return 0
            
    except Exception as e:
        print(f"❌ Scanner error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)





