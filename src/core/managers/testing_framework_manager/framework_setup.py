#!/usr/bin/env python3
"""Setup and teardown helpers for the testing framework manager."""

import json
import logging
import random
from pathlib import Path

logger = logging.getLogger(__name__)


class FrameworkSetupMixin:
    """Mixin handling configuration loading and workspace setup."""

    def _load_manager_config(self) -> None:
        """Load manager-specific configuration from file."""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    if "testing" in config:
                        testing_config = config["testing"]
                        self.default_framework = testing_config.get(
                            "default_framework", "unittest"
                        )
                        self.max_parallel_tests = testing_config.get(
                            "max_parallel_tests", 4
                        )
                        self.test_timeout = testing_config.get("test_timeout", 300)
                        self.retry_failed_tests = testing_config.get(
                            "retry_failed_tests", True
                        )
                        self.max_retries = testing_config.get("max_retries", 3)
            else:
                logger.warning("Testing config file not found: %s", self.config_path)
        except Exception as e:
            logger.error(f"Failed to load testing config: {e}")

    def _initialize_testing_workspace(self) -> None:
        """Initialize the testing workspace."""
        self.workspace_path = Path("testing_workspaces")
        self.workspace_path.mkdir(exist_ok=True)
        logger.info("Testing workspace initialized")

    def _register_default_test_utilities(self) -> None:
        """Register default test data factories and assertions."""
        self.register_test_data_factory("string", lambda length=10: "a" * length)
        self.register_test_data_factory(
            "integer", lambda min_val=0, max_val=100: random.randint(min_val, max_val)
        )
        self.register_test_data_factory("list", lambda size=5: list(range(size)))
        self.register_test_assertion("equals", lambda a, b: a == b)
        self.register_test_assertion("not_equals", lambda a, b: a != b)
        self.register_test_assertion(
            "contains", lambda container, item: item in container
        )
        self.register_test_assertion("greater_than", lambda a, b: a > b)
        self.register_test_assertion("less_than", lambda a, b: a < b)
        logger.info("Default test utilities registered")

    def cleanup(self) -> None:
        """Cleanup testing framework manager resources."""
        try:
            self._test_suites.clear()
            self._test_results.clear()
            logger.info("TestingFrameworkManager cleanup completed")
        except Exception as e:
            logger.error(f"TestingFrameworkManager cleanup failed: {e}")
