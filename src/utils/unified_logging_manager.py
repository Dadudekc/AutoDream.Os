#!/usr/bin/env python3
"""
Unified Logging Manager - Centralized Logging Configuration

This module provides unified logging configuration for the entire Agent Cellphone V2 system.
Replaces all hardcoded debug flags and scattered logging.basicConfig() calls.

Follows Single Responsibility Principle - only logging management.
Architecture: Single Responsibility Principle - logging management only
LOC: 180 lines (under 400 limit)
"""

import os
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml
from src.utils.stability_improvements import stability_manager, safe_import


class UnifiedLoggingManager:
    """Unified logging manager for the entire system"""
    
    def __init__(self, config_file: str = "config/logging.yaml"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.loggers: Dict[str, logging.Logger] = {}
        self._setup_global_logging()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load logging configuration from YAML file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return yaml.safe_load(f) or {}
            else:
                print(f"⚠️  Logging config not found: {self.config_file}")
                return self._get_default_config()
        except Exception as e:
            print(f"❌ Failed to load logging config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default logging configuration"""
        return {
            "global": {
                "level": "INFO",
                "format": "%(asctime)s | %(name)s | %(levelname)8s | %(message)s",
                "date_format": "%Y-%m-%d %H:%M:%S"
            },
            "environments": {
                "development": {"level": "DEBUG", "console": True, "file": False},
                "production": {"level": "WARNING", "console": False, "file": True},
                "testing": {"level": "DEBUG", "console": True, "file": True}
            },
            "debug": {
                "enabled": False,
                "flask_debug": False,
                "verbose_logging": False
            }
        }
    
    def _setup_global_logging(self):
        """Setup global logging configuration"""
        try:
            # Get environment
            env = os.getenv("ENVIRONMENT", "development")
            env_config = self.config.get("environments", {}).get(env, {})
            
            # Get log level from environment or config
            log_level = os.getenv("LOG_LEVEL") or env_config.get("level") or self.config.get("global", {}).get("level", "INFO")
            numeric_level = getattr(logging, log_level.upper(), logging.INFO)
            
            # Clear existing handlers
            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
            
            # Setup basic configuration
            logging.basicConfig(
                level=numeric_level,
                format=self.config.get("global", {}).get("format", "%(asctime)s | %(levelname)8s | %(message)s"),
                datefmt=self.config.get("global", {}).get("date_format", "%Y-%m-%d %H:%M:%S")
            )
            
            # Add console handler if enabled
            if env_config.get("console", True):
                self._add_console_handler(root_logger, env_config)
            
            # Add file handler if enabled
            if env_config.get("file", False):
                file_path = env_config.get("file_path", f"logs/{env}.log")
                self._add_file_handler(root_logger, file_path)
            
            print(f"✅ Unified logging configured: {env} environment, level={log_level}")
            
        except Exception as e:
            print(f"❌ Failed to setup global logging: {e}")
            # Fallback to basic logging
            logging.basicConfig(level=logging.INFO)
    
    def _add_console_handler(self, logger: logging.Logger, env_config: Dict[str, Any]):
        """Add console handler to logger"""
        try:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, env_config.get("level", "INFO").upper(), logging.INFO))
            
            formatter = logging.Formatter(
                self.config.get("global", {}).get("format", "%(asctime)s | %(levelname)8s | %(message)s"),
                datefmt=self.config.get("global", {}).get("date_format", "%Y-%m-%d %H:%M:%S")
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
        except Exception as e:
            print(f"❌ Failed to add console handler: {e}")
    
    def _add_file_handler(self, logger: logging.Logger, file_path: str):
        """Add file handler to logger"""
        try:
            # Ensure log directory exists
            log_path = Path(file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                file_path,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            
            formatter = logging.Formatter(
                self.config.get("global", {}).get("format", "%(asctime)s | %(levelname)8s | %(message)s"),
                datefmt=self.config.get("global", {}).get("date_format", "%Y-%m-%d %H:%M:%S")
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        except Exception as e:
            print(f"❌ Failed to add file handler: {e}")
    
    def get_logger(self, name: str, level: Optional[str] = None) -> logging.Logger:
        """Get a configured logger instance"""
        if name in self.loggers:
            return self.loggers[name]
        
        logger = logging.getLogger(name)
        
        # Set level from module config or default
        if level:
            logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        else:
            module_level = self._get_module_level(name)
            logger.setLevel(module_level)
        
        # Don't propagate to root logger to avoid duplicate messages
        logger.propagate = False
        
        # Add handlers if logger doesn't have any
        if not logger.handlers:
            self._add_logger_handlers(logger, name)
        
        self.loggers[name] = logger
        return logger
    
    def _get_module_level(self, name: str) -> int:
        """Get log level for specific module"""
        try:
            modules_config = self.config.get("modules", {})
            
            # Find matching module configuration
            for module_prefix, module_config in modules_config.items():
                if name.startswith(module_prefix):
                    level_str = module_config.get("level", "INFO")
                    return getattr(logging, level_str.upper(), logging.INFO)
            
            # Default to global level
            global_level = self.config.get("global", {}).get("level", "INFO")
            return getattr(logging, global_level.upper(), logging.INFO)
            
        except Exception:
            return logging.INFO
    
    def _add_logger_handlers(self, logger: logging.Logger, name: str):
        """Add appropriate handlers to logger based on module configuration"""
        try:
            modules_config = self.config.get("modules", {})
            
            # Find module configuration
            module_config = None
            for module_prefix, config in modules_config.items():
                if name.startswith(module_prefix):
                    module_config = config
                    break
            
            if not module_config:
                # Use default handlers
                self._add_console_handler(logger, {"level": "INFO"})
                return
            
            # Add configured handlers
            handlers = module_config.get("handlers", ["console"])
            
            if "console" in handlers:
                self._add_console_handler(logger, {"level": module_config.get("level", "INFO")})
            
            if "file" in handlers:
                file_path = f"logs/{name.replace('.', '_')}.log"
                self._add_file_handler(logger, file_path)
                
        except Exception as e:
            print(f"❌ Failed to add logger handlers: {e}")
            # Fallback to console handler
            self._add_console_handler(logger, {"level": "INFO"})
    
    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled"""
        return os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    def get_flask_debug(self) -> bool:
        """Get Flask debug setting (replaces hardcoded app.run(debug=True))"""
        if self.is_debug_enabled():
            return self.config.get("debug", {}).get("flask_debug", False)
        return False
    
    def set_debug_mode(self, enabled: bool):
        """Set debug mode (updates environment variable)"""
        os.environ["DEBUG_MODE"] = str(enabled).lower()
        print(f"🔧 Debug mode {'enabled' if enabled else 'disabled'}")
    
    def reload_config(self):
        """Reload logging configuration"""
        self.config = self._load_config()
        self._setup_global_logging()
        # Clear cached loggers to force recreation
        self.loggers.clear()
        print("🔄 Logging configuration reloaded")


# Global logging manager instance
unified_logging_manager = UnifiedLoggingManager()


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance (convenience function)"""
    return unified_logging_manager.get_logger(name, level)


def is_debug_enabled() -> bool:
    """Check if debug mode is enabled (convenience function)"""
    return unified_logging_manager.is_debug_enabled()


def get_flask_debug() -> bool:
    """Get Flask debug setting (convenience function)"""
    return unified_logging_manager.get_flask_debug()


def set_debug_mode(enabled: bool):
    """Set debug mode (convenience function)"""
    unified_logging_manager.set_debug_mode(enabled)


def reload_logging_config():
    """Reload logging configuration (convenience function)"""
    unified_logging_manager.reload_config()


def run_smoke_test():
    """Run basic functionality test for UnifiedLoggingManager"""
    print("🧪 Running UnifiedLoggingManager Smoke Test...")
    
    try:
        # Test logger creation
        logger = get_logger("test_logger", "DEBUG")
        assert logger.name == "test_logger"
        assert logger.level == logging.DEBUG
        
        # Test debug mode
        set_debug_mode(True)
        assert is_debug_enabled() == True
        
        set_debug_mode(False)
        assert is_debug_enabled() == False
        
        # Test Flask debug setting
        flask_debug = get_flask_debug()
        assert isinstance(flask_debug, bool)
        
        print("✅ UnifiedLoggingManager Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ UnifiedLoggingManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for UnifiedLoggingManager testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified Logging Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--reload", action="store_true", help="Reload configuration")
    parser.add_argument("--get-logger", help="Get logger with name")
    parser.add_argument("--flask-debug", action="store_true", help="Check Flask debug setting")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    if args.debug:
        set_debug_mode(True)
        print("🔧 Debug mode enabled")
    
    if args.reload:
        reload_logging_config()
        return
    
    if args.get_logger:
        logger = get_logger(args.get_logger)
        print(f"✅ Logger '{args.get_logger}' created with level {logger.level}")
    
    if args.flask_debug:
        flask_debug = get_flask_debug()
        print(f"🔧 Flask debug setting: {flask_debug}")
    
    if not any([args.test, args.debug, args.reload, args.get_logger, args.flask_debug]):
        parser.print_help()


if __name__ == "__main__":
    main()
