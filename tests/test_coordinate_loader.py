#!/usr/bin/env python3
"""
Test Coordinate Loader - Comprehensive Test Suite
=================================================

Comprehensive test suite for coordinate loader functionality.
Tests all coordinate loading, validation, and management features.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestCoordinateLoader:
    """Test suite for coordinate loader."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.coord_path = str(Path(__file__).parent.parent / "config" / "coordinates.json")
        self.test_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        self.expected_coordinates = {
            "Agent-1": (-1269, 481),
            "Agent-2": (-308, 480),
            "Agent-3": (-1269, 1001),
            "Agent-4": (-308, 1000),
            "Agent-5": (652, 421),
            "Agent-6": (1612, 419),
            "Agent-7": (920, 851),
            "Agent-8": (1611, 941)
        }
    
    def test_coordinate_loader_initialization(self):
        """Test coordinate loader initialization."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader()
        assert loader.config_path == "config/coordinates.json"
        assert loader.coordinates == {}
        
        loader = CoordinateLoader("custom/path.json")
        assert loader.config_path == "custom/path.json"
        assert loader.coordinates == {}
    
    def test_coordinate_loading_success(self):
        """Test successful coordinate loading."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        assert "agents" in loader.coordinates
        assert len(loader.coordinates["agents"]) == 8
        
        for agent_id in self.test_agents:
            assert agent_id in loader.coordinates["agents"]
            agent_data = loader.coordinates["agents"][agent_id]
            assert "chat_input_coordinates" in agent_data
            assert "active" in agent_data
            assert "description" in agent_data
    
    def test_coordinate_loading_file_not_found(self):
        """Test coordinate loading when file doesn't exist."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader("nonexistent/path.json")
        loader.load()
        
        # Should fall back to default coordinates
        assert "agents" in loader.coordinates
        assert len(loader.coordinates["agents"]) == 8
    
    def test_coordinate_loading_invalid_json(self):
        """Test coordinate loading with invalid JSON."""
        from core.coordinate_loader import CoordinateLoader
        
        # Create temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name
        
        try:
            loader = CoordinateLoader(temp_path)
            loader.load()
            
            # Should fall back to default coordinates
            assert "agents" in loader.coordinates
            assert len(loader.coordinates["agents"]) == 8
        finally:
            Path(temp_path).unlink()
    
    def test_get_agent_coordinates_success(self):
        """Test successful agent coordinate retrieval."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        for agent_id, expected_coords in self.expected_coordinates.items():
            coords = loader.get_agent_coordinates(agent_id)
            assert coords == expected_coords
    
    def test_get_agent_coordinates_invalid_agent(self):
        """Test agent coordinate retrieval with invalid agent."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        with pytest.raises(ValueError, match="Agent InvalidAgent not found in coordinates"):
            loader.get_agent_coordinates("InvalidAgent")
    
    def test_get_all_coordinates(self):
        """Test getting all coordinates."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        all_coords = loader.get_all_coordinates()
        assert len(all_coords) == 8
        
        for agent_id, expected_coords in self.expected_coordinates.items():
            assert agent_id in all_coords
            assert all_coords[agent_id] == expected_coords
    
    def test_get_agent_ids(self):
        """Test getting agent IDs."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        agent_ids = loader.get_agent_ids()
        assert len(agent_ids) == 8
        assert set(agent_ids) == set(self.test_agents)
    
    def test_get_coords_compatibility(self):
        """Test get_coords method for compatibility."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        for agent_id, expected_coords in self.expected_coordinates.items():
            coords_obj = loader.get_coords(agent_id)
            assert hasattr(coords_obj, 'tuple')
            assert coords_obj.tuple == expected_coords
    
    def test_get_coords_invalid_agent(self):
        """Test get_coords method with invalid agent."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        with pytest.raises(ValueError, match="Agent InvalidAgent not found in coordinates"):
            loader.get_coords("InvalidAgent")
    
    def test_validate_all(self):
        """Test validate_all method."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        validation_report = loader.validate_all()
        assert hasattr(validation_report, 'is_all_ok')
        assert hasattr(validation_report, 'issues')
        assert validation_report.is_all_ok() == True
        assert validation_report.issues == []
    
    def test_coordinate_data_structure(self):
        """Test coordinate data structure."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        for agent_id in self.test_agents:
            agent_data = loader.coordinates["agents"][agent_id]
            
            # Check required fields
            assert "active" in agent_data
            assert "chat_input_coordinates" in agent_data
            assert "onboarding_coordinates" in agent_data
            assert "description" in agent_data
            
            # Check data types
            assert isinstance(agent_data["active"], bool)
            assert isinstance(agent_data["chat_input_coordinates"], list)
            assert isinstance(agent_data["onboarding_coordinates"], list)
            assert isinstance(agent_data["description"], str)
            
            # Check coordinate format
            assert len(agent_data["chat_input_coordinates"]) == 2
            assert len(agent_data["onboarding_coordinates"]) == 2
            assert all(isinstance(coord, int) for coord in agent_data["chat_input_coordinates"])
            assert all(isinstance(coord, int) for coord in agent_data["onboarding_coordinates"])
    
    def test_coordinate_loader_thread_safety(self):
        """Test coordinate loader thread safety."""
        from core.coordinate_loader import CoordinateLoader
        import threading
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        results = []
        
        def get_coordinates():
            for agent_id in self.test_agents:
                coords = loader.get_agent_coordinates(agent_id)
                results.append((agent_id, coords))
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=get_coordinates)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all results are correct
        assert len(results) == 5 * 8  # 5 threads * 8 agents
        
        for agent_id, coords in results:
            assert coords == self.expected_coordinates[agent_id]
    
    def test_coordinate_loader_memory_usage(self):
        """Test coordinate loader memory usage."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        # Test multiple loads don't cause memory leaks
        for _ in range(10):
            loader.load()
            coords = loader.get_agent_coordinates("Agent-1")
            assert coords == self.expected_coordinates["Agent-1"]
    
    def test_coordinate_loader_error_handling(self):
        """Test coordinate loader error handling."""
        from core.coordinate_loader import CoordinateLoader
        
        # Test with None path
        loader = CoordinateLoader(None)
        loader.load()
        assert "agents" in loader.coordinates
        
        # Test with empty string path
        loader = CoordinateLoader("")
        loader.load()
        assert "agents" in loader.coordinates
    
    def test_coordinate_loader_performance(self):
        """Test coordinate loader performance."""
        from core.coordinate_loader import CoordinateLoader
        import time
        
        loader = CoordinateLoader(self.coord_path)
        
        # Test load performance
        start_time = time.time()
        loader.load()
        load_time = time.time() - start_time
        
        # Load should be fast (less than 1 second)
        assert load_time < 1.0
        
        # Test coordinate retrieval performance
        start_time = time.time()
        for _ in range(1000):
            coords = loader.get_agent_coordinates("Agent-1")
        retrieval_time = time.time() - start_time
        
        # Retrieval should be very fast (less than 0.1 seconds for 1000 calls)
        assert retrieval_time < 0.1
    
    def test_coordinate_loader_edge_cases(self):
        """Test coordinate loader edge cases."""
        from core.coordinate_loader import CoordinateLoader
        
        loader = CoordinateLoader(self.coord_path)
        loader.load()
        
        # Test with empty agent ID
        with pytest.raises(ValueError):
            loader.get_agent_coordinates("")
        
        # Test with None agent ID
        with pytest.raises(ValueError):
            loader.get_agent_coordinates(None)
        
        # Test with whitespace agent ID
        with pytest.raises(ValueError):
            loader.get_agent_coordinates("   ")
    
    def test_coordinate_loader_custom_coordinates(self):
        """Test coordinate loader with custom coordinates."""
        from core.coordinate_loader import CoordinateLoader
        
        # Create custom coordinates
        custom_coords = {
            "version": "2.0",
            "agents": {
                "CustomAgent-1": {
                    "active": True,
                    "chat_input_coordinates": [100, 200],
                    "onboarding_coordinates": [150, 250],
                    "description": "Custom Agent 1"
                },
                "CustomAgent-2": {
                    "active": False,
                    "chat_input_coordinates": [300, 400],
                    "onboarding_coordinates": [350, 450],
                    "description": "Custom Agent 2"
                }
            }
        }
        
        # Create temporary file with custom coordinates
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(custom_coords, f)
            temp_path = f.name
        
        try:
            loader = CoordinateLoader(temp_path)
            loader.load()
            
            # Test custom coordinates
            coords1 = loader.get_agent_coordinates("CustomAgent-1")
            assert coords1 == (100, 200)
            
            coords2 = loader.get_agent_coordinates("CustomAgent-2")
            assert coords2 == (300, 400)
            
            agent_ids = loader.get_agent_ids()
            assert len(agent_ids) == 2
            assert "CustomAgent-1" in agent_ids
            assert "CustomAgent-2" in agent_ids
            
        finally:
            Path(temp_path).unlink()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])


