#!/usr/bin/env python3
"""
Smoke Test for V2 Comprehensive Messaging System

Quick validation that the TRULY comprehensive messaging system works
with ALL features from all 5 original systems consolidated into one.

Author: V2 Testing Specialist
License: MIT
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def smoke_test_comprehensive_system():
    """Run smoke test for V2 comprehensive messaging system"""
    print("🧪 V2 Comprehensive Messaging System - Smoke Test")
    print("=" * 60)
    
    try:
        # Test 1: Import the comprehensive messaging system
        print("✅ Test 1: Importing V2 comprehensive messaging system...")
        from core.v2_comprehensive_messaging_system import (
            V2MessageType, V2MessagePriority, V2MessageStatus, V2AgentStatus,
            V2TaskStatus, V2WorkflowStatus, V2WorkflowType, V2AgentCapability,
            V2Message, V2AgentInfo, V2ComprehensiveMessagingSystem,
            create_onboarding_message, create_coordination_message, create_broadcast_message,
            create_task_message, create_workflow_message
        )
        print("   ✅ Import successful - ALL 5 systems consolidated!")
        
        # Test 2: Verify comprehensive enum coverage
        print("✅ Test 2: Verifying comprehensive enum coverage...")
        message_type_count = len(V2MessageType)
        priority_count = len(V2MessagePriority)
        status_count = len(V2MessageStatus)
        agent_status_count = len(V2AgentStatus)
        task_status_count = len(V2TaskStatus)
        workflow_status_count = len(V2WorkflowStatus)
        workflow_type_count = len(V2WorkflowType)
        agent_capability_count = len(V2AgentCapability)
        
        print(f"   ✅ Message Types: {message_type_count} (should be 40+)")
        print(f"   ✅ Priorities: {priority_count} (should be 5)")
        print(f"   ✅ Statuses: {status_count} (should be 9)")
        print(f"   ✅ Agent Statuses: {agent_status_count} (should be 9)")
        print(f"   ✅ Task Statuses: {task_status_count} (should be 8)")
        print(f"   ✅ Workflow Statuses: {workflow_status_count} (should be 17)")
        print(f"   ✅ Workflow Types: {workflow_type_count} (should be 6)")
        print(f"   ✅ Agent Capabilities: {agent_capability_count} (should be 6)")
        
        # Verify we have comprehensive coverage
        assert message_type_count >= 40, f"Expected 40+ message types, got {message_type_count}"
        assert priority_count == 5, f"Expected 5 priorities, got {priority_count}"
        assert status_count >= 9, f"Expected 9+ statuses, got {status_count}"
        assert agent_status_count >= 9, f"Expected 9+ agent statuses, got {agent_status_count}"
        assert task_status_count >= 8, f"Expected 8+ task statuses, got {task_status_count}"
        assert workflow_status_count >= 17, f"Expected 17+ workflow statuses, got {workflow_status_count}"
        assert workflow_type_count >= 6, f"Expected 6+ workflow types, got {workflow_type_count}"
        assert agent_capability_count >= 6, f"Expected 6+ agent capabilities, got {agent_capability_count}"
        
        # Test 3: Create comprehensive message with ALL features
        print("✅ Test 3: Creating comprehensive message with ALL features...")
        message = V2Message(
            message_type=V2MessageType.ONBOARDING_PHASE,
            priority=V2MessagePriority.CRITICAL,
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            subject="Comprehensive Smoke Test",
            content="Testing ALL features from all 5 systems",
            payload={"test": "comprehensive", "systems": 5},
            requires_acknowledgment=True,
            is_onboarding_message=True,
            phase_number=1,
            workflow_id="smoke-test-workflow",
            task_id="smoke-test-task",
            ttl=3600,
            max_retries=5,
            sequence_number=1,
            dependencies=["msg-1", "msg-2"],
            tags=["smoke", "comprehensive", "unified"]
        )
        
        print(f"   ✅ Message created with ID: {message.message_id}")
        print(f"   ✅ Message type: {message.message_type.value}")
        print(f"   ✅ Priority: {message.priority.value}")
        print(f"   ✅ Workflow ID: {message.workflow_id}")
        print(f"   ✅ Task ID: {message.task_id}")
        print(f"   ✅ Dependencies: {message.dependencies}")
        print(f"   ✅ Tags: {message.tags}")
        
        # Test 4: Initialize comprehensive messaging system
        print("✅ Test 4: Initializing comprehensive messaging system...")
        messaging_system = V2ComprehensiveMessagingSystem()
        print(f"   ✅ System active: {messaging_system.communication_active}")
        print(f"   ✅ Queue metrics: {messaging_system.queue_metrics}")
        
        # Test 5: Test ALL message types from all systems
        print("✅ Test 5: Testing ALL message types from all systems...")
        
        # Core Communication (from agent_communication.py)
        core_msg_id = messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.TASK_ASSIGNMENT,
            subject="Core Communication Test",
            content="Testing core communication features",
            priority=V2MessagePriority.HIGH
        )
        print(f"   ✅ Core communication message sent: {core_msg_id}")
        
        # Advanced Messaging (from message_types.py)
        advanced_msg_id = messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.VALIDATION,
            subject="Advanced Messaging Test",
            content="Testing advanced messaging features",
            priority=V2MessagePriority.NORMAL,
            ttl=1800,
            tags=["advanced", "validation"]
        )
        print(f"   ✅ Advanced messaging message sent: {advanced_msg_id}")
        
        # Workflow Management (from shared_enums.py)
        workflow_msg_id = messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.CONTRACT_ASSIGNMENT,
            subject="Workflow Management Test",
            content="Testing workflow management features",
            priority=V2MessagePriority.URGENT,
            workflow_id="smoke-workflow",
            sequence_number=1
        )
        print(f"   ✅ Workflow management message sent: {workflow_msg_id}")
        
        # V2 Specific
        v2_msg_id = messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.ONBOARDING_PHASE,
            subject="V2 Specific Test",
            content="Testing V2 specific features",
            priority=V2MessagePriority.CRITICAL,
            requires_acknowledgment=True,
            is_onboarding_message=True,
            phase_number=1
        )
        print(f"   ✅ V2 specific message sent: {v2_msg_id}")
        
        # Test 6: Test comprehensive message retrieval
        print("✅ Test 6: Testing comprehensive message retrieval...")
        messages = messaging_system.get_messages_for_agent("Agent-1")
        print(f"   ✅ Retrieved {len(messages)} messages for Agent-1")
        
        # Verify priority sorting (CRITICAL first, then URGENT, then HIGH, then NORMAL)
        priorities = [msg.priority.value for msg in messages]
        print(f"   ✅ Priority order: {priorities}")
        assert priorities == [5, 4, 3, 2], f"Expected priority order [5,4,3,2], got {priorities}"
        
        # Test 7: Test comprehensive agent registration
        print("✅ Test 7: Testing comprehensive agent registration...")
        capabilities = [
            V2AgentCapability.TASK_EXECUTION,
            V2AgentCapability.DECISION_MAKING,
            V2AgentCapability.COMMUNICATION
        ]
        
        success = messaging_system.register_agent(
            agent_id="SmokeTestAgent",
            name="Smoke Test Agent",
            capabilities=capabilities,
            endpoint="http://localhost:8000",
            metadata={"test": True, "comprehensive": True}
        )
        
        print(f"   ✅ Agent registration: {'SUCCESS' if success else 'FAILED'}")
        assert success, "Agent registration should succeed"
        
        # Test 8: Test comprehensive system status
        print("✅ Test 8: Testing comprehensive system status...")
        status = messaging_system.get_system_status()
        
        print(f"   ✅ System active: {status['system_active']}")
        print(f"   ✅ Total messages: {status['total_messages']}")
        print(f"   ✅ Queued messages: {status['queued_messages']}")
        print(f"   ✅ Registered agents: {status['registered_agents']}")
        print(f"   ✅ Queue metrics: {status['queue_metrics']}")
        print(f"   ✅ Agent statuses: {status['agent_statuses']}")
        
        # Verify all status components are present
        required_keys = [
            "system_active", "total_messages", "queued_messages", "registered_agents",
            "agent_message_counts", "message_types", "priority_counts", "queue_metrics", "agent_statuses"
        ]
        for key in required_keys:
            assert key in status, f"Status missing key: {key}"
        
        # Test 9: Test comprehensive convenience functions
        print("✅ Test 9: Testing comprehensive convenience functions...")
        
        # Test all convenience functions
        onboarding_msg = create_onboarding_message("Agent-1", 1, "Welcome to Phase 1")
        coordination_msg = create_coordination_message("Agent-1", "Agent-2", "Let's coordinate")
        broadcast_msg = create_broadcast_message("SYSTEM", "System is online")
        task_msg = create_task_message("TaskManager", "Agent-1", "task-123", "Complete this task")
        workflow_msg = create_workflow_message("WorkflowEngine", "Agent-1", "workflow-456", "Workflow updated")
        
        print(f"   ✅ Onboarding message: {onboarding_msg.message_type.value}")
        print(f"   ✅ Coordination message: {coordination_msg.message_type.value}")
        print(f"   ✅ Broadcast message: {broadcast_msg.message_type.value}")
        print(f"   ✅ Task message: {task_msg.message_type.value}")
        print(f"   ✅ Workflow message: {workflow_msg.message_type.value}")
        
        # Test 10: Test comprehensive error handling
        print("✅ Test 10: Testing comprehensive error handling...")
        
        # Test acknowledging non-existent message
        ack_success = messaging_system.acknowledge_message("non-existent-id", "Agent-1")
        print(f"   ✅ Acknowledge non-existent message: {'FAILED as expected' if not ack_success else 'UNEXPECTED SUCCESS'}")
        assert not ack_success, "Should fail to acknowledge non-existent message"
        
        # Test acknowledging message that doesn't require acknowledgment
        non_ack_msg_id = messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.COORDINATION,
            subject="No Acknowledgment Required",
            content="This message doesn't require acknowledgment",
            requires_acknowledgment=False
        )
        
        ack_success = messaging_system.acknowledge_message(non_ack_msg_id, "Agent-1")
        print(f"   ✅ Acknowledge non-ack message: {'FAILED as expected' if not ack_success else 'UNEXPECTED SUCCESS'}")
        assert not ack_success, "Should fail to acknowledge message that doesn't require acknowledgment"
        
        # Test 11: Test comprehensive message acknowledgment
        print("✅ Test 11: Testing comprehensive message acknowledgment...")
        
        # Acknowledge the V2 specific message that requires acknowledgment
        ack_success = messaging_system.acknowledge_message(v2_msg_id, "Agent-1")
        print(f"   ✅ Acknowledge V2 message: {'SUCCESS' if ack_success else 'FAILED'}")
        assert ack_success, "Should succeed to acknowledge message that requires acknowledgment"
        
        # Test 12: Test comprehensive cleanup
        print("✅ Test 12: Testing comprehensive cleanup...")
        messaging_system.shutdown()
        print("   ✅ System shutdown complete")
        
        print("\n🎉 ALL COMPREHENSIVE SMOKE TESTS PASSED!")
        print("✅ V2 Comprehensive Messaging System is working correctly with ALL features!")
        return True
        
    except Exception as e:
        print(f"\n❌ COMPREHENSIVE SMOKE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def smoke_test_enum_completeness():
    """Test that ALL enums from all 5 systems are included"""
    print("\n🧪 Testing Enum Completeness")
    print("=" * 40)
    
    try:
        from core.v2_comprehensive_messaging_system import (
            V2MessageType, V2MessagePriority, V2MessageStatus, V2AgentStatus,
            V2TaskStatus, V2WorkflowStatus, V2WorkflowType, V2AgentCapability
        )
        
        # Test message types completeness
        print("✅ Testing Message Types Completeness...")
        
        # Core Communication (from agent_communication.py)
        core_types = [
            "task_assignment", "status_update", "performance_metric", "health_check",
            "coordination", "broadcast", "direct"
        ]
        
        # Advanced Messaging (from message_types.py)
        advanced_types = [
            "task", "response", "alert", "system", "validation", "feedback"
        ]
        
        # Workflow Management (from shared_enums.py)
        workflow_types = [
            "text", "notification", "command", "error", "contract_assignment",
            "emergency", "heartbeat", "system_command"
        ]
        
        # V2 specific
        v2_types = [
            "onboarding_start", "onboarding_phase", "onboarding_complete",
            "task_created", "task_started", "task_completed", "task_failed",
            "agent_registration", "agent_status", "agent_health", "agent_capability_update"
        ]
        
        all_expected_types = core_types + advanced_types + workflow_types + v2_types
        
        missing_types = []
        for expected_type in all_expected_types:
            if expected_type not in [t.value for t in V2MessageType]:
                missing_types.append(expected_type)
        
        if missing_types:
            print(f"❌ Missing message types: {missing_types}")
            return False
        else:
            print("   ✅ ALL expected message types are present")
        
        # Test priorities completeness
        print("✅ Testing Priorities Completeness...")
        priorities = [p.value for p in V2MessagePriority]
        expected_priorities = list(range(1, 6))  # 1-5
        if priorities != expected_priorities:
            print(f"❌ Priorities mismatch: expected {expected_priorities}, got {priorities}")
            return False
        else:
            print("   ✅ ALL priorities are present")
        
        # Test statuses completeness
        print("✅ Testing Statuses Completeness...")
        statuses = [s.value for s in V2MessageStatus]
        expected_statuses = [
            "pending", "processing", "delivered", "acknowledged",
            "completed", "failed", "expired", "cancelled", "read"
        ]
        missing_statuses = []
        for expected in expected_statuses:
            if expected not in statuses:
                missing_statuses.append(expected)
        
        if missing_statuses:
            print(f"❌ Missing statuses: {missing_statuses}")
            return False
        else:
            print("   ✅ ALL expected statuses are present")
        
        print("✅ ALL enum completeness tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Enum completeness test failed: {e}")
        return False


def smoke_test_message_features():
    """Test that ALL message features from all 5 systems work"""
    print("\n🧪 Testing Message Features Completeness")
    print("=" * 45)
    
    try:
        from core.v2_comprehensive_messaging_system import (
            V2Message, V2MessageType, V2MessagePriority, V2MessageStatus
        )
        
        # Test message creation with ALL features
        print("✅ Testing message creation with ALL features...")
        message = V2Message(
            message_type=V2MessageType.ONBOARDING_PHASE,
            priority=V2MessagePriority.CRITICAL,
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            subject="Feature Test",
            content="Testing all features",
            payload={"test": "comprehensive"},
            requires_acknowledgment=True,
            is_onboarding_message=True,
            phase_number=1,
            workflow_id="test-workflow",
            task_id="test-task",
            ttl=3600,
            max_retries=5,
            sequence_number=1,
            dependencies=["msg-1", "msg-2"],
            tags=["test", "comprehensive"]
        )
        
        print("   ✅ Message created with ALL features")
        
        # Test serialization
        print("✅ Testing message serialization...")
        message_dict = message.to_dict()
        
        # Verify all fields are serialized
        required_fields = [
            "message_type", "priority", "sender_id", "recipient_id", "subject", "content",
            "payload", "requires_acknowledgment", "is_onboarding_message", "phase_number",
            "workflow_id", "task_id", "ttl", "max_retries", "sequence_number",
            "dependencies", "tags"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in message_dict:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing serialized fields: {missing_fields}")
            return False
        else:
            print("   ✅ ALL fields serialized correctly")
        
        # Test deserialization
        print("✅ Testing message deserialization...")
        restored_message = V2Message.from_dict(message_dict)
        
        # Verify all fields are restored
        assert restored_message.message_type == message.message_type
        assert restored_message.priority == message.priority
        assert restored_message.sender_id == message.sender_id
        assert restored_message.recipient_id == message.recipient_id
        assert restored_message.subject == message.subject
        assert restored_message.content == message.content
        assert restored_message.payload == message.payload
        assert restored_message.requires_acknowledgment == message.requires_acknowledgment
        assert restored_message.is_onboarding_message == message.is_onboarding_message
        assert restored_message.phase_number == message.phase_number
        assert restored_message.workflow_id == message.workflow_id
        assert restored_message.task_id == message.task_id
        assert restored_message.ttl == message.ttl
        assert restored_message.max_retries == message.max_retries
        assert restored_message.sequence_number == message.sequence_number
        assert restored_message.dependencies == message.dependencies
        assert restored_message.tags == message.tags
        
        print("   ✅ ALL fields deserialized correctly")
        
        # Test advanced features
        print("✅ Testing advanced features...")
        
        # Test TTL expiration
        message.ttl = 1
        assert not message.is_expired()
        import time
        time.sleep(1.1)
        assert message.is_expired()
        
        # Test retry logic
        message.ttl = None
        message.max_retries = 2
        assert message.can_retry()
        
        message.increment_retry()
        assert message.can_retry()
        
        message.increment_retry()
        assert not message.can_retry()
        assert message.status == V2MessageStatus.FAILED
        
        print("   ✅ ALL advanced features work correctly")
        
        print("✅ ALL message feature tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Message feature test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting V2 Comprehensive Messaging System Smoke Tests...")
    print("🎯 Testing ALL features from ALL 5 original systems consolidated into ONE!")
    
    # Run all comprehensive smoke tests
    test1_passed = smoke_test_comprehensive_system()
    test2_passed = smoke_test_enum_completeness()
    test3_passed = smoke_test_message_features()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE SMOKE TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Comprehensive System: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Enum Completeness: {'PASSED' if test2_passed else 'FAILED'}")
    print(f"✅ Message Features: {'PASSED' if test3_passed else 'FAILED'}")
    
    if all([test1_passed, test2_passed, test3_passed]):
        print("\n🎉 ALL COMPREHENSIVE SMOKE TESTS PASSED!")
        print("✅ V2 Comprehensive Messaging System is TRULY unified and production ready!")
        print("🚀 ALL features from ALL 5 original systems are working together!")
        sys.exit(0)
    else:
        print("\n❌ SOME COMPREHENSIVE SMOKE TESTS FAILED!")
        print("❌ V2 Comprehensive Messaging System needs fixes before production!")
        sys.exit(1)
