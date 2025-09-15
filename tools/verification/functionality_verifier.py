#!/usr/bin/env python3
"""
Functionality Verifier - V2 Compliance Module
==========================================

Focused module for verifying functionality preservation.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Functionality Verification
"""

import json
from pathlib import Path
from typing import Any


class FunctionalityVerifier:
    """Verifies functionality preservation during consolidation."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.baseline_file = project_root / "verification_baseline.json"
        self.results_dir = project_root / "verification_results"
        self.results_dir.mkdir(exist_ok=True)

    def verify_functionality_preservation(
        self, current_signature: dict[str, Any]
    ) -> dict[str, Any]:
        """Verify functionality preservation against baseline."""
        verification_result = {
            "timestamp": self._get_timestamp(),
            "baseline_exists": self.baseline_file.exists(),
            "verification_status": "unknown",
            "differences": {},
            "preservation_score": 0.0,
            "recommendations": [],
        }

        if not self.baseline_file.exists():
            verification_result["verification_status"] = "no_baseline"
            verification_result["recommendations"].append("Create baseline signature first")
            return verification_result

        # Load baseline
        try:
            with open(self.baseline_file, encoding="utf-8") as f:
                baseline_signature = json.load(f)
        except Exception as e:
            verification_result["verification_status"] = "baseline_error"
            verification_result["error"] = str(e)
            return verification_result

        # Compare signatures
        differences = self._compare_signatures(baseline_signature, current_signature)
        verification_result["differences"] = differences

        # Calculate preservation score
        preservation_score = self._calculate_preservation_score(
            baseline_signature, current_signature, differences
        )
        verification_result["preservation_score"] = preservation_score

        # Determine verification status
        if preservation_score >= 95.0:
            verification_result["verification_status"] = "preserved"
        elif preservation_score >= 80.0:
            verification_result["verification_status"] = "mostly_preserved"
        else:
            verification_result["verification_status"] = "degraded"

        # Generate recommendations
        verification_result["recommendations"] = self._generate_verification_recommendations(
            differences, preservation_score
        )

        return verification_result

    def _compare_signatures(
        self, baseline: dict[str, Any], current: dict[str, Any]
    ) -> dict[str, Any]:
        """Compare baseline and current signatures."""
        differences = {
            "file_changes": [],
            "import_changes": [],
            "function_changes": [],
            "class_changes": [],
            "test_changes": [],
        }

        # Compare file signatures
        baseline_files = baseline.get("file_signatures", {})
        current_files = current.get("file_signatures", {})

        # Check for changed files
        for file_path, baseline_hash in baseline_files.items():
            current_hash = current_files.get(file_path)
            if current_hash != baseline_hash:
                differences["file_changes"].append(
                    {
                        "file": file_path,
                        "baseline_hash": baseline_hash,
                        "current_hash": current_hash,
                        "change_type": "modified" if current_hash else "deleted",
                    }
                )

        # Check for new files
        for file_path, current_hash in current_files.items():
            if file_path not in baseline_files:
                differences["file_changes"].append(
                    {
                        "file": file_path,
                        "baseline_hash": None,
                        "current_hash": current_hash,
                        "change_type": "added",
                    }
                )

        # Compare other signatures (simplified)
        differences["import_changes"] = self._compare_dict_signatures(
            baseline.get("import_signatures", {}), current.get("import_signatures", {})
        )

        differences["function_changes"] = self._compare_dict_signatures(
            baseline.get("function_signatures", {}), current.get("function_signatures", {})
        )

        differences["class_changes"] = self._compare_dict_signatures(
            baseline.get("class_signatures", {}), current.get("class_signatures", {})
        )

        return differences

    def _compare_dict_signatures(self, baseline: dict, current: dict) -> list[dict[str, Any]]:
        """Compare dictionary signatures."""
        changes = []

        # Check for changes in existing items
        for key, baseline_value in baseline.items():
            current_value = current.get(key)
            if current_value != baseline_value:
                changes.append(
                    {
                        "key": key,
                        "baseline": baseline_value,
                        "current": current_value,
                        "change_type": "modified" if current_value else "deleted",
                    }
                )

        # Check for new items
        for key, current_value in current.items():
            if key not in baseline:
                changes.append(
                    {"key": key, "baseline": None, "current": current_value, "change_type": "added"}
                )

        return changes

    def _calculate_preservation_score(
        self, baseline: dict[str, Any], current: dict[str, Any], differences: dict[str, Any]
    ) -> float:
        """Calculate functionality preservation score."""
        total_items = 0
        preserved_items = 0

        # Count file signatures
        baseline_files = baseline.get("file_signatures", {})
        current_files = current.get("file_signatures", {})
        total_items += len(baseline_files)

        for file_path, baseline_hash in baseline_files.items():
            current_hash = current_files.get(file_path)
            if current_hash == baseline_hash:
                preserved_items += 1

        # Count other signatures
        for sig_type in ["import_signatures", "function_signatures", "class_signatures"]:
            baseline_sigs = baseline.get(sig_type, {})
            current_sigs = current.get(sig_type, {})
            total_items += len(baseline_sigs)

            for key, baseline_value in baseline_sigs.items():
                current_value = current_sigs.get(key)
                if current_value == baseline_value:
                    preserved_items += 1

        if total_items == 0:
            return 100.0

        return (preserved_items / total_items) * 100.0

    def _generate_verification_recommendations(
        self, differences: dict[str, Any], preservation_score: float
    ) -> list[str]:
        """Generate verification recommendations."""
        recommendations = []

        if preservation_score < 95.0:
            recommendations.append(
                "Functionality preservation below 95% - review changes carefully"
            )

        file_changes = differences.get("file_changes", [])
        if len(file_changes) > 10:
            recommendations.append(
                "High number of file changes detected - verify consolidation safety"
            )

        import_changes = differences.get("import_changes", [])
        if len(import_changes) > 5:
            recommendations.append(
                "Significant import changes detected - check dependency integrity"
            )

        function_changes = differences.get("function_changes", [])
        if len(function_changes) > 5:
            recommendations.append("Function signature changes detected - verify API compatibility")

        if preservation_score >= 95.0:
            recommendations.append(
                "Functionality preservation is excellent - consolidation appears safe"
            )

        return recommendations

    def save_baseline(self, signature: dict[str, Any]) -> Path:
        """Save functionality signature as baseline."""
        with open(self.baseline_file, "w", encoding="utf-8") as f:
            json.dump(signature, f, indent=2)

        return self.baseline_file

    def save_verification_result(self, result: dict[str, Any], filename: str = None) -> Path:
        """Save verification result to file."""
        if filename is None:
            timestamp = result.get("timestamp", "").replace(":", "-").replace(".", "-")
            filename = f"verification_result_{timestamp}.json"

        result_path = self.results_dir / filename

        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return result_path

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now().isoformat()
