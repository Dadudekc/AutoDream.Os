#!/usr/bin/env python3
"""
Delivery Status Tracker for V2 Message Delivery Service
Handles message delivery status tracking and statistics
"""

import logging
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class DeliveryStatusTracker:
    """Tracks message delivery status and statistics"""

    def __init__(self):
        self.delivery_status = {}

    def initialize_agent_status(self, agent_id: str):
        """Initialize delivery status for a new agent"""
        if agent_id not in self.delivery_status:
            self.delivery_status[agent_id] = {
                "delivery_count": 0,
                "successful_deliveries": 0,
                "failed_deliveries": 0,
                "last_message_type": None,
                "last_delivery_time": None,
                "last_success_time": None,
                "last_failure_time": None,
            }

    def record_successful_delivery(
        self, agent_id: str, message_type: str, timestamp: Optional[float] = None
    ):
        """Record a successful message delivery"""
        try:
            self.initialize_agent_status(agent_id)
            current_time = timestamp or time.time()

            self.delivery_status[agent_id].update({
                "last_message_type": message_type,
                "last_delivery_time": current_time,
                "last_success_time": current_time,
                "delivery_count": self.delivery_status[agent_id]["delivery_count"] + 1,
                "successful_deliveries": self.delivery_status[agent_id]["successful_deliveries"] + 1,
            })

            logger.info(f"✅ Delivery success recorded for {agent_id}: {message_type}")

        except Exception as e:
            logger.error(f"❌ Error recording successful delivery: {e}")

    def record_failed_delivery(
        self, agent_id: str, message_type: str, timestamp: Optional[float] = None
    ):
        """Record a failed message delivery"""
        try:
            self.initialize_agent_status(agent_id)
            current_time = timestamp or time.time()

            self.delivery_status[agent_id].update({
                "last_message_type": message_type,
                "last_delivery_time": current_time,
                "last_failure_time": current_time,
                "delivery_count": self.delivery_status[agent_id]["delivery_count"] + 1,
                "failed_deliveries": self.delivery_status[agent_id]["failed_deliveries"] + 1,
            })

            logger.error(f"❌ Delivery failure recorded for {agent_id}: {message_type}")

        except Exception as e:
            logger.error(f"❌ Error recording failed delivery: {e}")

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get delivery status for a specific agent"""
        return self.delivery_status.get(agent_id)

    def get_all_status(self) -> Dict[str, Any]:
        """Get delivery status for all agents"""
        return self.delivery_status.copy()

    def get_delivery_statistics(self) -> Dict[str, Any]:
        """Get overall delivery statistics"""
        try:
            total_deliveries = 0
            total_success = 0
            total_failures = 0

            for agent_status in self.delivery_status.values():
                total_deliveries += agent_status.get("delivery_count", 0)
                total_success += agent_status.get("successful_deliveries", 0)
                total_failures += agent_status.get("failed_deliveries", 0)

            success_rate = (
                (total_success / total_deliveries * 100) if total_deliveries > 0 else 0
            )

            return {
                "total_deliveries": total_deliveries,
                "total_success": total_success,
                "total_failures": total_failures,
                "success_rate": round(success_rate, 1),
                "agent_count": len(self.delivery_status),
            }

        except Exception as e:
            logger.error(f"❌ Error calculating delivery statistics: {e}")
            return {
                "total_deliveries": 0,
                "total_success": 0,
                "total_failures": 0,
                "success_rate": 0,
                "agent_count": 0,
            }

    def get_agent_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for all agents"""
        try:
            summary = {}
            for agent_id, status in self.delivery_status.items():
                delivery_count = status.get("delivery_count", 0)
                if delivery_count > 0:
                    success_rate = (
                        status.get("successful_deliveries", 0) / delivery_count * 100
                    )
                else:
                    success_rate = 0

                summary[agent_id] = {
                    "delivery_count": delivery_count,
                    "successful_deliveries": status.get("successful_deliveries", 0),
                    "failed_deliveries": status.get("failed_deliveries", 0),
                    "success_rate": round(success_rate, 1),
                    "last_delivery": status.get("last_delivery_time"),
                    "last_message_type": status.get("last_message_type"),
                }

            return summary

        except Exception as e:
            logger.error(f"❌ Error generating performance summary: {e}")
            return {}

    def reset_agent_status(self, agent_id: str):
        """Reset delivery status for a specific agent"""
        try:
            if agent_id in self.delivery_status:
                self.delivery_status[agent_id] = {
                    "delivery_count": 0,
                    "successful_deliveries": 0,
                    "failed_deliveries": 0,
                    "last_message_type": None,
                    "last_delivery_time": None,
                    "last_success_time": None,
                    "last_failure_time": None,
                }
                logger.info(f"🔄 Reset delivery status for {agent_id}")

        except Exception as e:
            logger.error(f"❌ Error resetting agent status: {e}")

    def reset_all_status(self):
        """Reset delivery status for all agents"""
        try:
            for agent_id in list(self.delivery_status.keys()):
                self.reset_agent_status(agent_id)
            logger.info("🔄 Reset delivery status for all agents")

        except Exception as e:
            logger.error(f"❌ Error resetting all status: {e}")

    def export_status_report(self) -> Dict[str, Any]:
        """Export comprehensive status report"""
        try:
            return {
                "timestamp": time.time(),
                "delivery_status": self.get_all_status(),
                "statistics": self.get_delivery_statistics(),
                "performance_summary": self.get_agent_performance_summary(),
            }

        except Exception as e:
            logger.error(f"❌ Error exporting status report: {e}")
            return {"error": str(e)}

