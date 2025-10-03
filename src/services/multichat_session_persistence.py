#!/usr/bin/env python3
"""
Multichat Session Persistence
============================

V2-compliant solution for maintaining chat sessions across Python processes
Simple, focused session management with multiple storage options
V2 Compliant: ≤200 lines, focused session persistence
"""

import json
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class ChatMessage:
    """Simple chat message data class"""

    id: str
    sender: str
    recipient: str
    content: str
    timestamp: float
    session_id: str


@dataclass
class ChatSession:
    """Simple chat session data class"""

    session_id: str
    participants: list[str]
    created_at: float
    last_activity: float
    message_count: int


class SessionPersistence:
    """V2-compliant session persistence manager"""

    def __init__(self, storage_type: str = "json", storage_path: str = "sessions"):
        self.storage_type = storage_type
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.init_storage()

    def init_storage(self):
        """Initialize storage system"""
        if self.storage_type == "json":
            self.init_json_storage()
        elif self.storage_type == "sqlite":
            self.init_sqlite_storage()
        elif self.storage_type == "memory":
            self.init_memory_storage()

    def init_json_storage(self):
        """Initialize JSON file storage"""
        self.sessions_file = self.storage_path / "sessions.json"
        self.messages_file = self.storage_path / "messages.json"

        # Create empty files if they don't exist
        if not self.sessions_file.exists():
            self.save_json_data(self.sessions_file, {})
        if not self.messages_file.exists():
            self.save_json_data(self.messages_file, [])

    def init_sqlite_storage(self):
        """Initialize SQLite database storage"""
        self.db_file = self.storage_path / "sessions.db"
        with sqlite3.connect(str(self.db_file)) as conn:
            # Create tables
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    participants TEXT,
                    created_at REAL,
                    last_activity REAL,
                    message_count INTEGER
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    sender TEXT,
                    recipient TEXT,
                    content TEXT,
                    timestamp REAL,
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
                """
            )

            conn.commit()

        # Store connection for later use
        self.with sqlite3.connect(str(self.db_file) as conn:)

        self.conn.commit()

    def init_memory_storage(self):
        """Initialize in-memory storage"""
        self.sessions = {}
        self.messages = []

    def create_session(self, session_id: str, participants: list[str]) -> ChatSession:
        """Create new chat session"""
        session = ChatSession(
            session_id=session_id,
            participants=participants,
            created_at=time.time(),
            last_activity=time.time(),
            message_count=0,
        )

        self.save_session(session)
        return session

    def save_session(self, session: ChatSession):
        """Save session to storage"""
        if self.storage_type == "json":
            self.save_session_json(session)
        elif self.storage_type == "sqlite":
            self.save_session_sqlite(session)
        elif self.storage_type == "memory":
            self.save_session_memory(session)

    def save_session_json(self, session: ChatSession):
        """Save session to JSON file"""
        sessions_data = self.load_json_data(self.sessions_file)
        sessions_data[session.session_id] = asdict(session)
        self.save_json_data(self.sessions_file, sessions_data)

    def save_session_sqlite(self, session: ChatSession):
        """Save session to SQLite database"""
        self.conn.execute(
            """
            INSERT OR REPLACE INTO sessions
            (session_id, participants, created_at, last_activity, message_count)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                session.session_id,
                json.dumps(session.participants),
                session.created_at,
                session.last_activity,
                session.message_count,
            ),
        )
        self.conn.commit()

    def save_session_memory(self, session: ChatSession):
        """Save session to memory"""
        self.sessions[session.session_id] = session

    def get_session(self, session_id: str) -> ChatSession | None:
        """Get session by ID"""
        if self.storage_type == "json":
            return self.get_session_json(session_id)
        elif self.storage_type == "sqlite":
            return self.get_session_sqlite(session_id)
        elif self.storage_type == "memory":
            return self.get_session_memory(session_id)
        return None

    def get_session_json(self, session_id: str) -> ChatSession | None:
        """Get session from JSON file"""
        sessions_data = self.load_json_data(self.sessions_file)
        session_data = sessions_data.get(session_id)
        if session_data:
            return ChatSession(**session_data)
        return None

    def get_session_sqlite(self, session_id: str) -> ChatSession | None:
        """Get session from SQLite database"""
        cursor = self.conn.execute(
            """
            SELECT session_id, participants, created_at, last_activity, message_count
            FROM sessions WHERE session_id = ?
        """,
            (session_id,),
        )

        row = cursor.fetchone()
        if row:
            return ChatSession(
                session_id=row[0],
                participants=json.loads(row[1]),
                created_at=row[2],
                last_activity=row[3],
                message_count=row[4],
            )
        return None

    def get_session_memory(self, session_id: str) -> ChatSession | None:
        """Get session from memory"""
        return self.sessions.get(session_id)

    def add_message(self, message: ChatMessage):
        """Add message to session"""
        # Update session activity
        session = self.get_session(message.session_id)
        if session:
            session.last_activity = time.time()
            session.message_count += 1
            self.save_session(session)

        # Save message
        if self.storage_type == "json":
            self.save_message_json(message)
        elif self.storage_type == "sqlite":
            self.save_message_sqlite(message)
        elif self.storage_type == "memory":
            self.save_message_memory(message)

    def save_message_json(self, message: ChatMessage):
        """Save message to JSON file"""
        messages_data = self.load_json_data(self.messages_file)
        messages_data.append(asdict(message))
        self.save_json_data(self.messages_file, messages_data)

    def save_message_sqlite(self, message: ChatMessage):
        """Save message to SQLite database"""
        self.conn.execute(
            """
            INSERT INTO messages
            (id, session_id, sender, recipient, content, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                message.id,
                message.session_id,
                message.sender,
                message.recipient,
                message.content,
                message.timestamp,
            ),
        )
        self.conn.commit()

    def save_message_memory(self, message: ChatMessage):
        """Save message to memory"""
        self.messages.append(message)

    def get_messages(self, session_id: str, limit: int = 100) -> list[ChatMessage]:
        """Get messages for session"""
        if self.storage_type == "json":
            return self.get_messages_json(session_id, limit)
        elif self.storage_type == "sqlite":
            return self.get_messages_sqlite(session_id, limit)
        elif self.storage_type == "memory":
            return self.get_messages_memory(session_id, limit)
        return []

    def get_messages_json(self, session_id: str, limit: int) -> list[ChatMessage]:
        """Get messages from JSON file"""
        messages_data = self.load_json_data(self.messages_file)
        session_messages = [
            ChatMessage(**msg) for msg in messages_data if msg.get("session_id") == session_id
        ]
        return sorted(session_messages, key=lambda x: x.timestamp)[-limit:]

    def get_messages_sqlite(self, session_id: str, limit: int) -> list[ChatMessage]:
        """Get messages from SQLite database"""
        cursor = self.conn.execute(
            """
            SELECT id, session_id, sender, recipient, content, timestamp
            FROM messages WHERE session_id = ?
            ORDER BY timestamp DESC LIMIT ?
        """,
            (session_id, limit),
        )

        messages = []
        for row in cursor.fetchall():
            messages.append(
                ChatMessage(
                    id=row[0],
                    session_id=row[1],
                    sender=row[2],
                    recipient=row[3],
                    content=row[4],
                    timestamp=row[5],
                )
            )
        return messages

    def get_messages_memory(self, session_id: str, limit: int) -> list[ChatMessage]:
        """Get messages from memory"""
        session_messages = [msg for msg in self.messages if msg.session_id == session_id]
        return sorted(session_messages, key=lambda x: x.timestamp)[-limit:]

    def cleanup_old_sessions(self, days: int = 30):
        """Clean up old sessions"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)

        if self.storage_type == "json":
            self.cleanup_json_sessions(cutoff_time)
        elif self.storage_type == "sqlite":
            self.cleanup_sqlite_sessions(cutoff_time)
        elif self.storage_type == "memory":
            self.cleanup_memory_sessions(cutoff_time)

    def cleanup_json_sessions(self, cutoff_time: float):
        """Clean up old JSON sessions"""
        sessions_data = self.load_json_data(self.sessions_file)
        messages_data = self.load_json_data(self.messages_file)

        # Remove old sessions
        old_sessions = [
            sid for sid, session in sessions_data.items() if session["last_activity"] < cutoff_time
        ]

        for sid in old_sessions:
            del sessions_data[sid]
            messages_data = [msg for msg in messages_data if msg.get("session_id") != sid]

        self.save_json_data(self.sessions_file, sessions_data)
        self.save_json_data(self.messages_file, messages_data)

    def cleanup_sqlite_sessions(self, cutoff_time: float):
        """Clean up old SQLite sessions"""
        self.conn.execute("DELETE FROM sessions WHERE last_activity < ?", (cutoff_time,))
        self.conn.execute("DELETE FROM messages WHERE timestamp < ?", (cutoff_time,))
        self.conn.commit()

    def cleanup_memory_sessions(self, cutoff_time: float):
        """Clean up old memory sessions"""
        self.sessions = {
            sid: session
            for sid, session in self.sessions.items()
            if session.last_activity >= cutoff_time
        }
        self.messages = [msg for msg in self.messages if msg.timestamp >= cutoff_time]

    def load_json_data(self, file_path: Path) -> Any:
        """Load JSON data from file"""
        try:
            with open(file_path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if "sessions" in str(file_path) else []

    def save_json_data(self, file_path: Path, data: Any):
        """Save JSON data to file"""
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def close(self):
        """Close storage connections"""
        if self.storage_type == "sqlite" and hasattr(self, "conn"):
            self.conn.close()
