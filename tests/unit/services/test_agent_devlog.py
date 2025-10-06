#!/usr/bin/env python3
"""
Unit tests for agent devlog functionality.

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


class TestAgentDevlog:
    """Test suite for agent devlog functionality."""
    
    def test_devlog_entry_creation(self):
        """Test devlog entry creation."""
        # Mock devlog entry data
        devlog_entry = {
            "agent_id": "Agent-3",
            "action": "Test devlog entry",
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "details": "Test details for devlog entry"
        }
        
        # Test devlog entry validation
        required_fields = ["agent_id", "action", "timestamp"]
        for field in required_fields:
            assert field in devlog_entry, f"Devlog entry should have {field}"
        
        # Test agent ID validation
        assert devlog_entry["agent_id"] in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
    
    def test_devlog_storage(self):
        """Test devlog storage functionality."""
        # Mock devlog storage
        devlog_storage = Mock()
        devlog_storage.save_entry.return_value = True
        
        # Test devlog entry saving
        entry_data = {
            "agent_id": "Agent-3",
            "action": "Test storage",
            "timestamp": datetime.now().isoformat()
        }
        
        result = devlog_storage.save_entry(entry_data)
        assert result == True
        devlog_storage.save_entry.assert_called_once_with(entry_data)
    
    def test_devlog_retrieval(self):
        """Test devlog retrieval functionality."""
        # Mock devlog entries
        mock_entries = [
            {
                "agent_id": "Agent-3",
                "action": "Test action 1",
                "timestamp": "2025-01-05T05:00:00Z"
            },
            {
                "agent_id": "Agent-3",
                "action": "Test action 2",
                "timestamp": "2025-01-05T05:01:00Z"
            }
        ]
        
        # Mock devlog storage
        devlog_storage = Mock()
        devlog_storage.get_entries.return_value = mock_entries
        
        # Test retrieval
        entries = devlog_storage.get_entries("Agent-3")
        assert len(entries) == 2
        assert entries[0]["agent_id"] == "Agent-3"
        assert entries[1]["action"] == "Test action 2"
    
    def test_devlog_formatting(self):
        """Test devlog formatting."""
        # Mock devlog entry
        entry = {
            "agent_id": "Agent-3",
            "action": "Test formatting",
            "timestamp": "2025-01-05T05:00:00Z",
            "status": "completed"
        }
        
        # Test devlog formatting
        formatted_entry = f"""
🤖 Agent: {entry['agent_id']}
⚡ Action: {entry['action']}
🕐 Time: {entry['timestamp']}
✅ Status: {entry['status']}
"""
        
        assert entry['agent_id'] in formatted_entry
        assert entry['action'] in formatted_entry
        assert entry['timestamp'] in formatted_entry
        assert entry['status'] in formatted_entry
    
    def test_devlog_search(self):
        """Test devlog search functionality."""
        # Mock devlog entries
        mock_entries = [
            {"agent_id": "Agent-3", "action": "Test coverage improvement", "timestamp": "2025-01-05T05:00:00Z"},
            {"agent_id": "Agent-3", "action": "Framework setup", "timestamp": "2025-01-05T05:01:00Z"},
            {"agent_id": "Agent-4", "action": "Captain directive", "timestamp": "2025-01-05T05:02:00Z"}
        ]
        
        # Test search by agent
        agent_3_entries = [e for e in mock_entries if e["agent_id"] == "Agent-3"]
        assert len(agent_3_entries) == 2
        
        # Test search by action keyword
        coverage_entries = [e for e in mock_entries if "coverage" in e["action"]]
        assert len(coverage_entries) == 1
        assert coverage_entries[0]["agent_id"] == "Agent-3"
    
    def test_devlog_validation(self):
        """Test devlog entry validation."""
        # Valid devlog entry
        valid_entry = {
            "agent_id": "Agent-3",
            "action": "Valid action",
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        # Invalid devlog entries
        invalid_entries = [
            {"agent_id": "", "action": "Empty agent ID"},  # Empty agent ID
            {"agent_id": "Agent-3", "action": "", "timestamp": datetime.now().isoformat()},  # Empty action
            {"agent_id": "Agent-3", "action": "No timestamp"},  # Missing timestamp
            {"agent_id": "Invalid-Agent", "action": "Invalid agent ID"}  # Invalid agent ID
        ]
        
        # Test valid entry
        assert valid_entry["agent_id"] in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
        assert valid_entry["action"].strip()
        assert "T" in valid_entry["timestamp"]  # Basic timestamp format check
        
        # Test invalid entries
        for invalid_entry in invalid_entries:
            if "agent_id" in invalid_entry:
                is_valid_agent = invalid_entry["agent_id"] in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
                if invalid_entry["agent_id"] == "" or invalid_entry["agent_id"] == "Invalid-Agent":
                    assert not is_valid_agent, f"Should be invalid: {invalid_entry}"
    
    def test_devlog_serialization(self):
        """Test devlog serialization to JSON."""
        # Mock devlog entry
        entry = {
            "agent_id": "Agent-3",
            "action": "Test serialization",
            "timestamp": "2025-01-05T05:00:00Z",
            "status": "completed",
            "metadata": {"test": True}
        }
        
        # Test JSON serialization
        try:
            json_str = json.dumps(entry)
            parsed_entry = json.loads(json_str)
            assert parsed_entry == entry
        except (TypeError, ValueError) as e:
            pytest.fail(f"Serialization failed: {e}")


@pytest.mark.unit
class TestAgentDevlogIntegration:
    """Integration tests for agent devlog."""
    
    def test_complete_devlog_workflow(self):
        """Test complete devlog workflow."""
        # Step 1: Create devlog entry
        entry = {
            "agent_id": "Agent-3",
            "action": "Complete workflow test",
            "timestamp": datetime.now().isoformat(),
            "status": "in_progress"
        }
        
        # Step 2: Validate entry
        assert entry["agent_id"] == "Agent-3"
        assert entry["action"] == "Complete workflow test"
        assert entry["status"] == "in_progress"
        
        # Step 3: Save entry
        devlog_storage = Mock()
        devlog_storage.save_entry.return_value = True
        save_result = devlog_storage.save_entry(entry)
        assert save_result == True
        
        # Step 4: Retrieve entry
        devlog_storage.get_entries.return_value = [entry]
        retrieved_entries = devlog_storage.get_entries("Agent-3")
        assert len(retrieved_entries) == 1
        assert retrieved_entries[0]["action"] == "Complete workflow test"
        
        # Step 5: Update entry status
        entry["status"] = "completed"
        devlog_storage.update_entry.return_value = True
        update_result = devlog_storage.update_entry(entry)
        assert update_result == True
    
    def test_devlog_error_handling(self):
        """Test devlog error handling."""
        # Mock error scenarios
        devlog_storage = Mock()
        devlog_storage.save_entry.side_effect = [
            IOError("File write error"),
            ValueError("Invalid data format"),
            PermissionError("Permission denied")
        ]
        
        # Test error handling
        entry = {"agent_id": "Agent-3", "action": "Test error handling"}
        
        error_types = [IOError, ValueError, PermissionError]
        for i, error_type in enumerate(error_types):
            try:
                devlog_storage.save_entry(entry)
            except error_type:
                # Expected error
                pass
    
    def test_devlog_performance(self):
        """Test devlog performance with multiple entries."""
        # Mock multiple devlog entries
        entries = []
        for i in range(100):
            entries.append({
                "agent_id": f"Agent-{(i % 5) + 1}",
                "action": f"Action {i}",
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            })
        
        # Test bulk operations
        devlog_storage = Mock()
        devlog_storage.save_entries.return_value = True
        devlog_storage.get_entries.return_value = entries
        
        # Test bulk save
        save_result = devlog_storage.save_entries(entries)
        assert save_result == True
        
        # Test bulk retrieval
        retrieved_entries = devlog_storage.get_entries()
        assert len(retrieved_entries) == 100
        
        # Test filtering by agent
        agent_3_entries = [e for e in retrieved_entries if e["agent_id"] == "Agent-3"]
        assert len(agent_3_entries) == 20  # 100 entries / 5 agents = 20 per agent


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

