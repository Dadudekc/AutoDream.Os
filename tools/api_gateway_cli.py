#!/usr/bin/env python3
"""
API Gateway CLI Tool
====================

Command-line interface for V3-011 API Gateway Development.
Provides utilities for managing API Gateway configuration, testing endpoints,
and monitoring performance.

Usage:
    python tools/api_gateway_cli.py --help
    python tools/api_gateway_cli.py start --port 8080
    python tools/api_gateway_cli.py test --endpoint /health
    python tools/api_gateway_cli.py docs --output api_docs.json
"""

import sys
import argparse
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.v3.v3_011_api_gateway import APIGateway, RateLimitConfig, AuthConfig, AuthMethod


class APIGatewayCLI:
    """CLI interface for API Gateway management."""
    
    def __init__(self):
        """Initialize CLI interface."""
        self.gateway: Optional[APIGateway] = None
        self.base_url = "http://localhost:8080"
    
    def start_server(self, port: int = 8080, host: str = "localhost"):
        """Start API Gateway server."""
        try:
            print(f"🚀 Starting API Gateway server on {host}:{port}")
            
            # Initialize gateway
            self.gateway = APIGateway()
            self.base_url = f"http://{host}:{port}"
            
            # Register default endpoints
            self._register_default_endpoints()
            
            print(f"✅ API Gateway started successfully")
            print(f"📡 Base URL: {self.base_url}")
            print(f"📚 API Documentation: {self.base_url}/docs")
            print(f"🔍 Health Check: {self.base_url}/health")
            print(f"⚡ Rate Limiting: Enabled")
            print(f"🔒 Authentication: JWT")
            
            # Keep server running
            print("\n🔄 Server running... Press Ctrl+C to stop")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Server stopped")
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return 1
        
        return 0
    
    def test_endpoint(self, endpoint: str, method: str = "GET", 
                     headers: Optional[Dict[str, str]] = None,
                     data: Optional[str] = None) -> int:
        """Test API endpoint."""
        try:
            print(f"🧪 Testing endpoint: {method} {endpoint}")
            
            if not self.gateway:
                self.gateway = APIGateway()
                self._register_default_endpoints()
            
            # Process request
            response = self.gateway.process_request(
                endpoint, method, headers or {}, data, "127.0.0.1"
            )
            
            # Display results
            print(f"📊 Status Code: {response['status_code']}")
            print(f"⏱️  Processing Time: {response.get('processing_time', 0):.3f}s")
            
            if response.get('headers'):
                print("📋 Headers:")
                for key, value in response['headers'].items():
                    print(f"   {key}: {value}")
            
            print("📄 Response Body:")
            print(json.dumps(response.get('body', {}), indent=2))
            
            if response['status_code'] >= 400:
                print("❌ Request failed")
                return 1
            else:
                print("✅ Request successful")
                return 0
                
        except Exception as e:
            print(f"❌ Error testing endpoint: {e}")
            return 1
    
    def generate_docs(self, output_file: Optional[str] = None) -> int:
        """Generate API documentation."""
        try:
            print("📚 Generating API documentation...")
            
            if not self.gateway:
                self.gateway = APIGateway()
                self._register_default_endpoints()
            
            # Generate documentation
            docs = self.gateway.generate_api_documentation()
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(docs, f, indent=2)
                print(f"✅ Documentation saved to: {output_file}")
            else:
                print("📄 API Documentation:")
                print(json.dumps(docs, indent=2))
            
            return 0
            
        except Exception as e:
            print(f"❌ Error generating documentation: {e}")
            return 1
    
    def show_health(self) -> int:
        """Show API Gateway health status."""
        try:
            print("🔍 Checking API Gateway health...")
            
            if not self.gateway:
                self.gateway = APIGateway()
                self._register_default_endpoints()
            
            # Get health status
            health = self.gateway.get_health_status()
            
            print("📊 Health Status:")
            print(f"   Status: {health['status']}")
            print(f"   Timestamp: {health['timestamp']}")
            print(f"   Endpoints Registered: {health['endpoints_registered']}")
            print(f"   Versions Available: {health['versions_available']}")
            print(f"   Rate Limiting: {'Enabled' if health['rate_limiting_enabled'] else 'Disabled'}")
            print(f"   Authentication: {'Enabled' if health['authentication_enabled'] else 'Disabled'}")
            print(f"   Recent Requests: {health['recent_requests']}")
            
            if health['status'] == 'healthy':
                print("✅ API Gateway is healthy")
                return 0
            else:
                print("❌ API Gateway is unhealthy")
                return 1
                
        except Exception as e:
            print(f"❌ Error checking health: {e}")
            return 1
    
    def configure_rate_limiting(self, requests_per_minute: int, 
                               burst_limit: int = None) -> int:
        """Configure rate limiting."""
        try:
            print(f"⚙️  Configuring rate limiting: {requests_per_minute} requests/minute")
            
            if not self.gateway:
                self.gateway = APIGateway()
            
            # Update rate limiting configuration
            self.gateway.rate_limit_config.requests_per_minute = requests_per_minute
            if burst_limit:
                self.gateway.rate_limit_config.burst_limit = burst_limit
            
            print("✅ Rate limiting configured successfully")
            return 0
            
        except Exception as e:
            print(f"❌ Error configuring rate limiting: {e}")
            return 1
    
    def configure_authentication(self, method: str, secret_key: str = None) -> int:
        """Configure authentication."""
        try:
            print(f"🔒 Configuring authentication: {method}")
            
            if not self.gateway:
                self.gateway = APIGateway()
            
            # Update authentication configuration
            auth_method = AuthMethod(method.lower())
            self.gateway.auth_config.method = auth_method
            
            if secret_key:
                self.gateway.auth_config.secret_key = secret_key
            
            print("✅ Authentication configured successfully")
            return 0
            
        except Exception as e:
            print(f"❌ Error configuring authentication: {e}")
            return 1
    
    def _register_default_endpoints(self):
        """Register default API endpoints."""
        if not self.gateway:
            return
        
        def health_handler(path, method, headers, body):
            return {
                "status_code": 200,
                "body": {"status": "healthy", "timestamp": time.time()},
                "headers": {"Content-Type": "application/json"}
            }
        
        def status_handler(path, method, headers, body):
            return {
                "status_code": 200,
                "body": {
                    "agents": ["Agent-1", "Agent-2", "Agent-3", "Agent-4"],
                    "status": "active"
                },
                "headers": {"Content-Type": "application/json"}
            }
        
        def docs_handler(path, method, headers, body):
            docs = self.gateway.generate_api_documentation()
            return {
                "status_code": 200,
                "body": docs,
                "headers": {"Content-Type": "application/json"}
            }
        
        # Register endpoints
        self.gateway.register_endpoint("/health", "GET", health_handler, auth_required=False)
        self.gateway.register_endpoint("/status", "GET", status_handler)
        self.gateway.register_endpoint("/docs", "GET", docs_handler, auth_required=False)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="API Gateway CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Start server command
    start_parser = subparsers.add_parser("start", help="Start API Gateway server")
    start_parser.add_argument("--port", type=int, default=8080, help="Server port")
    start_parser.add_argument("--host", default="localhost", help="Server host")
    
    # Test endpoint command
    test_parser = subparsers.add_parser("test", help="Test API endpoint")
    test_parser.add_argument("endpoint", help="Endpoint to test")
    test_parser.add_argument("--method", default="GET", help="HTTP method")
    test_parser.add_argument("--headers", help="Headers as JSON string")
    test_parser.add_argument("--data", help="Request body data")
    
    # Generate docs command
    docs_parser = subparsers.add_parser("docs", help="Generate API documentation")
    docs_parser.add_argument("--output", help="Output file path")
    
    # Health check command
    health_parser = subparsers.add_parser("health", help="Check API Gateway health")
    
    # Configure rate limiting command
    rate_parser = subparsers.add_parser("rate-limit", help="Configure rate limiting")
    rate_parser.add_argument("requests_per_minute", type=int, help="Requests per minute")
    rate_parser.add_argument("--burst", type=int, help="Burst limit")
    
    # Configure authentication command
    auth_parser = subparsers.add_parser("auth", help="Configure authentication")
    auth_parser.add_argument("method", choices=["jwt", "api_key", "basic", "none"], help="Authentication method")
    auth_parser.add_argument("--secret-key", help="Secret key for authentication")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    cli = APIGatewayCLI()
    
    try:
        if args.command == "start":
            return cli.start_server(args.port, args.host)
        elif args.command == "test":
            headers = json.loads(args.headers) if args.headers else None
            return cli.test_endpoint(args.endpoint, args.method, headers, args.data)
        elif args.command == "docs":
            return cli.generate_docs(args.output)
        elif args.command == "health":
            return cli.show_health()
        elif args.command == "rate-limit":
            return cli.configure_rate_limiting(args.requests_per_minute, args.burst)
        elif args.command == "auth":
            return cli.configure_authentication(args.method, args.secret_key)
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())




