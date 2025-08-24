"""Orchestrator for the webcam filter system."""
import logging
from typing import Dict, Any, Optional

from .webcam_configuration import default_webcam_config
from .webcam_filter_processor import WebcamFilterProcessor
from .webcam_video_handler import WebcamVideoHandler
from .webcam_ui_components import get_filter_status

logger = logging.getLogger(__name__)


class WebcamFilterSystem:
    """High level interface for webcam filtering."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or default_webcam_config()
        self.filter_processor = WebcamFilterProcessor()
        self.video_handler = WebcamVideoHandler(self.config, self.filter_processor)
        logger.info("🎨 Webcam Filter System initialized successfully")

    # ---- filter management ----
    def add_filter(
        self, filter_name: str, parameters: Optional[Dict[str, Any]] = None
    ) -> bool:
        return self.filter_processor.add_filter(filter_name, parameters)

    def remove_filter(self, filter_name: str) -> bool:
        return self.filter_processor.remove_filter(filter_name)

    def clear_filters(self) -> bool:
        return self.filter_processor.clear_filters()

    # ---- lifecycle ----
    def start_filtering(self) -> bool:
        return self.video_handler.start()

    def stop_filtering(self) -> bool:
        return self.video_handler.stop()

    # ---- frame utilities ----
    def save_filtered_frame(self, filename: Optional[str] = None) -> bool:
        return self.video_handler.save_filtered_frame(filename)

    # ---- information ----
    def get_filter_status(self) -> Dict[str, Any]:
        return get_filter_status(self.video_handler, self.filter_processor)

    def get_available_filters(self):
        return self.filter_processor.get_available_filters()

    def get_filter_parameters(self, filter_name: str):
        return self.filter_processor.get_filter_parameters(filter_name)
