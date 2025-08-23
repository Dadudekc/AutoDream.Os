#!/usr/bin/env python3
"""
Security Monitoring and Access Control Systems
Real-time security monitoring, logging, and access management
"""

import time
import json
import logging
import hashlib
import hmac
import secrets
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import sqlite3
import os


@dataclass
class SecurityLogEntry:
    """Security log entry structure"""

    timestamp: float
    event_type: str
    source_ip: str
    user: str
    success: bool
    details: Dict
    session_id: Optional[str] = None
    severity: str = "info"


@dataclass
class SecurityAlert:
    """Security alert structure"""

    level: str
    message: str
    source: str
    acknowledged: bool
    timestamp: float
    incident_id: Optional[str] = None
    assigned_to: Optional[str] = None


@dataclass
class UserSession:
    """User session information"""

    session_id: str
    user_id: str
    is_active: bool
    created_at: float
    last_activity: float
    ip_address: str
    user_agent: str


@dataclass
class AuthenticationResult:
    """Authentication result structure"""

    success: bool
    user_id: Optional[str]
    session_id: Optional[str] = None
    error_message: Optional[str] = None


class SecurityMonitor:
    """Real-time security monitoring system"""

    def __init__(self, log_file: str = "security.log", db_file: str = "security.db"):
        self.logger = logging.getLogger(__name__)
        self.log_file = log_file
        self.db_file = db_file
        self.is_monitoring = False
        self.monitoring_thread = None
        self.alert_thresholds = {
            "failed_logins": 5,
            "suspicious_ips": 10,
            "unusual_activity": 3,
        }
        self.monitoring_stats = {
            "events_processed": 0,
            "alerts_generated": 0,
            "incidents_created": 0,
        }

        # Initialize database
        self._init_database()

    def start_monitoring(self):
        """Start real-time security monitoring"""
        if self.is_monitoring:
            self.logger.warning("Security monitoring already active")
            return

        try:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop, daemon=True
            )
            self.monitoring_thread.start()

            self.logger.info("Security monitoring started successfully")

        except Exception as e:
            self.logger.error(f"Failed to start security monitoring: {e}")
            self.is_monitoring = False

    def stop_monitoring(self):
        """Stop security monitoring"""
        if not self.is_monitoring:
            return

        try:
            self.is_monitoring = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=5)

            self.logger.info("Security monitoring stopped")

        except Exception as e:
            self.logger.error(f"Error stopping security monitoring: {e}")

    def log_security_event(
        self,
        event_type: str,
        source_ip: str,
        user: str,
        success: bool,
        details: Dict = None,
        session_id: str = None,
        severity: str = "info",
    ) -> Dict:
        """Log security event to database and file"""
        try:
            timestamp = time.time()
            details = details or {}

            # Create log entry
            log_entry = SecurityLogEntry(
                timestamp=timestamp,
                event_type=event_type,
                source_ip=source_ip,
                user=user,
                success=success,
                details=details,
                session_id=session_id,
                severity=severity,
            )

            # Log to file
            self._write_log_to_file(log_entry)

            # Store in database
            self._store_log_in_database(log_entry)

            # Update monitoring stats
            self.monitoring_stats["events_processed"] += 1

            # Check for alert conditions
            self._check_alert_conditions(log_entry)

            return asdict(log_entry)

        except Exception as e:
            self.logger.error(f"Failed to log security event: {e}")
            return {}

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Process pending alerts
                self._process_pending_alerts()

                # Update threat intelligence
                self._update_threat_intelligence()

                # Generate security reports
                self._generate_security_reports()

                # Sleep for monitoring interval
                time.sleep(30)  # 30 second monitoring interval

            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error

    def _init_database(self):
        """Initialize security database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Create security logs table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS security_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    event_type TEXT NOT NULL,
                    source_ip TEXT NOT NULL,
                    user TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    details TEXT,
                    session_id TEXT,
                    severity TEXT DEFAULT 'info'
                )
            """
            )

            # Create security alerts table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS security_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    source TEXT NOT NULL,
                    acknowledged BOOLEAN DEFAULT FALSE,
                    timestamp REAL NOT NULL,
                    incident_id TEXT,
                    assigned_to TEXT
                )
            """
            )

            # Create user sessions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at REAL NOT NULL,
                    last_activity REAL NOT NULL,
                    ip_address TEXT NOT NULL,
                    user_agent TEXT
                )
            """
            )

            # Create indexes for performance
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON security_logs(timestamp)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_logs_event_type ON security_logs(event_type)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_logs_source_ip ON security_logs(source_ip)"
            )

            conn.commit()
            conn.close()

            self.logger.info("Security database initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize security database: {e}")

    def _write_log_to_file(self, log_entry: SecurityLogEntry):
        """Write log entry to file"""
        try:
            timestamp_str = datetime.fromtimestamp(log_entry.timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            log_line = f"{timestamp_str} | {log_entry.severity.upper()} | {log_entry.event_type} | {log_entry.source_ip} | {log_entry.user} | {'SUCCESS' if log_entry.success else 'FAILURE'}\n"

            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line)

        except Exception as e:
            self.logger.error(f"Failed to write log to file: {e}")

    def _store_log_in_database(self, log_entry: SecurityLogEntry):
        """Store log entry in database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO security_logs
                (timestamp, event_type, source_ip, user, success, details, session_id, severity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    log_entry.timestamp,
                    log_entry.event_type,
                    log_entry.source_ip,
                    log_entry.user,
                    log_entry.success,
                    json.dumps(log_entry.details),
                    log_entry.session_id,
                    log_entry.severity,
                ),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Failed to store log in database: {e}")

    def _check_alert_conditions(self, log_entry: SecurityLogEntry):
        """Check if log entry triggers alert conditions"""
        try:
            # Check for failed login attempts
            if log_entry.event_type == "login_attempt" and not log_entry.success:
                self._check_failed_login_alert(log_entry)

            # Check for suspicious IP activity
            self._check_suspicious_ip_alert(log_entry)

            # Check for unusual activity patterns
            self._check_unusual_activity_alert(log_entry)

        except Exception as e:
            self.logger.error(f"Alert condition check failed: {e}")

    def _check_failed_login_alert(self, log_entry: SecurityLogEntry):
        """Check for failed login alert conditions"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Count failed logins for this IP in the last hour
            one_hour_ago = time.time() - 3600
            cursor.execute(
                """
                SELECT COUNT(*) FROM security_logs
                WHERE event_type = 'login_attempt'
                AND success = FALSE
                AND source_ip = ?
                AND timestamp > ?
            """,
                (log_entry.source_ip, one_hour_ago),
            )

            failed_count = cursor.fetchone()[0]
            conn.close()

            if failed_count >= self.alert_thresholds["failed_logins"]:
                alert = SecurityAlert(
                    level="high",
                    message=f"Multiple failed login attempts from {log_entry.source_ip}",
                    source="security_monitor",
                    acknowledged=False,
                    timestamp=time.time(),
                )

                self._create_security_alert(alert)

        except Exception as e:
            self.logger.error(f"Failed login alert check failed: {e}")

    def _check_suspicious_ip_alert(self, log_entry: SecurityLogEntry):
        """Check for suspicious IP activity"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Count events from this IP in the last hour
            one_hour_ago = time.time() - 3600
            cursor.execute(
                """
                SELECT COUNT(*) FROM security_logs
                WHERE source_ip = ?
                AND timestamp > ?
            """,
                (log_entry.source_ip, one_hour_ago),
            )

            event_count = cursor.fetchone()[0]
            conn.close()

            if event_count >= self.alert_thresholds["suspicious_ips"]:
                alert = SecurityAlert(
                    level="medium",
                    message=f"High activity from suspicious IP {log_entry.source_ip}",
                    source="security_monitor",
                    acknowledged=False,
                    timestamp=time.time(),
                )

                self._create_security_alert(alert)

        except Exception as e:
            self.logger.error(f"Suspicious IP alert check failed: {e}")

    def _check_unusual_activity_alert(self, log_entry: SecurityLogEntry):
        """Check for unusual activity patterns"""
        try:
            # Check for off-hours activity
            current_hour = datetime.fromtimestamp(log_entry.timestamp).hour
            if current_hour < 6 or current_hour > 22:
                alert = SecurityAlert(
                    level="low",
                    message=f"Off-hours activity detected from {log_entry.source_ip}",
                    source="security_monitor",
                    acknowledged=False,
                    timestamp=time.time(),
                )

                self._create_security_alert(alert)

        except Exception as e:
            self.logger.error(f"Unusual activity alert check failed: {e}")

    def _create_security_alert(self, alert: SecurityAlert):
        """Create and store security alert"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO security_alerts
                (level, message, source, acknowledged, timestamp, incident_id, assigned_to)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    alert.level,
                    alert.message,
                    alert.source,
                    alert.acknowledged,
                    alert.timestamp,
                    alert.incident_id,
                    alert.assigned_to,
                ),
            )

            conn.commit()
            conn.close()

            self.monitoring_stats["alerts_generated"] += 1
            self.logger.warning(f"Security alert created: {alert.message}")

        except Exception as e:
            self.logger.error(f"Failed to create security alert: {e}")

    def _process_pending_alerts(self):
        """Process pending security alerts"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Get unacknowledged alerts
            cursor.execute(
                """
                SELECT * FROM security_alerts
                WHERE acknowledged = FALSE
                ORDER BY timestamp DESC
            """
            )

            alerts = cursor.fetchall()
            conn.close()

            # Process each alert (in production, this would trigger notifications)
            for alert in alerts:
                self.logger.info(f"Processing alert: {alert[2]}")  # alert[2] is message

        except Exception as e:
            self.logger.error(f"Failed to process pending alerts: {e}")

    def _update_threat_intelligence(self):
        """Update threat intelligence feeds"""
        # This would integrate with external threat intelligence services
        pass

    def _generate_security_reports(self):
        """Generate periodic security reports"""
        # This would generate daily/weekly security reports
        pass


class AlertSystem:
    """Security alert management system"""

    def __init__(self, db_file: str = "security.db"):
        self.logger = logging.getLogger(__name__)
        self.db_file = db_file

    def create_alert(
        self,
        level: str,
        message: str,
        source: str,
        incident_id: str = None,
        assigned_to: str = None,
    ) -> Dict:
        """Create a new security alert"""
        try:
            alert = SecurityAlert(
                level=level,
                message=message,
                source=source,
                acknowledged=False,
                timestamp=time.time(),
                incident_id=incident_id,
                assigned_to=assigned_to,
            )

            # Store alert in database
            self._store_alert(alert)

            # Log alert creation
            self.logger.warning(f"Security alert created: {message}")

            return asdict(alert)

        except Exception as e:
            self.logger.error(f"Failed to create alert: {e}")
            return {}

    def acknowledge_alert(self, alert_id: int, user: str) -> bool:
        """Acknowledge a security alert"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE security_alerts
                SET acknowledged = TRUE, assigned_to = ?
                WHERE id = ?
            """,
                (user, alert_id),
            )

            conn.commit()
            conn.close()

            self.logger.info(f"Alert {alert_id} acknowledged by {user}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to acknowledge alert: {e}")
            return False

    def get_active_alerts(self, level: str = None) -> List[Dict]:
        """Get active (unacknowledged) alerts"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            if level:
                cursor.execute(
                    """
                    SELECT * FROM security_alerts
                    WHERE acknowledged = FALSE AND level = ?
                    ORDER BY timestamp DESC
                """,
                    (level,),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM security_alerts
                    WHERE acknowledged = FALSE
                    ORDER BY timestamp DESC
                """
                )

            alerts = cursor.fetchall()
            conn.close()

            # Convert to list of dictionaries
            alert_list = []
            for alert in alerts:
                alert_dict = {
                    "id": alert[0],
                    "level": alert[1],
                    "message": alert[2],
                    "source": alert[3],
                    "acknowledged": bool(alert[4]),
                    "timestamp": alert[5],
                    "incident_id": alert[6],
                    "assigned_to": alert[7],
                }
                alert_list.append(alert_dict)

            return alert_list

        except Exception as e:
            self.logger.error(f"Failed to get active alerts: {e}")
            return []

    def _store_alert(self, alert: SecurityAlert):
        """Store alert in database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO security_alerts
                (level, message, source, acknowledged, timestamp, incident_id, assigned_to)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    alert.level,
                    alert.message,
                    alert.source,
                    alert.acknowledged,
                    alert.timestamp,
                    alert.incident_id,
                    alert.assigned_to,
                ),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Failed to store alert: {e}")


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

            # Update user last login
            cursor.execute(
                """
                UPDATE users SET last_login = ? WHERE username = ?
            """,
                (current_time, username),
            )

            conn.commit()
            conn.close()

            self.logger.info(f"Session created for user {username}")
            return session_id

        except Exception as e:
            self.logger.error(f"Failed to create user session: {e}")
            return None

    def _log_authentication_event(
        self, username: str, source_ip: str, success: bool, user_agent: str = None
    ):
        """Log authentication event"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO auth_logs (username, source_ip, success, timestamp, user_agent)
                VALUES (?, ?, ?, ?, ?)
            """,
                (username, source_ip, success, time.time(), user_agent),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"Failed to log authentication event: {e}")

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

            if result and result[0]:
                return time.time() < result[0]

            return False

        except Exception as e:
            self.logger.error(f"Lockout check failed: {e}")
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

            if result:
                failed_attempts = result[0] + 1

                if failed_attempts >= self.max_login_attempts:
                    # Lock account
                    lockout_until = time.time() + self.lockout_duration
                    cursor.execute(
                        """
                        UPDATE users
                        SET failed_attempts = ?, locked_until = ?
                        WHERE username = ?
                    """,
                        (failed_attempts, lockout_until, username),
                    )

                    self.logger.warning(
                        f"User {username} account locked due to failed attempts"
                    )
                else:
                    # Increment failed attempts
                    cursor.execute(
                        """
                        UPDATE users SET failed_attempts = ? WHERE username = ?
                    """,
                        (failed_attempts, username),
                    )

                conn.commit()

            conn.close()

        except Exception as e:
            self.logger.error(f"Lockout condition check failed: {e}")


class RoleBasedAccessControl:
    """Role-based access control system"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.roles = {
            "admin": {
                "permissions": ["read", "write", "delete", "admin"],
                "resources": ["*"],
            },
            "user": {
                "permissions": ["read"],
                "resources": ["user_data", "public_data"],
            },
            "analyst": {
                "permissions": ["read", "write"],
                "resources": ["analytics", "reports"],
            },
        }

    def check_access(self, user: str, resource: str, permission: str) -> bool:
        """Check if user has access to resource with specified permission"""
        try:
            # Get user role (in production, this would query user database)
            user_role = self._get_user_role(user)

            if not user_role:
                return False

            role_config = self.roles.get(user_role)
            if not role_config:
                return False

            # Check if user has the required permission
            if permission not in role_config["permissions"]:
                return False

            # Check if user has access to the resource
            if "*" in role_config["resources"]:
                return True

            if resource in role_config["resources"]:
                return True

            return False

        except Exception as e:
            self.logger.error(f"Access control check failed: {e}")
            return False

    def _get_user_role(self, user: str) -> str:
        """Get user role (simplified for testing)"""
        # In production, this would query user database
        if user == "admin":
            return "admin"
        elif user == "analyst":
            return "analyst"
        else:
            return "user"


class SessionManager:
    """User session management system"""

    def __init__(self, db_file: str = "security.db"):
        self.logger = logging.getLogger(__name__)
        self.db_file = db_file
        self.session_timeout = 3600  # 1 hour

    def create_session(self, user_id: str) -> UserSession:
        """Create new user session"""
        try:
            session_id = secrets.token_urlsafe(32)
            current_time = time.time()

            # Create session object
            session = UserSession(
                session_id=session_id,
                user_id=user_id,
                is_active=True,
                created_at=current_time,
                last_activity=current_time,
                ip_address="127.0.0.1",  # Would be actual IP in production
                user_agent="test-agent",  # Would be actual user agent in production
            )

            # Store in database
            self._store_session(session)

            self.logger.info(f"Session created for user {user_id}")
            return session

        except Exception as e:
            self.logger.error(f"Failed to create session: {e}")
            return None

    def invalidate_session(self, session_id: str):
        """Invalidate user session"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE user_sessions
                SET is_active = FALSE
                WHERE session_id = ?
            """,
                (session_id,),
            )

            conn.commit()
            conn.close()

            self.logger.info(f"Session {session_id} invalidated")

        except Exception as e:
            self.logger.error(f"Failed to invalidate session: {e}")

    def _store_session(self, session: UserSession):
        """Store session in database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO user_sessions
                (session_id, user_id, is_active, created_at, last_activity, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
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

        except Exception as e:
            self.logger.error(f"Failed to store session: {e}")


# Export main classes
__all__ = [
    "SecurityMonitor",
    "AlertSystem",
    "AuthenticationSystem",
    "RoleBasedAccessControl",
    "SessionManager",
    "SecurityLogEntry",
    "SecurityAlert",
    "UserSession",
    "AuthenticationResult",
]
