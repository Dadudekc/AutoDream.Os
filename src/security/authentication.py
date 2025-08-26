#!/usr/bin/env python3
"""
Authentication and Security System - Agent Cellphone V2

Provides comprehensive authentication, session management, and security features.
Integrates with core infrastructure for unified security management.

Author: Security Integration Specialist
V2 Standards: ≤200 LOC, SRP, OOP principles, BaseManager inheritance
"""

import logging
import hashlib
import secrets
import sqlite3
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from ..core.base_manager import BaseManager, ManagerStatus, ManagerPriority


@dataclass
class User:
    """User account information"""
    user_id: str
    username: str
    email: str
    password_hash: str
    role: str
    is_active: bool
    created_at: str
    last_login: Optional[str] = None
    failed_attempts: int = 0
    locked_until: Optional[str] = None


@dataclass
class UserSession:
    """User session information"""
    session_id: str
    user_id: str
    is_active: bool
    created_at: str
    last_activity: str
    ip_address: str
    user_agent: str


class AuthenticationManager(BaseManager):
    """
    Authentication Manager - Manages user authentication and security
    
    Now inherits from BaseManager for unified functionality
    """
    
    def __init__(self, db_file: str = "security.db"):
        """Initialize authentication manager with BaseManager"""
        super().__init__(
            manager_id="authentication_manager",
            name="Authentication Manager",
            description="Manages user authentication, sessions, and security"
        )
        
        self.db_file = db_file
        self.max_failed_attempts = 5
        self.lockout_duration = 900  # 15 minutes
        self.session_timeout = 3600  # 1 hour
        
        # Security tracking
        self.failed_login_attempts: Dict[str, int] = {}
        self.locked_accounts: Dict[str, str] = {}
        self.active_sessions: Dict[str, UserSession] = {}
        
        self.logger.info("Authentication Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize authentication system"""
        try:
            self.logger.info("Starting Authentication Manager...")
            
            # Initialize database
            if not self._initialize_database():
                raise RuntimeError("Failed to initialize database")
            
            # Clear tracking data
            self.failed_login_attempts.clear()
            self.locked_accounts.clear()
            self.active_sessions.clear()
            
            self.logger.info("Authentication Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Authentication Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup authentication system"""
        try:
            self.logger.info("Stopping Authentication Manager...")
            
            # Invalidate all active sessions
            self._invalidate_all_sessions()
            
            # Clear tracking data
            self.failed_login_attempts.clear()
            self.locked_accounts.clear()
            self.active_sessions.clear()
            
            self.logger.info("Authentication Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Authentication Manager: {e}")
    
    def _on_heartbeat(self):
        """Authentication manager heartbeat"""
        try:
            # Clean up expired sessions
            self._cleanup_expired_sessions()
            
            # Check for locked accounts that can be unlocked
            self._check_locked_accounts()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize authentication resources"""
        try:
            # Initialize data structures
            self.failed_login_attempts = {}
            self.locked_accounts = {}
            self.active_sessions = {}
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup authentication resources"""
        try:
            # Clear data
            self.failed_login_attempts.clear()
            self.locked_accounts.clear()
            self.active_sessions.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reset failed attempts
            self.failed_login_attempts.clear()
            self.locked_accounts.clear()
            
            # Reinitialize database connection
            if self._initialize_database():
                self.logger.info("Recovery successful")
                return True
            else:
                self.logger.error("Recovery failed - could not reinitialize database")
                return False
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Authentication Management Methods
    # ============================================================================
    
    def authenticate_user(self, username: str, password: str, ip_address: str = "", user_agent: str = "") -> Optional[str]:
        """Authenticate user and create session"""
        try:
            # Check if account is locked
            if self._is_account_locked(username):
                self.logger.warning(f"Login attempt for locked account: {username}")
                return None
            
            # Verify credentials
            user = self._get_user_by_username(username)
            if not user or not self._verify_password(password, user.password_hash):
                self._record_failed_attempt(username)
                self.logger.warning(f"Failed login attempt for user: {username}")
                return None
            
            # Reset failed attempts on successful login
            self._reset_failed_attempts(username)
            
            # Create session
            session_id = self._create_session(user.user_id, ip_address, user_agent)
            
            # Update last login
            self._update_last_login(user.user_id)
            
            # Record operation
            self.record_operation("authenticate_user", True, 0.0)
            
            self.logger.info(f"User {username} authenticated successfully")
            return session_id
            
        except Exception as e:
            self.logger.error(f"Authentication failed for {username}: {e}")
            self.record_operation("authenticate_user", False, 0.0)
            return None
    
    def validate_session(self, session_id: str) -> Optional[UserSession]:
        """Validate and return session information"""
        try:
            # Check active sessions cache first
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                if self._is_session_valid(session):
                    # Update last activity
                    self._update_session_activity(session_id)
                    return session
                else:
                    # Remove expired session from cache
                    del self.active_sessions[session_id]
            
            # Query database
            session = self._get_session_from_db(session_id)
            if session and self._is_session_valid(session):
                # Add to cache
                self.active_sessions[session_id] = session
                # Update last activity
                self._update_session_activity(session_id)
                
                # Record operation
                self.record_operation("validate_session", True, 0.0)
                
                return session
            
            # Record operation
            self.record_operation("validate_session", False, 0.0)
            return None
            
        except Exception as e:
            self.logger.error(f"Session validation failed: {e}")
            self.record_operation("validate_session", False, 0.0)
            return None
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate user session"""
        try:
            # Remove from cache
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            
            # Update database
            success = self._deactivate_session_db(session_id)
            
            # Record operation
            self.record_operation("invalidate_session", success, 0.0)
            
            if success:
                self.logger.info(f"Session {session_id} invalidated")
            else:
                self.logger.warning(f"Failed to invalidate session {session_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to invalidate session {session_id}: {e}")
            self.record_operation("invalidate_session", False, 0.0)
            return False
    
    def create_user(self, username: str, email: str, password: str, role: str = "user") -> bool:
        """Create new user account"""
        try:
            # Check if username already exists
            if self._get_user_by_username(username):
                self.logger.warning(f"Username {username} already exists")
                return False
            
            # Hash password
            password_hash = self._hash_password(password)
            
            # Create user
            user_id = f"user_{int(time.time())}"
            user = User(
                user_id=user_id,
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                is_active=True,
                created_at=datetime.now().isoformat()
            )
            
            # Save to database
            success = self._save_user_to_db(user)
            
            # Record operation
            self.record_operation("create_user", success, 0.0)
            
            if success:
                self.logger.info(f"User {username} created successfully")
            else:
                self.logger.error(f"Failed to create user {username}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to create user {username}: {e}")
            self.record_operation("create_user", False, 0.0)
            return False
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        try:
            user = self._get_user_by_id(user_id)
            if not user:
                return None
            
            # Record operation
            self.record_operation("get_user_info", True, 0.0)
            
            return {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "last_login": user.last_login,
                "failed_attempts": user.failed_attempts
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get user info for {user_id}: {e}")
            self.record_operation("get_user_info", False, 0.0)
            return None
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        try:
            count = len(self.active_sessions)
            
            # Record operation
            self.record_operation("get_active_sessions_count", True, 0.0)
            
            return count
            
        except Exception as e:
            self.logger.error(f"Failed to get active sessions count: {e}")
            self.record_operation("get_active_sessions_count", False, 0.0)
            return 0
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _initialize_database(self) -> bool:
        """Initialize security database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    is_active INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    last_login TEXT,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until TEXT
                )
            """)
            
            # Create sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    is_active INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    last_activity TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            conn.commit()
            conn.close()
            
            self.logger.info("Security database initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            return False
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == password_hash
    
    def _get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username from database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT user_id, username, email, password_hash, role, is_active, created_at, last_login, failed_attempts, locked_until FROM users WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return User(
                    user_id=result[0],
                    username=result[1],
                    email=result[2],
                    password_hash=result[3],
                    role=result[4],
                    is_active=bool(result[5]),
                    created_at=result[6],
                    last_login=result[7],
                    failed_attempts=result[8],
                    locked_until=result[9]
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get user by username {username}: {e}")
            return None
    
    def _get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID from database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT user_id, username, email, password_hash, role, is_active, created_at, last_login, failed_attempts, locked_until FROM users WHERE user_id = ?",
                (user_id,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return User(
                    user_id=result[0],
                    username=result[1],
                    email=result[2],
                    password_hash=result[3],
                    role=result[4],
                    is_active=bool(result[5]),
                    created_at=result[6],
                    last_login=result[7],
                    failed_attempts=result[8],
                    locked_until=result[9]
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get user by ID {user_id}: {e}")
            return None
    
    def _save_user_to_db(self, user: User) -> bool:
        """Save user to database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO users (user_id, username, email, password_hash, role, is_active, created_at, last_login, failed_attempts, locked_until) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user.user_id, user.username, user.email, user.password_hash, user.role, user.is_active, user.created_at, user.last_login, user.failed_attempts, user.locked_until)
            )
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save user to database: {e}")
            return False
    
    def _create_session(self, user_id: str, ip_address: str, user_agent: str) -> str:
        """Create new user session"""
        try:
            session_id = secrets.token_urlsafe(32)
            
            session = UserSession(
                session_id=session_id,
                user_id=user_id,
                is_active=True,
                created_at=datetime.now().isoformat(),
                last_activity=datetime.now().isoformat(),
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Save to database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO user_sessions (session_id, user_id, is_active, created_at, last_activity, ip_address, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (session.session_id, session.user_id, session.is_active, session.created_at, session.last_activity, session.ip_address, session.user_agent)
            )
            
            conn.commit()
            conn.close()
            
            # Add to cache
            self.active_sessions[session_id] = session
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to create session: {e}")
            return ""
    
    def _get_session_from_db(self, session_id: str) -> Optional[UserSession]:
        """Get session from database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT session_id, user_id, is_active, created_at, last_activity, ip_address, user_agent FROM user_sessions WHERE session_id = ?",
                (session_id,)
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
                    user_agent=result[6]
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get session from database: {e}")
            return None
    
    def _is_session_valid(self, session: UserSession) -> bool:
        """Check if session is valid and not expired"""
        try:
            if not session.is_active:
                return False
            
            # Check timeout
            last_activity = datetime.fromisoformat(session.last_activity)
            if (datetime.now() - last_activity).total_seconds() > self.session_timeout:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to check session validity: {e}")
            return False
    
    def _update_session_activity(self, session_id: str):
        """Update session last activity timestamp"""
        try:
            current_time = datetime.now().isoformat()
            
            # Update cache
            if session_id in self.active_sessions:
                self.active_sessions[session_id].last_activity = current_time
            
            # Update database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE user_sessions SET last_activity = ? WHERE session_id = ?",
                (current_time, session_id)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to update session activity: {e}")
    
    def _deactivate_session_db(self, session_id: str) -> bool:
        """Deactivate session in database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE user_sessions SET is_active = 0 WHERE session_id = ?",
                (session_id,)
            )
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to deactivate session in database: {e}")
            return False
    
    def _record_failed_attempt(self, username: str):
        """Record failed login attempt"""
        try:
            if username not in self.failed_login_attempts:
                self.failed_login_attempts[username] = 0
            
            self.failed_login_attempts[username] += 1
            
            # Lock account if too many failed attempts
            if self.failed_login_attempts[username] >= self.max_failed_attempts:
                self._lock_account(username)
                
        except Exception as e:
            self.logger.error(f"Failed to record failed attempt: {e}")
    
    def _reset_failed_attempts(self, username: str):
        """Reset failed login attempts for user"""
        try:
            if username in self.failed_login_attempts:
                del self.failed_login_attempts[username]
            
            # Update database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE username = ?",
                (username,)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to reset failed attempts: {e}")
    
    def _lock_account(self, username: str):
        """Lock user account"""
        try:
            lock_until = datetime.now() + timedelta(seconds=self.lockout_duration)
            lock_until_str = lock_until.isoformat()
            
            self.locked_accounts[username] = lock_until_str
            
            # Update database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET locked_until = ? WHERE username = ?",
                (lock_until_str, username)
            )
            
            conn.commit()
            conn.close()
            
            self.logger.warning(f"Account {username} locked until {lock_until_str}")
            
        except Exception as e:
            self.logger.error(f"Failed to lock account {username}: {e}")
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked"""
        try:
            # Check cache first
            if username in self.locked_accounts:
                lock_until = datetime.fromisoformat(self.locked_accounts[username])
                if datetime.now() < lock_until:
                    return True
                else:
                    # Remove expired lock
                    del self.locked_accounts[username]
                    return False
            
            # Check database
            user = self._get_user_by_username(username)
            if user and user.locked_until:
                lock_until = datetime.fromisoformat(user.locked_until)
                if datetime.now() < lock_until:
                    # Update cache
                    self.locked_accounts[username] = user.locked_until
                    return True
                else:
                    # Clear expired lock
                    self._clear_account_lock(username)
                    return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to check account lock status: {e}")
            return False
    
    def _clear_account_lock(self, username: str):
        """Clear account lock"""
        try:
            # Remove from cache
            if username in self.locked_accounts:
                del self.locked_accounts[username]
            
            # Update database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET locked_until = NULL WHERE username = ?",
                (username,)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to clear account lock: {e}")
    
    def _update_last_login(self, user_id: str):
        """Update user's last login timestamp"""
        try:
            current_time = datetime.now().isoformat()
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE user_id = ?",
                (current_time, user_id)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to update last login: {e}")
    
    def _cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        try:
            expired_sessions = []
            
            for session_id, session in list(self.active_sessions.items()):
                if not self._is_session_valid(session):
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self.active_sessions[session_id]
                self._deactivate_session_db(session_id)
            
            if expired_sessions:
                self.logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup expired sessions: {e}")
    
    def _check_locked_accounts(self):
        """Check for locked accounts that can be unlocked"""
        try:
            unlocked_accounts = []
            
            for username, lock_until_str in list(self.locked_accounts.items()):
                lock_until = datetime.fromisoformat(lock_until_str)
                if datetime.now() >= lock_until:
                    unlocked_accounts.append(username)
            
            for username in unlocked_accounts:
                del self.locked_accounts[username]
                self._clear_account_lock(username)
            
            if unlocked_accounts:
                self.logger.info(f"Unlocked {len(unlocked_accounts)} accounts")
                
        except Exception as e:
            self.logger.error(f"Failed to check locked accounts: {e}")
    
    def _invalidate_all_sessions(self):
        """Invalidate all active sessions"""
        try:
            # Deactivate all sessions in database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE user_sessions SET is_active = 0")
            
            conn.commit()
            conn.close()
            
            # Clear cache
            self.active_sessions.clear()
            
            self.logger.info("All sessions invalidated")
            
        except Exception as e:
            self.logger.error(f"Failed to invalidate all sessions: {e}")


class SessionManager(BaseManager):
    """User session management system - Legacy compatibility
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, db_file: str = "security.db"):
        super().__init__(
            manager_id="session_manager",
            name="Session Manager",
            description="Manages user sessions and authentication state"
        )
        
        self.db_file = db_file
        self.session_timeout = 3600  # 1 hour
        
        # Session management tracking
        self.session_operations: List[Dict[str, Any]] = []
        self.session_validations = 0
        self.session_invalidations = 0
        self.failed_operations: List[Dict[str, Any]] = []
        
        self.logger.info("Session Manager initialized")

    def validate_session(self, session_id: str) -> Optional[UserSession]:
        """Validate and return session information"""
        start_time = time.time()
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
                
                # Record successful operation
                self.session_validations += 1
                self.record_operation("validate_session", True, time.time() - start_time)
                
                return session

            # Record failed operation
            self.record_operation("validate_session", False, time.time() - start_time)
            return None

        except Exception as e:
            self.logger.error(f"Session validation failed: {e}")
            self.record_operation("validate_session", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "validate_session",
                "session_id": session_id,
                "error": str(e),
                "timestamp": time.time()
            })
            return None

    def _deactivate_session(self, session_id: str):
        """Deactivate expired session"""
        start_time = time.time()
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE user_sessions SET is_active = 0 WHERE session_id = ?",
                (session_id,),
            )

            conn.commit()
            conn.close()
            
            # Record operation
            self.record_operation("deactivate_session", True, time.time() - start_time)

        except Exception as e:
            self.logger.error(f"Failed to deactivate session: {e}")
            self.record_operation("deactivate_session", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "deactivate_session",
                "session_id": session_id,
                "error": str(e),
                "timestamp": time.time()
            })

    def _update_session_activity(self, session_id: str):
        """Update session last activity timestamp"""
        start_time = time.time()
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE user_sessions SET last_activity = ? WHERE session_id = ?",
                (time.time(), session_id),
            )

            conn.commit()
            conn.close()
            
            # Record operation
            self.record_operation("update_session_activity", True, time.time() - start_time)

        except Exception as e:
            self.logger.error(f"Failed to update session activity: {e}")
            self.record_operation("update_session_activity", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "update_session_activity",
                "session_id": session_id,
                "error": str(e),
                "timestamp": time.time()
            })

    def invalidate_session(self, session_id: str):
        """Invalidate user session"""
        start_time = time.time()
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE user_sessions SET is_active = 0 WHERE session_id = ?",
                (session_id,),
            )

            conn.commit()
            conn.close()

            # Record successful operation
            self.session_invalidations += 1
            self.record_operation("invalidate_session", True, time.time() - start_time)
            self.logger.info(f"Session {session_id} invalidated")

        except Exception as e:
            self.logger.error(f"Failed to invalidate session: {e}")
            self.record_operation("invalidate_session", False, time.time() - start_time)
            self.failed_operations.append({
                "operation": "invalidate_session",
                "session_id": session_id,
                "error": str(e),
                "timestamp": time.time()
            })

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize session management system"""
        try:
            self.logger.info("Starting Session Manager...")
            
            # Clear tracking data
            self.session_operations.clear()
            self.session_validations = 0
            self.session_invalidations = 0
            self.failed_operations.clear()
            
            self.logger.info("Session Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Session Manager: {e}")
            return False
    
    def _on_stop(self) -> bool:
        """Cleanup session management system"""
        try:
            self.logger.info("Stopping Session Manager...")
            
            # Save session management data
            self._save_session_management_data()
            
            self.logger.info("Session Manager stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop Session Manager: {e}")
            return False
    
    def _on_heartbeat(self) -> bool:
        """Session management health check"""
        try:
            # Check session management health
            health_status = self._check_session_management_health()
            
            # Update metrics
            self.metrics.update(
                operations_count=len(self.session_operations),
                success_rate=self._calculate_success_rate(),
                average_response_time=self._calculate_average_response_time(),
                health_status=health_status
            )
            
            return health_status == "healthy"
            
        except Exception as e:
            self.logger.error(f"Session Manager heartbeat failed: {e}")
            return False
    
    def _on_initialize_resources(self) -> bool:
        """Initialize session management resources"""
        try:
            # Initialize database connection
            self._initialize_database()
            
            # Initialize session tracking
            self.session_operations = []
            self.session_validations = 0
            self.session_invalidations = 0
            self.failed_operations = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Session Manager resources: {e}")
            return False
    
    def _on_cleanup_resources(self) -> bool:
        """Cleanup session management resources"""
        try:
            # Save session management data
            self._save_session_management_data()
            
            # Clear tracking data
            self.session_operations.clear()
            self.session_validations = 0
            self.session_invalidations = 0
            self.failed_operations.clear()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup Session Manager resources: {e}")
            return False
    
    def _on_recovery_attempt(self) -> bool:
        """Attempt to recover from errors"""
        try:
            self.logger.info("Attempting Session Manager recovery...")
            
            # Reinitialize database connection
            if self._initialize_database():
                self.logger.info("Session Manager recovery successful")
                return True
            else:
                self.logger.error("Session Manager recovery failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Session Manager recovery attempt failed: {e}")
            return False
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_session_management_data(self):
        """Save session management data for persistence"""
        try:
            data = {
                "session_validations": self.session_validations,
                "session_invalidations": self.session_invalidations,
                "failed_operations": self.failed_operations,
                "timestamp": time.time()
            }
            
            # Save to file or database as needed
            # For now, just log the data
            self.logger.info(f"Session management data: {data}")
            
        except Exception as e:
            self.logger.error(f"Failed to save session management data: {e}")
    
    def _check_session_management_health(self) -> str:
        """Check session management system health"""
        try:
            # Check if database is accessible
            conn = sqlite3.connect(self.db_file)
            conn.close()
            
            # Check if we have recent operations
            if len(self.session_operations) > 0:
                return "healthy"
            else:
                return "idle"
                
        except Exception as e:
            self.logger.error(f"Session management health check failed: {e}")
            return "unhealthy"
    
    def _calculate_success_rate(self) -> float:
        """Calculate operation success rate"""
        try:
            if len(self.session_operations) == 0:
                return 1.0
            
            successful_ops = sum(1 for op in self.session_operations if op.get("success", False))
            return successful_ops / len(self.session_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate success rate: {e}")
            return 0.0
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average operation response time"""
        try:
            if len(self.session_operations) == 0:
                return 0.0
            
            total_time = sum(op.get("duration", 0.0) for op in self.session_operations)
            return total_time / len(self.session_operations)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate average response time: {e}")
            return 0.0
    
    def _initialize_database(self) -> bool:
        """Initialize session database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create sessions table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    is_active INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    last_activity TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            
            self.logger.info("Session database initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize session database: {e}")
            return False


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
