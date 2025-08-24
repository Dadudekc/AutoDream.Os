#!/usr/bin/env python3
"""
Authentication System - Agent Cellphone V2
=========================================

User authentication, session management, and access control.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sqlite3
import hashlib
import hmac
import secrets
import time
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class UserSession:
    """User session information"""
    session_id: str
    user_id: str
    is_active: bool
    created_at: float
    last_activity: float
    ip_address: str
    user_agent: Optional[str] = None


@dataclass
class AuthenticationResult:
    """Authentication result"""
    success: bool
    user_id: Optional[str]
    session_id: Optional[str] = None
    error_message: Optional[str] = None


class AuthenticationSystem:
    """User authentication and session management system"""

    def __init__(self, db_file: str = "security.db"):
        self.logger = logging.getLogger(__name__)
        self.db_file = db_file
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 3
        self.lockout_duration = 1800  # 30 minutes

        # Initialize authentication database
        self._init_auth_database()

    def authenticate_user(
        self, username: str, password: str, source_ip: str, user_agent: str = None
    ) -> AuthenticationResult:
        """Authenticate user credentials"""
        try:
            # Check if user is locked out
            if self._is_user_locked_out(username):
                return AuthenticationResult(
                    success=False,
                    user_id=None,
                    error_message="Account temporarily locked due to failed attempts",
                )

            # Verify credentials (in production, use proper password hashing)
            if self._verify_credentials(username, password):
                # Create user session
                session_id = self._create_user_session(username, source_ip, user_agent)

                # Log successful authentication
                self._log_authentication_event(username, source_ip, True)

                return AuthenticationResult(
                    success=True, user_id=username, session_id=session_id
                )
            else:
                # Log failed authentication
                self._log_authentication_event(username, source_ip, False)

                # Check if user should be locked out
                self._check_lockout_conditions(username)

                return AuthenticationResult(
                    success=False, user_id=None, error_message="Invalid credentials"
                )

        except Exception as e:
            self.logger.error(f"Authentication failed for {username}: {e}")
            return AuthenticationResult(
                success=False, user_id=None, error_message="Authentication system error"
            )

    def _init_auth_database(self):
        """Initialize authentication database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Create users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    last_login REAL,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until REAL DEFAULT 0
                )
            """
            )

            # Create user_sessions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    created_at REAL NOT NULL,
                    last_activity REAL NOT NULL,
                    ip_address TEXT NOT NULL,
                    user_agent TEXT
                )
            """
            )

            # Create authentication logs table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS auth_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    source_ip TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    timestamp REAL NOT NULL,
                    user_agent TEXT
                )
            """
            )

            # Create default admin user if not exists
            cursor.execute("SELECT username FROM users WHERE username = ?", ("admin",))
            if not cursor.fetchone():
                self._create_default_user(cursor, "admin", "secure_password_123")

            conn.commit()
            conn.close()

            self.logger.info("Authentication database initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize authentication database: {e}")

    def _create_default_user(self, cursor, username: str, password: str):
        """Create default user with hashed password"""
        try:
            salt = secrets.token_hex(16)
            password_hash = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), salt.encode(), 100000
            )

            cursor.execute(
                """
                INSERT INTO users (username, password_hash, salt, created_at)
                VALUES (?, ?, ?, ?)
            """,
                (username, password_hash.hex(), salt, time.time()),
            )

        except Exception as e:
            self.logger.error(f"Failed to create default user: {e}")

    def _verify_credentials(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT password_hash, salt FROM users WHERE username = ?", (username,)
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                stored_hash, salt = result
                # Verify password hash
                computed_hash = hashlib.pbkdf2_hmac(
                    "sha256", password.encode(), salt.encode(), 100000
                )
                return hmac.compare_digest(stored_hash, computed_hash.hex())

            return False

        except Exception as e:
            self.logger.error(f"Credential verification failed: {e}")
            return False

    def _create_user_session(
        self, username: str, source_ip: str, user_agent: str = None
    ) -> str:
        """Create new user session"""
        try:
            session_id = secrets.token_urlsafe(32)
            current_time = time.time()

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Create session record
            cursor.execute(
                """
                INSERT INTO user_sessions
                (session_id, user_id, is_active, created_at, last_activity, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    session_id,
                    username,
                    True,
                    current_time,
                    current_time,
                    source_ip,
                    user_agent,
                ),
            )

            conn.commit()
            conn.close()

            return session_id

        except Exception as e:
            self.logger.error(f"Failed to create user session: {e}")
            return None

    def _is_user_locked_out(self, username: str) -> bool:
        """Check if user account is locked out"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT locked_until FROM users WHERE username = ?", (username,)
            )
            result = cursor.fetchone()
            conn.close()

            if result and result[0] > 0:
                return time.time() < result[0]

            return False

        except Exception as e:
            self.logger.error(f"Failed to check lockout status: {e}")
            return False

    def _check_lockout_conditions(self, username: str):
        """Check if user should be locked out after failed attempts"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Get current failed attempts
            cursor.execute(
                "SELECT failed_attempts FROM users WHERE username = ?", (username,)
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                failed_attempts = result[0] + 1

                if failed_attempts >= self.max_login_attempts:
                    # Lock user account
                    lockout_until = time.time() + self.lockout_duration
                    
                    conn = sqlite3.connect(self.db_file)
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET failed_attempts = ?, locked_until = ? WHERE username = ?",
                        (failed_attempts, lockout_until, username),
                    )
                    conn.commit()
                    conn.close()

                    self.logger.warning(f"User {username} locked out until {lockout_until}")
                else:
                    # Update failed attempts count
                    conn = sqlite3.connect(self.db_file)
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET failed_attempts = ? WHERE username = ?",
                        (failed_attempts, username),
                    )
                    conn.commit()
                    conn.close()

        except Exception as e:
            self.logger.error(f"Failed to check lockout conditions: {e}")

    def _log_authentication_event(self, username: str, source_ip: str, success: bool):
        """Log authentication event"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO auth_logs (username, source_ip, success, timestamp)
                VALUES (?, ?, ?, ?)
            """,
                (username, source_ip, success, time.time()),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Failed to log authentication event: {e}")


class SessionManager:
    """User session management system"""

    def __init__(self, db_file: str = "security.db"):
        self.logger = logging.getLogger(__name__)
        self.db_file = db_file
        self.session_timeout = 3600  # 1 hour

    def validate_session(self, session_id: str) -> Optional[UserSession]:
        """Validate and return session information"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT session_id, user_id, is_active, created_at, last_activity, ip_address, user_agent
                FROM user_sessions WHERE session_id = ?
            """,
                (session_id,),
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                session = UserSession(
                    session_id=result[0],
                    user_id=result[1],
                    is_active=result[2],
                    created_at=result[3],
                    last_activity=result[4],
                    ip_address=result[5],
                    user_agent=result[6],
                )

                # Check if session is expired
                if time.time() - session.last_activity > self.session_timeout:
                    self._deactivate_session(session_id)
                    return None

                # Update last activity
                self._update_session_activity(session_id)
                return session

            return None

        except Exception as e:
            self.logger.error(f"Session validation failed: {e}")
            return None

    def _deactivate_session(self, session_id: str):
        """Deactivate expired session"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE user_sessions SET is_active = 0 WHERE session_id = ?",
                (session_id,),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Failed to deactivate session: {e}")

    def _update_session_activity(self, session_id: str):
        """Update session last activity timestamp"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE user_sessions SET last_activity = ? WHERE session_id = ?",
                (time.time(), session_id),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Failed to update session activity: {e}")

    def invalidate_session(self, session_id: str):
        """Invalidate user session"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE user_sessions SET is_active = 0 WHERE session_id = ?",
                (session_id,),
            )

            conn.commit()
            conn.close()

            self.logger.info(f"Session {session_id} invalidated")

        except Exception as e:
            self.logger.error(f"Failed to invalidate session: {e}")


class RoleBasedAccessControl:
    """Role-based access control system"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.roles = {
            "admin": ["read", "write", "delete", "admin"],
            "user": ["read", "write"],
            "guest": ["read"],
        }

    def check_permission(self, user_role: str, action: str) -> bool:
        """Check if user has permission for action"""
        try:
            if user_role in self.roles:
                return action in self.roles[user_role]
            return False
        except Exception as e:
            self.logger.error(f"Permission check failed: {e}")
            return False

    def get_user_permissions(self, user_role: str) -> list:
        """Get all permissions for user role"""
        try:
            return self.roles.get(user_role, [])
        except Exception as e:
            self.logger.error(f"Failed to get user permissions: {e}")
            return []
