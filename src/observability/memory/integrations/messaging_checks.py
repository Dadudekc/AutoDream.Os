"""
Messaging Integrations - Memory Leak Prevention
===============================================

Memory leak prevention for V2_SWARM messaging system.
Implements file resource guards, message validation, and instrumentation.

Author: Agent-7 (Web Development Expert)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions, KISS principle
"""

import logging
import time
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ============================================================
# FILE RESOURCE GUARD (Context Manager Pattern)
# ============================================================

class FileResourceGuard:
    """
    Context manager for safe file operations with automatic cleanup.
    Prevents file descriptor leaks in messaging system.
    """
    
    def __init__(self, file_path: str, mode: str = 'r', encoding: str = 'utf-8'):
        """Initialize file resource guard"""
        self.file_path = file_path
        self.mode = mode
        self.encoding = encoding
        self.file_handle = None
        self.opened = False
    
    def __enter__(self):
        """Open file with resource tracking"""
        try:
            self.with open(self.file_path, self.mode, encoding=self.encoding) as file_handle:
            self.opened = True
            logger.debug(f"FileResourceGuard: Opened {self.file_path}")
            return self.file_handle
        except Exception as e:
            logger.error(f"FileResourceGuard: Error opening {self.file_path}: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close file with guaranteed cleanup"""
        if self.file_handle and self.opened:
            try:
                self.file_handle.close()
                logger.debug(f"FileResourceGuard: Closed {self.file_path}")
            except Exception as e:
                logger.error(f"FileResourceGuard: Error closing {self.file_path}: {e}")
            finally:
                self.file_handle = None
                self.opened = False
        return False


# ============================================================
# MESSAGE SIZE VALIDATOR
# ============================================================

class MessageSizeValidator:
    """
    Validates message sizes to prevent memory bloat.
    Enforces reasonable message size limits.
    """
    
    def __init__(self, max_size_mb: float = 1.0):
        """Initialize message size validator"""
        self.max_size_bytes = int(max_size_mb * 1024 * 1024)
        logger.info(f"MessageSizeValidator initialized: max_size={max_size_mb}MB")
    
    def validate(self, message: str) -> Dict[str, Any]:
        """Validate message size"""
        try:
            message_bytes = len(message.encode('utf-8'))
            
            if message_bytes > self.max_size_bytes:
                return {
                    'is_valid': False,
                    'reason': f"Message size {message_bytes} bytes exceeds limit {self.max_size_bytes} bytes",
                    'message_size_bytes': message_bytes,
                    'metadata': {'max_size_bytes': self.max_size_bytes}
                }
            
            return {
                'is_valid': True,
                'reason': "Message size within limits",
                'message_size_bytes': message_bytes,
                'metadata': {'max_size_bytes': self.max_size_bytes}
            }
        except Exception as e:
            logger.error(f"Message validation error: {e}")
            return {
                'is_valid': False,
                'reason': f"Validation error: {str(e)}",
                'message_size_bytes': 0,
                'metadata': {'error': str(e)}
            }


# ============================================================
# MESSAGING OPERATIONS INSTRUMENTATION
# ============================================================

class MessagingInstrumentation:
    """Instruments messaging operations for memory tracking."""
    
    def __init__(self):
        """Initialize messaging instrumentation"""
        self.metrics_history = []
        self.max_history = 100
    
    @contextmanager
    def instrument_operation(self, operation: str, message_size_bytes: int):
        """Context manager for instrumenting messaging operations"""
        start_time = time.time()
        try:
            yield
        finally:
            duration_ms = (time.time() - start_time) * 1000
            self.metrics_history.append({
                'operation': operation,
                'duration_ms': duration_ms,
                'message_size_bytes': message_size_bytes,
                'timestamp': time.time()
            })
            if len(self.metrics_history) > self.max_history:
                self.metrics_history.pop(0)
            logger.debug(f"Operation {operation}: {duration_ms:.2f}ms")


# ============================================================
# COORDINATION REQUEST PURGER
# ============================================================

class CoordinationRequestPurger:
    """
    Purges old coordination requests to prevent memory accumulation.
    Implements time-based and count-based purging strategies.
    """
    
    def __init__(self, max_age_seconds: int = 3600, max_count: int = 1000):
        """Initialize coordination request purger"""
        self.max_age_seconds = max_age_seconds
        self.max_count = max_count
        logger.info(f"CoordinationRequestPurger initialized")
    
    def purge_old_requests(self, requests: Dict[str, Dict]) -> Dict[str, Any]:
        """Purge old coordination requests (time and count based)"""
        current_time = time.time()
        
        # Time-based purging
        remaining = {
            rid: rdata for rid, rdata in requests.items()
            if (current_time - rdata.get('timestamp', 0)) <= self.max_age_seconds
        }
        
        # Count-based purging (keep most recent)
        if len(remaining) > self.max_count:
            sorted_reqs = sorted(
                remaining.items(),
                key=lambda x: x[1].get('timestamp', 0),
                reverse=True
            )
            remaining = dict(sorted_reqs[:self.max_count])
        
        purged_count = len(requests) - len(remaining)
        logger.info(f"Purged {purged_count} old coordination requests")
        
        return {
            'purged_count': purged_count,
            'remaining_count': len(remaining),
            'remaining_requests': remaining
        }


# ============================================================
# INTEGRATION WITH PHASE 1 DETECTORS
# ============================================================

class MessagingMemoryIntegration:
    """
    Integrates messaging checks with Phase 1 memory policy framework.
    Provides unified memory management for messaging operations.
    """
    
    def __init__(self, policy_manager=None):
        """Initialize messaging memory integration"""
        self.policy_manager = policy_manager
        self.validator = MessageSizeValidator()
        self.instrumentation = MessagingInstrumentation()
        self.purger = CoordinationRequestPurger()
        logger.info("MessagingMemoryIntegration initialized")


# Export all public classes and functions
__all__ = [
    'FileResourceGuard',
    'MessageSizeValidator',
    'MessagingInstrumentation',
    'CoordinationRequestPurger',
    'MessagingMemoryIntegration',
]

