"""
Browser Unified Configuration.

V2 Compliance: Rewritten from Chat_Mate config with V2 patterns
Author: Agent-7 - Repository Cloning Specialist
License: MIT
"""

from pathlib import Path
from typing import Any, Dict, Optional


class BrowserConfig:
    """
    Browser configuration for unified driver management.
    
    Provides configuration for:
    - Chrome driver paths
    - Mobile emulation profiles
    - Cookie persistence
    - Performance settings
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize browser configuration.
        
        Args:
            config_dict: Optional configuration dictionary
        """
        config = config_dict or {}
        
        # Directory paths
        self.template_dir = Path(config.get('template_dir', 'templates'))
        self.output_dir = Path(config.get('output_dir', 'outputs'))
        self.log_dir = Path(config.get('log_dir', 'logs'))
        self.profile_dir = Path(config.get('profile_dir', 'runtime/browser/profiles'))
        self.cookie_file = Path(config.get('cookie_file', 'runtime/browser/cookies.json'))
        
        # Driver settings
        self.driver_type = config.get('driver_type', 'chrome')
        self.undetected_mode = config.get('undetected_mode', True)
        self.headless = config.get('headless', False)
        
        # Performance settings
        self.page_load_timeout = config.get('page_load_timeout', 30)
        self.implicit_wait = config.get('implicit_wait', 10)
        self.max_instances = config.get('max_instances', 3)
        
        # Mobile emulation
        self.mobile_emulation_enabled = config.get('mobile_emulation_enabled', False)
        self.mobile_device = config.get('mobile_device', 'iphone_12')
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return getattr(self, key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict[str, Any]: Configuration as dictionary
        """
        return {
            'template_dir': str(self.template_dir),
            'output_dir': str(self.output_dir),
            'log_dir': str(self.log_dir),
            'profile_dir': str(self.profile_dir),
            'cookie_file': str(self.cookie_file),
            'driver_type': self.driver_type,
            'undetected_mode': self.undetected_mode,
            'headless': self.headless,
            'page_load_timeout': self.page_load_timeout,
            'implicit_wait': self.implicit_wait,
            'max_instances': self.max_instances,
            'mobile_emulation_enabled': self.mobile_emulation_enabled,
            'mobile_device': self.mobile_device
        }


# Global default config instance
config = BrowserConfig()
