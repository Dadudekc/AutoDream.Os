#!/usr/bin/env python3
"""
Knowledge Storage - Agent Cellphone V2
======================================

Database operations and storage management for the knowledge database system.
Extracted from monolithic knowledge_database.py for better modularity.

Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .knowledge_models import KnowledgeEntry, KnowledgeRelationship, SearchIndexEntry


class KnowledgeStorage:
    """Core storage operations for knowledge database"""
    
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.KnowledgeStorage")
        self.init_database()
    
    def init_database(self):
        """Initialize the knowledge database schema"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Main knowledge entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_entries (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    source TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    agent_id TEXT NOT NULL,
                    related_entries TEXT NOT NULL,
                    metadata TEXT NOT NULL
                )
            """)
            
            # Knowledge relationships table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id TEXT NOT NULL,
                    related_id TEXT NOT NULL,
                    relationship_type TEXT NOT NULL,
                    strength REAL NOT NULL,
                    created_at REAL NOT NULL,
                    FOREIGN KEY (entry_id) REFERENCES knowledge_entries (id),
                    FOREIGN KEY (related_id) REFERENCES knowledge_entries (id)
                )
            """)
            
            # Search index table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id TEXT NOT NULL,
                    search_text TEXT NOT NULL,
                    weight REAL NOT NULL,
                    FOREIGN KEY (entry_id) REFERENCES knowledge_entries (id)
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON knowledge_entries (category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags ON knowledge_entries (tags)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_agent ON knowledge_entries (agent_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_created ON knowledge_entries (created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_search ON search_index (search_text)")
            
            conn.commit()
            conn.close()
            self.logger.info(f"Knowledge database initialized: {self.db_path}")
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise
    
    def store_knowledge(self, entry: KnowledgeEntry) -> bool:
        """Store a new knowledge entry"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO knowledge_entries
                (id, title, content, category, tags, source, confidence,
                 created_at, updated_at, agent_id, related_entries, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.id,
                entry.title,
                entry.content,
                entry.category,
                json.dumps(entry.tags),
                entry.source,
                entry.confidence,
                entry.created_at,
                entry.updated_at,
                entry.agent_id,
                json.dumps(entry.related_entries),
                json.dumps(entry.metadata),
            ))
            
            # Update search index
            self._update_search_index(entry, cursor)
            
            conn.commit()
            conn.close()
            self.logger.info(f"Knowledge entry stored: {entry.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store knowledge entry: {e}")
            return False
    
    def _update_search_index(self, entry: KnowledgeEntry, cursor: sqlite3.Cursor):
        """Update search index for an entry"""
        # Remove old index entries
        cursor.execute("DELETE FROM search_index WHERE entry_id = ?", (entry.id,))
        
        # Create new index entries with weights
        search_texts = [
            (entry.title, 1.0),
            (entry.content, 0.8),
            (" ".join(entry.tags), 0.9),
            (entry.category, 0.7),
            (entry.source, 0.5),
        ]
        
        for text, weight in search_texts:
            if text:
                cursor.execute("""
                    INSERT INTO search_index (entry_id, search_text, weight)
                    VALUES (?, ?, ?)
                """, (entry.id, text.lower(), weight))
    
    def get_knowledge_by_id(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Retrieve a knowledge entry by ID"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, content, category, tags, source, confidence,
                       created_at, updated_at, agent_id, related_entries, metadata
                FROM knowledge_entries WHERE id = ?
            """, (entry_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return KnowledgeEntry.from_dict({
                    'id': row[0], 'title': row[1], 'content': row[2],
                    'category': row[3], 'tags': row[4], 'source': row[5],
                    'confidence': row[6], 'created_at': row[7], 'updated_at': row[8],
                    'agent_id': row[9], 'related_entries': row[10], 'metadata': row[11]
                })
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve knowledge entry: {e}")
            return None
    
    def get_knowledge_by_category(self, category: str, limit: int = 50) -> List[KnowledgeEntry]:
        """Retrieve knowledge entries by category"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, content, category, tags, source, confidence,
                       created_at, updated_at, agent_id, related_entries, metadata
                FROM knowledge_entries 
                WHERE category = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (category, limit))
            
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
            self.logger.error(f"Failed to retrieve knowledge by category: {e}")
            return []
    
    def get_knowledge_by_agent(self, agent_id: str, limit: int = 50) -> List[KnowledgeEntry]:
        """Retrieve knowledge entries by agent"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, content, category, tags, source, confidence,
                       created_at, updated_at, agent_id, related_entries, metadata
                FROM knowledge_entries 
                WHERE agent_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (agent_id, limit))
            
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
            self.logger.error(f"Failed to retrieve knowledge by agent: {e}")
            return []
    
    def delete_knowledge(self, entry_id: str) -> bool:
        """Delete a knowledge entry"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Delete related data first
            cursor.execute("DELETE FROM search_index WHERE entry_id = ?", (entry_id,))
            cursor.execute("DELETE FROM knowledge_relationships WHERE entry_id = ? OR related_id = ?", 
                         (entry_id, entry_id))
            
            # Delete main entry
            cursor.execute("DELETE FROM knowledge_entries WHERE id = ?", (entry_id,))
            
            conn.commit()
            conn.close()
            self.logger.info(f"Knowledge entry deleted: {entry_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete knowledge entry: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Count entries
            cursor.execute("SELECT COUNT(*) FROM knowledge_entries")
            total_entries = cursor.fetchone()[0]
            
            # Count by category
            cursor.execute("SELECT category, COUNT(*) FROM knowledge_entries GROUP BY category")
            category_counts = dict(cursor.fetchall())
            
            # Count by agent
            cursor.execute("SELECT agent_id, COUNT(*) FROM knowledge_entries GROUP BY agent_id")
            agent_counts = dict(cursor.fetchall())
            
            # Average confidence
            cursor.execute("SELECT AVG(confidence) FROM knowledge_entries")
            avg_confidence = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            return {
                'total_entries': total_entries,
                'category_counts': category_counts,
                'agent_counts': agent_counts,
                'average_confidence': round(avg_confidence, 3)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {e}")
            return {}
    
    def close(self):
        """Close database connections"""
        # SQLite connections are automatically closed, but this provides a clean interface
        pass


# Export main class
__all__ = ['KnowledgeStorage']
