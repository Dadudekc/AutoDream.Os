#!/usr/bin/env python3
"""
General Cycle Escalation Threshold Standardizer
==============================================

V2 Compliant: ≤400 lines, implements escalation threshold standardization
for all agent roles in the General Cycle.

This module standardizes escalation thresholds across all agent roles
to ensure consistent escalation behavior and prevent role confusion.

🐝 WE ARE SWARM - General Cycle Optimization
"""

import json
import logging
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EscalationStandardizer:
    """Standardizes escalation thresholds across all agent roles."""

    def __init__(self, config_dir: str = "config"):
        """Initialize escalation standardizer."""
        self.config_dir = Path(config_dir)
        self.standard_threshold = "10_minutes"
        self.escalation_levels = {
            "CRITICAL": "immediate",
            "HIGH": "5_minutes",
            "MEDIUM": "10_minutes",
            "LOW": "30_minutes",
        }

    def standardize_all_roles(self) -> dict[str, Any]:
        """Standardize escalation thresholds for all agent roles."""
        logger.info("Starting escalation threshold standardization")

        results = {
            "standardized_roles": [],
            "updated_files": [],
            "standard_threshold": self.standard_threshold,
        }

        # Process all role protocol files
        protocol_dir = self.config_dir / "protocols"
        if protocol_dir.exists():
            for protocol_file in protocol_dir.glob("*.json"):
                if self._standardize_role_file(protocol_file):
                    results["standardized_roles"].append(protocol_file.stem)
                    results["updated_files"].append(str(protocol_file))

        logger.info(f"Standardized {len(results['standardized_roles'])} roles")
        return results

    def _standardize_role_file(self, protocol_file: Path) -> bool:
        """Standardize escalation thresholds in a role protocol file."""
        try:
            with open(protocol_file, encoding="utf-8") as f:
                data = json.load(f)

            updated = False

            # Standardize escalation procedures
            if "escalation_procedures" in data:
                for procedure, threshold in data["escalation_procedures"].items():
                    if isinstance(threshold, str) and "minute" in threshold.lower():
                        data["escalation_procedures"][procedure] = self.standard_threshold
                        updated = True

            # Standardize general cycle adaptations
            if "general_cycle_adaptations" in data:
                for phase, config in data["general_cycle_adaptations"].items():
                    if isinstance(config, dict) and "escalation_threshold" in config:
                        config["escalation_threshold"] = self.standard_threshold
                        updated = True

            # Save updated file
            if updated:
                with open(protocol_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"Updated escalation thresholds in {protocol_file.name}")
                return True

        except Exception as e:
            logger.error(f"Error processing {protocol_file}: {e}")

        return False

    def validate_standardization(self) -> dict[str, Any]:
        """Validate that standardization was applied correctly."""
        logger.info("Validating escalation threshold standardization")

        validation_results = {
            "validated_files": [],
            "non_standard_files": [],
            "standard_threshold": self.standard_threshold,
        }

        protocol_dir = self.config_dir / "protocols"
        if protocol_dir.exists():
            for protocol_file in protocol_dir.glob("*.json"):
                if self._validate_file(protocol_file):
                    validation_results["validated_files"].append(str(protocol_file))
                else:
                    validation_results["non_standard_files"].append(str(protocol_file))

        return validation_results

    def _validate_file(self, protocol_file: Path) -> bool:
        """Validate that a file has standard escalation thresholds."""
        try:
            with open(protocol_file, encoding="utf-8") as f:
                data = json.load(f)

            # Check escalation procedures
            if "escalation_procedures" in data:
                for threshold in data["escalation_procedures"].values():
                    if isinstance(threshold, str) and threshold != self.standard_threshold:
                        return False

            # Check general cycle adaptations
            if "general_cycle_adaptations" in data:
                for config in data["general_cycle_adaptations"].values():
                    if isinstance(config, dict) and "escalation_threshold" in config:
                        if config["escalation_threshold"] != self.standard_threshold:
                            return False

            return True

        except Exception as e:
            logger.error(f"Error validating {protocol_file}: {e}")
            return False


def main():
    """Main execution function."""
    standardizer = EscalationStandardizer()

    # Execute standardization
    results = standardizer.standardize_all_roles()
    print(f"Standardized {len(results['standardized_roles'])} roles")
    print(f"Updated {len(results['updated_files'])} files")

    # Validate results
    validation = standardizer.validate_standardization()
    print(f"Validated {len(validation['validated_files'])} files")

    if validation["non_standard_files"]:
        print(f"Non-standard files: {validation['non_standard_files']}")


if __name__ == "__main__":
    main()
