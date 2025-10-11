#!/usr/bin/env python3
"""
Functionality Comparison Engine
================================

Compares current functionality against baseline.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored from: functionality_verification.py
License: MIT
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class FunctionalityComparison:
    """Compares functionality signatures."""

    def __init__(self, baseline_file: Path):
        """Initialize comparison engine."""
        self.baseline_file = baseline_file

    def save_baseline(self, signature: dict[str, Any]) -> None:
        """Save functionality baseline."""
        with open(self.baseline_file, "w", encoding="utf-8") as f:
            json.dump(signature, f, indent=2, ensure_ascii=False)
        print(f"✅ Baseline saved to {self.baseline_file}")

    def load_baseline(self) -> dict[str, Any] | None:
        """Load functionality baseline."""
        if self.baseline_file.exists():
            with open(self.baseline_file, encoding="utf-8") as f:
                return json.load(f)
        return None

    def compare_with_baseline(self, current_signature: dict[str, Any]) -> dict[str, Any]:
        """Compare current state with baseline."""
        baseline = self.load_baseline()
        if not baseline:
            return {"error": "No baseline found. Run --baseline first."}

        comparison = {
            "timestamp": datetime.now().isoformat(),
            "baseline_timestamp": baseline["timestamp"],
            "files_changed": [],
            "functions_lost": [],
            "classes_lost": [],
            "new_functions": [],
            "new_classes": [],
            "import_changes": [],
            "risk_assessment": "LOW",
        }

        # Compare files
        baseline_files = set(baseline["files"].keys())
        current_files = set(current_signature["files"].keys())

        removed_files = baseline_files - current_files
        added_files = current_files - baseline_files

        for file in removed_files:
            comparison["files_changed"].append(f"REMOVED: {file}")

        for file in added_files:
            comparison["files_changed"].append(f"ADDED: {file}")

        # Compare functions and classes in common files
        common_files = baseline_files & current_files
        for file in common_files:
            baseline_info = baseline["files"][file]
            current_info = current_signature["files"][file]

            # Check functions
            baseline_funcs = set(baseline_info.get("functions", []))
            current_funcs = set(current_info.get("functions", []))
            lost_funcs = baseline_funcs - current_funcs
            new_funcs = current_funcs - baseline_funcs

            for func in lost_funcs:
                comparison["functions_lost"].append(f"{file}:{func}")
            for func in new_funcs:
                comparison["new_functions"].append(f"{file}:{func}")

            # Check classes
            baseline_classes = set(baseline_info.get("classes", []))
            current_classes = set(current_info.get("classes", []))
            lost_classes = baseline_classes - current_classes
            new_classes = current_classes - baseline_classes

            for cls in lost_classes:
                comparison["classes_lost"].append(f"{file}:{cls} (class)")
            for cls in new_classes:
                comparison["new_classes"].append(f"{file}:{cls} (class)")

        # Assess risk
        if comparison["functions_lost"] or len(removed_files) > 10:
            comparison["risk_assessment"] = "HIGH"
        elif len(comparison["files_changed"]) > 20:
            comparison["risk_assessment"] = "MEDIUM"
        else:
            comparison["risk_assessment"] = "LOW"

        return comparison
