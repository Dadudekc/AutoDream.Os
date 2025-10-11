#!/usr/bin/env python3
"""
V3-011: API Gateway Development Implementation
==============================================

V2 compliant API Gateway coordinator that imports core and advanced modules.
Maintains all functionality while staying under 400 lines.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import core and advanced modules
from v3.v3_011_api_gateway_core import APIGateway, main as core_main
from v3.v3_011_api_gateway_advanced import LoadBalancer, APIMonitor, main as advanced_main

logger = logging.getLogger(__name__)


class APIGatewayCoordinator:
    """Coordinator for API Gateway core and advanced features."""
    
    def __init__(self):
        self.core_gateway = APIGateway()
        self.load_balancer = LoadBalancer()
        self.monitor = APIMonitor()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize all API Gateway components."""
        try:
            # Initialize core gateway
            self.core_gateway = APIGateway()
            
            # Initialize load balancer with sample servers
            self.load_balancer.add_server({
                "host": "localhost",
                "port": 8001,
                "weight": 1,
                "health_check_url": "/health"
            })
            self.load_balancer.add_server({
                "host": "localhost", 
                "port": 8002,
                "weight": 2,
                "health_check_url": "/health"
            })
            
            # Initialize monitor
            self.monitor = APIMonitor()
            
            self.is_initialized = True
            logger.info("API Gateway Coordinator initialized successfully")
            
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise
    
    def register_endpoint(self, path: str, method: str, handler: callable, 
                         auth_required: bool = True, rate_limit: int = None):
        """Register endpoint with core gateway."""
        if not self.is_initialized:
            self.initialize()
        
        self.core_gateway.register_endpoint(
            path, method, handler, auth_required, rate_limit
        )
    
    def handle_request(self, path: str, method: str, headers: dict, 
                      body: str = None, client_ip: str = "127.0.0.1") -> dict:
        """Handle request through load balancer and core gateway."""
        if not self.is_initialized:
            self.initialize()
        
        # Get backend server from load balancer
        server = self.load_balancer.get_next_server()
        if not server:
            return {
                "status_code": 503,
                "body": {"error": "No healthy servers available"},
                "headers": {"Content-Type": "application/json"}
            }
        
        # Handle request through core gateway
        response = self.core_gateway.handle_request(path, method, headers, body, client_ip)
        
        # Record metrics
        self.monitor.record_request(
            endpoint=path,
            method=method,
            status_code=response.status_code,
            response_time_ms=0,  # Would be calculated in real implementation
            client_ip=client_ip
        )
        
        return {
            "status_code": response.status_code,
            "body": response.body,
            "headers": response.headers,
            "server": f"{server['host']}:{server['port']}"
        }
    
    def get_health_status(self) -> dict:
        """Get comprehensive health status."""
        if not self.is_initialized:
            return {"status": "not_initialized"}
        
        core_health = self.core_gateway.get_health_status()
        monitor_dashboard = self.monitor.get_health_dashboard()
        
        return {
            **core_health,
            "load_balancer": {
                "servers": len(self.load_balancer.servers),
                "healthy_servers": len([s for s in self.load_balancer.servers if s.get("is_healthy", True)])
            },
            "monitoring": {
                "total_requests": monitor_dashboard["overall_stats"].get("total_requests", 0),
                "alert_count": monitor_dashboard["alert_count"],
                "monitoring_active": monitor_dashboard["monitoring_active"]
            }
        }
    
    def generate_documentation(self) -> dict:
        """Generate comprehensive API documentation."""
        if not self.is_initialized:
            return {"error": "Gateway not initialized"}
        
        core_docs = self.core_gateway.generate_api_documentation()
        
        return {
            **core_docs,
            "features": {
                "load_balancing": True,
                "monitoring": True,
                "rate_limiting": True,
                "authentication": True
            },
            "load_balancer": {
                "strategy": "round_robin",
                "servers": len(self.load_balancer.servers)
            }
        }


def main():
    """Main execution function."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        print("🚀 Starting V3-011 API Gateway Development...")
        
        # Run core implementation
        print("\n📋 Running Core API Gateway...")
        core_result = core_main()
        
        # Run advanced features
        print("\n⚡ Running Advanced Features...")
        advanced_result = advanced_main()
        
        # Initialize coordinator
        print("\n🔗 Initializing API Gateway Coordinator...")
        coordinator = APIGatewayCoordinator()
        coordinator.initialize()
        
        # Register sample endpoints
        def sample_handler(path: str, method: str, headers: dict, body: str = None) -> dict:
            return {
                "status_code": 200,
                "body": {"message": f"Hello from {path}", "method": method},
                "headers": {"Content-Type": "application/json"}
            }
        
        coordinator.register_endpoint("/health", "GET", sample_handler, auth_required=False)
        coordinator.register_endpoint("/status", "GET", sample_handler)
        coordinator.register_endpoint("/agents", "GET", sample_handler)
        
        # Get comprehensive status
        health = coordinator.get_health_status()
        docs = coordinator.generate_documentation()
        
        print("\n✅ V3-011 API Gateway Development completed successfully!")
        print(f"📊 Core Result: {'SUCCESS' if core_result == 0 else 'FAILED'}")
        print(f"⚡ Advanced Result: {'SUCCESS' if advanced_result == 0 else 'FAILED'}")
        print(f"🔗 Coordinator Status: {'INITIALIZED' if coordinator.is_initialized else 'FAILED'}")
        print(f"📚 Documentation: {len(docs.get('endpoints', []))} endpoints documented")
        print(f"🏥 Health: {health.get('status', 'unknown')}")
        print(f"⚖️ Load Balancer: {health.get('load_balancer', {}).get('servers', 0)} servers")
        print(f"📈 Monitoring: {health.get('monitoring', {}).get('total_requests', 0)} requests tracked")
        
        return 0 if all(r == 0 for r in [core_result, advanced_result]) else 1
        
    except Exception as e:
        logger.error(f"V3-011 Coordinator error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())



