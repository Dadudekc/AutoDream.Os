"""
Knowledge Base Core Module - V2 Compliant (≤300 lines)
Core data structures and basic operations for the shared knowledge base.
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


class KnowledgeBaseCore:
    """
    Core knowledge base operations for AutoDream.OS design principles.
    
    Handles basic CRUD operations and data validation for design principles,
    code patterns, and anti-patterns.
    """
    
    def __init__(self):
        self.design_principles = self._load_design_principles()
        self.code_patterns = self._load_code_patterns()
        self.anti_patterns = self._load_anti_patterns()
        self.project_guidelines = self._load_project_guidelines()
    
    def _load_design_principles(self) -> Dict[str, DesignPrinciple]:
        """Load core design principles."""
        return {
            "KISS": self._create_kiss_principle(),
            "YAGNI": self._create_yagni_principle(),
            "Single Responsibility": self._create_sr_principle(),
            "Error Handling": self._create_error_handling_principle(),
            "Fail Fast": self._create_fail_fast_principle(),
            "Composition over Inheritance": self._create_composition_principle()
        }
    
    def _create_kiss_principle(self) -> DesignPrinciple:
        """Create KISS principle."""
        return DesignPrinciple(
            name="Keep It Simple, Stupid",
            category=PrincipleCategory.SIMPLICITY,
            description="Prefer simple solutions over complex ones",
            rationale="Simple code is easier to understand, debug, and maintain.",
            examples=["Use built-in data types", "Prefer functions over classes", "Choose clarity over cleverness"],
            anti_examples=["Complex inheritance hierarchies", "Over-engineering simple operations"],
            enforcement_level="required",
            related_principles=["YAGNI", "Single Responsibility"]
        )
    
    def _create_yagni_principle(self) -> DesignPrinciple:
        """Create YAGNI principle."""
        return DesignPrinciple(
            name="You Aren't Gonna Need It",
            category=PrincipleCategory.SIMPLICITY,
            description="Don't build features until you actually need them",
            rationale="Building unused features wastes time and adds complexity.",
            examples=["Start with simple data structures", "Build specific solutions first"],
            anti_examples=["Building 'future-proof' interfaces", "Adding configuration 'just in case'"],
            enforcement_level="required",
            related_principles=["KISS", "Single Responsibility"]
        )
    
    def _create_sr_principle(self) -> DesignPrinciple:
        """Create Single Responsibility principle."""
        return DesignPrinciple(
            name="Single Responsibility Principle",
            category=PrincipleCategory.MAINTAINABILITY,
            description="Each component should have one clear purpose",
            rationale="Components with single responsibilities are easier to understand, test, and modify.",
            examples=["Separate data access from business logic", "One function, one clear purpose"],
            anti_examples=["God classes that handle everything", "Functions that do multiple unrelated things"],
            enforcement_level="required",
            related_principles=["KISS", "Separation of Concerns"]
        )
    
    def _create_error_handling_principle(self) -> DesignPrinciple:
        """Create Error Handling principle."""
        return DesignPrinciple(
            name="Consistent Error Handling",
            category=PrincipleCategory.MAINTAINABILITY,
            description="Handle errors consistently throughout the system",
            rationale="Consistent error handling makes debugging easier and improves user experience.",
            examples=["Use specific exception types", "Provide meaningful error messages"],
            anti_examples=["Bare except clauses", "Silent failures without logging"],
            enforcement_level="required",
            related_principles=["Fail Fast", "Defensive Programming"]
        )
    
    def _create_fail_fast_principle(self) -> DesignPrinciple:
        """Create Fail Fast principle."""
        return DesignPrinciple(
            name="Fail Fast Principle",
            category=PrincipleCategory.MAINTAINABILITY,
            description="Detect and report errors as early as possible",
            rationale="Early error detection makes debugging easier and prevents cascading failures.",
            examples=["Validate inputs at system boundaries", "Use type hints and runtime checks"],
            anti_examples=["Allowing invalid data to propagate", "Silent type conversions"],
            enforcement_level="recommended",
            related_principles=["Error Handling", "Defensive Programming"]
        )
    
    def _create_composition_principle(self) -> DesignPrinciple:
        """Create Composition over Inheritance principle."""
        return DesignPrinciple(
            name="Composition over Inheritance",
            category=PrincipleCategory.MAINTAINABILITY,
            description="Prefer composition to inheritance for code reuse",
            rationale="Composition is more flexible and less brittle than inheritance.",
            examples=["Use dependency injection", "Compose behavior from multiple sources"],
            anti_examples=["Deep inheritance hierarchies", "Complex multiple inheritance"],
            enforcement_level="recommended",
            related_principles=["YAGNI", "Single Responsibility"]
        )
    
    def _load_code_patterns(self) -> Dict[str, CodePattern]:
        """Load preferred code patterns."""
        return {
            "Simple Function": self._create_simple_function_pattern(),
            "Data Class": self._create_data_class_pattern(),
            "Repository Pattern": self._create_repository_pattern(),
            "Service Layer": self._create_service_layer_pattern()
        }
    
    def _create_simple_function_pattern(self) -> CodePattern:
        """Create Simple Function pattern."""
        return CodePattern(
            name="Simple Function",
            pattern_type="behavioral",
            description="Use simple functions for straightforward operations",
            code_example="def calculate_total(items): return sum(item.price for item in items)",
            when_to_use=["Single operation", "No shared state", "Simple business logic"],
            when_not_to_use=["Complex state management", "Multiple operations", "Need polymorphism"],
            complexity_score=1
        )
    
    def _create_data_class_pattern(self) -> CodePattern:
        """Create Data Class pattern."""
        return CodePattern(
            name="Data Class",
            pattern_type="structural",
            description="Use dataclasses for simple data containers",
            code_example="@dataclass\nclass User:\n    id: int\n    name: str",
            when_to_use=["Simple data containers", "Immutable data", "API models"],
            when_not_to_use=["Complex business logic", "Mutable state", "Need inheritance"],
            complexity_score=2
        )
    
    def _create_repository_pattern(self) -> CodePattern:
        """Create Repository pattern."""
        return CodePattern(
            name="Repository Pattern",
            pattern_type="structural",
            description="Abstract data access behind simple interfaces",
            code_example="class UserRepository:\n    def get_user(self, id): pass",
            when_to_use=["Abstract data access", "Multiple data sources", "Testing"],
            when_not_to_use=["Simple CRUD", "No abstraction needed", "Over-engineering"],
            complexity_score=4
        )
    
    def _create_service_layer_pattern(self) -> CodePattern:
        """Create Service Layer pattern."""
        return CodePattern(
            name="Service Layer",
            pattern_type="behavioral",
            description="Encapsulate business logic in service classes",
            code_example="class UserService:\n    def create_user(self, name, email): pass",
            when_to_use=["Complex business logic", "Multiple data sources", "Transactions"],
            when_not_to_use=["Simple CRUD", "No business logic", "Over-engineering"],
            complexity_score=3
        )
    
    def _load_anti_patterns(self) -> Dict[str, AntiPattern]:
        """Load code anti-patterns to avoid."""
        return {
            "God Class": self._create_god_class_anti_pattern(),
            "Premature Optimization": self._create_premature_optimization_anti_pattern(),
            "Bare Except": self._create_bare_except_anti_pattern(),
            "Stringly Typed": self._create_stringly_typed_anti_pattern(),
            "Copy-Paste Programming": self._create_copy_paste_anti_pattern()
        }
    
    def _create_god_class_anti_pattern(self) -> AntiPattern:
        """Create God Class anti-pattern."""
        return AntiPattern(
            name="God Class",
            description="A class that knows too much or does too much",
            why_bad="Violates single responsibility, hard to test and maintain",
            common_manifestations=["Classes with 20+ methods", "Multiple concerns", "Too many dependencies"],
            better_alternatives=["Break into smaller classes", "Use composition", "Apply SRP"],
            severity="major"
        )
    
    def _create_premature_optimization_anti_pattern(self) -> AntiPattern:
        """Create Premature Optimization anti-pattern."""
        return AntiPattern(
            name="Premature Optimization",
            description="Optimizing code before understanding performance requirements",
            why_bad="Adds complexity without proven benefit, wastes development time",
            common_manifestations=["Complex algorithms for small data", "Caching everything", "Micro-optimizations"],
            better_alternatives=["Measure first", "Start simple", "Profile before optimizing"],
            severity="minor"
        )
    
    def _create_bare_except_anti_pattern(self) -> AntiPattern:
        """Create Bare Except anti-pattern."""
        return AntiPattern(
            name="Bare Except Clauses",
            description="Using 'except:' without specifying exception types",
            why_bad="Hides errors and makes debugging difficult",
            common_manifestations=["except: pass", "except: continue", "except: return None"],
            better_alternatives=["Use specific exception types", "Log errors with context"],
            severity="critical"
        )
    
    def _create_stringly_typed_anti_pattern(self) -> AntiPattern:
        """Create Stringly Typed anti-pattern."""
        return AntiPattern(
            name="Stringly Typed Code",
            description="Using strings where enums or types would be better",
            why_bad="Prone to typos, no IDE support, runtime errors",
            common_manifestations=["if status == 'active'", "return 'success'", "Magic strings"],
            better_alternatives=["Use enums", "Use type hints", "Use constants"],
            severity="major"
        )
    
    def _create_copy_paste_anti_pattern(self) -> AntiPattern:
        """Create Copy-Paste Programming anti-pattern."""
        return AntiPattern(
            name="Copy-Paste Programming",
            description="Duplicating code instead of extracting common functionality",
            why_bad="Creates maintenance burden, inconsistent behavior",
            common_manifestations=["Copying functions", "Duplicating validation", "Repeating error handling"],
            better_alternatives=["Extract common functionality", "Use inheritance", "Apply DRY"],
            severity="major"
        )
    
    def _load_project_guidelines(self) -> Dict[str, Any]:
        """Load project-specific guidelines."""
        return {
            "file_limits": {"max_file_lines": 300, "max_class_lines": 100, "max_function_lines": 30},
            "naming_conventions": {"functions": "snake_case", "classes": "PascalCase", "constants": "UPPER_SNAKE_CASE"},
            "import_guidelines": {"standard_library_first": True, "third_party_second": True, "local_imports_last": True},
            "documentation_requirements": {"public_functions": "Must have docstrings", "classes": "Must have class docstrings"},
            "testing_requirements": {"unit_tests": "Required for all public functions", "coverage_threshold": 85},
            "error_handling_standards": {"use_specific_exceptions": True, "log_errors_with_context": True}
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