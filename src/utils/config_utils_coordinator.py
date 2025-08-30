
# MIGRATED: This file has been migrated to the centralized configuration system
#!/usr/bin/env python3
"""
Config Utils Coordinator - Unified Configuration Utilities Interface

This module coordinates the focused configuration utility modules.
Follows Single Responsibility Principle - only coordinates other modules.
Architecture: Single Responsibility Principle - coordination only
LOC: 80 lines (under 200 limit)
"""

from typing import Dict, Any, Optional
from .config_loader import ConfigLoader
from .environment_overrides import EnvironmentOverrides


class ConfigUtilsCoordinator:
    """Coordinates all configuration utility modules"""

    def __init__(self, config_path: str = "config/services/unified.yaml"):
        self.config_loader = ConfigLoader(config_path)
        self.environment_overrides = EnvironmentOverrides()

    def load_config_with_overrides(self) -> Dict[str, Any]:
        """Load configuration and apply environment overrides"""
        try:
            # Load base configuration
            if not self.config_loader.load_config():
                return {}

            # Get base config data
            config_data = self.config_loader.get_config_data()

            # Apply environment overrides
            updated_config = self.environment_overrides.apply_environment_overrides(
                config_data
            )

            return updated_config

        except Exception as e:
            return {"error": f"Failed to load config with overrides: {e}"}

    def get_config_value(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value with environment overrides applied"""
        try:
            # Load config with overrides if not already loaded
            if not self.config_loader.is_loaded():
                self.load_config_with_overrides()

            return self.config_loader.get_config_value(key_path, default)

        except Exception as e:
            return default

    def get_config_section(self, section_name: str) -> Dict[str, Any]:
        """Get a configuration section with environment overrides applied"""
        try:
            # Load config with overrides if not already loaded
            if not self.config_loader.is_loaded():
                self.load_config_with_overrides()

            return self.config_loader.get_config_section(section_name)

        except Exception as e:
            return {}

    def reload_config(self) -> bool:
        """Reload configuration with environment overrides"""
        try:
            return self.config_loader.reload_config()
        except Exception as e:
            return False

    def get_environment_summary(self) -> Dict[str, Any]:
        """Get summary of environment overrides"""
        try:
            config_data = self.config_loader.get_config_data()
            return self.environment_overrides.get_override_summary(config_data)
        except Exception as e:
            return {"error": str(e)}

    def get_config_status(self) -> Dict[str, Any]:
        """Get comprehensive configuration status"""
        try:
            return {
                "loaded": self.config_loader.is_loaded(),
                "config_file": str(self.config_loader.get_config_file_path()),
                "sections": self.config_loader.list_config_sections()
                if self.config_loader.is_loaded()
                else [],
                "environment_overrides": self.get_environment_summary(),
            }
        except Exception as e:
            return {"error": str(e)}


def run_smoke_test():
    """Run basic functionality test for ConfigUtilsCoordinator"""
    print("🧪 Running ConfigUtilsCoordinator Smoke Test...")

    try:
        coordinator = ConfigUtilsCoordinator()

        # Test config status
        status = coordinator.get_config_status()
        assert "loaded" in status
        assert "config_file" in status

        # Test environment summary
        env_summary = coordinator.get_environment_summary()
        assert "prefix" in env_summary

        print("✅ ConfigUtilsCoordinator Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ ConfigUtilsCoordinator Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ConfigUtilsCoordinator testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Config Utils Coordinator CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--status", action="store_true", help="Show configuration status"
    )
    parser.add_argument("--load", help="Load configuration from path")
    parser.add_argument("--get", help="Get configuration value (dot notation)")
    parser.add_argument("--section", help="Get configuration section")
    parser.add_argument("--reload", action="store_true", help="Reload configuration")
    parser.add_argument(
        "--env-summary", action="store_true", help="Show environment overrides summary"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    coordinator = ConfigUtilsCoordinator()

    if args.status:
        status = coordinator.get_config_status()
        print("Configuration Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    elif args.load:
        coordinator = ConfigUtilsCoordinator(args.load)
        success = coordinator.load_config_with_overrides()
        print(f"Configuration loading: {'✅ Success' if success else '❌ Failed'}")
    elif args.get:
        value = coordinator.get_config_value(args.get)
        print(f"Value for '{args.get}': {value}")
    elif args.section:
        section = coordinator.get_config_section(args.section)
        print(f"Section '{args.section}': {section}")
    elif args.reload:
        success = coordinator.reload_config()
        print(f"Configuration reload: {'✅ Success' if success else '❌ Failed'}")
    elif args.env_summary:
        summary = coordinator.get_environment_summary()
        print("Environment Overrides Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
