"""FastAPI endpoints for controlling streaming services."""

from typing import Dict, Any

try:  # pragma: no cover - optional dependency
    from fastapi import APIRouter, HTTPException
except Exception:  # pragma: no cover - optional dependency
    APIRouter = None  # type: ignore
    HTTPException = Exception

from .streaming_service import StreamingService

router = APIRouter() if APIRouter else None
_service = StreamingService()

if router:

    @router.post("/stream/start")
    def start_stream(config: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new live stream."""
        if not _service.start_live_stream(config["name"], config):
            raise HTTPException(status_code=400, detail="Failed to start stream")
        return {"status": "started"}

    @router.post("/stream/stop/{name}")
    def stop_stream(name: str) -> Dict[str, Any]:
        """Stop an existing live stream."""
        if not _service.stop_live_stream(name):
            raise HTTPException(status_code=404, detail="Stream not found")
        return {"status": "stopped"}

    @router.get("/stream/status/{name}")
    def stream_status(name: str) -> Dict[str, Any]:
        """Retrieve streaming session status."""
        status = _service.get_streaming_status(name)
        if "error" in status:
            raise HTTPException(status_code=404, detail=status["error"])
        return status

    @router.patch("/stream/{name}/quality/{quality}")
    def update_quality(name: str, quality: str) -> Dict[str, Any]:
        """Update quality preset of a live stream."""
        if not _service.update_stream_quality(name, quality):
            raise HTTPException(status_code=400, detail="Failed to update quality")
        return {"status": "updated"}
