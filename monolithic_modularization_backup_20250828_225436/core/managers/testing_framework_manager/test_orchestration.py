#!/usr/bin/env python3
"""Unified testing framework manager leveraging modular mixins."""

import logging
import unittest
from collections import defaultdict
from typing import Any, Callable, Dict, List

from ..base_manager import BaseManager
from .configuration import TestConfiguration
from .framework_setup import FrameworkSetupMixin
from .performance_analysis import PerformanceAnalysisMixin
from .strategy_management import StrategyManagementMixin
from .test_execution import TestExecutionMixin
from .test_utilities import TestUtilitiesMixin
from .result_aggregation import TestSuiteResult

logger = logging.getLogger(__name__)


class TestingFrameworkManager(
    FrameworkSetupMixin,
    PerformanceAnalysisMixin,
    StrategyManagementMixin,
    TestExecutionMixin,
    TestUtilitiesMixin,
    BaseManager,
):
    """Orchestrates test execution, analysis, and strategy management."""

    def __init__(self, config_path: str = "config/testing_framework_manager.json"):
        super().__init__(
            manager_name="TestingFrameworkManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True,
        )

        self._test_suites: Dict[str, unittest.TestSuite] = {}
        self._test_results: List[TestSuiteResult] = []
        self._test_configurations: Dict[str, TestConfiguration] = {}
        self._test_data_factories: Dict[str, Callable] = {}
        self._test_assertions: Dict[str, Callable] = {}

        self._execution_history: List[Dict[str, Any]] = []
        self._performance_metrics: Dict[str, List[float]] = defaultdict(list)
        self._coverage_data: Dict[str, Dict[str, float]] = {}

        self.default_framework = "unittest"
        self.max_parallel_tests = 4
        self.test_timeout = 300
        self.retry_failed_tests = True
        self.max_retries = 3

        self._load_manager_config()
        self._initialize_testing_workspace()
        self._register_default_test_utilities()
