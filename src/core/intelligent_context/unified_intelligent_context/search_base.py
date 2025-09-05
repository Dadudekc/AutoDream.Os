"""
Intelligent Context Search Base
==============================

Base functionality for intelligent context search operations.
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


class IntelligentContextSearchBase:
    """Base intelligent context search engine."""
    
    def __init__(self):
        """Initialize intelligent context search."""
        self.search_history: List[Dict[str, Any]] = []
        self.search_patterns: Dict[str, str] = {}
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'
        }
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """Get search history."""
        return self.search_history.copy()
    
    def clear_search_history(self):
        """Clear search history."""
        self.search_history.clear()
    
    def add_search_pattern(self, pattern_name: str, pattern: str):
        """Add search pattern."""
        self.search_patterns[pattern_name] = pattern
    
    def get_search_patterns(self) -> Dict[str, str]:
        """Get search patterns."""
        return self.search_patterns.copy()
    
    def _record_search(self, query: str, result_count: int):
        """Record search in history."""
        self.search_history.append({
            'query': query,
            'result_count': result_count,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search statistics."""
        if not self.search_history:
            return {
                'total_searches': 0,
                'average_results': 0,
                'most_common_queries': [],
                'search_patterns_count': len(self.search_patterns)
            }
        
        total_searches = len(self.search_history)
        total_results = sum(entry['result_count'] for entry in self.search_history)
        average_results = total_results / total_searches if total_searches > 0 else 0
        
        # Get most common queries
        query_counts = {}
        for entry in self.search_history:
            query = entry['query']
            query_counts[query] = query_counts.get(query, 0) + 1
        
        most_common_queries = sorted(
            query_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return {
            'total_searches': total_searches,
            'average_results': average_results,
            'most_common_queries': most_common_queries,
            'search_patterns_count': len(self.search_patterns)
        }
