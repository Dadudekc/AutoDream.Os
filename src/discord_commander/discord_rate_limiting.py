import logging

logger = logging.getLogger(__name__)
"""
Discord Rate Limiting - V2 Compliant Module
===========================================

Rate limiting and throttling for Discord Agent Bot.
V2 COMPLIANT: Rate limiting logic under 100 lines.

Features:
- Global rate limiting
- User-specific cooldowns
- Command throttling
- Performance monitoring

Author: Agent-3 (Quality Assurance Co-Captain) - V2 Refactoring
License: MIT
"""
import time
from typing import Any

try:
    from .rate_limits import RateLimiter
except ImportError as e:
    logger.info(f"⚠️ Import warning: {e}")
    RateLimiter = None


class DiscordRateLimiter:
    """Rate limiting and throttling for Discord Agent Bot."""

    def __init__(self, bot):
        """Initialize rate limiter."""
        self.bot = bot
        global_rate = int(os.getenv("RATE_LIMIT_GLOBAL_PER_SEC", "5"))
        user_cooldown = int(os.getenv("RATE_LIMIT_USER_COOLDOWN_SEC", "2"))
        if RateLimiter:
            self.rate_limiter = RateLimiter(global_rate, user_cooldown)
        else:
            self.rate_limiter = None
        self.user_last_command: dict[int, float] = {}
        self.global_command_count = 0
        self.global_window_start = time.time()
        self.max_global_commands = global_rate
        self.user_cooldown_seconds = user_cooldown

    async def acquire(self, user_id: int) -> bool:
        """Acquire rate limit permission for user."""
        if self.rate_limiter:
            try:
                await self.rate_limiter.acquire(user_id)
                return True
            except Exception:
                return False
        else:
            return self._fallback_acquire(user_id)

    def release(self):
        """Release rate limit permission."""
        if self.rate_limiter:
            try:
                self.rate_limiter.release()
            except Exception:
                pass

    def _fallback_acquire(self, user_id: int) -> bool:
        """Fallback rate limiting implementation."""
        current_time = time.time()
        if current_time - self.global_window_start >= 1.0:
            self.global_command_count = 0
            self.global_window_start = current_time
        if self.global_command_count >= self.max_global_commands:
            return False
        if user_id in self.user_last_command:
            time_since_last = current_time - self.user_last_command[user_id]
            if time_since_last < self.user_cooldown_seconds:
                return False
        self.user_last_command[user_id] = current_time
        self.global_command_count += 1
        return True

    def get_rate_limit_status(self) -> dict[str, Any]:
        """Get current rate limiting status."""
        current_time = time.time()
        if self.rate_limiter:
            return {
                "rate_limiter_available": True,
                "global_commands_remaining": self.max_global_commands - self.global_command_count,
                "window_reset_in": 1.0 - (current_time - self.global_window_start),
            }
        else:
            return {
                "rate_limiter_available": False,
                "fallback_mode": True,
                "global_commands_remaining": self.max_global_commands - self.global_command_count,
                "window_reset_in": 1.0 - (current_time - self.global_window_start),
                "active_users": len(self.user_last_command),
            }

    def reset_user_cooldown(self, user_id: int):
        """Reset cooldown for specific user."""
        if user_id in self.user_last_command:
            del self.user_last_command[user_id]

    def reset_all_cooldowns(self):
        """Reset all user cooldowns."""
        self.user_last_command.clear()
        self.global_command_count = 0
        self.global_window_start = time.time()
