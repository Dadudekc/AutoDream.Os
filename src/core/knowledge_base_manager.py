"""
Knowledge Base Manager Module - V2 Compliant (≤200 lines)
High-level knowledge management operations and batch processing.
"""

from typing import Any

from .knowledge_base_core import (
    AntiPattern,
    CodePattern,
    DesignPrinciple,
    KnowledgeBaseCore,
    PrincipleCategory,
)


class KnowledgeBaseManager:
    """
    High-level knowledge management for AutoDream.OS design principles.

    Handles batch operations, search, filtering, and analytics for the
    knowledge base system.
    """

    def __init__(self, core: KnowledgeBaseCore | None = None):
        """Initialize the knowledge manager with core instance."""
        self.core = core or KnowledgeBaseCore()

    def bulk_add_principles(self, principles: list[dict[str, Any]]) -> list[str]:
        """Add multiple design principles in batch."""
        added_principles = []

        for principle_data in principles:
            try:
                principle = DesignPrinciple(
                    name=principle_data["name"],
                    category=PrincipleCategory(principle_data["category"]),
                    description=principle_data["description"],
                    rationale=principle_data["rationale"],
                    examples=principle_data.get("examples", []),
                    anti_examples=principle_data.get("anti_examples", []),
                    enforcement_level=principle_data.get("enforcement_level", "optional"),
                    related_principles=principle_data.get("related_principles", []),
                )
                self.core.design_principles[principle.name] = principle
                added_principles.append(principle.name)
            except Exception as e:
                print(f"Failed to add principle {principle_data.get('name', 'unknown')}: {e}")

        return added_principles

    def bulk_add_patterns(self, patterns: list[dict[str, Any]]) -> list[str]:
        """Add multiple code patterns in batch."""
        added_patterns = []

        for pattern_data in patterns:
            try:
                pattern = CodePattern(
                    name=pattern_data["name"],
                    pattern_type=pattern_data["pattern_type"],
                    description=pattern_data["description"],
                    code_example=pattern_data["code_example"],
                    when_to_use=pattern_data.get("when_to_use", []),
                    when_not_to_use=pattern_data.get("when_not_to_use", []),
                    complexity_score=pattern_data.get("complexity_score", 1),
                )
                self.core.code_patterns[pattern.name] = pattern
                added_patterns.append(pattern.name)
            except Exception as e:
                print(f"Failed to add pattern {pattern_data.get('name', 'unknown')}: {e}")

        return added_patterns

    def search_knowledge(self, query: str, search_type: str = "all") -> dict[str, list[Any]]:
        """Search across all knowledge types."""
        results = {"principles": [], "patterns": [], "anti_patterns": []}

        query_lower = query.lower()

        if search_type in ["all", "principles"]:
            for principle in self.core.design_principles.values():
                if (
                    query_lower in principle.name.lower()
                    or query_lower in principle.description.lower()
                    or query_lower in principle.rationale.lower()
                ):
                    results["principles"].append(principle)

        if search_type in ["all", "patterns"]:
            for pattern in self.core.code_patterns.values():
                if (
                    query_lower in pattern.name.lower()
                    or query_lower in pattern.description.lower()
                ):
                    results["patterns"].append(pattern)

        if search_type in ["all", "anti_patterns"]:
            for anti_pattern in self.core.anti_patterns.values():
                if (
                    query_lower in anti_pattern.name.lower()
                    or query_lower in anti_pattern.description.lower()
                ):
                    results["anti_patterns"].append(anti_pattern)

        return results

    def filter_by_category(self, category: PrincipleCategory) -> list[DesignPrinciple]:
        """Filter principles by category."""
        return self.core.get_principles_by_category(category)

    def filter_by_complexity(self, max_complexity: int = 3) -> list[CodePattern]:
        """Filter patterns by complexity score."""
        return self.core.get_simple_patterns(max_complexity)

    def filter_by_severity(self, severity: str) -> list[AntiPattern]:
        """Filter anti-patterns by severity."""
        return [
            anti_pattern
            for anti_pattern in self.core.anti_patterns.values()
            if anti_pattern.severity == severity
        ]

    def get_statistics(self) -> dict[str, Any]:
        """Get comprehensive statistics about the knowledge base."""
        return {
            "total_principles": len(self.core.design_principles),
            "total_patterns": len(self.core.code_patterns),
            "total_anti_patterns": len(self.core.anti_patterns),
            "principles_by_category": {
                category.value: len(self.core.get_principles_by_category(category))
                for category in PrincipleCategory
            },
            "patterns_by_complexity": {
                f"complexity_{i}": len(
                    [p for p in self.core.code_patterns.values() if p.complexity_score == i]
                )
                for i in range(1, 11)
            },
            "anti_patterns_by_severity": {
                severity: len(self.filter_by_severity(severity))
                for severity in ["critical", "major", "minor"]
            },
            "required_principles": len(self.core.get_required_principles()),
            "critical_anti_patterns": len(self.core.get_critical_anti_patterns()),
        }

    def export_knowledge(self, export_type: str = "all") -> dict[str, Any]:
        """Export knowledge base data."""
        export_data = {}

        if export_type in ["all", "principles"]:
            export_data["principles"] = {
                name: {
                    "name": p.name,
                    "category": p.category.value,
                    "description": p.description,
                    "rationale": p.rationale,
                    "examples": p.examples,
                    "anti_examples": p.anti_examples,
                    "enforcement_level": p.enforcement_level,
                    "related_principles": p.related_principles,
                }
                for name, p in self.core.design_principles.items()
            }

        if export_type in ["all", "patterns"]:
            export_data["patterns"] = {
                name: {
                    "name": p.name,
                    "pattern_type": p.pattern_type,
                    "description": p.description,
                    "code_example": p.code_example,
                    "when_to_use": p.when_to_use,
                    "when_not_to_use": p.when_not_to_use,
                    "complexity_score": p.complexity_score,
                }
                for name, p in self.core.code_patterns.items()
            }

        if export_type in ["all", "anti_patterns"]:
            export_data["anti_patterns"] = {
                name: {
                    "name": ap.name,
                    "description": ap.description,
                    "why_bad": ap.why_bad,
                    "common_manifestations": ap.common_manifestations,
                    "better_alternatives": ap.better_alternatives,
                    "severity": ap.severity,
                }
                for name, ap in self.core.anti_patterns.items()
            }

        if export_type in ["all", "guidelines"]:
            export_data["guidelines"] = self.core.get_all_guidelines()

        return export_data

    def import_knowledge(self, import_data: dict[str, Any]) -> dict[str, int]:
        """Import knowledge base data."""
        import_results = {
            "principles_added": 0,
            "patterns_added": 0,
            "anti_patterns_added": 0,
            "errors": 0,
        }

        # Import principles
        if "principles" in import_data:
            principles_data = [
                principle_data for principle_data in import_data["principles"].values()
            ]
            added = self.bulk_add_principles(principles_data)
            import_results["principles_added"] = len(added)

        # Import patterns
        if "patterns" in import_data:
            patterns_data = [pattern_data for pattern_data in import_data["patterns"].values()]
            added = self.bulk_add_patterns(patterns_data)
            import_results["patterns_added"] = len(added)

        # Import anti-patterns
        if "anti_patterns" in import_data:
            for name, anti_pattern_data in import_data["anti_patterns"].items():
                try:
                    anti_pattern = AntiPattern(
                        name=anti_pattern_data["name"],
                        description=anti_pattern_data["description"],
                        why_bad=anti_pattern_data["why_bad"],
                        common_manifestations=anti_pattern_data["common_manifestations"],
                        better_alternatives=anti_pattern_data["better_alternatives"],
                        severity=anti_pattern_data["severity"],
                    )
                    self.core.anti_patterns[name] = anti_pattern
                    import_results["anti_patterns_added"] += 1
                except Exception as e:
                    print(f"Failed to import anti-pattern {name}: {e}")
                    import_results["errors"] += 1

        return import_results

    def validate_knowledge_consistency(self) -> dict[str, list[str]]:
        """Validate consistency across knowledge base."""
        issues = {
            "missing_related_principles": [],
            "invalid_categories": [],
            "complexity_mismatches": [],
        }

        # Check for missing related principles
        for principle in self.core.design_principles.values():
            for related in principle.related_principles:
                if related not in self.core.design_principles:
                    issues["missing_related_principles"].append(
                        f"Principle '{principle.name}' references missing '{related}'"
                    )

        # Check for invalid categories
        for principle in self.core.design_principles.values():
            if not isinstance(principle.category, PrincipleCategory):
                issues["invalid_categories"].append(
                    f"Principle '{principle.name}' has invalid category"
                )

        # Check complexity scores
        for pattern in self.core.code_patterns.values():
            if not (1 <= pattern.complexity_score <= 10):
                issues["complexity_mismatches"].append(
                    f"Pattern '{pattern.name}' has invalid complexity score: {pattern.complexity_score}"
                )

        return issues
