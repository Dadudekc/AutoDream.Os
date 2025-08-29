"""UI and status helpers for the webcam filter system."""
from typing import Dict, Any


def get_filter_status(video_handler, filter_processor) -> Dict[str, Any]:
    """Return status information for the webcam system."""
    return {
        "is_running": video_handler.is_running,
        "active_filters": len(filter_processor.active_filters),
        "filter_pipeline": [f["name"] for f in filter_processor.filter_pipeline],
        "camera_connected": video_handler.camera is not None
        and video_handler.camera.isOpened(),
        "obs_connected": video_handler.obs_integration is not None,
        "frame_buffer_size": len(video_handler.frame_buffer),
        "config": video_handler.config,
    }
