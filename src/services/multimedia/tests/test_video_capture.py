#!/usr/bin/env python3
"""
Test suite for VideoCaptureService
Comprehensive testing of video capture functionality with TDD methodology
"""

import pytest
import numpy as np
import cv2
import threading
import time

from src.utils.stability_improvements import stability_manager, safe_import
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from src.services.multimedia.video_capture_service import VideoCaptureService


class TestVideoCaptureService:
    """Test suite for VideoCaptureService"""

    @pytest.fixture
    def video_service(self):
        """Create a fresh VideoCaptureService instance for each test"""
        return VideoCaptureService()

    @pytest.fixture
    def mock_frame(self):
        """Create a mock video frame for testing"""
        return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    def test_initialization(self, video_service):
        """Test VideoCaptureService initialization"""
        assert video_service.capture_threads == {}
        assert video_service.is_capturing == False
        assert video_service.frame_callbacks == {}
        assert video_service.capture_config["fps"] == 30
        assert video_service.capture_config["resolution"] == (640, 480)

    def test_start_webcam_capture_success(self, video_service):
        """Test successful webcam capture start"""
        with patch("cv2.VideoCapture") as mock_cv2:
            # Mock successful capture initialization
            mock_cap = Mock()
            mock_cap.isOpened.return_value = True
            mock_cv2.return_value = mock_cap

            # Mock threading
            with patch("threading.Thread") as mock_thread:
                mock_thread_instance = Mock()
                mock_thread.return_value = mock_thread_instance

                result = video_service.start_webcam_capture(device_id=0)

                assert result == True
                assert video_service.is_capturing == True
                assert 0 in video_service.capture_threads
                assert video_service.capture_threads[0]["active"] == True
                mock_cap.set.assert_called()
                mock_thread_instance.start.assert_called_once()

    def test_start_webcam_capture_device_failure(self, video_service):
        """Test webcam capture start with device failure"""
        with patch("cv2.VideoCapture") as mock_cv2:
            mock_cap = Mock()
            mock_cap.isOpened.return_value = False
            mock_cv2.return_value = mock_cap

            result = video_service.start_webcam_capture(device_id=0)

            assert result == False
            assert video_service.is_capturing == False
            assert 0 not in video_service.capture_threads

    def test_start_webcam_capture_already_running(self, video_service):
        """Test webcam capture start when already running"""
        # Setup existing capture
        video_service.capture_threads[0] = {"active": True, "capture": Mock()}

        result = video_service.start_webcam_capture(device_id=0)

        assert result == False

    def test_start_screen_capture_success(self, video_service):
        """Test successful screen capture start"""
        with patch("PIL.ImageGrab") as mock_pil, patch(
            "threading.Thread"
        ) as mock_thread:
            mock_thread_instance = Mock()
            mock_thread.return_value = mock_thread_instance

            result = video_service.start_screen_capture()

            assert result == True
            assert video_service.is_capturing == True
            assert "screen" in video_service.capture_threads
            assert video_service.capture_threads["screen"]["active"] == True
            mock_thread_instance.start.assert_called_once()

    def test_start_screen_capture_missing_dependencies(self, video_service):
        """Test screen capture start with missing dependencies"""
        with patch(
            "builtins.__import__", side_effect=ImportError("No module named 'PIL'")
        ):
            result = video_service.start_screen_capture()
            assert result == False

    def test_stop_capture_specific_device(self, video_service):
        """Test stopping capture for specific device"""
        # Setup mock capture
        mock_cap = Mock()
        video_service.capture_threads[0] = {
            "active": True,
            "capture": mock_cap,
            "thread": Mock(),
        }

        result = video_service.stop_capture(device_id=0)

        assert result == True
        assert 0 not in video_service.capture_threads
        mock_cap.release.assert_called_once()

    def test_stop_capture_all_devices(self, video_service):
        """Test stopping all captures"""
        # Setup multiple mock captures
        mock_cap1 = Mock()
        mock_cap2 = Mock()
        video_service.capture_threads[0] = {
            "active": True,
            "capture": mock_cap1,
            "thread": Mock(),
        }
        video_service.capture_threads[1] = {
            "active": True,
            "capture": mock_cap2,
            "thread": Mock(),
        }
        video_service.is_capturing = True

        result = video_service.stop_capture()

        assert result == True
        assert video_service.is_capturing == False
        assert len(video_service.capture_threads) == 0
        mock_cap1.release.assert_called_once()
        mock_cap2.release.assert_called_once()

    def test_get_frame(self, video_service, mock_frame):
        """Test getting frame from device"""
        video_service.frame_callbacks[0] = mock_frame

        result = video_service.get_frame(device_id=0)

        assert result is not None
        assert np.array_equal(result, mock_frame)

    def test_get_frame_not_available(self, video_service):
        """Test getting frame when not available"""
        result = video_service.get_frame(device_id=999)

        assert result == None

    def test_apply_filter_grayscale(self, video_service, mock_frame):
        """Test applying grayscale filter"""
        result = video_service.apply_filter(mock_frame, "grayscale")

        assert result is not None
        assert len(result.shape) == 2  # Grayscale should be 2D

    def test_apply_filter_blur(self, video_service, mock_frame):
        """Test applying blur filter"""
        result = video_service.apply_filter(mock_frame, "blur", kernel_size=5)

        assert result is not None
        assert result.shape == mock_frame.shape

    def test_apply_filter_edge_detection(self, video_service, mock_frame):
        """Test applying edge detection filter"""
        result = video_service.apply_filter(mock_frame, "edge_detection")

        assert result is not None
        assert len(result.shape) == 2  # Edge detection should be 2D

    def test_apply_filter_color_inversion(self, video_service, mock_frame):
        """Test applying color inversion filter"""
        result = video_service.apply_filter(mock_frame, "color_inversion")

        assert result is not None
        assert result.shape == mock_frame.shape

    def test_apply_filter_unknown_type(self, video_service, mock_frame):
        """Test applying unknown filter type"""
        result = video_service.apply_filter(mock_frame, "unknown_filter")

        assert result is not None
        assert np.array_equal(result, mock_frame)  # Should return original frame

    def test_save_frame_success(self, video_service, mock_frame, tmp_path):
        """Test successful frame saving"""
        filepath = tmp_path / "test_frame.jpg"

        with patch("cv2.imwrite") as mock_imwrite:
            mock_imwrite.return_value = True

            result = video_service.save_frame(mock_frame, str(filepath))

            assert result == True
            mock_imwrite.assert_called_once_with(str(filepath), mock_frame)

    def test_save_frame_failure(self, video_service, mock_frame):
        """Test frame saving failure"""
        with patch("cv2.imwrite") as mock_imwrite:
            mock_imwrite.return_value = False

            result = video_service.save_frame(mock_frame, "/invalid/path/frame.jpg")

            assert result == False

    def test_get_capture_status(self, video_service):
        """Test getting capture status"""
        # Setup some mock captures
        video_service.is_capturing = True
        video_service.capture_threads[0] = {"active": True, "capture": Mock()}
        video_service.frame_callbacks[0] = Mock()

        status = video_service.get_capture_status()

        assert status["is_capturing"] == True
        assert status["active_captures"] == 1
        assert 0 in status["devices"]
        assert 0 in status["frame_callbacks"]
        assert "config" in status

    def test_webcam_capture_loop_with_callback(self, video_service):
        """Test webcam capture loop with callback function"""
        mock_cap = Mock()
        mock_cap.read.side_effect = [
            (True, np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8))
        ]

        callback_called = False

        def test_callback(frame):
            nonlocal callback_called
            callback_called = True
            return frame

        # Set up capture thread info
        video_service.capture_threads[0] = {"active": True}
        video_service.is_capturing = True

        # Run capture loop briefly
        video_service._webcam_capture_loop(mock_cap, 0, test_callback)

        # Verify callback was called
        assert callback_called == True

    def test_webcam_capture_loop_callback_error(self, video_service):
        """Test webcam capture loop with callback error"""
        mock_cap = Mock()
        mock_cap.read.side_effect = [
            (True, np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8))
        ]

        def error_callback(frame):
            raise Exception("Callback error")

        # Set up capture thread info
        video_service.capture_threads[0] = {"active": True}
        video_service.is_capturing = True

        # Should not raise exception, should handle error gracefully
        try:
            video_service._webcam_capture_loop(mock_cap, 0, error_callback)
        except Exception:
            pytest.fail("Capture loop should handle callback errors gracefully")

    def test_screen_capture_loop(self, video_service):
        """Test screen capture loop functionality"""
        with patch("PIL.ImageGrab.grab") as mock_grab, patch(
            "cv2.cvtColor"
        ) as mock_cvt, patch("numpy.array") as mock_array:
            mock_screenshot = Mock()
            mock_grab.return_value = mock_screenshot
            mock_array.return_value = np.random.randint(
                0, 255, (480, 640, 3), dtype=np.uint8
            )
            mock_cvt.return_value = np.random.randint(
                0, 255, (480, 640, 3), dtype=np.uint8
            )

            # Set up capture thread info
            video_service.capture_threads["screen"] = {"active": True}
            video_service.is_capturing = True

            # Run capture loop briefly
            video_service._screen_capture_loop(None, None)

            # Verify screenshot was captured
            mock_grab.assert_called()

    def test_capture_config_modification(self, video_service):
        """Test capture configuration modification"""
        # Test FPS modification
        video_service.capture_config["fps"] = 60
        assert video_service.capture_config["fps"] == 60

        # Test resolution modification
        video_service.capture_config["resolution"] = (1280, 720)
        assert video_service.capture_config["resolution"] == (1280, 720)

        # Test codec modification
        video_service.capture_config["codec"] = "MJPG"
        assert video_service.capture_config["codec"] == "MJPG"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
