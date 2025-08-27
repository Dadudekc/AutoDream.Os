#!/usr/bin/env python3
"""
API Gateway Manager - V2 Modular Architecture
============================================

Unified API gateway management and routing system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import threading
import time
import json
import uuid
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import aiohttp
from urllib.parse import urlparse, urljoin

from ..types.api_types import (
    APIVersion, HTTPMethod, ServiceStatus, AuthenticationLevel, RateLimitType,
    ServiceEndpoint, APIRequest, APIResponse, RouteDefinition, RateLimitInfo
)

logger = logging.getLogger(__name__)


class APIGatewayManager:
    """
    API Gateway Manager - Single responsibility: Manage API gateway operations
    
    Handles all API gateway operations including:
    - Service registration and discovery
    - Request routing and forwarding
    - Authentication and authorization
    - Rate limiting and throttling
    - Health monitoring and load balancing
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the API gateway manager"""
        self.logger = logging.getLogger(f"{__name__}.APIGatewayManager")
        
        # Configuration
        self.config = config or {}
        
        # Service registry
        self.registered_services: Dict[str, ServiceEndpoint] = {}
        self.service_endpoints: Dict[str, List[ServiceEndpoint]] = defaultdict(list)
        
        # Route registry
        self.routes: Dict[str, RouteDefinition] = {}
        self.route_patterns: List[str] = []
        
        # Request/Response tracking
        self.request_history: List[APIRequest] = []
        self.response_history: List[APIResponse] = []
        
        # Gateway state
        self.gateway_active = False
        self.gateway_thread: Optional[threading.Thread] = None
        self.lock = threading.RLock()
        
        # Configuration
        self.health_check_interval = self.config.get("health_check_interval", 60)
        self.max_history = self.config.get("max_history", 10000)
        self.request_timeout = self.config.get("request_timeout", 30)
        
        # Rate limiting
        self.rate_limits: Dict[str, RateLimitInfo] = {}
        
        # Performance tracking
        self.request_count = 0
        self.error_count = 0
        self.start_time = time.time()
        
        self.logger.info("✅ API Gateway Manager initialized successfully")

    def register_service(
        self,
        service_id: str,
        name: str,
        version: str,
        base_url: str,
        health_check_url: Optional[str] = None,
        metadata: Dict[str, Any] = None,
        authentication_required: bool = False,
        rate_limit: Optional[int] = None,
        timeout: float = 30.0
    ) -> bool:
        """Register a new service with the gateway"""
        try:
            with self.lock:
                if service_id in self.registered_services:
                    self.logger.warning(f"Service {service_id} already registered")
                    return False
                
                service = ServiceEndpoint(
                    service_id=service_id,
                    name=name,
                    version=version,
                    base_url=base_url,
                    health_check_url=health_check_url,
                    status=ServiceStatus.UNKNOWN,
                    metadata=metadata or {},
                    authentication_required=authentication_required,
                    rate_limit=rate_limit,
                    timeout=timeout
                )
                
                self.registered_services[service_id] = service
                self.service_endpoints[version].append(service)
                
                # Setup rate limiting if configured
                if rate_limit:
                    self.rate_limits[service_id] = RateLimitInfo(
                        service_id=service_id,
                        limit_type=RateLimitType.PER_MINUTE,
                        limit_value=rate_limit,
                        window_start=datetime.now()
                    )
                
                self.logger.info(f"Service registered: {service_id} ({name} v{version})")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to register service {service_id}: {e}")
            return False

    def unregister_service(self, service_id: str) -> bool:
        """Unregister a service from the gateway"""
        try:
            with self.lock:
                if service_id not in self.registered_services:
                    self.logger.warning(f"Service {service_id} not found")
                    return False
                
                service = self.registered_services[service_id]
                self.service_endpoints[service.version].remove(service)
                del self.registered_services[service_id]
                
                # Remove rate limiting
                if service_id in self.rate_limits:
                    del self.rate_limits[service_id]
                
                self.logger.info(f"Service unregistered: {service_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to unregister service {service_id}: {e}")
            return False

    def register_route(
        self,
        path: str,
        method: HTTPMethod,
        service_id: str,
        handler: Callable,
        requires_auth: bool = False,
        auth_level: AuthenticationLevel = AuthenticationLevel.NONE,
        rate_limit: Optional[int] = None,
        timeout: float = 30.0
    ) -> bool:
        """Register a new route with the gateway"""
        try:
            with self.lock:
                route_key = f"{method.value}:{path}"
                
                if route_key in self.routes:
                    self.logger.warning(f"Route {route_key} already registered")
                    return False
                
                route = RouteDefinition(
                    path=path,
                    method=method,
                    service_id=service_id,
                    handler=handler,
                    requires_auth=requires_auth,
                    auth_level=auth_level,
                    rate_limit=rate_limit,
                    timeout=timeout
                )
                
                self.routes[route_key] = route
                self.route_patterns.append(path)
                
                self.logger.info(f"Route registered: {route_key} -> {service_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to register route {path}: {e}")
            return False

    def route_request(self, request: APIRequest) -> APIResponse:
        """Route a request through the gateway"""
        try:
            self.request_count += 1
            start_time = time.time()
            
            # Find matching route
            route_key = f"{request.method.value}:{request.path}"
            route = self.routes.get(route_key)
            
            if not route:
                return self._create_error_response(
                    request.request_id, "Route not found", 404
                )
            
            # Check authentication if required
            if route.requires_auth:
                auth_result = self._validate_authentication(request, route.auth_level)
                if not auth_result:
                    return self._create_error_response(
                        request.request_id, "Authentication required", 401
                    )
            
            # Check rate limiting
            if not self._check_rate_limit(route.service_id):
                return self._create_error_response(
                    request.request_id, "Rate limit exceeded", 429
                )
            
            # Execute handler
            try:
                result = route.handler(request)
                execution_time = time.time() - start_time
                
                # Create successful response
                response = APIResponse(
                    request_id=request.request_id,
                    status_code=200,
                    headers={"Content-Type": "application/json"},
                    body=result,
                    processing_time=execution_time,
                    service_id=route.service_id
                )
                
                self.logger.info(f"Request routed successfully: {route_key} ({execution_time:.3f}s)")
                return response
                
            except Exception as e:
                self.error_count += 1
                self.logger.error(f"Handler execution error: {e}")
                return self._create_error_response(
                    request.request_id, f"Internal error: {str(e)}", 500
                )
                
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Request routing error: {e}")
            return self._create_error_response(
                request.request_id, f"Gateway error: {str(e)}", 500
            )

    def _validate_authentication(self, request: APIRequest, auth_level: AuthenticationLevel) -> bool:
        """Validate authentication for the request"""
        try:
            if auth_level == AuthenticationLevel.NONE:
                return True
            
            if not request.authentication_token:
                return False
            
            # Basic token validation (in production, implement proper JWT/OAuth validation)
            if auth_level == AuthenticationLevel.TOKEN:
                return len(request.authentication_token) > 10
            
            if auth_level == AuthenticationLevel.JWT:
                # Implement JWT validation
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Authentication validation error: {e}")
            return False

    def _check_rate_limit(self, service_id: str) -> bool:
        """Check if request is within rate limits"""
        try:
            if service_id not in self.rate_limits:
                return True
            
            rate_limit = self.rate_limits[service_id]
            current_time = datetime.now()
            
            # Reset counters if window has passed
            if rate_limit.window_start:
                window_duration = timedelta(minutes=1)  # Default to per-minute
                if current_time - rate_limit.window_start >= window_duration:
                    rate_limit.current_count = 0
                    rate_limit.window_start = current_time
            
            # Check current count
            if rate_limit.is_exceeded():
                return False
            
            # Increment counter
            rate_limit.current_count += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Rate limit check error: {e}")
            return True  # Allow request if rate limiting fails

    def _create_error_response(self, request_id: str, message: str, status_code: int) -> APIResponse:
        """Create an error response"""
        return APIResponse(
            request_id=request_id,
            status_code=status_code,
            headers={"Content-Type": "application/json"},
            body={"error": message, "status_code": status_code},
            error_message=message
        )

    def get_service(self, service_id: str) -> Optional[ServiceEndpoint]:
        """Get a specific service"""
        return self.registered_services.get(service_id)

    def get_services_by_version(self, version: str) -> List[ServiceEndpoint]:
        """Get all services for a specific version"""
        return self.service_endpoints.get(version, [])

    def get_all_services(self) -> List[ServiceEndpoint]:
        """Get all registered services"""
        return list(self.registered_services.values())

    def get_route(self, path: str, method: HTTPMethod) -> Optional[RouteDefinition]:
        """Get a specific route"""
        route_key = f"{method.value}:{path}"
        return self.routes.get(route_key)

    def get_all_routes(self) -> List[RouteDefinition]:
        """Get all registered routes"""
        return list(self.routes.values())

    def get_gateway_status(self) -> Dict[str, Any]:
        """Get gateway status and statistics"""
        try:
            uptime = time.time() - self.start_time
            
            return {
                "gateway_active": self.gateway_active,
                "uptime_seconds": uptime,
                "total_requests": self.request_count,
                "total_errors": self.error_count,
                "success_rate": (self.request_count - self.error_count) / self.request_count if self.request_count > 0 else 0.0,
                "registered_services": len(self.registered_services),
                "registered_routes": len(self.routes),
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get gateway status: {e}")
            return {"error": str(e)}

    def start_gateway(self):
        """Start the API gateway"""
        try:
            if self.gateway_active:
                self.logger.info("Gateway already active")
                return
            
            self.gateway_active = True
            
            # Start health monitoring thread
            self.gateway_thread = threading.Thread(target=self._health_monitoring_loop, daemon=True)
            self.gateway_thread.start()
            
            self.logger.info("✅ API Gateway started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start gateway: {e}")

    def stop_gateway(self):
        """Stop the API gateway"""
        try:
            self.gateway_active = False
            
            if self.gateway_thread:
                self.gateway_thread.join(timeout=5.0)
            
            self.logger.info("✅ API Gateway stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop gateway: {e}")

    def _health_monitoring_loop(self):
        """Health monitoring loop for registered services"""
        while self.gateway_active:
            try:
                self._check_service_health()
                time.sleep(self.health_check_interval)
                
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(5)

    def _check_service_health(self):
        """Check health of all registered services"""
        try:
            for service_id, service in self.registered_services.items():
                if service.health_check_url:
                    # In production, implement actual health check HTTP calls
                    # For now, just update timestamp
                    service.last_health_check = datetime.now()
                    service.status = ServiceStatus.HEALTHY
                    
        except Exception as e:
            self.logger.error(f"Service health check error: {e}")

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.stop_gateway()
            self.logger.info("✅ API Gateway Manager cleanup completed")
        except Exception as e:
            self.logger.error(f"API Gateway Manager cleanup failed: {e}")


