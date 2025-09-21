#!/usr/bin/env python3
"""
V3-012: UI Screens
==================

Screen definitions and navigation for Dream.OS mobile app.
V2 compliant with focus on screen management.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from v3.v3_012_ui_components import UIComponent, ComponentFactory, ComponentRenderer


class ScreenType(Enum):
    """Screen types."""
    LOGIN = "login"
    DASHBOARD = "dashboard"
    SETTINGS = "settings"
    PROFILE = "profile"
    DETAILS = "details"
    LIST = "list"


@dataclass
class Screen:
    """Screen structure."""
    screen_id: str
    name: str
    screen_type: ScreenType
    components: List[UIComponent]
    navigation: Dict[str, Any]
    styles: Dict[str, Any]
    created_at: datetime


class ScreenFactory:
    """Factory for creating screens."""
    
    def __init__(self):
        self.component_factory = ComponentFactory()
        self.renderer = ComponentRenderer()
    
    def create_login_screen(self) -> Screen:
        """Create login screen."""
        components = [
            self.component_factory.create_text("title", "Welcome to Dream.OS", "title"),
            self.component_factory.create_input("username", "Username"),
            self.component_factory.create_input("password", "Password", "password"),
            self.component_factory.create_button("login_btn", "Login", "onLogin"),
            self.component_factory.create_button("register_btn", "Register", "onRegister", "secondary")
        ]
        
        return Screen(
            screen_id="login",
            name="Login Screen",
            screen_type=ScreenType.LOGIN,
            components=components,
            navigation={
                "next_screen": "dashboard",
                "back_enabled": False
            },
            styles={
                "backgroundColor": "#F2F2F7",
                "padding": "20px"
            },
            created_at=datetime.now()
        )
    
    def create_dashboard_screen(self) -> Screen:
        """Create dashboard screen."""
        components = [
            self.component_factory.create_text("welcome", "Dashboard", "title"),
            self.component_factory.create_card("stats_card", "Statistics", "View your stats"),
            self.component_factory.create_card("recent_card", "Recent Activity", "View recent activity"),
            self.component_factory.create_list("quick_actions", ["Settings", "Profile", "Help"]),
            self.component_factory.create_button("refresh_btn", "Refresh", "onRefresh")
        ]
        
        return Screen(
            screen_id="dashboard",
            name="Dashboard Screen",
            screen_type=ScreenType.DASHBOARD,
            components=components,
            navigation={
                "next_screen": "settings",
                "back_enabled": True,
                "tabs": ["Home", "Activity", "Profile"]
            },
            styles={
                "backgroundColor": "#FFFFFF",
                "padding": "16px"
            },
            created_at=datetime.now()
        )
    
    def create_settings_screen(self) -> Screen:
        """Create settings screen."""
        components = [
            self.component_factory.create_text("title", "Settings", "title"),
            self.component_factory.create_card("account_card", "Account", "Manage your account"),
            self.component_factory.create_card("privacy_card", "Privacy", "Privacy settings"),
            self.component_factory.create_card("notifications_card", "Notifications", "Notification preferences"),
            self.component_factory.create_button("save_btn", "Save Changes", "onSave"),
            self.component_factory.create_button("logout_btn", "Logout", "onLogout", "secondary")
        ]
        
        return Screen(
            screen_id="settings",
            name="Settings Screen",
            screen_type=ScreenType.SETTINGS,
            components=components,
            navigation={
                "next_screen": "profile",
                "back_enabled": True
            },
            styles={
                "backgroundColor": "#F2F2F7",
                "padding": "16px"
            },
            created_at=datetime.now()
        )
    
    def create_profile_screen(self) -> Screen:
        """Create profile screen."""
        components = [
            self.component_factory.create_text("title", "Profile", "title"),
            self.component_factory.create_card("avatar_card", "Profile Picture", "Update your photo"),
            self.component_factory.create_input("name_input", "Full Name"),
            self.component_factory.create_input("email_input", "Email Address"),
            self.component_factory.create_input("bio_input", "Bio"),
            self.component_factory.create_button("update_btn", "Update Profile", "onUpdate"),
            self.component_factory.create_button("cancel_btn", "Cancel", "onCancel", "secondary")
        ]
        
        return Screen(
            screen_id="profile",
            name="Profile Screen",
            screen_type=ScreenType.PROFILE,
            components=components,
            navigation={
                "next_screen": "dashboard",
                "back_enabled": True
            },
            styles={
                "backgroundColor": "#FFFFFF",
                "padding": "16px"
            },
            created_at=datetime.now()
        )


class ScreenManager:
    """Screen management and navigation."""
    
    def __init__(self):
        self.screens = {}
        self.current_screen = None
        self.screen_history = []
        self.factory = ScreenFactory()
    
    def register_screen(self, screen: Screen):
        """Register a screen."""
        self.screens[screen.screen_id] = screen
        print(f"📱 Registered screen: {screen.name}")
    
    def navigate_to(self, screen_id: str) -> bool:
        """Navigate to a specific screen."""
        if screen_id not in self.screens:
            print(f"❌ Screen not found: {screen_id}")
            return False
        
        # Add current screen to history
        if self.current_screen:
            self.screen_history.append(self.current_screen)
        
        # Navigate to new screen
        self.current_screen = screen_id
        print(f"🔄 Navigated to: {self.screens[screen_id].name}")
        return True
    
    def go_back(self) -> bool:
        """Go back to previous screen."""
        if not self.screen_history:
            print("❌ No previous screen")
            return False
        
        previous_screen = self.screen_history.pop()
        self.current_screen = previous_screen
        print(f"⬅️ Went back to: {self.screens[previous_screen].name}")
        return True
    
    def get_current_screen(self) -> Optional[Screen]:
        """Get current screen."""
        if not self.current_screen:
            return None
        return self.screens.get(self.current_screen)
    
    def render_current_screen(self) -> Dict[str, Any]:
        """Render current screen."""
        screen = self.get_current_screen()
        if not screen:
            return {"error": "No current screen"}
        
        return self.factory.renderer.render_screen(screen.components)
    
    def get_screen_list(self) -> List[Dict[str, Any]]:
        """Get list of all screens."""
        return [
            {
                "id": screen_id,
                "name": screen.name,
                "type": screen.screen_type.value,
                "component_count": len(screen.components),
                "created_at": screen.created_at.isoformat()
            }
            for screen_id, screen in self.screens.items()
        ]


class NavigationController:
    """Navigation flow controller."""
    
    def __init__(self):
        self.screen_manager = ScreenManager()
        self.navigation_flows = {
            "onboarding": ["login", "dashboard"],
            "main_app": ["dashboard", "settings", "profile"],
            "settings_flow": ["settings", "profile"]
        }
    
    def initialize_app_screens(self):
        """Initialize all app screens."""
        factory = ScreenFactory()
        
        # Create and register screens
        screens = [
            factory.create_login_screen(),
            factory.create_dashboard_screen(),
            factory.create_settings_screen(),
            factory.create_profile_screen()
        ]
        
        for screen in screens:
            self.screen_manager.register_screen(screen)
        
        # Set initial screen
        self.screen_manager.navigate_to("login")
    
    def execute_navigation_flow(self, flow_name: str) -> bool:
        """Execute a predefined navigation flow."""
        if flow_name not in self.navigation_flows:
            print(f"❌ Unknown flow: {flow_name}")
            return False
        
        flow = self.navigation_flows[flow_name]
        for screen_id in flow:
            if not self.screen_manager.navigate_to(screen_id):
                return False
        
        print(f"✅ Completed flow: {flow_name}")
        return True
    
    def get_navigation_status(self) -> Dict[str, Any]:
        """Get current navigation status."""
        return {
            "current_screen": self.screen_manager.current_screen,
            "screen_history": self.screen_manager.screen_history,
            "total_screens": len(self.screen_manager.screens),
            "available_flows": list(self.navigation_flows.keys())
        }


def main():
    """Main execution function."""
    print("📱 V3-012 UI Screens - Testing...")
    
    # Initialize navigation controller
    nav_controller = NavigationController()
    nav_controller.initialize_app_screens()
    
    # Test navigation
    print("\n🔄 Testing navigation...")
    nav_controller.screen_manager.navigate_to("dashboard")
    nav_controller.screen_manager.navigate_to("settings")
    nav_controller.screen_manager.go_back()
    
    # Test flow execution
    print("\n📋 Testing flows...")
    nav_controller.execute_navigation_flow("main_app")
    
    # Get status
    status = nav_controller.get_navigation_status()
    screen_list = nav_controller.screen_manager.get_screen_list()
    
    print(f"\n📊 Navigation Status:")
    print(f"   Current Screen: {status['current_screen']}")
    print(f"   Total Screens: {status['total_screens']}")
    print(f"   Available Flows: {len(status['available_flows'])}")
    
    print(f"\n📱 Screen List:")
    for screen in screen_list:
        print(f"   - {screen['name']} ({screen['type']}) - {screen['component_count']} components")
    
    print("\n✅ V3-012 UI Screens completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

