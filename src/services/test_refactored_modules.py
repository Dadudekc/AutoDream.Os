#!/usr/bin/env python3
"""
Test script for refactored V2 Message Delivery Service modules
Verifies that all components work together correctly
"""

import sys
import os
import time

# Add the services directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_coordinate_manager():
    """Test the coordinate manager module"""
    print("🧪 Testing Coordinate Manager...")
    
    try:
        from coordinate_manager import CoordinateManager
        
        cm = CoordinateManager()
        
        # Test basic functionality
        coords = cm.get_all_coordinates()
        print(f"✅ Loaded {len(coords)} agent coordinates")
        
        # Test getting specific agent
        agent_1 = cm.get_agent_coordinates("agent_1")
        if agent_1:
            print(f"✅ Agent 1 coordinates: ({agent_1['input_x']}, {agent_1['input_y']})")
        
        # Test coordinate update
        success = cm.update_agent_coordinates("agent_1", 999, 888)
        print(f"✅ Coordinate update: {'Success' if success else 'Failed'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Coordinate Manager test failed: {e}")
        return False

def test_delivery_status_tracker():
    """Test the delivery status tracker module"""
    print("🧪 Testing Delivery Status Tracker...")
    
    try:
        from delivery_status_tracker import DeliveryStatusTracker
        
        dst = DeliveryStatusTracker()
        
        # Test status initialization
        dst.initialize_agent_status("test_agent")
        
        # Test recording deliveries
        dst.record_successful_delivery("test_agent", "test_message")
        dst.record_failed_delivery("test_agent", "test_message")
        
        # Test getting status
        status = dst.get_agent_status("test_agent")
        if status:
            print(f"✅ Test agent status: {status['delivery_count']} deliveries")
        
        # Test statistics
        stats = dst.get_delivery_statistics()
        print(f"✅ Delivery statistics: {stats['total_deliveries']} total")
        
        return True
        
    except Exception as e:
        print(f"❌ Delivery Status Tracker test failed: {e}")
        return False

def test_message_delivery_core():
    """Test the message delivery core module"""
    print("🧪 Testing Message Delivery Core...")
    
    try:
        from message_delivery_core import MessageDeliveryCore
        
        mdc = MessageDeliveryCore()
        
        # Test delivery methods
        methods = mdc.get_delivery_methods()
        print(f"✅ Available delivery methods: {list(methods.keys())}")
        
        # Test PyAutoGUI availability
        pyautogui_available = mdc.is_pyautogui_available()
        print(f"✅ PyAutoGUI available: {pyautogui_available}")
        
        return True
        
    except Exception as e:
        print(f"❌ Message Delivery Core test failed: {e}")
        return False

def test_main_service():
    """Test the main service integration"""
    print("🧪 Testing Main Service Integration...")
    
    try:
        from v2_message_delivery_service import V2MessageDeliveryService
        
        service = V2MessageDeliveryService()
        
        # Test basic service functionality
        status = service.get_delivery_status()
        print(f"✅ Service status retrieved: {len(status['agent_coordinates'])} agents")
        
        # Test coordinate access
        coords = service.get_all_agent_coordinates()
        print(f"✅ Agent coordinates accessed: {len(coords)} agents")
        
        # Test statistics
        stats = service.get_delivery_statistics()
        print(f"✅ Service statistics: {stats['total_deliveries']} total deliveries")
        
        # Clean shutdown
        service.shutdown()
        
        return True
        
    except Exception as e:
        print(f"❌ Main Service test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Refactored V2 Message Delivery Service Modules")
    print("=" * 60)
    
    tests = [
        test_coordinate_manager,
        test_delivery_status_tracker,
        test_message_delivery_core,
        test_main_service,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Refactoring successful.")
        return 0
    else:
        print("⚠️ Some tests failed. Please review the issues.")
        return 1

if __name__ == "__main__":
    exit(main())

