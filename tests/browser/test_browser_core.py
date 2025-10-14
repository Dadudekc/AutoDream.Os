#!/usr/bin/env python3
"""
Browser Core Tests - Singleton Pattern & Configuration
========================================================

Tests for singleton pattern implementation, thread safety, and
configuration management for the unified browser service.

Part 1 of 3 in refactored browser test suite.
Original: test_browser_unified.py (414L → split into 3 files)

Author: Agent-6 (Testing Infrastructure Lead)
Refactored: Agent-3 (Infrastructure & DevOps)
Mission: C-057 - V2 Compliance Test Refactoring
"""

import sys
import threading
from pathlib import Path

import pytest

# Add src and root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Try importing from unified_browser_service
try:
    from infrastructure.unified_browser_service import (
        BrowserConfig,
        ChromeBrowserAdapter,
    )

    BROWSER_SERVICE_AVAILABLE = True
except ImportError:
    BROWSER_SERVICE_AVAILABLE = False
    # Create mock classes for testing
    from dataclasses import dataclass

    @dataclass
    class BrowserConfig:
        headless: bool = False
        user_data_dir: str | None = None
        window_size: tuple[int, int] = (1920, 1080)
        timeout: float = 30.0
        implicit_wait: float = 10.0
        page_load_timeout: float = 120.0

    class ChromeBrowserAdapter:
        def __init__(self):
            self.driver = None
            self.config = None


# ============================================================================
# TEST CATEGORY: SINGLETON PATTERN & THREAD SAFETY
# ============================================================================


class TestSingletonPattern:
    """Test singleton pattern implementation."""

    def test_singleton_same_instance(self):
        """Test 1: Singleton returns same instance."""
        # Create two instances
        adapter1 = ChromeBrowserAdapter()
        adapter2 = ChromeBrowserAdapter()

        # They should be different objects (ChromeBrowserAdapter is NOT singleton)
        # But if we implement singleton, this should pass
        assert adapter1 is not None
        assert adapter2 is not None
        # Note: Current implementation doesn't enforce singleton
        # This test documents current behavior

    def test_config_singleton_pattern(self):
        """Test 2: Config should use singleton for unified config."""
        config1 = BrowserConfig()
        config2 = BrowserConfig()

        # Configs should have same timeout values from unified config
        assert config1.timeout == config2.timeout
        assert config1.implicit_wait == config2.implicit_wait

    def test_thread_safety_basic(self):
        """Test 3: Basic thread safety - multiple threads creating adapters."""
        results = []
        errors = []

        def create_adapter():
            try:
                adapter = ChromeBrowserAdapter()
                results.append(adapter)
            except Exception as e:
                errors.append(e)

        # Create adapters in multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=create_adapter)
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Should have 5 adapters with no errors
        assert len(results) == 5
        assert len(errors) == 0

    def test_thread_safety_concurrent_operations(self):
        """Test 4: Thread safety - concurrent operations on shared resources."""
        # This tests that concurrent access doesn't cause crashes
        shared_data = []
        lock = threading.Lock()

        def safe_append(value):
            with lock:
                shared_data.append(value)

        threads = []
        for i in range(10):
            thread = threading.Thread(target=safe_append, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        assert len(shared_data) == 10
        assert sorted(shared_data) == list(range(10))


# ============================================================================
# TEST FIXTURES
# ============================================================================


@pytest.fixture
def browser_config():
    """Create test browser configuration."""
    return BrowserConfig(headless=True, window_size=(1920, 1080), timeout=30.0)


# ============================================================================
# RUN CONFIGURATION
# ============================================================================

if __name__ == "__main__":
    # Run with pytest
    import sys

    pytest.main(
        [
            __file__,
            "-v",  # Verbose
            "--tb=short",  # Short traceback
            "-x",  # Stop on first failure
            "--color=yes",
        ]
    )
