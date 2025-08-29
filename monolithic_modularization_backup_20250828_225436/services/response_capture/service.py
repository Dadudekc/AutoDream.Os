from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import logging
import threading

from .algorithm import dispatch_response, is_likely_ai_response
from .data_access import (
from .models import CaptureConfig, CaptureStatus, CaptureStrategy, CapturedResponse
from __future__ import annotations
import time

"""Service for capturing AI responses from various sources."""



    clear_response_file,
    get_clipboard_content,
    init_file_monitoring,
    read_response_file,
)


class ResponseCaptureService:
    """Orchestrates response capture across multiple sources."""

    def __init__(self, config: CaptureConfig):
        self.config = config
        self.status = CaptureStatus.IDLE
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.response_handlers: List[Callable[[CapturedResponse], None]] = []
        self.logger = logging.getLogger(__name__)
        self.watched_files: Dict[str, float] = init_file_monitoring(config, self.logger)

    # Lifecycle management
    def start_capture(self) -> bool:
        """Start response capture monitoring."""
        if self.monitoring:
            self.logger.warning("Capture already running")
            return False

        try:
            self.monitoring = True
            self.status = CaptureStatus.MONITORING
            self.stop_event.clear()
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            self.logger.info("Response capture started")
            return True
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Failed to start capture: %s", exc)
            self.status = CaptureStatus.ERROR
            return False

    def stop_capture(self) -> bool:
        """Stop response capture monitoring."""
        try:
            self.monitoring = False
            self.status = CaptureStatus.IDLE
            self.stop_event.set()
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=2)
            self.logger.info("Response capture stopped")
            return True
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Failed to stop capture: %s", exc)
            return False

    # Monitoring loop
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring and not self.stop_event.is_set():
            try:
                self._check_file_responses()
                if self.config.strategy in [CaptureStrategy.CLIPBOARD, CaptureStrategy.HYBRID]:
                    self._check_clipboard()
                time.sleep(0.5)
            except Exception as exc:  # noqa: BLE001
                self.logger.error("Monitor loop error: %s", exc)
                time.sleep(1)

    # File response handling
    def _check_file_responses(self) -> None:
        """Check for new responses in watched files."""
        for file_path, last_modified in list(self.watched_files.items()):
            try:
                current_modified = Path(file_path).stat().st_mtime
                if current_modified > last_modified:
                    self._capture_file_response(file_path)
                    self.watched_files[file_path] = current_modified
            except Exception as exc:  # noqa: BLE001
                self.logger.error("Error checking file %s: %s", file_path, exc)

    def _capture_file_response(self, file_path: str) -> None:
        """Capture response from a file."""
        try:
            self.status = CaptureStatus.CAPTURING
            agent_id = Path(file_path).parent.name
            content = read_response_file(file_path)
            if content:
                response = CapturedResponse(
                    agent_id=agent_id,
                    content=content,
                    source="file",
                    timestamp=time.time(),
                    metadata={"file_path": file_path},
                )
                self._process_captured_response(response)
                clear_response_file(file_path, self.logger)
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Failed to capture file response: %s", exc)
            self.status = CaptureStatus.ERROR
        finally:
            self.status = CaptureStatus.MONITORING

    # Clipboard handling
    def _check_clipboard(self) -> None:
        """Check clipboard for new responses."""
        try:
            content = get_clipboard_content(self.logger)
            if content and is_likely_ai_response(content):
                response = CapturedResponse(
                    agent_id="clipboard",
                    content=content,
                    source="clipboard",
                    timestamp=time.time(),
                )
                self._process_captured_response(response)
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Clipboard check error: %s", exc)

    # Response processing
    def _process_captured_response(self, response: CapturedResponse) -> None:
        """Process a captured response."""
        try:
            self.logger.info(
                "Captured response from %s: %s...", response.agent_id, response.content[:100]
            )
            dispatch_response(response, self.response_handlers)
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Failed to process captured response: %s", exc)

    def register_handler(self, handler: Callable[[CapturedResponse], None]) -> None:
        """Register a response handler."""
        self.response_handlers.append(handler)
        self.logger.info("Registered response handler")

    # Public API
    def capture_response(self, agent: str, text: str, source: str) -> bool:
        """Manually capture a response."""
        try:
            response = CapturedResponse(
                agent_id=agent, content=text, source=source, timestamp=time.time()
            )
            self._process_captured_response(response)
            return True
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Failed to capture response: %s", exc)
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get current service status."""
        return {
            "status": self.status.value,
            "monitoring": self.monitoring,
            "watched_files": len(self.watched_files),
            "handlers": len(self.response_handlers),
            "strategy": self.config.strategy.value,
        }

