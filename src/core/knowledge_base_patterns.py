#!/usr/bin/env python3
"""
Knowledge Base Patterns - Code Patterns Management
==================================================

Code patterns management for knowledge base system.
Handles creation and management of code patterns and anti-patterns.

V2 Compliance: ≤400 lines, focused patterns management module
Author: Agent-6 (Quality Assurance Specialist)
"""

from .knowledge_base_models import AntiPattern, CodePattern


class KnowledgeBasePatterns:
    """
    Code patterns management for knowledge base.

    Handles creation and management of code patterns and anti-patterns.
    """

    def __init__(self):
        """Initialize patterns manager."""
        self.patterns: dict[str, CodePattern] = {}
        self.anti_patterns: dict[str, AntiPattern] = {}
        self._load_code_patterns()
        self._load_anti_patterns()

    def _load_code_patterns(self) -> None:
        """Load all code patterns."""
        self.patterns = {
            "simple_function": self._create_simple_function_pattern(),
            "data_class": self._create_data_class_pattern(),
            "repository": self._create_repository_pattern(),
            "service_layer": self._create_service_layer_pattern(),
        }

    def _create_simple_function_pattern(self) -> CodePattern:
        """Create simple function pattern."""
        return CodePattern(
            name="Simple Function",
            pattern_type="behavioral",
            description="Small, focused functions with single responsibility",
            code_example="""
def calculate_total(items: list[Item]) -> float:
    \"\"\"Calculate total price of items.\"\"\"
    return sum(item.price for item in items)
            """,
            when_to_use=["Single responsibility", "Clear input/output", "Easy to test"],
            when_not_to_use=[
                "Multiple responsibilities",
                "Complex side effects",
                "Too many parameters",
            ],
            complexity_score=1,
        )

    def _create_data_class_pattern(self) -> CodePattern:
        """Create data class pattern."""
        return CodePattern(
            name="Data Class",
            pattern_type="structural",
            description="Simple data containers with minimal logic",
            code_example="""
@dataclass
class User:
    name: str
    email: str
    created_at: datetime
            """,
            when_to_use=["Data containers", "Simple structures", "Immutable data"],
            when_not_to_use=["Complex business logic", "Heavy computations", "State management"],
            complexity_score=1,
        )

    def _create_repository_pattern(self) -> CodePattern:
        """Create repository pattern."""
        return CodePattern(
            name="Repository Pattern",
            pattern_type="structural",
            description="Abstracts data access logic",
            code_example="""
class UserRepository:
    def get_user(self, user_id: str) -> User | None:
        # Data access logic
        pass
            """,
            when_to_use=["Data access abstraction", "Testing with mocks", "Multiple data sources"],
            when_not_to_use=["Simple CRUD operations", "Single data source", "Over-abstraction"],
            complexity_score=3,
        )

    def _create_service_layer_pattern(self) -> CodePattern:
        """Create service layer pattern."""
        return CodePattern(
            name="Service Layer",
            pattern_type="structural",
            description="Business logic layer between controllers and repositories",
            code_example="""
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_data: dict) -> User:
        # Business logic
        pass
            """,
            when_to_use=[
                "Complex business logic",
                "Multiple data sources",
                "Transaction management",
            ],
            when_not_to_use=["Simple CRUD operations", "Thin business logic", "Over-abstraction"],
            complexity_score=4,
        )

    def _load_anti_patterns(self) -> None:
        """Load all anti-patterns."""
        self.anti_patterns = {
            "god_class": self._create_god_class_anti_pattern(),
            "premature_optimization": self._create_premature_optimization_anti_pattern(),
            "bare_except": self._create_bare_except_anti_pattern(),
            "stringly_typed": self._create_stringly_typed_anti_pattern(),
            "copy_paste": self._create_copy_paste_anti_pattern(),
        }

    def _create_god_class_anti_pattern(self) -> AntiPattern:
        """Create god class anti-pattern."""
        return AntiPattern(
            name="God Class",
            description="A class that knows too much or does too much",
            why_bad="Violates single responsibility principle, hard to maintain",
            examples=[
                "UserManager class handling users, emails, files, and database",
                "Single class with 20+ methods",
                "Class with multiple unrelated responsibilities",
            ],
            how_to_fix=[
                "Split into smaller, focused classes",
                "Apply single responsibility principle",
                "Use composition over inheritance",
            ],
            severity="critical",
        )

    def _create_premature_optimization_anti_pattern(self) -> AntiPattern:
        """Create premature optimization anti-pattern."""
        return AntiPattern(
            name="Premature Optimization",
            description="Optimizing code before measuring performance",
            why_bad="Wastes time, adds complexity, may not solve real problems",
            examples=[
                "Using complex algorithms for small datasets",
                "Micro-optimizations without profiling",
                "Optimizing before identifying bottlenecks",
            ],
            how_to_fix=[
                "Measure first, optimize second",
                "Profile to find real bottlenecks",
                "Keep code simple until optimization is needed",
            ],
            severity="high",
        )

    def _create_bare_except_anti_pattern(self) -> AntiPattern:
        """Create bare except anti-pattern."""
        return AntiPattern(
            name="Bare Except",
            description="Using bare except clauses without specific exception types",
            why_bad="Catches all exceptions, including system exits and keyboard interrupts",
            examples=[
                "try: ... except: pass",
                "try: ... except Exception: ...",
                "Catching all exceptions without handling",
            ],
            how_to_fix=[
                "Catch specific exception types",
                "Handle exceptions appropriately",
                "Use finally for cleanup",
            ],
            severity="critical",
        )

    def _create_stringly_typed_anti_pattern(self) -> AntiPattern:
        """Create stringly typed anti-pattern."""
        return AntiPattern(
            name="Stringly Typed",
            description="Using strings instead of proper types",
            why_bad="No type safety, runtime errors, hard to refactor",
            examples=[
                "Using strings for status codes",
                "String-based configuration",
                "Magic strings throughout code",
            ],
            how_to_fix=["Use enums for fixed values", "Create proper data types", "Use type hints"],
            severity="medium",
        )

    def _create_copy_paste_anti_pattern(self) -> AntiPattern:
        """Create copy-paste anti-pattern."""
        return AntiPattern(
            name="Copy-Paste Programming",
            description="Copying code instead of creating reusable components",
            why_bad="Code duplication, maintenance nightmare, inconsistent behavior",
            examples=[
                "Duplicated validation logic",
                "Similar functions with slight differences",
                "Copy-pasted error handling",
            ],
            how_to_fix=[
                "Extract common functionality",
                "Create reusable functions",
                "Use inheritance or composition",
            ],
            severity="high",
        )

    def get_code_pattern(self, name: str) -> CodePattern | None:
        """Get a specific code pattern by name."""
        return self.patterns.get(name)

    def get_simple_patterns(self) -> list[CodePattern]:
        """Get all simple patterns (complexity score ≤ 2)."""
        return [p for p in self.patterns.values() if p.complexity_score <= 2]

    def get_anti_pattern(self, name: str) -> AntiPattern | None:
        """Get a specific anti-pattern by name."""
        return self.anti_patterns.get(name)

    def get_critical_anti_patterns(self) -> list[AntiPattern]:
        """Get all critical anti-patterns."""
        return [ap for ap in self.anti_patterns.values() if ap.severity == "critical"]


__all__ = ["KnowledgeBasePatterns"]
