"""Route builders and default route helpers."""

from datetime import datetime
from typing import Any, Dict, List

from .frontend_router_config import RouteConfig


class RouteBuilder:
    """Fluent builder for :class:`RouteConfig`."""

    def __init__(self):
        self.path = "/"
        self.name = ""
        self.component = ""
        self.props: Dict[str, Any] = {}
        self.meta: Dict[str, Any] = {}
        self.children: List["RouteBuilder"] = []
        self.guards: List[str] = []
        self.middleware: List[str] = []
        self.lazy_load = False
        self.cache = True

    def set_path(self, path: str) -> "RouteBuilder":
        self.path = path
        return self

    def set_name(self, name: str) -> "RouteBuilder":
        self.name = name
        return self

    def set_component(self, component: str) -> "RouteBuilder":
        self.component = component
        return self

    def set_props(self, props: Dict[str, Any]) -> "RouteBuilder":
        self.props = props
        return self

    def set_meta(self, meta: Dict[str, Any]) -> "RouteBuilder":
        self.meta = meta
        return self

    def add_child(self, child: "RouteBuilder") -> "RouteBuilder":
        self.children.append(child)
        return self

    def add_guard(self, guard_name: str) -> "RouteBuilder":
        self.guards.append(guard_name)
        return self

    def add_middleware(self, middleware_name: str) -> "RouteBuilder":
        self.middleware.append(middleware_name)
        return self

    def set_lazy_load(self, lazy: bool) -> "RouteBuilder":
        self.lazy_load = lazy
        return self

    def set_cache(self, cache: bool) -> "RouteBuilder":
        self.cache = cache
        return self

    def build(self) -> RouteConfig:
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


def create_default_routes() -> List[RouteConfig]:
    """Return a set of default application routes."""

    home = (
        RouteBuilder()
        .set_path("/")
        .set_name("home")
        .set_component("HomePage")
        .set_props({"title": "Home"})
        .set_meta({"requiresAuth": False})
        .build()
    )

    dashboard = (
        RouteBuilder()
        .set_path("/dashboard")
        .set_name("dashboard")
        .set_component("DashboardPage")
        .set_props({"title": "Dashboard"})
        .set_meta({"requiresAuth": True})
        .add_guard("auth")
        .build()
    )

    settings = (
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
        )
        .add_child(
            RouteBuilder()
            .set_path("security")
            .set_name("security-settings")
            .set_component("SecuritySettings")
            .set_props({"title": "Security Settings"})
        )
        .build()
    )

    api_docs = (
        RouteBuilder()
        .set_path("/api-docs")
        .set_name("api-docs")
        .set_component("APIDocsPage")
        .set_props({"title": "API Documentation"})
        .set_meta({"requiresAuth": False})
        .build()
    )

    return [home, dashboard, settings, api_docs]


def route(path: str, name: str = "", component: str = "") -> RouteBuilder:
    """Convenience decorator-style builder."""
    return RouteBuilder().set_path(path).set_name(name).set_component(component)


__all__ = ["RouteBuilder", "create_default_routes", "route"]
