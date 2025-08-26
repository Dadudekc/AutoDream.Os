#!/usr/bin/env python3
"""
Status Manager Consolidation Integration Test
============================================

Tests the consolidated StatusManager to ensure all functionality
from the 7 deleted files is properly integrated.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import unittest
import tempfile
import shutil
import os
import time
import json
from pathlib import Path
from unittest.mock import Mock, patch

from src.core.managers.status_manager import (
    StatusManager,
    StatusLevel,
    HealthStatus,
    UpdateFrequency,
    StatusEventType,
    StatusItem,
    HealthMetric,
    ComponentHealth,
    StatusEvent,
    StatusMetrics,
    ActivitySummary
)


class TestStatusManagerConsolidation(unittest.TestCase):
    """Test consolidated status manager system"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / "config"
        self.config_dir.mkdir()
        
        # Create test configuration
        self.test_config = {
            "health_check_interval": 30,
            "max_status_history": 100,
            "auto_resolve_timeout": 3600
        }
        
        self.config_file = self.config_dir / "status_manager.json"
        with open(self.config_file, 'w') as f:
            json.dump(self.test_config, f)
        
        # Initialize manager
        self.status_manager = StatusManager(str(self.config_file))
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            self.status_manager.shutdown()
        except:
            pass
        shutil.rmtree(self.temp_dir)
    
    def test_01_initialization(self):
        """Test StatusManager initialization"""
        self.assertIsNotNone(self.status_manager)
        self.assertEqual(self.status_manager.manager_id, "status_manager")
        self.assertEqual(self.status_manager.name, "StatusManager")
        self.assertEqual(self.status_manager.description, "Unified status manager consolidating 7 separate files")
        
        # Check data structures
        self.assertIsInstance(self.status_manager.status_items, dict)
        self.assertIsInstance(self.status_manager.component_health, dict)
        self.assertIsInstance(self.status_manager.health_checks, dict)
        self.assertIsInstance(self.status_manager.status_events, dict)
    
    def test_02_status_levels(self):
        """Test StatusLevel enum values"""
        self.assertEqual(StatusLevel.INFO.value, "info")
        self.assertEqual(StatusLevel.WARNING.value, "warning")
        self.assertEqual(StatusLevel.ERROR.value, "error")
        self.assertEqual(StatusLevel.CRITICAL.value, "critical")
        self.assertEqual(StatusLevel.SUCCESS.value, "success")
    
    def test_03_health_status(self):
        """Test HealthStatus enum values"""
        self.assertEqual(HealthStatus.HEALTHY.value, "healthy")
        self.assertEqual(HealthStatus.DEGRADED.value, "degraded")
        self.assertEqual(HealthStatus.UNHEALTHY.value, "unhealthy")
        self.assertEqual(HealthStatus.CRITICAL.value, "critical")
        self.assertEqual(HealthStatus.UNKNOWN.value, "unknown")
    
    def test_04_update_frequency(self):
        """Test UpdateFrequency enum values"""
        self.assertEqual(UpdateFrequency.REAL_TIME.value, "real_time")
        self.assertEqual(UpdateFrequency.HIGH_FREQUENCY.value, "high_frequency")
        self.assertEqual(UpdateFrequency.MEDIUM_FREQUENCY.value, "medium_frequency")
        self.assertEqual(UpdateFrequency.LOW_FREQUENCY.value, "low_frequency")
    
    def test_05_status_event_types(self):
        """Test StatusEventType enum values"""
        self.assertEqual(StatusEventType.STATUS_CHANGE.value, "status_change")
        self.assertEqual(StatusEventType.HEALTH_ALERT.value, "health_alert")
        self.assertEqual(StatusEventType.PERFORMANCE_DEGRADATION.value, "performance_degradation")
        self.assertEqual(StatusEventType.SYSTEM_ERROR.value, "system_error")
        self.assertEqual(StatusEventType.RECOVERY.value, "recovery")
    
    def test_06_add_status(self):
        """Test adding status items"""
        # Add status for test component
        status_id = self.status_manager.add_status(
            "test_component",
            "operational",
            StatusLevel.SUCCESS,
            "Test status message",
            {"test": True}
        )
        
        self.assertIsNotNone(status_id)
        self.assertIn(status_id, self.status_manager.status_items)
        
        # Verify status item
        status_item = self.status_manager.status_items[status_id]
        self.assertEqual(status_item.component, "test_component")
        self.assertEqual(status_item.status, "operational")
        self.assertEqual(status_item.level, StatusLevel.SUCCESS)
        self.assertEqual(status_item.message, "Test status message")
        self.assertEqual(status_item.metadata, {"test": True})
        self.assertFalse(status_item.resolved)
    
    def test_07_get_status(self):
        """Test status retrieval"""
        # Add multiple status items
        self.status_manager.add_status("comp1", "online", StatusLevel.SUCCESS, "Component 1 online")
        self.status_manager.add_status("comp2", "offline", StatusLevel.ERROR, "Component 2 offline")
        self.status_manager.add_status("comp1", "degraded", StatusLevel.WARNING, "Component 1 degraded")
        
        # Get status for specific component
        comp1_status = self.status_manager.get_status("comp1")
        self.assertIsInstance(comp1_status, StatusItem)
        self.assertEqual(comp1_status.component, "comp1")
        self.assertEqual(comp1_status.status, "degraded")  # Most recent
        
        # Get all status items
        all_status = self.status_manager.get_status()
        self.assertIsInstance(all_status, list)
        self.assertEqual(len(all_status), 3)
    
    def test_08_health_checks(self):
        """Test health check functionality"""
        # Register custom health check
        def test_health_check():
            return HealthStatus.HEALTHY
        
        self.status_manager.register_health_check("test_check", test_health_check)
        self.assertIn("test_check", self.status_manager.health_checks)
        
        # Run health checks
        results = self.status_manager.run_health_checks()
        self.assertIsInstance(results, dict)
        self.assertIn("test_check", results)
        self.assertEqual(results["test_check"], HealthStatus.HEALTHY)
    
    def test_09_status_summary(self):
        """Test status summary generation"""
        # Add various status items
        self.status_manager.add_status("comp1", "online", StatusLevel.SUCCESS, "Healthy")
        self.status_manager.add_status("comp2", "warning", StatusLevel.WARNING, "Warning")
        self.status_manager.add_status("comp3", "error", StatusLevel.ERROR, "Error")
        self.status_manager.add_status("comp4", "critical", StatusLevel.CRITICAL, "Critical")
        
        # Get summary
        summary = self.status_manager.get_status_summary()
        self.assertIsInstance(summary, StatusMetrics)
        self.assertEqual(summary.total_components, 4)
        self.assertEqual(summary.healthy_components, 1)
        self.assertEqual(summary.warning_components, 1)
        self.assertEqual(summary.error_components, 1)
        self.assertEqual(summary.critical_components, 1)
    
    def test_10_active_alerts(self):
        """Test active alerts retrieval"""
        # Add status items with different levels
        self.status_manager.add_status("comp1", "online", StatusLevel.SUCCESS, "Healthy")
        self.status_manager.add_status("comp2", "warning", StatusLevel.WARNING, "Warning")
        self.status_manager.add_status("comp3", "error", StatusLevel.ERROR, "Error")
        
        # Get active alerts (warning, error, critical)
        alerts = self.status_manager.get_active_alerts()
        self.assertIsInstance(alerts, list)
        self.assertEqual(len(alerts), 2)  # warning + error
        
        # Verify alert levels
        alert_levels = [alert.level for alert in alerts]
        self.assertIn(StatusLevel.WARNING, alert_levels)
        self.assertIn(StatusLevel.ERROR, alert_levels)
        self.assertNotIn(StatusLevel.SUCCESS, alert_levels)
    
    def test_11_resolve_status(self):
        """Test status resolution"""
        # Add status item
        status_id = self.status_manager.add_status(
            "test_comp", "error", StatusLevel.ERROR, "Test error"
        )
        
        # Verify it's not resolved
        self.assertFalse(self.status_manager.status_items[status_id].resolved)
        
        # Resolve status
        success = self.status_manager.resolve_status(status_id, "Fixed the issue")
        self.assertTrue(success)
        
        # Verify resolution
        status_item = self.status_manager.status_items[status_id]
        self.assertTrue(status_item.resolved)
        self.assertIsNotNone(status_item.resolution_time)
        self.assertEqual(status_item.message, "Fixed the issue")
    
    def test_12_status_events(self):
        """Test status event emission"""
        # Add status to trigger event
        status_id = self.status_manager.add_status(
            "event_test", "online", StatusLevel.SUCCESS, "Event test"
        )
        
        # Verify event was created
        self.assertGreater(len(self.status_manager.status_events), 0)
        
        # Find the event
        events = list(self.status_manager.status_events.values())
        event = events[0]  # Should be the first event
        
        self.assertEqual(event.component_id, "event_test")
        self.assertEqual(event.event_type, StatusEventType.STATUS_CHANGE)
        self.assertEqual(event.new_status, "online")
        self.assertEqual(event.message, "Event test")
    
    def test_13_cleanup_old_items(self):
        """Test cleanup of old status items"""
        # Set small max history for testing
        self.status_manager.max_status_history = 3
        
        # Add more items than max
        for i in range(5):
            self.status_manager.add_status(
                f"comp{i}", "online", StatusLevel.SUCCESS, f"Component {i}"
            )
        
        # Verify cleanup occurred
        self.assertLessEqual(len(self.status_manager.status_items), 3)
    
    def test_14_abstract_methods(self):
        """Test abstract method implementations"""
        # Test health check
        health_result = self.status_manager._health_check()
        self.assertIsInstance(health_result, dict)
        self.assertIn("status", health_result)
        self.assertIn("health_checks", health_result)
        
        # Test get status
        status_result = self.status_manager._get_status()
        self.assertIsInstance(status_result, dict)
        self.assertIn("status", status_result)
        self.assertIn("summary", status_result)
        
        # Test get metrics
        metrics_result = self.status_manager._get_metrics()
        self.assertIsInstance(metrics_result, dict)
        self.assertIn("status_items_count", metrics_result)
        self.assertIn("events_count", metrics_result)
    
    def test_15_command_processing(self):
        """Test command processing"""
        # Test add_status command
        result = self.status_manager._process_command("add_status", {
            "component": "cmd_test",
            "status": "online",
            "level": "success",
            "message": "Command test"
        })
        
        self.assertEqual(result["result"], "success")
        self.assertIn("status_id", result)
        
        # Test get_status command
        result = self.status_manager._process_command("get_status", {
            "component": "cmd_test"
        })
        
        self.assertEqual(result["result"], "success")
        self.assertIn("status", result)
        
        # Test unknown command
        result = self.status_manager._process_command("unknown", {})
        self.assertEqual(result["result"], "error")
    
    def test_16_event_handling(self):
        """Test event handling"""
        # Handle status update event
        self.status_manager._handle_event("status_update", {
            "component": "event_comp",
            "status": "online",
            "level": "success",
            "message": "Event test"
        })
        
        # Verify status was added
        status = self.status_manager.get_status("event_comp")
        self.assertIsNotNone(status)
        self.assertEqual(status.status, "online")
    
    def test_17_config_validation(self):
        """Test configuration validation"""
        # Valid config
        valid_config = {
            "health_check_interval": 30,
            "max_status_history": 100,
            "auto_resolve_timeout": 3600
        }
        
        is_valid = self.status_manager._validate_config(valid_config)
        self.assertTrue(is_valid)
        
        # Invalid config (missing keys)
        invalid_config = {"health_check_interval": 30}
        is_valid = self.status_manager._validate_config(invalid_config)
        self.assertFalse(is_valid)
    
    def test_18_state_management(self):
        """Test state backup and restore"""
        # Add some status items
        self.status_manager.add_status("backup_test", "online", StatusLevel.SUCCESS, "Backup test")
        
        # Backup state
        backup = self.status_manager._backup_state()
        self.assertIsInstance(backup, dict)
        self.assertIn("status_items", backup)
        
        # Clear current state
        self.status_manager._reset_state()
        self.assertEqual(len(self.status_manager.status_items), 0)
        
        # Restore state
        self.status_manager._restore_state(backup)
        self.assertGreater(len(self.status_manager.status_items), 0)
    
    def test_19_smoke_test(self):
        """Test smoke test function"""
        # Import and run smoke test
        from src.core.managers.status_manager import run_smoke_test
        success = run_smoke_test()
        self.assertTrue(success)
    
    def test_20_integration_compatibility(self):
        """Test integration with existing systems"""
        # Test that StatusManager can be imported from core.status
        from src.core.status import StatusManager as ImportedStatusManager
        self.assertEqual(ImportedStatusManager, StatusManager)
        
        # Test that all expected types are available
        from src.core.status import (
            StatusLevel, HealthStatus, UpdateFrequency, StatusEventType,
            StatusItem, HealthMetric, ComponentHealth, StatusEvent,
            StatusMetrics, ActivitySummary
        )
        
        self.assertIsNotNone(StatusLevel)
        self.assertIsNotNone(HealthStatus)
        self.assertIsNotNone(UpdateFrequency)
        self.assertIsNotNone(StatusEventType)


if __name__ == "__main__":
    unittest.main(verbosity=2)
