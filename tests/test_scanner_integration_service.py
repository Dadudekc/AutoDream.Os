"""Tests for :mod:`scanner_integration_service`."""

from src.services.scanner_integration_service import ScannerIntegrationService


def test_process_scan_defaults():
    service = ScannerIntegrationService()
    assert service.process_scan({"x": 1, "y": 2}) == {"x": 1, "y": 2}


def test_process_scan_with_offsets():
    service = ScannerIntegrationService(x_offset=10, y_offset=-5)
    assert service.process_scan({"x": 5, "y": 5}) == {"x": 15, "y": 0}

