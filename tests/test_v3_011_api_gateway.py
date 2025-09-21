#!/usr/bin/env python3
"""
Test suite for V3-011 API Gateway Development
=============================================

Comprehensive tests for API Gateway functionality including rate limiting,
authentication, endpoint registration, and documentation generation.
"""

import sys
import pytest
import time
from pathlib import Path
from unittest.mock import Mock, patch

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.v3.v3_011_api_gateway import (
    APIGateway, RateLimiter, Authenticator, 
    RateLimitConfig, AuthConfig, AuthMethod, RateLimitType
)


class TestRateLimiter:
    """Test rate limiting functionality."""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization."""
        config = RateLimitConfig(requests_per_minute=10, window_size=60)
        limiter = RateLimiter(config)
        
        assert limiter.config.requests_per_minute == 10
        assert limiter.config.window_size == 60
        assert limiter.config.enabled is True
    
    def test_rate_limiter_allows_requests_within_limit(self):
        """Test rate limiter allows requests within limit."""
        config = RateLimitConfig(requests_per_minute=5, window_size=60)
        limiter = RateLimiter(config)
        
        # Should allow 5 requests
        for i in range(5):
            assert limiter.is_allowed("test_key") is True
    
    def test_rate_limiter_blocks_requests_over_limit(self):
        """Test rate limiter blocks requests over limit."""
        config = RateLimitConfig(requests_per_minute=3, window_size=60)
        limiter = RateLimiter(config)
        
        # Allow 3 requests
        for i in range(3):
            assert limiter.is_allowed("test_key") is True
        
        # 4th request should be blocked
        assert limiter.is_allowed("test_key") is False
    
    def test_rate_limiter_resets_after_window(self):
        """Test rate limiter resets after window period."""
        config = RateLimitConfig(requests_per_minute=2, window_size=1)  # 1 second window
        limiter = RateLimiter(config)
        
        # Use up limit
        assert limiter.is_allowed("test_key") is True
        assert limiter.is_allowed("test_key") is True
        assert limiter.is_allowed("test_key") is False
        
        # Wait for window to reset
        time.sleep(1.1)
        
        # Should allow requests again
        assert limiter.is_allowed("test_key") is True
    
    def test_rate_limiter_disabled_allows_all_requests(self):
        """Test rate limiter when disabled allows all requests."""
        config = RateLimitConfig(enabled=False)
        limiter = RateLimiter(config)
        
        # Should allow unlimited requests
        for i in range(100):
            assert limiter.is_allowed("test_key") is True
    
    def test_get_remaining_requests(self):
        """Test getting remaining requests."""
        config = RateLimitConfig(requests_per_minute=5, window_size=60)
        limiter = RateLimiter(config)
        
        # Initially should have 5 remaining
        assert limiter.get_remaining_requests("test_key") == 5
        
        # After 2 requests, should have 3 remaining
        limiter.is_allowed("test_key")
        limiter.is_allowed("test_key")
        assert limiter.get_remaining_requests("test_key") == 3


class TestAuthenticator:
    """Test authentication functionality."""
    
    def test_authenticator_initialization(self):
        """Test authenticator initialization."""
        config = AuthConfig(method=AuthMethod.JWT)
        auth = Authenticator(config)
        
        assert auth.config.method == AuthMethod.JWT
        assert auth.config.secret_key == "default_secret_key"
    
    def test_authentication_none_method(self):
        """Test authentication with NONE method."""
        config = AuthConfig(method=AuthMethod.NONE)
        auth = Authenticator(config)
        
        # Should always return True
        assert auth.authenticate({}) is True
        assert auth.authenticate({"Authorization": "Bearer token"}) is True
    
    def test_authentication_api_key_method(self):
        """Test authentication with API key method."""
        config = AuthConfig(method=AuthMethod.API_KEY, api_key_header="X-API-Key")
        auth = Authenticator(config)
        
        # Generate a token
        token = auth.generate_token("test_user")
        assert token != ""
        
        # Should authenticate with valid API key
        assert auth.authenticate({"X-API-Key": token}) is True
        
        # Should not authenticate without API key
        assert auth.authenticate({}) is False
        
        # Should not authenticate with invalid API key
        assert auth.authenticate({"X-API-Key": "invalid"}) is False
    
    def test_authentication_jwt_method(self):
        """Test authentication with JWT method."""
        config = AuthConfig(method=AuthMethod.JWT, jwt_header="Authorization")
        auth = Authenticator(config)
        
        # Generate a token
        token = auth.generate_token("test_user")
        assert token != ""
        
        # Should authenticate with valid JWT
        assert auth.authenticate({"Authorization": f"Bearer {token}"}) is True
        
        # Should not authenticate without Bearer prefix
        assert auth.authenticate({"Authorization": token}) is False
        
        # Should not authenticate with invalid token
        assert auth.authenticate({"Authorization": "Bearer invalid"}) is False


class TestAPIGateway:
    """Test API Gateway functionality."""
    
    def test_api_gateway_initialization(self):
        """Test API Gateway initialization."""
        gateway = APIGateway()
        
        assert gateway.rate_limit_config.requests_per_minute == 100
        assert gateway.auth_config.method == AuthMethod.JWT
        assert len(gateway.endpoints) == 0
        assert len(gateway.versions) == 1  # Default v1 version
        assert "v1" in gateway.versions
    
    def test_register_endpoint(self):
        """Test endpoint registration."""
        gateway = APIGateway()
        
        def sample_handler(path, method, headers, body):
            return {"status_code": 200, "body": {"message": "test"}}
        
        # Register endpoint
        result = gateway.register_endpoint("/test", "GET", sample_handler)
        assert result is True
        
        # Check endpoint was registered
        assert "GET:/test" in gateway.endpoints
        endpoint = gateway.endpoints["GET:/test"]
        assert endpoint["path"] == "/test"
        assert endpoint["method"] == "GET"
        assert endpoint["handler"] == sample_handler
    
    def test_register_endpoint_with_custom_config(self):
        """Test endpoint registration with custom configuration."""
        gateway = APIGateway()
        
        def sample_handler(path, method, headers, body):
            return {"status_code": 200, "body": {"message": "test"}}
        
        # Register endpoint with custom config
        result = gateway.register_endpoint(
            "/test", "POST", sample_handler,
            version="v2",
            rate_limit_type=RateLimitType.PER_USER,
            auth_required=False
        )
        
        assert result is True
        endpoint = gateway.endpoints["POST:/test"]
        assert endpoint["version"] == "v2"
        assert endpoint["rate_limit_type"] == RateLimitType.PER_USER
        assert endpoint["auth_required"] is False
    
    def test_process_request_success(self):
        """Test successful request processing."""
        gateway = APIGateway()
        
        def sample_handler(path, method, headers, body):
            return {
                "status_code": 200,
                "body": {"message": "success"},
                "headers": {"Content-Type": "application/json"}
            }
        
        # Register endpoint
        gateway.register_endpoint("/test", "GET", sample_handler, auth_required=False)
        
        # Process request
        response = gateway.process_request(
            "/test", "GET", {}, None, "127.0.0.1"
        )
        
        assert response["status_code"] == 200
        assert response["body"]["message"] == "success"
        assert "processing_time" in response
        assert "X-RateLimit-Remaining" in response["headers"]
    
    def test_process_request_endpoint_not_found(self):
        """Test request processing with non-existent endpoint."""
        gateway = APIGateway()
        
        response = gateway.process_request(
            "/nonexistent", "GET", {}, None, "127.0.0.1"
        )
        
        assert response["status_code"] == 404
        assert "Endpoint not found" in response["body"]["error"]
    
    def test_process_request_authentication_required(self):
        """Test request processing with authentication required."""
        gateway = APIGateway()
        
        def sample_handler(path, method, headers, body):
            return {"status_code": 200, "body": {"message": "success"}}
        
        # Register endpoint with auth required
        gateway.register_endpoint("/test", "GET", sample_handler, auth_required=True)
        
        # Process request without authentication
        response = gateway.process_request(
            "/test", "GET", {}, None, "127.0.0.1"
        )
        
        assert response["status_code"] == 401
        assert "Authentication required" in response["body"]["error"]
    
    def test_process_request_rate_limit_exceeded(self):
        """Test request processing with rate limit exceeded."""
        # Create gateway with very low rate limit
        rate_config = RateLimitConfig(requests_per_minute=1, window_size=60)
        gateway = APIGateway(rate_limit_config=rate_config)
        
        def sample_handler(path, method, headers, body):
            return {"status_code": 200, "body": {"message": "success"}}
        
        # Register endpoint
        gateway.register_endpoint("/test", "GET", sample_handler, auth_required=False)
        
        # First request should succeed
        response1 = gateway.process_request("/test", "GET", {}, None, "127.0.0.1")
        assert response1["status_code"] == 200
        
        # Second request should be rate limited
        response2 = gateway.process_request("/test", "GET", {}, None, "127.0.0.1")
        assert response2["status_code"] == 429
        assert "Rate limit exceeded" in response2["body"]["error"]
        assert "X-RateLimit-Remaining" in response2["headers"]
    
    def test_generate_api_documentation(self):
        """Test API documentation generation."""
        gateway = APIGateway()
        
        def sample_handler(path, method, headers, body):
            return {"status_code": 200, "body": {"message": "test"}}
        
        # Register some endpoints
        gateway.register_endpoint("/test1", "GET", sample_handler)
        gateway.register_endpoint("/test2", "POST", sample_handler, auth_required=False)
        
        # Generate documentation
        docs = gateway.generate_api_documentation()
        
        assert docs["title"] == "Dream.OS V3 API Gateway"
        assert docs["version"] == "1.0.0"
        assert "authentication" in docs
        assert "rate_limiting" in docs
        assert "versions" in docs
        assert "endpoints" in docs
        assert len(docs["endpoints"]) == 2
        
        # Check endpoint documentation
        endpoint_paths = [ep["path"] for ep in docs["endpoints"]]
        assert "/test1" in endpoint_paths
        assert "/test2" in endpoint_paths
    
    def test_get_health_status(self):
        """Test health status retrieval."""
        gateway = APIGateway()
        
        # Register some endpoints
        def sample_handler(path, method, headers, body):
            return {"status_code": 200, "body": {"message": "test"}}
        
        gateway.register_endpoint("/test", "GET", sample_handler)
        
        # Get health status
        health = gateway.get_health_status()
        
        assert health["status"] == "healthy"
        assert "timestamp" in health
        assert "uptime" in health
        assert health["endpoints_registered"] == 1
        assert health["versions_available"] == 1
        assert "rate_limiting_enabled" in health
        assert "authentication_enabled" in health
        assert "recent_requests" in health


class TestIntegration:
    """Integration tests for API Gateway."""
    
    def test_full_workflow(self):
        """Test complete API Gateway workflow."""
        # Initialize gateway
        gateway = APIGateway()
        
        # Register multiple endpoints
        def health_handler(path, method, headers, body):
            return {"status_code": 200, "body": {"status": "healthy"}}
        
        def status_handler(path, method, headers, body):
            return {"status_code": 200, "body": {"agents": ["Agent-1", "Agent-2"]}}
        
        gateway.register_endpoint("/health", "GET", health_handler, auth_required=False)
        gateway.register_endpoint("/status", "GET", status_handler)
        
        # Process requests
        health_response = gateway.process_request("/health", "GET", {}, None, "127.0.0.1")
        assert health_response["status_code"] == 200
        assert health_response["body"]["status"] == "healthy"
        
        # Generate documentation
        docs = gateway.generate_api_documentation()
        assert len(docs["endpoints"]) == 2
        
        # Get health status
        health_status = gateway.get_health_status()
        assert health_status["endpoints_registered"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])




