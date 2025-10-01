"""
Knowledge Base Data Factories
==============================

Data factory methods for knowledge base principles, patterns, and anti-patterns.
Modular split from knowledge_base_core.py for V2 compliance.

Author: Agent-7 (Web Development Expert)
License: MIT
V2 Compliance: ≤400 lines
"""

from .knowledge_base_core import AntiPattern, CodePattern, DesignPrinciple, PrincipleCategory


def create_kiss_principle() -> DesignPrinciple:
    """Create KISS principle."""
    return DesignPrinciple(
        name="Keep It Simple, Stupid",
        category=PrincipleCategory.SIMPLICITY,
        description="Prefer simple solutions over complex ones",
        rationale="Simple code is easier to understand, debug, and maintain.",
        examples=[
            "Use built-in data types",
            "Prefer functions over classes",
            "Choose clarity over cleverness",
        ],
        anti_examples=["Complex inheritance hierarchies", "Over-engineering simple operations"],
        enforcement_level="required",
        related_principles=["YAGNI", "Single Responsibility"],
    )


def create_yagni_principle() -> DesignPrinciple:
    """Create YAGNI principle."""
    return DesignPrinciple(
        name="You Aren't Gonna Need It",
        category=PrincipleCategory.SIMPLICITY,
        description="Don't build features until you actually need them",
        rationale="Building unused features wastes time and adds complexity.",
        examples=["Start with simple data structures", "Build specific solutions first"],
        anti_examples=[
            "Building 'future-proof' interfaces",
            "Adding configuration 'just in case'",
        ],
        enforcement_level="required",
        related_principles=["KISS", "Single Responsibility"],
    )


def create_sr_principle() -> DesignPrinciple:
    """Create Single Responsibility principle."""
    return DesignPrinciple(
        name="Single Responsibility Principle",
        category=PrincipleCategory.MAINTAINABILITY,
        description="Each component should have one clear purpose",
        rationale="Components with single responsibilities are easier to understand, test, and modify.",
        examples=[
            "Separate data access from business logic",
            "One function, one clear purpose",
        ],
        anti_examples=[
            "God classes that handle everything",
            "Functions that do multiple unrelated things",
        ],
        enforcement_level="required",
        related_principles=["KISS", "Separation of Concerns"],
    )


def create_error_handling_principle() -> DesignPrinciple:
    """Create Error Handling principle."""
    return DesignPrinciple(
        name="Consistent Error Handling",
        category=PrincipleCategory.MAINTAINABILITY,
        description="Handle errors consistently throughout the system",
        rationale="Consistent error handling makes debugging easier and improves user experience.",
        examples=["Use specific exception types", "Provide meaningful error messages"],
        anti_examples=["Bare except clauses", "Silent failures without logging"],
        enforcement_level="required",
        related_principles=["Fail Fast", "Defensive Programming"],
    )


def create_fail_fast_principle() -> DesignPrinciple:
    """Create Fail Fast principle."""
    return DesignPrinciple(
        name="Fail Fast Principle",
        category=PrincipleCategory.MAINTAINABILITY,
        description="Detect and report errors as early as possible",
        rationale="Early error detection makes debugging easier and prevents cascading failures.",
        examples=["Validate inputs at system boundaries", "Use type hints and runtime checks"],
        anti_examples=["Allowing invalid data to propagate", "Silent type conversions"],
        enforcement_level="recommended",
        related_principles=["Error Handling", "Defensive Programming"],
    )


def create_composition_principle() -> DesignPrinciple:
    """Create Composition over Inheritance principle."""
    return DesignPrinciple(
        name="Composition over Inheritance",
        category=PrincipleCategory.MAINTAINABILITY,
        description="Prefer composition to inheritance for code reuse",
        rationale="Composition is more flexible and less brittle than inheritance.",
        examples=["Use dependency injection", "Compose behavior from multiple sources"],
        anti_examples=["Deep inheritance hierarchies", "Complex multiple inheritance"],
        enforcement_level="recommended",
        related_principles=["YAGNI", "Single Responsibility"],
    )


def create_simple_function_pattern() -> CodePattern:
    """Create Simple Function pattern."""
    return CodePattern(
        name="Simple Function",
        pattern_type="behavioral",
        description="Use simple functions for straightforward operations",
        code_example="def calculate_total(items): return sum(item.price for item in items)",
        when_to_use=["Single operation", "No shared state", "Simple business logic"],
        when_not_to_use=[
            "Complex state management",
            "Multiple operations",
            "Need polymorphism",
        ],
        complexity_score=1,
    )


def create_data_class_pattern() -> CodePattern:
    """Create Data Class pattern."""
    return CodePattern(
        name="Data Class",
        pattern_type="structural",
        description="Use dataclasses for simple data containers",
        code_example="@dataclass\nclass User:\n    id: int\n    name: str",
        when_to_use=["Simple data containers", "Immutable data", "API models"],
        when_not_to_use=["Complex business logic", "Mutable state", "Need inheritance"],
        complexity_score=2,
    )


def create_repository_pattern() -> CodePattern:
    """Create Repository pattern."""
    return CodePattern(
        name="Repository Pattern",
        pattern_type="structural",
        description="Abstract data access behind simple interfaces",
        code_example="class UserRepository:\n    def get_user(self, id): pass",
        when_to_use=["Abstract data access", "Multiple data sources", "Testing"],
        when_not_to_use=["Simple CRUD", "No abstraction needed", "Over-engineering"],
        complexity_score=4,
    )


def create_service_layer_pattern() -> CodePattern:
    """Create Service Layer pattern."""
    return CodePattern(
        name="Service Layer",
        pattern_type="behavioral",
        description="Encapsulate business logic in service classes",
        code_example="class UserService:\n    def create_user(self, name, email): pass",
        when_to_use=["Complex business logic", "Multiple data sources", "Transactions"],
        when_not_to_use=["Simple CRUD", "No business logic", "Over-engineering"],
        complexity_score=3,
    )


def create_god_class_anti_pattern() -> AntiPattern:
    """Create God Class anti-pattern."""
    return AntiPattern(
        name="God Class",
        description="A class that knows too much or does too much",
        why_bad="Violates single responsibility, hard to test and maintain",
        common_manifestations=[
            "Classes with 20+ methods",
            "Multiple concerns",
            "Too many dependencies",
        ],
        better_alternatives=["Break into smaller classes", "Use composition", "Apply SRP"],
        severity="major",
    )


def create_premature_optimization_anti_pattern() -> AntiPattern:
    """Create Premature Optimization anti-pattern."""
    return AntiPattern(
        name="Premature Optimization",
        description="Optimizing code before understanding performance requirements",
        why_bad="Adds complexity without proven benefit, wastes development time",
        common_manifestations=[
            "Complex algorithms for small data",
            "Caching everything",
            "Micro-optimizations",
        ],
        better_alternatives=["Measure first", "Start simple", "Profile before optimizing"],
        severity="minor",
    )


def create_bare_except_anti_pattern() -> AntiPattern:
    """Create Bare Except anti-pattern."""
    return AntiPattern(
        name="Bare Except Clauses",
        description="Using 'except:' without specifying exception types",
        why_bad="Hides errors and makes debugging difficult",
        common_manifestations=["except: pass", "except: continue", "except: return None"],
        better_alternatives=["Use specific exception types", "Log errors with context"],
        severity="critical",
    )


def create_stringly_typed_anti_pattern() -> AntiPattern:
    """Create Stringly Typed anti-pattern."""
    return AntiPattern(
        name="Stringly Typed Code",
        description="Using strings where enums or types would be better",
        why_bad="Prone to typos, no IDE support, runtime errors",
        common_manifestations=["if status == 'active'", "return 'success'", "Magic strings"],
        better_alternatives=["Use enums", "Use type hints", "Use constants"],
        severity="major",
    )


def create_copy_paste_anti_pattern() -> AntiPattern:
    """Create Copy-Paste Programming anti-pattern."""
    return AntiPattern(
        name="Copy-Paste Programming",
        description="Duplicating code instead of extracting common functionality",
        why_bad="Creates maintenance burden, inconsistent behavior",
        common_manifestations=[
            "Copying functions",
            "Duplicating validation",
            "Repeating error handling",
        ],
        better_alternatives=["Extract common functionality", "Use inheritance", "Apply DRY"],
        severity="major",
    )


def get_project_guidelines() -> dict:
    """Load project-specific guidelines."""
    return {
        "file_limits": {
            "max_file_lines": 300,
            "max_class_lines": 100,
            "max_function_lines": 30,
        },
        "naming_conventions": {
            "functions": "snake_case",
            "classes": "PascalCase",
            "constants": "UPPER_SNAKE_CASE",
        },
        "import_guidelines": {
            "standard_library_first": True,
            "third_party_second": True,
            "local_imports_last": True,
        },
        "documentation_requirements": {
            "public_functions": "Must have docstrings",
            "classes": "Must have class docstrings",
        },
        "testing_requirements": {
            "unit_tests": "Required for all public functions",
            "coverage_threshold": 85,
        },
        "error_handling_standards": {
            "use_specific_exceptions": True,
            "log_errors_with_context": True,
        },
    }

