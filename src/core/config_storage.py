#!/usr/bin/env python3
"""
Config Storage Module - Configuration Storage and Retrieval Operations

This module handles configuration storage, retrieval, and persistence.
Follows Single Responsibility Principle - only storage operations.
Architecture: Single Responsibility Principle - storage only
LOC: 120 lines (under 200 limit)
"""

import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging

from .config_models import ConfigSection, ConfigType, ConfigValidationLevel

logger = logging.getLogger(__name__)


# ConfigSection now imported from unified config_models


class ConfigStorage:
    """
    Configuration storage and retrieval system

    Responsibilities:
    - Configuration data storage
    - Value retrieval and setting
    - Configuration persistence
    """

    def __init__(self):
        self.configs: Dict[str, ConfigSection] = {}
        self.logger = logging.getLogger(f"{__name__}.ConfigStorage")

    def store_config_section(self, section: ConfigSection) -> bool:
        """Store a configuration section"""
        try:
            self.configs[section.name] = section
            self.logger.info(f"Stored config section: {section.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to store config section {section.name}: {e}")
            return False

    def get_config_section(self, section_name: str) -> Optional[ConfigSection]:
        """Get a configuration section by name"""
        return self.configs.get(section_name)

    def get_config_value(self, section_name: str, key: str, default: Any = None) -> Any:
        """Get a configuration value from a specific section"""
        section = self.get_config_section(section_name)
        if not section:
            return default

        return section.data.get(key, default)

    def set_config_value(self, section_name: str, key: str, value: Any) -> bool:
        """Set a configuration value in a specific section"""
        try:
            if section_name not in self.configs:
                # Create new section if it doesn't exist
                self.configs[section_name] = ConfigSection(
                    name=section_name, data={}, source_file=None, last_modified=None
                )

            self.configs[section_name].data[key] = value
            self.logger.info(f"Set config value: {section_name}.{key} = {value}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to set config value: {e}")
            return False

    def remove_config_section(self, section_name: str) -> bool:
        """Remove a configuration section"""
        try:
            if section_name in self.configs:
                del self.configs[section_name]
                self.logger.info(f"Removed config section: {section_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove config section {section_name}: {e}")
            return False

    def list_config_sections(self) -> list:
        """List all configuration section names"""
        return list(self.configs.keys())

    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of all configuration sections"""
        summary = {}
        for section_name, section in self.configs.items():
            summary[section_name] = {
                "keys_count": len(section.data),
                "source_file": section.source_file,
                "last_modified": section.last_modified,
            }
        return summary

    def save_config_section(
        self, section_name: str, output_path: Optional[str] = None
    ) -> bool:
        """Save a configuration section to file"""
        try:
            section = self.get_config_section(section_name)
            if not section:
                return False

            if not output_path:
                output_path = f"{section_name}.yaml"

            output_file = Path(output_path)

            with open(output_file, "w", encoding="utf-8") as f:
                yaml.dump(section.data, f, default_flow_style=False, indent=2)

            self.logger.info(f"Saved config section {section_name} to {output_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save config section {section_name}: {e}")
            return False

    def clear_all_configs(self) -> bool:
        """Clear all stored configurations"""
        try:
            self.configs.clear()
            self.logger.info("Cleared all configurations")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear configurations: {e}")
            return False


def run_smoke_test():
    """Run basic functionality test for ConfigStorage"""
    print("🧪 Running ConfigStorage Smoke Test...")

    try:
        storage = ConfigStorage()

        # Test setting config value
        success = storage.set_config_value("test", "key", "value")
        assert success

        # Test getting config value
        value = storage.get_config_value("test", "key")
        assert value == "value"

        # Test getting section
        section = storage.get_config_section("test")
        assert section is not None
        assert section.name == "test"

        # Test listing sections
        sections = storage.list_config_sections()
        assert "test" in sections

        # Test summary
        summary = storage.get_config_summary()
        assert "test" in summary

        print("✅ ConfigStorage Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ ConfigStorage Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ConfigStorage testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Config Storage CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--set", nargs=3, metavar=("SECTION", "KEY", "VALUE"), help="Set config value"
    )
    parser.add_argument(
        "--get", nargs=2, metavar=("SECTION", "KEY"), help="Get config value"
    )
    parser.add_argument("--section", help="Get config section")
    parser.add_argument("--list", action="store_true", help="List all sections")
    parser.add_argument("--summary", action="store_true", help="Show config summary")
    parser.add_argument(
        "--save", nargs=2, metavar=("SECTION", "PATH"), help="Save section to file"
    )
    parser.add_argument("--clear", action="store_true", help="Clear all configs")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    storage = ConfigStorage()

    if args.set:
        section_name, key, value = args.set
        success = storage.set_config_value(section_name, key, value)
        print(f"Setting config value: {'✅ Success' if success else '❌ Failed'}")
    elif args.get:
        section_name, key = args.get
        value = storage.get_config_value(section_name, key)
        print(f"Value for {section_name}.{key}: {value}")
    elif args.section:
        section = storage.get_config_section(args.section)
        if section:
            print(f"Section '{args.section}': {section.data}")
        else:
            print(f"Section '{args.section}' not found")
    elif args.list:
        sections = storage.list_config_sections()
        print("Configuration sections:")
        for section in sections:
            print(f"  {section}")
    elif args.summary:
        summary = storage.get_config_summary()
        print("Configuration Summary:")
        for section, info in summary.items():
            print(f"  {section}: {info['keys_count']} keys")
    elif args.save:
        section_name, output_path = args.save
        success = storage.save_config_section(section_name, output_path)
        print(f"Saving config section: {'✅ Success' if success else '❌ Failed'}")
    elif args.clear:
        success = storage.clear_all_configs()
        print(f"Clearing configs: {'✅ Success' if success else '❌ Failed'}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
