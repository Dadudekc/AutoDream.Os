#!/usr/bin/env python3
"""
Test Script for New Unified Testing Framework
============================================

Tests the newly created unified testing and messaging framework.
"""

import sys
import os
sys.path.append('src/services/testing')

def test_imports():
    """Test that all modules can be imported."""
    try:
        from core_framework import TestFramework, TestConfig, TestStatus
        from message_queue import UnifiedMessageQueue, MessagePriority
        from service_integration import ServiceIntegrationTester
        from performance_tester import PerformanceTester
        from execution_engine import TestExecutor
        from data_manager import TestDataManager
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_message_queue():
    """Test the message queue system."""
    try:
        from message_queue import UnifiedMessageQueue, MessagePriority, MessageType
        
        # Create message queue
        queue = UnifiedMessageQueue()
        
        # Test sending messages
        msg_id1 = queue.send_message("agent1", "agent2", "Hello", MessagePriority.NORMAL)
        msg_id2 = queue.send_message("agent1", "agent2", "Urgent", MessagePriority.HIGH)
        
        print(f"✅ Message queue test passed - Messages: {msg_id1}, {msg_id2}")
        return True
    except Exception as e:
        print(f"❌ Message queue test failed: {e}")
        return False

def test_core_framework():
    """Test the core testing framework."""
    try:
        from core_framework import TestConfig, TestStatus
        
        # Test configuration
        config = TestConfig(test_timeout=60.0, max_retries=2)
        
        # Test enums
        status = TestStatus.PASSED
        
        print(f"✅ Core framework test passed - Config: {config.test_timeout}s, Status: {status.value}")
        return True
    except Exception as e:
        print(f"❌ Core framework test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing New Unified Testing Framework")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Message Queue", test_message_queue),
        ("Core Framework", test_core_framework),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! New framework is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
