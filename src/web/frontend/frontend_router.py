#!/usr/bin/env python3
"""
Frontend Routing System
Agent_Cellphone_V2_Repository TDD Integration Project

This module provides a comprehensive frontend routing system with:
- Client-side routing
- Route configuration management
- Navigation state management
- Route guards and middleware
- Dynamic route loading

Author: Web Development & UI Framework Specialist
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    children: List["RouteConfig"]
    guards: List[str]
    middleware: List[str]
    lazy_load: bool
    cache: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class NavigationState:
    """Current navigation state"""

    current_route: str
    previous_route: Optional[str]
    route_params: Dict[str, Any]
    query_params: Dict[str, Any]
    navigation_history: List[str]
    breadcrumbs: List[Dict[str, Any]]
    timestamp: datetime


@dataclass
class RouteGuard:
    """Route guard configuration"""

    name: str
    condition: Callable
    redirect_to: Optional[str]
    message: str
    priority: int


@dataclass
class RouteMiddleware:
    """Route middleware configuration"""

    name: str
    handler: Callable
    order: int
    async_handler: bool


class RouteMatcher:
    """Matches URL patterns to route configurations"""

    def __init__(self):
        self.pattern_cache: Dict[str, re.Pattern] = {}

    def match_route(
        self, url: str, route_config: RouteConfig
    ) -> Optional[Dict[str, Any]]:
        """Match a URL against a route configuration"""
        try:
            # Convert route path to regex pattern
            pattern = self._get_pattern(route_config.path)

            # Match the URL
            match = pattern.match(url)
            if match:
                return {
                    "matched": True,
                    "params": match.groupdict(),
                    "route_config": route_config,
                }

            return None
        except Exception as e:
            logger.error(f"Error matching route {url} against {route_config.path}: {e}")
            return None

    def _get_pattern(self, route_path: str) -> re.Pattern:
        """Get compiled regex pattern for a route path"""
        if route_path in self.pattern_cache:
            return self.pattern_cache[route_path]

        # Convert route path to regex pattern
        # e.g., "/users/:id" -> r"^/users/(?P<id>[^/]+)$"
        pattern = route_path

        # Replace path parameters
        pattern = re.sub(r":(\w+)", r"(?P<\1>[^/]+)", pattern)

        # Add start and end anchors
        pattern = f"^{pattern}$"

        # Compile and cache
        compiled_pattern = re.compile(pattern)
        self.pattern_cache[route_path] = compiled_pattern

        return compiled_pattern


# ============================================================================
# FRONTEND ROUTER
# ============================================================================


class FrontendRouter:
    """Main frontend router class"""

    def __init__(self):
        self.routes: List[RouteConfig] = []
        self.route_map: Dict[str, RouteConfig] = {}
        self.named_routes: Dict[str, RouteConfig] = {}
        self.matcher = RouteMatcher()
        self.navigation_state = NavigationState(
            current_route="/",
            previous_route=None,
            route_params={},
            query_params={},
            navigation_history=["/"],
            breadcrumbs=[],
            timestamp=datetime.now(),
        )
        self.guards: Dict[str, RouteGuard] = {}
        self.middleware: Dict[str, RouteMiddleware] = {}
        self.before_each_hooks: List[Callable] = []
        self.after_each_hooks: List[Callable] = []
        self.error_handlers: Dict[str, Callable] = {}

        logger.info("Frontend router initialized")

    def add_route(self, route_config: RouteConfig) -> "FrontendRouter":
        """Add a route to the router"""
        try:
            # Validate route configuration
            self._validate_route_config(route_config)

            # Add to routes list
            self.routes.append(route_config)

            # Add to route map
            self.route_map[route_config.path] = route_config

            # Add to named routes if name is provided
            if route_config.name:
                self.named_routes[route_config.name] = route_config

            # Add children routes recursively
            for child in route_config.children:
                child_path = f"{route_config.path.rstrip('/')}/{child.path.lstrip('/')}"
                child_config = RouteConfig(
                    path=child_path,
                    name=child.name,
                    component=child.component,
                    props=child.props,
                    meta=child.meta,
                    children=[],
                    guards=child.guards,
                    middleware=child.middleware,
                    lazy_load=child.lazy_load,
                    cache=child.cache,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                self.add_route(child_config)

            logger.info(f"Added route: {route_config.path}")
            return self

        except Exception as e:
            logger.error(f"Error adding route {route_config.path}: {e}")
            raise

    def add_routes(self, routes: List[RouteConfig]) -> "FrontendRouter":
        """Add multiple routes at once"""
        for route in routes:
            self.add_route(route)
        return self

    def remove_route(self, path: str) -> bool:
        """Remove a route from the router"""
        try:
            if path in self.route_map:
                route_config = self.route_map[path]

                # Remove from all collections
                self.routes = [r for r in self.routes if r.path != path]
                del self.route_map[path]

                if route_config.name in self.named_routes:
                    del self.named_routes[route_config.name]

                logger.info(f"Removed route: {path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error removing route {path}: {e}")
            return False

    def get_route(self, path: str) -> Optional[RouteConfig]:
        """Get a route by path"""
        return self.route_map.get(path)

    def get_named_route(self, name: str) -> Optional[RouteConfig]:
        """Get a route by name"""
        return self.named_routes.get(name)

    def match_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Match a URL against all routes"""
        try:
            # Try exact match first
            if url in self.route_map:
                return {
                    "matched": True,
                    "params": {},
                    "route_config": self.route_map[url],
                }

            # Try pattern matching
            for route_config in self.routes:
                match_result = self.matcher.match_route(url, route_config)
                if match_result:
                    return match_result

            return None

        except Exception as e:
            logger.error(f"Error matching URL {url}: {e}")
            return None

    def navigate_to(self, path: str, replace: bool = False) -> bool:
        """Navigate to a new route"""
        try:
            # Parse URL and query parameters
            url_parts = path.split("?")
            route_path = url_parts[0]
            query_params = {}

            if len(url_parts) > 1:
                query_params = self._parse_query_string(url_parts[1])

            # Match the route
            match_result = self.match_url(route_path)
            if not match_result:
                logger.warning(f"No route found for path: {route_path}")
                return False

            route_config = match_result["route_config"]
            route_params = match_result["params"]

            # Run route guards
            if not self._run_route_guards(route_config):
                logger.warning(f"Route guard failed for path: {route_path}")
                return False

            # Run before hooks
            self._run_before_hooks(route_config, route_params, query_params)

            # Update navigation state
            self._update_navigation_state(
                route_path, route_params, query_params, replace
            )

            # Run after hooks
            self._run_after_hooks(route_config, route_params, query_params)

            logger.info(f"Navigated to: {route_path}")
            return True

        except Exception as e:
            logger.error(f"Error navigating to {path}: {e}")
            return False

    def add_guard(self, guard: RouteGuard) -> "FrontendRouter":
        """Add a route guard"""
        self.guards[guard.name] = guard
        logger.info(f"Added route guard: {guard.name}")
        return self

    def add_middleware(self, middleware: RouteMiddleware) -> "FrontendRouter":
        """Add route middleware"""
        self.middleware[middleware.name] = middleware
        logger.info(f"Added route middleware: {middleware.name}")
        return self

    def before_each(self, hook: Callable) -> "FrontendRouter":
        """Add a before navigation hook"""
        self.before_each_hooks.append(hook)
        return self

    def after_each(self, hook: Callable) -> "FrontendRouter":
        """Add an after navigation hook"""
        self.after_each_hooks.append(hook)
        return self

    def on_error(self, error_type: str, handler: Callable) -> "FrontendRouter":
        """Add an error handler"""
        self.error_handlers[error_type] = handler
        return self

    def get_navigation_state(self) -> NavigationState:
        """Get current navigation state"""
        return self.navigation_state

    def get_breadcrumbs(self) -> List[Dict[str, Any]]:
        """Get breadcrumbs for current route"""
        return self.navigation_state.breadcrumbs

    def go_back(self) -> bool:
        """Navigate back in history"""
        if len(self.navigation_state.navigation_history) > 1:
            previous_route = self.navigation_state.navigation_history[-2]
            return self.navigate_to(previous_route, replace=True)
        return False

    def go_forward(self) -> bool:
        """Navigate forward in history"""
        # This would require maintaining a forward history stack
        # For now, return False
        return False

    def _validate_route_config(self, route_config: RouteConfig):
        """Validate route configuration"""
        if not route_config.path:
            raise ValueError("Route path is required")

        if not route_config.component:
            raise ValueError("Route component is required")

        if route_config.path in self.route_map:
            raise ValueError(f"Route path already exists: {route_config.path}")

        if route_config.name and route_config.name in self.named_routes:
            raise ValueError(f"Route name already exists: {route_config.name}")

    def _parse_query_string(self, query_string: str) -> Dict[str, Any]:
        """Parse query string into dictionary"""
        query_params = {}
        try:
            for param in query_string.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    query_params[key] = value
        except Exception as e:
            logger.error(f"Error parsing query string: {e}")

        return query_params

    def _run_route_guards(self, route_config: RouteConfig) -> bool:
        """Run route guards"""
        try:
            for guard_name in route_config.guards:
                guard = self.guards.get(guard_name)
                if guard:
                    if not guard.condition():
                        logger.warning(f"Route guard failed: {guard_name}")
                        return False

            return True

        except Exception as e:
            logger.error(f"Error running route guards: {e}")
            return False

    def _run_before_hooks(
        self,
        route_config: RouteConfig,
        route_params: Dict[str, Any],
        query_params: Dict[str, Any],
    ):
        """Run before navigation hooks"""
        try:
            for hook in self.before_each_hooks:
                hook(route_config, route_params, query_params)
        except Exception as e:
            logger.error(f"Error in before hook: {e}")

    def _run_after_hooks(
        self,
        route_config: RouteConfig,
        route_params: Dict[str, Any],
        query_params: Dict[str, Any],
    ):
        """Run after navigation hooks"""
        try:
            for hook in self.after_each_hooks:
                hook(route_config, route_params, query_params)
        except Exception as e:
            logger.error(f"Error in after hook: {e}")

    def _update_navigation_state(
        self,
        path: str,
        route_params: Dict[str, Any],
        query_params: Dict[str, Any],
        replace: bool,
    ):
        """Update navigation state"""
        try:
            # Update navigation state
            if not replace:
                self.navigation_state.previous_route = (
                    self.navigation_state.current_route
                )
                self.navigation_state.navigation_history.append(path)
            else:
                # Replace current route in history
                if self.navigation_state.navigation_history:
                    self.navigation_state.navigation_history[-1] = path

            self.navigation_state.current_route = path
            self.navigation_state.route_params = route_params
            self.navigation_state.query_params = query_params
            self.navigation_state.timestamp = datetime.now()

            # Update breadcrumbs
            self._update_breadcrumbs(path)

        except Exception as e:
            logger.error(f"Error updating navigation state: {e}")

    def _update_breadcrumbs(self, path: str):
        """Update breadcrumbs for current route"""
        try:
            breadcrumbs = []
            path_parts = path.strip("/").split("/")

            current_path = ""
            for i, part in enumerate(path_parts):
                if part:
                    current_path += f"/{part}"
                    breadcrumbs.append(
                        {
                            "path": current_path,
                            "name": part.replace("-", " ").title(),
                            "active": i == len(path_parts) - 1,
                        }
                    )

            self.navigation_state.breadcrumbs = breadcrumbs

        except Exception as e:
            logger.error(f"Error updating breadcrumbs: {e}")


# ============================================================================
# ROUTE CONFIGURATION BUILDER
# ============================================================================


class RouteBuilder:
    """Builder for creating route configurations"""

    def __init__(self):
        self.path = ""
        self.name = ""
        self.component = ""
        self.props = {}
        self.meta = {}
        self.children = []
        self.guards = []
        self.middleware = []
        self.lazy_load = False
        self.cache = True

    def set_path(self, path: str) -> "RouteBuilder":
        """Set route path"""
        self.path = path
        return self

    def set_name(self, name: str) -> "RouteBuilder":
        """Set route name"""
        self.name = name
        return self

    def set_component(self, component: str) -> "RouteBuilder":
        """Set route component"""
        self.component = component
        return self

    def set_props(self, props: Dict[str, Any]) -> "RouteBuilder":
        """Set route props"""
        self.props = props
        return self

    def set_meta(self, meta: Dict[str, Any]) -> "RouteBuilder":
        """Set route metadata"""
        self.meta = meta
        return self

    def add_child(self, child: "RouteBuilder") -> "RouteBuilder":
        """Add child route"""
        self.children.append(child)
        return self

    def add_guard(self, guard_name: str) -> "RouteBuilder":
        """Add route guard"""
        self.guards.append(guard_name)
        return self

    def add_middleware(self, middleware_name: str) -> "RouteBuilder":
        """Add route middleware"""
        self.middleware.append(middleware_name)
        return self

    def set_lazy_load(self, lazy: bool) -> "RouteBuilder":
        """Set lazy loading"""
        self.lazy_load = lazy
        return self

    def set_cache(self, cache: bool) -> "RouteBuilder":
        """Set caching"""
        self.cache = cache
        return self

    def build(self) -> RouteConfig:
        """Build the route configuration"""
        return RouteConfig(
            path=self.path,
            name=self.name,
            component=self.component,
            props=self.props,
            meta=self.meta,
            children=[child.build() for child in self.children],
            guards=self.guards,
            middleware=self.middleware,
            lazy_load=self.lazy_load,
            cache=self.cache,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


# ============================================================================
# PREDEFINED ROUTE CONFIGURATIONS
# ============================================================================


def create_default_routes() -> List[RouteConfig]:
    """Create default route configurations"""

    # Home route
    home_route = (
        RouteBuilder()
        .set_path("/")
        .set_name("home")
        .set_component("HomePage")
        .set_props({"title": "Home"})
        .set_meta({"requiresAuth": False})
        .build()
    )

    # Dashboard route
    dashboard_route = (
        RouteBuilder()
        .set_path("/dashboard")
        .set_name("dashboard")
        .set_component("DashboardPage")
        .set_props({"title": "Dashboard"})
        .set_meta({"requiresAuth": True})
        .add_guard("auth")
        .build()
    )

    # Settings route with children
    settings_route = (
        RouteBuilder()
        .set_path("/settings")
        .set_name("settings")
        .set_component("SettingsPage")
        .set_props({"title": "Settings"})
        .set_meta({"requiresAuth": True})
        .add_guard("auth")
        .add_child(
            RouteBuilder()
            .set_path("profile")
            .set_name("profile-settings")
            .set_component("ProfileSettings")
            .set_props({"title": "Profile Settings"})
            .build()
        )
        .add_child(
            RouteBuilder()
            .set_path("security")
            .set_name("security-settings")
            .set_component("SecuritySettings")
            .set_props({"title": "Security Settings"})
            .build()
        )
        .build()
    )

    # API documentation route
    api_docs_route = (
        RouteBuilder()
        .set_path("/api-docs")
        .set_name("api-docs")
        .set_component("APIDocsPage")
        .set_props({"title": "API Documentation"})
        .set_meta({"requiresAuth": False})
        .build()
    )

    return [home_route, dashboard_route, settings_route, api_docs_route]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def create_router_with_default_routes() -> FrontendRouter:
    """Create a router with default routes"""
    router = FrontendRouter()
    default_routes = create_default_routes()
    router.add_routes(default_routes)
    return router


def route(path: str, name: str = "", component: str = "") -> RouteBuilder:
    """Decorator for creating routes"""
    return RouteBuilder().set_path(path).set_name(name).set_component(component)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Example usage
    router = create_router_with_default_routes()

    # Add custom route
    custom_route = (
        RouteBuilder()
        .set_path("/custom")
        .set_name("custom")
        .set_component("CustomPage")
        .set_props({"title": "Custom Page"})
        .build()
    )

    router.add_route(custom_route)

    # Test navigation
    print("Testing navigation...")
    router.navigate_to("/dashboard")
    router.navigate_to("/settings/profile")

    # Print current state
    state = router.get_navigation_state()
    print(f"Current route: {state.current_route}")
    print(f"Breadcrumbs: {[b['name'] for b in state.breadcrumbs]}")

    print("Frontend router setup complete!")
