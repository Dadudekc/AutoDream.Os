from src.utils.config_core import get_config

# MIGRATED: This file has been migrated to the centralized configuration system
"""Shared configuration for test infrastructure."""

TEST_FILE_PATTERN = "test_*.py"
COVERAGE_REPORT_PRECISION = get_config('COVERAGE_REPORT_PRECISION', 2)
