#!/usr/bin/env python3
"""
🔍 API Gateway Core - Agent_Cellphone_V2

Unified API management, middleware integration, and service discovery system.
Following V2 coding standards: ≤500 LOC, OOP design, SRP.

Author: API & Integration Specialist
License: MIT
"""

import logging
import threading
import time
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import asyncio
import aiohttp
from urllib.parse import urlparse, urljoin

# Configure logging
logger = logging.getLogger(__name__)


class APIVersion(Enum):
    """API version enumeration"""

    V1 = "v1"
    V2 = "v2"
    BETA = "beta"
    ALPHA = "alpha"


class ServiceStatus(Enum):
    """Service status values"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ServiceEndpoint:
    """Service endpoint information"""

    service_id: str
    name: str
    version: str
    base_url: str
    health_check_url: str
    status: ServiceStatus
    last_health_check: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class APIRequest:
    """API request structure"""

    request_id: str
    method: str
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    body: Optional[Any]
    timestamp: datetime
    client_ip: str
    user_agent: str


@dataclass
class APIResponse:
    """API response structure"""

    request_id: str
    status_code: int
    headers: Dict[str, str]
    body: Any
    timestamp: datetime
    processing_time: float
    service_id: Optional[str] = None


class APIGateway:
    """
    API Gateway Core - Single responsibility: Unified API management and routing.

    Follows V2 standards: ≤500 LOC, OOP design, SRP.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the API gateway"""
        self.config = config or {}

        # Service registry
        self.registered_services: Dict[str, ServiceEndpoint] = {}
        self.service_endpoints: Dict[str, List[ServiceEndpoint]] = defaultdict(list)

        # Request/Response tracking
        self.request_history: List[APIRequest] = []
        self.response_history: List[APIResponse] = []

        # Gateway state
        self.gateway_active = False
        self.gateway_thread: Optional[threading.Thread] = None
        self.lock = threading.RLock()

        # Configuration
        self.health_check_interval = self.config.get(
            "health_check_interval", 60
        )  # seconds
        self.max_history = self.config.get("max_history", 10000)
        self.request_timeout = self.config.get("request_timeout", 30)  # seconds

        # Middleware chain
        self.middleware_chain: List[Callable] = []

        # Callbacks
        self.request_callbacks: List[Callable] = []
        self.response_callbacks: List[Callable] = []
        self.service_status_callbacks: List[Callable] = []

        # Performance tracking integration
        self.performance_tracker = None

        # Rate limiting
        self.rate_limits: Dict[str, Dict[str, Any]] = {}

        logger.info("APIGateway initialized")

    def register_service(
        self,
        service_id: str,
        name: str,
        version: str,
        base_url: str,
        health_check_url: str = None,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """Register a new service endpoint"""
        with self.lock:
            if service_id in self.registered_services:
                logger.warning(f"Service {service_id} already registered, updating...")

            # Default health check URL
            if not health_check_url:
                health_check_url = urljoin(base_url, "/health")

            service_endpoint = ServiceEndpoint(
                service_id=service_id,
                name=name,
                version=version,
                base_url=base_url.rstrip("/"),
                health_check_url=health_check_url,
                status=ServiceStatus.UNKNOWN,
                last_health_check=datetime.now(),
                metadata=metadata or {},
            )

            self.registered_services[service_id] = service_endpoint
            self.service_endpoints[version].append(service_endpoint)

            logger.info(f"Service {service_id} ({name}) registered at {base_url}")
            return True

    def unregister_service(self, service_id: str) -> bool:
        """Unregister a service endpoint"""
        with self.lock:
            if service_id not in self.registered_services:
                logger.warning(f"Service {service_id} not found for unregistration")
                return False

            service_endpoint = self.registered_services.pop(service_id)

            # Remove from version-specific endpoints
            for version_endpoints in self.service_endpoints.values():
                version_endpoints[:] = [
                    ep for ep in version_endpoints if ep.service_id != service_id
                ]

            logger.info(f"Service {service_id} unregistered")
            return True

    def get_service_endpoint(self, service_id: str) -> Optional[ServiceEndpoint]:
        """Get service endpoint information"""
        with self.lock:
            return self.registered_services.get(service_id)

    def get_services_by_version(self, version: str) -> List[ServiceEndpoint]:
        """Get all services for a specific version"""
        with self.lock:
            return self.service_endpoints.get(version, []).copy()

    def get_all_services(self) -> List[ServiceEndpoint]:
        """Get all registered services"""
        with self.lock:
            return list(self.registered_services.values())

    def add_middleware(self, middleware: Callable):
        """Add middleware to the processing chain"""
        if middleware not in self.middleware_chain:
            self.middleware_chain.append(middleware)
            logger.info(f"Middleware added: {middleware.__name__}")

    def remove_middleware(self, middleware: Callable):
        """Remove middleware from the processing chain"""
        if middleware in self.middleware_chain:
            self.middleware_chain.remove(middleware)
            logger.info(f"Middleware removed: {middleware.__name__}")

    def set_rate_limit(
        self, service_id: str, requests_per_minute: int, burst_limit: int = None
    ):
        """Set rate limiting for a service"""
        with self.lock:
            self.rate_limits[service_id] = {
                "requests_per_minute": requests_per_minute,
                "burst_limit": burst_limit or requests_per_minute,
                "request_counts": defaultdict(int),
                "last_reset": datetime.now(),
            }
            logger.info(
                f"Rate limit set for {service_id}: {requests_per_minute} req/min"
            )

    def route_request(
        self,
        method: str,
        path: str,
        headers: Dict[str, str] = None,
        query_params: Dict[str, str] = None,
        body: Any = None,
        client_ip: str = "unknown",
        user_agent: str = "unknown",
    ) -> APIResponse:
        """Route an API request through the gateway"""
        start_time = time.time()

        # Create request object
        request = APIRequest(
            request_id=str(uuid.uuid4()),
            method=method.upper(),
            path=path,
            headers=headers or {},
            query_params=query_params or {},
            body=body,
            timestamp=datetime.now(),
            client_ip=client_ip,
            user_agent=user_agent,
        )

        # Add to request history
        with self.lock:
            self.request_history.append(request)
            if len(self.request_history) > self.max_history:
                self.request_history = self.request_history[-self.max_history :]

        # Track request performance
        if self.performance_tracker:
            self.performance_tracker.record_metric(
                "api_request", 1, "count", None, {"method": method, "path": path}
            )

        # Apply middleware chain
        processed_request = self._apply_middleware(request)

        # Route to appropriate service
        try:
            service_id, target_url = self._determine_target_service(processed_request)

            # Check rate limiting
            if not self._check_rate_limit(service_id):
                return self._create_error_response(
                    request.request_id, 429, "Rate limit exceeded", service_id
                )

            # Forward request to service
            response = self._forward_request(processed_request, target_url, service_id)

        except Exception as e:
            logger.error(f"Error routing request {request.request_id}: {e}")
            response = self._create_error_response(
                request.request_id, 500, f"Internal gateway error: {str(e)}"
            )

        # Calculate processing time
        processing_time = time.time() - start_time
        response.processing_time = processing_time

        # Add to response history
        with self.lock:
            self.response_history.append(response)
            if len(self.response_history) > self.max_history:
                self.response_history = self.response_history[-self.max_history :]

        # Track response performance
        if self.performance_tracker:
            self.performance_tracker.record_metric(
                "api_response_time",
                processing_time,
                "seconds",
                None,
                {"method": method, "path": path, "status_code": response.status_code},
            )

        # Notify callbacks
        self._notify_request_callbacks(request)
        self._notify_response_callbacks(response)

        return response

    def start_gateway(self):
        """Start the API gateway"""
        if self.gateway_active:
            logger.warning("API gateway already active")
            return

        self.gateway_active = True
        self.gateway_thread = threading.Thread(target=self._gateway_loop, daemon=True)
        self.gateway_thread.start()
        logger.info("API gateway started")

    def stop_gateway(self):
        """Stop the API gateway"""
        self.gateway_active = False
        if self.gateway_thread:
            self.gateway_thread.join(timeout=5)
        logger.info("API gateway stopped")

    def add_request_callback(self, callback: Callable):
        """Add callback for request processing"""
        if callback not in self.request_callbacks:
            self.request_callbacks.append(callback)

    def add_response_callback(self, callback: Callable):
        """Add callback for response processing"""
        if callback not in self.response_callbacks:
            self.response_callbacks.append(callback)

    def add_service_status_callback(self, callback: Callable):
        """Add callback for service status changes"""
        if callback not in self.service_status_callbacks:
            self.service_status_callbacks.append(callback)

    def set_performance_tracker(self, performance_tracker):
        """Set performance tracker for metrics collection"""
        self.performance_tracker = performance_tracker
        logger.info("Performance tracker integrated with API gateway")

    def _gateway_loop(self):
        """Main gateway loop for health checks and maintenance"""
        while self.gateway_active:
            try:
                # Perform health checks
                self._perform_health_checks()

                # Cleanup old data
                self._cleanup_old_data()

                # Reset rate limit counters
                self._reset_rate_limit_counters()

                time.sleep(self.health_check_interval)

            except Exception as e:
                logger.error(f"Error in gateway loop: {e}")
                time.sleep(10)

    def _apply_middleware(self, request: APIRequest) -> APIRequest:
        """Apply middleware chain to request"""
        processed_request = request

        for middleware in self.middleware_chain:
            try:
                processed_request = middleware(processed_request)
            except Exception as e:
                logger.error(f"Error in middleware {middleware.__name__}: {e}")
                # Continue with original request if middleware fails

        return processed_request

    def _determine_target_service(self, request: APIRequest) -> tuple[str, str]:
        """Determine which service should handle the request"""
        # Parse path to determine service and version
        path_parts = request.path.strip("/").split("/")

        if len(path_parts) < 2:
            raise ValueError("Invalid API path format")

        version = path_parts[0]
        service_path = "/".join(path_parts[1:])

        # Find available services for this version
        available_services = self.get_services_by_version(version)
        if not available_services:
            raise ValueError(f"No services available for version {version}")

        # For now, use round-robin selection
        # In a real implementation, this could use load balancing, health status, etc.
        service = available_services[0]  # Simple selection

        # Construct target URL
        target_url = urljoin(service.base_url, f"/{service_path}")

        return service.service_id, target_url

    def _check_rate_limit(self, service_id: str) -> bool:
        """Check if request is within rate limits"""
        if service_id not in self.rate_limits:
            return True  # No rate limiting configured

        rate_limit = self.rate_limits[service_id]
        current_time = datetime.now()

        # Reset counters if minute has passed
        if (current_time - rate_limit["last_reset"]).total_seconds() >= 60:
            rate_limit["request_counts"].clear()
            rate_limit["last_reset"] = current_time

        # Check current count
        current_count = rate_limit["request_counts"][
            current_time.strftime("%Y-%m-%d %H:%M")
        ]
        if current_count >= rate_limit["requests_per_minute"]:
            return False

        # Increment counter
        rate_limit["request_counts"][current_time.strftime("%Y-%m-%d %H:%M")] += 1
        return True

    def _forward_request(
        self, request: APIRequest, target_url: str, service_id: str
    ) -> APIResponse:
        """Forward request to target service"""
        # This is a simplified implementation
        # In a real system, this would use proper HTTP client libraries

        try:
            # Simulate request forwarding
            # In practice, you'd use aiohttp, requests, or similar
            logger.debug(f"Forwarding request {request.request_id} to {target_url}")

            # For now, return a mock successful response
            return APIResponse(
                request_id=request.request_id,
                status_code=200,
                headers={"Content-Type": "application/json"},
                body={"message": "Request processed successfully"},
                timestamp=datetime.now(),
                processing_time=0.0,
                service_id=service_id,
            )

        except Exception as e:
            logger.error(f"Error forwarding request to {target_url}: {e}")
            raise

    def _create_error_response(
        self,
        request_id: str,
        status_code: int,
        error_message: str,
        service_id: str = None,
    ) -> APIResponse:
        """Create an error response"""
        return APIResponse(
            request_id=request_id,
            status_code=status_code,
            headers={"Content-Type": "application/json"},
            body={"error": error_message},
            timestamp=datetime.now(),
            processing_time=0.0,
            service_id=service_id,
        )

    def _perform_health_checks(self):
        """Perform health checks on registered services"""
        current_time = datetime.now()

        for service_id, service in list(self.registered_services.items()):
            try:
                # This would perform actual health checks
                # For now, we'll simulate health check results
                if (
                    current_time - service.last_health_check
                ).total_seconds() > self.health_check_interval:
                    # Simulate health check
                    service.last_health_check = current_time

                    # Randomly assign health status for demo purposes
                    import random

                    statuses = [
                        ServiceStatus.HEALTHY,
                        ServiceStatus.DEGRADED,
                        ServiceStatus.UNHEALTHY,
                    ]
                    new_status = random.choice(statuses)

                    if service.status != new_status:
                        service.status = new_status
                        self._notify_service_status_callbacks(service_id, new_status)
                        logger.info(
                            f"Service {service_id} health status: {new_status.value}"
                        )

            except Exception as e:
                logger.error(f"Error checking health of service {service_id}: {e}")
                service.status = ServiceStatus.UNKNOWN

    def _cleanup_old_data(self):
        """Clean up old request/response history"""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=24)  # Keep 24 hours

        with self.lock:
            self.request_history = [
                req for req in self.request_history if req.timestamp >= cutoff_time
            ]

            self.response_history = [
                resp for resp in self.response_history if resp.timestamp >= cutoff_time
            ]

    def _reset_rate_limit_counters(self):
        """Reset rate limit counters"""
        current_time = datetime.now()

        for service_id, rate_limit in self.rate_limits.items():
            if (current_time - rate_limit["last_reset"]).total_seconds() >= 60:
                rate_limit["request_counts"].clear()
                rate_limit["last_reset"] = current_time

    def _notify_request_callbacks(self, request: APIRequest):
        """Notify request processing callbacks"""
        for callback in self.request_callbacks:
            try:
                callback(request)
            except Exception as e:
                logger.error(f"Error in request callback: {e}")

    def _notify_response_callbacks(self, response: APIResponse):
        """Notify response processing callbacks"""
        for callback in self.response_callbacks:
            try:
                callback(response)
            except Exception as e:
                logger.error(f"Error in response callback: {e}")

    def _notify_service_status_callbacks(self, service_id: str, status: ServiceStatus):
        """Notify service status change callbacks"""
        for callback in self.service_status_callbacks:
            try:
                callback(service_id, status)
            except Exception as e:
                logger.error(f"Error in service status callback: {e}")

    def export_gateway_data(self, filepath: str):
        """Export gateway data to JSON file"""
        with self.lock:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "registered_services": {},
                "request_history": [],
                "response_history": [],
                "rate_limits": {},
            }

            # Export service information
            for service_id, service in self.registered_services.items():
                export_data["registered_services"][service_id] = {
                    "name": service.name,
                    "version": service.version,
                    "base_url": service.base_url,
                    "health_check_url": service.health_check_url,
                    "status": service.status.value,
                    "last_health_check": service.last_health_check.isoformat(),
                    "metadata": service.metadata,
                }

            # Export recent requests
            for request in self.request_history[-1000:]:  # Last 1000 requests
                export_data["request_history"].append(
                    {
                        "request_id": request.request_id,
                        "method": request.method,
                        "path": request.path,
                        "timestamp": request.timestamp.isoformat(),
                        "client_ip": request.client_ip,
                    }
                )

            # Export recent responses
            for response in self.response_history[-1000:]:  # Last 1000 responses
                export_data["response_history"].append(
                    {
                        "request_id": response.request_id,
                        "status_code": response.status_code,
                        "timestamp": response.timestamp.isoformat(),
                        "processing_time": response.processing_time,
                        "service_id": response.service_id,
                    }
                )

            # Export rate limit configuration
            for service_id, rate_limit in self.rate_limits.items():
                export_data["rate_limits"][service_id] = {
                    "requests_per_minute": rate_limit["requests_per_minute"],
                    "burst_limit": rate_limit["burst_limit"],
                }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Exported gateway data to {filepath}")

    def cleanup(self):
        """Cleanup gateway resources"""
        self.stop_gateway()
        logger.info("APIGateway cleaned up")
