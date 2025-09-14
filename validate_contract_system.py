#!/usr/bin/env python3
"""
Contract System Validation Script
=================================

Validates the contract system functionality and ensures all contracts
are properly configured and accessible.
"""

import json
from pathlib import Path
from typing import Any

import yaml


class ContractSystemValidator:
    """Validates the contract system functionality."""

    def __init__(self, contracts_dir: str = "contracts"):
        self.contracts_dir = Path(contracts_dir)
        self.validation_results = {
            "total_contracts": 0,
            "valid_contracts": 0,
            "invalid_contracts": 0,
            "missing_files": 0,
            "yaml_validation": True,
            "contract_references": [],
            "errors": [],
        }

    def validate_contract_system(self) -> dict[str, Any]:
        """Validate the entire contract system."""
        print("🔍 CONTRACT SYSTEM VALIDATION")
        print("=" * 50)

        # Validate swarm_contract.yaml
        if not self._validate_swarm_contract():
            self.validation_results["yaml_validation"] = False
            return self.validation_results

        # Validate individual contracts
        self._validate_contract_files()

        # Validate contract references
        self._validate_contract_references()

        # Print validation summary
        self._print_validation_summary()

        return self.validation_results

    def _validate_swarm_contract(self) -> bool:
        """Validate swarm_contract.yaml file."""
        swarm_contract_path = self.contracts_dir / "swarm_contract.yaml"

        if not swarm_contract_path.exists():
            self.validation_results["errors"].append("❌ swarm_contract.yaml not found")
            return False

        try:
            with open(swarm_contract_path, encoding="utf-8") as f:
                swarm_data = yaml.safe_load(f)

            # Validate required sections
            required_sections = ["swarm_contract"]

            for section in required_sections:
                if section not in swarm_data:
                    self.validation_results["errors"].append(
                        f"❌ Missing required section: {section}"
                    )
                    return False

            swarm_contract = swarm_data.get("swarm_contract", {})

            # Validate agent_roles within swarm_contract
            if "agent_roles" not in swarm_contract:
                self.validation_results["errors"].append(
                    "❌ Missing agent_roles in swarm_contract section"
                )
                return False

            # Validate available_contracts structure
            available_contracts = swarm_data.get("available_contracts", {})
            for contract_id, contract_info in available_contracts.items():
                required_fields = ["file", "title", "priority", "deadline", "value", "focus"]
                for field in required_fields:
                    if field not in contract_info:
                        self.validation_results["errors"].append(
                            f"❌ Contract {contract_id} missing field: {field}"
                        )

            print("✅ swarm_contract.yaml validation passed")
            return True

        except Exception as e:
            self.validation_results["errors"].append(
                f"❌ Error validating swarm_contract.yaml: {e}"
            )
            return False

    def _validate_contract_files(self) -> None:
        """Validate individual contract JSON files."""
        if not self.contracts_dir.exists():
            self.validation_results["errors"].append("❌ Contracts directory not found")
            return

        # Get all JSON files (excluding archive)
        contract_files = []
        for file_path in self.contracts_dir.glob("*.json"):
            if "archive" not in str(file_path):
                contract_files.append(file_path)

        self.validation_results["total_contracts"] = len(contract_files)

        for contract_file in contract_files:
            self._validate_single_contract(contract_file)

    def _validate_single_contract(self, contract_path: Path) -> None:
        """Validate a single contract file."""
        try:
            with open(contract_path, encoding="utf-8") as f:
                contract_data = json.load(f)

            # Validate required fields
            required_fields = [
                "contract_id",
                "contract_title",
                "agent_id",
                "contract_type",
                "priority",
                "status",
                "contract_details",
            ]

            for field in required_fields:
                if field not in contract_data:
                    self.validation_results["errors"].append(
                        f"❌ Contract {contract_path.name} missing field: {field}"
                    )
                    self.validation_results["invalid_contracts"] += 1
                    return

            # Validate contract_details structure
            contract_details = contract_data.get("contract_details", {})
            required_details = ["description", "objectives", "deliverables", "success_criteria"]

            for detail in required_details:
                if detail not in contract_details:
                    self.validation_results["errors"].append(
                        f"❌ Contract {contract_path.name} missing contract_details field: {detail}"
                    )
                    self.validation_results["invalid_contracts"] += 1
                    return

            # Add to valid contracts
            self.validation_results["valid_contracts"] += 1
            self.validation_results["contract_references"].append(
                {
                    "id": contract_data["contract_id"],
                    "title": contract_data["contract_title"],
                    "file": contract_path.name,
                    "priority": contract_data["priority"],
                    "status": contract_data["status"],
                }
            )

            print(f"✅ Validated contract: {contract_path.name}")

        except Exception as e:
            self.validation_results["errors"].append(
                f"❌ Error validating {contract_path.name}: {e}"
            )
            self.validation_results["invalid_contracts"] += 1

    def _validate_contract_references(self) -> None:
        """Validate that all contracts referenced in swarm_contract.yaml exist."""
        swarm_contract_path = self.contracts_dir / "swarm_contract.yaml"

        try:
            with open(swarm_contract_path, encoding="utf-8") as f:
                swarm_data = yaml.safe_load(f)

            available_contracts = swarm_data.get("available_contracts", {})

            for contract_id, contract_info in available_contracts.items():
                contract_file = contract_info.get("file")
                if not contract_file:
                    self.validation_results["errors"].append(
                        f"❌ Contract {contract_id} missing file reference"
                    )
                    continue

                contract_path = self.contracts_dir / contract_file
                if not contract_path.exists():
                    self.validation_results["errors"].append(
                        f"❌ Referenced contract file not found: {contract_file}"
                    )
                    self.validation_results["missing_files"] += 1

        except Exception as e:
            self.validation_results["errors"].append(
                f"❌ Error validating contract references: {e}"
            )

    def _print_validation_summary(self) -> None:
        """Print validation summary."""
        print("\n📊 VALIDATION SUMMARY")
        print("=" * 30)
        print(f"Total Contracts: {self.validation_results['total_contracts']}")
        print(f"Valid Contracts: {self.validation_results['valid_contracts']}")
        print(f"Invalid Contracts: {self.validation_results['invalid_contracts']}")
        print(f"Missing Files: {self.validation_results['missing_files']}")
        print(
            f"YAML Validation: {'✅ PASSED' if self.validation_results['yaml_validation'] else '❌ FAILED'}"
        )

        if self.validation_results["contract_references"]:
            print("\n📋 Available Contracts:")
            for contract in self.validation_results["contract_references"]:
                status_icon = "✅" if contract["status"] == "AVAILABLE" else "🔄"
                print(f"  {status_icon} {contract['id']}: {contract['title']}")
                print(f"      Priority: {contract['priority']} | File: {contract['file']}")

        if self.validation_results["errors"]:
            print("\n❌ ERRORS FOUND:")
            for error in self.validation_results["errors"]:
                print(f"  {error}")

        # Overall validation result
        total_errors = len(self.validation_results["errors"])
        if total_errors == 0 and self.validation_results["yaml_validation"]:
            print("\n🎉 CONTRACT SYSTEM VALIDATION: SUCCESS")
            print("✅ All contracts are valid and properly configured")
            print("✅ Contract system is ready for agent assignment")
        else:
            print(f"\n⚠️ CONTRACT SYSTEM VALIDATION: ISSUES FOUND ({total_errors} errors)")
            print("❌ Contract system requires attention before use")


def main():
    """Main validation function."""
    print("🤖 Agent-6 Contract System Validation")
    print("Specialty: Web Interface & Communication")
    print("-" * 50)

    validator = ContractSystemValidator()

    # Run validation
    results = validator.validate_contract_system()

    # Return exit code based on validation
    if results["yaml_validation"] and len(results["errors"]) == 0:
        print("\n✅ CONTRACT SYSTEM READY FOR USE")
        return 0
    else:
        print("\n❌ CONTRACT SYSTEM REQUIRES FIXES")
        return 1


if __name__ == "__main__":
    exit(main())
