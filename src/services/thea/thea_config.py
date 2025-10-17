#!/usr/bin/env python3
"""
Thea Configuration Module
==========================

Centralized configuration for Thea service.

Author: Agent-2 (Architecture) - V2 Consolidation
License: MIT
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class TheaConfig:
    """Configuration for Thea service."""

    # URLs
    thea_url: str = (
        "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
    )
    chatgpt_base_url: str = "https://chatgpt.com/"

    # File paths
    cookie_file: str = "thea_cookies.json"
    responses_dir: str = "thea_responses"

    # Browser settings
    headless: bool = False
    window_width: int = 1920
    window_height: int = 1080

    # Timeouts (seconds)
    login_timeout: int = 60
    response_timeout: int = 120
    navigation_delay: float = 2.0
    typing_delay: float = 0.1

    # PyAutoGUI settings
    use_pyautogui: bool = True
    pyautogui_typing_interval: float = 0.01

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0

    # Response capture
    save_responses: bool = True
    save_screenshots: bool = True
    save_metadata: bool = True

    def __post_init__(self):
        """Validate and setup paths."""
        self.cookie_path = Path(self.cookie_file)
        self.responses_path = Path(self.responses_dir)
        self.responses_path.mkdir(parents=True, exist_ok=True)


# Default configuration instance
DEFAULT_CONFIG = TheaConfig()

