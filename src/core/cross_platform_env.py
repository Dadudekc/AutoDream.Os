#!/usr/bin/env python3
"""
Cross-Platform Environment Utilities
=====================================

This module provides cross-platform environment utilities for the Agent Cellphone V2 system,
ensuring consistent environment variable handling across Windows and Linux platforms.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Optional, Dict, Any, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrossPlatformEnvironment:
    """Cross-platform environment management utilities."""
    
    def __init__(self):
        self.platform = platform.system()
        self.is_windows = self.platform == "Windows"
        self.is_linux = self.platform == "Linux"
        self.is_macos = self.platform == "Darwin"
    
    def get_env_var(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable with platform-specific handling."""
        value = os.environ.get(name, default)
        
        # Handle platform-specific environment variable variations
        if value is None and self.is_windows:
            # Windows: Try uppercase version
            value = os.environ.get(name.upper(), default)
        elif value is None and not self.is_windows:
            # Linux/macOS: Try lowercase version
            value = os.environ.get(name.lower(), default)
        
        return value
    
    def set_env_var(self, name: str, value: str, overwrite: bool = True):
        """Set environment variable."""
        if overwrite or name not in os.environ:
            os.environ[name] = value
    
    def get_path_env(self) -> list:
        """Get PATH environment variable as list."""
        path_str = self.get_env_var('PATH', '')
        if self.is_windows:
            return path_str.split(';') if path_str else []
        else:
            return path_str.split(':') if path_str else []
    
    def add_to_path(self, path: Union[str, Path]):
        """Add path to PATH environment variable."""
        path = str(Path(path).resolve())
        current_path = self.get_path_env()
        
        if path not in current_path:
            current_path.append(path)
            
            if self.is_windows:
                os.environ['PATH'] = ';'.join(current_path)
            else:
                os.environ['PATH'] = ':'.join(current_path)
    
    def get_python_path(self) -> Path:
        """Get Python executable path."""
        return Path(sys.executable)
    
    def get_python_version(self) -> str:
        """Get Python version string."""
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def get_platform_info(self) -> Dict[str, Any]:
        """Get comprehensive platform information."""
        return {
            "platform": self.platform,
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.architecture(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": self.get_python_version(),
            "python_executable": str(self.get_python_path()),
            "is_windows": self.is_windows,
            "is_linux": self.is_linux,
            "is_macos": self.is_macos,
            "path_separator": os.sep,
            "line_separator": os.linesep,
            "temp_dir": os.environ.get('TMPDIR', os.environ.get('TEMP', '/tmp')),
            "home_dir": str(Path.home())
        }
    
    def load_env_file(self, env_file: Union[str, Path]) -> bool:
        """Load environment variables from file."""
        env_file = Path(env_file)
        
        if not env_file.exists():
            logger.warning(f"Environment file not found: {env_file}")
            return False
        
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value pairs
                    if '=' in line:
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
                        value = value.strip()
                        
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
# SECURITY: Key placeholder - replace with environment variable
            
            logger.info(f"Loaded environment variables from {env_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading environment file {env_file}: {e}")
            return False
    
    def get_agent_config(self) -> Dict[str, Any]:
        """Get agent-specific configuration from environment."""
        config = {}
        
        # Discord configuration
# SECURITY: Token placeholder - replace with environment variable
        config['discord_channel_id'] = self.get_env_var('DISCORD_CHANNEL_ID')
        
        # Agent-specific Discord channels
        for i in range(1, 9):
            channel_id = self.get_env_var(f'DISCORD_CHANNEL_AGENT_{i}')
            if channel_id:
                config[f'agent_{i}_channel'] = channel_id
        
        # Major update channel
        config['major_update_channel'] = self.get_env_var('MAJOR_UPDATE_DISCORD_CHANNEL_ID')
        
        # Thea configuration
        config['thea_username'] = self.get_env_var('THEA_USERNAME')
# SECURITY: Password placeholder - replace with environment variable
        
        # Database configuration
        config['database_path'] = self.get_env_var('DATABASE_PATH', 'data/agent_system.db')
        
        # Logging configuration
        config['log_level'] = self.get_env_var('LOG_LEVEL', 'INFO')
        config['log_file'] = self.get_env_var('LOG_FILE')
        
        return config
    
    def validate_required_env_vars(self, required_vars: list) -> Dict[str, bool]:
        """Validate that required environment variables are set."""
        results = {}
        
        for var in required_vars:
            value = self.get_env_var(var)
            results[var] = value is not None and value.strip() != ''
        
        return results
    
    def get_development_config(self) -> Dict[str, Any]:
        """Get development-specific configuration."""
        config = {
            'is_development': self.get_env_var('DEVELOPMENT', 'false').lower() == 'true',
            'debug_mode': self.get_env_var('DEBUG', 'false').lower() == 'true',
            'test_mode': self.get_env_var('TEST_MODE', 'false').lower() == 'true',
            'mock_services': self.get_env_var('MOCK_SERVICES', 'false').lower() == 'true'
        }
        
        return config

# Global instance for easy access
env_manager = CrossPlatformEnvironment()

# Convenience functions
def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with platform-specific handling."""
    return env_manager.get_env_var(name, default)

def set_env_var(name: str, value: str, overwrite: bool = True):
    """Set environment variable."""
    env_manager.set_env_var(name, value, overwrite)

def load_env_file(env_file: Union[str, Path]) -> bool:
    """Load environment variables from file."""
    return env_manager.load_env_file(env_file)

def get_platform_info() -> Dict[str, Any]:
    """Get comprehensive platform information."""
    return env_manager.get_platform_info()

def get_agent_config() -> Dict[str, Any]:
    """Get agent-specific configuration from environment."""
    return env_manager.get_agent_config()

def get_development_config() -> Dict[str, Any]:
    """Get development-specific configuration."""
    return env_manager.get_development_config()

def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"

def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"

def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"

def is_development() -> bool:
    """Check if running in development mode."""
    return get_development_config()['is_development']

def is_debug_mode() -> bool:
    """Check if running in debug mode."""
    return get_development_config()['debug_mode']

def is_test_mode() -> bool:
    """Check if running in test mode."""
    return get_development_config()['test_mode']


