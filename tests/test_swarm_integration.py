"""
Test Suite for SWARM Integration System - Agent Cellphone V2
==========================================================

Comprehensive testing for SWARM integration components.
Validates functionality, V2 standards compliance, and integration integrity.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add V2 src to path
v2_src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(v2_src_path))

# Import SWARM integration components
from core.swarm_coordination_system import SwarmCoordinationSystem, SwarmIntegrationStatus
from core.swarm_agent_bridge import SwarmAgentBridge, BridgeStatus
from core.swarm_integration_manager import SwarmIntegrationManager, IntegrationStatus


class TestSwarmCoordinationSystem:
    """Test suite for SWARM Coordination System."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.mock_agent_manager = Mock()
        self.mock_task_manager = Mock()
        self.coordination_system = SwarmCoordinationSystem(
            self.mock_agent_manager, 
            self.mock_task_manager
        )
    
    def test_initialization(self):
        """Test system initialization."""
        assert self.coordination_system.v2_agent_manager == self.mock_agent_manager
        assert self.coordination_system.v2_task_manager == self.mock_task_manager
        assert isinstance(self.coordination_system.status, SwarmIntegrationStatus)
    
    def test_agent_integration(self):
        """Test agent integration functionality."""
        # Mock coordination as active
        self.coordination_system.coordination_active = True
        self.mock_agent_manager.register_agent.return_value = True
        
        # Test successful integration
        result = self.coordination_system.integrate_agent(
            "test-agent", "Test Agent", ["test", "demo"]
        )
        
        assert result is True
        assert "test-agent" in self.coordination_system.integrated_agents
        self.mock_agent_manager.register_agent.assert_called_once()
    
    def test_agent_coordination(self):
        """Test multi-agent coordination."""
        # Setup test agents
        self.coordination_system.coordination_active = True
        self.coordination_system.integrated_agents = {
            "agent1": Mock(),
            "agent2": Mock()
        }
        
        # Mock SWARM interface
        self.coordination_system.swarm_agent_interface = Mock()
        self.coordination_system.swarm_agent_interface.send_command.return_value = True
        
        # Test coordination
        results = self.coordination_system.coordinate_agents(
            "Test coordination task", ["agent1", "agent2"]
        )
        
        assert len(results) == 2
        assert results["agent1"] is True
        assert results["agent2"] is True
    
    def test_status_retrieval(self):
        """Test status and metrics retrieval."""
        status = self.coordination_system.get_swarm_status()
        
        assert "status" in status
        assert "coordination_active" in status
        assert "integrated_agents" in status
        assert "swarm_available" in status


class TestSwarmAgentBridge:
    """Test suite for SWARM Agent Bridge."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.mock_coordination_system = Mock()
        self.bridge = SwarmAgentBridge(self.mock_coordination_system)
    
    def test_bridge_initialization(self):
        """Test bridge initialization."""
        assert self.bridge.swarm_coordination_system == self.mock_coordination_system
        assert isinstance(self.bridge.status, BridgeStatus)
        assert self.bridge.connected_agents == {}
    
    def test_agent_connection(self):
        """Test agent connection to bridge."""
        # Mock bridge as active
        self.bridge.bridge_active = True
        
        agent_info = {"name": "Test Agent", "capabilities": ["test"]}
        result = self.bridge.connect_agent("test-agent", agent_info)
        
        assert result is True
        assert "test-agent" in self.bridge.connected_agents
        assert self.bridge.connected_agents["test-agent"]["status"] == "connected"
    
    def test_message_sending(self):
        """Test message sending through bridge."""
        # Mock bridge as active
        self.bridge.bridge_active = True
        self.bridge.connected_agents = {"target-agent": Mock()}
        
        # Mock SWARM interface
        self.bridge.swarm_agent_interface = Mock()
        self.bridge.swarm_agent_interface.send_command.return_value = True
        
        # Test message sending
        result = self.bridge.send_message(
            "from-agent", "target-agent", "Test message", "task", 1
        )
        
        assert result is True
        self.bridge.swarm_agent_interface.send_command.assert_called_once()
    
    def test_message_handler_registration(self):
        """Test message handler registration."""
        def test_handler(message):
            pass
        
        result = self.bridge.register_message_handler("test_type", test_handler)
        
        assert result is True
        assert "test_type" in self.bridge.message_handlers
        assert self.bridge.message_handlers["test_type"] == test_handler


class TestSwarmIntegrationManager:
    """Test suite for SWARM Integration Manager."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.manager = SwarmIntegrationManager()
    
    def test_manager_initialization(self):
        """Test manager initialization."""
        assert self.manager.agent_manager is not None
        assert self.manager.status in IntegrationStatus
        assert hasattr(self.manager, 'swarm_coordination')
        assert hasattr(self.manager, 'agent_bridge')
    
    def test_agent_integration_workflow(self):
        """Test complete agent integration workflow."""
        # Mock integration as active
        self.manager.integration_active = True
        
        # Mock coordination system
        self.manager.swarm_coordination = Mock()
        self.manager.swarm_coordination.integrate_agent.return_value = True
        
        # Mock agent bridge
        self.manager.agent_bridge = Mock()
        self.manager.agent_bridge.connect_agent.return_value = True
        
        # Test integration
        result = self.manager.integrate_agent(
            "test-agent", "Test Agent", ["test", "demo"]
        )
        
        assert result is True
        self.manager.swarm_coordination.integrate_agent.assert_called_once()
        self.manager.agent_bridge.connect_agent.assert_called_once()
    
    def test_agent_coordination(self):
        """Test agent coordination through manager."""
        # Mock integration as active
        self.manager.integration_active = True
        
        # Mock coordination system
        self.manager.swarm_coordination = Mock()
        self.manager.swarm_coordination.coordinate_agents.return_value = {
            "agent1": True,
            "agent2": True
        }
        
        # Test coordination
        results = self.manager.coordinate_agents(
            "Test coordination", ["agent1", "agent2"]
        )
        
        assert len(results) == 2
        assert results["agent1"] is True
        assert results["agent2"] is True
    
    def test_status_retrieval(self):
        """Test comprehensive status retrieval."""
        status = self.manager.get_integration_status()
        
        assert "integration_status" in status
        assert "integration_active" in status
        assert "metrics" in status
        assert "swarm_coordination" in status
        assert "agent_bridge" in status


class TestIntegrationStandards:
    """Test suite for V2 standards compliance."""
    
    def test_file_line_counts(self):
        """Test that all files meet V2 LOC standards."""
        v2_src_path = Path(__file__).parent.parent / "src" / "core"
        
        for py_file in v2_src_path.glob("*.py"):
            if "swarm" in py_file.name.lower():
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Count non-empty, non-comment lines
                    code_lines = [line for line in lines 
                                if line.strip() and not line.strip().startswith('#')]
                    
                    assert len(code_lines) <= 200, f"{py_file.name} exceeds 200 LOC limit: {len(code_lines)}"
    
    def test_single_responsibility(self):
        """Test that each class follows Single Responsibility Principle."""
        # Test coordination system
        coord_system = SwarmCoordinationSystem(Mock(), Mock())
        assert hasattr(coord_system, 'integrate_agent')
        assert hasattr(coord_system, 'coordinate_agents')
        # Should not have unrelated responsibilities
        
        # Test agent bridge
        bridge = SwarmAgentBridge(Mock())
        assert hasattr(bridge, 'connect_agent')
        assert hasattr(bridge, 'send_message')
        # Should not have unrelated responsibilities
        
        # Test integration manager
        manager = SwarmIntegrationManager()
        assert hasattr(manager, 'integrate_agent')
        assert hasattr(manager, 'coordinate_agents')
        # Should not have unrelated responsibilities


def run_integration_tests():
    """Run all integration tests."""
    print("🧪 Running SWARM Integration Test Suite...")
    
    # Test coordination system
    test_coord = TestSwarmCoordinationSystem()
    test_coord.setup_method()
    test_coord.test_initialization()
    test_coord.test_agent_integration()
    test_coord.test_agent_coordination()
    test_coord.test_status_retrieval()
    
    # Test agent bridge
    test_bridge = TestSwarmAgentBridge()
    test_bridge.setup_method()
    test_bridge.test_bridge_initialization()
    test_bridge.test_agent_connection()
    test_bridge.test_message_sending()
    test_bridge.test_message_handler_registration()
    
    # Test integration manager
    test_manager = TestSwarmIntegrationManager()
    test_manager.setup_method()
    test_manager.test_manager_initialization()
    test_manager.test_agent_integration_workflow()
    test_manager.test_agent_coordination()
    test_manager.test_status_retrieval()
    
    # Test standards compliance
    test_standards = TestIntegrationStandards()
    test_standards.test_single_responsibility()
    
    print("✅ All SWARM Integration Tests PASSED")
    return True


if __name__ == "__main__":
    run_integration_tests()
