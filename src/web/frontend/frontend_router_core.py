"""Core routing classes for the frontend system."""

import logging
import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .frontend_router_config import (
    NavigationState,
    RouteConfig,
    RouteGuard,
    RouteMiddleware,
)
from .frontend_router_middleware import (
    parse_query_string,
    run_hooks,
    run_route_guards,
)

logger = logging.getLogger(__name__)


class RouteMatcher:
    """Simple URL matcher using compiled regular expressions."""

    def __init__(self):
        self.pattern_cache: Dict[str, re.Pattern] = {}

    def match_route(self, url: str, route_config: RouteConfig) -> Optional[Dict[str, Any]]:
        pattern = self._get_pattern(route_config.path)
        match = pattern.match(url)
        if match:
            return {
                "matched": True,
                "params": match.groupdict(),
                "route_config": route_config,
            }
        return None

    def _get_pattern(self, route_path: str) -> re.Pattern:
        if route_path not in self.pattern_cache:
            pattern = re.sub(r":(\w+)", r"(?P<\1>[^/]+)", route_path)
            self.pattern_cache[route_path] = re.compile(f"^{pattern}$")
        return self.pattern_cache[route_path]


class FrontendRouter:
    """Lightweight frontend router with guard and hook support."""

    def __init__(self):
        self.routes: List[RouteConfig] = []
        self.route_map: Dict[str, RouteConfig] = {}
        self.named_routes: Dict[str, RouteConfig] = {}
        self.matcher = RouteMatcher()
        self.navigation_state = NavigationState()
        self.guards: Dict[str, RouteGuard] = {}
        self.middleware: Dict[str, RouteMiddleware] = {}
        self.before_each_hooks: List[Callable] = []
        self.after_each_hooks: List[Callable] = []

    def add_route(self, route_config: RouteConfig) -> "FrontendRouter":
        self.routes.append(route_config)
        self.route_map[route_config.path] = route_config
        if route_config.name:
            self.named_routes[route_config.name] = route_config
        for child in route_config.children:
            child_path = f"{route_config.path.rstrip('/')}/{child.path.lstrip('/')}"
            child_config = RouteConfig(
                path=child_path,
                name=child.name,
                component=child.component,
                props=child.props,
                meta=child.meta,
                children=child.children,
                guards=child.guards,
                middleware=child.middleware,
                lazy_load=child.lazy_load,
                cache=child.cache,
            )
            self.add_route(child_config)
        return self

    def add_routes(self, routes: List[RouteConfig]) -> "FrontendRouter":
        for route in routes:
            self.add_route(route)
        return self

    def get_route(self, path: str) -> Optional[RouteConfig]:
        return self.route_map.get(path)

    def get_named_route(self, name: str) -> Optional[RouteConfig]:
        return self.named_routes.get(name)

    def match_url(self, url: str) -> Optional[Dict[str, Any]]:
        if url in self.route_map:
            return {"matched": True, "params": {}, "route_config": self.route_map[url]}
        for route in self.routes:
            match = self.matcher.match_route(url, route)
            if match:
                return match
        return None

    def navigate_to(self, path: str, replace: bool = False) -> bool:
        url_parts = path.split("?")
        route_path = url_parts[0]
        query_params = (
            parse_query_string(url_parts[1]) if len(url_parts) > 1 else {}
        )
        match_result = self.match_url(route_path)
        if not match_result:
            return False
        route_config = match_result["route_config"]
        route_params = match_result["params"]
        if not run_route_guards(route_config, self.guards):
            return False
        run_hooks(self.before_each_hooks, route_config, route_params, query_params)
        self._update_navigation_state(route_path, route_params, query_params, replace)
        run_hooks(self.after_each_hooks, route_config, route_params, query_params)
        return True

    def add_guard(self, guard: RouteGuard) -> "FrontendRouter":
        self.guards[guard.name] = guard
        return self

    def add_middleware(self, middleware: RouteMiddleware) -> "FrontendRouter":
        self.middleware[middleware.name] = middleware
        return self

    def before_each(self, hook: Callable) -> "FrontendRouter":
        self.before_each_hooks.append(hook)
        return self

    def after_each(self, hook: Callable) -> "FrontendRouter":
        self.after_each_hooks.append(hook)
        return self

    def get_navigation_state(self) -> NavigationState:
        return self.navigation_state

    def get_breadcrumbs(self) -> List[Dict[str, Any]]:
        return self.navigation_state.breadcrumbs

    def _update_navigation_state(
        self,
        path: str,
        route_params: Dict[str, Any],
        query_params: Dict[str, Any],
        replace: bool,
    ) -> None:
        state = self.navigation_state
        if not replace:
            state.previous_route = state.current_route
            state.navigation_history.append(path)
        state.current_route = path
        state.route_params = route_params
        state.query_params = query_params
        state.timestamp = datetime.now()
        route = self.route_map.get(path)
        state.breadcrumbs.append({"path": path, "name": route.name if route else path})


__all__ = ["FrontendRouter", "RouteMatcher"]
