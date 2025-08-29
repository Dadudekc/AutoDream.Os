#!/usr/bin/env python3
"""
Simple test for workflow engine integration
"""

print("🚀 Starting simple test...")

try:
    # Test basic import
    print("Testing import...")
    from .workflow_engine_integration import FSMWorkflowIntegration
    print("✅ Import successful!")
    
    # Test instantiation
    print("Testing instantiation...")
    integration = FSMWorkflowIntegration()
    print("✅ Instantiation successful!")
    
    # Test basic method
    print("Testing health check...")
    health = integration.get_integration_health()
    print(f"✅ Health check successful: {health['overall_health']}")
    
    print("\n🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
