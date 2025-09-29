"""
Shared Knowledge Base - V2 Compliant Wrapper (≤100 lines)
Centralized design principles and best practices.
Contains the collective wisdom for maintaining project consistency.
"""

from typing import Any

from .knowledge_base_core import (
    AntiPattern,
    CodePattern,
    DesignPrinciple,
    KnowledgeBaseCore,
    PrincipleCategory,
)
from .knowledge_base_manager import KnowledgeBaseManager
from .knowledge_base_retriever import KnowledgeBaseRetriever


class SharedKnowledgeBase:
    """
    V2 Compliant wrapper for AutoDream.OS knowledge base system.

    Provides backward compatibility while delegating to modular components.
    """

    def __init__(self):
        """Initialize the knowledge base with modular components."""
        self.core = KnowledgeBaseCore()
        self.manager = KnowledgeBaseManager(self.core)
        self.retriever = KnowledgeBaseRetriever(self.core)

    # Delegate to core for basic operations
    @property
    def design_principles(self):
        return self.core.design_principles

    @property
    def code_patterns(self):
        return self.core.code_patterns

    @property
    def anti_patterns(self):
        return self.core.anti_patterns

    @property
    def project_guidelines(self):
        return self.core.project_guidelines

    def get_principle(self, name: str) -> DesignPrinciple:
        """Get a specific design principle."""
        return self.core.get_principle(name)

    def get_principles_by_category(self, category: PrincipleCategory) -> list[DesignPrinciple]:
        """Get all principles in a specific category."""
        return self.core.get_principles_by_category(category)

    def get_required_principles(self) -> list[DesignPrinciple]:
        """Get all required principles."""
        return self.core.get_required_principles()

    def get_code_pattern(self, name: str) -> CodePattern:
        """Get a specific code pattern."""
        return self.core.get_code_pattern(name)

    def get_simple_patterns(self, max_complexity: int = 3) -> list[CodePattern]:
        """Get code patterns with complexity below threshold."""
        return self.core.get_simple_patterns(max_complexity)

    def get_anti_pattern(self, name: str) -> AntiPattern:
        """Get a specific anti-pattern."""
        return self.core.get_anti_pattern(name)

    def get_critical_anti_patterns(self) -> list[AntiPattern]:
        """Get all critical anti-patterns."""
        return self.core.get_critical_anti_patterns()

    def validate_code_against_principles(self, code_snippet: str) -> dict[str, list[str]]:
        """Validate code against design principles."""
        return self.core.validate_code_against_principles(code_snippet)

    def get_guideline(self, guideline_type: str) -> Any:
        """Get specific project guidelines."""
        return self.core.get_guideline(guideline_type)

    def get_all_guidelines(self) -> dict[str, Any]:
        """Get all project guidelines."""
        return self.core.get_all_guidelines()

    def suggest_simplification(self, complex_code_description: str) -> list[str]:
        """Suggest simplifications based on principles."""
        return self.core.suggest_simplification(complex_code_description)


# Global knowledge base instance
knowledge_base = SharedKnowledgeBase()


def get_knowledge_base() -> SharedKnowledgeBase:
    """Get the global knowledge base instance."""
    return knowledge_base


def get_principle(name: str) -> DesignPrinciple:
    """Get a design principle by name."""
    return knowledge_base.get_principle(name)


def get_required_principles() -> list[DesignPrinciple]:
    """Get all required design principles."""
    return knowledge_base.get_required_principles()


def validate_code(code_snippet: str) -> dict[str, list[str]]:
    """Validate code against design principles."""
    return knowledge_base.validate_code_against_principles(code_snippet)


def suggest_simplification(description: str) -> list[str]:
    """Get simplification suggestions."""
    return knowledge_base.suggest_simplification(description)
