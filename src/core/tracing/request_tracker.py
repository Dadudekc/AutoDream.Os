# V3-004: Distributed Tracing Implementation - Request Tracker
# Agent-1: Architecture Foundation Specialist
#
# Request tracking functionality for V2_SWARM system

import logging
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from .jaeger_tracer import trace_manager


class RequestStatus(Enum):
    """Request status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class RequestInfo:
    """Request information structure."""

    request_id: str
    method: str
    path: str
    headers: dict[str, str]
    query_params: dict[str, Any]
    body: Any | None
    user_id: str | None
    agent_id: str | None
    timestamp: datetime
    status: RequestStatus
    duration: float | None = None
    error_message: str | None = None
    trace_id: str | None = None
    span_id: str | None = None


class RequestTracker:
    """Request tracking for distributed tracing."""

    def __init__(self):
        self.active_requests: dict[str, RequestInfo] = {}
        self.completed_requests: list[RequestInfo] = []
        self.tracer = trace_manager.get_tracer()
        self.logger = logging.getLogger(__name__)

    def start_request(
        self,
        method: str,
        path: str,
        headers: dict[str, str] = None,
        query_params: dict[str, Any] = None,
        body: Any = None,
        user_id: str = None,
        agent_id: str = None,
    ) -> str:
        """Start tracking a new request."""
        request_id = str(uuid.uuid4())

        request_info = RequestInfo(
            request_id=request_id,
            method=method,
            path=path,
            headers=headers or {},
            query_params=query_params or {},
            body=body,
            user_id=user_id,
            agent_id=agent_id,
            timestamp=datetime.utcnow(),
            status=RequestStatus.PENDING,
        )

        self.active_requests[request_id] = request_info

        # Create trace span for request
        with self.tracer.trace_span(
            f"{method} {path}",
            {
                "request.id": request_id,
                "http.method": method,
                "http.url": path,
                "user.id": user_id,
                "agent.id": agent_id,
            },
        ) as span:
            request_info.trace_id = self.tracer.get_trace_id()
            request_info.span_id = self.tracer.get_span_id()

            # Add request details to span
            self.tracer.add_span_tags(
                {
                    "request.headers": str(request_info.headers),
                    "request.query_params": str(request_info.query_params),
                }
            )

        self.logger.info(f"Started tracking request {request_id}: {method} {path}")
        return request_id

    def update_request_status(
        self, request_id: str, status: RequestStatus, error_message: str = None
    ) -> bool:
        """Update request status."""
        if request_id not in self.active_requests:
            self.logger.warning(f"Request {request_id} not found in active requests")
            return False

        request_info = self.active_requests[request_id]
        request_info.status = status

        if error_message:
            request_info.error_message = error_message

        # Update trace span
        with self.tracer.trace_span("request_status_update") as span:
            self.tracer.add_span_tags(
                {
                    "request.id": request_id,
                    "request.status": status.value,
                    "request.error": error_message or "",
                }
            )

        self.logger.info(f"Updated request {request_id} status to {status.value}")
        return True

    def complete_request(
        self,
        request_id: str,
        status: RequestStatus = RequestStatus.COMPLETED,
        error_message: str = None,
    ) -> bool:
        """Complete request tracking."""
        if request_id not in self.active_requests:
            self.logger.warning(f"Request {request_id} not found in active requests")
            return False

        request_info = self.active_requests[request_id]
        request_info.status = status
        request_info.duration = (datetime.utcnow() - request_info.timestamp).total_seconds()

        if error_message:
            request_info.error_message = error_message

        # Move to completed requests
        self.completed_requests.append(request_info)
        del self.active_requests[request_id]

        # Update trace span
        with self.tracer.trace_span("request_completion") as span:
            self.tracer.add_span_tags(
                {
                    "request.id": request_id,
                    "request.status": status.value,
                    "request.duration": request_info.duration,
                    "request.error": error_message or "",
                }
            )

        self.logger.info(f"Completed request {request_id} with status {status.value}")
        return True

    def get_request_info(self, request_id: str) -> RequestInfo | None:
        """Get request information."""
        return self.active_requests.get(request_id)

    def get_active_requests(self) -> list[RequestInfo]:
        """Get all active requests."""
        return list(self.active_requests.values())

    def get_completed_requests(self, limit: int = 100) -> list[RequestInfo]:
        """Get completed requests."""
        return self.completed_requests[-limit:]

    def get_requests_by_user(self, user_id: str) -> list[RequestInfo]:
        """Get requests by user ID."""
        user_requests = []

        # Check active requests
        for request in self.active_requests.values():
            if request.user_id == user_id:
                user_requests.append(request)

        # Check completed requests
        for request in self.completed_requests:
            if request.user_id == user_id:
                user_requests.append(request)

        return user_requests

    def get_requests_by_agent(self, agent_id: str) -> list[RequestInfo]:
        """Get requests by agent ID."""
        agent_requests = []

        # Check active requests
        for request in self.active_requests.values():
            if request.agent_id == agent_id:
                agent_requests.append(request)

        # Check completed requests
        for request in self.completed_requests:
            if request.agent_id == agent_id:
                agent_requests.append(request)

        return agent_requests

    def get_request_statistics(self) -> dict[str, Any]:
        """Get request statistics."""
        total_requests = len(self.active_requests) + len(self.completed_requests)
        active_count = len(self.active_requests)
        completed_count = len(self.completed_requests)

        # Calculate status distribution
        status_counts = {}
        for request in self.completed_requests:
            status = request.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        # Calculate average duration
        durations = [r.duration for r in self.completed_requests if r.duration is not None]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_requests": total_requests,
            "active_requests": active_count,
            "completed_requests": completed_count,
            "status_distribution": status_counts,
            "average_duration": avg_duration,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def cleanup_old_requests(self, max_age_hours: int = 24) -> int:
        """Clean up old completed requests."""
        cutoff_time = datetime.utcnow().timestamp() - (max_age_hours * 3600)

        original_count = len(self.completed_requests)
        self.completed_requests = [
            req for req in self.completed_requests if req.timestamp.timestamp() > cutoff_time
        ]

        cleaned_count = original_count - len(self.completed_requests)

        if cleaned_count > 0:
            self.logger.info(f"Cleaned up {cleaned_count} old requests")

        return cleaned_count

    def export_request_data(self) -> list[dict[str, Any]]:
        """Export request data for analysis."""
        export_data = []

        # Export active requests
        for request in self.active_requests.values():
            export_data.append(asdict(request))

        # Export recent completed requests
        for request in self.completed_requests[-1000:]:  # Last 1000 requests
            export_data.append(asdict(request))

        return export_data
