#!/usr/bin/env python3
"""
Coordination Tracker - Track agent coordination requests
======================================================

Coordination tracking functionality extracted from consolidated_messaging_service.py
for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
import time

logger = logging.getLogger(__name__)


class CoordinationTracker:
    """Track coordination requests for protocol compliance."""

    def __init__(self) -> None:
        """Initialize coordination tracker."""
        self.coordination_requests: dict = {}

    def track_coordination_request(self, from_agent: str, to_agent: str, message: str) -> str:
        """Track coordination requests for protocol compliance."""
        request_id = f"{from_agent}_{to_agent}_{int(time.time())}"
        self.coordination_requests[request_id] = {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "message": message,
            "timestamp": time.time(),
            "acknowledged": False,
            "responded": False,
            "completed": False,
        }
        logger.info(f"Coordination request tracked: {request_id}")
        return request_id

    def acknowledge_request(self, request_id: str) -> bool:
        """Mark coordination request as acknowledged."""
        if request_id in self.coordination_requests:
            self.coordination_requests[request_id]["acknowledged"] = True
            logger.info(f"Coordination request acknowledged: {request_id}")
            return True
        return False

    def mark_request_responded(self, request_id: str) -> bool:
        """Mark coordination request as responded."""
        if request_id in self.coordination_requests:
            self.coordination_requests[request_id]["responded"] = True
            logger.info(f"Coordination request responded: {request_id}")
            return True
        return False

    def mark_request_completed(self, request_id: str) -> bool:
        """Mark coordination request as completed."""
        if request_id in self.coordination_requests:
            self.coordination_requests[request_id]["completed"] = True
            logger.info(f"Coordination request completed: {request_id}")
            return True
        return False

    def check_response_protocol(self) -> dict[str, list[str]]:
        """Check for protocol violations."""
        violations = {"overdue": [], "unacknowledged": [], "incomplete": []}
        current_time = time.time()

        for request_id, request in self.coordination_requests.items():
            # Check for overdue responses (>2 agent cycles = ~10 minutes)
            if current_time - request["timestamp"] > 600 and not request["acknowledged"]:
                violations["overdue"].append(request_id)

            # Check for unacknowledged requests (>1 agent cycle = ~5 minutes)
            if current_time - request["timestamp"] > 300 and not request["acknowledged"]:
                violations["unacknowledged"].append(request_id)

            # Check for incomplete responses (>1 hour without completion)
            if current_time - request["timestamp"] > 3600 and not request["completed"]:
                violations["incomplete"].append(request_id)

        return violations

    def get_active_requests(self) -> list[str]:
        """Get list of active coordination requests."""
        return [
            req_id for req_id, req in self.coordination_requests.items() if not req["completed"]
        ]

    def get_request_status(self, request_id: str) -> dict:
        """Get status of specific coordination request."""
        return self.coordination_requests.get(request_id, {})

    def cleanup_completed_requests(self, max_age_hours: int = 24) -> int:
        """Clean up old completed requests."""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        cleaned_count = 0

        requests_to_remove = []
        for request_id, request in self.coordination_requests.items():
            if request["completed"] and current_time - request["timestamp"] > max_age_seconds:
                requests_to_remove.append(request_id)

        for request_id in requests_to_remove:
            del self.coordination_requests[request_id]
            cleaned_count += 1

        logger.info(f"Cleaned up {cleaned_count} old coordination requests")
        return cleaned_count

    def get_coordination_stats(self) -> dict:
        """Get coordination tracking statistics."""
        total_requests = len(self.coordination_requests)
        active_requests = len(self.get_active_requests())
        acknowledged_requests = len(
            [r for r in self.coordination_requests.values() if r["acknowledged"]]
        )
        completed_requests = len([r for r in self.coordination_requests.values() if r["completed"]])

        return {
            "total_requests": total_requests,
            "active_requests": active_requests,
            "acknowledged_requests": acknowledged_requests,
            "completed_requests": completed_requests,
            "completion_rate": completed_requests / total_requests if total_requests > 0 else 0,
        }
