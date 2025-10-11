#!/usr/bin/env python3
"""
V3-012: Mobile User Interface
=============================

V2 compliant mobile UI coordinator.
"""

import sys
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import UI modules
from v3.v3_012_ui_components import ComponentFactory, ComponentRenderer
from v3.v3_012_ui_screens import ScreenFactory, ScreenManager, NavigationController


class MobileUICoordinator:
    """Coordinator for mobile UI components and screens."""
    
    def __init__(self):
        self.component_factory = ComponentFactory()
        self.component_renderer = ComponentRenderer()
        self.screen_factory = ScreenFactory()
        self.screen_manager = ScreenManager()
        self.navigation_controller = NavigationController()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize mobile UI system."""
        try:
            self.navigation_controller.initialize_app_screens()
            self.screen_manager.screens = self.navigation_controller.screen_manager.screens
            self.screen_manager.current_screen = self.navigation_controller.screen_manager.current_screen
            self.is_initialized = True
            print("📱 Mobile UI Coordinator initialized successfully")
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            raise
    
    def navigate_to_screen(self, screen_id: str) -> bool:
        """Navigate to specific screen."""
        if not self.is_initialized:
            self.initialize()
        return self.screen_manager.navigate_to(screen_id)
    
    def go_back(self) -> bool:
        """Go back to previous screen."""
        return self.screen_manager.go_back()
    
    def get_current_screen_data(self) -> Dict[str, Any]:
        """Get current screen data."""
        if not self.is_initialized:
            return {"error": "UI not initialized"}
        
        screen = self.screen_manager.get_current_screen()
        if not screen:
            return {"error": "No current screen"}
        
        return {
            "screen_id": screen.screen_id,
            "name": screen.name,
            "type": screen.screen_type.value,
            "component_count": len(screen.components)
        }
    
    def render_current_screen(self) -> Dict[str, Any]:
        """Render current screen with all components."""
        if not self.is_initialized:
            return {"error": "UI not initialized"}
        return self.screen_manager.render_current_screen()
    
    def get_ui_status(self) -> Dict[str, Any]:
        """Get comprehensive UI status."""
        if not self.is_initialized:
            return {"status": "not_initialized"}
        
        screen_list = self.screen_manager.get_screen_list()
        nav_status = self.navigation_controller.get_navigation_status()
        
        return {
            "status": "initialized",
            "current_screen": self.screen_manager.current_screen,
            "total_screens": len(screen_list),
            "screen_history": nav_status["screen_history"],
            "available_flows": nav_status["available_flows"],
            "initialized_at": datetime.now().isoformat()
        }


def main():
    """Main execution function."""
    print("📱 V3-012 Mobile User Interface - Testing...")
    
    try:
        # Initialize coordinator
        coordinator = MobileUICoordinator()
        coordinator.initialize()
        
        # Test navigation
        print("\n🔄 Testing navigation...")
        coordinator.navigate_to_screen("dashboard")
        coordinator.navigate_to_screen("settings")
        coordinator.go_back()
        
        # Test flow execution
        print("\n📋 Testing navigation flows...")
        coordinator.execute_navigation_flow("main_app")
        
        # Get status
        ui_status = coordinator.get_ui_status()
        
        print(f"\n📊 UI Status:")
        print(f"   Status: {ui_status['status']}")
        print(f"   Current Screen: {ui_status['current_screen']}")
        print(f"   Total Screens: {ui_status['total_screens']}")
        print(f"   Available Flows: {len(ui_status['available_flows'])}")
        
        print("\n✅ V3-012 Mobile User Interface completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ V3-012 implementation error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

