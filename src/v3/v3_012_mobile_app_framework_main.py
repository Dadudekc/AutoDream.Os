#!/usr/bin/env python3
"""
V3-012 Mobile Application Framework - Main
==========================================

Main mobile application framework with builder and convenience functions.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, main framework functionality
"""

from datetime import datetime
from typing import Any

from .v3_012_mobile_app_framework_core import (
    ComponentType,
    MobileAppFrameworkCore,
    MobileComponent,
    Platform,
)
from .v3_012_mobile_app_framework_templates import ComponentTemplateManager


class MobileAppFramework:
    """Core mobile application framework"""

    def __init__(self):
        self.core = MobileAppFrameworkCore()
        self.templates = ComponentTemplateManager()

    def create_component(
        self,
        component_id: str,
        name: str,
        component_type: ComponentType,
        platform: Platform,
        dependencies: list[str] = None,
        properties: dict[str, Any] = None,
    ) -> MobileComponent:
        """Create new mobile component"""
        return self.core.create_component(
            component_id, name, component_type, platform, dependencies, properties
        )

    def generate_component_code(self, component: MobileComponent) -> str:
        """Generate code for mobile component"""
        return self.templates.generate_component_code(component)

    def get_platform_config(self, platform: Platform) -> dict[str, Any]:
        """Get platform configuration"""
        return self.core.get_platform_config(platform)

    def list_components(self, platform: Platform | None = None) -> list[MobileComponent]:
        """List components, optionally filtered by platform"""
        return self.core.list_components(platform)

    def export_project_structure(self, project_name: str) -> dict[str, Any]:
        """Export complete project structure"""
        return self.core.export_project_structure(project_name)


class MobileAppBuilder:
    """Mobile application builder and generator"""

    def __init__(self):
        self.framework = MobileAppFramework()
        self.build_configs = self._initialize_build_configs()

    def _initialize_build_configs(self) -> dict[str, dict[str, Any]]:
        """Initialize build configurations"""
        return {
            "development": {
                "debug": True,
                "minify": False,
                "source_maps": True,
                "hot_reload": True,
            },
            "staging": {"debug": False, "minify": True, "source_maps": True, "hot_reload": False},
            "production": {
                "debug": False,
                "minify": True,
                "source_maps": False,
                "hot_reload": False,
            },
        }

    def create_dream_os_app(self) -> dict[str, Any]:
        """Create Dream.OS mobile application structure"""
        # Create core components for Dream.OS
        components = []

        # Main app screen
        main_screen = self.framework.create_component(
            "main_screen",
            "MainScreen",
            ComponentType.SCREEN,
            Platform.CROSS_PLATFORM,
            properties={"navigation": "NavigationProp", "route": "RouteProp"},
        )
        components.append(main_screen)

        # Dream.OS service
        dream_service = self.framework.create_component(
            "dream_service",
            "DreamOSService",
            ComponentType.SERVICE,
            Platform.CROSS_PLATFORM,
            properties={"api_url": "string", "auth_token": "string"},
        )
        components.append(dream_service)

        # Storage utility
        storage_util = self.framework.create_component(
            "storage_util", "StorageUtil", ComponentType.STORAGE, Platform.CROSS_PLATFORM
        )
        components.append(storage_util)

        # Performance widget
        perf_widget = self.framework.create_component(
            "perf_widget",
            "PerformanceWidget",
            ComponentType.WIDGET,
            Platform.CROSS_PLATFORM,
            properties={"metrics": "PerformanceMetrics", "onPress": "() => void"},
        )
        components.append(perf_widget)

        return {
            "app_name": "Dream.OS Mobile",
            "version": "1.0.0",
            "platforms": ["android", "ios", "web"],
            "components": [component.component_id for component in components],
            "created_at": datetime.now().isoformat(),
        }

    def generate_build_config(self, environment: str) -> dict[str, Any]:
        """Generate build configuration for environment"""
        config = self.build_configs.get(environment, self.build_configs["development"])
        return {
            "environment": environment,
            "config": config,
            "platforms": list(self.framework.core.platform_configs.keys()),
            "generated_at": datetime.now().isoformat(),
        }


# Global mobile app framework instance
mobile_framework = MobileAppFramework()
mobile_builder = MobileAppBuilder()


def create_mobile_component(
    component_id: str,
    name: str,
    component_type: ComponentType,
    platform: Platform,
    dependencies: list[str] = None,
    properties: dict[str, Any] = None,
) -> MobileComponent:
    """Create mobile component"""
    return mobile_framework.create_component(
        component_id, name, component_type, platform, dependencies, properties
    )


def generate_component_code(component: MobileComponent) -> str:
    """Generate code for mobile component"""
    return mobile_framework.generate_component_code(component)


def create_dream_os_app() -> dict[str, Any]:
    """Create Dream.OS mobile application"""
    return mobile_builder.create_dream_os_app()


if __name__ == "__main__":
    # Test mobile app framework
    print("Creating Dream.OS Mobile App...")
    app = create_dream_os_app()
    print(f"App created: {app}")

    # Test component creation
    component = create_mobile_component(
        "test_component",
        "TestComponent",
        ComponentType.SCREEN,
        Platform.CROSS_PLATFORM,
        properties={"title": "string", "data": "any[]"},
    )
    print(f"Component created: {component.name}")

    # Generate component code
    code = generate_component_code(component)
    print(f"Generated code length: {len(code)} characters")
