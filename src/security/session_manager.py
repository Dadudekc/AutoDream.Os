import logging
import secrets
import sqlite3
from datetime import datetime
from typing import Dict, Optional

from .models import UserSession


class SessionManager:
    """Handles user session creation and validation"""

    def __init__(self, db_file: str = "security.db", session_timeout: int = 3600):
        self.db_file = db_file
        self.session_timeout = session_timeout
        self.active_sessions: Dict[str, UserSession] = {}
        self.logger = logging.getLogger(__name__)
        self._initialize_database()

    def create_session(self, user_id: str, ip_address: str, user_agent: str) -> str:
        """Create a new session for a user"""
        try:
            session_id = secrets.token_urlsafe(32)
            session = UserSession(
                session_id=session_id,
                user_id=user_id,
                is_active=True,
                created_at=datetime.now().isoformat(),
                last_activity=datetime.now().isoformat(),
                ip_address=ip_address,
                user_agent=user_agent,
            )

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_sessions (session_id, user_id, is_active, created_at, last_activity, ip_address, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    session.session_id,
                    session.user_id,
                    session.is_active,
                    session.created_at,
                    session.last_activity,
                    session.ip_address,
                    session.user_agent,
                ),
            )
            conn.commit()
            conn.close()

            self.active_sessions[session_id] = session
            return session_id
        except Exception as e:
            self.logger.error(f"Failed to create session: {e}")
            return ""

    def validate_session(self, session_id: str) -> Optional[UserSession]:
        """Validate and return session information"""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                if self._is_session_valid(session):
                    self._update_session_activity(session_id)
                    return session
                del self.active_sessions[session_id]

            session = self._get_session_from_db(session_id)
            if session and self._is_session_valid(session):
                self.active_sessions[session_id] = session
                self._update_session_activity(session_id)
                return session
            return None
        except Exception as e:
            self.logger.error(f"Session validation failed: {e}")
            return None

    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate a session"""
        try:
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            return self._deactivate_session_db(session_id)
        except Exception as e:
            self.logger.error(f"Failed to invalidate session {session_id}: {e}")
            return False

    def cleanup_expired_sessions(self):
        """Remove expired sessions from cache and database"""
        try:
            expired = [sid for sid, sess in self.active_sessions.items() if not self._is_session_valid(sess)]
            for sid in expired:
                del self.active_sessions[sid]
                self._deactivate_session_db(sid)
            if expired:
                self.logger.info(f"Cleaned up {len(expired)} expired sessions")
        except Exception as e:
            self.logger.error(f"Failed to cleanup expired sessions: {e}")

    def invalidate_all_sessions(self):
        """Invalidate all sessions"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("UPDATE user_sessions SET is_active = 0")
            conn.commit()
            conn.close()
            self.active_sessions.clear()
        except Exception as e:
            self.logger.error(f"Failed to invalidate all sessions: {e}")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _initialize_database(self) -> bool:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    is_active INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    last_activity TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT
                )
                """
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize session database: {e}")
            return False

    def _get_session_from_db(self, session_id: str) -> Optional[UserSession]:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT session_id, user_id, is_active, created_at, last_activity, ip_address, user_agent FROM user_sessions WHERE session_id = ?",
                (session_id,),
            )
            result = cursor.fetchone()
            conn.close()
            if result:
                return UserSession(
                    session_id=result[0],
                    user_id=result[1],
                    is_active=bool(result[2]),
                    created_at=result[3],
                    last_activity=result[4],
                    ip_address=result[5],
                    user_agent=result[6],
                )
            return None
        except Exception as e:
            self.logger.error(f"Failed to get session from database: {e}")
            return None

    def _update_session_activity(self, session_id: str):
        try:
            current_time = datetime.now().isoformat()
            if session_id in self.active_sessions:
                self.active_sessions[session_id].last_activity = current_time
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user_sessions SET last_activity = ? WHERE session_id = ?",
                (current_time, session_id),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Failed to update session activity: {e}")

    def _deactivate_session_db(self, session_id: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user_sessions SET is_active = 0 WHERE session_id = ?",
                (session_id,),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Failed to deactivate session in database: {e}")
            return False

    def _is_session_valid(self, session: UserSession) -> bool:
        try:
            if not session.is_active:
                return False
            last_activity = datetime.fromisoformat(session.last_activity)
            return (datetime.now() - last_activity).total_seconds() <= self.session_timeout
        except Exception as e:
            self.logger.error(f"Failed to check session validity: {e}")
            return False
