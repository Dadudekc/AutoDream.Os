"""Command-line interface for the response capture service."""

from __future__ import annotations

import argparse

from .models import CaptureConfig, CaptureStrategy
from .service import ResponseCaptureService


def run_smoke_test() -> bool:
    """Run basic functionality test for ResponseCaptureService."""
    config = CaptureConfig(strategy=CaptureStrategy.FILE)
    service = ResponseCaptureService(config)
    assert service.capture_response("test-agent", "Test response", "manual")
    status = service.get_status()
    return status["status"] == "idle"


def main() -> None:
    """CLI interface for ResponseCaptureService testing."""
    parser = argparse.ArgumentParser(description="Response Capture Service CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--start", action="store_true", help="Start capture service")
    parser.add_argument("--stop", action="store_true", help="Stop capture service")
    parser.add_argument("--status", action="store_true", help="Show service status")
    parser.add_argument("--capture", nargs=3, metavar=("AGENT", "TEXT", "SOURCE"), help="Capture response")
    args = parser.parse_args()

    config = CaptureConfig(strategy=CaptureStrategy.FILE)
    service = ResponseCaptureService(config)

    if args.test:
        success = run_smoke_test()
        print(f"Smoke test {'PASSED' if success else 'FAILED'}")
    elif args.start:
        print(f"Start capture: {'SUCCESS' if service.start_capture() else 'FAILED'}")
    elif args.stop:
        print(f"Stop capture: {'SUCCESS' if service.stop_capture() else 'FAILED'}")
    elif args.status:
        for key, value in service.get_status().items():
            print(f"{key}: {value}")
    elif args.capture:
        agent, text, source = args.capture
        success = service.capture_response(agent, text, source)
        print(f"Capture response: {'SUCCESS' if success else 'FAILED'}")
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover - manual CLI execution
    main()
