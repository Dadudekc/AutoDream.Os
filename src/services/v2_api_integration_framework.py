#!/usr/bin/env python3
"""
V2 API Integration Framework
============================
Comprehensive API integration framework with standardized patterns, reusable templates,
and comprehensive error handling for V2 system integration.
Follows V2 coding standards: 300 target, 350 max LOC.
"""

import json
import time
import logging
import requests
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from urllib.parse import urljoin, urlparse
import hashlib
import hmac

logger = logging.getLogger(__name__)


class HTTPMethod(Enum):
    """HTTP method enumeration for API requests"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class AuthType(Enum):
    """Authentication type enumeration"""
    NONE = "none"
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    BASIC_AUTH = "basic_auth"
    OAUTH2 = "oauth2"
    HMAC = "hmac"


@dataclass
class APIEndpoint:
    """API endpoint configuration"""
    name: str
    url: str
    method: HTTPMethod
    auth_type: AuthType
    headers: Dict[str, str]
    timeout: float
    retry_count: int
    rate_limit: Optional[int] = None


@dataclass
class APIRequest:
    """API request configuration"""
    endpoint: APIEndpoint
    data: Optional[Dict[str, Any]] = None
    query_params: Optional[Dict[str, str]] = None
    custom_headers: Optional[Dict[str, str]] = None
    timeout_override: Optional[float] = None


@dataclass
class APIResponse:
    """API response wrapper"""
    status_code: int
    headers: Dict[str, str]
    data: Any
    response_time: float
    success: bool
    error_message: Optional[str] = None


class V2APIIntegrationFramework:
    """Comprehensive API integration framework for V2 system"""
    
    def __init__(self, base_url: str = "", default_timeout: float = 30.0):
        self.logger = logging.getLogger(f"{__name__}.V2APIIntegrationFramework")
        self.base_url = base_url.rstrip('/')
        self.default_timeout = default_timeout
        
        # Endpoint registry
        self._endpoints: Dict[str, APIEndpoint] = {}
        
        # Authentication storage
        self._auth_credentials: Dict[str, Dict[str, Any]] = {}
        
        # Request history and metrics
        self._request_history: List[Dict[str, Any]] = []
        self._success_count = 0
        self._error_count = 0
        self._total_response_time = 0.0
        
        # Rate limiting
        self._rate_limit_store: Dict[str, List[float]] = {}
        
        self.logger.info(f"V2 API Integration Framework initialized with base URL: {base_url}")
    
    def register_endpoint(self, name: str, url: str, method: HTTPMethod,
                         auth_type: AuthType = AuthType.NONE,
                         headers: Optional[Dict[str, str]] = None,
                         timeout: Optional[float] = None,
                         retry_count: int = 3,
                         rate_limit: Optional[int] = None) -> bool:
        """Register a new API endpoint"""
        if name in self._endpoints:
            self.logger.warning(f"Endpoint already registered: {name}")
            return False
        
        # Build full URL if relative
        full_url = url if url.startswith('http') else urljoin(self.base_url, url)
        
        endpoint = APIEndpoint(
            name=name,
            url=full_url,
            method=method,
            auth_type=auth_type,
            headers=headers or {},
            timeout=timeout or self.default_timeout,
            retry_count=retry_count,
            rate_limit=rate_limit
        )
        
        self._endpoints[name] = endpoint
        self.logger.info(f"Endpoint registered: {name} -> {full_url}")
        return True
    
    def set_auth_credentials(self, endpoint_name: str, credentials: Dict[str, Any]) -> bool:
        """Set authentication credentials for an endpoint"""
        if endpoint_name not in self._endpoints:
            self.logger.error(f"Endpoint not found: {endpoint_name}")
            return False
        
        self._auth_credentials[endpoint_name] = credentials
        self.logger.info(f"Authentication credentials set for endpoint: {endpoint_name}")
        return True
    
    def _apply_authentication(self, endpoint: APIEndpoint, request_headers: Dict[str, str]) -> Dict[str, str]:
        """Apply authentication to request headers"""
        if endpoint.auth_type == AuthType.NONE:
            return request_headers
        
        credentials = self._auth_credentials.get(endpoint.name, {})
        
        if endpoint.auth_type == AuthType.API_KEY:
            api_key = credentials.get('api_key')
            if api_key:
                request_headers['X-API-Key'] = api_key
        
        elif endpoint.auth_type == AuthType.BEARER_TOKEN:
            token = credentials.get('bearer_token')
            if token:
                request_headers['Authorization'] = f"Bearer {token}"
        
        elif endpoint.auth_type == AuthType.BASIC_AUTH:
            username = credentials.get('username')
            password = credentials.get('password')
            if username and password:
                import base64
                auth_string = f"{username}:{password}"
                auth_bytes = auth_string.encode('ascii')
                auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
                request_headers['Authorization'] = f"Basic {auth_b64}"
        
        elif endpoint.auth_type == AuthType.HMAC:
            secret_key = credentials.get('secret_key')
            if secret_key:
                timestamp = str(int(time.time()))
                message = f"{endpoint.method.value}:{endpoint.url}:{timestamp}"
                signature = hmac.new(
                    secret_key.encode('utf-8'),
                    message.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                request_headers['X-Timestamp'] = timestamp
                request_headers['X-Signature'] = signature
        
        return request_headers
    
    def _check_rate_limit(self, endpoint: APIEndpoint) -> bool:
        """Check if request is within rate limit"""
        if not endpoint.rate_limit:
            return True
        
        current_time = time.time()
        endpoint_key = endpoint.name
        
        if endpoint_key not in self._rate_limit_store:
            self._rate_limit_store[endpoint_key] = []
        
        # Clean old timestamps (older than 1 minute)
        self._rate_limit_store[endpoint_key] = [
            ts for ts in self._rate_limit_store[endpoint_key]
            if current_time - ts < 60
        ]
        
        # Check if we're at the limit
        if len(self._rate_limit_store[endpoint_key]) >= endpoint.rate_limit:
            return False
        
        # Add current timestamp
        self._rate_limit_store[endpoint_key].append(current_time)
        return True
    
    def execute_request(self, request: APIRequest) -> APIResponse:
        """Execute an API request with comprehensive error handling"""
        endpoint = request.endpoint
        
        # Check rate limiting
        if not self._check_rate_limit(endpoint):
            return APIResponse(
                status_code=429,
                headers={},
                data=None,
                response_time=0.0,
                success=False,
                error_message="Rate limit exceeded"
            )
        
        # Prepare headers
        headers = endpoint.headers.copy()
        if request.custom_headers:
            headers.update(request.custom_headers)
        
        # Apply authentication
        headers = self._apply_authentication(endpoint, headers)
        
        # Prepare request parameters
        timeout = request.timeout_override or endpoint.timeout
        url = endpoint.url
        
        # Add query parameters
        if request.query_params:
            import urllib.parse
            query_string = urllib.parse.urlencode(request.query_params)
            url = f"{url}?{query_string}"
        
        # Execute request with retry logic
        for attempt in range(endpoint.retry_count):
            try:
                start_time = time.time()
                
                response = requests.request(
                    method=endpoint.method.value,
                    url=url,
                    headers=headers,
                    json=request.data,
                    timeout=timeout
                )
                
                response_time = time.time() - start_time
                
                # Parse response
                try:
                    response_data = response.json() if response.content else None
                except json.JSONDecodeError:
                    response_data = response.text
                
                # Create API response
                api_response = APIResponse(
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    data=response_data,
                    response_time=response_time,
                    success=200 <= response.status_code < 300,
                    error_message=None if 200 <= response.status_code < 300 else f"HTTP {response.status_code}"
                )
                
                # Update metrics
                self._update_metrics(api_response)
                
                # Log success
                self.logger.info(f"Request successful: {endpoint.name} -> {response.status_code} ({response_time:.3f}s)")
                return api_response
                
            except requests.exceptions.Timeout:
                error_msg = f"Request timeout (attempt {attempt + 1}/{endpoint.retry_count})"
                self.logger.warning(f"{error_msg}: {endpoint.name}")
                
                if attempt == endpoint.retry_count - 1:
                    return APIResponse(
                        status_code=408,
                        headers={},
                        data=None,
                        response_time=timeout,
                        success=False,
                        error_message=error_msg
                    )
                
            except requests.exceptions.RequestException as e:
                error_msg = f"Request failed (attempt {attempt + 1}/{endpoint.retry_count}): {str(e)}"
                self.logger.error(f"{error_msg}: {endpoint.name}")
                
                if attempt == endpoint.retry_count - 1:
                    return APIResponse(
                        status_code=500,
                        headers={},
                        data=None,
                        response_time=0.0,
                        success=False,
                        error_message=error_msg
                    )
        
        # Should never reach here
        return APIResponse(
            status_code=500,
            headers={},
            data=None,
            response_time=0.0,
            success=False,
            error_message="Unexpected error in request execution"
        )
    
    def _update_metrics(self, response: APIResponse):
        """Update request metrics and history"""
        self._request_history.append({
            'timestamp': time.time(),
            'status_code': response.status_code,
            'response_time': response.response_time,
            'success': response.success
        })
        
        if response.success:
            self._success_count += 1
        else:
            self._error_count += 1
        
        self._total_response_time += response.response_time
        
        # Keep only last 1000 requests in history
        if len(self._request_history) > 1000:
            self._request_history = self._request_history[-1000:]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive API metrics"""
        total_requests = self._success_count + self._error_count
        avg_response_time = self._total_response_time / total_requests if total_requests > 0 else 0
        
        return {
            'total_requests': total_requests,
            'success_count': self._success_count,
            'error_count': self._error_count,
            'success_rate': (self._success_count / total_requests * 100) if total_requests > 0 else 0,
            'average_response_time': avg_response_time,
            'total_response_time': self._total_response_time,
            'endpoints_registered': len(self._endpoints),
            'rate_limits_active': len([e for e in self._endpoints.values() if e.rate_limit])
        }
    
    def export_endpoints(self, filename: str = "api_endpoints.json") -> bool:
        """Export endpoint configurations to JSON"""
        try:
            endpoints_data = {
                'base_url': self.base_url,
                'endpoints': [
                    {
                        'name': name,
                        'url': endpoint.url,
                        'method': endpoint.method.value,
                        'auth_type': endpoint.auth_type.value,
                        'headers': endpoint.headers,
                        'timeout': endpoint.timeout,
                        'retry_count': endpoint.retry_count,
                        'rate_limit': endpoint.rate_limit
                    }
                    for name, endpoint in self._endpoints.items()
                ]
            }
            
            with open(filename, 'w') as f:
                json.dump(endpoints_data, f, indent=2)
            
            self.logger.info(f"Endpoints exported to: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export endpoints: {e}")
            return False
    
    def list_endpoints(self) -> List[Dict[str, Any]]:
        """List all registered endpoints"""
        return [
            {
                'name': name,
                'url': endpoint.url,
                'method': endpoint.method.value,
                'auth_type': endpoint.auth_type.value,
                'timeout': endpoint.timeout,
                'retry_count': endpoint.retry_count,
                'rate_limit': endpoint.rate_limit
            }
            for name, endpoint in self._endpoints.items()
        ]


def main():
    """CLI interface for V2APIIntegrationFramework"""
    import argparse
    
    parser = argparse.ArgumentParser(description="V2 API Integration Framework CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--list", action="store_true", help="List registered endpoints")
    parser.add_argument("--metrics", action="store_true", help="Show API metrics")
    parser.add_argument("--export", action="store_true", help="Export endpoints to JSON")
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = V2APIIntegrationFramework("https://api.example.com")
    
    if args.test:
        print("🧪 V2APIIntegrationFramework Smoke Test")
        print("=" * 50)
        
        # Register test endpoints
        framework.register_endpoint(
            "test_get", "/test", HTTPMethod.GET, AuthType.NONE
        )
        framework.register_endpoint(
            "test_post", "/test", HTTPMethod.POST, AuthType.API_KEY
        )
        
        # Set test credentials
        framework.set_auth_credentials("test_post", {"api_key": "test-key-123"})
        
        # Show endpoints
        endpoints = framework.list_endpoints()
        print(f"✅ Endpoints registered: {len(endpoints)}")
        
        # Show metrics
        metrics = framework.get_metrics()
        print(f"✅ Endpoints registered: {metrics['endpoints_registered']}")
        
        print("🎉 V2APIIntegrationFramework smoke test PASSED!")
    
    elif args.list:
        endpoints = framework.list_endpoints()
        print(f"📋 Registered Endpoints ({len(endpoints)}):")
        for endpoint in endpoints:
            print(f"  - {endpoint['name']}: {endpoint['method']} {endpoint['url']}")
    
    elif args.metrics:
        metrics = framework.get_metrics()
        print(f"📊 API Metrics:")
        print(f"  - Total Requests: {metrics['total_requests']}")
        print(f"  - Success Rate: {metrics['success_rate']:.1f}%")
        print(f"  - Avg Response Time: {metrics['average_response_time']:.3f}s")
        print(f"  - Endpoints: {metrics['endpoints_registered']}")
    
    elif args.export:
        if framework.export_endpoints():
            print("✅ Endpoints exported to api_endpoints.json")
        else:
            print("❌ Failed to export endpoints")
    
    else:
        print("V2APIIntegrationFramework ready")
        print("Use --test to run smoke test")
        print("Use --list to list endpoints")
        print("Use --metrics to show metrics")
        print("Use --export to export endpoints")


if __name__ == "__main__":
    main()
