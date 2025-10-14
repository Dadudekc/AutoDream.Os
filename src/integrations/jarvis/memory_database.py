"""
Memory Database Operations - V2 Compliant
==========================================

Database initialization and persistence for Jarvis memory system.
Extracted from memory_system.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist
Date: 2025-10-11
"""

import json
import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .memory_system import MemorySystem


class MemoryDatabase:
    """Handles database operations for memory system."""

    def __init__(self, memory_system: "MemorySystem"):
        """Initialize with memory system reference."""
        self.system = memory_system
        self.db_file = memory_system.db_file
        self.memory_file = memory_system.memory_file

    def init_database(self):
        """Initialize SQLite database for persistent memory"""
        try:
            self.system.conn = sqlite3.connect(self.db_file, check_same_thread=False)
            self.system.cursor = self.system.conn.cursor()

            # Create tables
            self.system.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    user_message TEXT,
                    jarvis_response TEXT,
                    context TEXT,
                    session_id TEXT
                )
            """
            )

            self.system.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp REAL
                )
            """
            )

            self.system.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_info (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp REAL
                )
            """
            )

            self.system.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS learned_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern TEXT,
                    action TEXT,
                    success_rate REAL,
                    last_used REAL,
                    usage_count INTEGER DEFAULT 0
                )
            """
            )

            self.system.conn.commit()
            self.system.logger.info("Database initialized successfully")

        except Exception as e:
            self.system.logger.error(f"Error initializing database: {e}")

    def load_memory(self):
        """Load memory from JSON file"""
        try:
            with open(self.memory_file) as f:
                memory_data = json.load(f)
                self.system.short_term_memory = memory_data.get("short_term", [])
                self.system.user_preferences = memory_data.get("preferences", {})
                self.system.conversation_context = memory_data.get("context", {})
        except FileNotFoundError:
            self.system.logger.info("No existing memory file found, starting fresh")
        except Exception as e:
            self.system.logger.error(f"Error loading memory: {e}")

    def save_memory(self):
        """Save memory to JSON file"""
        try:
            memory_data = {
                "short_term": self.system.short_term_memory,
                "preferences": self.system.user_preferences,
                "context": self.system.conversation_context,
            }
            with open(self.memory_file, "w") as f:
                json.dump(memory_data, f, indent=2)
        except Exception as e:
            self.system.logger.error(f"Error saving memory: {e}")
