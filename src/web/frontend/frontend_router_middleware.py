"""Middleware and guard utilities for the frontend router."""

from typing import Any, Dict, Iterable

from .frontend_router_config import RouteConfig, RouteGuard


def parse_query_string(query_string: str) -> Dict[str, Any]:
    """Parse a query string into a dictionary."""
    params: Dict[str, Any] = {}
    for part in query_string.split("&"):
        if "=" in part:
            key, value = part.split("=", 1)
            params[key] = value
    return params


def run_route_guards(route_config: RouteConfig, guards: Dict[str, RouteGuard]) -> bool:
    """Execute guards associated with a route."""
    for name in route_config.guards:
        guard = guards.get(name)
        if guard and not guard.condition():
            return False
    return True


def run_hooks(
    hooks: Iterable, route_config: RouteConfig, params: Dict[str, Any], query: Dict[str, Any]
) -> None:
    """Execute a collection of hook callables."""
    for hook in hooks:
        try:
            hook(route_config, params, query)
        except Exception:
            continue


__all__ = ["parse_query_string", "run_route_guards", "run_hooks"]
