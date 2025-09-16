#!/usr/bin/env python3
"""
Coordinate Loader Core Testing Suite
====================================

Core test suite for the CoordinateLoader class.
Tests cover essential functionality:
- Coordinate loading from configuration files
- Default coordinate fallback
- Agent coordinate retrieval
- Error handling

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import json
import pytest
from unittest.mock import Mock, patch, mock_open

from src.core.coordinate_loader import CoordinateLoader


class TestCoordinateLoaderCore:
    """Core unit tests for CoordinateLoader class."""

    def test_loader_initialization_default(self):
        """Test CoordinateLoader initialization with default config path."""
        loader = CoordinateLoader()
        
        assert loader.config_path == "config/coordinates.json"
        assert loader.coordinates == {}

    def test_loader_initialization_custom_path(self):
        """Test CoordinateLoader initialization with custom config path."""
        custom_path = "custom/path/coordinates.json"
        loader = CoordinateLoader(config_path=custom_path)
        
        assert loader.config_path == custom_path
        assert loader.coordinates == {}

    def test_load_coordinates_success(self):
        """Test successful coordinate loading from file."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]},
                "Agent-2": {"chat_input_coordinates": [300, 400]}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('os.path.exists', return_value=True):
                loader = CoordinateLoader()
                loader.load()
                
                assert loader.coordinates == mock_coordinates

    def test_load_coordinates_file_not_found(self):
        """Test coordinate loading when file doesn't exist."""
        with patch('os.path.exists', return_value=False):
            loader = CoordinateLoader()
            loader.load()
            
            # Should use default coordinates
            assert "agents" in loader.coordinates
            assert "Agent-1" in loader.coordinates["agents"]

    def test_load_coordinates_invalid_json(self):
        """Test coordinate loading with invalid JSON."""
        with patch('builtins.open', mock_open(read_data="invalid json content")):
            with patch('os.path.exists', return_value=True):
                loader = CoordinateLoader()
                loader.load()
                
                # Should use default coordinates
                assert "agents" in loader.coordinates
                assert "Agent-1" in loader.coordinates["agents"]

    def test_get_default_coordinates(self):
        """Test default coordinates structure."""
        loader = CoordinateLoader()
        default_coords = loader._get_default_coordinates()
        
        assert "agents" in default_coords
        assert len(default_coords["agents"]) == 8
        
        # Check specific agents
        assert "Agent-1" in default_coords["agents"]
        assert "Agent-4" in default_coords["agents"]
        assert "Agent-8" in default_coords["agents"]
        
        # Check coordinate structure
        agent1_coords = default_coords["agents"]["Agent-1"]
        assert "chat_input_coordinates" in agent1_coords
        assert isinstance(agent1_coords["chat_input_coordinates"], list)
        assert len(agent1_coords["chat_input_coordinates"]) == 2

    def test_get_agent_coordinates_success(self):
        """Test successful agent coordinate retrieval."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]},
                "Agent-2": {"chat_input_coordinates": [300, 400]}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('os.path.exists', return_value=True):
                loader = CoordinateLoader()
                loader.load()
                
                coords = loader.get_agent_coordinates("Agent-1")
                assert coords == (100, 200)

    def test_get_agent_coordinates_agent_not_found(self):
        """Test agent coordinate retrieval for non-existent agent."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('os.path.exists', return_value=True):
                loader = CoordinateLoader()
                loader.load()
                
                with pytest.raises(ValueError, match="Agent NonExistentAgent not found"):
                    loader.get_agent_coordinates("NonExistentAgent")

    def test_get_agent_coordinates_missing_coordinates(self):
        """Test agent coordinate retrieval when coordinates are missing."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"other_data": "value"}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('os.path.exists', return_value=True):
                loader = CoordinateLoader()
                loader.load()
                
                coords = loader.get_agent_coordinates("Agent-1")
                assert coords == (0, 0)

    def test_get_all_coordinates_success(self):
        """Test getting all agent coordinates."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]},
                "Agent-2": {"chat_input_coordinates": [300, 400]},
                "Agent-3": {"other_data": "value"}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('os.path.exists', return_value=True):
                loader = CoordinateLoader()
                loader.load()
                
                all_coords = loader.get_all_coordinates()
                
                assert all_coords["Agent-1"] == (100, 200)
                assert all_coords["Agent-2"] == (300, 400)
                assert all_coords["Agent-3"] == (0, 0)

    def test_get_agent_ids_success(self):
        """Test getting list of agent IDs."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]},
                "Agent-2": {"chat_input_coordinates": [300, 400]},
                "Agent-3": {"chat_input_coordinates": [500, 600]}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('os.path.exists', return_value=True):
                loader = CoordinateLoader()
                loader.load()
                
                agent_ids = loader.get_agent_ids()
                
                assert len(agent_ids) == 3
                assert "Agent-1" in agent_ids
                assert "Agent-2" in agent_ids
                assert "Agent-3" in agent_ids

    def test_get_coords_success(self):
        """Test getting coordinates object for agent."""
        mock_coordinates = {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [100, 200]}
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_coordinates))):
            with patch('os.path.exists', return_value=True):
                loader = CoordinateLoader()
                loader.load()
                
                coords_obj = loader.get_coords("Agent-1")
                
                assert hasattr(coords_obj, 'tuple')
                assert coords_obj.tuple == (100, 200)

    def test_validate_all_success(self):
        """Test coordinate validation."""
        loader = CoordinateLoader()
        validation_report = loader.validate_all()
        
        assert hasattr(validation_report, 'is_all_ok')
        assert hasattr(validation_report, 'issues')
        assert validation_report.is_all_ok() is True
        assert validation_report.issues == []


if __name__ == "__main__":
    """Run tests directly for development."""
    print("🧪 CoordinateLoader Core Testing Suite")
    print("=" * 50)
    
    # Run basic tests
    test_instance = TestCoordinateLoaderCore()
    
    try:
        test_instance.test_loader_initialization_default()
        print("✅ Loader initialization test passed")
    except Exception as e:
        print(f"❌ Loader initialization test failed: {e}")
    
    try:
        test_instance.test_load_coordinates_success()
        print("✅ Load coordinates success test passed")
    except Exception as e:
        print(f"❌ Load coordinates success test failed: {e}")
    
    try:
        test_instance.test_get_agent_coordinates_success()
        print("✅ Get agent coordinates test passed")
    except Exception as e:
        print(f"❌ Get agent coordinates test failed: {e}")
    
    print("\n🎉 Core CoordinateLoader tests completed!")
    print("📊 Run full suite with: python -m pytest tests/unit/test_coordinate_loader_core.py -v")