"""
Persistent Memory System - SQLite-based persistent memory with LRU caching.
Based on Dream.OS patterns with V2 compliance and KISS principles.

Features:
- SQLite database for persistent storage
- LRU caching for performance optimization
- Data compression for storage efficiency
- Thread-safe operations
- Memory management and cleanup
"""

import os
import sqlite3
import json
import zlib
import threading
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from cachetools import LRUCache

logger = logging.getLogger(__name__)

class PersistentMemoryManager:
    """
    Persistent memory system with SQLite database and LRU caching.
    V2 Compliant: ≤400 lines, simple data classes, direct method calls.
    """
    
    def __init__(self, db_path: str = "memory/persistent_memory.db", cache_size: int = 1000):
        """Initialize PersistentMemoryManager."""
        self.db_path = Path(db_path)
        self.cache_size = cache_size
        self._lock = threading.Lock()
        
        # Ensure memory directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize LRU cache
        self.cache = LRUCache(maxsize=cache_size)
        
        # Initialize database
        self._init_database()
        
        logger.info(f"PersistentMemoryManager initialized with DB: {self.db_path}")
    
    def _init_database(self) -> None:
        """Initialize SQLite database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create memory entries table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memory_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key TEXT UNIQUE NOT NULL,
                        value BLOB NOT NULL,
                        compressed INTEGER DEFAULT 0,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        access_count INTEGER DEFAULT 0,
                        last_accessed TEXT
                    )
                """)
                
                # Create indexes for performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_key ON memory_entries(key)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_updated_at ON memory_entries(updated_at)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_access_count ON memory_entries(access_count)")
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _compress_data(self, data: Any) -> bytes:
        """Compress data for storage."""
        try:
            json_data = json.dumps(data).encode('utf-8')
            return zlib.compress(json_data)
        except Exception as e:
            logger.error(f"Failed to compress data: {e}")
            return json.dumps(data).encode('utf-8')
    
    def _decompress_data(self, data: bytes, compressed: bool) -> Any:
        """Decompress data from storage."""
        try:
            if compressed:
                json_data = zlib.decompress(data)
            else:
                json_data = data
            return json.loads(json_data.decode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to decompress data: {e}")
            return None
    
    def set(self, key: str, value: Any, compress: bool = True) -> bool:
        """Set a value in persistent memory."""
        try:
            with self._lock:
                # Compress data if requested
                compressed_data = self._compress_data(value) if compress else json.dumps(value).encode('utf-8')
                
                # Update database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    now = datetime.now(timezone.utc).isoformat()
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO memory_entries 
                        (key, value, compressed, created_at, updated_at, access_count, last_accessed)
                        VALUES (?, ?, ?, 
                                COALESCE((SELECT created_at FROM memory_entries WHERE key = ?), ?),
                                ?, 0, ?)
                    """, (key, compressed_data, 1 if compress else 0, key, now, now, now))
                    
                    conn.commit()
                
                # Update cache
                self.cache[key] = {
                    'value': value,
                    'updated_at': now,
                    'access_count': 0
                }
                
                logger.info(f"Memory entry set: {key}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to set memory entry {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from persistent memory."""
        try:
            with self._lock:
                # Check cache first
                if key in self.cache:
                    entry = self.cache[key]
                    entry['access_count'] += 1
                    entry['last_accessed'] = datetime.now(timezone.utc).isoformat()
                    logger.info(f"Memory entry retrieved from cache: {key}")
                    return entry['value']
                
                # Get from database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT value, compressed, access_count FROM memory_entries 
                        WHERE key = ?
                    """, (key,))
                    
                    result = cursor.fetchone()
                    if result is None:
                        logger.info(f"Memory entry not found: {key}")
                        return None
                    
                    value_data, compressed, access_count = result
                    value = self._decompress_data(value_data, bool(compressed))
                    
                    if value is None:
                        logger.error(f"Failed to decompress value for key: {key}")
                        return None
                    
                    # Update access count and last accessed
                    now = datetime.now(timezone.utc).isoformat()
                    cursor.execute("""
                        UPDATE memory_entries 
                        SET access_count = ?, last_accessed = ?
                        WHERE key = ?
                    """, (access_count + 1, now, key))
                    conn.commit()
                    
                    # Update cache
                    self.cache[key] = {
                        'value': value,
                        'updated_at': now,
                        'access_count': access_count + 1
                    }
                    
                    logger.info(f"Memory entry retrieved from database: {key}")
                    return value
                    
        except Exception as e:
            logger.error(f"Failed to get memory entry {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a value from persistent memory."""
        try:
            with self._lock:
                # Remove from database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM memory_entries WHERE key = ?", (key,))
                    conn.commit()
                
                # Remove from cache
                if key in self.cache:
                    del self.cache[key]
                
                logger.info(f"Memory entry deleted: {key}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete memory entry {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in persistent memory."""
        try:
            with self._lock:
                # Check cache first
                if key in self.cache:
                    return True
                
                # Check database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1 FROM memory_entries WHERE key = ?", (key,))
                    return cursor.fetchone() is not None
                    
        except Exception as e:
            logger.error(f"Failed to check memory entry existence {key}: {e}")
            return False
    
    def list_keys(self, pattern: Optional[str] = None) -> List[str]:
        """List all keys in persistent memory."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if pattern:
                    cursor.execute("SELECT key FROM memory_entries WHERE key LIKE ?", (pattern,))
                else:
                    cursor.execute("SELECT key FROM memory_entries")
                
                return [row[0] for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Failed to list memory keys: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total entries
                cursor.execute("SELECT COUNT(*) FROM memory_entries")
                total_entries = cursor.fetchone()[0]
                
                # Get cache stats
                cache_size = len(self.cache)
                cache_hits = sum(entry.get('access_count', 0) for entry in self.cache.values())
                
                # Get database size
                cursor.execute("SELECT SUM(LENGTH(value)) FROM memory_entries")
                db_size = cursor.fetchone()[0] or 0
                
                return {
                    'total_entries': total_entries,
                    'cache_size': cache_size,
                    'cache_hits': cache_hits,
                    'database_size_bytes': db_size,
                    'database_path': str(self.db_path)
                }
                
        except Exception as e:
            logger.error(f"Failed to get memory stats: {e}")
            return {}
    
    def cleanup(self, max_age_days: int = 30) -> int:
        """Clean up old memory entries."""
        try:
            cutoff_date = datetime.now(timezone.utc).replace(
                day=datetime.now(timezone.utc).day - max_age_days
            ).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM memory_entries WHERE updated_at < ?", (cutoff_date,))
                deleted_count = cursor.rowcount
                conn.commit()
            
            logger.info(f"Cleaned up {deleted_count} old memory entries")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup memory: {e}")
            return 0
    
    def clear(self) -> bool:
        """Clear all memory entries."""
        try:
            with self._lock:
                # Clear database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM memory_entries")
                    conn.commit()
                
                # Clear cache
                self.cache.clear()
                
                logger.info("All memory entries cleared")
                return True
                
        except Exception as e:
            logger.error(f"Failed to clear memory: {e}")
            return False

# Global persistent memory manager instance
persistent_memory = PersistentMemoryManager()

def set_memory(key: str, value: Any, compress: bool = True) -> bool:
    """Set a value in persistent memory."""
    return persistent_memory.set(key, value, compress)

def get_memory(key: str) -> Optional[Any]:
    """Get a value from persistent memory."""
    return persistent_memory.get(key)

def delete_memory(key: str) -> bool:
    """Delete a value from persistent memory."""
    return persistent_memory.delete(key)

def memory_exists(key: str) -> bool:
    """Check if a key exists in persistent memory."""
    return persistent_memory.exists(key)

def list_memory_keys(pattern: Optional[str] = None) -> List[str]:
    """List all keys in persistent memory."""
    return persistent_memory.list_keys(pattern)

def get_memory_stats() -> Dict[str, Any]:
    """Get memory system statistics."""
    return persistent_memory.get_stats()

def cleanup_memory(max_age_days: int = 30) -> int:
    """Clean up old memory entries."""
    return persistent_memory.cleanup(max_age_days)

def clear_memory() -> bool:
    """Clear all memory entries."""
    return persistent_memory.clear()

