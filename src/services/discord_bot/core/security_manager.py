#!/usr/bin/env python3
"""
Security Manager
================

Security policies and rate limiting system for Discord bot.
"""

import asyncio
import logging
import time
import hashlib
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque

import discord
from discord import app_commands

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatType(Enum):
    """Threat types."""
    RATE_LIMIT = "rate_limit"
    SPAM = "spam"
    UNAUTHORIZED = "unauthorized"
    MALICIOUS = "malicious"
    SUSPICIOUS = "suspicious"


@dataclass
class SecurityEvent:
    """Security event record."""
    id: str
    user_id: str
    event_type: ThreatType
    severity: SecurityLevel
    timestamp: float
    details: Dict[str, Any]
    action_taken: str


@dataclass
class RateLimit:
    """Rate limit configuration."""
    requests: int
    window: int  # seconds
    burst: int = 0  # burst allowance
    penalty: int = 0  # penalty seconds


class SecurityManager:
    """Security manager for Discord bot."""
    
    def __init__(self, bot):
        """Initialize security manager."""
        self.bot = bot
        self.rate_limits: Dict[str, RateLimit] = {}
        self.user_activity: Dict[str, deque] = defaultdict(lambda: deque())
        self.blocked_users: Set[str] = set()
        self.suspicious_users: Set[str] = set()
        self.security_events: List[SecurityEvent] = []
        self.security_policies: Dict[str, Any] = {}
        
        # Initialize security policies
        self._init_security_policies()
        
        # Initialize rate limits
        self._init_rate_limits()
        
        # Start security monitoring
        asyncio.create_task(self._security_monitoring_loop())
        
        logger.info("[SUCCESS] Security Manager initialized")
    
    def _init_security_policies(self):
        """Initialize security policies."""
        self.security_policies = {
            "max_commands_per_minute": 10,
            "max_commands_per_hour": 100,
            "max_failed_attempts": 5,
            "block_duration": 3600,  # 1 hour
            "suspicious_threshold": 3,
            "auto_block_enabled": True,
            "log_security_events": True,
            "notify_admins": True
        }
        logger.info("[SUCCESS] Security policies initialized")
    
    def _init_rate_limits(self):
        """Initialize rate limits."""
        self.rate_limits = {
            "global": RateLimit(requests=1000, window=3600, burst=100),  # 1000/hour, 100 burst
            "per_user": RateLimit(requests=100, window=3600, burst=10),  # 100/hour, 10 burst
            "per_command": RateLimit(requests=20, window=3600, burst=5),  # 20/hour, 5 burst
            "per_channel": RateLimit(requests=500, window=3600, burst=50),  # 500/hour, 50 burst
            "admin_commands": RateLimit(requests=50, window=3600, burst=10),  # 50/hour, 10 burst
            "devlog_commands": RateLimit(requests=30, window=3600, burst=5),  # 30/hour, 5 burst
        }
        logger.info("[SUCCESS] Rate limits initialized")
    
    async def _security_monitoring_loop(self):
        """Security monitoring loop."""
        while True:
            try:
                await self._cleanup_old_activity()
                await self._check_suspicious_activity()
                await self._update_user_ratings()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"[ERROR] Error in security monitoring: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _cleanup_old_activity(self):
        """Clean up old activity records."""
        current_time = time.time()
        cutoff_time = current_time - 3600  # Keep 1 hour of history
        
        for user_id in list(self.user_activity.keys()):
            user_activity = self.user_activity[user_id]
            
            # Remove old entries
            while user_activity and user_activity[0] < cutoff_time:
                user_activity.popleft()
            
            # Remove empty entries
            if not user_activity:
                del self.user_activity[user_id]
    
    async def _check_suspicious_activity(self):
        """Check for suspicious activity patterns."""
        current_time = time.time()
        
        for user_id, activity in self.user_activity.items():
            if len(activity) > self.security_policies["suspicious_threshold"]:
                # Check for rapid-fire commands
                recent_activity = [t for t in activity if current_time - t < 60]
                if len(recent_activity) > 10:  # More than 10 commands in 1 minute
                    await self._handle_security_threat(
                        user_id, ThreatType.SPAM, SecurityLevel.MEDIUM,
                        {"commands_in_minute": len(recent_activity)}
                    )
    
    async def _update_user_ratings(self):
        """Update user security ratings."""
        # This would implement a more sophisticated user rating system
        pass
    
    async def check_rate_limit(self, user_id: str, command_name: str, 
                             channel_id: str = None) -> bool:
        """Check if user is within rate limits."""
        current_time = time.time()
        
        # Check global rate limit
        if not await self._check_specific_rate_limit("global", user_id, current_time):
            await self._handle_security_threat(
                user_id, ThreatType.RATE_LIMIT, SecurityLevel.MEDIUM,
                {"limit_type": "global", "command": command_name}
            )
            return False
        
        # Check per-user rate limit
        if not await self._check_specific_rate_limit("per_user", user_id, current_time):
            await self._handle_security_threat(
                user_id, ThreatType.RATE_LIMIT, SecurityLevel.MEDIUM,
                {"limit_type": "per_user", "command": command_name}
            )
            return False
        
        # Check per-command rate limit
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
            await self._handle_security_threat(
                user_id, ThreatType.RATE_LIMIT, SecurityLevel.MEDIUM,
                {"limit_type": "per_command", "command": command_name}
            )
            return False
        
        # Check per-channel rate limit (if channel specified)
        if channel_id:
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
                await self._handle_security_threat(
                    user_id, ThreatType.RATE_LIMIT, SecurityLevel.MEDIUM,
                    {"limit_type": "per_channel", "command": command_name, "channel": channel_id}
                )
                return False
        
        # Check command-specific rate limits
        if command_name.startswith("admin"):
            if not await self._check_specific_rate_limit("admin_commands", user_id, current_time):
                return False
        
        if "devlog" in command_name:
            if not await self._check_specific_rate_limit("devlog_commands", user_id, current_time):
                return False
        
        # Record activity
        self.user_activity[user_id].append(current_time)
        
        return True
    
    async def _check_specific_rate_limit(self, limit_type: str, user_id: str, 
                                       current_time: float) -> bool:
        """Check specific rate limit for a user."""
        if limit_type not in self.rate_limits:
            return True
        
        limit = self.rate_limits[limit_type]
        
        # Get or create user activity record
        if not hasattr(self, '_rate_limit_records'):
            self._rate_limit_records = defaultdict(lambda: deque())
        
        user_records = self._rate_limit_records[f"{user_id}_{limit_type}"]
        
        # Remove old records outside the window
        cutoff_time = current_time - limit.window
        while user_records and user_records[0] < cutoff_time:
            user_records.popleft()
        
        # Check if within limits
        if len(user_records) >= limit.requests:
            return False
        
        # Add current request
        user_records.append(current_time)
        
        return True
    
    def _check_rate_limit(self, user_id: int, limit_type: str, 
                         current_time: float) -> bool:
        """Check specific rate limit."""
        if limit_type not in self.rate_limits:
            return True
        
        limit = self.rate_limits[limit_type]
        
        # Get or create user activity record
        if not hasattr(self, '_rate_limit_records'):
            self._rate_limit_records = defaultdict(lambda: deque())
        
# SECURITY: Key placeholder - replace with environment variable
        
        # Remove old records outside the window
        cutoff_time = current_time - limit.window
        while user_records and user_records[0] < cutoff_time:
            user_records.popleft()
        
        # Check if within limits
        if len(user_records) >= limit.requests:
            return False
        
        # Add current request
        user_records.append(current_time)
        
        return True
    
    async def _handle_security_threat(self, user_id: str, threat_type: ThreatType,
                                    severity: SecurityLevel, details: Dict[str, Any]):
        """Handle security threat."""
        event_id = hashlib.md5(f"{user_id}_{threat_type}_{time.time()}".encode()).hexdigest()[:8]
        
        event = SecurityEvent(
            id=event_id,
            user_id=user_id,
            event_type=threat_type,
            severity=severity,
            timestamp=time.time(),
            details=details,
            action_taken=""
        )
        
        # Determine action based on threat type and severity
        if threat_type == ThreatType.RATE_LIMIT:
            if severity == SecurityLevel.MEDIUM:
                event.action_taken = "rate_limit_warning"
                self.suspicious_users.add(user_id)
            elif severity == SecurityLevel.HIGH:
                event.action_taken = "temporary_block"
                await self._block_user(user_id, 300)  # 5 minutes
            elif severity == SecurityLevel.CRITICAL:
                event.action_taken = "extended_block"
                await self._block_user(user_id, 3600)  # 1 hour
        
        elif threat_type == ThreatType.SPAM:
            event.action_taken = "spam_detection"
            self.suspicious_users.add(user_id)
            if severity == SecurityLevel.HIGH:
                await self._block_user(user_id, 600)  # 10 minutes
        
        elif threat_type == ThreatType.UNAUTHORIZED:
            event.action_taken = "unauthorized_access"
            await self._block_user(user_id, 1800)  # 30 minutes
        
        elif threat_type == ThreatType.MALICIOUS:
            event.action_taken = "malicious_activity"
            await self._block_user(user_id, 7200)  # 2 hours
        
        # Record event
        self.security_events.append(event)
        
        # Log security event
        if self.security_policies["log_security_events"]:
            logger.warning(f"[ALERT] Security threat: {threat_type.value} - {user_id} - {severity.value}")
        
        # Notify admins if enabled
        if self.security_policies["notify_admins"]:
            await self._notify_admins(event)
    
    async def _block_user(self, user_id: str, duration: int):
        """Block user for specified duration."""
        self.blocked_users.add(user_id)
        
        # Schedule unblock
        asyncio.create_task(self._unblock_user_after(user_id, duration))
        
        logger.warning(f"[BLOCKED] User blocked: {user_id} for {duration} seconds")
    
    async def _unblock_user_after(self, user_id: str, duration: int):
        """Unblock user after specified duration."""
        await asyncio.sleep(duration)
        
        if user_id in self.blocked_users:
            self.blocked_users.remove(user_id)
            logger.info(f"[SUCCESS] User unblocked: {user_id}")
    
    async def _notify_admins(self, event: SecurityEvent):
        """Notify administrators of security event."""
        try:
            # This would send notification to admin channels
            logger.info(f"[NOTIFY] Admin notification: {event.event_type.value} - {event.user_id}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to notify admins: {e}")
    
    def is_user_blocked(self, user_id: str) -> bool:
        """Check if user is blocked."""
        return user_id in self.blocked_users
    
    def is_user_suspicious(self, user_id: str) -> bool:
        """Check if user is marked as suspicious."""
        return user_id in self.suspicious_users
    
    async def get_security_stats(self) -> Dict[str, Any]:
        """Get security statistics."""
        current_time = time.time()
        recent_events = [e for e in self.security_events if current_time - e.timestamp < 3600]
        
        return {
            "total_events": len(self.security_events),
            "recent_events": len(recent_events),
            "blocked_users": len(self.blocked_users),
            "suspicious_users": len(self.suspicious_users),
            "active_users": len(self.user_activity),
            "threat_types": {
                threat_type.value: len([e for e in recent_events if e.event_type == threat_type])
                for threat_type in ThreatType
            },
            "severity_levels": {
                severity.value: len([e for e in recent_events if e.severity == severity])
                for severity in SecurityLevel
            }
        }
    
    async def create_security_embed(self) -> discord.Embed:
        """Create Discord embed for security status."""
        stats = await self.get_security_stats()
        
        embed = discord.Embed(
            title="🛡️ Security Status",
            color=discord.Color.red() if stats["blocked_users"] > 0 else discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(
            name="Blocked Users",
            value=str(stats["blocked_users"]),
            inline=True
        )
        embed.add_field(
            name="Suspicious Users",
            value=str(stats["suspicious_users"]),
            inline=True
        )
        embed.add_field(
            name="Active Users",
            value=str(stats["active_users"]),
            inline=True
        )
        
        embed.add_field(
            name="Recent Events (1h)",
            value=str(stats["recent_events"]),
            inline=True
        )
        embed.add_field(
            name="Total Events",
            value=str(stats["total_events"]),
            inline=True
        )
        
        if stats["recent_events"] > 0:
            threat_summary = "\n".join([
                f"{threat}: {count}" for threat, count in stats["threat_types"].items() if count > 0
            ])
            embed.add_field(
                name="Recent Threats",
                value=threat_summary or "None",
                inline=False
            )
        
        embed.set_footer(text="🐝 WE ARE SWARM - Security Manager")
        return embed
