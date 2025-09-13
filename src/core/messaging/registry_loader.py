"""
Registry loader for messaging systems.

Provides the Single Source of Truth (SSOT) for all messaging systems
with dynamic import resolution and category filtering.
"""

from __future__ import annotations
import importlib
import dataclasses
import yaml
import pathlib
import typing as t
import logging

logger = logging.getLogger(__name__)

# Default registry path
REG_PATH = pathlib.Path("config/messaging_systems.yaml")


@dataclasses.dataclass(frozen=True)
class SystemSpec:
    """Specification for a messaging system."""
    id: str
    name: str
    category: str
    module: str
    entrypoint: str
    critical: bool = False

    def __str__(self) -> str:
        """String representation of the system spec."""
        criticality = "🔴" if self.critical else "🟡"
        return f"{criticality} [{self.category}] {self.id} :: {self.module}.{self.entrypoint}"


def load_registry(path: pathlib.Path = REG_PATH) -> list[SystemSpec]:
    """
    Load the messaging systems registry from YAML.

    Args:
        path: Path to the YAML registry file

    Returns:
        List of SystemSpec objects

    Raises:
        FileNotFoundError: If registry file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    if not path.exists():
        raise FileNotFoundError(f"Registry file not found: {path}")

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Failed to parse registry YAML: {e}")

    specs: list[SystemSpec] = []
    for system_data in data.get("systems", []):
        try:
            spec = SystemSpec(**system_data)
            specs.append(spec)
        except TypeError as e:
            logger.warning(f"Invalid system spec: {system_data}, error: {e}")
            continue

    logger.info(f"Loaded {len(specs)} messaging systems from {path}")
    return specs


def resolve(spec: SystemSpec) -> t.Any:
    """
    Resolve a system spec to its actual class/function.

    Args:
        spec: SystemSpec to resolve

    Returns:
        The resolved class or function

    Raises:
        ImportError: If module cannot be imported
        AttributeError: If entrypoint doesn't exist in module
    """
    try:
        module = importlib.import_module(spec.module)
        return getattr(module, spec.entrypoint)
    except ImportError as e:
        raise ImportError(f"Failed to import module {spec.module}: {e}")
    except AttributeError as e:
        raise AttributeError(f"Entrypoint {spec.entrypoint} not found in {spec.module}: {e}")


def iter_specs(category: str | None = None) -> t.Iterator[SystemSpec]:
    """
    Iterate over system specs, optionally filtered by category.

    Args:
        category: Optional category filter (core, cli, external, ai, supporting)

    Yields:
        SystemSpec objects matching the filter
    """
    for spec in load_registry():
        if category is None or spec.category == category:
            yield spec


def get_system_by_id(system_id: str) -> SystemSpec | None:
    """
    Get a system spec by its ID.

    Args:
        system_id: The system ID to look up

    Returns:
        SystemSpec if found, None otherwise
    """
    for spec in load_registry():
        if spec.id == system_id:
            return spec
    return None


def get_critical_systems() -> list[SystemSpec]:
    """
    Get all critical messaging systems.

    Returns:
        List of critical SystemSpec objects
    """
    return [spec for spec in load_registry() if spec.critical]


def get_systems_by_category() -> dict[str, list[SystemSpec]]:
    """
    Get all systems grouped by category.

    Returns:
        Dictionary mapping category names to lists of SystemSpec objects
    """
    categories: dict[str, list[SystemSpec]] = {}
    for spec in load_registry():
        if spec.category not in categories:
            categories[spec.category] = []
        categories[spec.category].append(spec)
    return categories
