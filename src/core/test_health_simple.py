#!/usr/bin/env python3
"""
Simple Health System Test - Quick validation of Unified Health System

Quick test to verify the health system is working correctly.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from core.managers.health_manager import HealthManager
    
    print("✅ Import successful")
    
    # Initialize health manager
    health_manager = HealthManager()
    print("✅ Health Manager initialized successfully")
    
    # Check default thresholds
    print(f"✅ Default thresholds: {len(health_system.thresholds)}")
    
    # Get system status
    status = health_system.get_system_health()
    print(f"✅ System status: {status['system_status']}")
    
    # Test component registration
    test_component = "test_health_component"
    if health_system.register_component(test_component, ComponentType.AGENT):
        print(f"✅ Component registered: {test_component}")
        
        # Test metric recording
        if health_system.record_metric(test_component, "cpu_usage", 75.0, "%"):
            print("✅ Metric recorded successfully")
            
            # Get component health
            snapshot = health_system.get_component_health(test_component)
            if snapshot:
                print(f"✅ Component health score: {snapshot.health_score}")
            else:
                print("❌ Failed to get component health")
        else:
            print("❌ Failed to record metric")
        
        # Cleanup
        health_system.unregister_component(test_component)
        print(f"✅ Component unregistered: {test_component}")
    else:
        print("❌ Failed to register component")
    
    # Export health report
    report = health_system.export_health_report()
    if report:
        print("✅ Health report exported successfully")
    else:
        print("❌ Failed to export health report")
    
    print("\n🎉 Unified Health System test completed successfully!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
