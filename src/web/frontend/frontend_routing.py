#!/usr/bin/env python3
"""
Frontend Routing Module
Agent_Cellphone_V2_Repository TDD Integration Project

This module handles all routing concerns extracted from the monolithic frontend_app.py file.

Author: Agent-8 (Integration Enhancement Manager)
Contract: MODERATE-021 - Frontend App Modularization
License: MIT
"""

import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Mock logger for testing
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import from core module (commented out for testing)
# from .frontend_app_core import FrontendRoute, create_route



# ============================================================================
# ROUTING MODELS & DATA STRUCTURES
# ============================================================================


@dataclass
class RouteConfig:
    """Configuration for a frontend route"""
    
    path: str
    name: str
    component: str
    props: Dict[str, Any]
    meta: Dict[str, Any]
    middleware: List[str]
    guards: List[str]
    children: List["RouteConfig"]
    created_at: datetime
    updated_at: datetime


@dataclass
class RouteMatch:
    """Result of route matching"""
    
    route: RouteConfig
    params: Dict[str, str]
    query: Dict[str, str]
    matched_path: str
    score: float


class RouteGuard:
    """Base class for route guards"""
    
    def __init__(self, name: str):
        self.name = name
    
    def can_activate(self, route: RouteConfig, context: Dict[str, Any]) -> bool:
        """Check if route can be activated"""
        raise NotImplementedError("Subclasses must implement can_activate")
    
    def get_error_message(self) -> str:
        """Get error message if guard fails"""
        return f"Route guard '{self.name}' failed"


class AuthenticationGuard(RouteGuard):
    """Guard for authentication-required routes"""
    
    def __init__(self):
        super().__init__("authentication")
    
    def can_activate(self, route: RouteConfig, context: Dict[str, Any]) -> bool:
        """Check if user is authenticated"""
        user = context.get("user")
        return user is not None and user.get("authenticated", False)
    
    def get_error_message(self) -> str:
        return "Authentication required for this route"


class RoleGuard(RouteGuard):
    """Guard for role-based access control"""
    
    def __init__(self, required_roles: List[str]):
        super().__init__("role")
        self.required_roles = required_roles
    
    def can_activate(self, route: RouteConfig, context: Dict[str, Any]) -> bool:
        """Check if user has required roles"""
        user = context.get("user", {})
        user_roles = user.get("roles", [])
        return any(role in user_roles for role in self.required_roles)
    
    def get_error_message(self) -> str:
        return f"Required roles: {', '.join(self.required_roles)}"


# ============================================================================
# ROUTING MANAGER
# ============================================================================


class RoutingManager:
    """Manages frontend routing configuration and navigation"""
    
    def __init__(self):
        self.routes: List[RouteConfig] = []
        self.guards: Dict[str, RouteGuard] = {}
        self.middleware: Dict[str, Callable] = {}
        self.current_route: Optional[RouteConfig] = None
        self.route_history: List[RouteConfig] = []
        
        # Register default guards
        self._register_default_guards()
    
    def _register_default_guards(self):
        """Register default route guards"""
        self.register_guard("auth", AuthenticationGuard())
        self.register_guard("admin", RoleGuard(["admin"]))
        self.register_guard("user", RoleGuard(["user", "admin"]))
    
    def register_guard(self, name: str, guard: RouteGuard):
        """Register a route guard"""
        self.guards[name] = guard
        logger.info(f"Registered route guard: {name}")
    
    def register_middleware(self, name: str, middleware_func: Callable):
        """Register route middleware"""
        self.middleware[name] = middleware_func
        logger.info(f"Registered route middleware: {name}")
    
    def add_route(self, route: RouteConfig):
        """Add a new route"""
        self.routes.append(route)
        logger.info(f"Added route: {route.path} -> {route.component}")
    
    def add_routes(self, routes: List[RouteConfig]):
        """Add multiple routes"""
        for route in routes:
            self.add_route(route)
    
    def find_route(self, path: str) -> Optional[RouteMatch]:
        """Find a route that matches the given path"""
        best_match = None
        best_score = 0.0
        
        for route in self.routes:
            match = self._match_route(route, path)
            if match and match.score > best_score:
                best_match = match
                best_score = match.score
        
        return best_match
    
    def _match_route(self, route: RouteConfig, path: str) -> Optional[RouteMatch]:
        """Match a specific route against a path"""
        # Simple path matching - could be enhanced with regex patterns
        if route.path == path:
            return RouteMatch(
                route=route,
                params={},
                query={},
                matched_path=path,
                score=1.0
            )
        
        # Check for parameterized routes (e.g., /user/:id)
        if ":" in route.path:
            match = self._match_parameterized_route(route, path)
            if match:
                return match
        
        # Check child routes
        for child in route.children:
            child_match = self._match_route(child, path)
            if child_match:
                return child_match
        
        return None
    
    def _match_parameterized_route(self, route: RouteConfig, path: str) -> Optional[RouteMatch]:
        """Match parameterized routes (e.g., /user/:id)"""
        route_parts = route.path.split("/")
        path_parts = path.split("/")
        
        if len(route_parts) != len(path_parts):
            return None
        
        params = {}
        for route_part, path_part in zip(route_parts, path_parts):
            if route_part.startswith(":"):
                # This is a parameter
                param_name = route_part[1:]
                params[param_name] = path_part
            elif route_part != path_part:
                # Path parts don't match
                return None
        
        return RouteMatch(
            route=route,
            params=params,
            query={},
            matched_path=path,
            score=0.9  # Slightly lower score for parameterized routes
        )
    
    def navigate_to(self, path: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Navigate to a specific route"""
        context = context or {}
        
        # Find matching route
        route_match = self.find_route(path)
        if not route_match:
            return {
                "success": False,
                "error": f"Route not found: {path}",
                "route": None
            }
        
        route = route_match.route
        
        # Check route guards
        guard_result = self._check_route_guards(route, context)
        if not guard_result["success"]:
            return guard_result
        
        # Execute route middleware
        middleware_result = self._execute_route_middleware(route, context)
        if not middleware_result["success"]:
            return middleware_result
        
        # Update current route
        if self.current_route:
            self.route_history.append(self.current_route)
        
        self.current_route = route
        
        logger.info(f"Navigated to route: {path} -> {route.component}")
        
        return {
            "success": True,
            "route": route,
            "params": route_match.params,
            "query": route_match.query,
            "component": route.component,
            "props": route.props
        }
    
    def _check_route_guards(self, route: RouteConfig, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if route can be activated based on guards"""
        for guard_name in route.guards:
            guard = self.guards.get(guard_name)
            if guard and not guard.can_activate(route, context):
                return {
                    "success": False,
                    "error": guard.get_error_message(),
                    "guard": guard_name
                }
        
        return {"success": True}
    
    def _execute_route_middleware(self, route: RouteConfig, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute route middleware"""
        for middleware_name in route.middleware:
            middleware_func = self.middleware.get(middleware_name)
            if middleware_func:
                try:
                    result = middleware_func(route, context)
                    if not result.get("success", True):
                        return result
                except Exception as e:
                    logger.error(f"Error in middleware {middleware_name}: {e}")
                    return {
                        "success": False,
                        "error": f"Middleware error: {str(e)}",
                        "middleware": middleware_name
                    }
        
        return {"success": True}
    
    def go_back(self) -> Optional[RouteConfig]:
        """Navigate back to previous route"""
        if self.route_history:
            previous_route = self.route_history.pop()
            self.current_route = previous_route
            logger.info(f"Navigated back to: {previous_route.path}")
            return previous_route
        return None
    
    def get_current_route(self) -> Optional[RouteConfig]:
        """Get current route"""
        return self.current_route
    
    def get_route_history(self) -> List[RouteConfig]:
        """Get route navigation history"""
        return self.route_history.copy()
    
    def clear_history(self):
        """Clear route navigation history"""
        self.route_history.clear()
        logger.info("Route history cleared")


# ============================================================================
# ROUTE CONFIGURATION HELPERS
# ============================================================================


def create_route_config(
    path: str,
    name: str,
    component: str,
    props: Dict[str, Any] = None,
    meta: Dict[str, Any] = None,
    middleware: List[str] = None,
    guards: List[str] = None,
    children: List[RouteConfig] = None
) -> RouteConfig:
    """Create a new route configuration"""
    return RouteConfig(
        path=path,
        name=name,
        component=component,
        props=props or {},
        meta=meta or {},
        middleware=middleware or [],
        guards=guards or [],
        children=children or [],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


def create_nested_routes(
    parent_path: str,
    parent_name: str,
    routes: List[Dict[str, Any]]
) -> List[RouteConfig]:
    """Create nested routes under a parent path"""
    nested_routes = []
    
    for route_data in routes:
        route = create_route_config(
            path=f"{parent_path}{route_data['path']}",
            name=route_data['name'],
            component=route_data['component'],
            props=route_data.get('props', {}),
            meta=route_data.get('meta', {}),
            middleware=route_data.get('middleware', []),
            guards=route_data.get('guards', [])
        )
        nested_routes.append(route)
    
    return nested_routes


def create_route_group(
    base_path: str,
    routes: List[Dict[str, Any]]
) -> List[RouteConfig]:
    """Create a group of routes with a common base path"""
    return create_nested_routes(base_path, "", routes)


# ============================================================================
# DEFAULT ROUTE CONFIGURATIONS
# ============================================================================


def get_default_routes() -> List[RouteConfig]:
    """Get default route configurations"""
    return [
        create_route_config("/", "Home", "HomePage", {}, {"title": "Home"}),
        create_route_config("/about", "About", "AboutPage", {}, {"title": "About"}),
        create_route_config("/contact", "Contact", "ContactPage", {}, {"title": "Contact"}),
        create_route_config("/dashboard", "Dashboard", "DashboardPage", {}, {"title": "Dashboard"}, guards=["auth"]),
        create_route_config("/admin", "Admin", "AdminPage", {}, {"title": "Admin"}, guards=["admin"]),
    ]


def get_api_routes() -> List[RouteConfig]:
    """Get API route configurations"""
    return [
        create_route_config("/api/health", "Health", "HealthCheck", {}, {"api": True}),
        create_route_config("/api/status", "Status", "StatusCheck", {}, {"api": True}),
        create_route_config("/api/config", "Config", "ConfigEndpoint", {}, {"api": True}),
    ]


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Test the routing module
    print("Frontend Routing Module")
    print("=" * 40)
    
    # Test route creation
    route = create_route_config("/test", "Test", "TestComponent")
    print(f"Created route: {route.path} -> {route.component}")
    
    # Test routing manager
    manager = RoutingManager()
    manager.add_routes(get_default_routes())
    print(f"Added {len(manager.routes)} default routes")
    
    # Test route finding
    match = manager.find_route("/")
    if match:
        print(f"Found route: {match.route.name} -> {match.route.component}")
    
    # Test navigation
    result = manager.navigate_to("/")
    print(f"Navigation result: {result['success']}")
    
    print("Routing module tests completed successfully!")
