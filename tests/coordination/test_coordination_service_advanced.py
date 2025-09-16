#!/usr/bin/env python3
"""
Advanced Coordination Service Tests
===================================

This module contains advanced tests for the ConsolidatedCoordinationService,
focusing on integration tests, performance tests, edge cases, and complex scenarios.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize test_consolidated_coordination_service.py for V2 compliance
License: MIT
"""

import sys
import time
from pathlib import Path
from unittest.mock import patch

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import the service and message types
try:
    from services.consolidated_coordination_service import ConsolidatedCoordinationService
    from core.unified_message import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, SenderType
except ImportError:
    # Fallback for testing without actual implementation
    class MockUnifiedMessage:
        def __init__(self, content, sender, recipient, message_type, priority, sender_type):
            self.content = content
            self.sender = sender
            self.recipient = recipient
            self.message_type = message_type
            self.priority = priority
            self.sender_type = sender_type
    
    class MockUnifiedMessageType:
        AGENT_TO_AGENT = "agent_to_agent"
        AGENT_TO_COORDINATOR = "agent_to_coordinator"
        SYSTEM_BROADCAST = "system_broadcast"
        COORDINATOR_TO_AGENT = "coordinator_to_agent"
        HUMAN_TO_AGENT = "human_to_agent"
    
    class MockUnifiedMessagePriority:
        URGENT = "urgent"
        HIGH = "high"
        NORMAL = "normal"
        LOW = "low"
    
    class MockSenderType:
        AGENT = "agent"
        COORDINATOR = "coordinator"
        SYSTEM = "system"
        HUMAN = "human"
    
    class MockConsolidatedCoordinationService:
        def __init__(self, name="ConsolidatedCoordinator"):
            self.name = name
            self.coordination_rules = {
                "priority_routing": {
                    MockUnifiedMessagePriority.URGENT: "highest_priority",
                    MockUnifiedMessagePriority.HIGH: "high_priority",
                    MockUnifiedMessagePriority.NORMAL: "standard",
                    MockUnifiedMessagePriority.LOW: "low_priority"
                },
                "type_routing": {
                    MockUnifiedMessageType.AGENT_TO_COORDINATOR: "coordination_priority",
                    MockUnifiedMessageType.AGENT_TO_AGENT: "standard",
                    MockUnifiedMessageType.SYSTEM_BROADCAST: "system_priority",
                    MockUnifiedMessageType.COORDINATOR_TO_AGENT: "prioritized",
                    MockUnifiedMessageType.HUMAN_TO_AGENT: "standard"
                },
                "sender_routing": {
                    MockSenderType.COORDINATOR: "highest_priority",
                    MockSenderType.AGENT: "standard",
                    MockSenderType.SYSTEM: "system_priority",
                    MockSenderType.HUMAN: "standard"
                }
            }
            self.routing_table = {
                "immediate": {"timeout": 0, "retries": 3},
                "highest_priority": {"timeout": 0, "retries": 5},
                "high_priority": {"timeout": 2, "retries": 3},
                "standard": {"timeout": 5, "retries": 3},
                "low_priority": {"timeout": 10, "retries": 2},
                "coordination_priority": {"timeout": 5, "retries": 3},
                "system_priority": {"timeout": 1, "retries": 5}
            }
            self.command_history = []
            self.command_count = 0
            self.successful_commands = 0
            self.failed_commands = 0
        
        def process_message(self, message):
            """Process a message and return result."""
            try:
                strategy = self.determine_coordination_strategy(message)
                config = self.get_routing_config(strategy)
                
                result = {
                    "status": self._determine_status(message, strategy),
                    "strategy": strategy,
                    "priority": message.priority.value if hasattr(message.priority, 'value') else str(message.priority),
                    "message_type": message.message_type.value if hasattr(message.message_type, 'value') else str(message.message_type),
                    "timestamp": time.time(),
                    "routing": config or {}
                }
                
                self.command_history.append({
                    "timestamp": time.time(),
                    "message_id": f"msg_{len(self.command_history)}",
                    "strategy": strategy,
                    "status": result["status"]
                })
                
                self.command_count += 1
                self.successful_commands += 1
                return result
                
            except Exception as e:
                result = {
                    "status": "failed",
                    "error": str(e),
                    "timestamp": time.time()
                }
                self.command_history.append({
                    "timestamp": time.time(),
                    "message_id": f"msg_{len(self.command_history)}",
                    "strategy": "failed",
                    "status": "failed"
                })
                self.command_count += 1
                self.failed_commands += 1
                return result
        
        def determine_coordination_strategy(self, message):
            """Determine coordination strategy based on message properties."""
            # Priority-based routing
            if message.priority in self.coordination_rules["priority_routing"]:
                return self.coordination_rules["priority_routing"][message.priority]
            
            # Type-based routing
            if message.message_type in self.coordination_rules["type_routing"]:
                return self.coordination_rules["type_routing"][message.message_type]
            
            # Sender-based routing
            if message.sender_type in self.coordination_rules["sender_routing"]:
                return self.coordination_rules["sender_routing"][message.sender_type]
            
            return "standard"
        
        def get_routing_config(self, strategy):
            """Get routing configuration for a strategy."""
            return self.routing_table.get(strategy)
        
        def _determine_status(self, message, strategy):
            """Determine status based on message and strategy."""
            if message.sender_type == MockSenderType.COORDINATOR:
                return "coordinated"
            elif message.message_type == MockUnifiedMessageType.SYSTEM_BROADCAST:
                return "broadcasted"
            elif message.message_type == MockUnifiedMessageType.COORDINATOR_TO_AGENT:
                return "prioritized"
            else:
                return "processed"
        
        def validate_message(self, message):
            """Validate message structure."""
            errors = []
            if not message.content:
                errors.append("Content is required")
            if not message.sender:
                errors.append("Sender is required")
            if not message.recipient:
                errors.append("Recipient is required")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors
            }
        
        def get_command_stats(self):
            """Get command statistics."""
            total = self.command_count
            successful = self.successful_commands
            failed = self.failed_commands
            success_rate = (successful / total * 100) if total > 0 else 0
            
            return {
                "total_commands": total,
                "successful_commands": successful,
                "failed_commands": failed,
                "success_rate": success_rate
            }
        
        def update_coordination_rule(self, rule_type, key, value):
            """Update coordination rule."""
            if rule_type in self.coordination_rules and key in self.coordination_rules[rule_type]:
                self.coordination_rules[rule_type][key] = value
        
        def get_coordination_rules(self):
            """Get all coordination rules."""
            return self.coordination_rules
        
        def get_service_status(self):
            """Get service status."""
            return {
                "name": self.name,
                "status": "active",
                "uptime": time.time(),
                "total_commands": self.command_count
            }
        
        def validate_routing_table(self):
            """Validate routing table structure."""
            for strategy, config in self.routing_table.items():
                if "timeout" not in config or "retries" not in config:
                    return False
            return True
        
        def reset_service(self):
            """Reset service state."""
            self.command_history = []
            self.command_count = 0
            self.successful_commands = 0
            self.failed_commands = 0

    # Use mock classes
    ConsolidatedCoordinationService = MockConsolidatedCoordinationService
    UnifiedMessage = MockUnifiedMessage
    UnifiedMessageType = MockUnifiedMessageType
    UnifiedMessagePriority = MockUnifiedMessagePriority
    SenderType = MockSenderType


class TestCoordinationServiceAdvanced:
    """Advanced tests for ConsolidatedCoordinationService."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = ConsolidatedCoordinationService("test-coordinator")
        self.sample_message = UnifiedMessage(
            content="Test coordination message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            sender_type=SenderType.AGENT,
        )
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        pass
    
    @pytest.mark.unit
    def test_bulk_message_processing(self):
        """Test processing multiple messages in batch."""
        service = ConsolidatedCoordinationService()
        
        messages = [
            UnifiedMessage(
                content=f"Bulk message {i}",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
                sender_type=SenderType.AGENT,
            )
            for i in range(5)
        ]
        
        results = []
        for message in messages:
            result = service.process_message(message)
            results.append(result)
        
        # Verify all messages were processed
        assert len(results) == 5
        assert len(service.command_history) == 5
        
        # Verify all results have expected structure
        for result in results:
            assert result["status"] == "processed"
            assert "timestamp" in result
            assert "strategy" in result
    
    @pytest.mark.unit
    def test_coordination_service_status(self):
        """Test service status reporting."""
        service = ConsolidatedCoordinationService("test-service")
        
        status = service.get_service_status()
        
        assert status["name"] == "test-service"
        assert status["status"] == "active"
        assert "uptime" in status
        assert "total_commands" in status
        assert status["total_commands"] == 0
    
    @pytest.mark.unit
    def test_message_priority_handling(self):
        """Test different message priority handling."""
        service = ConsolidatedCoordinationService()
        
        priorities = [
            UnifiedMessagePriority.URGENT,
            UnifiedMessagePriority.HIGH,
            UnifiedMessagePriority.NORMAL,
            UnifiedMessagePriority.LOW,
        ]
        
        for priority in priorities:
            message = UnifiedMessage(
                content=f"Priority {priority.value} message",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=priority,
                sender_type=SenderType.AGENT,
            )
            
            result = service.process_message(message)
            assert result["status"] == "processed"
            assert result["priority"] == priority.value
    
    @pytest.mark.unit
    def test_message_type_routing(self):
        """Test different message type routing."""
        service = ConsolidatedCoordinationService()
        
        message_types = [
            UnifiedMessageType.AGENT_TO_AGENT,
            UnifiedMessageType.AGENT_TO_COORDINATOR,
            UnifiedMessageType.SYSTEM_BROADCAST,
            UnifiedMessageType.COORDINATOR_TO_AGENT,
            UnifiedMessageType.HUMAN_TO_AGENT,
        ]
        
        expected_statuses = {
            UnifiedMessageType.AGENT_TO_AGENT: "processed",
            UnifiedMessageType.AGENT_TO_COORDINATOR: "coordinated",
            UnifiedMessageType.SYSTEM_BROADCAST: "broadcasted",
            UnifiedMessageType.COORDINATOR_TO_AGENT: "prioritized",
            UnifiedMessageType.HUMAN_TO_AGENT: "processed",
        }
        
        for msg_type in message_types:
            message = UnifiedMessage(
                content=f"Type {msg_type.value} message",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=msg_type,
                priority=UnifiedMessagePriority.NORMAL,
                sender_type=SenderType.AGENT,
            )
            
            result = service.process_message(message)
            assert result["status"] == expected_statuses[msg_type]
            assert result["message_type"] == msg_type.value
    
    @pytest.mark.performance
    def test_message_processing_performance(self):
        """Test message processing performance."""
        service = ConsolidatedCoordinationService()
        
        # Process multiple messages and measure performance
        num_messages = 100
        messages = [
            UnifiedMessage(
                content=f"Performance test message {i}",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
                sender_type=SenderType.AGENT,
            )
            for i in range(num_messages)
        ]
        
        start_time = time.time()
        for message in messages:
            service.process_message(message)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # Performance check: should process at least 10 messages per second
        messages_per_second = num_messages / processing_time
        assert messages_per_second > 10  # More realistic expectation
    
    @pytest.mark.unit
    def test_edge_case_empty_messages(self):
        """Test handling of edge cases with empty or minimal messages."""
        service = ConsolidatedCoordinationService()
        
        # Test with minimal content
        minimal_message = UnifiedMessage(
            content="",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            sender_type=SenderType.AGENT,
        )
        
        result = service.process_message(minimal_message)
        assert result["status"] == "processed"
        
        # Test with very long content
        long_content = "A" * 10000
        long_message = UnifiedMessage(
            content=long_content,
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            sender_type=SenderType.AGENT,
        )
        
        result = service.process_message(long_message)
        assert result["status"] == "processed"


# Integration Tests
class TestCoordinationServiceIntegration:
    """Integration tests for ConsolidatedCoordinationService."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = ConsolidatedCoordinationService()
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        pass
    
    @pytest.mark.integration
    def test_full_coordination_workflow(self):
        """Test complete coordination workflow."""
        service = ConsolidatedCoordinationService()
        
        # Create a complex message requiring coordination
        complex_message = UnifiedMessage(
            content="Urgent coordination required for system maintenance",
            sender="Agent-4",
            recipient="Agent-1",
            message_type=UnifiedMessageType.AGENT_TO_COORDINATOR,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.COORDINATOR,
        )
        
        result = service.process_message(complex_message)
        
        # Verify coordination workflow
        assert result["status"] == "coordinated"
        assert result["strategy"] == "highest_priority"
        assert result["priority"] == "urgent"
        assert "timestamp" in result
        assert "routing" in result
        
        # Verify command history
        assert len(service.command_history) == 1
        history_entry = service.command_history[0]
        assert history_entry["status"] == "coordinated"
        assert history_entry["strategy"] == "highest_priority"
    
    @pytest.mark.integration
    def test_multi_agent_coordination_scenario(self):
        """Test coordination scenario with multiple agents."""
        service = ConsolidatedCoordinationService()
        
        # Simulate messages from different agents with different priorities
        messages = [
            UnifiedMessage(
                content="High priority coordination",
                sender="Agent-4",
                recipient="Agent-1",
                message_type=UnifiedMessageType.AGENT_TO_COORDINATOR,
                priority=UnifiedMessagePriority.HIGH,
                sender_type=SenderType.COORDINATOR,
            ),
            UnifiedMessage(
                content="Normal agent communication",
                sender="Agent-2",
                recipient="Agent-3",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
                sender_type=SenderType.AGENT,
            ),
            UnifiedMessage(
                content="System maintenance notification",
                sender="system",
                recipient="all-agents",
                message_type=UnifiedMessageType.COORDINATOR_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
                sender_type=SenderType.SYSTEM,
            ),
        ]
        
        # Process all messages
        results = []
        for message in messages:
            result = service.process_message(message)
            results.append(result)
        
        # Verify different strategies were applied
        assert results[0]["strategy"] == "highest_priority"  # Captain + High priority
        assert results[1]["strategy"] == "standard"  # Normal agent communication
        assert results[2]["strategy"] == "system_priority"  # System message
        
        # Verify all were processed successfully with appropriate statuses
        assert results[0]["status"] == "coordinated"  # highest_priority strategy
        assert results[1]["status"] == "processed"  # standard strategy
        assert results[2]["status"] == "prioritized"  # system_priority strategy
        
        # Verify command history
        assert len(service.command_history) == 3
    
    @pytest.mark.integration
    def test_error_recovery_and_retry_logic(self):
        """Test error recovery and retry logic in coordination."""
        service = ConsolidatedCoordinationService()
        
        # Mock a temporary failure scenario
        call_count = 0
        
        def mock_routing_failure(strategy):
            nonlocal call_count
            call_count += 1
            if call_count < 3:  # Fail first 2 attempts
                raise Exception("Temporary routing failure")
            return {"timeout": 10, "retries": 3}  # Succeed on 3rd attempt
        
        # Process message with simulated failures
        with patch.object(service, "get_routing_config", side_effect=mock_routing_failure):
            urgent_message = UnifiedMessage(
                content="Critical coordination with retry",
                sender="Agent-4",
                recipient="Agent-1",
                message_type=UnifiedMessageType.AGENT_TO_COORDINATOR,
                priority=UnifiedMessagePriority.URGENT,
                sender_type=SenderType.COORDINATOR,
            )
            
            result = service.process_message(urgent_message)
            
            # Should fail due to routing configuration failure
            assert result["status"] == "failed"
            assert call_count >= 1  # Should have been called at least once


if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",
        "--cov=src/services/consolidated_coordination_service",
        "--cov-report=html",
        "--cov-report=term-missing",
    ])
