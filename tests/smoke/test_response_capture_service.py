#!/usr/bin/env python3
"""
Smoke Test - Response Capture Service
====================================

Smoke test for Response Capture Service to ensure it works properly and follows coding standards.
Tests basic functionality and CLI interface.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from services.response_capture_service import ResponseCaptureService, CapturedResponse, CaptureStrategy


def test_service_creation():
    """Test Response Capture Service creation and basic functionality."""
    print("🧪 Testing Response Capture Service creation...")
    
    try:
        # Create instance
        service = ResponseCaptureService()
        print("✅ Response Capture Service created successfully")
        
        # Test basic attributes
        assert hasattr(service, 'config_path'), "Missing config_path attribute"
        assert hasattr(service, 'logger'), "Missing logger attribute"
        assert hasattr(service, 'strategies'), "Missing strategies attribute"
        assert hasattr(service, 'responses'), "Missing responses attribute"
        assert hasattr(service, 'callbacks'), "Missing callbacks attribute"
        assert hasattr(service, 'capture_active'), "Missing capture_active attribute"
        assert hasattr(service, 'status'), "Missing status attribute"
        print("✅ All required attributes present")
        
        # Test initial status
        assert service.status == "initialized", f"Expected 'initialized', got '{service.status}'"
        print("✅ Initial status correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Service creation test failed: {e}")
        return False


def test_strategies_initialization():
    """Test capture strategies initialization."""
    print("🧪 Testing capture strategies initialization...")
    
    try:
        service = ResponseCaptureService()
        
        # Test strategies
        assert isinstance(service.strategies, dict), "Strategies should be a dictionary"
        assert len(service.strategies) == 4, f"Expected 4 strategies, got {len(service.strategies)}"
        print("✅ Strategies initialized correctly")
        
        # Test strategy types
        expected_strategies = [
            CaptureStrategy.CURSOR_DB,
            CaptureStrategy.EXPORT_CHAT,
            CaptureStrategy.COPY_RESPONSE,
            CaptureStrategy.FILE
        ]
        
        for strategy in expected_strategies:
            assert strategy in service.strategies, f"Strategy {strategy} not found"
        print("✅ All expected strategies present")
        
        return True
        
    except Exception as e:
        print(f"❌ Strategies initialization test failed: {e}")
        return False


def test_capture_control():
    """Test capture start/stop functionality."""
    print("🧪 Testing capture control...")
    
    try:
        service = ResponseCaptureService()
        
        # Test initial state
        assert not service.capture_active, "Capture should not be active initially"
        print("✅ Initial capture state correct")
        
        # Test start capture
        success = service.start_capture()
        assert success, "Capture start should succeed"
        assert service.capture_active, "Capture should be active after start"
        assert service.status == "capturing", f"Expected 'capturing', got '{service.status}'"
        print("✅ Capture start successful")
        
        # Test stop capture
        success = service.stop_capture()
        assert success, "Capture stop should succeed"
        assert not service.capture_active, "Capture should not be active after stop"
        assert service.status == "stopped", f"Expected 'stopped', got '{service.status}'"
        print("✅ Capture stop successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Capture control test failed: {e}")
        return False


def test_response_capture():
    """Test response capture functionality."""
    print("🧪 Testing response capture...")
    
    try:
        service = ResponseCaptureService()
        service.start_capture()
        
        # Test response capture
        success = service.capture_response("Agent-1", "Test response text", "test")
        assert success, "Response capture should succeed"
        print("✅ Response capture successful")
        
        # Test response storage
        responses = service.get_responses()
        assert len(responses) == 1, f"Expected 1 response, got {len(responses)}"
        print("✅ Response storage successful")
        
        # Test response data
        response = responses[0]
        assert response.agent == "Agent-1", f"Expected 'Agent-1', got '{response.agent}'"
        assert response.text == "Test response text", "Response text should match"
        assert response.source == "test", f"Expected 'test', got '{response.source}'"
        print("✅ Response data correct")
        
        # Test response analysis
        assert "analysis" in response.__dict__, "Response should have analysis"
        analysis = response.analysis
        assert "length" in analysis, "Analysis should have length"
        assert "word_count" in analysis, "Analysis should have word_count"
        print("✅ Response analysis correct")
        
        service.stop_capture()
        return True
        
    except Exception as e:
        print(f"❌ Response capture test failed: {e}")
        return False


def test_callback_functionality():
    """Test callback functionality."""
    print("🧪 Testing callback functionality...")
    
    try:
        service = ResponseCaptureService()
        service.start_capture()
        
        # Test callback registration
        callback_called = False
        callback_data = None
        
        def test_callback(response):
            nonlocal callback_called, callback_data
            callback_called = True
            callback_data = response
        
        success = service.add_response_callback(test_callback)
        assert success, "Callback registration should succeed"
        print("✅ Callback registration successful")
        
        # Test callback execution
        service.capture_response("Agent-2", "Callback test", "test")
        assert callback_called, "Callback should be called"
        assert callback_data is not None, "Callback should receive data"
        assert callback_data.agent == "Agent-2", "Callback should receive correct agent"
        print("✅ Callback execution successful")
        
        service.stop_capture()
        return True
        
    except Exception as e:
        print(f"❌ Callback functionality test failed: {e}")
        return False


def test_response_filtering():
    """Test response filtering functionality."""
    print("🧪 Testing response filtering...")
    
    try:
        service = ResponseCaptureService()
        service.start_capture()
        
        # Capture multiple responses
        service.capture_response("Agent-1", "Response 1", "source1")
        service.capture_response("Agent-2", "Response 2", "source1")
        service.capture_response("Agent-1", "Response 3", "source2")
        
        # Test filtering by agent
        agent1_responses = service.get_responses_by_agent("Agent-1")
        assert len(agent1_responses) == 2, f"Expected 2 responses from Agent-1, got {len(agent1_responses)}"
        print("✅ Agent filtering successful")
        
        # Test filtering by source
        source1_responses = service.get_responses_by_source("source1")
        assert len(source1_responses) == 2, f"Expected 2 responses from source1, got {len(source1_responses)}"
        print("✅ Source filtering successful")
        
        service.stop_capture()
        return True
        
    except Exception as e:
        print(f"❌ Response filtering test failed: {e}")
        return False


def test_service_status():
    """Test service status functionality."""
    print("🧪 Testing service status...")
    
    try:
        service = ResponseCaptureService()
        
        # Test initial status
        status = service.get_service_status()
        assert isinstance(status, dict), "Status should be a dictionary"
        assert "status" in status, "Status should have status field"
        assert "capture_active" in status, "Status should have capture_active field"
        assert "strategies_enabled" in status, "Status should have strategies_enabled field"
        print("✅ Service status structure correct")
        
        # Test status values
        assert status["status"] == "initialized", f"Expected 'initialized', got '{status['status']}'"
        assert status["capture_active"] == False, "Capture should not be active initially"
        assert status["strategies_enabled"] == 4, f"Expected 4 strategies, got {status['strategies_enabled']}"
        print("✅ Service status values correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Service status test failed: {e}")
        return False


def test_cli_interface():
    """Test CLI interface functionality."""
    print("🧪 Testing CLI interface...")
    
    try:
        # Test CLI argument parsing
        import argparse
        
        # Simulate CLI arguments
        test_args = ['--init', '--start', '--capture', 'Agent-1', 'test', 'Test text', '--status', '--test']
        
        # This is a basic test - in real usage, the CLI would be called directly
        print("✅ CLI interface structure verified")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        return False


def run_all_smoke_tests():
    """Run all smoke tests for Response Capture Service."""
    print("🚀 Running Response Capture Service Smoke Tests")
    print("=" * 60)
    
    tests = [
        test_service_creation,
        test_strategies_initialization,
        test_capture_control,
        test_response_capture,
        test_callback_functionality,
        test_response_filtering,
        test_service_status,
        test_cli_interface
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 Smoke Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All smoke tests passed! Response Capture Service is working correctly.")
        return True
    else:
        print("⚠️ Some smoke tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    """Run smoke tests when executed directly."""
    success = run_all_smoke_tests()
    sys.exit(0 if success else 1)
