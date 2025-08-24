#!/usr/bin/env python3
"""
Messaging Integration Tests - Agent Cellphone V2
===============================================

TDD tests for messaging system integration with autonomous development.
Tests communication between agents using the V2 messaging system.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import unittest
import json
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from ..communication.development_communication import DevelopmentCommunication
from ...core.messaging import V2MessageQueue, V2Message, V2MessagePriority, V2MessageType, V2MessageStatus


class TestMessagingIntegration(unittest.TestCase):
    """Test messaging system integration with autonomous development"""
    
    def setUp(self):
        """Set up test messaging infrastructure"""
        self.communication = DevelopmentCommunication()
        self.message_queue = V2MessageQueue()
        
        # Mock agent IDs for testing
        self.agent_dev = "agent_dev_001"
        self.agent_test = "agent_test_001"
        self.agent_coord = "agent_coord_001"
        
        # Test message content
        self.test_task_data = {
            "task_id": "task_001",
            "title": "Implement authentication",
            "priority": "high",
            "estimated_hours": 8
        }
    
    def test_v2_message_creation(self):
        """Test creating V2 messages for development tasks"""
        message = V2Message(
            message_id="msg_001",
            sender_id=self.agent_coord,
            recipient_id=self.agent_dev,
            message_type=V2MessageType.TASK_ASSIGNMENT,
            content=self.test_task_data,
            priority=V2MessagePriority.HIGH,
            timestamp=datetime.now()
        )
        
        self.assertEqual(message.message_id, "msg_001")
        self.assertEqual(message.sender_id, self.agent_coord)
        self.assertEqual(message.recipient_id, self.agent_dev)
        self.assertEqual(message.message_type, V2MessageType.TASK_ASSIGNMENT)
        self.assertEqual(message.priority, V2MessagePriority.HIGH)
        self.assertEqual(message.content["task_id"], "task_001")
    
    def test_message_queue_operations(self):
        """Test V2 message queue operations"""
        # Create and enqueue messages
        message1 = V2Message(
            message_id="msg_001",
            sender_id=self.agent_coord,
            recipient_id=self.agent_dev,
            message_type=V2MessageType.TASK_ASSIGNMENT,
            content=self.test_task_data,
            priority=V2MessagePriority.HIGH,
            timestamp=datetime.now()
        )
        
        message2 = V2Message(
            message_id="msg_002",
            sender_id=self.agent_dev,
            recipient_id=self.agent_coord,
            message_type=V2MessageType.TASK_UPDATE,
            content={"task_id": "task_001", "status": "in_progress"},
            priority=V2MessagePriority.MEDIUM,
            timestamp=datetime.now()
        )
        
        # Enqueue messages
        self.message_queue.enqueue(message1)
        self.message_queue.enqueue(message2)
        
        # Check queue size
        self.assertEqual(self.message_queue.size(), 2)
        
        # Dequeue messages (should be priority-based)
        dequeued1 = self.message_queue.dequeue()
        dequeued2 = self.message_queue.dequeue()
        
        # High priority should come first
        self.assertEqual(dequeued1.priority, V2MessagePriority.HIGH)
        self.assertEqual(dequeued2.priority, V2MessagePriority.MEDIUM)
        
        # Queue should be empty
        self.assertEqual(self.message_queue.size(), 0)
    
    def test_development_communication_integration(self):
        """Test development communication with V2 messaging"""
        # Send message through development communication
        message_id = self.communication.send_message(
            sender_id=self.agent_coord,
            recipient_id=self.agent_dev,
            message_type="task_assignment",
            content=self.test_task_data,
            priority="high",
            requires_ack=True
        )
        
        # Verify message was created
        self.assertIsNotNone(message_id)
        self.assertIn(message_id, self.communication.messages)
        
        # Verify message content
        message = self.communication.messages[message_id]
        self.assertEqual(message.sender_id, self.agent_coord)
        self.assertEqual(message.recipient_id, self.agent_dev)
        self.assertEqual(message.message_type, "task_assignment")
        self.assertEqual(message.content["task_id"], "task_001")
        self.assertTrue(message.requires_ack)
        self.assertFalse(message.acknowledged)
    
    def test_message_acknowledgment_flow(self):
        """Test complete message acknowledgment flow"""
        # Send message requiring acknowledgment
        message_id = self.communication.send_message(
            sender_id=self.agent_coord,
            recipient_id=self.agent_dev,
            message_type="task_assignment",
            content=self.test_task_data,
            priority="high",
            requires_ack=True
        )
        
        # Verify pending acknowledgment
        self.assertEqual(
            self.communication.communication_stats["messages_pending_ack"], 
            1
        )
        
        # Acknowledge message
        self.communication.acknowledge_message(message_id)
        
        # Verify acknowledgment
        message = self.communication.messages[message_id]
        self.assertTrue(message.acknowledged)
        self.assertIsNotNone(message.acknowledged_at)
        
        # Verify stats updated
        self.assertEqual(
            self.communication.communication_stats["messages_acknowledged"], 
            1
        )
        self.assertEqual(
            self.communication.communication_stats["messages_pending_ack"], 
            0
        )
    
    def test_message_type_handlers(self):
        """Test message type handlers for different development scenarios"""
        # Test task assignment handler
        with patch.object(self.communication, '_handle_task_assignment') as mock_handler:
            message_id = self.communication.send_message(
                sender_id=self.agent_coord,
                recipient_id=self.agent_dev,
                message_type="task_assignment",
                content=self.test_task_data,
                priority="high"
            )
            
            # Verify handler was called
            mock_handler.assert_called_once()
        
        # Test task update handler
        with patch.object(self.communication, '_handle_task_update') as mock_handler:
            message_id = self.communication.send_message(
                sender_id=self.agent_dev,
                recipient_id=self.agent_coord,
                message_type="task_update",
                content={"task_id": "task_001", "progress": 50},
                priority="medium"
            )
            
            # Verify handler was called
            mock_handler.assert_called_once()
    
    def test_priority_based_message_routing(self):
        """Test priority-based message routing and processing"""
        # Send messages with different priorities
        high_priority_msg = self.communication.send_message(
            sender_id=self.agent_coord,
            recipient_id=self.agent_dev,
            message_type="urgent_task",
            content={"task_id": "task_urgent", "priority": "critical"},
            priority="critical"
        )
        
        medium_priority_msg = self.communication.send_message(
            sender_id=self.agent_coord,
            recipient_id=self.agent_dev,
            message_type="regular_task",
            content={"task_id": "task_regular", "priority": "medium"},
            priority="medium"
        )
        
        # Verify both messages exist
        self.assertIn(high_priority_msg, self.communication.messages)
        self.assertIn(medium_priority_msg, self.communication.messages)
        
        # Verify priority tracking
        high_msg = self.communication.messages[high_priority_msg]
        medium_msg = self.communication.messages[medium_priority_msg]
        
        self.assertEqual(high_msg.priority, "critical")
        self.assertEqual(medium_msg.priority, "medium")
    
    def test_message_error_handling(self):
        """Test message error handling and recovery"""
        # Send message with invalid content
        with self.assertRaises(ValueError):
            self.communication.send_message(
                sender_id="",
                recipient_id=self.agent_dev,
                message_type="task_assignment",
                content={},
                priority="high"
            )
        
        # Verify error stats updated
        self.assertEqual(
            self.communication.communication_stats["communication_errors"], 
            1
        )
    
    def test_message_history_and_analytics(self):
        """Test message history tracking and analytics"""
        # Send multiple messages
        for i in range(5):
            self.communication.send_message(
                sender_id=self.agent_coord,
                recipient_id=self.agent_dev,
                message_type=f"task_{i}",
                content={"task_id": f"task_{i:03d}"},
                priority="medium"
            )
        
        # Verify message history
        self.assertEqual(len(self.communication.messages), 5)
        self.assertEqual(
            self.communication.communication_stats["total_messages_sent"], 
            5
        )
        
        # Test message retrieval by type
        task_messages = [
            msg for msg in self.communication.messages.values()
            if msg.message_type.startswith("task_")
        ]
        self.assertEqual(len(task_messages), 5)
    
    def test_agent_heartbeat_monitoring(self):
        """Test agent heartbeat monitoring through messaging"""
        # Send heartbeat message
        heartbeat_msg = self.communication.send_message(
            sender_id=self.agent_dev,
            recipient_id=self.agent_coord,
            message_type="agent_heartbeat",
            content={
                "agent_id": self.agent_dev,
                "status": "active",
                "current_task": "task_001",
                "memory_usage": 0.75,
                "cpu_usage": 0.60
            },
            priority="low"
        )
        
        # Verify heartbeat handling
        with patch.object(self.communication, '_handle_agent_heartbeat') as mock_handler:
            message = self.communication.messages[heartbeat_msg]
            self.communication._process_message(message)
            mock_handler.assert_called_once_with(message)
    
    def test_coordination_request_handling(self):
        """Test coordination request message handling"""
        # Send coordination request
        coord_request = self.communication.send_message(
            sender_id=self.agent_dev,
            recipient_id=self.agent_coord,
            message_type="coordination_request",
            content={
                "request_type": "resource_allocation",
                "agent_id": self.agent_dev,
                "required_resources": ["memory", "cpu"],
                "priority": "high"
            },
            priority="high",
            requires_ack=True
        )
        
        # Verify coordination request handling
        with patch.object(self.communication, '_handle_coordination_request') as mock_handler:
            message = self.communication.messages[coord_request]
            self.communication._process_message(message)
            mock_handler.assert_called_once_with(message)


if __name__ == '__main__':
    unittest.main()
