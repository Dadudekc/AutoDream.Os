"""
Project Registry - Single Source of Truth for AutoDream.OS
Manages shared project state, component ownership, and design patterns.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Component:
    """Represents a project component with ownership and purpose."""

    path: str
    purpose: str
    owner: str
    created_at: str
    last_modified: str
    status: str = "active"  # active, deprecated, refactoring
    dependencies: list[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class DesignPattern:
    """Represents an approved design pattern or principle."""

    name: str
    description: str
    examples: list[str]
    anti_patterns: list[str]
    enforcement_level: str = "required"  # required, recommended, optional


@dataclass
class ProjectRegistry:
    """Single Source of Truth for project state and design decisions."""

    project_name: str
    version: str
    components: dict[str, Component]
    patterns: list[DesignPattern]
    last_updated: str
    active_agents: list[str]

    def __post_init__(self):
        if not hasattr(self, "active_agents") or self.active_agents is None:
            self.active_agents = []


class ProjectRegistryManager:
    """Manages the project registry with thread-safe operations."""

    def __init__(self, registry_path: str = "project_registry.json"):
        self.registry_path = Path(registry_path)
        self._registry: ProjectRegistry | None = None

    def load_registry(self) -> ProjectRegistry:
        """Load the registry from disk, creating default if not exists."""
        if self._registry is not None:
            return self._registry

        if not self.registry_path.exists():
            self._create_default_registry()

        with open(self.registry_path, encoding="utf-8") as f:
            data = json.load(f)

        # Convert components back to Component objects
        components = {}
        for name, comp_data in data.get("components", {}).items():
            components[name] = Component(**comp_data)

        # Convert patterns back to DesignPattern objects
        patterns = [DesignPattern(**pattern_data) for pattern_data in data.get("patterns", [])]

        self._registry = ProjectRegistry(
            project_name=data.get("project_name", "AutoDream.OS"),
            version=data.get("version", "2.1.0"),
            components=components,
            patterns=patterns,
            last_updated=data.get("last_updated", datetime.now().isoformat()),
            active_agents=data.get("active_agents", []),
        )

        return self._registry

    def save_registry(self) -> None:
        """Save the registry to disk."""
        if self._registry is None:
            return

        # Convert to serializable format
        data = {
            "project_name": self._registry.project_name,
            "version": self._registry.version,
            "components": {name: asdict(comp) for name, comp in self._registry.components.items()},
            "patterns": [asdict(pattern) for pattern in self._registry.patterns],
            "last_updated": datetime.now().isoformat(),
            "active_agents": self._registry.active_agents,
        }

        # Ensure directory exists
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _create_default_registry(self) -> None:
        """Create a default registry with AutoDream.OS patterns."""
        default_patterns = [
            DesignPattern(
                name="KISS Principle",
                description="Keep It Simple, Stupid - prefer simple solutions",
                examples=[
                    "Use simple functions instead of complex classes",
                    "Prefer if/else over complex match statements",
                    "Use built-in types instead of custom wrappers",
                ],
                anti_patterns=[
                    "Over-engineering simple problems",
                    "Creating abstractions before they're needed",
                    "Complex inheritance hierarchies",
                ],
                enforcement_level="required",
            ),
            DesignPattern(
                name="YAGNI",
                description="You Aren't Gonna Need It - don't build features until needed",
                examples=[
                    "Start with simple data structures",
                    "Add complexity only when requirements demand it",
                    "Prefer composition over inheritance",
                ],
                anti_patterns=[
                    "Building features for hypothetical future needs",
                    "Creating complex interfaces for simple use cases",
                    "Over-abstracting before understanding requirements",
                ],
                enforcement_level="required",
            ),
            DesignPattern(
                name="Single Responsibility",
                description="Each component should have one clear purpose",
                examples=[
                    "Separate data access from business logic",
                    "Keep UI components focused on presentation",
                    "Isolate external service integrations",
                ],
                anti_patterns=[
                    "God classes that do everything",
                    "Functions that handle multiple concerns",
                    "Modules mixing different abstraction levels",
                ],
                enforcement_level="required",
            ),
            DesignPattern(
                name="Error Handling",
                description="Use anyhow for consistent error handling",
                examples=[
                    "from anyhow import Result, Context",
                    "def process_data() -> Result[str]: ...",
                    "Use .context() for error context",
                ],
                anti_patterns=[
                    "Bare except clauses",
                    "Silent error swallowing",
                    "Inconsistent error types",
                ],
                enforcement_level="required",
            ),
        ]

        self._registry = ProjectRegistry(
            project_name="AutoDream.OS",
            version="2.1.0",
            components={},
            patterns=default_patterns,
            last_updated=datetime.now().isoformat(),
            active_agents=[],
        )
        self.save_registry()

    def register_component(
        self, name: str, path: str, purpose: str, owner: str, dependencies: list[str] = None
    ) -> Component:
        """Register a new component in the registry."""
        registry = self.load_registry()

        if dependencies is None:
            dependencies = []

        component = Component(
            path=path,
            purpose=purpose,
            owner=owner,
            created_at=datetime.now().isoformat(),
            last_modified=datetime.now().isoformat(),
            dependencies=dependencies,
        )

        registry.components[name] = component
        self.save_registry()

        return component

    def get_component(self, name: str) -> Component | None:
        """Get a component by name."""
        registry = self.load_registry()
        return registry.components.get(name)

    def check_component_exists(self, name: str) -> bool:
        """Check if a component already exists."""
        registry = self.load_registry()
        return name in registry.components

    def update_component(self, name: str, **updates) -> bool:
        """Update an existing component."""
        registry = self.load_registry()

        if name not in registry.components:
            return False

        component = registry.components[name]
        for key, value in updates.items():
            if hasattr(component, key):
                setattr(component, key, value)

        component.last_modified = datetime.now().isoformat()
        self.save_registry()

        return True

    def get_approved_patterns(self) -> list[DesignPattern]:
        """Get all approved design patterns."""
        registry = self.load_registry()
        return registry.patterns

    def validate_design_decision(self, decision: str, context: str = "") -> dict[str, Any]:
        """Validate a design decision against approved patterns."""
        registry = self.load_registry()
        violations = []
        recommendations = []

        for pattern in registry.patterns:
            # Simple keyword-based validation (can be enhanced with NLP)
            for anti_pattern in pattern.anti_patterns:
                if any(
                    keyword in decision.lower()
                    for keyword in ["complex", "advanced", "sophisticated", "enterprise"]
                ):
                    if pattern.enforcement_level == "required":
                        violations.append(
                            {
                                "pattern": pattern.name,
                                "violation": anti_pattern,
                                "severity": "error",
                            }
                        )
                    else:
                        recommendations.append(
                            {
                                "pattern": pattern.name,
                                "suggestion": f"Consider: {pattern.description}",
                                "severity": "warning",
                            }
                        )

        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "recommendations": recommendations,
        }

    def get_agent_components(self, agent_id: str) -> list[Component]:
        """Get all components owned by a specific agent."""
        registry = self.load_registry()
        return [comp for comp in registry.components.values() if comp.owner == agent_id]

    def transfer_component_ownership(self, component_name: str, new_owner: str) -> bool:
        """Transfer ownership of a component to another agent."""
        return self.update_component(component_name, owner=new_owner)

    def get_registry_summary(self) -> dict[str, Any]:
        """Get a summary of the current registry state."""
        registry = self.load_registry()

        return {
            "project_name": registry.project_name,
            "version": registry.version,
            "total_components": len(registry.components),
            "active_agents": registry.active_agents,
            "component_breakdown": {
                "by_owner": {
                    agent: len(self.get_agent_components(agent)) for agent in registry.active_agents
                },
                "by_status": {
                    status: len([c for c in registry.components.values() if c.status == status])
                    for status in ["active", "deprecated", "refactoring"]
                },
            },
            "last_updated": registry.last_updated,
        }


# Global registry manager instance
registry_manager = ProjectRegistryManager()


def get_registry() -> ProjectRegistry:
    """Get the current project registry."""
    return registry_manager.load_registry()


def register_component(
    name: str, path: str, purpose: str, owner: str, dependencies: list[str] = None
) -> Component:
    """Register a new component."""
    return registry_manager.register_component(name, path, purpose, owner, dependencies)


def check_component_exists(name: str) -> bool:
    """Check if a component exists before creating it."""
    return registry_manager.check_component_exists(name)


def validate_design_decision(decision: str, context: str = "") -> dict[str, Any]:
    """Validate a design decision against project patterns."""
    return registry_manager.validate_design_decision(decision, context)
