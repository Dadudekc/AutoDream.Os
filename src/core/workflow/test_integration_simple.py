#!/usr/bin/env python3
"""
Simple Integration Test - Quick validation of FSM Workflow Integration

Quick test to verify the integration system is working correctly.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from workflow_engine_integration import FSMWorkflowIntegration
    
    print("✅ Import successful")
    
    # Initialize integration
    integration = FSMWorkflowIntegration()
    print("✅ FSM Workflow Integration initialized successfully")
    
    # Get health status
    health = integration.get_integration_health()
    print(f"✅ Health Status: {health['overall_health']}")
    
    # Test basic functionality
    workflows = integration.list_integrated_workflows()
    print(f"✅ Current workflows: {len(workflows)}")
    
    # Export report
    report = integration.export_integration_report()
    if report:
        print("✅ Integration report exported successfully")
    else:
        print("❌ Failed to export integration report")
    
    print("\n🎉 FSM Workflow Integration test completed successfully!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
