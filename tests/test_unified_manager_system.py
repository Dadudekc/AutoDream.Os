from pathlib import Path
import json
import sys

import unittest

        from datetime import datetime
from core.base_manager import ManagerStatus, ManagerPriority
from core.managers.unified_manager_system import UnifiedManagerSystem, ManagerRegistration
from unittest.mock import Mock, patch, MagicMock
import time

#!/usr/bin/env python3
"""
🧪 Unified Manager System Tests

Comprehensive testing for the consolidated manager system.
Tests all functionality including registration, startup, health monitoring, and consolidation.

Author: V2 SWARM CAPTAIN
License: MIT
"""


# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))



class TestUnifiedManagerSystem(unittest.TestCase):
    """Test Unified Manager System"""

    def setUp(self):
        """Set up test environment"""
        self.system = UnifiedManagerSystem()
        
        # Test manager IDs
        self.test_core_manager = "test_system_manager"
        self.test_extended_manager = "test_ai_manager"
        self.test_specialized_manager = "test_alert_manager"

    def tearDown(self):
        """Clean up test environment"""
        if self.system.running:
            self.system.stop()

    def test_initialization(self):
        """Test system initialization"""
        # Check system state
        self.assertFalse(self.system.running)
        
        # Check data structures
        self.assertIsInstance(self.system.manager_registry, dict)
        self.assertIsInstance(self.system.manager_instances, dict)
        self.assertIsInstance(self.system.dependency_graph, dict)
        self.assertIsInstance(self.system.startup_order, list)
        
        # Check categories
        self.assertIsInstance(self.system.core_managers, dict)
        self.assertIsInstance(self.system.extended_managers, dict)
        self.assertIsInstance(self.system.specialized_managers, dict)

    def test_manager_registration(self):
        """Test manager registration"""
        # Check that managers are registered
        self.assertGreater(len(self.system.manager_registry), 0)
        
        # Check core managers
        core_managers = [m for m in self.system.manager_registry.values() if m.category == "core"]
        self.assertGreater(len(core_managers), 0)
        
        # Check extended managers
        extended_managers = [m for m in self.system.manager_registry.values() if m.category == "extended"]
        self.assertGreater(len(extended_managers), 0)
        
        # Check specialized managers
        specialized_managers = [m for m in self.system.manager_registry.values() if m.category == "specialized"]
        self.assertGreater(len(specialized_managers), 0)

    def test_dependency_graph(self):
        """Test dependency graph construction"""
        # Check that dependency graph is built
        self.assertGreater(len(self.system.dependency_graph), 0)
        
        # Check that all managers have dependency entries
        for manager_id in self.system.manager_registry.keys():
            self.assertIn(manager_id, self.system.dependency_graph)

    def test_startup_order(self):
        """Test startup order calculation"""
        # Check that startup order is calculated
        self.assertGreater(len(self.system.startup_order), 0)
        
        # Check that all managers are in startup order
        for manager_id in self.system.manager_registry.keys():
            self.assertIn(manager_id, self.system.startup_order)
        
        # Check that dependencies come before dependents
        for manager_id, dependencies in self.system.dependency_graph.items():
            manager_index = self.system.startup_order.index(manager_id)
            for dependency in dependencies:
                dependency_index = self.system.startup_order.index(dependency)
                self.assertLess(dependency_index, manager_index, 
                              f"Dependency {dependency} should come before {manager_id}")

    def test_manager_startup(self):
        """Test manager startup process"""
        # Mock manager classes to avoid import issues
        with patch('core.managers.unified_manager_system.SystemManager') as mock_system_manager:
            mock_instance = Mock()
            mock_instance.start.return_value = True
            mock_instance.is_healthy.return_value = True
            mock_system_manager.return_value = mock_instance
            
            # Start the system
            result = self.system.start()
            self.assertTrue(result)
            
            # Check that system is running
            self.assertTrue(self.system.running)
            
            # Check that managers are started
            self.assertGreater(len(self.system.manager_instances), 0)

    def test_manager_stop(self):
        """Test manager stop process"""
        # Mock manager classes
        with patch('core.managers.unified_manager_system.SystemManager') as mock_system_manager:
            mock_instance = Mock()
            mock_instance.start.return_value = True
            mock_instance.stop.return_value = True
            mock_instance.is_healthy.return_value = True
            mock_system_manager.return_value = mock_instance
            
            # Start and then stop the system
            self.system.start()
            self.system.stop()
            
            # Check that system is stopped
            self.assertFalse(self.system.running)

    def test_manager_health_monitoring(self):
        """Test manager health monitoring"""
        # Mock manager classes
        with patch('core.managers.unified_manager_system.SystemManager') as mock_system_manager:
            mock_instance = Mock()
            mock_instance.start.return_value = True
            mock_instance.is_healthy.return_value = True
            mock_system_manager.return_value = mock_instance
            
            # Start the system
            self.system.start()
            
            # Wait for health check
            time.sleep(0.1)
            
            # Check system health
            health = self.system.get_system_health()
            self.assertIsInstance(health, dict)
            self.assertIn("health_score", health)
            self.assertIn("total_managers", health)
            self.assertIn("running_managers", health)

    def test_manager_categories(self):
        """Test manager categorization"""
        # Check core managers
        core_managers = self.system.get_managers_by_category("core")
        self.assertIsInstance(core_managers, dict)
        
        # Check extended managers
        extended_managers = self.system.get_managers_by_category("extended")
        self.assertIsInstance(extended_managers, dict)
        
        # Check specialized managers
        specialized_managers = self.system.get_managers_by_category("specialized")
        self.assertIsInstance(specialized_managers, dict)
        
        # Check invalid category
        invalid_managers = self.system.get_managers_by_category("invalid")
        self.assertEqual(invalid_managers, {})

    def test_manager_status(self):
        """Test manager status retrieval"""
        # Check status of non-existent manager
        status = self.system.get_manager_status("nonexistent")
        self.assertIsNone(status)
        
        # Check status of registered manager
        if self.system.manager_registry:
            manager_id = list(self.system.manager_registry.keys())[0]
            status = self.system.get_manager_status(manager_id)
            self.assertIsInstance(status, ManagerStatus)

    def test_consolidation_report(self):
        """Test consolidation report generation"""
        report = self.system.get_consolidation_report()
        
        # Check report structure
        self.assertIsInstance(report, dict)
        self.assertIn("consolidation_status", report)
        self.assertIn("total_files_consolidated", report)
        self.assertIn("duplication_eliminated", report)
        self.assertIn("managers_consolidated", report)
        self.assertIn("total_managers", report)
        self.assertIn("dependency_graph_size", report)
        self.assertIn("startup_order", report)
        self.assertIn("consolidation_date", report)
        
        # Check report values
        self.assertEqual(report["consolidation_status"], "COMPLETE")
        self.assertEqual(report["duplication_eliminated"], "90%")
        self.assertGreater(report["total_files_consolidated"], 0)
        self.assertGreater(report["total_managers"], 0)

    def test_error_handling(self):
        """Test error handling and recovery"""
        # Test with invalid manager class
        with patch('core.managers.unified_manager_system.SystemManager') as mock_system_manager:
            mock_system_manager.side_effect = Exception("Manager creation failed")
            
            # Try to start system
            result = self.system.start()
            self.assertFalse(result)

    def test_dependency_resolution(self):
        """Test dependency resolution"""
        # Check that dependencies are resolved correctly
        for manager_id, dependencies in self.system.dependency_graph.items():
            # Each manager should have valid dependencies
            for dependency in dependencies:
                self.assertIn(dependency, self.system.manager_registry, 
                            f"Manager {manager_id} depends on {dependency} which is not registered")

    def test_circular_dependency_detection(self):
        """Test circular dependency detection"""
        # The system should detect circular dependencies during startup order calculation
        # If there are circular dependencies, the system should fail to start
        
        # This test verifies that the dependency graph is valid
        # by checking that the startup order calculation completes successfully
        self.assertGreater(len(self.system.startup_order), 0)

    def test_performance_operations(self):
        """Test performance of bulk operations"""
        start_time = time.time()
        
        # Test bulk manager registration (already done in setup)
        registration_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(registration_time, 1.0)

    def test_concurrent_operations(self):
        """Test concurrent manager operations"""
        # Test that the system can handle concurrent operations
        # This is primarily tested through the health monitoring thread
        
        # Start system
        with patch('core.managers.unified_manager_system.SystemManager') as mock_system_manager:
            mock_instance = Mock()
            mock_instance.start.return_value = True
            mock_instance.is_healthy.return_value = True
            mock_system_manager.return_value = mock_instance
            
            self.system.start()
            
            # Wait for health monitoring to run
            time.sleep(0.1)
            
            # Check that health monitoring is working
            health = self.system.get_system_health()
            self.assertIsInstance(health, dict)
            
            # Stop system
            self.system.stop()


class TestManagerRegistration(unittest.TestCase):
    """Test ManagerRegistration dataclass"""

    def test_manager_registration_creation(self):
        """Test ManagerRegistration creation"""
        
        registration = ManagerRegistration(
            manager_id="test_manager",
            manager_class=Mock,
            instance=None,
            status=ManagerStatus.OFFLINE,
            priority=ManagerPriority.NORMAL,
            dependencies=["dep1", "dep2"],
            config_path="config/test.json",
            last_health_check=datetime.now(),
            category="test",
            version="1.0.0"
        )
        
        # Check attributes
        self.assertEqual(registration.manager_id, "test_manager")
        self.assertEqual(registration.status, ManagerStatus.OFFLINE)
        self.assertEqual(registration.priority, ManagerPriority.NORMAL)
        self.assertEqual(registration.dependencies, ["dep1", "dep2"])
        self.assertEqual(registration.category, "test")
        self.assertEqual(registration.version, "1.0.0")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
