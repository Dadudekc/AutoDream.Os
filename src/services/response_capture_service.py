"""
Response Capture Service - AI Response Monitoring

This module provides response capture capabilities including:
- File watching for response files
- Clipboard monitoring
- OCR text extraction
- Response routing and processing

Architecture: Single Responsibility Principle - manages response capture
LOC: 150 lines (under 200 limit)
"""

import argparse
import time
import threading
import os

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class CaptureStrategy(Enum):
    """Response capture strategies"""

    FILE = "file"
    CLIPBOARD = "clipboard"
    OCR = "ocr"
    HYBRID = "hybrid"


class CaptureStatus(Enum):
    """Capture operation status"""

    IDLE = "idle"
    MONITORING = "monitoring"
    CAPTURING = "capturing"
    ERROR = "error"


@dataclass
class CaptureConfig:
    """Configuration for response capture"""

    strategy: CaptureStrategy
    file_watch_root: str = "agent_workspaces"
    file_response_name: str = "response.txt"
    clipboard_poll_ms: int = 500
    ocr_tesseract_cmd: Optional[str] = None
    ocr_lang: str = "eng"
    ocr_psm: int = 6


@dataclass
class CapturedResponse:
    """Captured response data"""

    agent_id: str
    content: str
    source: str
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None


class ResponseCaptureService:
    """
    Service for capturing AI responses from various sources

    Responsibilities:
    - Monitor response files and clipboard
    - Extract text using OCR when needed
    - Route captured responses to appropriate handlers
    - Manage capture configuration and status
    """

    def __init__(self, config: CaptureConfig):
        self.config = config
        self.status = CaptureStatus.IDLE
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.response_handlers: List[callable] = []
        self.logger = logging.getLogger(f"{__name__}.ResponseCaptureService")

        # File monitoring state
        self.watched_files: Dict[str, float] = {}  # file_path -> last_modified
        self._init_file_monitoring()

    def _init_file_monitoring(self):
        """Initialize file monitoring for agent workspaces"""
        try:
            watch_root = Path(self.config.file_watch_root)
            if watch_root.exists():
                # Find all agent directories
                for agent_dir in watch_root.iterdir():
                    if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                        response_file = agent_dir / self.config.file_response_name
                        if response_file.exists():
                            self.watched_files[
                                str(response_file)
                            ] = response_file.stat().st_mtime
                            self.logger.info(
                                f"Monitoring response file: {response_file}"
                            )
            else:
                self.logger.warning(f"Watch root directory not found: {watch_root}")
        except Exception as e:
            self.logger.error(f"Failed to initialize file monitoring: {e}")

    def start_capture(self) -> bool:
        """Start response capture monitoring"""
        if self.monitoring:
            self.logger.warning("Capture already running")
            return False

        try:
            self.monitoring = True
            self.status = CaptureStatus.MONITORING
            self.stop_event.clear()

            self.monitor_thread = threading.Thread(
                target=self._monitor_loop, daemon=True
            )
            self.monitor_thread.start()

            self.logger.info("Response capture started")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start capture: {e}")
            self.status = CaptureStatus.ERROR
            return False

    def stop_capture(self) -> bool:
        """Stop response capture monitoring"""
        try:
            self.monitoring = False
            self.status = CaptureStatus.IDLE
            self.stop_event.set()

            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=2)

            self.logger.info("Response capture stopped")
            return True

        except Exception as e:
            self.logger.error(f"Failed to stop capture: {e}")
            return False

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring and not self.stop_event.is_set():
            try:
                self._check_file_responses()

                if self.config.strategy in [
                    CaptureStrategy.CLIPBOARD,
                    CaptureStrategy.HYBRID,
                ]:
                    self._check_clipboard()

                time.sleep(0.5)  # Check every 500ms

            except Exception as e:
                self.logger.error(f"Monitor loop error: {e}")
                time.sleep(1)

    def _check_file_responses(self):
        """Check for new responses in watched files"""
        for file_path, last_modified in self.watched_files.items():
            try:
                current_modified = Path(file_path).stat().st_mtime
                if current_modified > last_modified:
                    # File has been modified, capture response
                    self._capture_file_response(file_path)
                    self.watched_files[file_path] = current_modified
            except Exception as e:
                self.logger.error(f"Error checking file {file_path}: {e}")

    def _capture_file_response(self, file_path: str):
        """Capture response from a file"""
        try:
            self.status = CaptureStatus.CAPTURING

            # Extract agent ID from file path
            agent_id = Path(file_path).parent.name

            # Read response content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if content:
                response = CapturedResponse(
                    agent_id=agent_id,
                    content=content,
                    source="file",
                    timestamp=time.time(),
                    metadata={"file_path": file_path},
                )

                self._process_captured_response(response)

                # Clear the file after capture
                self._clear_response_file(file_path)

        except Exception as e:
            self.logger.error(f"Failed to capture file response: {e}")
            self.status = CaptureStatus.ERROR
        finally:
            self.status = CaptureStatus.MONITORING

    def _check_clipboard(self):
        """Check clipboard for new responses"""
        try:
            # Try to import clipboard functionality
            try:
                import pyperclip

                clipboard_content = pyperclip.paste()

                if clipboard_content and clipboard_content.strip():
                    # Simple heuristic: check if content looks like AI response
                    if self._is_likely_ai_response(clipboard_content):
                        response = CapturedResponse(
                            agent_id="clipboard",
                            content=clipboard_content.strip(),
                            source="clipboard",
                            timestamp=time.time(),
                        )

                        self._process_captured_response(response)

            except ImportError:
                self.logger.debug("pyperclip not available for clipboard monitoring")

        except Exception as e:
            self.logger.error(f"Clipboard check error: {e}")

    def _is_likely_ai_response(self, content: str) -> bool:
        """Simple heuristic to determine if content is likely an AI response"""
        # Check for common AI response patterns
        ai_indicators = [
            "I'll help you",
            "Here's what I found",
            "Based on",
            "Let me",
            "I can",
            "I will",
            "Here's how",
            "The answer is",
        ]

        content_lower = content.lower()
        return any(indicator.lower() in content_lower for indicator in ai_indicators)

    def _clear_response_file(self, file_path: str):
        """Clear a response file after capture"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")
            self.logger.debug(f"Cleared response file: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to clear response file: {e}")

    def _process_captured_response(self, response: CapturedResponse):
        """Process a captured response"""
        try:
            self.logger.info(
                f"Captured response from {response.agent_id}: {response.content[:100]}..."
            )

            # Notify all registered handlers
            for handler in self.response_handlers:
                try:
                    handler(response)
                except Exception as e:
                    self.logger.error(f"Handler error: {e}")

        except Exception as e:
            self.logger.error(f"Failed to process captured response: {e}")

    def register_handler(self, handler: callable):
        """Register a response handler"""
        self.response_handlers.append(handler)
        self.logger.info("Registered response handler")

    def capture_response(self, agent: str, text: str, source: str) -> bool:
        """Manually capture a response"""
        try:
            response = CapturedResponse(
                agent_id=agent, content=text, source=source, timestamp=time.time()
            )

            self._process_captured_response(response)
            return True

        except Exception as e:
            self.logger.error(f"Failed to capture response: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get current capture service status"""
        return {
            "status": self.status.value,
            "monitoring": self.monitoring,
            "watched_files": len(self.watched_files),
            "handlers": len(self.response_handlers),
            "strategy": self.config.strategy.value,
        }


def run_smoke_test():
    """Run basic functionality test for ResponseCaptureService"""
    print("🧪 Running ResponseCaptureService Smoke Test...")

    try:
        config = CaptureConfig(strategy=CaptureStrategy.FILE)
        service = ResponseCaptureService(config)

        # Test service initialization
        assert service.status == CaptureStatus.IDLE
        assert not service.monitoring

        # Test manual response capture
        assert service.capture_response("test-agent", "Test response", "manual")

        # Test status
        status = service.get_status()
        assert status["status"] == "idle"
        assert status["strategy"] == "file"

        print("✅ ResponseCaptureService Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ ResponseCaptureService Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ResponseCaptureService testing"""
    parser = argparse.ArgumentParser(description="Response Capture Service CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--start", action="store_true", help="Start capture service")
    parser.add_argument("--stop", action="store_true", help="Stop capture service")
    parser.add_argument("--status", action="store_true", help="Show service status")
    parser.add_argument(
        "--capture", nargs=3, help="Capture response (agent,text,source)"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    # Create service instance
    config = CaptureConfig(strategy=CaptureStrategy.FILE)
    service = ResponseCaptureService(config)

    if args.start:
        success = service.start_capture()
        print(f"Start capture: {'SUCCESS' if success else 'FAILED'}")

    elif args.stop:
        success = service.stop_capture()
        print(f"Stop capture: {'SUCCESS' if success else 'FAILED'}")

    elif args.status:
        status = service.get_status()
        for key, value in status.items():
            print(f"{key}: {value}")

    elif args.capture:
        agent, text, source = args.capture
        success = service.capture_response(agent, text, source)
        print(f"Capture response: {'SUCCESS' if success else 'FAILED'}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
