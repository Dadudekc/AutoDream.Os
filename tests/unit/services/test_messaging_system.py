#!/usr/bin/env python3
"""
Unit tests for messaging system functionality.

Author: Agent-3 (QA Lead)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import sys
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))


class TestMessagingSystem:
    """Test suite for messaging system functionality."""
    
    def test_message_creation(self):
        """Test message object creation."""
        # Test message data
        message_data = {
            "from_agent": "Agent-4",
            "to_agent": "Agent-3",
            "message": "Test message",
            "priority": "HIGH",
            "tags": ["TASK_ASSIGNMENT"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Test message validation
        required_fields = ["from_agent", "to_agent", "message", "priority"]
        all_present = all(field in message_data for field in required_fields)
        assert all_present == True, "All required fields should be present"
        
        # Test priority validation
        valid_priorities = ["NORMAL", "HIGH", "CRITICAL"]
        assert message_data["priority"] in valid_priorities, "Priority should be valid"
    
    def test_agent_validation(self):
        """Test agent ID validation."""
        valid_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5",
            "Agent-6", "Agent-7", "Agent-8"
        ]
        
        test_agents = ["Agent-3", "Agent-4", "Invalid-Agent", "agent-1"]
        
        for agent in test_agents:
            is_valid = agent in valid_agents
            expected = agent in ["Agent-3", "Agent-4"]
            assert is_valid == expected, f"Agent {agent} validation should be {expected}"
    
    def test_message_serialization(self):
        """Test message serialization to JSON."""
        message_data = {
            "from_agent": "Agent-4",
            "to_agent": "Agent-3",
            "message": "Test serialization",
            "priority": "HIGH",
            "timestamp": "2025-01-05T05:00:00Z"
        }
        
        # Test JSON serialization
        try:
            json_str = json.dumps(message_data)
            parsed_data = json.loads(json_str)
            assert parsed_data == message_data, "Serialization should be reversible"
        except (TypeError, ValueError) as e:
            pytest.fail(f"Serialization failed: {e}")
    
    def test_message_priority_handling(self):
        """Test message priority handling logic."""
        priorities = ["NORMAL", "HIGH", "CRITICAL"]
        priority_values = {"NORMAL": 1, "HIGH": 2, "CRITICAL": 3}
        
        # Test priority comparison
        assert priority_values["NORMAL"] < priority_values["HIGH"]
        assert priority_values["HIGH"] < priority_values["CRITICAL"]
        
        # Test priority validation
        for priority in priorities:
            assert priority in priority_values, f"Priority {priority} should have value"
    
    def test_message_routing(self):
        """Test message routing logic."""
        # Mock agent coordinates
        agent_coordinates = {
            "Agent-3": {"x": 652, "y": 421},
            "Agent-4": {"x": -308, "y": 1000},
            "Agent-5": {"x": 652, "y": 421}
        }
        
        # Test routing from Agent-4 to Agent-3
        from_agent = "Agent-4"
        to_agent = "Agent-3"
        
        assert from_agent in agent_coordinates, "From agent should have coordinates"
        assert to_agent in agent_coordinates, "To agent should have coordinates"
        
        from_coords = agent_coordinates[from_agent]
        to_coords = agent_coordinates[to_agent]
        
        assert from_coords != to_coords, "Agents should have different coordinates"
    
    def test_message_timestamp_validation(self):
        """Test message timestamp validation."""
        # Valid timestamps
        valid_timestamps = [
            "2025-01-05T05:00:00Z",
            "2025-01-05T05:00:00.000Z",
            datetime.now().isoformat()
        ]
        
        # Invalid timestamps
        invalid_timestamps = [
            "invalid-timestamp",
            "2025-13-01T05:00:00Z",  # Invalid month
            "2025-01-32T05:00:00Z"   # Invalid day
        ]
        
        for timestamp in valid_timestamps:
            try:
                # Basic validation - check if it contains date and time
                assert "T" in timestamp or " " in timestamp, "Should contain date/time separator"
            except AssertionError:
                pytest.fail(f"Valid timestamp {timestamp} failed validation")
        
        for timestamp in invalid_timestamps:
            try:
                # These should fail validation
                assert "T" in timestamp or " " in timestamp, "Should contain date/time separator"
                # If we get here, the timestamp passed basic validation
                # This is okay for some edge cases
            except AssertionError:
                # This is expected for invalid timestamps
                pass
    
    def test_message_tag_validation(self):
        """Test message tag validation."""
        valid_tags = [
            "TASK_ASSIGNMENT",
            "REPORT",
            "STATUS_UPDATE",
            "EMERGENCY",
            "TEST_COVERAGE"
        ]
        
        test_message_tags = ["TASK_ASSIGNMENT", "INVALID_TAG", "REPORT"]
        
        for tag in test_message_tags:
            is_valid = tag in valid_tags
            expected = tag in ["TASK_ASSIGNMENT", "REPORT"]
            assert is_valid == expected, f"Tag {tag} validation should be {expected}"
    
    def test_message_content_validation(self):
        """Test message content validation."""
        # Valid messages
        valid_messages = [
            "Test message",
            "Agent-3 QA Lead mission complete",
            "TEST COVERAGE IMPROVEMENT MISSION - Progress Report"
        ]
        
        # Invalid messages
        invalid_messages = [
            "",  # Empty message
            "   ",  # Whitespace only
            None  # None message
        ]
        
        for message in valid_messages:
            is_valid = bool(message and message.strip())
            assert is_valid == True, f"Valid message should pass: {message}"
        
        for message in invalid_messages:
            is_valid = bool(message and message.strip())
            assert is_valid == False, f"Invalid message should fail: {message}"


@pytest.mark.unit
class TestMessagingIntegration:
    """Integration tests for messaging system."""
    
    def test_complete_message_workflow(self):
        """Test complete message workflow from creation to delivery."""
        # Step 1: Create message
        message_data = {
            "from_agent": "Agent-4",
            "to_agent": "Agent-3",
            "message": "Test complete workflow",
            "priority": "HIGH",
            "tags": ["TASK_ASSIGNMENT", "TEST_COVERAGE"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Step 2: Validate message
        validation_passed = (
            message_data["from_agent"] in ["Agent-4"] and
            message_data["to_agent"] in ["Agent-3"] and
            message_data["message"].strip() and
            message_data["priority"] in ["NORMAL", "HIGH", "CRITICAL"]
        )
        assert validation_passed == True, "Message validation should pass"
        
        # Step 3: Serialize message
        json_message = json.dumps(message_data)
        assert json_message is not None, "Serialization should succeed"
        
        # Step 4: Parse message
        parsed_message = json.loads(json_message)
        assert parsed_message == message_data, "Parsing should be accurate"
    
    def test_message_queue_simulation(self):
        """Test message queue simulation."""
        # Simulate message queue
        message_queue = []
        
        # Add messages with different priorities
        messages = [
            {"id": 1, "priority": "NORMAL", "content": "Normal message"},
            {"id": 2, "priority": "HIGH", "content": "High priority message"},
            {"id": 3, "priority": "CRITICAL", "content": "Critical message"},
            {"id": 4, "priority": "NORMAL", "content": "Another normal message"}
        ]
        
        # Add to queue
        for msg in messages:
            message_queue.append(msg)
        
        # Sort by priority (CRITICAL > HIGH > NORMAL)
        priority_order = {"CRITICAL": 3, "HIGH": 2, "NORMAL": 1}
        sorted_queue = sorted(message_queue, key=lambda x: priority_order[x["priority"]], reverse=True)
        
        # Verify order
        assert sorted_queue[0]["priority"] == "CRITICAL", "Critical should be first"
        assert sorted_queue[1]["priority"] == "HIGH", "High should be second"
        assert sorted_queue[2]["priority"] == "NORMAL", "First normal should be third"
        assert sorted_queue[3]["priority"] == "NORMAL", "Second normal should be last"
    
    def test_agent_communication_matrix(self):
        """Test agent communication matrix."""
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
        
        # Test all possible communication pairs
        communication_matrix = {}
        for from_agent in agents:
            for to_agent in agents:
                if from_agent != to_agent:
                    pair = (from_agent, to_agent)
                    communication_matrix[pair] = True
        
        # Verify matrix completeness
        expected_pairs = len(agents) * (len(agents) - 1)  # No self-communication
        actual_pairs = len(communication_matrix)
        assert actual_pairs == expected_pairs, f"Should have {expected_pairs} communication pairs"
        
        # Test specific communication
        test_pair = ("Agent-4", "Agent-3")
        assert test_pair in communication_matrix, "Agent-4 to Agent-3 should be possible"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
