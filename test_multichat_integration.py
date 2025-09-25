#!/usr/bin/env python3
"""
Multichat Integration Test Script
================================

Simple test script for Agent-4 to test multichat workflow integration.
V2 compliant and ready to run.

Author: Agent-7 (Integration Specialist)
License: MIT
"""

import sys
import time
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_multichat_imports():
    """Test multichat component imports."""
    print("🧪 Testing multichat imports...")
    
    try:
        from src.services.messaging.multichat_response import multichat_respond
        from src.services.messaging.workflow_integration import MessagingWorkflowIntegration
        from src.services.messaging.agent_context import set_agent_context
        print("✅ All multichat imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_agent_context():
    """Test agent context functionality."""
    print("🧪 Testing agent context...")
    
    try:
        from src.services.messaging.agent_context import set_agent_context, get_current_agent
        
        # Set agent context
        set_agent_context("Agent-4")
        current_agent = get_current_agent()
        
        if current_agent == "Agent-4":
            print("✅ Agent context test successful")
            return True
        else:
            print(f"❌ Agent context mismatch: expected Agent-4, got {current_agent}")
            return False
            
    except Exception as e:
        print(f"❌ Agent context error: {e}")
        return False

def test_multichat_response():
    """Test multichat response functionality."""
    print("🧪 Testing multichat response...")
    
    try:
        from src.services.messaging.multichat_response import multichat_respond
        from src.services.messaging.agent_context import set_agent_context
        
        # Set agent context
        set_agent_context("Agent-4")
        
        # Test response
        success, result = multichat_respond(
            "Agent-7", 
            "Testing multichat workflow integration - Agent-4"
        )
        
        if success:
            print("✅ Multichat response test successful")
            print(f"   Result: {result}")
            return True
        else:
            print(f"❌ Multichat response failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Multichat response error: {e}")
        return False

def test_workflow_integration():
    """Test workflow integration."""
    print("🧪 Testing workflow integration...")
    
    try:
        from src.services.messaging.workflow_integration import MessagingWorkflowIntegration
        from src.services.messaging.agent_context import set_agent_context
        
        # Set agent context
        set_agent_context("Agent-4")
        
        # Initialize workflow integration
        workflow = MessagingWorkflowIntegration()
        
        # Test task coordination
        coordination = workflow.workflow_coordinate_task(
            task="Multichat workflow testing",
            required_agents=["Agent-7", "Agent-8"],
            coordination_message="Testing multichat workflow integration"
        )
        
        if 'error' not in coordination:
            print("✅ Workflow integration test successful")
            print(f"   Chat ID: {coordination.get('chat_id', 'N/A')}")
            return True
        else:
            print(f"❌ Workflow integration failed: {coordination['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow integration error: {e}")
        return False

def main():
    """Main test runner."""
    print("🚀 Multichat Integration Test Suite")
    print("=" * 40)
    print("Testing multichat workflow integration for Agent-4")
    print()
    
    tests = [
        test_multichat_imports,
        test_agent_context,
        test_multichat_response,
        test_workflow_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
            time.sleep(0.5)  # Brief pause between tests
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All multichat integration tests PASSED!")
        print("✅ Agent-4 can proceed with multichat workflow integration")
    else:
        print("⚠️ Some tests failed - check results above")
        print("❌ Agent-4 should troubleshoot before proceeding")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




