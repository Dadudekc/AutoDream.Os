#!/usr/bin/env python3
"""
Core Manager - Agent Cellphone V2
=================================

Core business logic manager with strict OOP design and CLI testing interface.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional


class CoreManager:
    """
    Core Manager - Single responsibility: Core system management and coordination.

    This class manages the core system functionality including:
    - System initialization
    - Configuration management
    - Component coordination
    - Health monitoring
    """

    def __init__(self, config_path: str = "config"):
        """Initialize Core Manager with configuration path."""
        self.config_path = Path(config_path)
        self.logger = self._setup_logging()
        self.config = self._load_configuration()
        self.components = {}
        self.status = "initialized"

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the core manager."""
        logger = logging.getLogger("CoreManager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_configuration(self) -> Dict:
        """Load system configuration from config files."""
        config = {}

        try:
            # Load runtime modes
            modes_file = self.config_path / "modes_runtime.json"
            if modes_file.exists():
                with open(modes_file, "r") as f:
                    config["modes"] = json.load(f)
                    self.logger.info("Runtime modes configuration loaded")

            # Load agent coordinates
            coords_file = self.config_path / "cursor_agent_coords.json"
            if coords_file.exists():
                with open(coords_file, "r") as f:
                    config["coordinates"] = json.load(f)
                    self.logger.info("Agent coordinates configuration loaded")

        except Exception as e:
            self.logger.error(f"Configuration loading failed: {e}")
            config = {}

        return config

    def initialize_system(self) -> bool:
        """Initialize the core system."""
        try:
            self.logger.info("Initializing core system...")

            # Verify configuration
            if not self.config:
                self.logger.error("No configuration loaded")
                return False

            # Set status
            self.status = "running"
            self.logger.info("Core system initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"System initialization failed: {e}")
            self.status = "error"
            return False

    def get_system_status(self) -> Dict:
        """Get current system status."""
        return {
            "status": self.status,
            "config_loaded": bool(self.config),
            "components": len(self.components),
            "config_keys": list(self.config.keys()) if self.config else [],
        }

    def register_component(self, name: str, component: object) -> bool:
        """Register a component with the core manager."""
        try:
            self.components[name] = component
            self.logger.info(f"Component '{name}' registered successfully")
            return True
        except Exception as e:
            self.logger.error(f"Component registration failed: {e}")
            return False

    def get_component(self, name: str) -> Optional[object]:
        """Get a registered component by name."""
        return self.components.get(name)

    def shutdown_system(self) -> bool:
        """Shutdown the core system."""
        try:
            self.logger.info("Shutting down core system...")
            self.status = "shutdown"
            self.components.clear()
            self.logger.info("Core system shutdown complete")
            return True
        except Exception as e:
            self.logger.error(f"System shutdown failed: {e}")
            return False


def main():
    """CLI interface for Core Manager testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Core Manager Testing Interface")
    parser.add_argument("--init", action="store_true", help="Initialize core system")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--test", action="store_true", help="Run core manager tests")
    parser.add_argument("--shutdown", action="store_true", help="Shutdown core system")

    args = parser.parse_args()

    # Create core manager instance
    manager = CoreManager()

    if args.init or not any([args.init, args.status, args.test, args.shutdown]):
        print("🚀 Core Manager - Agent Cellphone V2")
        success = manager.initialize_system()
        print(f"System initialization: {'✅ Success' if success else '❌ Failed'}")

    if args.status:
        status = manager.get_system_status()
        print("📊 System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")

    if args.test:
        print("🧪 Running core manager tests...")
        try:
            # Test component registration
            test_component = {"name": "test", "type": "test"}
            success = manager.register_component("test", test_component)
            print(f"Component registration: {'✅ Success' if success else '❌ Failed'}")

            # Test component retrieval
            component = manager.get_component("test")
            print(f"Component retrieval: {'✅ Success' if component else '❌ Failed'}")

        except Exception as e:
            print(f"❌ Core manager test failed: {e}")

    if args.shutdown:
        success = manager.shutdown_system()
        print(f"System shutdown: {'✅ Success' if success else '❌ Failed'}")


if __name__ == "__main__":
    main()
