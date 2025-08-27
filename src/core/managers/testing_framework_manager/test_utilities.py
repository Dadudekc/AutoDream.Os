#!/usr/bin/env python3
"""Utility helpers for test data and assertions."""

import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class TestUtilitiesMixin:
    """Mixin providing test data factories and assertion helpers."""

    def create_test_data(self, data_type: str, **kwargs) -> Any:
        """Create test data using registered factories."""
        try:
            if data_type in self._test_data_factories:
                factory = self._test_data_factories[data_type]
                return factory(**kwargs)
            logger.warning("No test data factory found for type: %s", data_type)
            return None
        except Exception as e:
            logger.error(f"Failed to create test data for type '{data_type}': {e}")
            return None

    def register_test_data_factory(
        self, data_type: str, factory_func: Callable
    ) -> None:
        """Register a test data factory function."""
        self._test_data_factories[data_type] = factory_func
        logger.info("Registered test data factory for type: %s", data_type)

    def assert_test_condition(self, assertion_type: str, *args, **kwargs) -> bool:
        """Execute a test assertion using registered assertion functions."""
        try:
            if assertion_type in self._test_assertions:
                assertion_func = self._test_assertions[assertion_type]
                return assertion_func(*args, **kwargs)
            logger.warning("No test assertion found for type: %s", assertion_type)
            return False
        except Exception as e:
            logger.error(f"Failed to execute test assertion '{assertion_type}': {e}")
            return False

    def register_test_assertion(
        self, assertion_type: str, assertion_func: Callable
    ) -> None:
        """Register a test assertion function."""
        self._test_assertions[assertion_type] = assertion_func
        logger.info("Registered test assertion for type: %s", assertion_type)
