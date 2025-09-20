"""
Shared Knowledge Base - Centralized design principles and best practices.
Contains the collective wisdom for maintaining project consistency.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class PrincipleCategory(Enum):
    """Categories of design principles."""
    SIMPLICITY = "simplicity"
    MAINTAINABILITY = "maintainability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    TESTING = "testing"
    DOCUMENTATION = "documentation"


@dataclass
class DesignPrinciple:
    """Represents a design principle with examples and guidelines."""
    name: str
    category: PrincipleCategory
    description: str
    rationale: str
    examples: List[str]
    anti_examples: List[str]
    enforcement_level: str  # required, recommended, optional
    related_principles: List[str] = None
    
    def __post_init__(self):
        if self.related_principles is None:
            self.related_principles = []


@dataclass
class CodePattern:
    """Represents a preferred code pattern."""
    name: str
    pattern_type: str  # structural, behavioral, creational
    description: str
    code_example: str
    when_to_use: List[str]
    when_not_to_use: List[str]
    complexity_score: int  # 1-10, where 1 is simplest


@dataclass
class AntiPattern:
    """Represents a code anti-pattern to avoid."""
    name: str
    description: str
    why_bad: str
    common_manifestations: List[str]
    better_alternatives: List[str]
    severity: str  # critical, major, minor


class SharedKnowledgeBase:
    """
    Centralized knowledge base for AutoDream.OS design principles.
    
    This contains the collective wisdom that guides all agents in making
    consistent design decisions and maintaining code quality.
    """
    
    def __init__(self):
        self.design_principles = self._load_design_principles()
        self.code_patterns = self._load_code_patterns()
        self.anti_patterns = self._load_anti_patterns()
        self.project_guidelines = self._load_project_guidelines()
    
    def _load_design_principles(self) -> Dict[str, DesignPrinciple]:
        """Load core design principles."""
        return {
            "KISS": DesignPrinciple(
                name="Keep It Simple, Stupid",
                category=PrincipleCategory.SIMPLICITY,
                description="Prefer simple solutions over complex ones",
                rationale="Simple code is easier to understand, debug, and maintain. Complexity is the enemy of reliability.",
                examples=[
                    "Use built-in data types instead of custom wrappers",
                    "Prefer functions over classes for simple operations",
                    "Use if/else instead of complex match statements when appropriate",
                    "Choose clarity over cleverness"
                ],
                anti_examples=[
                    "Creating complex inheritance hierarchies for simple data",
                    "Using design patterns where simple functions would suffice",
                    "Over-engineering simple CRUD operations",
                    "Premature optimization that adds complexity"
                ],
                enforcement_level="required",
                related_principles=["YAGNI", "Single Responsibility"]
            ),
            
            "YAGNI": DesignPrinciple(
                name="You Aren't Gonna Need It",
                category=PrincipleCategory.SIMPLICITY,
                description="Don't build features until you actually need them",
                rationale="Building unused features wastes time and adds complexity. Start simple, add complexity when requirements demand it.",
                examples=[
                    "Start with simple data structures, add complexity when needed",
                    "Build specific solutions first, generalize later if needed",
                    "Avoid speculative features and abstractions",
                    "Focus on current requirements, not hypothetical future needs"
                ],
                anti_examples=[
                    "Building 'future-proof' interfaces before understanding requirements",
                    "Creating generic solutions for specific problems",
                    "Adding configuration options 'just in case'",
                    "Building extensible frameworks for simple use cases"
                ],
                enforcement_level="required",
                related_principles=["KISS", "Single Responsibility"]
            ),
            
            "Single Responsibility": DesignPrinciple(
                name="Single Responsibility Principle",
                category=PrincipleCategory.MAINTAINABILITY,
                description="Each component should have one clear purpose",
                rationale="Components with single responsibilities are easier to understand, test, and modify.",
                examples=[
                    "Separate data access from business logic",
                    "Keep UI components focused on presentation",
                    "Isolate external service integrations",
                    "One function, one clear purpose"
                ],
                anti_examples=[
                    "God classes that handle everything",
                    "Functions that do multiple unrelated things",
                    "Modules mixing different abstraction levels",
                    "Controllers that contain business logic"
                ],
                enforcement_level="required",
                related_principles=["KISS", "Separation of Concerns"]
            ),
            
            "Error Handling": DesignPrinciple(
                name="Consistent Error Handling",
                category=PrincipleCategory.MAINTAINABILITY,
                description="Handle errors consistently throughout the system",
                rationale="Consistent error handling makes debugging easier and improves user experience.",
                examples=[
                    "Use specific exception types instead of generic ones",
                    "Provide meaningful error messages",
                    "Log errors with sufficient context",
                    "Handle errors at appropriate abstraction levels"
                ],
                anti_examples=[
                    "Bare except clauses that swallow all errors",
                    "Silent failures without logging",
                    "Generic 'Something went wrong' messages",
                    "Ignoring errors and continuing execution"
                ],
                enforcement_level="required",
                related_principles=["Fail Fast", "Defensive Programming"]
            ),
            
            "Fail Fast": DesignPrinciple(
                name="Fail Fast Principle",
                category=PrincipleCategory.MAINTAINABILITY,
                description="Detect and report errors as early as possible",
                rationale="Early error detection makes debugging easier and prevents cascading failures.",
                examples=[
                    "Validate inputs at system boundaries",
                    "Use type hints and runtime checks",
                    "Assert invariants in critical code paths",
                    "Throw exceptions for invalid states"
                ],
                anti_examples=[
                    "Allowing invalid data to propagate through the system",
                    "Silent type conversions that hide bugs",
                    "Continuing execution with invalid state",
                    "Delaying error detection until much later"
                ],
                enforcement_level="recommended",
                related_principles=["Error Handling", "Defensive Programming"]
            ),
            
            "Composition over Inheritance": DesignPrinciple(
                name="Composition over Inheritance",
                category=PrincipleCategory.MAINTAINABILITY,
                description="Prefer composition to inheritance for code reuse",
                rationale="Composition is more flexible and less brittle than inheritance.",
                examples=[
                    "Use dependency injection instead of inheritance",
                    "Compose behavior from multiple sources",
                    "Prefer interfaces over abstract base classes",
                    "Use delegation instead of inheritance"
                ],
                anti_examples=[
                    "Deep inheritance hierarchies",
                    "Inheriting from concrete classes",
                    "Using inheritance for code reuse alone",
                    "Complex multiple inheritance scenarios"
                ],
                enforcement_level="recommended",
                related_principles=["YAGNI", "Single Responsibility"]
            )
        }
    
    def _load_code_patterns(self) -> Dict[str, CodePattern]:
        """Load preferred code patterns."""
        return {
            "Simple Function": CodePattern(
                name="Simple Function",
                pattern_type="behavioral",
                description="Use simple functions for straightforward operations",
                code_example="""
def calculate_total(items: List[Item]) -> float:
    return sum(item.price for item in items)
""",
                when_to_use=[
                    "Single operation with clear input/output",
                    "No shared state required",
                    "Simple business logic"
                ],
                when_not_to_use=[
                    "Complex state management needed",
                    "Multiple related operations",
                    "Need for polymorphism"
                ],
                complexity_score=1
            ),
            
            "Data Class": CodePattern(
                name="Data Class",
                pattern_type="structural",
                description="Use dataclasses for simple data containers",
                code_example="""
@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime
""",
                when_to_use=[
                    "Simple data containers",
                    "Immutable data structures",
                    "API response models"
                ],
                when_not_to_use=[
                    "Complex business logic needed",
                    "Mutable state with complex operations",
                    "Need for inheritance"
                ],
                complexity_score=2
            ),
            
            "Repository Pattern": CodePattern(
                name="Repository Pattern",
                pattern_type="structural",
                description="Abstract data access behind simple interfaces",
                code_example="""
class UserRepository:
    def get_user(self, user_id: int) -> Optional[User]:
        # Implementation details hidden
        pass
    
    def save_user(self, user: User) -> None:
        # Implementation details hidden
        pass
""",
                when_to_use=[
                    "Need to abstract data access",
                    "Multiple data sources",
                    "Testing with mock data"
                ],
                when_not_to_use=[
                    "Simple CRUD with single data source",
                    "No need for abstraction",
                    "Over-engineering simple operations"
                ],
                complexity_score=4
            ),
            
            "Service Layer": CodePattern(
                name="Service Layer",
                pattern_type="behavioral",
                description="Encapsulate business logic in service classes",
                code_example="""
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create_user(self, name: str, email: str) -> User:
        # Business logic here
        if not email or '@' not in email:
            raise ValueError("Invalid email")
        return self.user_repo.save_user(User(name=name, email=email))
""",
                when_to_use=[
                    "Complex business logic",
                    "Multiple data sources involved",
                    "Need for transaction management"
                ],
                when_not_to_use=[
                    "Simple CRUD operations",
                    "No business logic",
                    "Over-engineering simple operations"
                ],
                complexity_score=3
            )
        }
    
    def _load_anti_patterns(self) -> Dict[str, AntiPattern]:
        """Load code anti-patterns to avoid."""
        return {
            "God Class": AntiPattern(
                name="God Class",
                description="A class that knows too much or does too much",
                why_bad="Violates single responsibility, hard to test and maintain",
                common_manifestations=[
                    "Classes with 20+ methods",
                    "Classes that handle multiple concerns",
                    "Classes with too many dependencies",
                    "Classes that are hard to name concisely"
                ],
                better_alternatives=[
                    "Break into smaller, focused classes",
                    "Use composition instead of inheritance",
                    "Extract related functionality into separate classes",
                    "Apply single responsibility principle"
                ],
                severity="major"
            ),
            
            "Premature Optimization": AntiPattern(
                name="Premature Optimization",
                description="Optimizing code before understanding performance requirements",
                why_bad="Adds complexity without proven benefit, wastes development time",
                common_manifestations=[
                    "Using complex algorithms for small datasets",
                    "Caching everything without measuring need",
                    "Micro-optimizations that reduce readability",
                    "Over-engineering for hypothetical scale"
                ],
                better_alternatives=[
                    "Measure first, optimize second",
                    "Start with simple, readable solutions",
                    "Profile before optimizing",
                    "Optimize based on actual bottlenecks"
                ],
                severity="minor"
            ),
            
            "Bare Except": AntiPattern(
                name="Bare Except Clauses",
                description="Using 'except:' without specifying exception types",
                why_bad="Hides errors and makes debugging difficult",
                common_manifestations=[
                    "except: pass",
                    "except: continue",
                    "except: return None",
                    "except: print('error')"
                ],
                better_alternatives=[
                    "Use specific exception types",
                    "Log errors with context",
                    "Handle errors appropriately",
                    "Let unexpected errors bubble up"
                ],
                severity="critical"
            ),
            
            "Stringly Typed": AntiPattern(
                name="Stringly Typed Code",
                description="Using strings where enums or types would be better",
                why_bad="Prone to typos, no IDE support, runtime errors",
                common_manifestations=[
                    "if status == 'active':",
                    "method = 'get' if use_get else 'post'",
                    "return 'success' or 'failure'",
                    "Using strings for configuration keys"
                ],
                better_alternatives=[
                    "Use enums for fixed sets of values",
                    "Use type hints and validation",
                    "Use constants for magic strings",
                    "Use dataclasses for structured data"
                ],
                severity="major"
            ),
            
            "Copy-Paste Programming": AntiPattern(
                name="Copy-Paste Programming",
                description="Duplicating code instead of extracting common functionality",
                why_bad="Creates maintenance burden, inconsistent behavior",
                common_manifestations=[
                    "Copying functions with minor changes",
                    "Duplicating validation logic",
                    "Repeating error handling code",
                    "Similar classes with slight differences"
                ],
                better_alternatives=[
                    "Extract common functionality into functions",
                    "Use inheritance or composition",
                    "Create reusable utility functions",
                    "Apply DRY principle"
                ],
                severity="major"
            )
        }
    
    def _load_project_guidelines(self) -> Dict[str, Any]:
        """Load project-specific guidelines."""
        return {
            "file_limits": {
                "max_file_lines": 300,
                "max_class_lines": 100,
                "max_function_lines": 30,
                "max_nesting_depth": 3,
                "max_function_parameters": 5
            },
            
            "naming_conventions": {
                "functions": "snake_case",
                "classes": "PascalCase",
                "constants": "UPPER_SNAKE_CASE",
                "private_methods": "_snake_case",
                "modules": "snake_case"
            },
            
            "import_guidelines": {
                "standard_library_first": True,
                "third_party_second": True,
                "local_imports_last": True,
                "one_import_per_line": True,
                "group_related_imports": True
            },
            
            "documentation_requirements": {
                "public_functions": "Must have docstrings",
                "classes": "Must have class docstrings",
                "modules": "Should have module docstrings",
                "complex_logic": "Should have inline comments",
                "api_endpoints": "Must be documented"
            },
            
            "testing_requirements": {
                "unit_tests": "Required for all public functions",
                "integration_tests": "Required for external integrations",
                "coverage_threshold": 85,
                "test_naming": "test_<function_name>_<scenario>",
                "mock_external_dependencies": True
            },
            
            "error_handling_standards": {
                "use_specific_exceptions": True,
                "log_errors_with_context": True,
                "provide_meaningful_messages": True,
                "handle_errors_at_appropriate_level": True,
                "fail_fast_on_invalid_input": True
            }
        }
    
    def get_principle(self, name: str) -> DesignPrinciple:
        """Get a specific design principle."""
        return self.design_principles.get(name)
    
    def get_principles_by_category(self, category: PrincipleCategory) -> List[DesignPrinciple]:
        """Get all principles in a specific category."""
        return [
            principle for principle in self.design_principles.values()
            if principle.category == category
        ]
    
    def get_required_principles(self) -> List[DesignPrinciple]:
        """Get all required principles."""
        return [
            principle for principle in self.design_principles.values()
            if principle.enforcement_level == "required"
        ]
    
    def get_code_pattern(self, name: str) -> CodePattern:
        """Get a specific code pattern."""
        return self.code_patterns.get(name)
    
    def get_simple_patterns(self, max_complexity: int = 3) -> List[CodePattern]:
        """Get code patterns with complexity below threshold."""
        return [
            pattern for pattern in self.code_patterns.values()
            if pattern.complexity_score <= max_complexity
        ]
    
    def get_anti_pattern(self, name: str) -> AntiPattern:
        """Get a specific anti-pattern."""
        return self.anti_patterns.get(name)
    
    def get_critical_anti_patterns(self) -> List[AntiPattern]:
        """Get all critical anti-patterns."""
        return [
            anti_pattern for anti_pattern in self.anti_patterns.values()
            if anti_pattern.severity == "critical"
        ]
    
    def validate_code_against_principles(self, code_snippet: str) -> Dict[str, List[str]]:
        """Validate code against design principles."""
        violations = {}
        
        # Check for anti-patterns
        for name, anti_pattern in self.anti_patterns.items():
            found_violations = []
            
            for manifestation in anti_pattern.common_manifestations:
                if manifestation.lower() in code_snippet.lower():
                    found_violations.append(manifestation)
            
            if found_violations:
                violations[f"anti_pattern_{name}"] = found_violations
        
        return violations
    
    def get_guideline(self, guideline_type: str) -> Any:
        """Get specific project guidelines."""
        return self.project_guidelines.get(guideline_type)
    
    def get_all_guidelines(self) -> Dict[str, Any]:
        """Get all project guidelines."""
        return self.project_guidelines.copy()
    
    def suggest_simplification(self, complex_code_description: str) -> List[str]:
        """Suggest simplifications based on principles."""
        suggestions = []
        
        # Simple keyword-based suggestions
        if "class" in complex_code_description.lower():
            suggestions.append("Consider using simple functions instead of classes")
        
        if "inheritance" in complex_code_description.lower():
            suggestions.append("Consider composition over inheritance")
        
        if "pattern" in complex_code_description.lower():
            suggestions.append("Start with simple implementation, add patterns only when needed")
        
        if "framework" in complex_code_description.lower():
            suggestions.append("Consider if built-in Python features would suffice")
        
        # General suggestions
        if not suggestions:
            suggestions.extend([
                "Start with the simplest implementation that works",
                "Use built-in data types when possible",
                "Prefer explicit over implicit",
                "Focus on readability over cleverness"
            ])
        
        return suggestions


# Global knowledge base instance
knowledge_base = SharedKnowledgeBase()


def get_knowledge_base() -> SharedKnowledgeBase:
    """Get the global knowledge base instance."""
    return knowledge_base


def get_principle(name: str) -> DesignPrinciple:
    """Get a design principle by name."""
    return knowledge_base.get_principle(name)


def get_required_principles() -> List[DesignPrinciple]:
    """Get all required design principles."""
    return knowledge_base.get_required_principles()


def validate_code(code_snippet: str) -> Dict[str, List[str]]:
    """Validate code against design principles."""
    return knowledge_base.validate_code_against_principles(code_snippet)


def suggest_simplification(description: str) -> List[str]:
    """Get simplification suggestions."""
    return knowledge_base.suggest_simplification(description)