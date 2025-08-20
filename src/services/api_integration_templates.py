#!/usr/bin/env python3
"""
V2 API Integration Templates
============================
Reusable API integration templates and patterns for common integration scenarios.
Follows V2 coding standards: 300 target, 350 max LOC.
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml

# Add parent directory to path for imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the API integration framework
try:
    from services.v2_api_integration_framework import (
        V2APIIntegrationFramework, APIEndpoint, APIRequest, APIResponse,
        HTTPMethod, AuthType
    )
except ImportError:
    from v2_api_integration_framework import (
        V2APIIntegrationFramework, APIEndpoint, APIRequest, APIResponse,
        HTTPMethod, AuthType
    )

logger = logging.getLogger(__name__)


@dataclass
class IntegrationTemplate:
    """API integration template configuration"""
    name: str
    description: str
    category: str
    endpoints: List[Dict[str, Any]]
    auth_config: Dict[str, Any]
    rate_limits: Dict[str, int]
    error_handling: Dict[str, Any]
    retry_strategy: Dict[str, Any]


class V2APIIntegrationTemplates:
    """Reusable API integration templates for common scenarios"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.V2APIIntegrationTemplates")
        self.templates: Dict[str, IntegrationTemplate] = {}
        self.frameworks: Dict[str, V2APIIntegrationFramework] = {}
        
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default integration templates"""
        # REST API Template
        self._add_template("rest_api", {
            "name": "REST API Integration",
            "description": "Standard REST API integration template with CRUD operations",
            "category": "rest",
            "endpoints": [
                {"name": "get_resource", "path": "/{resource}", "method": "GET", "auth": "api_key"},
                {"name": "create_resource", "path": "/{resource}", "method": "POST", "auth": "api_key"},
                {"name": "update_resource", "path": "/{resource}/{id}", "method": "PUT", "auth": "api_key"},
                {"name": "delete_resource", "path": "/{resource}/{id}", "method": "DELETE", "auth": "api_key"},
                {"name": "list_resources", "path": "/{resource}", "method": "GET", "auth": "api_key"}
            ],
            "auth_config": {"type": "api_key", "header": "X-API-Key"},
            "rate_limits": {"default": 100, "write_operations": 50},
            "error_handling": {"retry_on": [500, 502, 503, 504], "max_retries": 3},
            "retry_strategy": {"backoff": "exponential", "max_delay": 30}
        })
        
        # GraphQL API Template
        self._add_template("graphql_api", {
            "name": "GraphQL API Integration",
            "description": "GraphQL API integration template with query and mutation support",
            "category": "graphql",
            "endpoints": [
                {"name": "graphql_query", "path": "/graphql", "method": "POST", "auth": "bearer"},
                {"name": "graphql_mutation", "path": "/graphql", "method": "POST", "auth": "bearer"},
                {"name": "graphql_subscription", "path": "/graphql", "method": "POST", "auth": "bearer"}
            ],
            "auth_config": {"type": "bearer_token", "header": "Authorization"},
            "rate_limits": {"default": 200, "mutations": 100},
            "error_handling": {"retry_on": [500, 502, 503], "max_retries": 2},
            "retry_strategy": {"backoff": "linear", "max_delay": 10}
        })
        
        # Webhook Integration Template
        self._add_template("webhook_integration", {
            "name": "Webhook Integration",
            "description": "Webhook integration template for event-driven APIs",
            "category": "webhook",
            "endpoints": [
                {"name": "webhook_receiver", "path": "/webhook", "method": "POST", "auth": "hmac"},
                {"name": "webhook_status", "path": "/webhook/status", "method": "GET", "auth": "api_key"}
            ],
            "auth_config": {"type": "hmac", "algorithm": "sha256"},
            "rate_limits": {"default": 1000, "webhook_events": 500},
            "error_handling": {"retry_on": [429, 500], "max_retries": 5},
            "retry_strategy": {"backoff": "exponential", "max_delay": 60}
        })
        
        # OAuth2 Integration Template
        self._add_template("oauth2_integration", {
            "name": "OAuth2 Integration",
            "description": "OAuth2 integration template with token management",
            "category": "oauth2",
            "endpoints": [
                {"name": "authorize", "path": "/oauth/authorize", "method": "GET", "auth": "none"},
                {"name": "token", "path": "/oauth/token", "method": "POST", "auth": "basic"},
                {"name": "refresh", "path": "/oauth/token", "method": "POST", "auth": "basic"},
                {"name": "revoke", "path": "/oauth/revoke", "method": "POST", "auth": "basic"}
            ],
            "auth_config": {"type": "oauth2", "grant_types": ["authorization_code", "refresh_token"]},
            "rate_limits": {"default": 50, "token_operations": 20},
            "error_handling": {"retry_on": [500, 502], "max_retries": 2},
            "retry_strategy": {"backoff": "linear", "max_delay": 5}
        })
        
        # Microservices Template
        self._add_template("microservices", {
            "name": "Microservices Integration",
            "description": "Microservices integration template with service discovery",
            "category": "microservices",
            "endpoints": [
                {"name": "service_discovery", "path": "/discover", "method": "GET", "auth": "api_key"},
                {"name": "health_check", "path": "/health", "method": "GET", "auth": "none"},
                {"name": "service_call", "path": "/{service}/{operation}", "method": "POST", "auth": "bearer"}
            ],
            "auth_config": {"type": "bearer_token", "header": "Authorization"},
            "rate_limits": {"default": 200, "discovery": 100, "health": 1000},
            "error_handling": {"retry_on": [503, 504], "max_retries": 3},
            "retry_strategy": {"backoff": "exponential", "max_delay": 15}
        })
    
    def _add_template(self, key: str, template_data: Dict[str, Any]):
        """Add a template to the registry"""
        template = IntegrationTemplate(
            name=template_data["name"],
            description=template_data["description"],
            category=template_data["category"],
            endpoints=template_data["endpoints"],
            auth_config=template_data["auth_config"],
            rate_limits=template_data["rate_limits"],
            error_handling=template_data["error_handling"],
            retry_strategy=template_data["retry_strategy"]
        )
        self.templates[key] = template
    
    def create_framework_from_template(self, template_key: str, base_url: str,
                                     custom_config: Optional[Dict[str, Any]] = None) -> V2APIIntegrationFramework:
        """Create an API integration framework from a template"""
        if template_key not in self.templates:
            raise ValueError(f"Template not found: {template_key}")
        
        template = self.templates[template_key]
        framework = V2APIIntegrationFramework(base_url)
        
        # Apply template configuration
        for endpoint_config in template.endpoints:
            # Parse method
            method = HTTPMethod(endpoint_config["method"])
            
            # Parse auth type
            auth_type = self._parse_auth_type(endpoint_config["auth"])
            
            # Get rate limit
            rate_limit = template.rate_limits.get("default")
            if endpoint_config["name"] in template.rate_limits:
                rate_limit = template.rate_limits[endpoint_config["name"]]
            
            # Register endpoint
            framework.register_endpoint(
                name=endpoint_config["name"],
                url=endpoint_config["path"],
                method=method,
                auth_type=auth_type,
                rate_limit=rate_limit,
                retry_count=template.error_handling.get("max_retries", 3)
            )
        
        # Apply custom configuration if provided
        if custom_config:
            self._apply_custom_config(framework, custom_config)
        
        # Store framework
        framework_key = f"{template_key}_{int(time.time())}"
        self.frameworks[framework_key] = framework
        
        self.logger.info(f"Framework created from template '{template_key}': {framework_key}")
        return framework
    
    def _parse_auth_type(self, auth_string: str) -> AuthType:
        """Parse authentication type from string"""
        auth_mapping = {
            "none": AuthType.NONE,
            "api_key": AuthType.API_KEY,
            "bearer": AuthType.BEARER_TOKEN,
            "basic": AuthType.BASIC_AUTH,
            "oauth2": AuthType.OAUTH2,
            "hmac": AuthType.HMAC
        }
        return auth_mapping.get(auth_string.lower(), AuthType.NONE)
    
    def _apply_custom_config(self, framework: V2APIIntegrationFramework, config: Dict[str, Any]):
        """Apply custom configuration to framework"""
        # Apply custom headers
        if "headers" in config:
            for endpoint_name, headers in config["headers"].items():
                # This would require framework modification to support custom headers per endpoint
                pass
        
        # Apply custom timeouts
        if "timeouts" in config:
            for endpoint_name, timeout in config["timeouts"].items():
                # This would require framework modification to support custom timeouts per endpoint
                pass
    
    def export_template(self, template_key: str, filename: str = None) -> bool:
        """Export a template to JSON or YAML"""
        if template_key not in self.templates:
            self.logger.error(f"Template not found: {template_key}")
            return False
        
        if not filename:
            filename = f"{template_key}_template.json"
        
        template = self.templates[template_key]
        
        try:
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                with open(filename, 'w') as f:
                    yaml.dump(asdict(template), f, default_flow_style=False, indent=2)
            else:
                with open(filename, 'w') as f:
                    json.dump(asdict(template), f, indent=2)
            
            self.logger.info(f"Template exported to: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export template: {e}")
            return False
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates"""
        return [
            {
                'key': key,
                'name': template.name,
                'description': template.description,
                'category': template.category,
                'endpoint_count': len(template.endpoints)
            }
            for key, template in self.templates.items()
        ]
    
    def get_template_details(self, template_key: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a template"""
        if template_key not in self.templates:
            return None
        
        template = self.templates[template_key]
        return asdict(template)
    
    def create_custom_template(self, name: str, description: str, category: str,
                             endpoints: List[Dict[str, Any]], auth_config: Dict[str, Any],
                             rate_limits: Dict[str, int], error_handling: Dict[str, Any],
                             retry_strategy: Dict[str, Any]) -> str:
        """Create a custom integration template"""
        template_key = f"custom_{name.lower().replace(' ', '_')}_{int(time.time())}"
        
        template = IntegrationTemplate(
            name=name,
            description=description,
            category=category,
            endpoints=endpoints,
            auth_config=auth_config,
            rate_limits=rate_limits,
            error_handling=error_handling,
            retry_strategy=retry_strategy
        )
        
        self.templates[template_key] = template
        self.logger.info(f"Custom template created: {template_key}")
        return template_key


def main():
    """CLI interface for V2APIIntegrationTemplates"""
    import argparse
    
    parser = argparse.ArgumentParser(description="V2 API Integration Templates CLI")
    parser.add_argument("--list", action="store_true", help="List available templates")
    parser.add_argument("--details", type=str, help="Show template details")
    parser.add_argument("--export", type=str, help="Export template to file")
    parser.add_argument("--create-framework", type=str, help="Create framework from template")
    parser.add_argument("--base-url", type=str, default="https://api.example.com", help="Base URL for framework")
    
    args = parser.parse_args()
    
    # Initialize templates
    templates = V2APIIntegrationTemplates()
    
    if args.list:
        template_list = templates.list_templates()
        print(f"📋 Available Templates ({len(template_list)}):")
        for template in template_list:
            print(f"  - {template['key']}: {template['name']} ({template['category']})")
            print(f"    {template['description']}")
            print(f"    Endpoints: {template['endpoint_count']}")
            print()
    
    elif args.details:
        details = templates.get_template_details(args.details)
        if details:
            print(f"📋 Template Details: {details['name']}")
            print(f"Category: {details['category']}")
            print(f"Description: {details['description']}")
            print(f"Endpoints: {len(details['endpoints'])}")
            print(f"Auth Config: {details['auth_config']}")
            print(f"Rate Limits: {details['rate_limits']}")
        else:
            print(f"❌ Template not found: {args.details}")
    
    elif args.export:
        if templates.export_template(args.export):
            print(f"✅ Template exported: {args.export}")
        else:
            print(f"❌ Failed to export template: {args.export}")
    
    elif args.create_framework:
        try:
            framework = templates.create_framework_from_template(args.create_framework, args.base_url)
            print(f"✅ Framework created from template: {args.create_framework}")
            print(f"Endpoints registered: {len(framework.list_endpoints())}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    else:
        print("V2APIIntegrationTemplates ready")
        print("Use --list to list templates")
        print("Use --details <template> to show template details")
        print("Use --export <template> to export template")
        print("Use --create-framework <template> to create framework from template")


if __name__ == "__main__":
    main()
