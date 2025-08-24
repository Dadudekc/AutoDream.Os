"""Frontend router orchestrator."""

from .frontend_router_core import FrontendRouter, RouteMatcher
from .frontend_router_config import (
    RouteConfig,
    NavigationState,
    RouteGuard,
    RouteMiddleware,
)
from .frontend_router_handlers import (
    RouteBuilder,
    create_default_routes,
    route,
)
from .frontend_router_middleware import (
    parse_query_string,
    run_route_guards,
    run_hooks,
)

__all__ = [
    "FrontendRouter",
    "RouteMatcher",
    "RouteConfig",
    "NavigationState",
    "RouteGuard",
    "RouteMiddleware",
    "RouteBuilder",
    "create_router_with_default_routes",
    "create_default_routes",
    "route",
    "parse_query_string",
    "run_route_guards",
    "run_hooks",
]


def create_router_with_default_routes() -> FrontendRouter:
    """Return a router instance preloaded with default routes."""
    router = FrontendRouter()
    router.add_routes(create_default_routes())
    return router
