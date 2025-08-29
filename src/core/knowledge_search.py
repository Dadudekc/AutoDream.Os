#!/usr/bin/env python3
"""
Knowledge Search - Agent Cellphone V2
=====================================

Search and indexing functionality for the knowledge database system.
Extracted from monolithic knowledge_database.py for better modularity.

Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import sqlite3
import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .knowledge_models import KnowledgeEntry, SearchIndexEntry


class KnowledgeSearch:
    """Advanced search and indexing for knowledge database"""
    
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = Path(db_path)
        self.logger = logging.getLogger(f"{__name__}.KnowledgeSearch")
    
    def search_knowledge(self, query: str, limit: int = 20) -> List[Tuple[KnowledgeEntry, float]]:
        """Search knowledge base with relevance scoring"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Clean and tokenize query
            query_tokens = self._tokenize_query(query)
            
            # Search across multiple fields with weights
            results = []
            seen_entries = set()
            
            # Search in title (highest weight)
            title_results = self._search_field(cursor, 'title', query_tokens, 1.0, limit)
            for entry, score in title_results:
                if entry.id not in seen_entries:
                    results.append((entry, score))
                    seen_entries.add(entry.id)
            
            # Search in content
            content_results = self._search_field(cursor, 'content', query_tokens, 0.8, limit)
            for entry, score in content_results:
                if entry.id not in seen_entries:
                    results.append((entry, score))
                    seen_entries.add(entry.id)
            
            # Search in tags
            tag_results = self._search_field(cursor, 'tags', query_tokens, 0.9, limit)
            for entry, score in tag_results:
                if entry.id not in seen_entries:
                    results.append((entry, score))
                    seen_entries.add(entry.id)
            
            # Search in category
            category_results = self._search_field(cursor, 'category', query_tokens, 0.7, limit)
            for entry, score in category_results:
                if entry.id not in seen_entries:
                    results.append((entry, score))
                    seen_entries.add(entry.id)
            
            # Search in source
            source_results = self._search_field(cursor, 'source', query_tokens, 0.5, limit)
            for entry, score in source_results:
                if entry.id not in seen_entries:
                    results.append((entry, score))
                    seen_entries.add(entry.id)
            
            conn.close()
            
            # Sort by relevance score and limit results
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:limit]
            
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []
    
    def _tokenize_query(self, query: str) -> List[str]:
        """Tokenize search query into meaningful terms"""
        # Convert to lowercase and split on whitespace
        tokens = query.lower().split()
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        
        # Stem tokens (simple stemming)
        stemmed = []
        for token in tokens:
            if token.endswith('ing'):
                stemmed.append(token[:-3])
            elif token.endswith('ed'):
                stemmed.append(token[:-2])
            elif token.endswith('s'):
                stemmed.append(token[:-1])
            else:
                stemmed.append(token)
        
        return list(set(stemmed))  # Remove duplicates
    
    def _search_field(self, cursor: sqlite3.Cursor, field: str, tokens: List[str], 
                      base_weight: float, limit: int) -> List[Tuple[KnowledgeEntry, float]]:
        """Search in a specific field with token matching"""
        results = []
        
        for token in tokens:
            # Use LIKE for partial matching
            pattern = f"%{token}%"
            
            cursor.execute(f"""
                SELECT id, title, content, category, tags, source, confidence,
                       created_at, updated_at, agent_id, related_entries, metadata
                FROM knowledge_entries 
                WHERE {field} LIKE ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (pattern, limit))
            
            rows = cursor.fetchall()
            
            for row in rows:
                entry = KnowledgeEntry.from_dict({
                    'id': row[0], 'title': row[1], 'content': row[2],
                    'category': row[3], 'tags': row[4], 'source': row[5],
                    'confidence': row[6], 'created_at': row[7], 'updated_at': row[8],
                    'agent_id': row[9], 'related_entries': row[10], 'metadata': row[11]
                })
                
                # Calculate relevance score
                score = self._calculate_relevance_score(entry, token, field, base_weight)
                results.append((entry, score))
        
        return results
    
    def _calculate_relevance_score(self, entry: KnowledgeEntry, token: str, 
                                  field: str, base_weight: float) -> float:
        """Calculate relevance score for a search result"""
        score = base_weight
        
        # Boost score for exact matches
        if token.lower() in entry.title.lower():
            score += 0.3
        if token.lower() in entry.content.lower():
            score += 0.2
        if token.lower() in [tag.lower() for tag in entry.tags]:
            score += 0.4
        
        # Boost score for recent entries
        age_days = entry.get_age_days()
        if age_days <= 1:
            score += 0.2  # Very recent
        elif age_days <= 7:
            score += 0.1  # Recent
        elif age_days <= 30:
            score += 0.05  # Somewhat recent
        
        # Boost score for high confidence entries
        score += entry.confidence * 0.1
        
        return min(1.0, score)  # Cap at 1.0
    
    def search_by_tags(self, tags: List[str], limit: int = 50) -> List[KnowledgeEntry]:
        """Search for entries matching specific tags"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Build tag search query
            tag_conditions = []
            tag_params = []
            
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                tag_params.append(f"%{tag}%")
            
            if not tag_conditions:
                return []
            
            query = f"""
                SELECT id, title, content, category, tags, source, confidence,
                       created_at, updated_at, agent_id, related_entries, metadata
                FROM knowledge_entries 
                WHERE {' OR '.join(tag_conditions)}
                ORDER BY created_at DESC 
                LIMIT ?
            """
            
            cursor.execute(query, tag_params + [limit])
            rows = cursor.fetchall()
            conn.close()
            
            entries = []
            for row in rows:
                entry = KnowledgeEntry.from_dict({
                    'id': row[0], 'title': row[1], 'content': row[2],
                    'category': row[3], 'tags': row[4], 'source': row[5],
                    'confidence': row[6], 'created_at': row[7], 'updated_at': row[8],
                    'agent_id': row[9], 'related_entries': row[10], 'metadata': row[11]
                })
                entries.append(entry)
            
            return entries
            
        except Exception as e:
            self.logger.error(f"Tag search failed: {e}")
            return []
    
    def search_by_date_range(self, start_date: datetime, end_date: datetime, 
                            limit: int = 50) -> List[KnowledgeEntry]:
        """Search for entries within a date range"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            start_timestamp = start_date.timestamp()
            end_timestamp = end_date.timestamp()
            
            cursor.execute("""
                SELECT id, title, content, category, tags, source, confidence,
                       created_at, updated_at, agent_id, related_entries, metadata
                FROM knowledge_entries 
                WHERE created_at BETWEEN ? AND ?
                ORDER BY created_at DESC 
                LIMIT ?
            """, (start_timestamp, end_timestamp, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            entries = []
            for row in rows:
                entry = KnowledgeEntry.from_dict({
                    'id': row[0], 'title': row[1], 'content': row[2],
                    'category': row[3], 'tags': row[4], 'source': row[5],
                    'confidence': row[6], 'created_at': row[7], 'updated_at': row[8],
                    'agent_id': row[9], 'related_entries': row[10], 'metadata': row[11]
                })
                entries.append(entry)
            
            return entries
            
        except Exception as e:
            self.logger.error(f"Date range search failed: {e}")
            return []
    
    def get_search_suggestions(self, partial_query: str, limit: int = 10) -> List[str]:
        """Get search suggestions based on partial input"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Search for titles that start with the partial query
            pattern = f"{partial_query.lower()}%"
            
            cursor.execute("""
                SELECT DISTINCT title 
                FROM knowledge_entries 
                WHERE LOWER(title) LIKE ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (pattern, limit))
            
            suggestions = [row[0] for row in cursor.fetchall()]
            
            # Also search for tags
            cursor.execute("""
                SELECT DISTINCT tags 
                FROM knowledge_entries 
                WHERE tags LIKE ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (pattern, limit))
            
            tag_suggestions = []
            for row in cursor.fetchall():
                tags = json.loads(row[0])
                for tag in tags:
                    if tag.lower().startswith(partial_query.lower()):
                        tag_suggestions.append(tag)
            
            suggestions.extend(tag_suggestions[:limit//2])
            conn.close()
            
            return list(set(suggestions))[:limit]
            
        except Exception as e:
            self.logger.error(f"Search suggestions failed: {e}")
            return []
    
    def get_popular_searches(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get most popular search terms"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # This would require a search_log table to track actual searches
            # For now, return popular categories
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM knowledge_entries 
                GROUP BY category 
                ORDER BY count DESC 
                LIMIT ?
            """, (limit,))
            
            popular = [(row[0], row[1]) for row in cursor.fetchall()]
            conn.close()
            
            return popular
            
        except Exception as e:
            self.logger.error(f"Popular searches failed: {e}")
            return []


# Export main class
__all__ = ['KnowledgeSearch']
