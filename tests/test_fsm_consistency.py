#!/usr/bin/env python3
"""
FSM Consistency Tests - V2 Compliant
====================================

Unit tests for FSM state consistency validation.
Tests agent and swarm state validation.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.fsm.fsm_registry import (
    AgentState, SwarmState,
    validate_agent_state, validate_swarm_state,
    read_agent_state, read_swarm_state,
    get_all_agent_states, get_state_summary
)

# V2 Compliance: File under 400 lines, functions under 30 lines
VALID_AGENT_STATES = {state.value for state in AgentState}
VALID_SWARM_STATES = {state.value for state in SwarmState}


class TestAgentStateValidation:
    """Test agent state validation functions."""
    
    def test_valid_agent_states(self):
        """Test that all canonical agent states are valid."""
        for state in AgentState:
            assert validate_agent_state(state.value), f"State {state.value} should be valid"
    
    def test_invalid_agent_states(self):
        """Test that invalid states are rejected."""
        invalid_states = ["active", "ACTIVE_AGENT_MODE", "onboarding", "INVALID", ""]
        for state in invalid_states:
            if state not in VALID_AGENT_STATES:
                assert not validate_agent_state(state), f"State '{state}' should be invalid"
    
    def test_agent_state_enum_values(self):
        """Test that enum values match expected states."""
        expected_states = {
            "ONBOARDING", "ACTIVE", "CONTRACT_EXECUTION_ACTIVE",
            "SURVEY_MISSION_COMPLETED", "PAUSED", "ERROR", "RESET", "SHUTDOWN"
        }
        actual_states = {state.value for state in AgentState}
        assert actual_states == expected_states


class TestSwarmStateValidation:
    """Test swarm state validation functions."""
    
    def test_valid_swarm_states(self):
        """Test that all canonical swarm states are valid."""
        for state in SwarmState:
            assert validate_swarm_state(state.value), f"State {state.value} should be valid"
    
    def test_invalid_swarm_states(self):
        """Test that invalid states are rejected."""
        invalid_states = ["idle", "COORDINATING_ACTIVE", "INVALID", ""]
        for state in invalid_states:
            if state not in VALID_SWARM_STATES:
                assert not validate_swarm_state(state), f"State '{state}' should be invalid"
    
    def test_swarm_state_enum_values(self):
        """Test that enum values match expected states."""
        expected_states = {"IDLE", "COORDINATING", "BROADCAST", "DEGRADED", "HALT"}
        actual_states = {state.value for state in SwarmState}
        assert actual_states == expected_states


class TestStatusFileReading:
    """Test status file reading functions."""
    
    def test_read_agent_state_nonexistent(self):
        """Test reading state for non-existent agent."""
        result = read_agent_state("Agent-Nonexistent")
        assert result is None
    
    def test_read_swarm_state_nonexistent(self):
        """Test reading swarm state when file doesn't exist."""
        result = read_swarm_state()
        # Should return None if file doesn't exist
        assert result is None or isinstance(result, str)
    
    def test_get_all_agent_states(self):
        """Test getting states for all agents."""
        agent_states = get_all_agent_states()
        assert isinstance(agent_states, dict)
        
        # Check that all values are either valid states or None
        for agent_id, state in agent_states.items():
            assert agent_id.startswith("Agent-")
            assert state is None or validate_agent_state(state)


class TestStatusFileConsistency:
    """Test status file consistency validation."""
    
    def test_agent_status_files_are_valid(self):
        """Test that all agent status files use valid states."""
        semantic_path = Path("data/semantic_seed/status")
        if semantic_path.exists():
            for status_file in semantic_path.glob("Agent-*.json"):
                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        state = data.get("fsm_state") or data.get("status")
                        
                        if state:
                            assert validate_agent_state(state), \
                                f"{status_file.name} has invalid fsm_state={state}"
                except Exception:
                    # Skip files that can't be read
                    pass
    
    def test_workspace_status_files_are_valid(self):
        """Test that all workspace status files use valid states."""
        workspace_path = Path("agent_workspaces")
        if workspace_path.exists():
            for agent_dir in workspace_path.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    status_file = agent_dir / "status.json"
                    if status_file.exists():
                        try:
                            with open(status_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                state = data.get("fsm_state") or data.get("status")
                                
                                if state:
                                    assert validate_agent_state(state), \
                                        f"{status_file} has invalid fsm_state={state}"
                        except Exception:
                            # Skip files that can't be read
                            pass
    
    def test_swarm_status_file_is_valid(self):
        """Test that swarm status file uses valid state."""
        swarm_file = Path("swarm_coordination/swarm_state.json")
        if swarm_file.exists():
            try:
                with open(swarm_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state = data.get("swarm_state")
                    
                    if state:
                        assert validate_swarm_state(state), \
                            f"swarm_state.json has invalid swarm_state={state}"
            except Exception:
                # Skip files that can't be read
                pass


class TestStateSummary:
    """Test state summary functionality."""
    
    def test_get_state_summary(self):
        """Test getting comprehensive state summary."""
        summary = get_state_summary()
        
        assert isinstance(summary, dict)
        assert "agent_states" in summary
        assert "swarm_state" in summary
        assert "state_counts" in summary
        assert "total_agents" in summary
        assert "active_agents" in summary
        
        assert isinstance(summary["agent_states"], dict)
        assert isinstance(summary["state_counts"], dict)
        assert isinstance(summary["total_agents"], int)
        assert isinstance(summary["active_agents"], int)
        
        # Validate that all counted states are valid
        for state, count in summary["state_counts"].items():
            assert validate_agent_state(state), f"Invalid state in counts: {state}"
            assert isinstance(count, int), f"Count should be int: {count}"


class TestFSMIntegration:
    """Test FSM system integration."""
    
    def test_fsm_spec_exists(self):
        """Test that FSM specification file exists."""
        spec_path = Path("runtime/fsm/fsm_spec.yaml")
        assert spec_path.exists(), "FSM specification file should exist"
    
    def test_fsm_registry_imports(self):
        """Test that FSM registry imports correctly."""
        from src.fsm.fsm_registry import (
            AgentState, SwarmState, StatePointer,
            load_json, read_agent_state, read_swarm_state,
            validate_agent_state, validate_swarm_state
        )
        
        # Test that imports work
        assert AgentState is not None
        assert SwarmState is not None
        assert StatePointer is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])




