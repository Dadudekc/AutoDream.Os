"""
Intelligent Context Search
=========================

Search functionality for intelligent context operations.
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


class IntelligentContextSearch:
    """Intelligent context search engine."""
    
    def __init__(self):
        """Initialize intelligent context search."""
        self.search_history: List[Dict[str, Any]] = []
        self.search_patterns: Dict[str, str] = {}
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'
        }
    
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
            
            # Record search history
            self._record_search(query, len(results))
            
            return results
            
        except Exception as e:
            # Return empty results on error
            return []
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess search query."""
        # Convert to lowercase
        query = query.lower()
        
        # Remove special characters except spaces
        query = re.sub(r'[^\w\s]', '', query)
        
        # Remove stop words
        words = query.split()
        words = [word for word in words if word not in self.stop_words]
        
        return ' '.join(words)
    
    def _perform_search(
        self,
        query: str,
        context_type: ContextType = None,
        priority_filter: Priority = None,
        status_filter: Status = None
    ) -> List[SearchResult]:
        """Perform the actual search."""
        results = []
        
        # This is a simplified search implementation
        # In a real system, this would interface with a search engine or database
        
        # Mock search results for demonstration
        if query:
            # Create mock results based on query
            mock_results = self._create_mock_results(query, context_type, priority_filter, status_filter)
            results.extend(mock_results)
        
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
        
        # Mock mission context results
        if not context_type or context_type == ContextType.MISSION:
            if 'mission' in query or 'task' in query:
                results.append(SearchResult(
                    result_id=f"mock_mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    context_type=ContextType.MISSION,
                    relevance_score=0.85,
                    content={
                        "mission_id": "mock_mission_001",
                        "mission_name": f"Mock Mission for {query}",
                        "description": f"Sample mission description related to {query}",
                        "priority": Priority.HIGH.value,
                        "status": Status.ACTIVE.value,
                        "agent_id": "Agent-3",
                        "capabilities_required": ["infrastructure", "devops"]
                    },
                    metadata={"mock": True, "query": query}
                ))
        
        # Mock agent capability results
        if not context_type or context_type == ContextType.AGENT_CAPABILITY:
            if 'capability' in query or 'skill' in query:
                results.append(SearchResult(
                    result_id=f"mock_capability_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    context_type=ContextType.AGENT_CAPABILITY,
                    relevance_score=0.75,
                    content={
                        "agent_id": "Agent-3",
                        "capability_name": f"Mock Capability for {query}",
                        "capability_type": "infrastructure",
                        "proficiency_level": 0.9,
                        "success_rate": 0.85
                    },
                    metadata={"mock": True, "query": query}
                ))
        
        # Mock emergency context results
        if not context_type or context_type == ContextType.EMERGENCY:
            if 'emergency' in query or 'urgent' in query:
                results.append(SearchResult(
                    result_id=f"mock_emergency_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    context_type=ContextType.EMERGENCY,
                    relevance_score=0.95,
                    content={
                        "emergency_id": "mock_emergency_001",
                        "emergency_type": f"Mock Emergency for {query}",
                        "severity": Priority.CRITICAL.value,
                        "description": f"Sample emergency description related to {query}",
                        "affected_agents": ["Agent-3", "Agent-4"],
                        "required_actions": ["immediate_response", "coordination"]
                    },
                    metadata={"mock": True, "query": query}
                ))
        
        return results
    
    def _record_search(self, query: str, result_count: int):
        """Record search in history."""
        self.search_history.append({
            "query": query,
            "result_count": result_count,
            "timestamp": datetime.now(),
            "search_id": f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        })
        
        # Keep only last 100 searches
        if len(self.search_history) > 100:
            self.search_history = self.search_history[-100:]
    
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
    
    def search_with_pattern(self, query: str, pattern_name: str) -> List[SearchResult]:
        """Search using specific pattern."""
        if pattern_name not in self.search_patterns:
            return []
        
        pattern = self.search_patterns[pattern_name]
        
        # Apply pattern-based search
        if re.search(pattern, query, re.IGNORECASE):
            return self.search_contexts(query)
        
        return []
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search statistics."""
        if not self.search_history:
            return {
                "total_searches": 0,
                "average_results": 0.0,
                "most_common_queries": [],
                "search_frequency": {}
            }
        
        total_searches = len(self.search_history)
        average_results = sum(search["result_count"] for search in self.search_history) / total_searches
        
        # Count query frequency
        query_frequency = {}
        for search in self.search_history:
            query = search["query"]
            query_frequency[query] = query_frequency.get(query, 0) + 1
        
        # Get most common queries
        most_common_queries = sorted(
            query_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "total_searches": total_searches,
            "average_results": average_results,
            "most_common_queries": [{"query": q, "count": c} for q, c in most_common_queries],
            "search_frequency": query_frequency
        }
    
    def optimize_search_query(self, query: str) -> str:
        """Optimize search query."""
        # Remove redundant words
        words = query.split()
        optimized_words = []
        
        for word in words:
            if word not in optimized_words:
                optimized_words.append(word)
        
        # Add synonyms for common terms
        synonyms = {
            "mission": "task",
            "capability": "skill",
            "emergency": "urgent",
            "context": "situation"
        }
        
        optimized_query = []
        for word in optimized_words:
            optimized_query.append(word)
            if word in synonyms:
                optimized_query.append(synonyms[word])
        
        return ' '.join(optimized_query)
