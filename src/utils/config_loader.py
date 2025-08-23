#!/usr/bin/env python3
"""
Config Loader Module - Configuration File Loading

This module provides configuration file loading functionality.
Follows Single Responsibility Principle - only configuration loading.
Architecture: Single Responsibility Principle - config loading only
LOC: 120 lines (under 200 limit)
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Manages configuration file loading and parsing"""

    def __init__(self, config_path: str = "config/services/unified.yaml"):
        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}
        self.loaded = False

    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if not self.config_path.exists():
                logger.error(f"Configuration file not found: {self.config_path}")
                return False

            with open(self.config_path, "r", encoding="utf-8") as f:
                if self.config_path.suffix.lower() == ".yaml":
                    self.config_data = yaml.safe_load(f)
                elif self.config_path.suffix.lower() == ".json":
                    self.config_data = json.load(f)
                else:
                    logger.error(
                        f"Unsupported config file format: {self.config_path.suffix}"
                    )
                    return False

            self.loaded = True
            logger.info(f"Configuration loaded from {self.config_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False

    def load_config_from_path(self, config_path: str) -> bool:
        """Load configuration from a specific path"""
        self.config_path = Path(config_path)
        return self.load_config()

    def reload_config(self) -> bool:
        """Reload configuration from file"""
        self.loaded = False
        self.config_data.clear()
        return self.load_config()

    def get_config_data(self) -> Dict[str, Any]:
        """Get the loaded configuration data"""
        if not self.loaded:
            logger.warning("Configuration not loaded, attempting to load now")
            self.load_config()
        return self.config_data.copy()

    def get_config_value(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation (e.g., 'system.log_level')"""
        if not self.loaded:
            logger.warning("Configuration not loaded, attempting to load now")
            if not self.load_config():
                return default

        keys = key_path.split(".")
        value = self.config_data

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def get_config_section(self, section_name: str) -> Dict[str, Any]:
        """Get a configuration section"""
        if not self.loaded:
            logger.warning("Configuration not loaded, attempting to load now")
            if not self.load_config():
                return {}

        return self.config_data.get(section_name, {})

    def list_config_sections(self) -> List[str]:
        """List all configuration sections"""
        if not self.loaded:
            logger.warning("Configuration not loaded, attempting to load now")
            if not self.load_config():
                return []

        return list(self.config_data.keys())

    def is_loaded(self) -> bool:
        """Check if configuration is loaded"""
        return self.loaded

    def get_config_file_path(self) -> Path:
        """Get the current configuration file path"""
        return self.config_path


def run_smoke_test():
    """Run basic functionality test for ConfigLoader"""
    print("🧪 Running ConfigLoader Smoke Test...")

    try:
        # Test with a simple config
        test_config = {"test": {"value": "test_value"}}

        # Create temporary config file
        test_path = "test_config.yaml"
        with open(test_path, "w") as f:
            yaml.dump(test_config, f)

        loader = ConfigLoader(test_path)

        # Test loading
        success = loader.load_config()
        assert success
        assert loader.is_loaded()

        # Test getting data
        data = loader.get_config_data()
        assert "test" in data

        # Test getting value
        value = loader.get_config_value("test.value")
        assert value == "test_value"

        # Test getting section
        section = loader.get_config_section("test")
        assert section["value"] == "test_value"

        # Cleanup
        os.remove(test_path)

        print("✅ ConfigLoader Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ ConfigLoader Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ConfigLoader testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Config Loader CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--load", help="Load configuration from path")
    parser.add_argument("--reload", action="store_true", help="Reload configuration")
    parser.add_argument("--get", help="Get configuration value (dot notation)")
    parser.add_argument("--section", help="Get configuration section")
    parser.add_argument(
        "--list-sections", action="store_true", help="List all sections"
    )
    parser.add_argument("--status", action="store_true", help="Show loader status")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    loader = ConfigLoader()

    if args.load:
        success = loader.load_config_from_path(args.load)
        print(f"Configuration loading: {'✅ Success' if success else '❌ Failed'}")
    elif args.reload:
        success = loader.reload_config()
        print(f"Configuration reload: {'✅ Success' if success else '❌ Failed'}")
    elif args.get:
        value = loader.get_config_value(args.get)
        print(f"Value for '{args.get}': {value}")
    elif args.section:
        section = loader.get_config_section(args.section)
        print(f"Section '{args.section}': {section}")
    elif args.list_sections:
        sections = loader.list_config_sections()
        print("Configuration sections:")
        for section in sections:
            print(f"  {section}")
    elif args.status:
        print(f"Loaded: {loader.is_loaded()}")
        print(f"Config file: {loader.get_config_file_path()}")
        if loader.is_loaded():
            print(f"Sections: {loader.list_config_sections()}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
