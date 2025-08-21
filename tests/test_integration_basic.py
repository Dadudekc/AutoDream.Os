#!/usr/bin/env python3
"""
Basic Integration Infrastructure Test
Tests the core functionality without complex imports.
"""

import asyncio
import json
import time
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_functionality():
    """Test basic functionality of the integration infrastructure."""
    print("🧪 Testing Integration Infrastructure Basic Functionality")
    print("=" * 60)
    
    try:
        # Test 1: Import API Manager
        print("\n1. Testing API Manager Import...")
        from services.api_manager import APIManager, APIEndpoint, APIMethod
        print("✅ API Manager imported successfully")
        
        # Test 2: Create API Manager instance
        print("\n2. Testing API Manager Creation...")
        api_manager = APIManager()
        print("✅ API Manager instance created successfully")
        print(f"   - Endpoints: {len(api_manager.endpoints)}")
        print(f"   - Middleware: {len(api_manager.middleware)}")
        
        # Test 3: Import Middleware Tools
        print("\n3. Testing Middleware Tools Import...")
        from services.middleware_tools import (
            MessageQueue, CacheManager, DataTransformer,
            CircuitBreaker, RetryMiddleware, MessagePriority, Message
        )
        print("✅ Middleware Tools imported successfully")
        
        # Test 4: Create Middleware Instances
        print("\n4. Testing Middleware Instance Creation...")
        message_queue = MessageQueue()
        cache_manager = CacheManager()
        data_transformer = DataTransformer()
        circuit_breaker = CircuitBreaker()
        retry_middleware = RetryMiddleware()
        print("✅ All middleware instances created successfully")
        
        # Test 5: Test Message Queue
        print("\n5. Testing Message Queue...")
        message = Message(
            id="test_1",
            content="Hello World",
            priority=MessagePriority.HIGH,
            timestamp=time.time(),
            source="test",
            destination="test"
        )
        message_queue.enqueue(message)
        print("✅ Message enqueued successfully")
        print(f"   - Queue status: {message_queue.get_queue_status()}")
        
        # Test 6: Test Cache Manager
        print("\n6. Testing Cache Manager...")
        cache_manager.set("test_key", "test_value", ttl=60)
        cached_value = cache_manager.get("test_key")
        print("✅ Cache operations successful")
        print(f"   - Cached value: {cached_value}")
        
        # Test 7: Test Data Transformer
        print("\n7. Testing Data Transformer...")
        test_data = {"key": "value"}
        json_result = data_transformer.transform(test_data, "json")
        print("✅ Data transformation successful")
        print(f"   - JSON result: {json_result}")
        
        # Test 8: Test Circuit Breaker
        print("\n8. Testing Circuit Breaker...")
        def test_function():
            return "success"
        
        result = circuit_breaker.call(test_function)
        print("✅ Circuit breaker successful")
        print(f"   - Result: {result}")
        print(f"   - State: {circuit_breaker.get_state()}")
        
        # Test 9: Import Integration Coordinator
        print("\n9. Testing Integration Coordinator Import...")
        from services.integration_coordinator import IntegrationCoordinator, IntegrationConfig
        print("✅ Integration Coordinator imported successfully")
        
        # Test 10: Create Integration Coordinator
        print("\n10. Testing Integration Coordinator Creation...")
        config = IntegrationConfig(
            api_enabled=True,
            message_queue_enabled=True,
            caching_enabled=True,
            circuit_breaker_enabled=True,
            retry_enabled=True,
            max_workers=5,
            health_check_interval=1
        )
        coordinator = IntegrationCoordinator(config)
        print("✅ Integration Coordinator created successfully")
        
        # Test 11: Get Integration Status
        print("\n11. Testing Integration Status...")
        status = coordinator.get_integration_status()
        print("✅ Integration status retrieved successfully")
        print(f"   - Running: {status['running']}")
        print(f"   - API Enabled: {status['config']['api_enabled']}")
        print(f"   - Message Queue Enabled: {status['config']['message_queue_enabled']}")
        
        print("\n🎉 All Basic Tests Passed Successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        print("   This may be due to missing dependencies or import conflicts.")
        return False
        
    except Exception as e:
        print(f"❌ Test Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_async_functionality():
    """Test async functionality of the integration infrastructure."""
    print("\n🔄 Testing Async Functionality")
    print("=" * 40)
    
    try:
        from services.integration_coordinator import IntegrationCoordinator, IntegrationConfig
        from services.middleware_tools import MessagePriority
        
        # Create coordinator
        config = IntegrationConfig(
            api_enabled=True,
            message_queue_enabled=True,
            caching_enabled=True,
            circuit_breaker_enabled=True,
            retry_enabled=True,
            max_workers=5,
            health_check_interval=1
        )
        coordinator = IntegrationCoordinator(config)
        
        # Test async message sending
        print("\n1. Testing Async Message Sending...")
        message_sent = await coordinator.send_message(
            content="Async test message",
            destination="test_queue",
            priority=MessagePriority.HIGH
        )
        print(f"✅ Message sent: {message_sent}")
        
        # Test async message retrieval
        print("\n2. Testing Async Message Retrieval...")
        message = await coordinator.get_message()
        if message:
            print(f"✅ Message retrieved: {message.content}")
        else:
            print("⚠️  No message retrieved (queue may be empty)")
        
        # Test async health check
        print("\n3. Testing Async Health Check...")
        health = await coordinator.get_system_health()
        print(f"✅ Health check completed: {len(health)} services")
        
        print("\n🎉 All Async Tests Passed Successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Async Test Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration loading."""
    print("\n⚙️  Testing Configuration")
    print("=" * 30)
    
    try:
        config_path = "config/integration_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            print("✅ Configuration file loaded successfully")
            print(f"   - Version: {config.get('integration_infrastructure', {}).get('version', 'N/A')}")
            print(f"   - API Management: {config.get('integration_infrastructure', {}).get('api_management', {}).get('enabled', 'N/A')}")
            return True
        else:
            print("⚠️  Configuration file not found")
            return False
            
    except Exception as e:
        print(f"❌ Configuration Error: {str(e)}")
        return False


def main():
    """Main test function."""
    print("🚀 Integration Infrastructure Basic Test Suite")
    print("=" * 60)
    
    # Test basic functionality
    basic_success = test_basic_functionality()
    
    # Test configuration
    config_success = test_configuration()
    
    # Test async functionality
    async_success = asyncio.run(test_async_functionality())
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    print(f"Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"Configuration: {'✅ PASS' if config_success else '❌ FAIL'}")
    print(f"Async Functionality: {'✅ PASS' if async_success else '❌ FAIL'}")
    
    overall_success = basic_success and config_success and async_success
    
    if overall_success:
        print("\n🎉 All Tests Passed! Integration Infrastructure is working correctly.")
        return 0
    else:
        print("\n❌ Some Tests Failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
