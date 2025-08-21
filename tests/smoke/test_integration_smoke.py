"""
Integration Infrastructure Smoke Test for Agent_Cellphone_V2_Repository
Quick verification that the integration system works correctly.
"""

import asyncio
import json
import time
import tempfile
import shutil
from pathlib import Path

# Import the components we're testing
from src.services.api_manager import APIManager, APIEndpoint, APIMethod
from src.services.middleware_orchestrator import MiddlewareOrchestrator, DataPacket
from src.services.service_registry import ServiceRegistry, ServiceInfo, ServiceType, ServiceMetadata, ServiceEndpoint
from src.services.integration_config_manager import IntegrationConfigManager, ConfigSource, ConfigScope
from src.services.integration_coordinator import IntegrationCoordinator


async def smoke_test_api_manager():
    """Smoke test for API Manager."""
    print("🧪 Testing API Manager...")
    
    api_manager = APIManager()
    
    # Test basic functionality
    assert api_manager.endpoints == []
    assert api_manager.middleware == []
    
    # Test adding endpoint
    async def test_handler(request, context):
        return {'status_code': 200, 'data': 'smoke_test'}
    
    endpoint = APIEndpoint(
        path="/smoke",
        method=APIMethod.GET,
        handler=test_handler,
        description="Smoke test endpoint"
    )
    
    api_manager.add_endpoint(endpoint)
    assert len(api_manager.endpoints) == 1
    
    # Test starting and stopping
    await api_manager.start()
    assert api_manager.running
    
    await api_manager.stop()
    assert not api_manager.running
    
    print("✅ API Manager smoke test passed")


async def smoke_test_middleware_orchestrator():
    """Smoke test for Middleware Orchestrator."""
    print("🧪 Testing Middleware Orchestrator...")
    
    orchestrator = MiddlewareOrchestrator()
    
    # Test basic functionality
    assert orchestrator.middleware_components == {}
    assert orchestrator.middleware_chains == []
    
    # Test starting and stopping
    await orchestrator.start()
    assert orchestrator.running
    
    await orchestrator.stop()
    assert not orchestrator.running
    
    print("✅ Middleware Orchestrator smoke test passed")


async def smoke_test_service_registry():
    """Smoke test for Service Registry."""
    print("🧪 Testing Service Registry...")
    
    registry = ServiceRegistry()
    
    # Test basic functionality
    assert registry.services == {}
    assert registry.service_names == {}
    
    # Test starting and stopping
    await registry.start()
    assert registry.running
    
    await registry.stop()
    assert not registry.running
    
    print("✅ Service Registry smoke test passed")


async def smoke_test_config_manager():
    """Smoke test for Configuration Manager."""
    print("🧪 Testing Configuration Manager...")
    
    # Create temporary config directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        config_manager = IntegrationConfigManager(temp_dir)
        
        # Test basic functionality
        assert config_manager.config_values != {}
        assert config_manager.validators != {}
        
        # Test setting and getting config
        config_manager.set_config_value(
            'smoke.test',
            'smoke_value',
            ConfigSource.FILE,
            ConfigScope.GLOBAL,
            'Smoke test config'
        )
        
        value = config_manager.get_config_value('smoke.test')
        assert value == 'smoke_value'
        
        # Test cleanup
        config_manager.cleanup()
        
    finally:
        # Cleanup temporary directory
        shutil.rmtree(temp_dir)
    
    print("✅ Configuration Manager smoke test passed")


async def smoke_test_integration_coordinator():
    """Smoke test for Integration Coordinator."""
    print("🧪 Testing Integration Coordinator...")
    
    # Create temporary config directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        coordinator = IntegrationCoordinator(temp_dir)
        
        # Test basic functionality
        assert coordinator.status.value == 'stopped'
        assert coordinator.config_manager is not None
        assert coordinator.api_manager is not None
        assert coordinator.middleware_orchestrator is not None
        assert coordinator.service_registry is not None
        
        # Test starting and stopping
        await coordinator.start()
        assert coordinator.status.value == 'running'
        
        # Test health check
        health = coordinator.get_system_health()
        assert 'status' in health
        assert 'components' in health
        
        # Test metrics
        metrics = coordinator.get_system_metrics()
        assert 'coordinator' in metrics
        assert 'api_manager' in metrics
        
        await coordinator.stop()
        assert coordinator.status.value == 'stopped'
        
    finally:
        # Cleanup temporary directory
        shutil.rmtree(temp_dir)
    
    print("✅ Integration Coordinator smoke test passed")


async def smoke_test_full_integration():
    """Smoke test for the complete integration system."""
    print("🧪 Testing Full Integration System...")
    
    # Create temporary config directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        coordinator = IntegrationCoordinator(temp_dir)
        
        # Start the complete system
        await coordinator.start()
        
        # Test API endpoints
        health_request = {
            'path': '/api/health',
            'method': 'GET',
            'headers': {},
            'client_id': 'smoke-test'
        }
        
        health_response = await coordinator.process_api_request(health_request)
        assert health_response['status_code'] == 200
        assert health_response['success'] == True
        
        # Test metrics endpoint
        metrics_request = {
            'path': '/api/metrics',
            'method': 'GET',
            'headers': {},
            'client_id': 'smoke-test'
        }
        
        metrics_response = await coordinator.process_api_request(metrics_request)
        assert metrics_response['status_code'] == 200
        assert metrics_response['success'] == True
        
        # Test configuration endpoint
        config_request = {
            'path': '/api/config',
            'method': 'GET',
            'headers': {},
            'client_id': 'smoke-test'
        }
        
        config_response = await coordinator.process_api_request(config_request)
        assert config_response['status_code'] == 200
        assert config_response['success'] == True
        
        # Test services endpoint
        services_request = {
            'path': '/api/services',
            'method': 'GET',
            'headers': {},
            'client_id': 'smoke-test'
        }
        
        services_response = await coordinator.process_api_request(services_request)
        assert services_response['status_code'] == 200
        assert services_response['success'] == True
        
        # Verify system health
        health = coordinator.get_system_health()
        assert health['healthy'] == True
        
        # Stop the system
        await coordinator.stop()
        
    finally:
        # Cleanup temporary directory
        shutil.rmtree(temp_dir)
    
    print("✅ Full Integration System smoke test passed")


async def run_all_smoke_tests():
    """Run all smoke tests."""
    print("🚀 Starting Integration Infrastructure Smoke Tests...")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Run individual component tests
        await smoke_test_api_manager()
        await smoke_test_middleware_orchestrator()
        await smoke_test_service_registry()
        await smoke_test_config_manager()
        await smoke_test_integration_coordinator()
        
        # Run full integration test
        await smoke_test_full_integration()
        
        # Calculate total time
        total_time = time.time() - start_time
        
        print("=" * 60)
        print(f"🎉 All smoke tests passed in {total_time:.2f} seconds!")
        print("✅ Integration Infrastructure is working correctly!")
        
        return True
        
    except Exception as e:
        print("=" * 60)
        print(f"❌ Smoke test failed: {str(e)}")
        print("🔍 Check the error details above")
        
        return False


def main():
    """Main function to run smoke tests."""
    try:
        success = asyncio.run(run_all_smoke_tests())
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️  Smoke tests interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error during smoke tests: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
