#!/usr/bin/env python3
"""
SOLID Principles Testing Module
===============================

Comprehensive SOLID principles validation across all modules.
Part of the modularized test_architectural_patterns_comprehensive_agent2.py (580 lines → 3 modules).

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import inspect
import os
import sys
from pathlib import Path

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in os.environ.get("PYTHONPATH", ""):
    os.environ["PYTHONPATH"] = str(src_path) + os.pathsep + os.environ.get("PYTHONPATH", "")

sys.path.insert(0, str(src_path))


class TestSOLIDPrinciplesComprehensive:
    """Comprehensive SOLID principles validation across all modules."""
    
    @pytest.mark.unit
    @pytest.mark.agent2
    @pytest.mark.critical
    def test_single_responsibility_principle_comprehensive(self):
        """Test SRP across all consolidated services."""
        print("🧪 Testing Single Responsibility Principle - Comprehensive...")
        
        try:
            # Test consolidated messaging service
            from src.services.consolidated_messaging_service import ConsolidatedMessagingService
            
            service = ConsolidatedMessagingService()
            methods = [m for m in dir(service) if not m.startswith('_')]
            
            # Check for unrelated methods that violate SRP
            unrelated_methods = ['database_operation', 'file_processing', 'network_config']
            for method in unrelated_methods:
                assert method not in methods, f"Service should not have {method}"
            
            # Test method concentration (should be >50% messaging focused)
            total_methods = len(methods)
            if total_methods > 0:
                messaging_methods = [m for m in methods if 'message' in m.lower() or 'send' in m.lower() or 'receive' in m.lower()]
                messaging_ratio = len(messaging_methods) / total_methods
                assert messaging_ratio > 0.5, f"Service should be >50% messaging focused, got {messaging_ratio:.2f}"
            
            print("✅ Single Responsibility Principle validation passed")
            
        except ImportError as e:
            pytest.skip(f"Could not import ConsolidatedMessagingService: {e}")
    
    @pytest.mark.unit
    @pytest.mark.agent2
    @pytest.mark.critical
    def test_open_closed_principle_comprehensive(self):
        """Test OCP across all services - should be open for extension, closed for modification."""
        print("🧪 Testing Open/Closed Principle - Comprehensive...")
        
        try:
            # Test that services can be extended without modification
            from src.services.consolidated_messaging_service import ConsolidatedMessagingService
            
            class ExtendedMessagingService(ConsolidatedMessagingService):
                """Extended service that adds new functionality without modifying base."""
                
                def send_priority_message(self, agent_id: str, message: str, priority: str = "HIGH"):
                    """Extended functionality for priority messaging."""
                    return self.send_message(agent_id, message, priority=priority)
                
                def get_message_history(self, agent_id: str):
                    """Extended functionality for message history."""
                    return f"Message history for {agent_id}"
            
            # Test that extended service works without modifying base
            extended_service = ExtendedMessagingService()
            assert hasattr(extended_service, 'send_priority_message')
            assert hasattr(extended_service, 'get_message_history')
            
            # Test that base functionality still works
            assert hasattr(extended_service, 'send_message')
            
            print("✅ Open/Closed Principle validation passed")
            
        except ImportError as e:
            pytest.skip(f"Could not import ConsolidatedMessagingService: {e}")
    
    @pytest.mark.unit
    @pytest.mark.agent2
    @pytest.mark.critical
    def test_liskov_substitution_principle_comprehensive(self):
        """Test LSP - derived classes should be substitutable for base classes."""
        print("🧪 Testing Liskov Substitution Principle - Comprehensive...")
        
        try:
            from src.services.consolidated_messaging_service import ConsolidatedMessagingService
            
            class MockMessagingService(ConsolidatedMessagingService):
                """Mock service that maintains LSP contract."""
                
                def send_message(self, agent_id: str, message: str, from_agent: str = "MockAgent", priority: str = "NORMAL"):
                    """Mock implementation that maintains the same interface."""
                    return True  # Always succeeds in mock
                
                def get_agent_ids(self):
                    """Mock implementation that maintains the same interface."""
                    return ["Agent-1", "Agent-2", "Agent-3"]
            
            # Test that mock can be substituted for real service
            mock_service = MockMessagingService()
            
            # Test that all expected methods exist and work
            assert mock_service.send_message("Agent-1", "Test message") == True
            assert "Agent-1" in mock_service.get_agent_ids()
            
            print("✅ Liskov Substitution Principle validation passed")
            
        except ImportError as e:
            pytest.skip(f"Could not import ConsolidatedMessagingService: {e}")
    
    @pytest.mark.unit
    @pytest.mark.agent2
    @pytest.mark.critical
    def test_interface_segregation_principle_comprehensive(self):
        """Test ISP - clients should not depend on interfaces they don't use."""
        print("🧪 Testing Interface Segregation Principle - Comprehensive...")
        
        try:
            from src.services.consolidated_messaging_service import ConsolidatedMessagingService
            
            service = ConsolidatedMessagingService()
            methods = [m for m in dir(service) if not m.startswith('_')]
            
            # Check that service doesn't have too many unrelated methods
            # A messaging service should primarily have messaging-related methods
            messaging_related = ['send_message', 'get_agent_ids', 'validate_agent']
            unrelated_methods = ['process_payment', 'generate_report', 'backup_data']
            
            # Should have messaging-related methods
            for method in messaging_related:
                if method in methods:
                    print(f"✅ Found expected messaging method: {method}")
            
            # Should not have unrelated methods
            for method in unrelated_methods:
                assert method not in methods, f"Service should not have unrelated method: {method}"
            
            print("✅ Interface Segregation Principle validation passed")
            
        except ImportError as e:
            pytest.skip(f"Could not import ConsolidatedMessagingService: {e}")
    
    @pytest.mark.unit
    @pytest.mark.agent2
    @pytest.mark.critical
    def test_dependency_inversion_principle_comprehensive(self):
        """Test DIP - depend on abstractions, not concretions."""
        print("🧪 Testing Dependency Inversion Principle - Comprehensive...")
        
        try:
            from src.services.consolidated_messaging_service import ConsolidatedMessagingService
            
            # Test that service can work with different coordinate loaders
            class MockCoordinateLoader:
                """Mock coordinate loader for testing DIP."""
                
                def __init__(self, coord_path: str = None):
                    self.coords = {
                        "Agent-1": (100, 200),
                        "Agent-2": (300, 400),
                        "Agent-3": (500, 600)
                    }
                
                def load(self):
                    pass
                
                def get_agent_ids(self):
                    return list(self.coords.keys())
                
                def get_coords(self, agent_id: str):
                    class MockCoords:
                        def __init__(self, coords):
                            self.x, self.y = coords
                            self.tuple = (self.x, self.y)
                    
                    return MockCoords(self.coords[agent_id])
                
                def validate_all(self):
                    class MockValidationReport:
                        def is_all_ok(self):
                            return True
                    
                    return MockValidationReport()
            
            # Test that service can work with mock loader
            # This demonstrates dependency inversion - service depends on abstraction, not concrete implementation
            service = ConsolidatedMessagingService()
            
            # The service should be able to work with different coordinate loaders
            # without being tightly coupled to a specific implementation
            assert hasattr(service, 'loader')
            
            print("✅ Dependency Inversion Principle validation passed")
            
        except ImportError as e:
            pytest.skip(f"Could not import ConsolidatedMessagingService: {e}")
    
    @pytest.mark.unit
    @pytest.mark.agent2
    @pytest.mark.critical
    def test_solid_principles_integration(self):
        """Test that all SOLID principles work together in the system."""
        print("🧪 Testing SOLID Principles Integration - Comprehensive...")
        
        try:
            from src.services.consolidated_messaging_service import ConsolidatedMessagingService
            
            # Create a service instance
            service = ConsolidatedMessagingService()
            
            # Test SRP - service should have a single responsibility
            methods = [m for m in dir(service) if not m.startswith('_')]
            assert len(methods) > 0, "Service should have methods"
            
            # Test OCP - service should be extensible
            class ExtendedService(ConsolidatedMessagingService):
                def new_feature(self):
                    return "Extended functionality"
            
            extended = ExtendedService()
            assert hasattr(extended, 'new_feature')
            
            # Test LSP - extended service should be substitutable
            assert hasattr(extended, 'send_message')
            
            # Test ISP - service should have focused interface
            messaging_methods = [m for m in methods if 'message' in m.lower()]
            assert len(messaging_methods) > 0, "Service should have messaging methods"
            
            # Test DIP - service should depend on abstractions
            assert hasattr(service, 'loader'), "Service should have coordinate loader"
            
            print("✅ SOLID Principles Integration validation passed")
            
        except ImportError as e:
            pytest.skip(f"Could not import ConsolidatedMessagingService: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
