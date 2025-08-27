import logging
import hashlib
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

from .models import User
from src.session_management.session_manager import SessionManager
from src.session_management.backends import SessionData, SQLiteSessionBackend
from ..core.base_manager import BaseManager


class AuthenticationManager(BaseManager):
    """Manages user authentication and account security"""

    def __init__(self, db_file: str = "security.db"):
        super().__init__(
            manager_id="authentication_manager",
            name="Authentication Manager",
            description="Manages user authentication and security",
        )
        self.db_file = db_file
        self.max_failed_attempts = 5
        self.lockout_duration = 900  # 15 minutes
        self.session_timeout = 3600  # 1 hour
        self.session_manager = SessionManager(
            SQLiteSessionBackend(db_file, self.logger),
            self.session_timeout,
            self.logger,
        )
        self.failed_login_attempts: Dict[str, int] = {}
        self.locked_accounts: Dict[str, str] = {}
        self.logger.info("Authentication Manager initialized")

    # ------------------------------------------------------------------
    # BaseManager hooks
    # ------------------------------------------------------------------
    def _on_start(self) -> bool:
        try:
            if not self._initialize_database():
                return False
            self.failed_login_attempts.clear()
            self.locked_accounts.clear()
            self.session_manager.invalidate_all_sessions()
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Authentication Manager: {e}")
            return False

    def _on_stop(self):
        try:
            self.session_manager.invalidate_all_sessions()
            self.failed_login_attempts.clear()
            self.locked_accounts.clear()
        except Exception as e:
            self.logger.error(f"Failed to stop Authentication Manager: {e}")

    def _on_heartbeat(self):
        try:
            self.session_manager.cleanup_expired_sessions()
            self._check_locked_accounts()
            self.record_operation("heartbeat", True, 0.0)
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)

    def _on_initialize_resources(self) -> bool:
        self.failed_login_attempts = {}
        self.locked_accounts = {}
        return True

    def _on_cleanup_resources(self):
        self.failed_login_attempts.clear()
        self.locked_accounts.clear()

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        try:
            self.failed_login_attempts.clear()
            self.locked_accounts.clear()
            return self._initialize_database()
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def authenticate_user(
        self,
        username: str,
        password: str,
        ip_address: str = "",
        user_agent: str = "",
    ) -> Optional[str]:
        try:
            if self._is_account_locked(username):
                return None

            user = self._get_user_by_username(username)
            if not user or not self._verify_password(password, user.password_hash):
                self._record_failed_attempt(username)
                return None

            self._reset_failed_attempts(username)
            session = self.session_manager.create_session(
                user.user_id, ip_address, user_agent
            )
            self._update_last_login(user.user_id)
            self.record_operation("authenticate_user", True, 0.0)
            return session.session_id
        except Exception as e:
            self.logger.error(f"Authentication failed for {username}: {e}")
            self.record_operation("authenticate_user", False, 0.0)
            return None

    def validate_session(self, session_id: str) -> Optional[SessionData]:
        session = self.session_manager.validate_session(session_id)
        self.record_operation("validate_session", session is not None, 0.0)
        return session

    def invalidate_session(self, session_id: str) -> bool:
        success = self.session_manager.invalidate_session(session_id)
        self.record_operation("invalidate_session", success, 0.0)
        return success

    def create_user(self, username: str, email: str, password: str, role: str = "user") -> bool:
        try:
            if self._get_user_by_username(username):
                return False
            password_hash = self._hash_password(password)
            user = User(
                user_id=f"user_{int(time.time())}",
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                is_active=True,
                created_at=datetime.now().isoformat(),
            )
            success = self._save_user_to_db(user)
            self.record_operation("create_user", success, 0.0)
            return success
        except Exception as e:
            self.logger.error(f"Failed to create user {username}: {e}")
            self.record_operation("create_user", False, 0.0)
            return False

    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        user = self._get_user_by_id(user_id)
        if not user:
            return None
        self.record_operation("get_user_info", True, 0.0)
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "last_login": user.last_login,
            "failed_attempts": user.failed_attempts,
        }

    def get_active_sessions_count(self) -> int:
        return len(self.session_manager.active_sessions)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _initialize_database(self) -> bool:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                """
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
                """
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            return False

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        return self._hash_password(password) == password_hash

    def _get_user_by_username(self, username: str) -> Optional[User]:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, username, email, password_hash, role, is_active, created_at, last_login, failed_attempts, locked_until FROM users WHERE username = ?",
                (username,),
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
                    locked_until=result[9],
                )
            return None
        except Exception as e:
            self.logger.error(f"Failed to get user by username {username}: {e}")
            return None

    def _get_user_by_id(self, user_id: str) -> Optional[User]:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, username, email, password_hash, role, is_active, created_at, last_login, failed_attempts, locked_until FROM users WHERE user_id = ?",
                (user_id,),
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
                    locked_until=result[9],
                )
            return None
        except Exception as e:
            self.logger.error(f"Failed to get user by ID {user_id}: {e}")
            return None

    def _save_user_to_db(self, user: User) -> bool:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (user_id, username, email, password_hash, role, is_active, created_at, last_login, failed_attempts, locked_until) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    user.user_id,
                    user.username,
                    user.email,
                    user.password_hash,
                    user.role,
                    user.is_active,
                    user.created_at,
                    user.last_login,
                    user.failed_attempts,
                    user.locked_until,
                ),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.logger.error(f"Failed to save user to database: {e}")
            return False

    def _record_failed_attempt(self, username: str):
        if username not in self.failed_login_attempts:
            self.failed_login_attempts[username] = 0
        self.failed_login_attempts[username] += 1
        if self.failed_login_attempts[username] >= self.max_failed_attempts:
            self._lock_account(username)

    def _reset_failed_attempts(self, username: str):
        if username in self.failed_login_attempts:
            del self.failed_login_attempts[username]
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE username = ?",
            (username,),
        )
        conn.commit()
        conn.close()

    def _lock_account(self, username: str):
        lock_until = datetime.now() + timedelta(seconds=self.lockout_duration)
        lock_until_str = lock_until.isoformat()
        self.locked_accounts[username] = lock_until_str
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET locked_until = ? WHERE username = ?",
            (lock_until_str, username),
        )
        conn.commit()
        conn.close()

    def _is_account_locked(self, username: str) -> bool:
        if username in self.locked_accounts:
            lock_until = datetime.fromisoformat(self.locked_accounts[username])
            if datetime.now() < lock_until:
                return True
            del self.locked_accounts[username]
        user = self._get_user_by_username(username)
        if user and user.locked_until:
            lock_until = datetime.fromisoformat(user.locked_until)
            if datetime.now() < lock_until:
                self.locked_accounts[username] = user.locked_until
                return True
            self._clear_account_lock(username)
        return False

    def _clear_account_lock(self, username: str):
        if username in self.locked_accounts:
            del self.locked_accounts[username]
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET locked_until = NULL WHERE username = ?",
            (username,),
        )
        conn.commit()
        conn.close()

    def _update_last_login(self, user_id: str):
        current_time = datetime.now().isoformat()
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET last_login = ? WHERE user_id = ?",
            (current_time, user_id),
        )
        conn.commit()
        conn.close()

    def _check_locked_accounts(self):
        unlocked = [u for u, t in list(self.locked_accounts.items()) if datetime.now() >= datetime.fromisoformat(t)]
        for username in unlocked:
            del self.locked_accounts[username]
            self._clear_account_lock(username)


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
        try:
            if user_role in self.roles:
                return action in self.roles[user_role]
            return False
        except Exception as e:
            self.logger.error(f"Permission check failed: {e}")
            return False

    def get_user_permissions(self, user_role: str) -> list:
        try:
            return self.roles.get(user_role, [])
        except Exception as e:
            self.logger.error(f"Failed to get user permissions: {e}")
            return []
