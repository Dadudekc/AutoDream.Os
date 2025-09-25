#!/usr/bin/env python3
"""
Swarm Brain Database Core
=========================

Core database operations for the swarm intelligence system.
V2 Compliance: ≤400 lines, focused database functionality.
"""

from __future__ import annotations
import sqlite3
import json
import time
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple, List
from .config import CONFIG
from . import paths  # ensure dirs

logger = logging.getLogger(__name__)

# Load schema SQL
SCHEMA_SQL = (Path(__file__).parent / "schema.sql").read_text()


class SwarmBrain:
    """Core database interface for the swarm intelligence system."""
    
    def __init__(self, path: Optional[Path] = None):
        """Initialize the Swarm Brain database."""
        self.path = Path(path or CONFIG.sqlite_path)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA_SQL)
        logger.info(f"Swarm Brain database initialized: {self.path}")
    
    def upsert_document(self, *, kind: str, ts: int = None, title: str = "", 
                       summary: str = "", tags: List[str] = None, meta: Dict[str, Any] = None,
                       canonical: str = "", project: str = None, agent_id: str = None,
                       ref_id: str = None) -> int:
        """Insert or update a document."""
        ts = ts or int(time.time())
        tags_json = json.dumps(tags or [])
        meta_json = json.dumps(meta or {})
        
        cur = self.conn.cursor()
        
        # Check if document exists by ref_id
        if ref_id:
            cur.execute("SELECT id FROM documents WHERE ref_id=?", (ref_id,))
            row = cur.fetchone()
        else:
            row = None
        
        if row:
            # Update existing document
            doc_id = row["id"]
            cur.execute("""UPDATE documents SET kind=?, project=?, agent_id=?, ts=?, 
                           title=?, summary=?, tags=?, meta=?, canonical=? WHERE id=?""",
                        (kind, project, agent_id, ts, title, summary, tags_json, meta_json, canonical, doc_id))
        else:
            # Insert new document
            cur.execute("""INSERT INTO documents(kind, ref_id, project, agent_id, ts, title, 
                           summary, tags, meta, canonical) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (kind, ref_id, project, agent_id, ts, title, summary, tags_json, meta_json, canonical))
            doc_id = cur.lastrowid
        
        self.conn.commit()
        return doc_id
    
    def insert_lens(self, table: str, doc_id: int, fields: Dict[str, Any]) -> None:
        """Insert data into a specialized lens table."""
        cols = ",".join(["doc_id"] + list(fields.keys()))
        qms = ",".join(["?"] * (1 + len(fields)))
        vals = [doc_id] + list(fields.values())
        
        self.conn.execute(f"INSERT OR REPLACE INTO {table}({cols}) VALUES({qms})", vals)
        self.conn.commit()
    
    def mark_embedded(self, doc_id: int, backend: str, dim: int, norm: float) -> None:
        """Mark a document as having embeddings."""
        self.conn.execute("""INSERT OR REPLACE INTO embeddings(doc_id, backend, dim, norm, created_at) 
                           VALUES(?,?,?,?,?)""",
                          (doc_id, backend, dim, norm, int(time.time())))
        self.conn.commit()
    
    def fetch_canonical_batch(self, where: str = "", params: Sequence[Any] = ()) -> Sequence[sqlite3.Row]:
        """Fetch documents with canonical text for embedding."""
        sql = "SELECT id, canonical, kind, project, agent_id, ts, tags, meta FROM documents"
        if where:
            sql += " WHERE " + where
        return self.conn.execute(sql, params).fetchall()
    
    def get(self, doc_id: int) -> Optional[sqlite3.Row]:
        """Get a document by ID."""
        return self.conn.execute("SELECT * FROM documents WHERE id=?", (doc_id,)).fetchone()
    
    def search_by_metadata(self, *, project: str = None, agent_id: str = None, 
                          kind: str = None, tags: List[str] = None, 
                          limit: int = 100) -> List[sqlite3.Row]:
        """Search documents by metadata filters."""
        conditions = []
        params = []
        
        if project:
            conditions.append("project = ?")
            params.append(project)
        
        if agent_id:
            conditions.append("agent_id = ?")
            params.append(agent_id)
        
        if kind:
            conditions.append("kind = ?")
            params.append(kind)
        
        if tags:
            for tag in tags:
                conditions.append("tags LIKE ?")
                params.append(f'%"{tag}"%')
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        sql = f"SELECT * FROM documents WHERE {where_clause} ORDER BY ts DESC LIMIT ?"
        params.append(limit)
        
        return self.conn.execute(sql, params).fetchall()
    
    def get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get statistics for a specific agent."""
        stats = {}
        
        # Total actions
        result = self.conn.execute("SELECT COUNT(*) as count FROM documents WHERE agent_id = ? AND kind = 'action'", 
                                  (agent_id,)).fetchone()
        stats["total_actions"] = result["count"]
        
        # Success rate
        result = self.conn.execute("""SELECT COUNT(*) as total, 
                                     SUM(CASE WHEN a.outcome = 'success' THEN 1 ELSE 0 END) as success
                                     FROM documents d 
                                     JOIN actions a ON d.id = a.doc_id 
                                     WHERE d.agent_id = ?""", (agent_id,)).fetchone()
        
        if result["total"] > 0:
            stats["success_rate"] = result["success"] / result["total"]
        else:
            stats["success_rate"] = 0.0
        
        # Most used tools
        result = self.conn.execute("""SELECT a.tool, COUNT(*) as count 
                                     FROM documents d 
                                     JOIN actions a ON d.id = a.doc_id 
                                     WHERE d.agent_id = ? 
                                     GROUP BY a.tool 
                                     ORDER BY count DESC 
                                     LIMIT 5""", (agent_id,)).fetchall()
        stats["top_tools"] = [{"tool": row["tool"], "count": row["count"]} for row in result]
        
        return stats
    
    def get_project_stats(self, project: str) -> Dict[str, Any]:
        """Get statistics for a specific project."""
        stats = {}
        
        # Total documents
        result = self.conn.execute("SELECT COUNT(*) as count FROM documents WHERE project = ?", 
                                  (project,)).fetchone()
        stats["total_documents"] = result["count"]
        
        # Document types
        result = self.conn.execute("""SELECT kind, COUNT(*) as count 
                                     FROM documents 
                                     WHERE project = ? 
                                     GROUP BY kind""", (project,)).fetchall()
        stats["document_types"] = {row["kind"]: row["count"] for row in result}
        
        # Agent participation
        result = self.conn.execute("""SELECT agent_id, COUNT(*) as count 
                                     FROM documents 
                                     WHERE project = ? 
                                     GROUP BY agent_id 
                                     ORDER BY count DESC""", (project,)).fetchall()
        stats["agent_participation"] = {row["agent_id"]: row["count"] for row in result}
        
        return stats
    
    def cleanup_old_documents(self, max_age_days: int = 30) -> int:
        """Clean up old documents."""
        cutoff_time = int(time.time()) - (max_age_days * 24 * 60 * 60)
        
        # Count documents to be deleted
        result = self.conn.execute("SELECT COUNT(*) as count FROM documents WHERE ts < ?", 
                                  (cutoff_time,)).fetchone()
        count = result["count"]
        
        if count > 0:
            # Delete old documents (cascade will handle related tables)
            self.conn.execute("DELETE FROM documents WHERE ts < ?", (cutoff_time,))
            self.conn.commit()
            logger.info(f"Cleaned up {count} old documents")
        
        return count
    
    def close(self):
        """Close the database connection."""
        self.conn.close()
        logger.info("Swarm Brain database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()




