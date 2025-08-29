"""Data storage utilities for agent responses."""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict

from .data_config import DEFAULT_DB_PATH


class AgentResponseDatabase:
    """SQLite-backed storage for agent responses and analysis."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path
        self.init_database()

    def connect(self) -> sqlite3.Connection:
        """Create a new database connection."""
        return sqlite3.connect(self.db_path)

    def init_database(self) -> None:
        """Initialize required tables if they do not exist."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                response_file TEXT NOT NULL,
                response_content TEXT,
                response_hash TEXT UNIQUE,
                task_id TEXT,
                response_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                processing_status TEXT DEFAULT 'new'
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS response_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                response_id INTEGER,
                analysis_type TEXT,
                analysis_result TEXT,
                confidence_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (response_id) REFERENCES agent_responses (id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generated_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_response_id INTEGER,
                task_title TEXT,
                task_description TEXT,
                assigned_agent TEXT,
                priority TEXT,
                dependencies TEXT,
                generated_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (source_response_id) REFERENCES agent_responses (id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workflow_chains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chain_name TEXT,
                trigger_response_type TEXT,
                next_task_template TEXT,
                conditions TEXT,
                created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
            """
        )
        conn.commit()
        conn.close()

    def insert_response(
        self,
        agent_id: str,
        response_file: str,
        response_content: str,
        response_hash: str,
        response_type: str,
        file_size: int,
    ) -> int:
        """Store an agent response and return its database ID."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO agent_responses
                (agent_id, response_file, response_content, response_hash, response_type, file_size)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    agent_id,
                    response_file,
                    response_content,
                    response_hash,
                    response_type,
                    file_size,
                ),
            )
            response_id = cursor.lastrowid
        return response_id

    def insert_analysis(self, response_id: int, analysis_result: Dict[str, Any]) -> None:
        """Store analysis results for a response."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO response_analysis
                (response_id, analysis_type, analysis_result, confidence_score)
                VALUES (?, ?, ?, ?)
                """,
                (
                    response_id,
                    "content_analysis",
                    json.dumps(analysis_result),
                    0.8,
                ),
            )

    def insert_task(self, response_id: int, task: Dict[str, Any]) -> None:
        """Store a generated task linked to a response."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO generated_tasks
                (source_response_id, task_title, task_description, assigned_agent, priority, dependencies)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    response_id,
                    task["title"],
                    task["description"],
                    task["agent"],
                    task["priority"],
                    json.dumps(task["dependencies"]),
                ),
            )

    def fetch_agent_progress_summary(self) -> Dict[str, Any]:
        """Get comprehensive progress summary for all agents."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT agent_id, COUNT(*) as response_count,
                       SUM(file_size) as total_size,
                       MAX(timestamp) as last_response
                FROM agent_responses
                GROUP BY agent_id
                """
            )
            agent_stats = cursor.fetchall()
            cursor.execute(
                """
                SELECT COUNT(*) as total_tasks,
                       COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks
                FROM generated_tasks
                """
            )
            task_stats = cursor.fetchone()
        return {
            "agent_stats": agent_stats,
            "task_stats": task_stats,
            "total_responses": sum(stat[1] for stat in agent_stats),
            "total_generated_tasks": task_stats[0] if task_stats else 0,
        }
