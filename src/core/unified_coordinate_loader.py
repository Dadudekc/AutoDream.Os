"""
Unified Coordinate Loader - V2 Compliant Main Interface
Agent-7 Repository Cloning Specialist - Phase 3 High Priority Consolidation

V2 Compliance: ≤400 lines, type hints, KISS principle
SSOT Implementation: Consolidates cursor_agent_coords.json and config/coordinates.json
"""

import time
from dataclasses import dataclass
from pathlib import Path

from .unified_coordinate_loader_core import CoordinateLoader
from .unified_coordinate_loader_models import (
    AgentCoordinates,
    CoordinateConfig,
    LoadResult,
    ValidationResult,
)


def load_agent_coordinates() -> LoadResult:
    """Load agent coordinates from available sources."""
    loader = CoordinateLoader()
    return loader.load_coordinates()


def get_agent_coordinates(agent_id: str) -> AgentCoordinates | None:
    """Get coordinates for a specific agent."""
    result = load_agent_coordinates()
    if result.success and result.config:
        return result.config.agents.get(agent_id)
    return None


def get_all_agent_coordinates() -> dict[str, AgentCoordinates]:
    """Get coordinates for all agents."""
    result = load_agent_coordinates()
    if result.success and result.config:
        return result.config.agents
    return {}


def get_active_agents() -> list[str]:
    """Get list of active agents based on coordinate availability."""
    coords = get_all_agent_coordinates()
    return list(coords.keys())


def validate_coordinate_config(config: CoordinateConfig) -> ValidationResult:
    """Validate coordinate configuration."""
    loader = CoordinateLoader()
    return loader.validate_coordinates(config)


def save_coordinate_config(config: CoordinateConfig, path: Path | None = None) -> bool:
    """Save coordinate configuration to file."""
    loader = CoordinateLoader()
    return loader.save_coordinates(config, path)


@dataclass
class CoordinateUpdate:
    """Coordinate update data."""

    agent_id: str
    action: str
    x: int = 0
    y: int = 0
    monitor: str = ""
    description: str = ""


def manage_agent_coordinates(update: CoordinateUpdate) -> bool:
    """Manage agent coordinates (update or remove)."""
    result = load_agent_coordinates()
    if not result.success or not result.config:
        return False

    if update.action == "update":
        result.config.agents[update.agent_id] = AgentCoordinates(
            x=update.x, y=update.y, monitor=update.monitor, description=update.description
        )
    elif update.action == "remove" and update.agent_id in result.config.agents:
        del result.config.agents[update.agent_id]
    else:
        return False

    result.config.last_updated = time.strftime("%Y-%m-%d %H:%M:%S")
    return save_coordinate_config(result.config)


def get_coordinate_summary() -> dict:
    """Get summary of coordinate configuration."""
    result = load_agent_coordinates()
    if not result.success or not result.config:
        return {
            "status": "error",
            "message": result.error,
            "agents": 0,
            "source": None,
        }

    validation = validate_coordinate_config(result.config)
    return {
        "status": "success" if validation.valid else "warning",
        "agents": len(result.config.agents),
        "source": result.config.source.value,
        "last_updated": result.config.last_updated,
        "validation_errors": validation.errors,
        "validation_warnings": validation.warnings,
    }


def main():
    """CLI entry point for coordinate loader."""
    import argparse

    parser = argparse.ArgumentParser(description="Unified Coordinate Loader")
    parser.add_argument("--agent", help="Get coordinates for specific agent")
    parser.add_argument("--list", action="store_true", help="List all agent coordinates")
    parser.add_argument("--validate", action="store_true", help="Validate coordinate configuration")
    parser.add_argument("--summary", action="store_true", help="Show coordinate summary")

    args = parser.parse_args()

    if any([args.agent, args.list, args.validate, args.summary]):
        _handle_cli_commands(args)
    else:
        parser.print_help()


def _handle_cli_commands(args):
    """Handle all CLI commands."""
    if args.agent:
        _handle_agent_command(args.agent)
    elif args.list:
        _handle_list_command()
    elif args.validate:
        _handle_validate_command()
    elif args.summary:
        _handle_summary_command()


def _handle_agent_command(agent_id: str):
    """Handle agent command."""
    coords = get_agent_coordinates(agent_id)
    if coords:
        print(f"{agent_id}: ({coords.x}, {coords.y}) on {coords.monitor}")
    else:
        print(f"No coordinates found for {agent_id}")


def _handle_list_command():
    """Handle list command."""
    all_coords = get_all_agent_coordinates()
    for agent_id, coords in all_coords.items():
        print(f"{agent_id}: ({coords.x}, {coords.y}) on {coords.monitor}")


def _handle_validate_command():
    """Handle validate command."""
    result = load_agent_coordinates()
    if result.success and result.config:
        validation = validate_coordinate_config(result.config)
        if validation.valid:
            print("✅ Coordinate configuration is valid")
        else:
            print("❌ Coordinate configuration has errors:")
            for error in validation.errors:
                print(f"  - {error}")
            for warning in validation.warnings:
                print(f"  ⚠️  {warning}")


def _handle_summary_command():
    """Handle summary command."""
    summary = get_coordinate_summary()
    print(f"Status: {summary['status']}")
    print(f"Agents: {summary['agents']}")
    print(f"Source: {summary['source']}")
    if summary.get("last_updated"):
        print(f"Last Updated: {summary['last_updated']}")


if __name__ == "__main__":
    main()
