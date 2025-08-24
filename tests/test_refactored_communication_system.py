#!/usr/bin/env python3
"""
Test Suite for Refactored Communication System - Agent_Cellphone_V2
==================================================================

Comprehensive testing of refactored communication system components.
Ensures V2 coding standards compliance: ≤200 LOC, OOP design, SRP.

Author: Agent-1 (Foundation & Testing Specialist)
License: MIT
"""

import pytest
import asyncio
import json
import tempfile

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# Import our refactored components
from src.core.screen_region_manager import ScreenRegionManager, ScreenRegion
from src.core.input_buffer_system import InputBufferSystem, BufferedInput
from src.core.broadcast_system import BroadcastSystem, BroadcastMessage
from src.core.communication_compatibility_layer import AgentCommunicationProtocol


class TestScreenRegionManager:
    """Test suite for ScreenRegionManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = ScreenRegionManager()
    
    def test_define_agent_region(self):
        """Test defining agent regions"""
        region = self.manager.define_agent_region("Agent-1", 100, 200, 300, 250)
        
        assert region.agent_id == "Agent-1"
        assert region.x == 100
        assert region.y == 200
        assert region.width == 300
        assert region.height == 250
        
        # Check sub-regions
        assert region.input_box['x'] == 110
        assert region.input_box['y'] == 420  # y + height - 30
        assert region.status_box['x'] == 110
        assert region.status_box['y'] == 210  # y + 10
        assert region.workspace_box['x'] == 110
        assert region.workspace_box['y'] == 240  # y + 40
    
    def test_get_agent_region(self):
        """Test retrieving agent regions"""
        self.manager.define_agent_region("Agent-1", 0, 0, 200, 200)
        
        region = self.manager.get_agent_region("Agent-1")
        assert region is not None
        assert region.agent_id == "Agent-1"
        
        # Test non-existent agent
        assert self.manager.get_agent_region("NonExistent") is None
    
    def test_coordinate_validation(self):
        """Test coordinate validation within regions"""
        self.manager.define_agent_region("Agent-1", 100, 100, 200, 200)
        
        # Test coordinates inside region
        assert self.manager.is_coordinate_in_region("Agent-1", 150, 150) is True
        assert self.manager.is_coordinate_in_region("Agent-1", 100, 100) is True
        assert self.manager.is_coordinate_in_region("Agent-1", 299, 299) is True
        
        # Test coordinates outside region
        assert self.manager.is_coordinate_in_region("Agent-1", 50, 50) is False
        assert self.manager.is_coordinate_in_region("Agent-1", 350, 350) is False
    
    def test_region_activation(self):
        """Test region activation/deactivation"""
        self.manager.define_agent_region("Agent-1", 0, 0, 200, 200)
        
        # Initially active
        assert self.manager.agent_regions["Agent-1"].active is True
        assert self.manager.region_stats['active_regions'] == 1
        
        # Deactivate
        self.manager.deactivate_region("Agent-1")
        assert self.manager.agent_regions["Agent-1"].active is False
        assert self.manager.region_stats['active_regions'] == 0
        
        # Reactivate
        self.manager.activate_region("Agent-1")
        assert self.manager.agent_regions["Agent-1"].active is True
        assert self.manager.region_stats['active_regions'] == 1
    
    def test_virtual_cursor_management(self):
        """Test virtual cursor management"""
        self.manager.define_agent_region("Agent-1", 0, 0, 200, 200)
        
        # Initial cursor position
        initial_cursor = self.manager.get_virtual_cursor("Agent-1")
        assert initial_cursor == (10, 10)
        
        # Update cursor
        self.manager.update_virtual_cursor("Agent-1", 150, 150)
        updated_cursor = self.manager.get_virtual_cursor("Agent-1")
        assert updated_cursor == (150, 150)
    
    def test_region_statistics(self):
        """Test region statistics tracking"""
        assert self.manager.region_stats['total_regions'] == 0
        assert self.manager.region_stats['active_regions'] == 0
        
        # Add regions
        self.manager.define_agent_region("Agent-1", 0, 0, 200, 200)
        self.manager.define_agent_region("Agent-2", 200, 0, 200, 200)
        
        stats = self.manager.get_region_stats()
        assert stats['total_regions'] == 2
        assert stats['active_regions'] == 2
        assert stats['defined_regions'] == 2
        assert stats['virtual_cursors'] == 2
    
    def test_cleanup(self):
        """Test cleanup functionality"""
        self.manager.define_agent_region("Agent-1", 0, 0, 200, 200)
        
        # Verify locks exist
        assert "Agent-1" in self.manager.region_locks
        
        # Cleanup (logs cleanup completion)
        self.manager.cleanup()
        
        # Verify cleanup method executed without errors
        # Note: asyncio.Lock objects are automatically cleaned up by garbage collection
        assert "Agent-1" in self.manager.region_locks  # Locks remain until object destruction


class TestInputBufferSystem:
    """Test suite for InputBufferSystem"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.buffer_system = InputBufferSystem()
    
    @pytest.mark.asyncio
    async def test_buffer_agent_input(self):
        """Test buffering agent input"""
        buffer_id = await self.buffer_system.buffer_agent_input(
            "Agent-1", "Test message", "input_box"
        )
        
        assert buffer_id.startswith("Agent-1_")
        assert len(self.buffer_system.agent_buffers) == 1
        
        buffered_input = self.buffer_system.get_buffered_input(buffer_id)
        assert buffered_input.agent_id == "Agent-1"
        assert buffered_input.message == "Test message"
        assert buffered_input.target_area == "input_box"
        assert buffered_input.status == 'buffered'
    
    @pytest.mark.asyncio
    async def test_execute_buffered_inputs(self):
        """Test executing buffered inputs"""
        # Buffer some inputs
        await self.buffer_system.buffer_agent_input("Agent-1", "Message 1")
        await self.buffer_system.buffer_agent_input("Agent-2", "Message 2")
        
        # Mock execution handler
        async def mock_handler(input_item):
            return True
        
        # Execute
        results = await self.buffer_system.execute_buffered_inputs(mock_handler)
        
        assert len(results) == 2
        assert all(results.values())  # All should be successful
        
        # Check status updates
        for buffer_id in results:
            input_item = self.buffer_system.get_buffered_input(buffer_id)
            assert input_item.status == 'executed'
    
    def test_get_agent_buffers(self):
        """Test retrieving buffers by agent"""
        # Add buffers for different agents
        asyncio.run(self.buffer_system.buffer_agent_input("Agent-1", "Message 1"))
        asyncio.run(self.buffer_system.buffer_agent_input("Agent-1", "Message 2"))
        asyncio.run(self.buffer_system.buffer_agent_input("Agent-2", "Message 3"))
        
        agent1_buffers = self.buffer_system.get_agent_buffers("Agent-1")
        agent2_buffers = self.buffer_system.get_agent_buffers("Agent-2")
        
        assert len(agent1_buffers) == 2
        assert len(agent2_buffers) == 1
        assert all(buf.agent_id == "Agent-1" for buf in agent1_buffers)
        assert all(buf.agent_id == "Agent-2" for buf in agent2_buffers)
    
    def test_retry_failed_input(self):
        """Test retrying failed inputs"""
        # Create a failed input
        buffer_id = "test_id"
        failed_input = BufferedInput(
            buffer_id=buffer_id,
            agent_id="Agent-1",
            message="Failed message",
            target_area="input_box",
            priority=1,
            timestamp=0,
            status='failed',
            line_breaks=False
        )
        
        self.buffer_system.agent_buffers[buffer_id] = failed_input
        
        # Retry
        success = self.buffer_system.retry_failed_input(buffer_id)
        assert success is True
        
        # Check status updated
        updated_input = self.buffer_system.get_buffered_input(buffer_id)
        assert updated_input.status == 'buffered'
        assert updated_input.retry_count == 1
    
    def test_buffer_statistics(self):
        """Test buffer statistics tracking"""
        # Add some buffers
        asyncio.run(self.buffer_system.buffer_agent_input("Agent-1", "Message 1"))
        asyncio.run(self.buffer_system.buffer_agent_input("Agent-2", "Message 2"))
        
        stats = self.buffer_system.get_buffer_stats()
        assert stats['total_buffered'] == 2
        assert stats['current_buffers'] == 2
        assert stats['pending_count'] == 2
        assert stats['failed_count'] == 0
    
    def test_cleanup(self):
        """Test cleanup functionality"""
        # Add some old buffers
        old_input = BufferedInput(
            buffer_id="old_id",
            agent_id="Agent-1",
            message="Old message",
            target_area="input_box",
            priority=1,
            timestamp=0,  # Very old timestamp
            status='executed',
            line_breaks=False
        )
        
        self.buffer_system.agent_buffers["old_id"] = old_input
        
        # Cleanup
        self.buffer_system.cleanup()
        
        # Verify old buffer removed
        assert "old_id" not in self.buffer_system.agent_buffers


class TestBroadcastSystem:
    """Test suite for BroadcastSystem"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.broadcast_system = BroadcastSystem()
    
    @pytest.mark.asyncio
    async def test_broadcast_message(self):
        """Test broadcasting messages"""
        message_id = await self.broadcast_system.broadcast_message(
            "Agent-1", "Test broadcast", "general", recipients=["Agent-2", "Agent-3"]
        )
        
        assert message_id.startswith("broadcast_Agent-1_")
        assert len(self.broadcast_system.message_history) == 1
        
        message = self.broadcast_system.get_broadcast_message(message_id)
        assert message.sender_id == "Agent-1"
        assert message.content == "Test broadcast"
        assert message.recipients == ["Agent-2", "Agent-3"]
        assert message.status == 'pending'
    
    @pytest.mark.asyncio
    async def test_recipient_handler_registration(self):
        """Test recipient handler registration"""
        async def mock_handler(message):
            return "processed"
        
        await self.broadcast_system.register_recipient_handler("Agent-1", mock_handler)
        
        assert "Agent-1" in self.broadcast_system.recipient_handlers
        assert self.broadcast_system.broadcast_stats['active_recipients'] == 1
        
        # Unregister
        await self.broadcast_system.unregister_recipient_handler("Agent-1")
        assert "Agent-1" not in self.broadcast_system.recipient_handlers
        assert self.broadcast_system.broadcast_stats['active_recipients'] == 0
    
    @pytest.mark.asyncio
    async def test_message_delivery(self):
        """Test message delivery to recipients"""
        # Register handlers
        delivery_results = []
        
        async def mock_handler1(message):
            delivery_results.append(("Agent-1", True, "success"))
            return "success"
        
        async def mock_handler2(message):
            delivery_results.append(("Agent-2", True, "success"))
            return "success"
        
        await self.broadcast_system.register_recipient_handler("Agent-1", mock_handler1)
        await self.broadcast_system.register_recipient_handler("Agent-2", mock_handler2)
        
        # Send broadcast
        message_id = await self.broadcast_system.broadcast_message(
            "Sender", "Test message", recipients=["Agent-1", "Agent-2"]
        )
        
        # Process delivery
        message = self.broadcast_system.get_broadcast_message(message_id)
        results = await self.broadcast_system._deliver_broadcast(message)
        
        assert len(results) == 2
        assert all(success for _, success, _ in results)
        assert message.status == 'delivered'
    
    def test_message_filtering(self):
        """Test message filtering by various criteria"""
        # Add some messages
        asyncio.run(self.broadcast_system.broadcast_message("Agent-1", "Message 1", "info"))
        asyncio.run(self.broadcast_system.broadcast_message("Agent-2", "Message 2", "error"))
        asyncio.run(self.broadcast_system.broadcast_message("Agent-1", "Message 3", "info"))
        
        # Filter by sender
        agent1_messages = self.broadcast_system.get_messages_by_sender("Agent-1")
        assert len(agent1_messages) == 2
        
        # Filter by type
        info_messages = self.broadcast_system.get_messages_by_type("info")
        assert len(info_messages) == 2
        
        error_messages = self.broadcast_system.get_messages_by_type("error")
        assert len(error_messages) == 1
    
    def test_broadcast_statistics(self):
        """Test broadcast statistics tracking"""
        # Send some broadcasts
        asyncio.run(self.broadcast_system.broadcast_message("Agent-1", "Message 1"))
        asyncio.run(self.broadcast_system.broadcast_message("Agent-2", "Message 2"))
        
        stats = self.broadcast_system.get_broadcast_stats()
        assert stats['total_broadcasts'] == 2
        assert stats['total_messages'] == 2
        assert stats['pending_count'] == 2
        assert stats['failed_count'] == 0


class TestAgentCommunicationSystem:
    """Test suite for AgentCommunicationSystem"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.comm_system = AgentCommunicationProtocol()
    
    @pytest.mark.asyncio
    async def test_system_initialization(self):
        """Test system initialization"""
        # Mock coordinate file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "Agent-1": {"x": 0, "y": 0},
                "Agent-2": {"x": 200, "y": 0}
            }, f)
            coords_file = f.name
        
        try:
            # Patch the coordinate file path
            with patch('src.core.communication_compatibility_layer.Path') as mock_path:
                mock_path.return_value = Path(coords_file)
                
                await self.comm_system.initialize_system()
                
                assert self.comm_system.is_running is True
                assert len(self.comm_system.region_manager.agent_regions) == 2
                
        finally:
            # Cleanup
            Path(coords_file).unlink()
    
    @pytest.mark.asyncio
    async def test_send_message_to_agent(self):
        """Test sending messages to specific agents"""
        # Setup a region
        self.comm_system.region_manager.define_agent_region("Agent-1", 0, 0, 200, 200)
        
        # Mock PyAutoGUI
        with patch('pyautogui.moveTo'), patch('pyautogui.click'), \
             patch('pyautogui.typewrite'), patch('pyautogui.press'):
            
            buffer_id = await self.comm_system.send_message_to_agent(
                "Agent-1", "Test message"
            )
            
            assert buffer_id.startswith("Agent-1_")
    
    @pytest.mark.asyncio
    async def test_broadcast_to_all_agents(self):
        """Test broadcasting to all agents"""
        # Setup regions
        self.comm_system.region_manager.define_agent_region("Agent-1", 0, 0, 200, 200)
        self.comm_system.region_manager.define_agent_region("Agent-2", 200, 0, 200, 200)
        
        broadcast_id = await self.comm_system.broadcast_to_all_agents(
            "Sender", "Test broadcast"
        )
        
        assert broadcast_id.startswith("broadcast_Sender_")
    
    def test_system_status(self):
        """Test system status retrieval"""
        # Setup some regions
        self.comm_system.region_manager.define_agent_region("Agent-1", 0, 0, 200, 200)
        
        status = self.comm_system.get_system_status()
        
        assert 'system_running' in status
        assert 'region_stats' in status
        assert 'buffer_stats' in status
        assert 'broadcast_stats' in status
        assert status['total_agents'] == 1
    
    @pytest.mark.asyncio
    async def test_system_shutdown(self):
        """Test system shutdown"""
        # Initialize first
        await self.comm_system.initialize_system()
        assert self.comm_system.is_running is True
        
        # Shutdown
        await self.comm_system.shutdown()
        assert self.comm_system.is_running is False


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
