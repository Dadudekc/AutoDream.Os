#!/usr/bin/env python3
"""
API Router - V2 Compliant
=========================

Automated API routing tool.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import requests
from typing import Dict, Any

class APIRouter:
    """Routes API requests intelligently."""
    
    def __init__(self):
        """Initialize API router."""
        self.routes = {}
        self.default_timeout = 30
    
    def add_route(self, path: str, service_url: str, method: str = "GET"):
        """Add API route."""
        self.routes[path] = {
            "url": service_url,
            "method": method
        }
    
    def route_request(self, path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route request to appropriate service."""
        try:
            if path not in self.routes:
                return {"success": False, "error": f"No route found for: {path}"}
            
            route = self.routes[path]
            url = route["url"]
            method = route["method"]
            
            if method == "GET":
                response = requests.get(url, params=params, timeout=self.default_timeout)
            elif method == "POST":
                response = requests.post(url, json=params, timeout=self.default_timeout)
            else:
                return {"success": False, "error": f"Unsupported method: {method}"}
            
            return {
                "success": True,
                "path": path,
                "status_code": response.status_code,
                "data": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def health_check_all_routes(self) -> Dict[str, Any]:
        """Check health of all routes."""
        results = {}
        
        for path, route in self.routes.items():
            results[path] = self.route_request(path)
        
        return results

def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="API Router")
    parser.add_argument("--path", help="Path to route")
    parser.add_argument("--params", help="Parameters as JSON")
    parser.add_argument("--health", action="store_true", help="Check all routes health")
    
    args = parser.parse_args()
    
    router = APIRouter()
    
    if args.health:
        result = router.health_check_all_routes()
    elif args.path:
        params = json.loads(args.params) if args.params else None
        result = router.route_request(args.path, params)
    else:
        result = {"error": "No action specified"}
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
