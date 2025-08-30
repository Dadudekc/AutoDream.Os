
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration for the auth integration tester."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AuthTesterConfig:
    """Simple configuration container for integration tests."""

    test_user: str = "admin"
    valid_password: str = "secure_password_123"
    invalid_password: str = "wrong_password"
    source_ip: str = "127.0.0.1"
    save_report_path: Optional[str] = "auth_integration_report.json"
    run_performance: bool = True
    run_security: bool = True
    timeout: int = 30
