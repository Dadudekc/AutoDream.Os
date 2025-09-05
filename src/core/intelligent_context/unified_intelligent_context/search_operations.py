"""
Intelligent Context Search Operations
====================================

Search operations for intelligent context search functionality.
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


class IntelligentContextSearchOperations:
    """Search operations for intelligent context search."""
    
    def __init__(self, base_search, logger=None):
        """Initialize search operations with base search reference."""
        self.base_search = base_search
        self.logger = logger
    
    def search_contexts(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None,
        limit: int = 10
    ) -> List[SearchResult]:
        """Search contexts with filters."""
        try:
            # Preprocess query
            processed_query = self._preprocess_query(query)
            
            # Get search results
            results = self._perform_search(processed_query, context_type, priority_filter, status_filter)
            
            # Sort by relevance
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            # Apply limit
            results = results[:limit]
            
            # Record search
            self.base_search._record_search(query, len(results))
            
            return results
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error searching contexts: {e}")
            return []
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess search query."""
        # Convert to lowercase
        query = query.lower()
        
        # Remove stop words
        words = query.split()
        filtered_words = [word for word in words if word not in self.base_search.stop_words]
        
        # Join words back
        processed_query = ' '.join(filtered_words)
        
        return processed_query
    
    def _perform_search(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None
    ) -> List[SearchResult]:
        """Perform the actual search."""
        # This is a simplified implementation
        # In a real system, this would search through actual context data
        results = self._create_mock_results(query, context_type, priority_filter, status_filter)
        
        return results
    
    def _create_mock_results(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None
    ) -> List[SearchResult]:
        """Create mock search results for demonstration."""
        results = []
        
        # Create some mock results based on query
        if 'mission' in query or context_type == ContextType.MISSION:
            results.append(SearchResult(
                result_id=f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="Sample Mission Context",
                description="A sample mission context for testing",
                relevance_score=0.8,
                context_type=ContextType.MISSION,
                metadata={"query": query}
            ))
        
        if 'capability' in query or context_type == ContextType.AGENT_CAPABILITY:
            results.append(SearchResult(
                result_id=f"capability_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="Sample Agent Capability",
                description="A sample agent capability for testing",
                relevance_score=0.7,
                context_type=ContextType.AGENT_CAPABILITY,
                metadata={"query": query}
            ))
        
        if 'emergency' in query or context_type == ContextType.EMERGENCY:
            results.append(SearchResult(
                result_id=f"emergency_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title="Sample Emergency Context",
                description="A sample emergency context for testing",
                relevance_score=0.9,
                context_type=ContextType.EMERGENCY,
                metadata={"query": query}
            ))
        
        return results
    
    def search_with_pattern(self, query: str, pattern_name: str) -> List[SearchResult]:
        """Search using a specific pattern."""
        try:
            if pattern_name not in self.base_search.search_patterns:
                return []
            
            pattern = self.base_search.search_patterns[pattern_name]
            
            # Apply pattern to query
            if pattern:
                # Simple pattern matching - in real implementation this would be more sophisticated
                if re.search(pattern, query, re.IGNORECASE):
                    return self.search_contexts(query)
            
            return []
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error searching with pattern: {e}")
            return []
    
    def optimize_search_query(self, query: str) -> str:
        """Optimize search query for better results."""
        try:
            # Remove extra whitespace
            query = ' '.join(query.split())
            
            # Convert to lowercase
            query = query.lower()
            
            # Remove special characters except spaces
            query = re.sub(r'[^\w\s]', '', query)
            
            # Remove duplicate words
            words = query.split()
            unique_words = []
            for word in words:
                if word not in unique_words:
                    unique_words.append(word)
            
            optimized_query = ' '.join(unique_words)
            
            return optimized_query
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error optimizing search query: {e}")
            return query
