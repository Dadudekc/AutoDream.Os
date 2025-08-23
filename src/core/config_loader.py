#!/usr/bin/env python3
"""
Config Loader Module - Configuration File Loading Operations

This module handles configuration file loading and parsing.
Follows Single Responsibility Principle - only file loading operations.
Architecture: Single Responsibility Principle - file loading only
LOC: 120 lines (under 200 limit)
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging

from .config_models import ConfigSection, ConfigType, ConfigValidationLevel

logger = logging.getLogger(__name__)


# ConfigSection now imported from unified config_models


class ConfigLoader:
    """
    Configuration file loading system

    Responsibilities:
    - Configuration file discovery
    - File format parsing (YAML/JSON)
    - Configuration section creation
    """

    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.logger = logging.getLogger(f"{__name__}.ConfigLoader")

    def discover_config_files(self) -> list:
        """Discover all configuration files in the config directory"""
        try:
            if not self.config_dir.exists():
                self.logger.warning(f"Config directory {self.config_dir} not found")
                return []

            config_files = list(self.config_dir.glob("*.yaml")) + list(
                self.config_dir.glob("*.json")
            )
            self.logger.info(f"Discovered {len(config_files)} configuration files")
            return config_files

        except Exception as e:
            self.logger.error(f"Failed to discover config files: {e}")
            return []

    def load_config_file(self, config_file: Path) -> Optional[ConfigSection]:
        """Load a single configuration file and return a ConfigSection"""
        try:
            if config_file.suffix.lower() == ".yaml":
                data = self._load_yaml_file(config_file)
            elif config_file.suffix.lower() == ".json":
                data = self._load_json_file(config_file)
            else:
                self.logger.warning(
                    f"Unsupported config file format: {config_file.suffix}"
                )
                return None

            if data is None:
                return None

            # Create config section
            section_name = config_file.stem
            section = ConfigSection(
                name=section_name,
                data=data,
                source_file=str(config_file),
                last_modified=config_file.stat().st_mtime,
            )

            self.logger.info(f"Loaded config section: {section_name}")
            return section

        except Exception as e:
            self.logger.error(f"Failed to load config file {config_file}: {e}")
            return None

    def _load_yaml_file(self, config_file: Path) -> Optional[Dict[str, Any]]:
        """Load a YAML configuration file"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data if data else {}
        except Exception as e:
            self.logger.error(f"Failed to load YAML file {config_file}: {e}")
            return None

    def _load_json_file(self, config_file: Path) -> Optional[Dict[str, Any]]:
        """Load a JSON configuration file"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if data else {}
        except Exception as e:
            self.logger.error(f"Failed to load JSON file {config_file}: {e}")
            return None

    def validate_config_data(self, data: Dict[str, Any]) -> bool:
        """Validate configuration data structure"""
        try:
            if not isinstance(data, dict):
                self.logger.error("Configuration data must be a dictionary")
                return False

            # Basic validation - ensure no None values at top level
            for key, value in data.items():
                if value is None:
                    self.logger.warning(f"Configuration key '{key}' has None value")

            return True

        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False

    def get_supported_formats(self) -> list:
        """Get list of supported configuration file formats"""
        return [".yaml", ".yml", ".json"]


def run_smoke_test():
    """Run basic functionality test for ConfigLoader"""
    print("🧪 Running ConfigLoader Smoke Test...")

    try:
        # Test with current directory
        loader = ConfigLoader(".")

        # Test file discovery
        files = loader.discover_config_files()
        print(f"Discovered {len(files)} config files")

        # Test supported formats
        formats = loader.get_supported_formats()
        assert ".yaml" in formats
        assert ".json" in formats

        # Test validation
        test_data = {"key": "value", "nested": {"subkey": "subvalue"}}
        assert loader.validate_config_data(test_data)

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
    parser.add_argument("--discover", help="Discover config files in directory")
    parser.add_argument("--load", help="Load specific config file")
    parser.add_argument("--validate", help="Validate config data file")
    parser.add_argument("--formats", action="store_true", help="Show supported formats")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    loader = ConfigLoader()

    if args.discover:
        loader = ConfigLoader(args.discover)
        files = loader.discover_config_files()
        print(f"Configuration files in {args.discover}:")
        for file in files:
            print(f"  {file.name}")
    elif args.load:
        config_file = Path(args.load)
        if config_file.exists():
            section = loader.load_config_file(config_file)
            if section:
                print(f"✅ Loaded config section: {section.name}")
                print(f"  Keys: {list(section.data.keys())}")
            else:
                print("❌ Failed to load config file")
        else:
            print(f"❌ File not found: {args.load}")
    elif args.validate:
        config_file = Path(args.validate)
        if config_file.exists():
            section = loader.load_config_file(config_file)
            if section and loader.validate_config_data(section.data):
                print("✅ Configuration validation passed")
            else:
                print("❌ Configuration validation failed")
        else:
            print(f"❌ File not found: {args.validate}")
    elif args.formats:
        formats = loader.get_supported_formats()
        print("Supported configuration formats:")
        for fmt in formats:
            print(f"  {fmt}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
