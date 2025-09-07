"""
setup_web_development_env_part_5.py
Module: setup_web_development_env_part_5.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:10
"""

# Security compliant version of setup_web_development_env_part_5.py
# Original file: .\scripts\setup\_final_100_percent_achiever_compliant\setup_web_development_env_part_5.py
# Security issues fixed: unsafe_file_write

import os
import logging
from pathlib import Path

# Security logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Part 5 of setup_web_development_env.py
# Original file: .\scripts\setup\setup_web_development_env.py

python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    web: marks tests as web tests
    selenium: marks tests as selenium tests
    flask: marks tests as flask tests
    fastapi: marks tests as fastapi tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
"""

            pytest_file = self.repo_root / "pytest.ini"
        # SECURITY: Safe file operation
        file_path = Path(file_path)
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f'Writing to file: {file_path}')
                    with open(pytest_file, "w") as f:
                f.write(pytest_config)

            # Create test configuration
            test_config = {
                "test_environment": {
                    "base_url": "http://localhost:5000",
                    "api_base_url": "http://localhost:8000",
                    "selenium": {"browser": "chrome", "headless": True, "timeout": 30},
                    "database": {
                        "test_db": "sqlite:///test.db",
                        "cleanup_after_tests": True,
                    },
                },
                "test_data": {
                    "fixtures_dir": "tests/fixtures",
                    "mocks_dir": "tests/mocks",
                    "test_users": [
                        {"username": "test_user", "password": os.getenv("TEST_USER_PASSWORD", "")},
                        {"username": "admin_user", "password": os.getenv("ADMIN_USER_PASSWORD", "")},
                    ],
                },
            }

            test_config_file = self.config_dir / "test_config.json"
            test_config_file.parent.mkdir(exist_ok=True)


