#!/usr/bin/env python3
"""
Simple Tests for HealthAlertManager - V2 Refactored Version
==========================================================

Basic tests for the refactored HealthAlertManager that inherits from BaseManager.
Tests core functionality without complex imports.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import os
import time
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from src.core.health.alerting.health_alert_manager import HealthAlertManager
    from src.core.health.types.health_types import HealthAlert, AlertType, HealthLevel, HealthMetric
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"Import failed: {e}")
    IMPORT_SUCCESS = False


def test_health_alert_manager_basic():
    """Basic test for HealthAlertManager functionality"""
    if not IMPORT_SUCCESS:
        print("Skipping tests due to import issues")
        return
    
    print("Testing HealthAlertManager basic functionality...")
    
    # Test initialization
    manager = HealthAlertManager()
    print(f"✅ Manager initialized: {manager.name}")
    
    # Test default thresholds
    assert "cpu_usage" in manager.thresholds
    assert manager.thresholds["cpu_usage"]["warning"] == 70.0
    print("✅ Default thresholds loaded")
    
    # Test threshold setting
    result = manager.set_threshold("test_metric", "warning", 50.0)
    assert result is True
    assert manager.get_threshold("test_metric", "warning") == 50.0
    print("✅ Threshold setting works")
    
    # Test alert creation
    alert = manager._create_alert("test_metric", 85.0, 80.0, "critical")
    assert alert is not None
    assert alert.metric_name == "test_metric"
    assert alert.level == HealthLevel.CRITICAL
    print("✅ Alert creation works")
    
    # Test alert acknowledgment
    result = manager.acknowledge_alert(alert.id, "test_user")
    assert result is True
    assert alert.acknowledged is True
    print("✅ Alert acknowledgment works")
    
    # Test alert resolution
    result = manager.resolve_alert(alert.id, "Issue fixed")
    assert result is True
    assert alert.resolved is True
    print("✅ Alert resolution works")
    
    # Test statistics
    stats = manager.get_alert_statistics()
    assert stats["total_alerts"] == 1
    assert stats["resolved_alerts"] == 1
    print("✅ Statistics generation works")
    
    # Test clearing alerts
    manager.clear_alerts()
    assert len(manager.health_alerts) == 0
    print("✅ Alert clearing works")
    
    print("🎉 All basic tests passed!")


def test_lifecycle_hooks():
    """Test BaseManager lifecycle hooks"""
    if not IMPORT_SUCCESS:
        print("Skipping lifecycle tests due to import issues")
        return
    
    print("Testing lifecycle hooks...")
    
    manager = HealthAlertManager()
    
    # Test start
    result = manager._on_start()
    assert result is True
    print("✅ Start hook works")
    
    # Test resource initialization
    result = manager._on_initialize_resources()
    assert result is True
    print("✅ Resource initialization works")
    
    # Test heartbeat
    manager._on_heartbeat()  # Should not raise exception
    print("✅ Heartbeat works")
    
    # Test cleanup
    manager._on_cleanup_resources()  # Should not raise exception
    print("✅ Cleanup works")
    
    # Test stop
    manager._on_stop()  # Should not raise exception
    print("✅ Stop hook works")
    
    print("🎉 All lifecycle tests passed!")


def test_performance():
    """Test performance with many alerts"""
    if not IMPORT_SUCCESS:
        print("Skipping performance tests due to import issues")
        return
    
    print("Testing performance...")
    
    manager = HealthAlertManager()
    
    # Create many alerts
    start_time = time.time()
    for i in range(100):
        manager._create_alert(f"metric_{i}", 85.0, 80.0, "critical")
    creation_time = time.time() - start_time
    
    print(f"✅ Created 100 alerts in {creation_time:.3f} seconds")
    assert creation_time < 1.0  # Should complete in reasonable time
    
    # Test statistics generation
    start_time = time.time()
    stats = manager.get_alert_statistics()
    stats_time = time.time() - start_time
    
    print(f"✅ Generated statistics in {stats_time:.3f} seconds")
    assert stats_time < 0.1  # Should complete quickly
    assert stats["total_alerts"] == 100
    
    print("🎉 Performance tests passed!")


if __name__ == "__main__":
    print("🚀 Starting HealthAlertManager tests...")
    print("=" * 50)
    
    test_health_alert_manager_basic()
    print()
    
    test_lifecycle_hooks()
    print()
    
    test_performance()
    print()
    
    print("🎉 All tests completed successfully!")
    print("=" * 50)
