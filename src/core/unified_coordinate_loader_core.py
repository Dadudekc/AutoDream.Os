"""
Unified Coordinate Loader Core - V2 Compliant
Agent-7 Repository Cloning Specialist - Phase 3 High Priority Consolidation

V2 Compliance: ≤400 lines, type hints, KISS principle
"""

import json
import os
from pathlib import Path

from .unified_coordinate_loader_models import (
    AgentCoordinates,
    CoordinateConfig,
    CoordinateSource,
    LoadResult,
    ValidationResult,
)


class CoordinateLoader:
    """Core coordinate loading functionality."""

    def __init__(self):
        self.primary_path = Path("config/coordinates.json")
        self.backup_path = Path("cursor_agent_coords.json")

    def load_coordinates(self) -> LoadResult:
        """Load coordinates from available sources."""
        # Try primary source first
        if self.primary_path.exists():
            return self._load_from_file(self.primary_path, CoordinateSource.PRIMARY)

        # Try backup source
        if self.backup_path.exists():
            return self._load_from_file(self.backup_path, CoordinateSource.BACKUP)

        # Try environment variables
        env_coords = self._load_from_environment()
        if env_coords:
            return LoadResult(
                success=True,
                config=env_coords,
                error=None,
                source=CoordinateSource.ENVIRONMENT,
            )

        return LoadResult(
            success=False,
            config=None,
            error="No coordinate sources available",
            source=None,
        )

    def _load_from_file(self, path: Path, source: CoordinateSource) -> LoadResult:
        """Load coordinates from a file."""
        try:
            with open(path) as f:
                data = json.load(f)

            config = self._parse_coordinate_data(data, source)
            return LoadResult(
                success=True,
                config=config,
                error=None,
                source=source,
            )
        except Exception as e:
            return LoadResult(
                success=False,
                config=None,
                error=f"Failed to load {path}: {str(e)}",
                source=source,
            )

    def _load_from_environment(self) -> CoordinateConfig | None:
        """Load coordinates from environment variables."""
        # Check for environment-based coordinates
        env_agents = {}
        for i in range(1, 9):  # Agents 1-8
            agent_key = f"AGENT_{i}_COORDS"
            if agent_key in os.environ:
                try:
                    coords_data = json.loads(os.environ[agent_key])
                    env_agents[f"Agent-{i}"] = AgentCoordinates(
                        x=coords_data["x"],
                        y=coords_data["y"],
                        monitor=coords_data.get("monitor", "unknown"),
                        description=coords_data.get("description", ""),
                    )
                except (json.JSONDecodeError, KeyError):
                    continue

        if env_agents:
            return CoordinateConfig(
                version="1.0",
                last_updated="environment",
                source=CoordinateSource.ENVIRONMENT,
                agents=env_agents,
            )

        return None

    def _parse_coordinate_data(self, data: dict, source: CoordinateSource) -> CoordinateConfig:
        """Parse coordinate data from loaded JSON."""
        agents = {}
        for agent_id, agent_data in data.get("agents", {}).items():
            agents[agent_id] = AgentCoordinates(
                x=agent_data["x"],
                y=agent_data["y"],
                monitor=agent_data.get("monitor", "unknown"),
                description=agent_data.get("description", ""),
            )

        return CoordinateConfig(
            version=data.get("version", "1.0"),
            last_updated=data.get("last_updated", "unknown"),
            source=source,
            agents=agents,
        )

    def validate_coordinates(self, config: CoordinateConfig) -> ValidationResult:
        """Validate coordinate configuration."""
        errors = []
        warnings = []

        for agent_id, coords in config.agents.items():
            self._validate_agent_coords(agent_id, coords, errors, warnings)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def _validate_agent_coords(
        self, agent_id: str, coords: AgentCoordinates, errors: list, warnings: list
    ):
        """Validate individual agent coordinates."""
        # Check coordinate bounds
        if coords.x < -2000 or coords.x > 2000:
            errors.append(f"{agent_id}: X coordinate {coords.x} out of bounds")
        if coords.y < -2000 or coords.y > 2000:
            errors.append(f"{agent_id}: Y coordinate {coords.y} out of bounds")

        # Check monitor assignment
        if coords.monitor not in ["Monitor 1", "Monitor 2", "unknown"]:
            warnings.append(f"{agent_id}: Unknown monitor '{coords.monitor}'")

    def save_coordinates(self, config: CoordinateConfig, path: Path | None = None) -> bool:
        """Save coordinates to file."""
        if path is None:
            path = self.primary_path

        try:
            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "version": config.version,
                "last_updated": config.last_updated,
                "source": config.source.value,
                "agents": {
                    agent_id: {
                        "x": coords.x,
                        "y": coords.y,
                        "monitor": coords.monitor,
                        "description": coords.description,
                    }
                    for agent_id, coords in config.agents.items()
                },
            }

            with open(path, "w") as f:
                json.dump(data, f, indent=2)

            return True
        except Exception:
            return False
