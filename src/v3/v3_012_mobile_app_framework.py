#!/usr/bin/env python3
"""
V3-012 Mobile Application Framework
===================================

Core mobile app framework for Dream.OS native integration.
Refactored into modular components for V2 compliance.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive mobile framework
"""

# Import all components from refactored modules
from .v3_012_mobile_app_framework_core import (
    ComponentType,
    MobileAppFrameworkCore,
    MobileComponent,
    Platform,
)
from .v3_012_mobile_app_framework_main import (
    MobileAppBuilder,
    MobileAppFramework,
    create_dream_os_app,
    create_mobile_component,
    generate_component_code,
    mobile_builder,
    mobile_framework,
)

# Re-export main classes for backward compatibility
__all__ = [
    # Core classes
    "Platform",
    "ComponentType",
    "MobileComponent",
    "MobileAppFrameworkCore",
    # Main framework
    "MobileAppFramework",
    "MobileAppBuilder",
    # Global instances
    "mobile_framework",
    "mobile_builder",
    # Convenience functions
    "create_mobile_component",
    "generate_component_code",
    "create_dream_os_app",
]


# For direct execution
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
