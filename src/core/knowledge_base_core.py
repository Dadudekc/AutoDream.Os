"""
Knowledge Base Core Interface - V2 Compliant
============================================

Main interface for knowledge base system.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

from typing import Any

from .knowledge_base_models import AntiPattern, CodePattern, DesignPrinciple, PrincipleCategory
from .knowledge_base_operations import KnowledgeBaseCore as KnowledgeBaseOperations
from .knowledge_base_patterns import KnowledgeBasePatterns
from .knowledge_base_principles import KnowledgeBasePrinciples


class KnowledgeBaseCore:
    """Main knowledge base core interface."""
    
    def __init__(self):
        """Initialize knowledge base core."""
        self.principles = KnowledgeBasePrinciples()
        self.patterns = KnowledgeBasePatterns()
        self.operations = KnowledgeBaseOperations()
    
    def get_principle(self, name: str) -> DesignPrinciple | None:
        """Get a specific principle by name."""
        return self.principles.get_principle(name)
    
    def get_principles_by_category(self, category: PrincipleCategory) -> list[DesignPrinciple]:
        """Get all principles in a category."""
        return self.principles.get_principles_by_category(category)
    
    def get_required_principles(self) -> list[DesignPrinciple]:
        """Get all required principles."""
        return self.principles.get_required_principles()
    
    def get_code_pattern(self, name: str) -> CodePattern | None:
        """Get a specific code pattern by name."""
        return self.patterns.get_code_pattern(name)
    
    def get_simple_patterns(self) -> list[CodePattern]:
        """Get all simple patterns."""
        return self.patterns.get_simple_patterns()
    
    def get_anti_pattern(self, name: str) -> AntiPattern | None:
        """Get a specific anti-pattern by name."""
        return self.patterns.get_anti_pattern(name)
    
    def get_critical_anti_patterns(self) -> list[AntiPattern]:
        """Get all critical anti-patterns."""
        return self.patterns.get_critical_anti_patterns()
    
    def validate_code_against_principles(self, code_analysis: dict[str, Any]) -> dict[str, Any]:
        """Validate code against design principles."""
        return self.operations.validate_code_against_principles(code_analysis)
    
    def get_guideline(self, guideline_name: str) -> Any:
        """Get a specific guideline by name."""
        return self.operations.get_guideline(guideline_name)