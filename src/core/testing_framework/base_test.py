#!/usr/bin/env python3
"""Base test classes for the modular testing framework."""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .testing_types import TestPriority, TestResult, TestStatus, TestType
from .async_utils import run_phase
from .result_handler import create_test_result


class BaseIntegrationTest(ABC):
    """Abstract base class for integration tests."""

    def __init__(self, test_name: str, test_type: TestType, priority: TestPriority = TestPriority.NORMAL):
        self.test_name = test_name
        self.test_type = test_type
        self.priority = priority
        self.status = TestStatus.PENDING
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.error_message: Optional[str] = None
        self.error_traceback: Optional[str] = None
        self.metrics: Dict[str, Any] = {}
        self.logs: List[str] = []
        self.assertions_passed = 0
        self.assertions_failed = 0
        self.test_data: Dict[str, Any] = {}

        self.logger = logging.getLogger(f"test.{self.__class__.__name__}")
        self.logger.setLevel(logging.INFO)

    @abstractmethod
    async def setup(self) -> bool:
        """Setup test environment and dependencies."""

    @abstractmethod
    async def execute(self) -> bool:
        """Execute the actual test logic."""

    @abstractmethod
    async def cleanup(self) -> bool:
        """Cleanup test environment and resources."""

    @abstractmethod
    async def validate(self) -> bool:
        """Validate test results and assertions."""

    async def run(self) -> TestResult:
        """Run the complete test lifecycle and return a result."""
        self.status = TestStatus.RUNNING
        self.start_time = time.time()

        try:
            self.logger.info("Starting test: %s", self.test_name)
            self.logs.append(f"Test started at {time.strftime('%H:%M:%S')}")

            await run_phase(self.setup, "setup", self.logger, self.logs)
            await run_phase(self.execute, "execute", self.logger, self.logs)
            await run_phase(self.validate, "validate", self.logger, self.logs)

            self.status = TestStatus.PASSED
            self.logs.append("Test completed successfully")
        except Exception as exc:
            self.status = TestStatus.FAILED
            self.error_message = str(exc)
            self.error_traceback = str(exc.__traceback__)
            self.logs.append(f"Test failed: {exc}")
            self.logger.error("Test failed: %s", exc)
        finally:
            await run_phase(self.cleanup, "cleanup", self.logger, self.logs, suppress_exceptions=True)
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            self.logs.append(f"Test finished at {time.strftime('%H:%M:%S')}")
            self.logger.info("Test %s finished with status: %s", self.test_name, self.status.value)

        return create_test_result(self, duration)
