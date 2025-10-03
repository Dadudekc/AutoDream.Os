#!/usr/bin/env python3
"""
Coordination Tracker - Enhanced Validation Integration
=====================================================

Tracks coordination requests and validates messaging protocols
for enhanced validation system integration.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
import threading
import time
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CoordinationRequest:
    """Coordination request tracking data structure."""

    request_id: str
    from_agent: str
    to_agent: str
    message: str
    timestamp: float
    status: str = "pending"
    response_received: bool = False
    response_timestamp: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "request_id": self.request_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "message": self.message,
            "timestamp": self.timestamp,
            "status": self.status,
            "response_received": self.response_received,
            "response_timestamp": self.response_timestamp,
        }


class CoordinationTracker:
    """Enhanced coordination tracking for messaging system."""

    def __init__(self, max_requests: int = 1000, cleanup_interval: int = 3600):
        """Initialize coordination tracker."""
        self.coordination_requests: dict[str, CoordinationRequest] = {}
        self.max_requests = max_requests
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()
        self._lock = threading.Lock()

        logger.info("CoordinationTracker initialized")

    def track_request(self, from_agent: str, to_agent: str, message: str) -> str:
        """Track a new coordination request."""
        request_id = f"{from_agent}_{to_agent}_{int(time.time() * 1000)}"

        with self._lock:
            # Cleanup if needed
            if len(self.coordination_requests) >= self.max_requests:
                self._cleanup_old_requests()

            request = CoordinationRequest(
                request_id=request_id,
                from_agent=from_agent,
                to_agent=to_agent,
                message=message,
                timestamp=time.time(),
            )

            self.coordination_requests[request_id] = request
            logger.info(f"Coordination request tracked: {request_id}")

            return request_id

    def mark_response_received(self, request_id: str) -> bool:
        """Mark a coordination request as having received a response."""
        with self._lock:
            if request_id in self.coordination_requests:
                self.coordination_requests[request_id].response_received = True
                self.coordination_requests[request_id].response_timestamp = time.time()
                self.coordination_requests[request_id].status = "completed"
                logger.info(f"Response marked for request: {request_id}")
                return True
            return False

    def get_pending_requests(self, agent_id: str) -> list[CoordinationRequest]:
        """Get pending requests for a specific agent."""
        with self._lock:
            pending = []
            for request in self.coordination_requests.values():
                if (
                    request.to_agent == agent_id
                    and not request.response_received
                    and request.status == "pending"
                ):
                    pending.append(request)
            return pending

    def get_request_stats(self) -> dict[str, Any]:
        """Get coordination request statistics."""
        with self._lock:
            total_requests = len(self.coordination_requests)
            pending_requests = sum(
                1 for r in self.coordination_requests.values() if r.status == "pending"
            )
            completed_requests = sum(
                1 for r in self.coordination_requests.values() if r.response_received
            )

            return {
                "total_requests": total_requests,
                "pending_requests": pending_requests,
                "completed_requests": completed_requests,
                "completion_rate": completed_requests / total_requests if total_requests > 0 else 0,
            }

    def _cleanup_old_requests(self) -> int:
        """Clean up old completed requests to prevent memory accumulation."""
        current_time = time.time()
        cleaned_count = 0

        # Remove completed requests older than cleanup_interval
        to_remove = []
        for request_id, request in self.coordination_requests.items():
            if (
                request.response_received
                and current_time - request.timestamp > self.cleanup_interval
            ):
                to_remove.append(request_id)

        for request_id in to_remove:
            del self.coordination_requests[request_id]
            cleaned_count += 1

        self.last_cleanup = current_time

        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old coordination requests")

        return cleaned_count

    def validate_coordination_protocol(self, from_agent: str, to_agent: str) -> dict[str, Any]:
        """Validate coordination protocol compliance."""
        validation_result = {"valid": True, "issues": [], "warnings": []}

        # Check for recent requests to same agent
        with self._lock:
            recent_requests = []
            current_time = time.time()

            for request in self.coordination_requests.values():
                if (
                    request.from_agent == from_agent
                    and request.to_agent == to_agent
                    and current_time - request.timestamp < 60
                ):  # Last minute
                    recent_requests.append(request)

            # Warn if too many recent requests
            if len(recent_requests) > 5:
                validation_result["warnings"].append(
                    f"High frequency of requests to {to_agent} in last minute"
                )

            # Check for unresponded requests
            unresponded = [r for r in recent_requests if not r.response_received]
            if unresponded:
                validation_result["warnings"].append(
                    f"{len(unresponded)} unresponded requests to {to_agent}"
                )

        return validation_result


class EnhancedCoordinationValidator:
    """Enhanced coordination validation for messaging system."""

    def __init__(self):
        """Initialize enhanced coordination validator."""
        self.tracker = CoordinationTracker()
        logger.info("EnhancedCoordinationValidator initialized")

    def validate_request(self, from_agent: str, to_agent: str, message: str) -> dict[str, Any]:
        """Validate coordination request before sending."""
        validation_result = {"valid": True, "issues": [], "warnings": [], "request_id": None}

        # Basic validation
        if not from_agent or not to_agent:
            validation_result["valid"] = False
            validation_result["issues"].append("Missing agent identifiers")
            return validation_result

        if not message or len(message.strip()) == 0:
            validation_result["valid"] = False
            validation_result["issues"].append("Empty message content")
            return validation_result

        # Protocol validation
        protocol_result = self.tracker.validate_coordination_protocol(from_agent, to_agent)
        validation_result["warnings"].extend(protocol_result["warnings"])

        if not protocol_result["valid"]:
            validation_result["valid"] = False
            validation_result["issues"].extend(protocol_result["issues"])

        # Track request if valid
        if validation_result["valid"]:
            request_id = self.tracker.track_request(from_agent, to_agent, message)
            validation_result["request_id"] = request_id

        return validation_result

    def mark_response(self, request_id: str) -> bool:
        """Mark response as received for a coordination request."""
        return self.tracker.mark_response_received(request_id)

    def get_stats(self) -> dict[str, Any]:
        """Get coordination validation statistics."""
        return self.tracker.get_request_stats()


# Global instance for enhanced validation integration
_coordination_tracker = None
_enhanced_validator = None


def get_coordination_tracker() -> CoordinationTracker:
    """Get global coordination tracker instance."""
    global _coordination_tracker
    if _coordination_tracker is None:
        _coordination_tracker = CoordinationTracker()
    return _coordination_tracker


def get_enhanced_validator() -> EnhancedCoordinationValidator:
    """Get global enhanced coordination validator instance."""
    global _enhanced_validator
    if _enhanced_validator is None:
        _enhanced_validator = EnhancedCoordinationValidator()
    return _enhanced_validator


# Export functions for enhanced validation integration
def validate_coordination_request(from_agent: str, to_agent: str, message: str) -> dict[str, Any]:
    """Validate coordination request (export function)."""
    validator = get_enhanced_validator()
    return validator.validate_request(from_agent, to_agent, message)


def mark_coordination_response(request_id: str) -> bool:
    """Mark coordination response (export function)."""
    validator = get_enhanced_validator()
    return validator.mark_response(request_id)


def get_coordination_stats() -> dict[str, Any]:
    """Get coordination statistics (export function)."""
    validator = get_enhanced_validator()
    return validator.get_stats()


logger.info("CoordinationTracker module loaded successfully")
