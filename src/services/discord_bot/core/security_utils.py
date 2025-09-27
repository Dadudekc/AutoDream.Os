#!/usr/bin/env python3
"""
Security Utilities
==================

Security helper functions for the Discord bot system.
"""

import re
import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class SecurityUtils:
    """Security utility functions."""
    
    # Sensitive patterns to mask in logs
    SENSITIVE_PATTERNS = [
        r'DISCORD_BOT_TOKEN[=:]\s*([^\s\n]+)',
        r'API_KEY[=:]\s*([^\s\n]+)',
        r'PASSWORD[=:]\s*([^\s\n]+)',
        r'SECRET[=:]\s*([^\s\n]+)',
        r'TOKEN[=:]\s*([^\s\n]+)',
        r'KEY[=:]\s*([^\s\n]+)',
    ]
    
    @staticmethod
    def mask_token(token: str, show_chars: int = 8) -> str:
        """Mask a token for secure logging."""
        if not token or len(token) < show_chars:
            return "***"
        return token[:show_chars] + "..." + token[-4:]
    
    @staticmethod
    def mask_sensitive_data(text: str) -> str:
        """Mask sensitive data in text for logging."""
        masked_text = text
        
        for pattern in SecurityUtils.SENSITIVE_PATTERNS:
            # Replace with masked version
            masked_text = re.sub(
                pattern,
                lambda m: m.group(0).replace(m.group(1), SecurityUtils.mask_token(m.group(1))),
                masked_text,
                flags=re.IGNORECASE
            )
        
        return masked_text
    
    @staticmethod
    def validate_path(path: str) -> bool:
        """Validate file path to prevent path traversal attacks."""
        try:
            # Resolve the path and check for path traversal
            resolved_path = Path(path).resolve()
            
            # Check for suspicious patterns
            path_str = str(resolved_path)
            suspicious_patterns = [
                '../', '..\\',  # Path traversal
                '~',            # Home directory
                '$',            # Environment variables
                '|', ';', '&', # Command injection
                '<', '>',       # Redirection
            ]
            
            for pattern in suspicious_patterns:
                if pattern in path_str:
                    logger.warning(f"[SECURITY] Suspicious path pattern detected: {pattern}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"[SECURITY] Path validation failed: {e}")
            return False
    
    @staticmethod
    def sanitize_command_args(args: list) -> list:
        """Sanitize command arguments to prevent injection."""
        sanitized = []
        
        for arg in args:
            if isinstance(arg, str):
                # Remove potentially dangerous characters
                sanitized_arg = re.sub(r'[|;&<>`$]', '', arg)
                if sanitized_arg != arg:
                    logger.warning(f"[SECURITY] Sanitized command argument: {arg} -> {sanitized_arg}")
                sanitized.append(sanitized_arg)
            else:
                sanitized.append(arg)
        
        return sanitized
    
    @staticmethod
    def create_secure_environment() -> Dict[str, str]:
        """Create a secure environment for subprocess execution."""
        secure_env = {}
        
        # Only include safe environment variables
        safe_vars = [
            'PATH', 'PYTHONPATH', 'PYTHONUTF8', 'PYTHONIOENCODING',
            'TEMP', 'TMP', 'HOME', 'USER', 'USERNAME',
            'DISCORD_BOT_TOKEN',  # Only if explicitly needed
        ]
        
        for var in safe_vars:
            value = os.environ.get(var)
            if value:
                secure_env[var] = value
        
        # Add system-specific variables
        if os.name == 'nt':
            secure_env.update({
                'SYSTEMROOT': os.environ.get('SYSTEMROOT', ''),
                'WINDIR': os.environ.get('WINDIR', ''),
            })
        
        return secure_env
    
    @staticmethod
    def log_security_event(event_type: str, user_id: str, details: str, severity: str = "MEDIUM"):
        """Log security events with proper formatting."""
        logger.warning(
            f"[SECURITY_EVENT] {event_type} - User: {SecurityUtils.mask_token(user_id)} - "
            f"Severity: {severity} - Details: {SecurityUtils.mask_sensitive_data(details)}"
        )
    
    @staticmethod
    def validate_discord_permissions(permissions: Any) -> bool:
        """Validate Discord permissions object."""
        try:
            # Check if permissions object is valid
            if not hasattr(permissions, 'administrator'):
                return False
            
            # Additional validation could be added here
            return True
        except Exception as e:
            logger.error(f"[SECURITY] Permission validation failed: {e}")
            return False


# Global instance for easy access
security_utils = SecurityUtils()
