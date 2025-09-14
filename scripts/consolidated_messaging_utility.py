#!/usr/bin/env python3
"""
Consolidated Messaging Utility
==============================

Unified messaging system for agent coordination, validation, and documentation.
Consolidates functionality from multiple messaging-related scripts.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class MessagingSystem:
    """Represents a messaging system configuration."""

    name: str
    type: str
    status: str
    config_path: str
    dependencies: List[str]


class MessagingUtility:
    """Unified messaging utility for agent coordination."""

    def __init__(self):
        """Initialize the messaging utility."""
        self.systems = []
        self.registry_path = Path("src/services/messaging/registry.json")

    def list_systems(self) -> List[MessagingSystem]:
        """List all available messaging systems."""
        systems = []

        # Check for consolidated messaging service
        if Path("src/services/consolidated_messaging_service.py").exists():
            systems.append(MessagingSystem(
                name="Consolidated Messaging Service",
                type="primary",
                status="active",
                config_path="src/services/consolidated_messaging_service.py",
                dependencies=["src/services/messaging/"]
            ))

        # Check for messaging CLI
        if Path("src/services/messaging/cli/messaging_cli.py").exists():
            systems.append(MessagingSystem(
                name="Messaging CLI",
                type="cli",
                status="active",
                config_path="src/services/messaging/cli/messaging_cli.py",
                dependencies=["src/services/messaging/"]
            ))

        # Check for PyAutoGUI messaging
        if Path("src/core/swarm_communication_coordinator.py").exists():
            systems.append(MessagingSystem(
                name="PyAutoGUI Swarm Communication",
                type="automation",
                status="active",
                config_path="src/core/swarm_communication_coordinator.py",
                dependencies=["pyautogui"]
            ))

        return systems

    def validate_registry(self) -> Dict[str, Any]:
        """Validate messaging system registry."""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "systems_found": 0
        }

        try:
            if self.registry_path.exists():
                with open(self.registry_path, 'r') as f:
                    registry = json.load(f)

                results["systems_found"] = len(registry.get("systems", []))

                # Validate each system
                for system in registry.get("systems", []):
                    if not system.get("name"):
                        results["errors"].append(f"System missing name: {system}")
                    if not system.get("type"):
                        results["warnings"].append(f"System missing type: {system.get('name', 'unknown')}")

                if results["errors"]:
                    results["valid"] = False
            else:
                results["warnings"].append("Registry file not found")

        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Failed to validate registry: {str(e)}")

        return results

    def generate_docs(self, output_dir: str = "docs/messaging/") -> bool:
        """Generate documentation for messaging systems."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            systems = self.list_systems()

            # Generate system overview
            overview_content = f"""# Messaging Systems Overview

## Available Systems

Total Systems: {len(systems)}

"""

            for system in systems:
                overview_content += f"""### {system.name}
- **Type**: {system.type}
- **Status**: {system.status}
- **Config**: {system.config_path}
- **Dependencies**: {', '.join(system.dependencies)}

"""

            with open(output_path / "messaging_systems.md", 'w') as f:
                f.write(overview_content)

            logger.info(f"Generated documentation in {output_dir}")
            return True

        except Exception as e:
            logger.error(f"Failed to generate docs: {str(e)}")
            return False

    def generate_stubs(self, output_dir: str = "stubs/messaging/") -> bool:
        """Generate Python stubs for messaging systems."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Generate consolidated messaging stub
            stub_content = '''"""Consolidated Messaging Service Stubs."""

from typing import Any, Dict, List, Optional

class ConsolidatedMessagingService:
    """Consolidated messaging service for agent coordination."""

    def send_message(self, agent_id: str, content: str, priority: str = "NORMAL") -> bool:
        """Send a message to an agent."""
        ...

    def broadcast_message(self, content: str, priority: str = "NORMAL") -> bool:
        """Broadcast a message to all agents."""
        ...

    def check_inbox(self, agent_id: str) -> List[Dict[str, Any]]:
        """Check inbox for an agent."""
        ...

class MessagingCLI:
    """Messaging CLI interface."""

    def run_command(self, command: str, args: List[str]) -> int:
        """Run a messaging CLI command."""
        ...
'''

            with open(output_path / "consolidated_messaging.pyi", 'w') as f:
                f.write(stub_content)

            logger.info(f"Generated stubs in {output_dir}")
            return True

        except Exception as e:
            logger.error(f"Failed to generate stubs: {str(e)}")
            return False

    def run_doctor(self) -> Dict[str, Any]:
        """Run messaging system diagnostics."""
        results = {
            "healthy": True,
            "issues": [],
            "recommendations": []
        }

        # Check systems
        systems = self.list_systems()
        if not systems:
            results["healthy"] = False
            results["issues"].append("No messaging systems found")
            results["recommendations"].append("Install consolidated messaging service")

        # Validate registry
        registry_validation = self.validate_registry()
        if not registry_validation["valid"]:
            results["healthy"] = False
            results["issues"].extend(registry_validation["errors"])

        # Check dependencies
        try:
            import pyautogui
        except ImportError:
            results["issues"].append("PyAutoGUI not installed - swarm automation unavailable")
            results["recommendations"].append("Install pyautogui for swarm coordination")

        return results


def main():
    """Main entry point for the messaging utility."""
    parser = argparse.ArgumentParser(description="Consolidated Messaging Utility")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List systems command
    list_parser = subparsers.add_parser("list", help="List messaging systems")

    # Validate registry command
    validate_parser = subparsers.add_parser("validate", help="Validate messaging registry")

    # Generate docs command
    docs_parser = subparsers.add_parser("docs", help="Generate documentation")
    docs_parser.add_argument("--output-dir", default="docs/messaging/", help="Output directory")

    # Generate stubs command
    stubs_parser = subparsers.add_parser("stubs", help="Generate Python stubs")
    stubs_parser.add_argument("--output-dir", default="stubs/messaging/", help="Output directory")

    # Doctor command
    doctor_parser = subparsers.add_parser("doctor", help="Run messaging diagnostics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    utility = MessagingUtility()

    try:
        if args.command == "list":
            systems = utility.list_systems()
            print(f"Found {len(systems)} messaging systems:")
            for system in systems:
                print(f"  - {system.name} ({system.type}) - {system.status}")

        elif args.command == "validate":
            results = utility.validate_registry()
            if results["valid"]:
                print("✅ Registry validation passed")
            else:
                print("❌ Registry validation failed:")
                for error in results["errors"]:
                    print(f"  - {error}")

        elif args.command == "docs":
            if utility.generate_docs(args.output_dir):
                print(f"✅ Documentation generated in {args.output_dir}")
            else:
                print("❌ Failed to generate documentation")
                return 1

        elif args.command == "stubs":
            if utility.generate_stubs(args.output_dir):
                print(f"✅ Stubs generated in {args.output_dir}")
            else:
                print("❌ Failed to generate stubs")
                return 1

        elif args.command == "doctor":
            results = utility.run_doctor()
            if results["healthy"]:
                print("✅ Messaging systems are healthy")
            else:
                print("❌ Messaging system issues found:")
                for issue in results["issues"]:
                    print(f"  - {issue}")
                print("\nRecommendations:")
                for rec in results["recommendations"]:
                    print(f"  - {rec}")

        return 0

    except Exception as e:
        logger.error(f"Command failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
