#!/usr/bin/env python3
"""
V3-012: API Integration Coordinator
===================================

V2 compliant API integration coordinator.
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import API modules
from v3.v3_012_api_core import APIClient, APIFactory, HTTPMethod, APIStatus
from v3.v3_012_api_performance import APIPerformanceMonitor, APICache


class APIIntegrationCoordinator:
    """Coordinates API integration components."""
    
    def __init__(self):
        self.clients = {}
        self.performance_monitor = APIPerformanceMonitor()
        self.cache = APICache(ttl_seconds=300)
        self.factory = APIFactory()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize API integration."""
        try:
            rest_config = self.factory.create_rest_config("https://api.dreamos.com")
            self.clients["rest"] = APIClient(rest_config)
            
            graphql_config = self.factory.create_graphql_config("https://graphql.dreamos.com")
            self.clients["graphql"] = APIClient(graphql_config)
            
            self.is_initialized = True
            print("🔌 API Integration Coordinator initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    async def make_request(self, client_name: str, method: HTTPMethod, endpoint: str,
                          data: Optional[Dict[str, Any]] = None,
                          headers: Optional[Dict[str, str]] = None,
                          use_cache: bool = False):
        """Make API request with performance tracking."""
        if not self.is_initialized:
            return self._create_error_response("API not initialized")
        
        if client_name not in self.clients:
            return self._create_error_response(f"Client {client_name} not found")
        
        client = self.clients[client_name]
        
        # Check cache first
        if use_cache and method == HTTPMethod.GET:
            cache_key = f"{client_name}_{endpoint}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                request = client.create_request(method, endpoint, data, headers)
                return client.create_response(
                    request, APIStatus.SUCCESS, 200, cached_data, response_time_ms=0.1
                )
        
        # Create request
        request = client.create_request(method, endpoint, data, headers)
        client.add_request(request)
        
        # Make actual HTTP request
        start_time = datetime.now()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method.value, request.url,
                    headers=request.headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=request.timeout)
                ) as response:
                    response_data = await response.json() if response.content_type == 'application/json' else None
                    response_time = (datetime.now() - start_time).total_seconds() * 1000
                    
                    api_response = client.create_response(
                        request, APIStatus.SUCCESS, response.status,
                        response_data, response_time_ms=response_time
                    )
                    
        except asyncio.TimeoutError:
            api_response = client.create_response(
                request, APIStatus.TIMEOUT, 408, error_message="Request timeout"
            )
        except Exception as e:
            api_response = client.create_response(
                request, APIStatus.NETWORK_ERROR, 0, error_message=str(e)
            )
        
        # Add response to client
        client.add_response(api_response)
        
        # Track performance
        self.performance_monitor.track_request_performance(request, api_response)
        
        # Cache successful GET responses
        if use_cache and method == HTTPMethod.GET and api_response.status == APIStatus.SUCCESS:
            cache_key = f"{client_name}_{endpoint}"
            self.cache.set(cache_key, api_response.data or {})
        
        return api_response
    
    def _create_error_response(self, error_message: str):
        """Create error response."""
        from v3.v3_012_api_core import APIResponse
        return APIResponse(
            request_id="error",
            status=APIStatus.ERROR,
            status_code=0,
            data=None,
            error_message=error_message,
            response_time_ms=0.0,
            created_at=datetime.now()
        )
    
    def get_client_status(self, client_name: str) -> Dict[str, Any]:
        """Get client status."""
        if client_name not in self.clients:
            return {"error": "Client not found"}
        
        client = self.clients[client_name]
        return {
            "client_name": client_name,
            "base_url": client.config.base_url,
            "timeout": client.config.timeout,
            "max_retries": client.config.max_retries,
            "total_requests": len(client.request_history),
            "total_responses": len(client.response_history),
            "success_rate": client.get_success_rate(),
            "average_response_time": client.get_average_response_time()
        }
    
    def get_all_clients_status(self) -> List[Dict[str, Any]]:
        """Get status of all clients."""
        return [self.get_client_status(name) for name in self.clients.keys()]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.is_initialized:
            return {"error": "API integration not initialized"}
        
        perf_summary = self.performance_monitor.get_performance_summary(5)
        cache_stats = self.cache.get_cache_stats()
        clients_status = self.get_all_clients_status()
        
        return {
            "performance": perf_summary,
            "cache": cache_stats,
            "clients": clients_status,
            "total_clients": len(self.clients),
            "monitoring_active": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def add_client(self, name: str, base_url: str, timeout: int = 30) -> bool:
        """Add new API client."""
        try:
            config = self.factory.create_config(base_url, timeout)
            client = APIClient(config)
            self.clients[name] = client
            print(f"✅ Added API client: {name}")
            return True
        except Exception as e:
            print(f"❌ Failed to add client {name}: {e}")
            return False
    
    def remove_client(self, name: str) -> bool:
        """Remove API client."""
        if name in self.clients:
            del self.clients[name]
            print(f"🗑️ Removed API client: {name}")
            return True
        return False
    
    def clear_cache(self):
        """Clear API cache."""
        self.cache.clear()
        print("🗄️ API cache cleared")
    
    def get_performance_recommendations(self) -> List[str]:
        """Get performance optimization recommendations."""
        return self.performance_monitor.get_performance_recommendations()
    
    def export_configuration(self, filepath: str) -> bool:
        """Export API configuration."""
        try:
            config_data = {
                "clients": self.get_all_clients_status(),
                "performance_summary": self.get_performance_summary(),
                "exported_at": datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(config_data, f, indent=2, default=str)
            
            print(f"📊 API configuration exported to {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False


async def main():
    """Main execution function."""
    print("🔌 V3-012 API Integration Coordinator - Testing...")
    
    try:
        coordinator = APIIntegrationCoordinator()
        coordinator.initialize()
        
        print("\n📡 Making sample API requests...")
        
        get_response = await coordinator.make_request(
            "rest", HTTPMethod.GET, "/users", use_cache=True
        )
        print(f"   GET /users: {get_response.status.value} ({get_response.status_code})")
        
        post_response = await coordinator.make_request(
            "rest", HTTPMethod.POST, "/users", 
            data={"name": "Test User", "email": "test@dreamos.com"}
        )
        print(f"   POST /users: {post_response.status.value} ({post_response.status_code})")
        
        rest_status = coordinator.get_client_status("rest")
        
        print(f"\n🔌 REST Client Status:")
        print(f"   Base URL: {rest_status['base_url']}")
        print(f"   Success Rate: {rest_status['success_rate']:.1f}%")
        print(f"   Avg Response Time: {rest_status['average_response_time']:.2f}ms")
        
        perf_summary = coordinator.get_performance_summary()
        
        print(f"\n📊 Performance Summary:")
        print(f"   Total Clients: {perf_summary['total_clients']}")
        print(f"   Cache Entries: {perf_summary['cache']['total_entries']}")
        print(f"   Active Alerts: {perf_summary['performance']['active_alerts']}")
        
        recommendations = coordinator.get_performance_recommendations()
        
        print(f"\n💡 Performance Recommendations:")
        for rec in recommendations:
            print(f"   - {rec}")
        
        coordinator.export_configuration("api_integration_config.json")
        
        print("\n✅ V3-012 API Integration Coordinator completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ V3-012 implementation error: {e}")
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))


