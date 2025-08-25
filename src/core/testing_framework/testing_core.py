#!/usr/bin/env python3
"""High-level orchestration for the testing framework."""

from __future__ import annotations

import asyncio
import logging
from typing import Iterable, List

from .base_test import BaseIntegrationTest
from .integration_tests import (
    CrossSystemCommunicationTest,
    ServiceIntegrationTest,
    DatabaseIntegrationTest,
)


class TestManager:
    """Lightweight orchestrator that runs integration tests sequentially."""

    def __init__(self, tests: Iterable[BaseIntegrationTest] | None = None):
        self.tests: List[BaseIntegrationTest] = list(tests or [])
        self.logger = logging.getLogger(__name__)

    def add_test(self, test: BaseIntegrationTest) -> None:
        self.tests.append(test)
        self.logger.info("Added test %s", test.test_name)

    async def run_all(self):
        results = []
        for test in self.tests:
            self.logger.info("Running %s", test.test_name)
            results.append(await test.run())
        return results


async def run_demo_suite():
    """Run a small demonstration suite of built-in tests."""
    manager = TestManager(
        [
            CrossSystemCommunicationTest("Communication Test"),
            ServiceIntegrationTest("Service Test"),
            DatabaseIntegrationTest("Database Test"),
        ]
    )
    return await manager.run_all()


def run_smoke_test() -> bool:
    """Execute the demo suite to verify orchestration works."""
    try:
        asyncio.run(run_demo_suite())
        print("🎉 Testing core smoke test passed!")
        return True
    except Exception as exc:  # pragma: no cover - defensive
        print(f"❌ Testing core smoke test failed: {exc}")
        return False


if __name__ == "__main__":  # pragma: no cover
    run_smoke_test()
