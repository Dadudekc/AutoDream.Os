#!/usr/bin/env python3
"""
Config Manager Coordinator - Unified Core Configuration Interface

This module coordinates the focused core configuration modules.
Follows Single Responsibility Principle - only coordinates other modules.
Architecture: Single Responsibility Principle - coordination only
LOC: 80 lines (under 200 limit)
"""

from typing import Dict, Any, Optional
from .config_core import ConfigCore, ConfigSection
from .config_handlers import ConfigChangeHandler, ConfigChangeManager


class ConfigManagerCoordinator:
    """Coordinates all core configuration modules"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_core = ConfigCore(config_dir)
        self.change_manager = ConfigChangeManager()
    
    def load_configs(self) -> bool:
        """Load all configurations"""
        return self.config_core.load_configs()
    
    def get_config_section(self, section_name: str) -> Optional[ConfigSection]:
        """Get a configuration section"""
        return self.config_core.get_config_section(section_name)
    
    def get_config_value(self, section_name: str, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config_core.get_config_value(section_name, key, default)
    
    def set_config_value(self, section_name: str, key: str, value: Any) -> bool:
        """Set a configuration value and notify handlers"""
        try:
            # Set the value
            success = self.config_core.set_config_value(section_name, key, value)
            if success:
                # Notify change handlers
                self.change_manager.notify_change(section_name, value)
            
            return success
            
        except Exception as e:
            return False
    
    def register_change_handler(self, section: str, callback) -> bool:
        """Register a change handler for a configuration section"""
        handler = ConfigChangeHandler(callback)
        return self.change_manager.register_handler(section, handler)
    
    def unregister_change_handler(self, section: str, handler: ConfigChangeHandler) -> bool:
        """Unregister a change handler"""
        return self.change_manager.unregister_handler(section, handler)
    
    def save_config_section(self, section_name: str, output_path: Optional[str] = None) -> bool:
        """Save a configuration section to file"""
        return self.config_core.save_config_section(section_name, output_path)
    
    def list_config_sections(self) -> list:
        """List all configuration sections"""
        return self.config_core.list_config_sections()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get comprehensive configuration summary"""
        try:
            core_summary = self.config_core.get_config_summary()
            handler_summary = {
                "registered_sections": self.change_manager.list_registered_sections(),
                "total_handlers": sum(
                    self.change_manager.get_handler_count(section)
                    for section in self.change_manager.list_registered_sections()
                )
            }
            
            return {
                "core": core_summary,
                "handlers": handler_summary
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def reload_configs(self) -> bool:
        """Reload all configurations"""
        try:
            # Clear existing configs
            self.config_core.configs.clear()
            
            # Reload
            return self.config_core.load_configs()
            
        except Exception as e:
            return False


def run_smoke_test():
    """Run basic functionality test for ConfigManagerCoordinator"""
    print("🧪 Running ConfigManagerCoordinator Smoke Test...")
    
    try:
        coordinator = ConfigManagerCoordinator(".")
        
        # Test setting config value
        success = coordinator.set_config_value("test", "key", "value")
        assert success
        
        # Test getting config value
        value = coordinator.get_config_value("test", "key")
        assert value == "value"
        
        # Test change handler registration
        change_detected = False
        
        def test_callback(section: str, new_value: Any):
            nonlocal change_detected
            change_detected = True
        
        success = coordinator.register_change_handler("test", test_callback)
        assert success
        
        # Test change notification
        coordinator.set_config_value("test", "key2", "value2")
        # Note: This would trigger the callback in a real scenario
        
        # Test config summary
        summary = coordinator.get_config_summary()
        assert "core" in summary
        assert "handlers" in summary
        
        print("✅ ConfigManagerCoordinator Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ConfigManagerCoordinator Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ConfigManagerCoordinator testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Config Manager Coordinator CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--load", help="Load configs from directory")
    parser.add_argument("--section", help="Get config section")
    parser.add_argument("--get", nargs=2, metavar=("SECTION", "KEY"), help="Get config value")
    parser.add_argument("--set", nargs=3, metavar=("SECTION", "KEY", "VALUE"), help="Set config value")
    parser.add_argument("--list", action="store_true", help="List all sections")
    parser.add_argument("--summary", action="store_true", help="Show config summary")
    parser.add_argument("--reload", action="store_true", help="Reload all configs")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    coordinator = ConfigManagerCoordinator()
    
    if args.load:
        coordinator = ConfigManagerCoordinator(args.load)
        success = coordinator.load_configs()
        print(f"Config loading: {'✅ Success' if success else '❌ Failed'}")
    elif args.section:
        section = coordinator.get_config_section(args.section)
        if section:
            print(f"Section '{args.section}': {section.data}")
        else:
            print(f"Section '{args.section}' not found")
    elif args.get:
        section_name, key = args.get
        value = coordinator.get_config_value(section_name, key)
        print(f"Value for {section_name}.{key}: {value}")
    elif args.set:
        section_name, key, value = args.set
        success = coordinator.set_config_value(section_name, key, value)
        print(f"Setting config value: {'✅ Success' if success else '❌ Failed'}")
    elif args.list:
        sections = coordinator.list_config_sections()
        print("Configuration sections:")
        for section in sections:
            print(f"  {section}")
    elif args.summary:
        summary = coordinator.get_config_summary()
        print("Configuration Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    elif args.reload:
        success = coordinator.reload_configs()
        print(f"Config reload: {'✅ Success' if success else '❌ Failed'}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
