"""
Intelligent Context Search Refactored
====================================

Refactored search functionality for intelligent context operations.
V2 Compliance: < 300 lines, single responsibility, search logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import (
    SearchResult, ContextRetrievalResult, ContextType, Priority, Status
)
from .search_base import IntelligentContextSearchBase
from .search_operations import IntelligentContextSearchOperations


class IntelligentContextSearch(IntelligentContextSearchBase):
    """Refactored intelligent context search engine."""
    
    def __init__(self):
        """Initialize intelligent context search."""
        super().__init__()
        
        # Initialize modular components
        self.operations = IntelligentContextSearchOperations(self, None)
    
    def search_contexts(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None,
        limit: int = 10
    ) -> List[SearchResult]:
        """Search contexts with filters."""
        return self.operations.search_contexts(query, context_type, priority_filter, status_filter, limit)
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess search query."""
        return self.operations._preprocess_query(query)
    
    def _perform_search(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None
    ) -> List[SearchResult]:
        """Perform the actual search."""
        return self.operations._perform_search(query, context_type, priority_filter, status_filter)
    
    def _create_mock_results(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None
    ) -> List[SearchResult]:
        """Create mock search results for demonstration."""
        return self.operations._create_mock_results(query, context_type, priority_filter, status_filter)
    
    def search_with_pattern(self, query: str, pattern_name: str) -> List[SearchResult]:
        """Search using a specific pattern."""
        return self.operations.search_with_pattern(query, pattern_name)
    
    def optimize_search_query(self, query: str) -> str:
        """Optimize search query for better results."""
        return self.operations.optimize_search_query(query)
