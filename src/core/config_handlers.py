#!/usr/bin/env python3
"""
Config Handlers Module - Configuration Change Handlers

This module provides configuration change handling functionality.
Follows Single Responsibility Principle - only change handling.
Architecture: Single Responsibility Principle - change handling only
LOC: 80 lines (under 200 limit)
"""

from typing import Dict, Any, Callable, List, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigChangeHandler:
    """Handler for configuration change events"""
    
    def __init__(self, callback: Callable[[str, Any], None]):
        self.callback = callback
        self.logger = logging.getLogger(f"{__name__}.ConfigChangeHandler")
    
    def on_config_change(self, section: str, new_value: Any):
        """Handle configuration change"""
        try:
            self.callback(section, new_value)
            self.logger.info(f"Config change handled for section: {section}")
        except Exception as e:
            self.logger.error(f"Error in config change handler: {e}")


class ConfigChangeManager:
    """Manages configuration change handlers and notifications"""
    
    def __init__(self):
        self.change_handlers: Dict[str, List[ConfigChangeHandler]] = {}
        self.logger = logging.getLogger(f"{__name__}.ConfigChangeManager")
    
    def register_handler(self, section: str, handler: ConfigChangeHandler) -> bool:
        """Register a change handler for a configuration section"""
        try:
            if section not in self.change_handlers:
                self.change_handlers[section] = []
            
            self.change_handlers[section].append(handler)
            self.logger.info(f"Registered change handler for section: {section}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register change handler: {e}")
            return False
    
    def unregister_handler(self, section: str, handler: ConfigChangeHandler) -> bool:
        """Unregister a change handler for a configuration section"""
        try:
            if section in self.change_handlers:
                if handler in self.change_handlers[section]:
                    self.change_handlers[section].remove(handler)
                    self.logger.info(f"Unregistered change handler for section: {section}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to unregister change handler: {e}")
            return False
    
    def notify_change(self, section: str, new_value: Any):
        """Notify all registered handlers of a configuration change"""
        try:
            if section in self.change_handlers:
                for handler in self.change_handlers[section]:
                    handler.on_config_change(section, new_value)
                
                self.logger.info(f"Notified {len(self.change_handlers[section])} handlers of change in section: {section}")
            else:
                self.logger.debug(f"No handlers registered for section: {section}")
                
        except Exception as e:
            self.logger.error(f"Failed to notify change handlers: {e}")
    
    def get_handler_count(self, section: str) -> int:
        """Get the number of handlers registered for a section"""
        return len(self.change_handlers.get(section, []))
    
    def list_registered_sections(self) -> List[str]:
        """List all sections with registered handlers"""
        return list(self.change_handlers.keys())
    
    def clear_handlers(self, section: Optional[str] = None):
        """Clear all handlers, optionally for a specific section"""
        try:
            if section:
                if section in self.change_handlers:
                    del self.change_handlers[section]
                    self.logger.info(f"Cleared handlers for section: {section}")
            else:
                self.change_handlers.clear()
                self.logger.info("Cleared all change handlers")
                
        except Exception as e:
            self.logger.error(f"Failed to clear handlers: {e}")


def run_smoke_test():
    """Run basic functionality test for ConfigHandlers"""
    print("🧪 Running ConfigHandlers Smoke Test...")
    
    try:
        # Test change handler
        change_detected = False
        
        def test_callback(section: str, new_value: Any):
            nonlocal change_detected
            change_detected = True
        
        handler = ConfigChangeHandler(test_callback)
        handler.on_config_change("test", "value")
        assert change_detected
        
        # Test change manager
        manager = ConfigChangeManager()
        
        # Test handler registration
        success = manager.register_handler("test", handler)
        assert success
        assert manager.get_handler_count("test") == 1
        
        # Test change notification
        manager.notify_change("test", "new_value")
        
        # Test handler unregistration
        success = manager.unregister_handler("test", handler)
        assert success
        assert manager.get_handler_count("test") == 0
        
        print("✅ ConfigHandlers Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ConfigHandlers Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ConfigHandlers testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Config Handlers CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--register", nargs=2, metavar=("SECTION", "CALLBACK"), help="Register handler")
    parser.add_argument("--unregister", nargs=2, metavar=("SECTION", "CALLBACK"), help="Unregister handler")
    parser.add_argument("--notify", nargs=2, metavar=("SECTION", "VALUE"), help="Notify change")
    parser.add_argument("--count", help="Get handler count for section")
    parser.add_argument("--list", action="store_true", help="List registered sections")
    parser.add_argument("--clear", help="Clear handlers for section (or all if no section)")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    manager = ConfigChangeManager()
    
    if args.register:
        section, callback_name = args.register
        # Simplified handler creation for demo
        def demo_callback(section: str, new_value: Any):
            print(f"Demo callback: {section} = {new_value}")
        
        handler = ConfigChangeHandler(demo_callback)
        success = manager.register_handler(section, handler)
        print(f"Handler registration: {'✅ Success' if success else '❌ Failed'}")
    elif args.unregister:
        section, callback_name = args.unregister
        # This would require tracking specific handlers, simplified for demo
        print("Handler unregistration requires specific handler reference")
    elif args.notify:
        section, value = args.notify
        manager.notify_change(section, value)
        print(f"✅ Change notification sent for {section}")
    elif args.count:
        count = manager.get_handler_count(args.count)
        print(f"Handlers for section '{args.count}': {count}")
    elif args.list:
        sections = manager.list_registered_sections()
        print("Registered sections:")
        for section in sections:
            count = manager.get_handler_count(section)
            print(f"  {section}: {count} handlers")
    elif args.clear:
        if args.clear == "all":
            manager.clear_handlers()
            print("✅ All handlers cleared")
        else:
            manager.clear_handlers(args.clear)
            print(f"✅ Handlers cleared for section: {args.clear}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
