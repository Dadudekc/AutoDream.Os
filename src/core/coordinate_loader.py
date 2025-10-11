"""
Unified Coordinate Loader for Team Beta Mission
Agent-7 Repository Cloning Specialist - Phase 3 High Priority Consolidation

V2 Compliance: ≤400 lines, type hints, KISS principle
SSOT Implementation: Consolidates cursor_agent_coords.json and config/coordinates.json
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
<<<<<<< HEAD
import os
<<<<<<< HEAD
from typing import Dict, Any
=======
from pathlib import Path


def _load_coordinates() -> Dict[str, Dict[str, Any]]:
    """Load agent coordinates from the cursor_agent_coords.json SSOT."""
    coord_file = Path("cursor_agent_coords.json")
    data = json.loads(coord_file.read_text(encoding="utf-8"))
    agents: Dict[str, Dict[str, Any]] = {}
    for agent_id, info in data.get("agents", {}).items():
        chat = info.get("chat_input_coordinates", [0, 0])
        onboarding = info.get("onboarding_input_coords", chat)  # Fallback to chat if not present
        agents[agent_id] = {
            "coords": tuple(chat),  # Store as tuple for coordinate loader
            "onboarding_coords": tuple(onboarding),  # Onboarding coordinates
            "x": chat[0],
            "y": chat[1],
            "description": info.get("description", ""),
        }
    return agents


COORDINATES: Dict[str, Dict[str, Any]] = _load_coordinates()

>>>>>>> origin/agent-3-v2-infrastructure-optimization

class CoordinateLoader:
    """Loads and manages agent coordinates for messaging system"""
    
    def __init__(self, config_path: str = "config/canonical_coordinates.json"):
        self.config_path = config_path
        self.canonical_path = "config/canonical_coordinates.json"
        self.coordinates = {}
    
    def load(self):
        """Load coordinates from configuration file"""
        self.coordinates = self._load_coordinates()
    
    def _load_coordinates(self) -> Dict[str, Any]:
        """Load coordinates preferring canonical SSOT; fallback to provided or defaults."""
        try:
            # Prefer canonical SSOT
            if os.path.exists(self.canonical_path):
                with open(self.canonical_path, 'r', encoding='utf-8') as f:
                    canonical = json.load(f)
            else:
                canonical = None

            # Load provided path if not canonical or for compatibility
            provided = None
            if self.config_path and os.path.exists(self.config_path) and self.config_path != self.canonical_path:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    provided = json.load(f)

            # Choose canonical if available; otherwise provided; otherwise defaults
            data = canonical if canonical is not None else (provided if provided is not None else self._get_default_coordinates())

            # If both exist, ensure no drift for agents present in canonical
            if canonical is not None and provided is not None:
                try:
                    for agent_key, coords in canonical.items():
                        if agent_key in provided and provided[agent_key] != coords:
                            print(f"Warning: coordinate drift detected for agent {agent_key}; using canonical value")
                            provided[agent_key] = coords
                    data = provided
                except Exception:
                    # If any issue, stick to canonical
                    data = canonical

            return {
                "agents": {
                    f"Agent-{k}": {"chat_input_coordinates": v} for k, v in data.items()
                }
            } if "agents" not in data else data
=======
from pathlib import Path
import time


class CoordinateSource(Enum):
    """Coordinate source enumeration."""
    PRIMARY = "primary"      # config/coordinates.json
    BACKUP = "backup"        # cursor_agent_coords.json
    ENVIRONMENT = "environment"


class AgentStatus(Enum):
    """Agent status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ONBOARDING = "onboarding"
    MAINTENANCE = "maintenance"


@dataclass
class AgentCoordinates:
    """Agent coordinates data structure."""
    x: int
    y: int
    monitor: str
    description: str


@dataclass
class CoordinateConfig:
    """Coordinate configuration data structure."""
    version: str
    last_updated: str
    agents: Dict[str, Dict[str, Any]]
    metadata: Dict[str, Any]


class UnifiedCoordinateLoader:
    """
    Unified Coordinate Loader - SSOT Implementation for Team Beta Mission.

    Consolidates multiple coordinate loading systems into a single,
    reliable, and maintainable solution with V2 compliance.
    """

    def __init__(self, primary_config_path: str = "config/coordinates.json",
                 backup_config_path: str = "cursor_agent_coords.json"):
        """Initialize unified coordinate loader."""
        self.primary_config_path = Path(primary_config_path)
        self.backup_config_path = Path(backup_config_path)
        self.current_config: Optional[CoordinateConfig] = None
        self.load_priority = [
            CoordinateSource.PRIMARY,
            CoordinateSource.BACKUP,
            CoordinateSource.ENVIRONMENT
        ]

    def load_coordinates(self) -> bool:
        """Load coordinates from available sources using priority order."""
        for source in self.load_priority:
            try:
                if source == CoordinateSource.PRIMARY:
                    if self._load_primary_config():
                        return True
                elif source == CoordinateSource.BACKUP:
                    if self._load_backup_config():
                        return True
                elif source == CoordinateSource.ENVIRONMENT:
                    if self._load_environment_config():
                        return True
            except Exception as e:
                print(f"Error loading from {source.value}: {e}")
                continue

        # If no config loaded, create default configuration
        self._create_default_config()
        return True

    def _load_primary_config(self) -> bool:
        """Load primary configuration from config/coordinates.json."""
        try:
            if not self.primary_config_path.exists():
                return False

            with open(self.primary_config_path, 'r') as f:
                data = json.load(f)

            self.current_config = CoordinateConfig(
                version=data.get("version", "1.0"),
                last_updated=data.get("last_updated", ""),
                agents=data.get("agents", {}),
                metadata=data.get("metadata", {})
            )
            return True
>>>>>>> origin/develop
        except Exception as e:
            print(f"Error loading primary config: {e}")
            return False

    def _load_backup_config(self) -> bool:
        """Load backup configuration from cursor_agent_coords.json."""
        try:
            if not self.backup_config_path.exists():
                return False

            with open(self.backup_config_path, 'r') as f:
                data = json.load(f)

            # Convert backup format to standard format
            agents = {}
            for agent_name, agent_data in data.get("agents", {}).items():
                agents[agent_name] = {
                    "active": agent_data.get("active", True),
                    "chat_input_coordinates": agent_data.get("chat_input_coordinates", [0, 0]),
                    "onboarding_coordinates": agent_data.get("onboarding_coordinates", [0, 0]),
                    "description": agent_data.get("description", "")
                }

            self.current_config = CoordinateConfig(
                version=data.get("version", "1.0"),
                last_updated=data.get("last_updated", ""),
                agents=agents,
                metadata={"source": "backup", "conversion": "automatic"}
            )
            return True
        except Exception as e:
            print(f"Error loading backup config: {e}")
            return False

    def _load_environment_config(self) -> bool:
        """Load configuration from environment variables."""
        try:
            # Try to load from environment if available
            env_coords = os.getenv("AGENT_COORDINATES")
            if not env_coords:
                return False

            data = json.loads(env_coords)
            self.current_config = CoordinateConfig(
                version=data.get("version", "1.0"),
                last_updated=data.get("last_updated", ""),
                agents=data.get("agents", {}),
                metadata={"source": "environment"}
            )
            return True
        except Exception as e:
            print(f"Error loading environment config: {e}")
            return False

    def _create_default_config(self):
        """Create default configuration when no sources available."""
        default_agents = {
            "Agent-1": {
                "active": True,
                "chat_input_coordinates": [-1269, 481],
                "onboarding_coordinates": [-1265, 171],
                "description": "Infrastructure Specialist"
            },
            "Agent-2": {
                "active": True,
                "chat_input_coordinates": [-308, 480],
                "onboarding_coordinates": [-304, 170],
                "description": "Data Processing Expert"
            },
            "Agent-3": {
                "active": True,
                "chat_input_coordinates": [-1269, 1001],
                "onboarding_coordinates": [-1265, 691],
                "description": "Quality Assurance Lead"
            },
            "Agent-4": {
                "active": True,
                "chat_input_coordinates": [-308, 1000],
                "onboarding_coordinates": [-304, 690],
                "description": "Project Coordinator"
            },
            "Agent-5": {
                "active": True,
                "chat_input_coordinates": [652, 421],
                "onboarding_coordinates": [656, 111],
                "description": "Business Intelligence"
            },
            "Agent-6": {
                "active": True,
                "chat_input_coordinates": [1612, 419],
                "onboarding_coordinates": [1616, 109],
                "description": "Code Quality Specialist"
            },
            "Agent-7": {
                "active": True,
                "chat_input_coordinates": [920, 851],
                "onboarding_coordinates": [924, 541],
                "description": "Web Development Expert"
            },
            "Agent-8": {
                "active": True,
                "chat_input_coordinates": [1611, 941],
                "onboarding_coordinates": [1615, 631],
                "description": "Integration Specialist"
            }
        }

        self.current_config = CoordinateConfig(
            version="2.0",
            last_updated=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            agents=default_agents,
            metadata={
                "source": "default",
                "created_by": "Agent-7",
                "team_beta_mission": True,
                "ssot_compliant": True
            }
        )

    def get_agent_coordinates(self, agent_name: str) -> Optional[AgentCoordinates]:
        """Get coordinates for a specific agent."""
        if not self.current_config:
            return None

        if agent_name not in self.current_config.agents:
            return None

        agent_data = self.current_config.agents[agent_name]
        coords = agent_data.get("chat_input_coordinates", [0, 0])

        return AgentCoordinates(
            x=coords[0],
            y=coords[1],
            monitor="primary",
            description=agent_data.get("description", "")
        )

    def get_all_agents(self) -> Dict[str, AgentCoordinates]:
        """Get coordinates for all agents."""
        if not self.current_config:
            return {}

        agents = {}
        for agent_name, agent_data in self.current_config.agents.items():
            coords = agent_data.get("chat_input_coordinates", [0, 0])
            agents[agent_name] = AgentCoordinates(
                x=coords[0],
                y=coords[1],
                monitor="primary",
                description=agent_data.get("description", "")
            )

        return agents

    def get_active_agents(self) -> Dict[str, AgentCoordinates]:
        """Get coordinates for active agents only."""
        if not self.current_config:
            return {}

        agents = {}
        for agent_name, agent_data in self.current_config.agents.items():
            if agent_data.get("active", True):
                coords = agent_data.get("chat_input_coordinates", [0, 0])
                agents[agent_name] = AgentCoordinates(
                    x=coords[0],
                    y=coords[1],
                    monitor="primary",
                    description=agent_data.get("description", "")
                )

        return agents

    def update_agent_coordinates(self, agent_name: str, x: int, y: int,
                               description: str = "") -> bool:
        """Update coordinates for a specific agent."""
        if not self.current_config:
            return False

        if agent_name not in self.current_config.agents:
            return False

        self.current_config.agents[agent_name].update({
            "chat_input_coordinates": [x, y],
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        })

        if description:
            self.current_config.agents[agent_name]["description"] = description

        self.current_config.last_updated = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return self._save_config()

    def _save_config(self) -> bool:
        """Save current configuration to primary config file."""
        try:
            if not self.primary_config_path.parent.exists():
                self.primary_config_path.parent.mkdir(parents=True, exist_ok=True)

            config_data = {
                "version": self.current_config.version,
                "last_updated": self.current_config.last_updated,
                "agents": self.current_config.agents,
                "metadata": self.current_config.metadata
            }

            with open(self.primary_config_path, 'w') as f:
                json.dump(config_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def validate_coordinates(self) -> List[str]:
        """Validate coordinate configuration and return issues."""
        issues = []

        if not self.current_config:
            issues.append("No coordinate configuration loaded")
            return issues

        # Check for duplicate coordinates
        coordinates = {}
        for agent_name, agent_data in self.current_config.agents.items():
            coords = tuple(agent_data.get("chat_input_coordinates", [0, 0]))
            if coords in coordinates:
                issues.append(f"Duplicate coordinates {coords} for {agent_name} and {coordinates[coords]}")
            coordinates[coords] = agent_name

        # Check for inactive agents
        inactive_agents = [name for name, data in self.current_config.agents.items()
                          if not data.get("active", True)]
        if inactive_agents:
            issues.append(f"Inactive agents found: {', '.join(inactive_agents)}")

        # Check for missing descriptions
        missing_descriptions = [name for name, data in self.current_config.agents.items()
                               if not data.get("description", "").strip()]
        if missing_descriptions:
            issues.append(f"Missing descriptions for: {', '.join(missing_descriptions)}")

        return issues

    def export_coordinate_report(self, filepath: str) -> bool:
        """Export coordinate configuration report."""
        try:
            report = {
                "coordinate_report": {
                    "report_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "configuration_source": self.current_config.metadata.get("source", "unknown") if self.current_config else "none",
                    "total_agents": len(self.current_config.agents) if self.current_config else 0,
                    "active_agents": len(self.get_active_agents()),
                    "validation_issues": self.validate_coordinates(),
                    "agents": [
                        {
                            "name": name,
                            "coordinates": {"x": coords.x, "y": coords.y},
                            "description": coords.description,
                            "active": name in self.get_active_agents()
                        }
                        for name, coords in self.get_all_agents().items()
                    ]
                }
            }

            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting coordinate report: {e}")
            return False


def create_unified_coordinate_loader() -> UnifiedCoordinateLoader:
    """Create unified coordinate loader instance."""
    return UnifiedCoordinateLoader()


if __name__ == "__main__":
    # Example usage
    loader = create_unified_coordinate_loader()

    # Load coordinates
    if loader.load_coordinates():
        print("✅ Unified coordinate loader operational")

        # Get all agents
        agents = loader.get_all_agents()
        print(f"📍 Loaded coordinates for {len(agents)} agents")

        # Validate configuration
        issues = loader.validate_coordinates()
        if issues:
            print(f"⚠️ Validation issues: {len(issues)}")
            for issue in issues:
                print(f"  - {issue}")
        else:
<<<<<<< HEAD
            raise ValueError(f"Agent {agent_id} not found in coordinates")
    
    def get_all_coordinates(self) -> Dict[str, tuple]:
        """Get all agent coordinates"""
        return {
            agent_id: (coords.get("chat_input_coordinates", [0, 0])[0], coords.get("chat_input_coordinates", [0, 0])[1])
            for agent_id, coords in self.coordinates.get("agents", {}).items()
        }
    
    def get_agent_ids(self) -> list:
        """Get list of all agent IDs"""
        return list(self.coordinates.get("agents", {}).keys())
    
    def get_coords(self, agent_id: str):
        """Get coordinates object for agent (compatible with messaging service)"""
        if agent_id in self.coordinates.get("agents", {}):
            agent_coords = self.coordinates["agents"][agent_id]
            coords = agent_coords.get("chat_input_coordinates", [0, 0])
            return type('Coords', (), {'tuple': (coords[0], coords[1])})()
        else:
            raise ValueError(f"Agent {agent_id} not found in coordinates")
    
    def validate_all(self):
        """Validate all coordinates (compatible with messaging service)"""
        issues = []
        try:
            # Basic shape and bounds validation
            for agent_id, data in self.coordinates.get("agents", {}).items():
                coords = data.get("chat_input_coordinates")
                if not isinstance(coords, list) or len(coords) < 2:
                    issues.append(f"Invalid format for {agent_id}")
                    continue
                x, y = coords[0], coords[1]
                if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                    issues.append(f"Non-numeric coordinates for {agent_id}")
                    continue
        except Exception as e:
            issues.append(f"Validation error: {e}")

<<<<<<< HEAD
        return type('ValidationReport', (), {
            'is_all_ok': lambda self: len(issues) == 0,
            'issues': issues
        })()
=======
    def get_onboarding_coordinates(self, agent_id: str) -> Tuple[int, int]:
        """Get onboarding coordinates for agent."""
        if agent_id in self.coordinates:
            return self.coordinates[agent_id]["onboarding_coords"]
        raise ValueError(f"No onboarding coordinates found for agent {agent_id}")
>>>>>>> origin/agent-3-v2-infrastructure-optimization

    def assert_canonical_consistency(self) -> None:
        """Raise if loaded coordinates drift from canonical SSOT where applicable."""
        try:
            if os.path.exists(self.canonical_path):
                with open(self.canonical_path, 'r', encoding='utf-8') as f:
                    canonical = json.load(f)
                for k, v in canonical.items():
                    agent_id = f"Agent-{k}"
                    cur = self.coordinates.get("agents", {}).get(agent_id, {})
                    if cur.get("chat_input_coordinates") != v:
                        raise AssertionError(f"Coordinate drift for {agent_id}: {cur.get('chat_input_coordinates')} != {v}")
        except AssertionError:
            raise
        except Exception:
            # Do not raise for missing canon or parsing issues, loader already warns
            pass
=======
            print("✅ No validation issues found")

        # Export report
        loader.export_coordinate_report("unified_coordinate_report.json")
        print("📊 Coordinate report exported to unified_coordinate_report.json")
    else:
        print("❌ Failed to load coordinates")

>>>>>>> origin/develop
