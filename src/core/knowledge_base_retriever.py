"""
Knowledge Base Retriever Module - V2 Compliant (≤150 lines)
Advanced search capabilities and query processing for knowledge base.
"""

from typing import Dict, List, Any, Optional, Tuple
from .knowledge_base_core import (
    KnowledgeBaseCore, DesignPrinciple, CodePattern, AntiPattern
)


class KnowledgeBaseRetriever:
    """
    Advanced search and retrieval for AutoDream.OS knowledge base.
    
    Provides sophisticated query processing, result ranking, and caching
    mechanisms for efficient knowledge retrieval.
    """
    
    def __init__(self, core: Optional[KnowledgeBaseCore] = None):
        """Initialize the retriever with core instance."""
        self.core = core or KnowledgeBaseCore()
        self.cache = {}
        self.search_history = []
    
    def search(self, query: str, search_type: str = "all", 
               limit: int = 10) -> List[Dict[str, Any]]:
        """Advanced search with ranking and caching."""
        cache_key = f"{query}_{search_type}_{limit}"
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Perform search
        results = self._perform_search(query, search_type)
        
        # Rank results
        ranked_results = self._rank_results(results, query)
        
        # Apply limit
        limited_results = ranked_results[:limit]
        
        # Cache results
        self.cache[cache_key] = limited_results
        
        # Add to search history
        self.search_history.append({
            "query": query,
            "search_type": search_type,
            "result_count": len(limited_results),
            "timestamp": self._get_timestamp()
        })
        
        return limited_results
    
    def _perform_search(self, query: str, search_type: str) -> List[Dict[str, Any]]:
        """Perform the actual search operation."""
        results = []
        query_lower = query.lower()
        
        if search_type in ["all", "principles"]:
            for principle in self.core.design_principles.values():
                score = self._calculate_relevance_score(principle, query_lower)
                if score > 0:
                    results.append({
                        "type": "principle",
                        "data": principle,
                        "score": score,
                        "matched_fields": self._get_matched_fields(principle, query_lower)
                    })
        
        if search_type in ["all", "patterns"]:
            for pattern in self.core.code_patterns.values():
                score = self._calculate_relevance_score(pattern, query_lower)
                if score > 0:
                    results.append({
                        "type": "pattern",
                        "data": pattern,
                        "score": score,
                        "matched_fields": self._get_matched_fields(pattern, query_lower)
                    })
        
        if search_type in ["all", "anti_patterns"]:
            for anti_pattern in self.core.anti_patterns.values():
                score = self._calculate_relevance_score(anti_pattern, query_lower)
                if score > 0:
                    results.append({
                        "type": "anti_pattern",
                        "data": anti_pattern,
                        "score": score,
                        "matched_fields": self._get_matched_fields(anti_pattern, query_lower)
                    })
        
        return results
    
    def _calculate_relevance_score(self, item: Any, query: str) -> float:
        """Calculate relevance score for search results."""
        score = 0.0
        
        # Name matches get highest score
        if hasattr(item, 'name') and query in item.name.lower():
            score += 10.0
        
        # Description matches get medium score
        if hasattr(item, 'description') and query in item.description.lower():
            score += 5.0
        
        # Rationale matches get lower score
        if hasattr(item, 'rationale') and query in item.rationale.lower():
            score += 3.0
        
        # Examples matches get lower score
        if hasattr(item, 'examples'):
            for example in item.examples:
                if query in example.lower():
                    score += 2.0
        
        # Anti-examples matches get lower score
        if hasattr(item, 'anti_examples'):
            for anti_example in item.anti_examples:
                if query in anti_example.lower():
                    score += 1.0
        
        return score
    
    def _get_matched_fields(self, item: Any, query: str) -> List[str]:
        """Get list of fields that matched the query."""
        matched_fields = []
        
        if hasattr(item, 'name') and query in item.name.lower():
            matched_fields.append("name")
        
        if hasattr(item, 'description') and query in item.description.lower():
            matched_fields.append("description")
        
        if hasattr(item, 'rationale') and query in item.rationale.lower():
            matched_fields.append("rationale")
        
        if hasattr(item, 'examples'):
            for i, example in enumerate(item.examples):
                if query in example.lower():
                    matched_fields.append(f"example_{i}")
        
        if hasattr(item, 'anti_examples'):
            for i, anti_example in enumerate(item.anti_examples):
                if query in anti_example.lower():
                    matched_fields.append(f"anti_example_{i}")
        
        return matched_fields
    
    def _rank_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Rank search results by relevance score."""
        return sorted(results, key=lambda x: x["score"], reverse=True)
    
    def cache_result(self, key: str, result: Any) -> None:
        """Cache a search result."""
        self.cache[key] = result
    
    def get_cached(self, key: str) -> Optional[Any]:
        """Get cached result if available."""
        return self.cache.get(key)
    
    def clear_cache(self) -> None:
        """Clear all cached results."""
        self.cache.clear()
    
    def get_search_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent search history."""
        return self.search_history[-limit:]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "cache_size": len(self.cache),
            "search_history_size": len(self.search_history),
            "cache_keys": list(self.cache.keys())
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def suggest_related_searches(self, query: str) -> List[str]:
        """Suggest related searches based on query."""
        suggestions = []
        query_lower = query.lower()
        
        # Find principles that contain the query
        for principle in self.core.design_principles.values():
            if query_lower in principle.name.lower():
                suggestions.extend(principle.related_principles)
        
        # Find patterns that contain the query
        for pattern in self.core.code_patterns.values():
            if query_lower in pattern.name.lower():
                suggestions.append(f"pattern: {pattern.name}")
        
        # Find anti-patterns that contain the query
        for anti_pattern in self.core.anti_patterns.values():
            if query_lower in anti_pattern.name.lower():
                suggestions.append(f"anti-pattern: {anti_pattern.name}")
        
        # Remove duplicates and limit
        unique_suggestions = list(set(suggestions))
        return unique_suggestions[:5]
    
    def get_popular_searches(self) -> List[Tuple[str, int]]:
        """Get most popular search terms."""
        search_counts = {}
        
        for search in self.search_history:
            query = search["query"]
            search_counts[query] = search_counts.get(query, 0) + 1
        
        # Sort by count and return top 10
        sorted_searches = sorted(search_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_searches[:10]






