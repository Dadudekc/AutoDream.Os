"""Configuration models for the frontend routing system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


@dataclass
class RouteConfig:
    """Configuration for a single route entry."""

    path: str
    name: str
    component: str
    props: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)
    children: List["RouteConfig"] = field(default_factory=list)
    guards: List[str] = field(default_factory=list)
    middleware: List[str] = field(default_factory=list)
    lazy_load: bool = False
    cache: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class NavigationState:
    """Represents current navigation details."""

    current_route: str = "/"
    previous_route: Optional[str] = None
    route_params: Dict[str, Any] = field(default_factory=dict)
    query_params: Dict[str, Any] = field(default_factory=dict)
    navigation_history: List[str] = field(default_factory=lambda: ["/"])
    breadcrumbs: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class RouteGuard:
    """Defines a guard that can block navigation."""

    name: str
    condition: Callable[[], bool]
    redirect_to: Optional[str] = None
    message: str = ""
    priority: int = 0


@dataclass
class RouteMiddleware:
    """Middleware executed during navigation."""

    name: str
    handler: Callable
    order: int = 0
    async_handler: bool = False


__all__ = [
    "RouteConfig",
    "NavigationState",
    "RouteGuard",
    "RouteMiddleware",
]
