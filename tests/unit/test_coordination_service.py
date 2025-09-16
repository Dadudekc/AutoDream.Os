#!/usr/bin/env python3
"""
Coordination Service Testing Suite
==================================

Comprehensive test suite for the CoordinationService and AgentFSM classes.
Tests cover:
- FSM state management and transitions
- Persistent state loading and saving
- Contract management
- Coordinate management
- Agent lifecycle management
- Error handling and edge cases

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from datetime import datetime

from src.coordination.coordination_service import CoordinationService, AgentFSM
from src.coordination.onboarding_coordinator import AgentState, ContractType, AgentContract


class TestAgentFSM:
    """Unit tests for AgentFSM class."""

    def test_fsm_initialization(self):
        """Test AgentFSM initialization."""
        fsm = AgentFSM("Agent-1")
        
        assert fsm.agent_id == "Agent-1"
        assert fsm.current_state == AgentState.UNINITIALIZED
        assert fsm.previous_state is None
        assert fsm.state_history == []
        assert fsm.transition_count == 0

    def test_fsm_transition_to_same_state(self):
        """Test FSM transition to the same state (should not create history entry)."""
        fsm = AgentFSM("Agent-1")
        initial_count = fsm.transition_count
        
        fsm.transition_to(AgentState.UNINITIALIZED)
        
        assert fsm.current_state == AgentState.UNINITIALIZED
        assert fsm.previous_state is None
        assert fsm.transition_count == initial_count
        assert len(fsm.state_history) == 0

    def test_fsm_transition_to_different_state(self):
        """Test FSM transition to a different state."""
        fsm = AgentFSM("Agent-1")
        
        fsm.transition_to(AgentState.ACTIVE)
        
        assert fsm.current_state == AgentState.ACTIVE
        assert fsm.previous_state == AgentState.UNINITIALIZED
        assert fsm.transition_count == 1
        assert len(fsm.state_history) == 1
        
        # Check history entry
        history_entry = fsm.state_history[0]
        assert history_entry["from"] == "UNINITIALIZED"
        assert history_entry["to"] == "ACTIVE"
        assert "timestamp" in history_entry

    def test_fsm_multiple_transitions(self):
        """Test multiple FSM transitions."""
        fsm = AgentFSM("Agent-1")
        
        # First transition
        fsm.transition_to(AgentState.ACTIVE)
        assert fsm.current_state == AgentState.ACTIVE
        assert fsm.transition_count == 1
        
        # Second transition
        fsm.transition_to(AgentState.BUSY)
        assert fsm.current_state == AgentState.BUSY
        assert fsm.previous_state == AgentState.ACTIVE
        assert fsm.transition_count == 2
        assert len(fsm.state_history) == 2
        
        # Third transition
        fsm.transition_to(AgentState.IDLE)
        assert fsm.current_state == AgentState.IDLE
        assert fsm.previous_state == AgentState.BUSY
        assert fsm.transition_count == 3
        assert len(fsm.state_history) == 3

    def test_fsm_get_state_info(self):
        """Test FSM get_state_info method."""
        fsm = AgentFSM("Agent-1")
        fsm.transition_to(AgentState.ACTIVE)
        fsm.transition_to(AgentState.BUSY)
        
        state_info = fsm.get_state_info()
        
        assert state_info["agent_id"] == "Agent-1"
        assert state_info["current_state"] == "BUSY"
        assert state_info["previous_state"] == "ACTIVE"
        assert state_info["transition_count"] == 2
        assert state_info["state_history_count"] == 2

    def test_fsm_get_state_info_initial_state(self):
        """Test FSM get_state_info with initial state."""
        fsm = AgentFSM("Agent-2")
        
        state_info = fsm.get_state_info()
        
        assert state_info["agent_id"] == "Agent-2"
        assert state_info["current_state"] == "UNINITIALIZED"
        assert state_info["previous_state"] is None
        assert state_info["transition_count"] == 0
        assert state_info["state_history_count"] == 0


class TestCoordinationService:
    """Unit tests for CoordinationService class."""

    def test_service_initialization(self):
        """Test CoordinationService initialization."""
        with patch('src.coordination.coordination_service.Path') as mock_path:
            mock_path.return_value.exists.return_value = False
            
            service = CoordinationService()
            
            assert len(service.swarm_agents) == 8
            assert "Agent-1" in service.swarm_agents
            assert "Agent-4" in service.swarm_agents
            assert len(service.agent_fsms) == 8
            assert len(service.contracts) == 0

    def test_load_coordinates_success(self):
        """Test successful coordinate loading."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]},
                "Agent-2": {"chat_input_coordinates": [300, 400]}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('pathlib.Path.exists', return_value=True):
                service = CoordinationService()
                
                assert service.agent_coordinates == mock_coordinates

    def test_load_coordinates_file_not_found(self):
        """Test coordinate loading when file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            service = CoordinationService()
            
            assert service.agent_coordinates == {}

    def test_load_coordinates_invalid_json(self):
        """Test coordinate loading with invalid JSON."""
        with patch('builtins.open', mock_open(read_data="invalid json")):
            with patch('pathlib.Path.exists', return_value=True):
                service = CoordinationService()
                
                assert service.agent_coordinates == {}

    def test_get_chat_coordinates_success(self):
        """Test successful chat coordinate retrieval."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('pathlib.Path.exists', return_value=True):
                service = CoordinationService()
                
                coords = service.get_chat_coordinates("Agent-1")
                assert coords == (100, 200)

    def test_get_chat_coordinates_agent_not_found(self):
        """Test chat coordinate retrieval for non-existent agent."""
        with patch('pathlib.Path.exists', return_value=False):
            service = CoordinationService()
            
            coords = service.get_chat_coordinates("NonExistentAgent")
            assert coords is None

    def test_get_chat_coordinates_missing_coordinates(self):
        """Test chat coordinate retrieval when coordinates are missing."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"other_data": "value"}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('pathlib.Path.exists', return_value=True):
                service = CoordinationService()
                
                coords = service.get_chat_coordinates("Agent-1")
                assert coords is None

    @patch('src.coordination.coordination_service.get_onboarding_coordinates')
    def test_get_onboarding_coordinates(self, mock_get_coords):
        """Test onboarding coordinate retrieval."""
        mock_get_coords.return_value = (500, 600)
        
        service = CoordinationService()
        coords = service.get_onboarding_coordinates("Agent-1")
        
        mock_get_coords.assert_called_once_with("Agent-1")
        assert coords == (500, 600)

    def test_create_contract(self):
        """Test contract creation."""
        service = CoordinationService()
        
        contract = service.create_contract(
            "Agent-1",
            ContractType.DEVELOPMENT,
            "Test contract",
            5,
            ["Agent-2"]
        )
        
        assert contract.agent_id == "Agent-1"
        assert contract.contract_type == ContractType.DEVELOPMENT
        assert contract.description == "Test contract"
        assert contract.estimated_cycles == 5
        assert contract.dependencies == ["Agent-2"]
        assert "Agent-1" in service.contracts

    def test_get_contract_existing(self):
        """Test getting existing contract."""
        service = CoordinationService()
        
        contract = service.create_contract(
            "Agent-1",
            ContractType.DEVELOPMENT,
            "Test contract",
            5
        )
        
        retrieved_contract = service.get_contract("Agent-1")
        assert retrieved_contract == contract

    def test_get_contract_non_existing(self):
        """Test getting non-existing contract."""
        service = CoordinationService()
        
        contract = service.get_contract("NonExistentAgent")
        assert contract is None

    def test_update_contract_status(self):
        """Test contract status update."""
        service = CoordinationService()
        
        contract = service.create_contract(
            "Agent-1",
            ContractType.DEVELOPMENT,
            "Test contract",
            5
        )
        
        service.update_contract_status("Agent-1", "in_progress", 50)
        
        assert contract.status == "in_progress"
        assert contract.progress_percentage == 50

    def test_update_contract_status_non_existing(self):
        """Test updating status of non-existing contract."""
        service = CoordinationService()
        
        # Should not raise exception
        service.update_contract_status("NonExistentAgent", "in_progress", 50)

    def test_get_agent_fsm_existing(self):
        """Test getting existing agent FSM."""
        service = CoordinationService()
        
        fsm = service.get_agent_fsm("Agent-1")
        assert fsm is not None
        assert fsm.agent_id == "Agent-1"

    def test_get_agent_fsm_non_existing(self):
        """Test getting non-existing agent FSM."""
        service = CoordinationService()
        
        fsm = service.get_agent_fsm("NonExistentAgent")
        assert fsm is None

    def test_transition_agent_state(self):
        """Test agent state transition."""
        service = CoordinationService()
        
        service.transition_agent_state("Agent-1", AgentState.ACTIVE)
        
        fsm = service.get_agent_fsm("Agent-1")
        assert fsm.current_state == AgentState.ACTIVE
        assert fsm.transition_count == 1

    def test_transition_agent_state_non_existing(self):
        """Test state transition for non-existing agent."""
        service = CoordinationService()
        
        # Should not raise exception
        service.transition_agent_state("NonExistentAgent", AgentState.ACTIVE)

    def test_get_agent_state_existing(self):
        """Test getting existing agent state."""
        service = CoordinationService()
        
        service.transition_agent_state("Agent-1", AgentState.ACTIVE)
        state = service.get_agent_state("Agent-1")
        
        assert state == AgentState.ACTIVE

    def test_get_agent_state_non_existing(self):
        """Test getting state of non-existing agent."""
        service = CoordinationService()
        
        state = service.get_agent_state("NonExistentAgent")
        assert state is None

    def test_get_all_agent_states(self):
        """Test getting all agent states."""
        service = CoordinationService()
        
        service.transition_agent_state("Agent-1", AgentState.ACTIVE)
        service.transition_agent_state("Agent-2", AgentState.BUSY)
        
        states = service.get_all_agent_states()
        
        assert states["Agent-1"] == "ACTIVE"
        assert states["Agent-2"] == "BUSY"
        assert states["Agent-3"] == "UNINITIALIZED"

    def test_get_contract_status(self):
        """Test getting contract status."""
        service = CoordinationService()
        
        service.create_contract("Agent-1", ContractType.DEVELOPMENT, "Test", 5)
        service.create_contract("Agent-2", ContractType.TESTING, "Test2", 3)
        
        status = service.get_contract_status()
        
        assert len(status) == 2
        assert "Agent-1" in status
        assert "Agent-2" in status

    def test_is_agent_onboarded_true(self):
        """Test checking if agent is onboarded (true case)."""
        service = CoordinationService()
        
        service.transition_agent_state("Agent-1", AgentState.ACTIVE)
        
        assert service.is_agent_onboarded("Agent-1") is True

    def test_is_agent_onboarded_false(self):
        """Test checking if agent is onboarded (false case)."""
        service = CoordinationService()
        
        assert service.is_agent_onboarded("Agent-1") is False

    def test_get_onboarded_agents(self):
        """Test getting list of onboarded agents."""
        service = CoordinationService()
        
        service.transition_agent_state("Agent-1", AgentState.ACTIVE)
        service.transition_agent_state("Agent-2", AgentState.BUSY)
        # Agent-3 remains UNINITIALIZED
        
        onboarded = service.get_onboarded_agents()
        
        assert "Agent-1" in onboarded
        assert "Agent-2" in onboarded
        assert "Agent-3" not in onboarded

    def test_get_agent_coordinates_summary(self):
        """Test getting agent coordinates summary."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]},
                "Agent-2": {"other_data": "value"}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('pathlib.Path.exists', return_value=True):
                service = CoordinationService()
                
                summary = service.get_agent_coordinates_summary()
                
                assert "Agent-1" in summary
                assert summary["Agent-1"]["coordinates"] == (100, 200)
                assert summary["Agent-1"]["has_coordinates"] is True
                assert summary["Agent-2"]["has_coordinates"] is False

    def test_validate_coordinates(self):
        """Test coordinate validation."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]},
                "Agent-2": {"other_data": "value"}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('pathlib.Path.exists', return_value=True):
                service = CoordinationService()
                
                validation = service.validate_coordinates()
                
                assert validation["Agent-1"] is True
                assert validation["Agent-2"] is False

    def test_get_system_status(self):
        """Test getting comprehensive system status."""
        service = CoordinationService()
        
        service.create_contract("Agent-1", ContractType.DEVELOPMENT, "Test", 5)
        service.transition_agent_state("Agent-1", AgentState.ACTIVE)
        
        status = service.get_system_status()
        
        assert status["total_agents"] == 8
        assert status["onboarded_agents"] == 1
        assert status["active_contracts"] == 1
        assert "agent_states" in status
        assert "contract_status" in status
        assert "coordinates_validation" in status
        assert "last_updated" in status

    def test_cleanup_expired_contracts(self):
        """Test cleanup of expired contracts."""
        service = CoordinationService()
        
        # Create contracts with different statuses
        contract1 = service.create_contract("Agent-1", ContractType.DEVELOPMENT, "Test1", 5)
        contract1.status = "completed"
        
        contract2 = service.create_contract("Agent-2", ContractType.TESTING, "Test2", 3)
        contract2.status = "active"
        
        contract3 = service.create_contract("Agent-3", ContractType.MAINTENANCE, "Test3", 2)
        contract3.status = "expired"
        
        service.cleanup_expired_contracts()
        
        # Only active contract should remain
        assert "Agent-1" not in service.contracts
        assert "Agent-2" in service.contracts
        assert "Agent-3" not in service.contracts

    def test_reset_agent_state(self):
        """Test resetting agent state."""
        service = CoordinationService()
        
        # Set up agent with state and contract
        service.transition_agent_state("Agent-1", AgentState.ACTIVE)
        service.create_contract("Agent-1", ContractType.DEVELOPMENT, "Test", 5)
        
        service.reset_agent_state("Agent-1")
        
        # Check that state is reset
        fsm = service.get_agent_fsm("Agent-1")
        assert fsm.current_state == AgentState.UNINITIALIZED
        assert fsm.transition_count == 0
        
        # Check that contract is removed
        assert "Agent-1" not in service.contracts

    def test_get_agent_statistics(self):
        """Test getting agent statistics."""
        service = CoordinationService()
        
        # Set up different agent states
        service.transition_agent_state("Agent-1", AgentState.ACTIVE)
        service.transition_agent_state("Agent-1", AgentState.BUSY)
        service.transition_agent_state("Agent-2", AgentState.ACTIVE)
        
        stats = service.get_agent_statistics()
        
        assert stats["total_agents"] == 8
        assert stats["state_distribution"]["ACTIVE"] == 1
        assert stats["state_distribution"]["BUSY"] == 1
        assert stats["state_distribution"]["UNINITIALIZED"] == 6
        assert stats["total_transitions"] == 3
        assert stats["average_transitions"] == 3 / 8


class TestCoordinationServicePersistence:
    """Tests for persistent state management."""

    def test_save_persistent_state(self):
        """Test saving persistent state."""
        with tempfile.TemporaryDirectory() as temp_dir:
            state_file = Path(temp_dir) / "persistent_state.json"
            
            with patch('src.coordination.coordination_service.Path') as mock_path:
                mock_path.return_value = state_file
                mock_path.return_value.parent.mkdir = Mock()
                
                service = CoordinationService()
                service.transition_agent_state("Agent-1", AgentState.ACTIVE)
                service.create_contract("Agent-1", ContractType.DEVELOPMENT, "Test", 5)
                
                service.save_persistent_state()
                
                # Verify file was created and contains expected data
                assert state_file.exists()
                with open(state_file) as f:
                    data = json.load(f)
                    assert "fsms" in data
                    assert "contracts" in data
                    assert "timestamp" in data

    def test_load_persistent_state_success(self):
        """Test successful persistent state loading."""
        state_data = {
            "fsms": {
                "Agent-1": {
                    "agent_id": "Agent-1",
                    "current_state": "ACTIVE",
                    "previous_state": "UNINITIALIZED",
                    "transition_count": 1,
                    "state_history_count": 1
                }
            },
            "contracts": [
                {
                    "agent_id": "Agent-1",
                    "contract_type": "DEVELOPMENT",
                    "description": "Test contract",
                    "estimated_cycles": 5,
                    "dependencies": [],
                    "status": "active",
                    "progress_percentage": 0,
                    "created_at": datetime.now().isoformat()
                }
            ]
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(state_data))):
            with patch('pathlib.Path.exists', return_value=True):
                service = CoordinationService()
                
                # Verify FSM state was restored
                fsm = service.get_agent_fsm("Agent-1")
                assert fsm.current_state == AgentState.ACTIVE
                assert fsm.transition_count == 1
                
                # Verify contract was restored
                contract = service.get_contract("Agent-1")
                assert contract is not None
                assert contract.contract_type == ContractType.DEVELOPMENT

    def test_load_persistent_state_file_not_found(self):
        """Test loading persistent state when file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            service = CoordinationService()
            
            # Should not raise exception
            assert len(service.contracts) == 0

    def test_load_persistent_state_invalid_json(self):
        """Test loading persistent state with invalid JSON."""
        with patch('builtins.open', mock_open(read_data="invalid json")):
            with patch('pathlib.Path.exists', return_value=True):
                service = CoordinationService()
                
                # Should not raise exception
                assert len(service.contracts) == 0


if __name__ == "__main__":
    """Run tests directly for development."""
    print("🧪 CoordinationService Testing Suite")
    print("=" * 50)
    
    # Run basic tests
    test_instance = TestAgentFSM()
    
    try:
        test_instance.test_fsm_initialization()
        print("✅ FSM initialization test passed")
    except Exception as e:
        print(f"❌ FSM initialization test failed: {e}")
    
    try:
        test_instance.test_fsm_transition_to_different_state()
        print("✅ FSM transition test passed")
    except Exception as e:
        print(f"❌ FSM transition test failed: {e}")
    
    # Run coordination service tests
    coord_test_instance = TestCoordinationService()
    
    try:
        coord_test_instance.test_service_initialization()
        print("✅ Service initialization test passed")
    except Exception as e:
        print(f"❌ Service initialization test failed: {e}")
    
    try:
        coord_test_instance.test_create_contract()
        print("✅ Contract creation test passed")
    except Exception as e:
        print(f"❌ Contract creation test failed: {e}")
    
    print("\n🎉 Core CoordinationService tests completed!")
    print("📊 Run full suite with: python -m pytest tests/unit/test_coordination_service.py -v")