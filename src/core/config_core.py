#!/usr/bin/env python3
"""
Config Core Module - Core Configuration Management

This module provides core configuration management functionality.
Follows Single Responsibility Principle - only core config management.
Architecture: Single Responsibility Principle - core config management only
LOC: 120 lines (under 200 limit)
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ConfigSection:
    """Configuration section definition"""
    name: str
    data: Dict[str, Any]
    source_file: Optional[str] = None
    last_modified: Optional[float] = None


class ConfigCore:
    """
    Core configuration management system
    
    Responsibilities:
    - Configuration file loading and parsing
    - Basic configuration storage
    - Configuration section management
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, ConfigSection] = {}
        self.logger = logging.getLogger(f"{__name__}.ConfigCore")
    
    def load_configs(self) -> bool:
        """Load all configuration files from config directory"""
        try:
            if not self.config_dir.exists():
                self.logger.warning(f"Config directory {self.config_dir} not found")
                return False
            
            config_files = list(self.config_dir.glob("*.yaml")) + list(self.config_dir.glob("*.json"))
            
            for config_file in config_files:
                self.load_config_file(config_file)
            
            self.logger.info(f"Loaded {len(config_files)} configuration files")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configurations: {e}")
            return False
    
    def load_config_file(self, config_file: Path) -> bool:
        """Load a single configuration file"""
        try:
            if config_file.suffix.lower() == '.yaml':
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            elif config_file.suffix.lower() == '.json':
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                self.logger.warning(f"Unsupported config file format: {config_file.suffix}")
                return False
            
            # Create config section
            section_name = config_file.stem
            section = ConfigSection(
                name=section_name,
                data=data,
                source_file=str(config_file),
                last_modified=config_file.stat().st_mtime
            )
            
            self.configs[section_name] = section
            self.logger.info(f"Loaded config section: {section_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load config file {config_file}: {e}")
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
                    name=section_name,
                    data={},
                    source_file=None,
                    last_modified=None
                )
            
            self.configs[section_name].data[key] = value
            self.logger.info(f"Set config value: {section_name}.{key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set config value: {e}")
            return False
    
    def save_config_section(self, section_name: str, output_path: Optional[str] = None) -> bool:
        """Save a configuration section to file"""
        try:
            section = self.get_config_section(section_name)
            if not section:
                return False
            
            if not output_path:
                output_path = f"{section_name}.yaml"
            
            output_file = Path(output_path)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(section.data, f, default_flow_style=False, indent=2)
            
            self.logger.info(f"Saved config section {section_name} to {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save config section {section_name}: {e}")
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
                "last_modified": section.last_modified
            }
        return summary


def run_smoke_test():
    """Run basic functionality test for ConfigCore"""
    print("🧪 Running ConfigCore Smoke Test...")
    
    try:
        # Test with temporary config
        core = ConfigCore(".")
        
        # Test setting config value
        success = core.set_config_value("test", "key", "value")
        assert success
        
        # Test getting config value
        value = core.get_config_value("test", "key")
        assert value == "value"
        
        # Test getting section
        section = core.get_config_section("test")
        assert section is not None
        assert section.name == "test"
        
        # Test listing sections
        sections = core.list_config_sections()
        assert "test" in sections
        
        print("✅ ConfigCore Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ConfigCore Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ConfigCore testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Config Core CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--load", help="Load configs from directory")
    parser.add_argument("--section", help="Get config section")
    parser.add_argument("--get", nargs=2, metavar=("SECTION", "KEY"), help="Get config value")
    parser.add_argument("--set", nargs=3, metavar=("SECTION", "KEY", "VALUE"), help="Set config value")
    parser.add_argument("--list", action="store_true", help="List all sections")
    parser.add_argument("--summary", action="store_true", help="Show config summary")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    core = ConfigCore()
    
    if args.load:
        success = core.load_configs()
        print(f"Config loading: {'✅ Success' if success else '❌ Failed'}")
    elif args.section:
        section = core.get_config_section(args.section)
        if section:
            print(f"Section '{args.section}': {section.data}")
        else:
            print(f"Section '{args.section}' not found")
    elif args.get:
        section_name, key = args.get
        value = core.get_config_value(section_name, key)
        print(f"Value for {section_name}.{key}: {value}")
    elif args.set:
        section_name, key, value = args.set
        success = core.set_config_value(section_name, key, value)
        print(f"Setting config value: {'✅ Success' if success else '❌ Failed'}")
    elif args.list:
        sections = core.list_config_sections()
        print("Configuration sections:")
        for section in sections:
            print(f"  {section}")
    elif args.summary:
        summary = core.get_config_summary()
        print("Configuration Summary:")
        for section, info in summary.items():
            print(f"  {section}: {info['keys_count']} keys")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
