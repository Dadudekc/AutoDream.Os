#!/usr/bin/env python3
"""
Thea Configuration - V2 Compliant Configuration Management
===========================================================

Centralized configuration for all Thea services with V2 compliance.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TheaConfig:
    """Configuration for Thea services."""

    # Core URLs
    thea_url: str = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5-thinking"
    chatgpt_base_url: str = "https://chatgpt.com"

    # Authentication
    username: str | None = None
    password: str | None = None
    cookie_file: str = "thea_cookies.json"
    use_cookies: bool = True

    # Browser settings
    use_selenium: bool = True
    headless: bool = False
    browser_timeout: int = 30
    page_load_timeout: int = 10

    # Response detection
    response_timeout: int = 120
    stable_secs: float = 3.0
    poll_interval: float = 0.5
    auto_continue: bool = True
    max_continue_clicks: int = 1

    # File paths
    responses_dir: Path = field(default_factory=lambda: Path("thea_responses"))
    logs_dir: Path = field(default_factory=lambda: Path("logs"))
    config_dir: Path = field(default_factory=lambda: Path("config"))

    # Message templates
    message_template_path: Path = field(default_factory=lambda: Path("messages/thea_consultation_message.md"))

    # Selenium options
    selenium_options: dict[str, Any] = field(default_factory=lambda: {
        "no_sandbox": True,
        "disable_dev_shm_usage": True,
        "disable_gpu": True,
        "window_size": "1920,1080",
        "disable_extensions": True,
        "disable_plugins": True,
        "disable_images": False,  # Keep images for better UX
    })

    # Input selectors (prioritized)
    input_selectors: list = field(default_factory=lambda: [
        "textarea[data-testid*='prompt']",
        "textarea[placeholder*='Message']",
        "#prompt-textarea",
        "textarea",
        "[contenteditable='true']"
    ])

    def __post_init__(self):
        """Initialize derived paths."""
        self.responses_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)

    @classmethod
    def from_env(cls) -> 'TheaConfig':
        """Create config from environment variables."""
        return cls(
            username=os.getenv('THEA_USERNAME'),
            password=os.getenv('THEA_PASSWORD'),
            cookie_file=os.getenv('THEA_COOKIE_FILE', 'thea_cookies.json'),
            use_cookies=os.getenv('THEA_USE_COOKIES', 'true').lower() == 'true',
            use_selenium=os.getenv('THEA_USE_SELENIUM', 'true').lower() == 'true',
            headless=os.getenv('THEA_HEADLESS', 'false').lower() == 'true',
            browser_timeout=int(os.getenv('THEA_BROWSER_TIMEOUT', '30')),
            response_timeout=int(os.getenv('THEA_RESPONSE_TIMEOUT', '120')),
        )

    @classmethod
    def from_args(cls, args) -> 'TheaConfig':
        """Create config from command line arguments."""
        return cls(
            username=getattr(args, 'username', None),
            password=getattr(args, 'password', None),
            use_selenium=not getattr(args, 'no_selenium', False),
            headless=getattr(args, 'headless', False),
            cookie_file=getattr(args, 'cookie_file', 'thea_cookies.json'),
            use_cookies=not getattr(args, 'no_cookies', False),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'thea_url': self.thea_url,
            'chatgpt_base_url': self.chatgpt_base_url,
            'username': self.username,
            'password': '***' if self.password else None,  # Don't expose password
            'cookie_file': self.cookie_file,
            'use_cookies': self.use_cookies,
            'use_selenium': self.use_selenium,
            'headless': self.headless,
            'browser_timeout': self.browser_timeout,
            'response_timeout': self.response_timeout,
            'responses_dir': str(self.responses_dir),
            'logs_dir': str(self.logs_dir),
        }


# Global config instance
_config_instance: TheaConfig | None = None


def get_thea_config() -> TheaConfig:
    """Get the global Thea configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = TheaConfig()
    return _config_instance


def set_thea_config(config: TheaConfig) -> None:
    """Set the global Thea configuration instance."""
    global _config_instance
    _config_instance = config
