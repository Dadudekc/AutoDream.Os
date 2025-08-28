#!/usr/bin/env python3
"""Smoke tests for the response capture service."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure src is on the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from services.response_capture import (
    CaptureConfig,
    CaptureStrategy,
    ResponseCaptureService,
)
from services.response_capture.cli import run_smoke_test


def test_smoke_test_runner() -> None:
    """Ensure the bundled smoke test runs successfully."""
    assert run_smoke_test()


def test_manual_capture_and_status() -> None:
    """Manual capture should succeed and report idle status."""
    service = ResponseCaptureService(CaptureConfig(strategy=CaptureStrategy.FILE))
    assert service.capture_response("Agent-1", "Test", "manual")
    status = service.get_status()
    assert status["status"] == "idle"
