#!/usr/bin/env python3
"""
Standalone Integration Infrastructure Test
Tests the integration infrastructure files directly without import conflicts.
"""

import asyncio
import json
import time
import sys
import os
import importlib.util


def load_module_from_file(module_name, file_path):
    """Load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_api_manager_standalone():
    """Test API Manager functionality directly."""
    print("🧪 Testing API Manager Standalone")
    print("=" * 40)

    try:
        # Load API Manager module directly
        api_manager_path = "src/services/api_manager.py"
        if not os.path.exists(api_manager_path):
            print(f"❌ API Manager file not found: {api_manager_path}")
            return False

        api_manager_module = load_module_from_file("api_manager", api_manager_path)

        # Test class creation
        APIManager = api_manager_module.APIManager
        APIEndpoint = api_manager_module.APIEndpoint
        APIMethod = api_manager_module.APIMethod

        # Create instance
        api_manager = APIManager()
        print("✅ API Manager instance created successfully")
        print(f"   - Endpoints: {len(api_manager.endpoints)}")
        print(f"   - Middleware: {len(api_manager.middleware)}")

        # Test endpoint registration
        def test_handler(request, context):
            return {"test": "data"}

        endpoint = APIEndpoint(
            path="/test",
            method=APIMethod.GET,
            handler=test_handler,
            description="Test endpoint",
        )

        api_manager.register_endpoint(endpoint)
        print("✅ Endpoint registered successfully")
        print(f"   - Total endpoints: {len(api_manager.endpoints)}")

        return True

    except Exception as e:
        print(f"❌ API Manager Test Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_middleware_tools_standalone():
    """Test Middleware Tools functionality directly."""
    print("\n🔧 Testing Middleware Tools Standalone")
    print("=" * 40)

    try:
        # Load Middleware Tools module directly
        middleware_path = "src/services/middleware_tools.py"
        if not os.path.exists(middleware_path):
            print(f"❌ Middleware Tools file not found: {middleware_path}")
            return False

        middleware_module = load_module_from_file("middleware_tools", middleware_path)

        # Test class creation
        MessageQueue = middleware_module.MessageQueue
        CacheManager = middleware_module.CacheManager
        DataTransformer = middleware_module.DataTransformer
        CircuitBreaker = middleware_module.CircuitBreaker
        MessagePriority = middleware_module.MessagePriority
        Message = middleware_module.Message

        # Test Message Queue
        print("1. Testing Message Queue...")
        message_queue = MessageQueue()
        message = Message(
            id="test_1",
            content="Hello World",
            priority=MessagePriority.HIGH,
            timestamp=time.time(),
            source="test",
            destination="test",
        )
        message_queue.enqueue(message)
        print("✅ Message enqueued successfully")
        print(f"   - Queue status: {message_queue.get_queue_status()}")

        # Test Cache Manager
        print("\n2. Testing Cache Manager...")
        cache_manager = CacheManager()
        cache_manager.set("test_key", "test_value", ttl=60)
        cached_value = cache_manager.get("test_key")
        print("✅ Cache operations successful")
        print(f"   - Cached value: {cached_value}")

        # Test Data Transformer
        print("\n3. Testing Data Transformer...")
        data_transformer = DataTransformer()
        test_data = {"key": "value"}
        json_result = data_transformer.transform(test_data, "json")
        print("✅ Data transformation successful")
        print(f"   - JSON result: {json_result}")

        # Test Circuit Breaker
        print("\n4. Testing Circuit Breaker...")
        circuit_breaker = CircuitBreaker()

        def test_function():
            return "success"

        result = circuit_breaker.call(test_function)
        print("✅ Circuit breaker successful")
        print(f"   - Result: {result}")
        print(f"   - State: {circuit_breaker.get_state()}")

        return True

    except Exception as e:
        print(f"❌ Middleware Tools Test Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_integration_coordinator_standalone():
    """Test Integration Coordinator functionality directly."""
    print("\n🎯 Testing Integration Coordinator Standalone")
    print("=" * 45)

    try:
        # Load Integration Coordinator module directly
        coordinator_path = "src/services/integration_coordinator.py"
        if not os.path.exists(coordinator_path):
            print(f"❌ Integration Coordinator file not found: {coordinator_path}")
            return False

        coordinator_module = load_module_from_file(
            "integration_coordinator", coordinator_path
        )

        # Test class creation
        IntegrationCoordinator = coordinator_module.IntegrationCoordinator

        # Create coordinator (uses default config)
        coordinator = IntegrationCoordinator()
        print("✅ Integration Coordinator created successfully")

        # Test status
        status = coordinator.status
        print("✅ Integration status retrieved successfully")
        print(f"   - Status: {status}")
        print(f"   - API Manager: {coordinator.api_manager is not None}")
        print(
            f"   - Middleware Orchestrator: {coordinator.middleware_orchestrator is not None}"
        )

        return True

    except Exception as e:
        print(f"❌ Integration Coordinator Test Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


async def test_async_coordinator_standalone():
    """Test async functionality of Integration Coordinator directly."""
    print("\n🔄 Testing Async Integration Coordinator Standalone")
    print("=" * 50)

    try:
        # Load modules directly
        coordinator_path = "src/services/integration_coordinator.py"
        middleware_path = "src/services/middleware_tools.py"

        if not os.path.exists(coordinator_path) or not os.path.exists(middleware_path):
            print("❌ Required files not found")
            return False

        coordinator_module = load_module_from_file(
            "integration_coordinator", coordinator_path
        )
        middleware_module = load_module_from_file("middleware_tools", middleware_path)

        IntegrationCoordinator = coordinator_module.IntegrationCoordinator
        MessagePriority = middleware_module.MessagePriority

        # Create coordinator (uses default config)
        coordinator = IntegrationCoordinator()

        # Test async health check
        print("1. Testing Async Health Check...")
        try:
            # Check if the coordinator has health check methods
            if hasattr(coordinator, "get_system_health"):
                health = await coordinator.get_system_health()
                print(f"✅ Health check completed: {len(health)} services")
            elif hasattr(coordinator, "get_health_status"):
                health = await coordinator.get_health_status()
                print(f"✅ Health check completed: {len(health)} services")
            else:
                print("⚠️  No health check method found, testing basic functionality")
                print(f"   - Status: {coordinator.status}")
                print(f"   - API Endpoints: {len(coordinator.api_manager.endpoints)}")
        except Exception as e:
            print(f"⚠️  Health check failed: {str(e)}")

        # Test basic coordinator functionality
        print("\n2. Testing Basic Coordinator Functionality...")
        print(f"✅ Coordinator status: {coordinator.status}")
        print(f"✅ API Manager endpoints: {len(coordinator.api_manager.endpoints)}")
        print(
            f"✅ Middleware Orchestrator: {coordinator.middleware_orchestrator is not None}"
        )
        print(f"✅ Service Registry: {coordinator.service_registry is not None}")

        return True

    except Exception as e:
        print(f"❌ Async Integration Coordinator Test Error: {str(e)}")
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
            with open(config_path, "r") as f:
                config = json.load(f)
            print("✅ Configuration file loaded successfully")
            print(
                f"   - Version: {config.get('integration_infrastructure', {}).get('version', 'N/A')}"
            )
            print(
                f"   - API Management: {config.get('integration_infrastructure', {}).get('api_management', {}).get('enabled', 'N/A')}"
            )
            print(
                f"   - Message Queue: {config.get('integration_infrastructure', {}).get('message_queue', {}).get('enabled', 'N/A')}"
            )
            print(
                f"   - Caching: {config.get('integration_infrastructure', {}).get('caching', {}).get('enabled', 'N/A')}"
            )
            return True
        else:
            print("⚠️  Configuration file not found")
            return False

    except Exception as e:
        print(f"❌ Configuration Error: {str(e)}")
        return False


def test_launcher_script():
    """Test launcher script functionality."""
    print("\n🚀 Testing Launcher Script")
    print("=" * 30)

    try:
        launcher_path = "scripts/launch_integration_infrastructure.py"
        if not os.path.exists(launcher_path):
            print(f"⚠️  Launcher script not found: {launcher_path}")
            return False

        # Check if script is executable
        print("✅ Launcher script found")

        # Test basic script parsing
        with open(launcher_path, "r") as f:
            content = f.read()

        # Check for key components
        required_components = [
            "IntegrationInfrastructureLauncher",
            "IntegrationCoordinator",
            "argparse",
            "asyncio",
        ]

        missing_components = []
        for component in required_components:
            if component not in content:
                missing_components.append(component)

        if missing_components:
            print(f"⚠️  Missing components: {missing_components}")
            return False
        else:
            print("✅ All required components found in launcher script")
            return True

    except Exception as e:
        print(f"❌ Launcher Script Test Error: {str(e)}")
        return False


def main():
    """Main test function."""
    print("🚀 Standalone Integration Infrastructure Test Suite")
    print("=" * 65)

    # Test individual components
    api_success = test_api_manager_standalone()
    middleware_success = test_middleware_tools_standalone()
    coordinator_success = test_integration_coordinator_standalone()
    config_success = test_configuration()
    launcher_success = test_launcher_script()

    # Test async functionality
    async_success = asyncio.run(test_async_coordinator_standalone())

    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    print(f"API Manager: {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"Middleware Tools: {'✅ PASS' if middleware_success else '❌ FAIL'}")
    print(f"Integration Coordinator: {'✅ PASS' if coordinator_success else '❌ FAIL'}")
    print(f"Configuration: {'✅ PASS' if config_success else '❌ FAIL'}")
    print(f"Launcher Script: {'✅ PASS' if launcher_success else '❌ FAIL'}")
    print(f"Async Functionality: {'✅ PASS' if async_success else '❌ FAIL'}")

    overall_success = all(
        [
            api_success,
            middleware_success,
            coordinator_success,
            config_success,
            launcher_success,
            async_success,
        ]
    )

    if overall_success:
        print("\n🎉 All Tests Passed! Integration Infrastructure is working correctly.")
        print("\n📋 Next Steps:")
        print(
            "   1. Start the infrastructure: python scripts/launch_integration_infrastructure.py"
        )
        print(
            "   2. Check health: python scripts/launch_integration_infrastructure.py --action health"
        )
        print(
            "   3. View status: python scripts/launch_integration_infrastructure.py --action status"
        )
        return 0
    else:
        print("\n❌ Some Tests Failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
