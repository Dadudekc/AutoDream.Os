#!/usr/bin/env python3
"""
Thea Error Recovery System - Robust Error Handling and Recovery
===============================================================

Comprehensive error recovery system for Thea autonomous operations.
Handles various failure scenarios and implements recovery strategies.

Features:
- Automatic session recovery
- Cookie validation and refresh
- Browser restart capabilities
- Network error handling
- Rate limiting and backoff
- Comprehensive error logging

Usage:
    from src.services.thea.thea_error_recovery import TheaErrorRecovery
    
    recovery = TheaErrorRecovery()
    success = recovery.handle_error(error, context)
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Types of errors that can occur in Thea operations."""
    BROWSER_INIT_FAILED = "browser_init_failed"
    COOKIE_INVALID = "cookie_invalid"
    NETWORK_ERROR = "network_error"
    ELEMENT_NOT_FOUND = "element_not_found"
    TIMEOUT_ERROR = "timeout_error"
    RATE_LIMITED = "rate_limited"
    SESSION_EXPIRED = "session_expired"
    UNKNOWN_ERROR = "unknown_error"


class RecoveryStrategy(Enum):
    """Recovery strategies for different error types."""
    RESTART_BROWSER = "restart_browser"
    REFRESH_COOKIES = "refresh_cookies"
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    CLEAR_SESSION = "clear_session"
    WAIT_AND_RETRY = "wait_and_retry"
    FALLBACK_MODE = "fallback_mode"


class TheaErrorRecovery:
    """Comprehensive error recovery system for Thea operations."""
    
    def __init__(self, 
                 max_retries: int = 3,
                 base_delay: int = 5,
                 max_delay: int = 60,
                 backoff_multiplier: float = 2.0):
        """
        Initialize the error recovery system.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay between retries (seconds)
            max_delay: Maximum delay between retries (seconds)
            backoff_multiplier: Multiplier for exponential backoff
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_multiplier = backoff_multiplier
        
        # Error tracking
        self.error_history: List[Dict[str, Any]] = []
        self.recovery_attempts: Dict[str, int] = {}
        
        # Rate limiting
        self.last_request_time = None
        self.min_request_interval = 2.0  # Minimum seconds between requests
        
        # Recovery strategies mapping
        self.strategy_mapping = {
            ErrorType.BROWSER_INIT_FAILED: RecoveryStrategy.RESTART_BROWSER,
            ErrorType.COOKIE_INVALID: RecoveryStrategy.REFRESH_COOKIES,
            ErrorType.NETWORK_ERROR: RecoveryStrategy.RETRY_WITH_BACKOFF,
            ErrorType.ELEMENT_NOT_FOUND: RecoveryStrategy.RETRY_WITH_BACKOFF,
            ErrorType.TIMEOUT_ERROR: RecoveryStrategy.WAIT_AND_RETRY,
            ErrorType.RATE_LIMITED: RecoveryStrategy.WAIT_AND_RETRY,
            ErrorType.SESSION_EXPIRED: RecoveryStrategy.CLEAR_SESSION,
            ErrorType.UNKNOWN_ERROR: RecoveryStrategy.RETRY_WITH_BACKOFF,
        }
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup error recovery logging."""
        log_dir = Path("logs/thea_recovery")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"thea_recovery_{timestamp}.log"
        
        recovery_logger = logging.getLogger("thea_recovery")
        recovery_logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        recovery_logger.addHandler(handler)
        
        self.recovery_logger = recovery_logger
    
    def classify_error(self, error: Exception, context: Dict[str, Any]) -> ErrorType:
        """
        Classify an error to determine the appropriate recovery strategy.
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
            
        Returns:
            ErrorType classification
        """
        error_str = str(error).lower()
        error_type = type(error).__name__
        
        # Browser initialization errors
        if any(keyword in error_str for keyword in ['browser', 'driver', 'selenium', 'chrome']):
            if 'init' in error_str or 'start' in error_str:
                return ErrorType.BROWSER_INIT_FAILED
        
        # Cookie-related errors
        if any(keyword in error_str for keyword in ['cookie', 'session', 'auth', 'login']):
            return ErrorType.COOKIE_INVALID
        
        # Network errors
        if any(keyword in error_str for keyword in ['network', 'connection', 'timeout', 'unreachable']):
            return ErrorType.NETWORK_ERROR
        
        # Element not found errors
        if any(keyword in error_str for keyword in ['element', 'selector', 'not found', 'no such']):
            return ErrorType.ELEMENT_NOT_FOUND
        
        # Timeout errors
        if 'timeout' in error_str or 'TimeoutException' in error_type:
            return ErrorType.TIMEOUT_ERROR
        
        # Rate limiting
        if any(keyword in error_str for keyword in ['rate', 'limit', 'too many', '429']):
            return ErrorType.RATE_LIMITED
        
        # Session expired
        if any(keyword in error_str for keyword in ['expired', 'invalid session', 'unauthorized']):
            return ErrorType.SESSION_EXPIRED
        
        return ErrorType.UNKNOWN_ERROR
    
    def handle_error(self, 
                    error: Exception, 
                    context: Dict[str, Any],
                    thea_system=None) -> bool:
        """
        Handle an error and attempt recovery.
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
            thea_system: TheaAutonomousSystem instance for recovery
            
        Returns:
            True if recovery was successful, False otherwise
        """
        error_type = self.classify_error(error, context)
        strategy = self.strategy_mapping.get(error_type, RecoveryStrategy.RETRY_WITH_BACKOFF)
        
        # Log the error
        self._log_error(error, error_type, context)
        
        # Check if we've exceeded max retries for this error type
        error_key = f"{error_type.value}_{context.get('operation', 'unknown')}"
        if self.recovery_attempts.get(error_key, 0) >= self.max_retries:
            self.recovery_logger.error(f"Max retries exceeded for {error_key}")
            return False
        
        # Increment recovery attempts
        self.recovery_attempts[error_key] = self.recovery_attempts.get(error_key, 0) + 1
        
        # Execute recovery strategy
        success = self._execute_recovery_strategy(strategy, error, context, thea_system)
        
        if success:
            self.recovery_logger.info(f"Recovery successful for {error_type.value}")
            # Reset recovery attempts on success
            self.recovery_attempts[error_key] = 0
        else:
            self.recovery_logger.error(f"Recovery failed for {error_type.value}")
        
        return success
    
    def _log_error(self, error: Exception, error_type: ErrorType, context: Dict[str, Any]):
        """Log error details for analysis."""
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type.value,
            "error_message": str(error),
            "error_class": type(error).__name__,
            "context": context,
            "recovery_attempts": self.recovery_attempts.copy()
        }
        
        self.error_history.append(error_record)
        self.recovery_logger.error(f"Error occurred: {error_type.value} - {error}")
    
    def _execute_recovery_strategy(self, 
                                 strategy: RecoveryStrategy,
                                 error: Exception,
                                 context: Dict[str, Any],
                                 thea_system=None) -> bool:
        """
        Execute the appropriate recovery strategy.
        
        Args:
            strategy: Recovery strategy to execute
            error: Original error
            context: Error context
            thea_system: TheaAutonomousSystem instance
            
        Returns:
            True if recovery successful, False otherwise
        """
        self.recovery_logger.info(f"Executing recovery strategy: {strategy.value}")
        
        try:
            if strategy == RecoveryStrategy.RESTART_BROWSER:
                return self._restart_browser(thea_system)
            
            elif strategy == RecoveryStrategy.REFRESH_COOKIES:
                return self._refresh_cookies(thea_system)
            
            elif strategy == RecoveryStrategy.RETRY_WITH_BACKOFF:
                return self._retry_with_backoff(context)
            
            elif strategy == RecoveryStrategy.CLEAR_SESSION:
                return self._clear_session(thea_system)
            
            elif strategy == RecoveryStrategy.WAIT_AND_RETRY:
                return self._wait_and_retry(context)
            
            elif strategy == RecoveryStrategy.FALLBACK_MODE:
                return self._fallback_mode(thea_system)
            
            else:
                self.recovery_logger.error(f"Unknown recovery strategy: {strategy}")
                return False
                
        except Exception as recovery_error:
            self.recovery_logger.error(f"Recovery strategy failed: {recovery_error}")
            return False
    
    def _restart_browser(self, thea_system) -> bool:
        """Restart the browser and reinitialize the system."""
        if not thea_system:
            return False
        
        try:
            self.recovery_logger.info("Restarting browser...")
            thea_system.cleanup()
            time.sleep(2)
            return thea_system.initialize()
        except Exception as e:
            self.recovery_logger.error(f"Browser restart failed: {e}")
            return False
    
    def _refresh_cookies(self, thea_system) -> bool:
        """Refresh cookies and reinitialize session."""
        if not thea_system:
            return False
        
        try:
            self.recovery_logger.info("Refreshing cookies...")
            thea_system.cookie_manager.clear_cookies()
            time.sleep(1)
            return thea_system.initialize()
        except Exception as e:
            self.recovery_logger.error(f"Cookie refresh failed: {e}")
            return False
    
    def _retry_with_backoff(self, context: Dict[str, Any]) -> bool:
        """Retry with exponential backoff."""
        attempt = context.get('attempt', 1)
        delay = min(self.base_delay * (self.backoff_multiplier ** attempt), self.max_delay)
        
        self.recovery_logger.info(f"Retrying with {delay}s delay (attempt {attempt})")
        time.sleep(delay)
        return True
    
    def _clear_session(self, thea_system) -> bool:
        """Clear session and start fresh."""
        if not thea_system:
            return False
        
        try:
            self.recovery_logger.info("Clearing session...")
            thea_system.cookie_manager.clear_cookies()
            thea_system.cleanup()
            time.sleep(3)
            return thea_system.initialize()
        except Exception as e:
            self.recovery_logger.error(f"Session clear failed: {e}")
            return False
    
    def _wait_and_retry(self, context: Dict[str, Any]) -> bool:
        """Wait for a longer period and retry."""
        wait_time = context.get('wait_time', 30)
        self.recovery_logger.info(f"Waiting {wait_time}s before retry...")
        time.sleep(wait_time)
        return True
    
    def _fallback_mode(self, thea_system) -> bool:
        """Enable fallback mode with reduced functionality."""
        self.recovery_logger.info("Enabling fallback mode...")
        # Implement fallback mode logic here
        return True
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics and recovery information."""
        if not self.error_history:
            return {"total_errors": 0}
        
        error_counts = {}
        for record in self.error_history:
            error_type = record["error_type"]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "error_counts": error_counts,
            "recovery_attempts": self.recovery_attempts,
            "last_error": self.error_history[-1] if self.error_history else None
        }
    
    def reset_statistics(self):
        """Reset error statistics."""
        self.error_history.clear()
        self.recovery_attempts.clear()
        self.recovery_logger.info("Error statistics reset")


# Convenience functions
def create_error_recovery(**kwargs) -> TheaErrorRecovery:
    """Create an error recovery system with default settings."""
    return TheaErrorRecovery(**kwargs)


if __name__ == "__main__":
    # Example usage
    print("🛡️ V2_SWARM Thea Error Recovery System")
    print("=" * 45)
    
    recovery = create_error_recovery()
    print("✅ Error recovery system created")
    print("📊 Statistics:", recovery.get_error_statistics())






