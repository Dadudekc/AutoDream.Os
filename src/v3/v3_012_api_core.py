#!/usr/bin/env python3
"""
V3-012: API Core Integration
============================

Core API integration functionality with V2 compliance.
Focuses on essential API operations and data structures.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class HTTPMethod(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class APIStatus(Enum):
    """API status."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    NETWORK_ERROR = "network_error"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"


@dataclass
class APIRequest:
    """API request structure."""
    request_id: str
    method: HTTPMethod
    url: str
    headers: Dict[str, str]
    data: Optional[Dict[str, Any]]
    timeout: int
    retry_count: int
    created_at: datetime


@dataclass
class APIResponse:
    """API response structure."""
    request_id: str
    status: APIStatus
    status_code: int
    data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    response_time_ms: float
    created_at: datetime


@dataclass
class APIConfig:
    """API configuration."""
    base_url: str
    timeout: int
    max_retries: int
    retry_delay: int
    headers: Dict[str, str]


class APIClient:
    """Core API client functionality."""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.request_history = []
        self.response_history = []
    
    def create_request(self, method: HTTPMethod, endpoint: str, 
                      data: Optional[Dict[str, Any]] = None, 
                      headers: Optional[Dict[str, str]] = None) -> APIRequest:
        """Create API request."""
        request_id = f"{method.value}_{int(datetime.now().timestamp())}"
        
        return APIRequest(
            request_id=request_id,
            method=method,
            url=f"{self.config.base_url}{endpoint}",
            headers={**self.config.headers, **(headers or {})},
            data=data,
            timeout=self.config.timeout,
            retry_count=0,
            created_at=datetime.now()
        )
    
    def create_response(self, request: APIRequest, status: APIStatus, 
                       status_code: int, data: Optional[Dict[str, Any]] = None,
                       error_message: Optional[str] = None, 
                       response_time_ms: float = 0.0) -> APIResponse:
        """Create API response."""
        return APIResponse(
            request_id=request.request_id,
            status=status,
            status_code=status_code,
            data=data,
            error_message=error_message,
            response_time_ms=response_time_ms,
            created_at=datetime.now()
        )
    
    def add_request(self, request: APIRequest):
        """Add request to history."""
        self.request_history.append(request)
    
    def add_response(self, response: APIResponse):
        """Add response to history."""
        self.response_history.append(response)
    
    def get_request_history(self) -> List[APIRequest]:
        """Get request history."""
        return self.request_history.copy()
    
    def get_response_history(self) -> List[APIResponse]:
        """Get response history."""
        return self.response_history.copy()
    
    def get_recent_requests(self, minutes: int = 5) -> List[APIRequest]:
        """Get recent requests."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            req for req in self.request_history 
            if req.created_at > cutoff_time
        ]
    
    def get_recent_responses(self, minutes: int = 5) -> List[APIResponse]:
        """Get recent responses."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            resp for resp in self.response_history 
            if resp.created_at > cutoff_time
        ]
    
    def get_success_rate(self) -> float:
        """Get success rate."""
        if not self.response_history:
            return 0.0
        
        successful = sum(1 for resp in self.response_history if resp.status == APIStatus.SUCCESS)
        return (successful / len(self.response_history)) * 100
    
    def get_average_response_time(self) -> float:
        """Get average response time."""
        if not self.response_history:
            return 0.0
        
        total_time = sum(resp.response_time_ms for resp in self.response_history)
        return total_time / len(self.response_history)
    
    def clear_history(self):
        """Clear request and response history."""
        self.request_history.clear()
        self.response_history.clear()


class APIFactory:
    """Factory for creating API configurations and clients."""
    
    @staticmethod
    def create_config(base_url: str, timeout: int = 30, 
                     max_retries: int = 3, retry_delay: int = 1) -> APIConfig:
        """Create API configuration."""
        return APIConfig(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "DreamOS-API-Client/1.0"
            }
        )
    
    @staticmethod
    def create_client(config: APIConfig) -> APIClient:
        """Create API client."""
        return APIClient(config)
    
    @staticmethod
    def create_rest_config(base_url: str) -> APIConfig:
        """Create REST API configuration."""
        return APIFactory.create_config(base_url, timeout=30, max_retries=3)
    
    @staticmethod
    def create_graphql_config(base_url: str) -> APIConfig:
        """Create GraphQL API configuration."""
        return APIFactory.create_config(base_url, timeout=60, max_retries=2)


def main():
    """Main execution function."""
    print("🔌 V3-012 API Core Integration - Testing...")
    
    # Create API configuration
    factory = APIFactory()
    config = factory.create_rest_config("https://api.dreamos.com")
    
    # Create API client
    client = APIClient(config)
    
    # Create sample requests
    get_request = client.create_request(HTTPMethod.GET, "/users")
    post_request = client.create_request(HTTPMethod.POST, "/users", {"name": "Test User"})
    
    # Add requests to history
    client.add_request(get_request)
    client.add_request(post_request)
    
    # Create sample responses
    success_response = client.create_response(
        get_request, APIStatus.SUCCESS, 200, {"users": []}, response_time_ms=150.5
    )
    error_response = client.create_response(
        post_request, APIStatus.ERROR, 400, error_message="Invalid data", response_time_ms=75.2
    )
    
    # Add responses to history
    client.add_response(success_response)
    client.add_response(error_response)
    
    # Get statistics
    success_rate = client.get_success_rate()
    avg_response_time = client.get_average_response_time()
    recent_requests = client.get_recent_requests(5)
    recent_responses = client.get_recent_responses(5)
    
    print(f"\n📊 API Statistics:")
    print(f"   Success Rate: {success_rate:.1f}%")
    print(f"   Average Response Time: {avg_response_time:.2f}ms")
    print(f"   Recent Requests: {len(recent_requests)}")
    print(f"   Recent Responses: {len(recent_responses)}")
    
    print("\n✅ V3-012 API Core Integration completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

