#!/usr/bin/env python3
"""
Knowledge Base Principles - Design Principles Management
=========================================================

Design principles management for knowledge base system.
Handles creation and management of design principles.

V2 Compliance: ≤400 lines, focused principles management module
Author: Agent-6 (Quality Assurance Specialist)
"""

from .knowledge_base_models import DesignPrinciple, PrincipleCategory


class KnowledgeBasePrinciples:
    """
    Design principles management for knowledge base.

    Handles creation and management of design principles.
    """

    def __init__(self):
        """Initialize principles manager."""
        self.principles: dict[str, DesignPrinciple] = {}
        self._load_design_principles()

    def _load_design_principles(self) -> None:
        """Load all design principles."""
        self.principles = {
            "kiss": self._create_kiss_principle(),
            "yagni": self._create_yagni_principle(),
            "sr": self._create_sr_principle(),
            "error_handling": self._create_error_handling_principle(),
            "fail_fast": self._create_fail_fast_principle(),
            "composition": self._create_composition_principle(),
        }

    def _create_kiss_principle(self) -> DesignPrinciple:
        """Create KISS principle."""
        return DesignPrinciple(
            name="KISS (Keep It Simple, Stupid)",
            category=PrincipleCategory.SIMPLICITY,
            description="Keep code simple and straightforward",
            rationale="Simple code is easier to understand, maintain, and debug",
            examples=[
                "Use clear variable names",
                "Write small, focused functions",
                "Avoid unnecessary complexity",
            ],
            anti_examples=[
                "Overly complex algorithms for simple problems",
                "Deeply nested conditionals",
                "Unnecessary abstractions",
            ],
            enforcement_level="required",
            related_principles=["yagni", "sr"],
        )

    def _create_yagni_principle(self) -> DesignPrinciple:
        """Create YAGNI principle."""
        return DesignPrinciple(
            name="YAGNI (You Aren't Gonna Need It)",
            category=PrincipleCategory.SIMPLICITY,
            description="Don't implement functionality until you need it",
            rationale="Avoids over-engineering and keeps code focused",
            examples=[
                "Don't add features 'just in case'",
                "Implement only current requirements",
                "Refactor when requirements change",
            ],
            anti_examples=[
                "Adding unused parameters",
                "Creating unnecessary abstractions",
                "Implementing future features early",
            ],
            enforcement_level="required",
            related_principles=["kiss", "sr"],
        )

    def _create_sr_principle(self) -> DesignPrinciple:
        """Create Single Responsibility principle."""
        return DesignPrinciple(
            name="Single Responsibility Principle",
            category=PrincipleCategory.MAINTAINABILITY,
            description="A class should have only one reason to change",
            rationale="Makes code more maintainable and testable",
            examples=[
                "Separate data access from business logic",
                "One class per responsibility",
                "Clear separation of concerns",
            ],
            anti_examples=[
                "God classes with multiple responsibilities",
                "Mixed concerns in single class",
                "Classes that do too much",
            ],
            enforcement_level="required",
            related_principles=["kiss", "composition"],
        )

    def _create_error_handling_principle(self) -> DesignPrinciple:
        """Create error handling principle."""
        return DesignPrinciple(
            name="Proper Error Handling",
            category=PrincipleCategory.MAINTAINABILITY,
            description="Handle errors gracefully and explicitly",
            rationale="Prevents crashes and provides clear error information",
            examples=[
                "Use specific exception types",
                "Provide meaningful error messages",
                "Log errors appropriately",
            ],
            anti_examples=["Bare except clauses", "Silent failures", "Generic error messages"],
            enforcement_level="required",
            related_principles=["fail_fast"],
        )

    def _create_fail_fast_principle(self) -> DesignPrinciple:
        """Create fail fast principle."""
        return DesignPrinciple(
            name="Fail Fast",
            category=PrincipleCategory.MAINTAINABILITY,
            description="Detect and report errors as early as possible",
            rationale="Easier to debug and fix issues early",
            examples=[
                "Validate inputs early",
                "Use assertions for invariants",
                "Check preconditions",
            ],
            anti_examples=["Silent failures", "Late error detection", "Ignoring validation errors"],
            enforcement_level="recommended",
            related_principles=["error_handling"],
        )

    def _create_composition_principle(self) -> DesignPrinciple:
        """Create composition over inheritance principle."""
        return DesignPrinciple(
            name="Composition Over Inheritance",
            category=PrincipleCategory.MAINTAINABILITY,
            description="Prefer composition to inheritance",
            rationale="More flexible and maintainable than inheritance",
            examples=[
                "Use dependency injection",
                "Compose objects from smaller parts",
                "Favor interfaces over concrete classes",
            ],
            anti_examples=[
                "Deep inheritance hierarchies",
                "Inheritance for code reuse only",
                "Complex inheritance chains",
            ],
            enforcement_level="recommended",
            related_principles=["sr"],
        )

    def get_principle(self, name: str) -> DesignPrinciple | None:
        """Get a specific principle by name."""
        return self.principles.get(name)

    def get_principles_by_category(self, category: PrincipleCategory) -> list[DesignPrinciple]:
        """Get all principles in a category."""
        return [p for p in self.principles.values() if p.category == category]

    def get_required_principles(self) -> list[DesignPrinciple]:
        """Get all required principles."""
        return [p for p in self.principles.values() if p.enforcement_level == "required"]


__all__ = ["KnowledgeBasePrinciples"]


