"""
Tests for Messaging Memory Integration - Phase 3
================================================

Test suite for messaging_checks.py and integration with Phase 1.

Author: Agent-7 (Web Development Expert)
License: MIT
"""

import pytest
import time
from pathlib import Path

from src.observability.memory.integrations.messaging_checks import (
    FileResourceGuard,
    MessageSizeValidator,
    MessagingInstrumentation,
    CoordinationRequestPurger,
    MessagingMemoryIntegration,
)
from src.observability.memory.integrations.messaging_service_patches import (
    MessagingServiceMemoryPatch,
    patch_messaging_service,
)


class TestFileResourceGuard:
    """Test FileResourceGuard context manager"""
    
    def test_file_resource_guard_open_close(self, tmp_path):
        """Test file opens and closes correctly"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")
        
        with FileResourceGuard(str(test_file), 'r') as f:
            content = f.read()
            assert content == "Test content"
    
    def test_file_resource_guard_write(self, tmp_path):
        """Test file write operations"""
        test_file = tmp_path / "output.txt"
        
        with FileResourceGuard(str(test_file), 'w') as f:
            f.write("Hello World")
        
        assert test_file.read_text() == "Hello World"
    
    def test_file_resource_guard_cleanup_on_error(self, tmp_path):
        """Test file handle cleanup on error"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test")
        
        try:
            with FileResourceGuard(str(test_file), 'r') as f:
                raise ValueError("Test error")
        except ValueError:
            pass
        
        # File should be closed despite error
        assert not hasattr(f, 'closed') or f.closed


class TestMessageSizeValidator:
    """Test MessageSizeValidator"""
    
    def test_small_message_validation(self):
        """Test validation of small message"""
        validator = MessageSizeValidator(max_size_mb=1.0)
        result = validator.validate("Small message")
        
        assert result.is_valid is True
        assert result.message_size_bytes > 0
    
    def test_large_message_validation(self):
        """Test validation of large message"""
        validator = MessageSizeValidator(max_size_mb=0.001)  # 1KB limit
        large_message = "X" * 10000  # 10KB message
        
        result = validator.validate(large_message)
        
        assert result.is_valid is False
        assert "exceeds limit" in result.reason
    
    def test_validation_error_handling(self):
        """Test error handling in validation"""
        validator = MessageSizeValidator()
        # Non-string input should be handled gracefully
        result = validator.validate(123)
        
        assert result.is_valid is False


class TestMessagingInstrumentation:
    """Test MessagingInstrumentation"""
    
    def test_instrumentation_context_manager(self):
        """Test instrumentation context manager"""
        instrumentation = MessagingInstrumentation()
        
        with instrumentation.instrument_operation("test_op", 100):
            time.sleep(0.01)  # Simulate work
        
        assert len(instrumentation.metrics_history) == 1
        assert instrumentation.metrics_history[0].operation == "test_op"
    
    def test_metrics_summary(self):
        """Test metrics summary generation"""
        instrumentation = MessagingInstrumentation()
        
        for i in range(5):
            with instrumentation.instrument_operation(f"op_{i}", 100):
                pass
        
        summary = instrumentation.get_metrics_summary()
        
        assert summary['total_operations'] == 5
        assert 'avg_duration_ms' in summary


class TestCoordinationRequestPurger:
    """Test CoordinationRequestPurger"""
    
    def test_purge_old_requests_by_age(self):
        """Test purging by age"""
        purger = CoordinationRequestPurger(max_age_seconds=60, max_count=1000)
        
        current_time = time.time()
        requests = {
            'req1': {'timestamp': current_time - 120},  # 2 minutes old
            'req2': {'timestamp': current_time - 30},   # 30 seconds old
            'req3': {'timestamp': current_time},        # Current
        }
        
        result = purger.purge_old_requests(requests)
        
        assert result['purged_count'] == 1
        assert result['remaining_count'] == 2
    
    def test_purge_by_count(self):
        """Test purging by count limit"""
        purger = CoordinationRequestPurger(max_age_seconds=3600, max_count=5)
        
        current_time = time.time()
        requests = {
            f'req{i}': {'timestamp': current_time - i}
            for i in range(10)
        }
        
        result = purger.purge_old_requests(requests)
        
        assert result['remaining_count'] <= 5
        assert result['purged_count'] >= 5


class TestMessagingMemoryIntegration:
    """Test MessagingMemoryIntegration"""
    
    def test_validate_and_instrument(self):
        """Test combined validation and instrumentation"""
        integration = MessagingMemoryIntegration()
        
        result = integration.validate_and_instrument("Test message", "send")
        
        assert result.is_valid is True
    
    def test_system_status(self):
        """Test system status reporting"""
        integration = MessagingMemoryIntegration()
        
        status = integration.get_system_status()
        
        assert 'validator_limits' in status
        assert 'instrumentation_metrics' in status
        assert 'purger_config' in status
    
    def test_multiple_integration_instances(self):
        """Test creating multiple integration instances"""
        integration1 = MessagingMemoryIntegration()
        integration2 = MessagingMemoryIntegration()
        
        assert integration1 is not integration2


class TestMessagingServiceMemoryPatch:
    """Test MessagingServiceMemoryPatch"""
    
    def test_patch_initialization(self):
        """Test patch initialization"""
        # Create mock messaging service
        class MockMessagingService:
            def __init__(self):
                self.coordination_requests = {}
        
        mock_service = MockMessagingService()
        patch = MessagingServiceMemoryPatch(mock_service)
        
        assert patch.messaging_service is mock_service
        assert patch.validator is not None
    
    def test_message_validation_before_send(self):
        """Test message validation before send"""
        class MockMessagingService:
            coordination_requests = {}
        
        mock_service = MockMessagingService()
        patch = MessagingServiceMemoryPatch(mock_service)
        
        result = patch.validate_message_before_send("Test message")
        
        assert result['valid'] is True
        assert 'size_bytes' in result
    
    def test_coordination_request_purging(self):
        """Test coordination request purging"""
        class MockMessagingService:
            def __init__(self):
                current_time = time.time()
                self.coordination_requests = {
                    'old': {'timestamp': current_time - 7200},  # 2 hours old
                    'new': {'timestamp': current_time}
                }
        
        mock_service = MockMessagingService()
        patch = MessagingServiceMemoryPatch(mock_service)
        
        result = patch.purge_coordination_requests()
        
        assert result['purged_count'] >= 0
        assert 'remaining_count' in result


# Integration tests with Phase 1 (if available)
class TestPhase1Integration:
    """Test integration with Phase 1 detectors"""
    
    def test_integration_with_policy_manager(self):
        """Test integration with Phase 1 policy manager"""
        try:
            from src.observability.memory.policies import MemoryPolicyManager
            
            policy_manager = MemoryPolicyManager()
            integration = MessagingMemoryIntegration(policy_manager)
            
            assert integration.policy_manager is not None
        except ImportError:
            pytest.skip("Phase 1 not available")

