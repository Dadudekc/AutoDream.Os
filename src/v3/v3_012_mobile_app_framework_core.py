#!/usr/bin/env python3
"""
V3-012 Mobile Application Framework - Core
==========================================

Core classes and data structures for mobile application framework.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, core mobile framework components
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class Platform(Enum):
    """Mobile platforms"""

    ANDROID = "android"
    IOS = "ios"
    WEB = "web"
    CROSS_PLATFORM = "cross_platform"


class ComponentType(Enum):
    """Mobile component types"""

    SCREEN = "screen"
    WIDGET = "widget"
    SERVICE = "service"
    UTILITY = "utility"
    STORAGE = "storage"


@dataclass
class MobileComponent:
    """Mobile component structure"""

    component_id: str
    name: str
    component_type: ComponentType
    platform: Platform
    dependencies: list[str]
    properties: dict[str, Any]
    methods: list[str]
    created_at: datetime


class MobileAppFrameworkCore:
    """Core mobile application framework functionality"""

    def __init__(self):
        self.components: dict[str, MobileComponent] = {}
        self.platform_configs = self._initialize_platform_configs()

    def _initialize_platform_configs(self) -> dict[Platform, dict[str, Any]]:
        """Initialize platform-specific configurations"""
        return {
            Platform.ANDROID: {
                "language": "Kotlin",
                "framework": "Android SDK",
                "build_tool": "Gradle",
                "min_sdk": 21,
                "target_sdk": 34,
                "package_name": "com.dreamos.app",
            },
            Platform.IOS: {
                "language": "Swift",
                "framework": "UIKit/SwiftUI",
                "build_tool": "Xcode",
                "min_version": "12.0",
                "target_version": "17.0",
                "bundle_id": "com.dreamos.app",
            },
            Platform.WEB: {
                "language": "TypeScript",
                "framework": "React Native Web",
                "build_tool": "Webpack",
                "min_browsers": ["Chrome 90", "Firefox 88", "Safari 14"],
                "pwa_support": True,
            },
            Platform.CROSS_PLATFORM: {
                "language": "TypeScript",
                "framework": "React Native",
                "build_tool": "Metro",
                "platforms": ["android", "ios", "web"],
                "native_modules": True,
            },
        }

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
        if dependencies is None:
            dependencies = []
        if properties is None:
            properties = {}

        component = MobileComponent(
            component_id=component_id,
            name=name,
            component_type=component_type,
            platform=platform,
            dependencies=dependencies,
            properties=properties,
            methods=self._generate_component_methods(component_type),
            created_at=datetime.now(),
        )

        self.components[component_id] = component
        return component

    def _generate_component_methods(self, component_type: ComponentType) -> list[str]:
        """Generate methods for component type"""
        method_map = {
            ComponentType.SCREEN: ["render", "componentDidMount", "componentWillUnmount"],
            ComponentType.WIDGET: ["render", "onPress", "onLongPress"],
            ComponentType.SERVICE: ["initialize", "start", "stop", "cleanup"],
            ComponentType.UTILITY: ["validate", "process", "format", "parse"],
            ComponentType.STORAGE: ["save", "load", "delete", "clear", "exists"],
        }
        return method_map.get(component_type, [])

    def get_platform_config(self, platform: Platform) -> dict[str, Any]:
        """Get platform configuration"""
        return self.platform_configs.get(platform, {})

    def list_components(self, platform: Platform | None = None) -> list[MobileComponent]:
        """List components, optionally filtered by platform"""
        if platform:
            return [c for c in self.components.values() if c.platform == platform]
        return list(self.components.values())

    def export_project_structure(self, project_name: str) -> dict[str, Any]:
        """Export complete project structure"""
        return {
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            "platforms": list(self.platform_configs.keys()),
            "components": {
                component_id: {
                    "name": component.name,
                    "type": component.component_type.value,
                    "platform": component.platform.value,
                    "dependencies": component.dependencies,
                    "properties": component.properties,
                    "methods": component.methods,
                    "created_at": component.created_at.isoformat(),
                }
                for component_id, component in self.components.items()
            },
            "total_components": len(self.components),
        }
