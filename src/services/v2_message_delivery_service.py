#!/usr/bin/env python3
"""
V2 Message Delivery Service
Actually delivers messages to agent input coordinates using V2 integration
"""

import logging
import time
import threading
from typing import Dict, Any, Optional, List
import queue

from coordinate_manager import CoordinateManager
from delivery_status_tracker import DeliveryStatusTracker
from message_delivery_core import MessageDeliveryCore

logger = logging.getLogger(__name__)


class V2MessageDeliveryService:
    """
    V2 Message Delivery Service
    Orchestrates message delivery using modular components
    """

    def __init__(self):
        # Initialize modular components
        self.coordinate_manager = CoordinateManager()
        self.status_tracker = DeliveryStatusTracker()
        self.delivery_core = MessageDeliveryCore()
        
        # Message queue for asynchronous delivery
        self.message_queue = queue.Queue()
        self.delivery_thread = None
        
        # Start message delivery thread
        self._start_delivery_thread()

    def _start_delivery_thread(self):
        """Start the message delivery thread"""
        try:
            self.delivery_thread = threading.Thread(
                target=self._delivery_worker, daemon=True
            )
            self.delivery_thread.start()
            logger.info("🔄 Message delivery thread started")
        except Exception as e:
            logger.error(f"❌ Error starting delivery thread: {e}")

    def _delivery_worker(self):
        """Worker thread for processing message queue"""
        while True:
            try:
                # Get message from queue
                message_data = self.message_queue.get(timeout=1.0)
                if message_data is None:  # Shutdown signal
                    break
                
                # Process the message
                self._deliver_message(message_data)
                
                # Mark task as done
                self.message_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ Error in delivery worker: {e}")
                if message_data:
                    self.message_queue.task_done()

    def _deliver_message(self, message_data: Dict[str, Any]):
        """Deliver a single message"""
        try:
            agent_id = message_data["agent_id"]
            message_type = message_data["type"]
            content = message_data.get("content", "")
            
            # Get agent coordinates
            agent_coords = self.coordinate_manager.get_agent_coordinates(agent_id)
            if not agent_coords:
                logger.error(f"❌ No coordinates found for agent {agent_id}")
                self.status_tracker.record_failed_delivery(agent_id, message_type)
                return

            # Deliver the message
            success = self.delivery_core.deliver_message(
                agent_coords, message_type, content, message_data
            )

            # Update status and coordinates
            if success:
                self.status_tracker.record_successful_delivery(agent_id, message_type)
                self.coordinate_manager.update_delivery_timestamp(agent_id)
                logger.info(f"✅ Message delivered successfully to {agent_id}")
            else:
                self.status_tracker.record_failed_delivery(agent_id, message_type)
                logger.error(f"❌ Failed to deliver message to {agent_id}")

        except Exception as e:
            logger.error(f"❌ Error delivering message: {e}")
            if "agent_id" in message_data:
                self.status_tracker.record_failed_delivery(
                    message_data["agent_id"], 
                    message_data.get("type", "unknown")
                )

    def send_message(
        self, agent_id: str, message_type: str, content: str = "", **kwargs
    ) -> bool:
        """Send a message to a specific agent"""
        try:
            message_data = {
                "agent_id": agent_id,
                "type": message_type,
                "content": content,
                "timestamp": time.time(),
                **kwargs,
            }

            # Add message to delivery queue
            self.message_queue.put(message_data)

            logger.info(f"📤 Message queued for delivery to {agent_id}: {message_type}")
            return True

        except Exception as e:
            logger.error(f"❌ Error queuing message: {e}")
            return False

    def send_message_sync(
        self, agent_id: str, message_type: str, content: str = "", **kwargs
    ) -> bool:
        """Send a message to a specific agent synchronously (for testing)"""
        try:
            message_data = {
                "agent_id": agent_id,
                "type": message_type,
                "content": content,
                "timestamp": time.time(),
                **kwargs,
            }

            # Deliver message immediately (bypassing queue)
            logger.info(f"📤 Sending message synchronously to {agent_id}: {message_type}")
            self._deliver_message(message_data)
            return True

        except Exception as e:
            logger.error(f"❌ Error sending message synchronously: {e}")
            return False

    def broadcast_message(
        self,
        message_type: str,
        content: str = "",
        target_agents: List[str] = None,
        **kwargs,
    ) -> Dict[str, bool]:
        """Broadcast a message to multiple agents"""
        try:
            if target_agents is None:
                target_agents = list(self.coordinate_manager.get_all_coordinates().keys())

            results = {}

            for agent_id in target_agents:
                success = self.send_message(agent_id, message_type, content, **kwargs)
                results[agent_id] = success

            logger.info(f"📢 Broadcast message sent to {len(target_agents)} agents")
            return results

        except Exception as e:
            logger.error(f"❌ Error broadcasting message: {e}")
            return {}

    def update_agent_coordinates(
        self, agent_id: str, input_x: int, input_y: int
    ) -> bool:
        """Update agent input coordinates"""
        return self.coordinate_manager.update_agent_coordinates(agent_id, input_x, input_y)

    def get_delivery_status(self) -> Dict[str, Any]:
        """Get comprehensive delivery status"""
        try:
            return {
                "delivery_status": self.status_tracker.get_all_status(),
                "agent_coordinates": self.coordinate_manager.get_all_coordinates(),
                "queue_size": self.message_queue.qsize(),
                "pyautogui_available": self.delivery_core.is_pyautogui_available(),
                "timestamp": time.time(),
            }

        except Exception as e:
            logger.error(f"❌ Error getting delivery status: {e}")
            return {"error": str(e)}

    def get_agent_coordinates(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get coordinates for a specific agent"""
        return self.coordinate_manager.get_agent_coordinates(agent_id)

    def get_all_agent_coordinates(self) -> Dict[str, Any]:
        """Get all agent coordinates"""
        return self.coordinate_manager.get_all_coordinates()

    def get_delivery_statistics(self) -> Dict[str, Any]:
        """Get delivery statistics"""
        return self.status_tracker.get_delivery_statistics()

    def get_agent_performance_summary(self) -> Dict[str, Any]:
        """Get agent performance summary"""
        return self.status_tracker.get_agent_performance_summary()

    def reset_delivery_status(self, agent_id: Optional[str] = None):
        """Reset delivery status for agent(s)"""
        if agent_id:
            self.status_tracker.reset_agent_status(agent_id)
        else:
            self.status_tracker.reset_all_status()

    def shutdown(self):
        """Shutdown the service gracefully"""
        try:
            # Send shutdown signal to delivery thread
            if self.delivery_thread and self.delivery_thread.is_alive():
                self.message_queue.put(None)
                self.delivery_thread.join(timeout=5.0)
                logger.info("🔄 Message delivery thread stopped")
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")


# CLI interface for testing
def main():
    """CLI interface for V2 Message Delivery Service"""
    from cli_interface import main as cli_main
    return cli_main()


if __name__ == "__main__":
    exit(main())

