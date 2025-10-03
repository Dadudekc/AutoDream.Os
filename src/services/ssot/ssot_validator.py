#!/usr/bin/env python3
"""
SSOT Validation Framework
=========================

V2 Compliant: ≤400 lines, implements comprehensive SSOT validation
across all system files and configurations.

This module provides automated validation of Single Source of Truth
compliance across agent roles, configurations, and documentation.

🐝 WE ARE SWARM - SSOT System Optimization
"""

import json
import logging
from pathlib import Path
from typing import Any

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SSOTValidator:
    """Validates Single Source of Truth compliance across all systems."""

    def __init__(self, project_root: str = "."):
        """Initialize SSOT validator."""
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        self.violations = []
        self.consistency_score = 0

    def validate_all(self) -> dict[str, Any]:
        """Validate SSOT compliance across all systems."""
        logger.info("Starting comprehensive SSOT validation")

        results = {
            "agent_roles": self._validate_agent_roles(),
            "configurations": self._validate_configurations(),
            "documentation": self._validate_documentation(),
            "coordinates": self._validate_coordinates(),
            "consistency_score": self.consistency_score,
            "violations": self.violations,
        }

        logger.info(f"SSOT validation complete. Score: {self.consistency_score}%")
        return results

    def _validate_agent_roles(self) -> dict[str, Any]:
        """Validate agent role consistency across all files."""
        logger.info("Validating agent role consistency")

        # Load all configuration files
        config_files = {
            "unified_config.json": self._load_json(self.config_dir / "unified_config.json"),
            "unified_config.yaml": self._load_yaml(self.config_dir / "unified_config.yaml"),
            "agent_capabilities.json": self._load_json(self.config_dir / "agent_capabilities.json"),
        }

        # Extract agent roles
        roles = {}
        for file_name, config in config_files.items():
            if config:
                roles[file_name] = self._extract_agent_roles(config)

        # Check consistency
        consistency_issues = []
        if len(roles) > 1:
            reference_roles = list(roles.values())[0]
            for file_name, file_roles in roles.items():
                if file_roles != reference_roles:
                    consistency_issues.append(f"Role mismatch in {file_name}")

        return {
            "files_checked": list(config_files.keys()),
            "consistency_issues": consistency_issues,
            "agent_roles": roles,
        }

    def _validate_configurations(self) -> dict[str, Any]:
        """Validate configuration consistency."""
        logger.info("Validating configuration consistency")

        json_config = self._load_json(self.config_dir / "unified_config.json")
        yaml_config = self._load_yaml(self.config_dir / "unified_config.yaml")

        if not json_config or not yaml_config:
            return {"error": "Configuration files not found"}

        # Compare key fields
        consistency_issues = []

        # Check agent roles
        if "agents" in json_config and "agents" in yaml_config:
            for agent_id in json_config["agents"]:
                if agent_id in yaml_config["agents"]:
                    json_role = json_config["agents"][agent_id].get("role")
                    yaml_role = yaml_config["agents"][agent_id].get("role")
                    if json_role != yaml_role:
                        consistency_issues.append(
                            f"Role mismatch for {agent_id}: JSON={json_role}, YAML={yaml_role}"
                        )

        return {
            "consistency_issues": consistency_issues,
            "json_agents": len(json_config.get("agents", {})),
            "yaml_agents": len(yaml_config.get("agents", {})),
        }

    def _validate_documentation(self) -> dict[str, Any]:
        """Validate documentation consistency."""
        logger.info("Validating documentation consistency")

        docs_to_check = ["AGENTS.md", "AGENT_ONBOARDING_CONTEXT_PACKAGE.md"]

        consistency_issues = []

        for doc_file in docs_to_check:
            doc_path = self.project_root / doc_file
            if doc_path.exists():
                content = doc_path.read_text(encoding="utf-8")

                # Check for Agent-6 SSOT_MANAGER references
                if "Agent-6 (SSOT_MANAGER)" in content:
                    consistency_issues.append(
                        f"{doc_file}: Agent-6 incorrectly listed as SSOT_MANAGER"
                    )

                # Check for Agent-8 SSOT_MANAGER references
                if "Agent-8 (SSOT_MANAGER)" not in content and "SSOT_MANAGER" in content:
                    consistency_issues.append(f"{doc_file}: Missing Agent-8 SSOT_MANAGER reference")

        return {"files_checked": docs_to_check, "consistency_issues": consistency_issues}

    def _validate_coordinates(self) -> dict[str, Any]:
        """Validate coordinate consistency."""
        logger.info("Validating coordinate consistency")

        coord_files = {
            "coordinates.json": self._load_json(self.config_dir / "coordinates.json"),
            "unified_config.json": self._load_json(self.config_dir / "unified_config.json"),
            "unified_config.yaml": self._load_yaml(self.config_dir / "unified_config.yaml"),
        }

        consistency_issues = []

        # Extract coordinates from all files
        all_coords = {}
        for file_name, config in coord_files.items():
            if config:
                all_coords[file_name] = self._extract_coordinates(config)

        # Check consistency
        if len(all_coords) > 1:
            reference_coords = list(all_coords.values())[0]
            for file_name, coords in all_coords.items():
                if coords != reference_coords:
                    consistency_issues.append(f"Coordinate mismatch in {file_name}")

        return {
            "files_checked": list(coord_files.keys()),
            "consistency_issues": consistency_issues,
            "coordinates": all_coords,
        }

    def _load_json(self, file_path: Path) -> dict[str, Any]:
        """Load JSON file safely."""
        try:
            if file_path.exists():
                with open(file_path, encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
        return {}

    def _load_yaml(self, file_path: Path) -> dict[str, Any]:
        """Load YAML file safely."""
        try:
            if file_path.exists():
                with open(file_path, encoding="utf-8") as f:
                    return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
        return {}

    def _extract_agent_roles(self, config: dict[str, Any]) -> dict[str, str]:
        """Extract agent roles from configuration."""
        roles = {}

        if "agents" in config:
            for agent_id, agent_config in config["agents"].items():
                if isinstance(agent_config, dict) and "role" in agent_config:
                    roles[agent_id] = agent_config["role"]

        return roles

    def _extract_coordinates(self, config: dict[str, Any]) -> dict[str, list[int]]:
        """Extract coordinates from configuration."""
        coords = {}

        if "agents" in config:
            for agent_id, agent_config in config["agents"].items():
                if isinstance(agent_config, dict) and "coordinates" in agent_config:
                    coords[agent_id] = agent_config["coordinates"]

        return coords


def main():
    """Main execution function."""
    validator = SSOTValidator()
    results = validator.validate_all()

    print("SSOT Validation Results:")
    print(f"Consistency Score: {results['consistency_score']}%")
    print(f"Violations: {len(results['violations'])}")

    if results["violations"]:
        print("\nViolations found:")
        for violation in results["violations"]:
            print(f"  - {violation}")


if __name__ == "__main__":
    main()
