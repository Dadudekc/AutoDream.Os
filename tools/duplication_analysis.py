#!/usr/bin/env python3
"""
Duplication Analysis - V2 Compliant
====================================

Analyzes scan results to categorize duplications.
Extracted from duplication_analyzer.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

import difflib
from typing import Any


class DuplicationAnalysis:
    """Analyzes and categorizes duplications."""

    def analyze_duplicates(self, scan_results: dict[str, Any]) -> dict[str, Any]:
        """Analyze scan results to categorize duplications."""
        print("🔍 Analyzing duplication patterns...")

        analysis = {
            "true_duplicates": [],
            "similar_functions": [],
            "false_duplicates": [],
            "consolidation_candidates": [],
            "risk_assessment": {},
        }

        # Analyze functions
        for hash_key, instances in scan_results["functions"].items():
            if len(instances) > 1:
                category = self._categorize_function_duplicates(instances)
                analysis[category].append(
                    {
                        "hash": hash_key,
                        "instances": instances,
                        "similarity_score": self._calculate_similarity(instances),
                    }
                )

        # Analyze classes
        for hash_key, instances in scan_results["classes"].items():
            if len(instances) > 1:
                category = self._categorize_class_duplicates(instances)
                analysis[category].append(
                    {
                        "hash": hash_key,
                        "instances": instances,
                        "similarity_score": self._calculate_similarity(instances),
                    }
                )

        # Generate consolidation plan
        from .duplication_planner import DuplicationPlanner

        planner = DuplicationPlanner()
        analysis["consolidation_plan"] = planner.generate_consolidation_plan(analysis)

        return analysis

    def _categorize_function_duplicates(self, instances: list[dict]) -> str:
        """Categorize function duplicates."""
        if len(instances) < 2:
            return "false_duplicates"

        names = [inst["name"] for inst in instances]
        files = [inst["file"] for inst in instances]

        # Same name in different modules might be different functions
        if len(set(names)) == 1 and len(set(files)) > 1:
            domains = [self._get_file_domain(f) for f in files]
            if len(set(domains)) > 1:
                return "false_duplicates"

        # Check content similarity
        contents = [inst["content"] for inst in instances]
        if self._are_contents_identical(contents):
            return "true_duplicates"
        elif self._are_contents_similar(contents):
            return "similar_functions"
        else:
            return "false_duplicates"

    def _categorize_class_duplicates(self, instances: list[dict]) -> str:
        """Categorize class duplicates."""
        if len(instances) < 2:
            return "false_duplicates"

        names = [inst["name"] for inst in instances]
        if len(set(names)) == 1:
            files = [inst["file"] for inst in instances]
            domains = [self._get_file_domain(f) for f in files]
            if len(set(domains)) > 1:
                return "false_duplicates"

        return "true_duplicates"

    def _get_file_domain(self, file_path: str) -> str:
        """Get the domain/module category of a file."""
        path_parts = file_path.split("/")
        if len(path_parts) >= 2:
            return path_parts[1]
        return "unknown"

    def _are_contents_identical(self, contents: list[str]) -> bool:
        """Check if contents are identical."""
        if not contents:
            return False
        first = contents[0]
        return all(content == first for content in contents)

    def _are_contents_similar(self, contents: list[str]) -> bool:
        """Check if contents are similar (but not identical)."""
        if len(contents) < 2:
            return False

        for i in range(len(contents)):
            for j in range(i + 1, len(contents)):
                similarity = difflib.SequenceMatcher(None, contents[i], contents[j]).ratio()
                if similarity > 0.8:  # 80% similar
                    return True
        return False

    def _calculate_similarity(self, instances: list[dict]) -> float:
        """Calculate average similarity between instances."""
        if len(instances) < 2:
            return 1.0

        contents = [inst["content"] for inst in instances]
        similarities = []

        for i in range(len(contents)):
            for j in range(i + 1, len(contents)):
                similarity = difflib.SequenceMatcher(None, contents[i], contents[j]).ratio()
                similarities.append(similarity)

        return sum(similarities) / len(similarities) if similarities else 1.0
