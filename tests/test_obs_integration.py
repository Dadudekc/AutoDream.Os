"""
OBS Virtual Camera Integration Test Suite
Agent_Cellphone_V2_Repository TDD Integration Project

Comprehensive testing for OBS integration capabilities
"""

import pytest
import numpy as np
import cv2
import time
import threading
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from web.multimedia.obs_integration import OBSVirtualCameraIntegration


class TestOBSVirtualCameraIntegration:
    """Test suite for OBS Virtual Camera Integration Service"""

    @pytest.fixture
    def obs_config(self):
        """Test configuration for OBS integration"""
        return {
            "obs_websocket_host": "localhost",
            "obs_websocket_port": 4455,
            "obs_websocket_password": "test_password",
            "virtual_camera_name": "Test_Virtual_Camera",
            "frame_rate": 30,
            "resolution": (1280, 720),
            "quality": "high",
            "buffer_size": 50,
            "auto_reconnect": True,
            "reconnect_interval": 5,
        }

    @pytest.fixture
    def mock_frame(self):
        """Mock video frame for testing"""
        return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    @pytest.fixture
    def obs_integration(self, obs_config):
        """OBS integration service instance for testing"""
        with patch("web.multimedia.obs_integration.HealthMonitorWeb"):
            service = OBSVirtualCameraIntegration(obs_config)
            yield service

    def test_initialization(self, obs_integration, obs_config):
        """Test OBS integration service initialization"""
        assert obs_integration.config == obs_config
        assert obs_integration.is_connected == False
        assert obs_integration.obs_websocket == None
        assert obs_integration.virtual_camera == None
        assert obs_integration.frame_buffer == []

    def test_default_config(self):
        """Test default configuration values"""
        service = OBSVirtualCameraIntegration()
        default_config = service.config

        assert default_config["obs_websocket_host"] == "localhost"
        assert default_config["obs_websocket_port"] == 4455
        assert default_config["frame_rate"] == 30
        assert default_config["resolution"] == (1920, 1080)
        assert default_config["buffer_size"] == 100

    @patch("web.multimedia.obs_integration.obswebsocket")
    def test_obs_websocket_connection_success(self, mock_obswebsocket, obs_integration):
        """Test successful OBS WebSocket connection"""
        # Mock successful connection
        mock_ws = Mock()
        mock_obswebsocket.obsws.return_value = mock_ws
        mock_ws.connect.return_value = None

        result = obs_integration._connect_obs_websocket()

        assert result == True
        assert obs_integration.obs_websocket == mock_ws
        mock_obswebsocket.obsws.assert_called_once()
        mock_ws.connect.assert_called_once()

    @patch("web.multimedia.obs_integration.obswebsocket")
    def test_obs_websocket_connection_failure(self, mock_obswebsocket, obs_integration):
        """Test failed OBS WebSocket connection"""
        # Mock connection failure
        mock_obswebsocket.obsws.side_effect = Exception("Connection failed")

        result = obs_integration._connect_obs_websocket()

        assert result == False
        assert obs_integration.obs_websocket == None

    @patch("web.multimedia.obs_integration.virtual_camera")
    def test_virtual_camera_setup_success(self, mock_virtual_camera, obs_integration):
        """Test successful virtual camera setup"""
        # Mock successful virtual camera setup
        mock_vc = Mock()
        mock_virtual_camera.VirtualCamera.return_value = mock_vc
        mock_vc.start.return_value = None

        result = obs_integration._setup_virtual_camera()

        assert result == True
        assert obs_integration.virtual_camera == mock_vc
        mock_virtual_camera.VirtualCamera.assert_called_once()
        mock_vc.start.assert_called_once()

    @patch("web.multimedia.obs_integration.virtual_camera")
    def test_virtual_camera_setup_failure(self, mock_virtual_camera, obs_integration):
        """Test failed virtual camera setup"""
        # Mock virtual camera setup failure
        mock_virtual_camera.VirtualCamera.side_effect = Exception("Setup failed")

        result = obs_integration._setup_virtual_camera()

        assert result == False
        assert obs_integration.virtual_camera == None

    def test_connect_to_obs_websocket_success(self, obs_integration):
        """Test successful OBS connection via WebSocket"""
        with patch.object(obs_integration, "_connect_obs_websocket", return_value=True):
            result = obs_integration.connect_to_obs()

            assert result == True
            assert obs_integration.is_connected == True

    def test_connect_to_obs_virtual_camera_fallback(self, obs_integration):
        """Test OBS connection fallback to virtual camera"""
        with patch.object(
            obs_integration, "_connect_obs_websocket", return_value=False
        ):
            with patch.object(
                obs_integration, "_setup_virtual_camera", return_value=True
            ):
                result = obs_integration.connect_to_obs()

                assert result == True
                assert obs_integration.is_connected == True

    def test_connect_to_obs_failure(self, obs_integration):
        """Test failed OBS connection"""
        with patch.object(
            obs_integration, "_connect_obs_websocket", return_value=False
        ):
            with patch.object(
                obs_integration, "_setup_virtual_camera", return_value=False
            ):
                result = obs_integration.connect_to_obs()

                assert result == False
                assert obs_integration.is_connected == False

    def test_disconnect_from_obs_success(self, obs_integration):
        """Test successful OBS disconnection"""
        # Setup connected state
        obs_integration.is_connected = True
        obs_integration.obs_websocket = Mock()
        obs_integration.virtual_camera = Mock()

        result = obs_integration.disconnect_from_obs()

        assert result == True
        assert obs_integration.is_connected == False

    def test_disconnect_from_obs_not_connected(self, obs_integration):
        """Test disconnection when not connected"""
        result = obs_integration.disconnect_from_obs()

        assert result == True
        assert obs_integration.is_connected == False

    def test_push_frame_to_obs_not_connected(self, obs_integration, mock_frame):
        """Test frame push when not connected to OBS"""
        with patch.object(obs_integration, "connect_to_obs", return_value=False):
            result = obs_integration.push_frame_to_obs(mock_frame)

            assert result == False

    def test_push_frame_to_obs_websocket_success(self, obs_integration, mock_frame):
        """Test successful frame push via WebSocket"""
        obs_integration.is_connected = True
        obs_integration.obs_websocket = Mock()

        with patch.object(obs_integration, "_push_frame_websocket", return_value=True):
            result = obs_integration.push_frame_to_obs(mock_frame)

            assert result == True
            assert len(obs_integration.frame_buffer) == 1

    def test_push_frame_to_obs_virtual_camera_success(
        self, obs_integration, mock_frame
    ):
        """Test successful frame push via virtual camera"""
        obs_integration.is_connected = True
        obs_integration.obs_websocket = None
        obs_integration.virtual_camera = Mock()

        with patch.object(
            obs_integration, "_push_frame_virtual_camera", return_value=True
        ):
            result = obs_integration.push_frame_to_obs(mock_frame)

            assert result == True
            assert len(obs_integration.frame_buffer) == 1

    def test_frame_buffer_management(self, obs_integration, mock_frame):
        """Test frame buffer size management"""
        obs_integration.is_connected = True
        obs_integration.virtual_camera = Mock()

        # Fill buffer beyond limit
        buffer_size = obs_integration.config["buffer_size"]
        for i in range(buffer_size + 10):
            with patch.object(
                obs_integration, "_push_frame_virtual_camera", return_value=True
            ):
                obs_integration.push_frame_to_obs(mock_frame)

        # Check buffer size is maintained
        assert len(obs_integration.frame_buffer) == buffer_size

    def test_frame_resizing(self, obs_integration, mock_frame):
        """Test frame resizing to match OBS resolution"""
        obs_integration.is_connected = True
        obs_integration.virtual_camera = Mock()
        target_resolution = obs_integration.config["resolution"]

        with patch.object(
            obs_integration, "_push_frame_virtual_camera", return_value=True
        ):
            obs_integration.push_frame_to_obs(mock_frame)

        # Check frame was resized
        resized_frame = obs_integration.frame_buffer[0]
        assert resized_frame.shape[:2] == target_resolution

    def test_start_streaming_success(self, obs_integration):
        """Test successful streaming start"""
        obs_integration.is_connected = True

        def mock_source():
            return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        with patch.object(obs_integration, "push_frame_to_obs", return_value=True):
            result = obs_integration.start_streaming(mock_source)

            assert result == True
            assert hasattr(obs_integration, "streaming_thread")
            assert obs_integration.streaming_thread.is_alive()

    def test_start_streaming_not_connected(self, obs_integration):
        """Test streaming start when not connected"""

        def mock_source():
            return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        result = obs_integration.start_streaming(mock_source)

        assert result == False

    def test_stop_streaming_success(self, obs_integration):
        """Test successful streaming stop"""
        obs_integration.is_connected = True
        obs_integration.streaming_thread = Mock()
        obs_integration.streaming_thread.is_alive.return_value = True
        obs_integration.streaming_thread.join.return_value = None

        result = obs_integration.stop_streaming()

        assert result == True
        assert obs_integration.is_connected == False

    def test_get_obs_status(self, obs_integration):
        """Test OBS status retrieval"""
        obs_integration.is_connected = True
        obs_integration.obs_websocket = Mock()
        obs_integration.virtual_camera = Mock()
        obs_integration.frame_buffer = [Mock()] * 5

        status = obs_integration.get_obs_status()

        assert status["is_connected"] == True
        assert status["websocket_connected"] == True
        assert status["virtual_camera_active"] == True
        assert status["frame_buffer_size"] == 5
        assert status["streaming_active"] == False

    def test_health_check_healthy(self, obs_integration):
        """Test health check when all services are healthy"""
        obs_integration.obs_websocket = Mock()
        obs_integration.virtual_camera = Mock()

        health = obs_integration.health_check()

        assert health["status"] == "healthy"
        assert "obs_websocket" in health["checks"]
        assert "virtual_camera" in health["checks"]
        assert health["checks"]["obs_websocket"]["status"] == "healthy"
        assert health["checks"]["virtual_camera"]["status"] == "healthy"

    def test_health_check_degraded(self, obs_integration):
        """Test health check when some services are unhealthy"""
        obs_integration.obs_websocket = None
        obs_integration.virtual_camera = None

        health = obs_integration.health_check()

        assert health["status"] == "degraded"
        assert health["checks"]["obs_websocket"]["status"] == "unhealthy"
        assert health["checks"]["virtual_camera"]["status"] == "unhealthy"

    def test_websocket_frame_push(self, obs_integration, mock_frame):
        """Test WebSocket frame push functionality"""
        obs_integration.obs_websocket = Mock()

        result = obs_integration._push_frame_websocket(mock_frame)

        assert result == True

    def test_virtual_camera_frame_push(self, obs_integration, mock_frame):
        """Test virtual camera frame push functionality"""
        obs_integration.virtual_camera = Mock()

        result = obs_integration._push_frame_virtual_camera(mock_frame)

        assert result == True
        obs_integration.virtual_camera.push_frame.assert_called_once()

    def test_virtual_camera_frame_push_failure(self, obs_integration, mock_frame):
        """Test virtual camera frame push failure"""
        obs_integration.virtual_camera = None

        result = obs_integration._push_frame_virtual_camera(mock_frame)

        assert result == False

    def test_auto_reconnect_configuration(self, obs_integration):
        """Test auto-reconnect configuration"""
        assert obs_integration.config["auto_reconnect"] == True
        assert obs_integration.config["reconnect_interval"] == 5

    def test_output_directory_creation(self, obs_integration):
        """Test OBS output directory creation"""
        # This test verifies that the output directory is created during initialization
        # The actual directory creation happens in _initialize_obs_integration
        assert (
            obs_integration.config.get("output_directory") is not None
            or "temp_directory" in obs_integration.config
        )


class TestOBSIntegrationPerformance:
    """Performance tests for OBS integration"""

    @pytest.fixture
    def performance_obs_integration(self):
        """OBS integration service for performance testing"""
        with patch("web.multimedia.obs_integration.HealthMonitorWeb"):
            service = OBSVirtualCameraIntegration()
            yield service

    def test_frame_push_performance(self, performance_obs_integration):
        """Test frame push performance"""
        performance_obs_integration.is_connected = True
        performance_obs_integration.virtual_camera = Mock()

        # Create test frame
        frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

        # Measure push performance
        start_time = time.time()
        with patch.object(
            performance_obs_integration, "_push_frame_virtual_camera", return_value=True
        ):
            for _ in range(100):
                performance_obs_integration.push_frame_to_obs(frame)

        end_time = time.time()
        total_time = end_time - start_time

        # Performance should be reasonable (less than 1 second for 100 frames)
        assert total_time < 1.0

    def test_buffer_performance(self, performance_obs_integration):
        """Test buffer management performance"""
        performance_obs_integration.is_connected = True
        performance_obs_integration.virtual_camera = Mock()

        # Create test frame
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        # Measure buffer performance
        start_time = time.time()
        with patch.object(
            performance_obs_integration, "_push_frame_virtual_camera", return_value=True
        ):
            for _ in range(1000):
                performance_obs_integration.push_frame_to_obs(frame)

        end_time = time.time()
        total_time = end_time - start_time

        # Performance should be reasonable (less than 5 seconds for 1000 frames)
        assert total_time < 5.0
        # Buffer size should be maintained
        assert (
            len(performance_obs_integration.frame_buffer)
            <= performance_obs_integration.config["buffer_size"]
        )


class TestOBSIntegrationErrorHandling:
    """Error handling tests for OBS integration"""

    @pytest.fixture
    def error_obs_integration(self):
        """OBS integration service for error testing"""
        with patch("web.multimedia.obs_integration.HealthMonitorWeb"):
            service = OBSVirtualCameraIntegration()
            yield service

    def test_websocket_connection_error_handling(self, error_obs_integration):
        """Test WebSocket connection error handling"""
        with patch("web.multimedia.obs_integration.obswebsocket") as mock_obswebsocket:
            mock_obswebsocket.obsws.side_effect = Exception("Network error")

            result = error_obs_integration._connect_obs_websocket()

            assert result == False

    def test_virtual_camera_error_handling(self, error_obs_integration):
        """Test virtual camera error handling"""
        with patch(
            "web.multimedia.obs_integration.virtual_camera"
        ) as mock_virtual_camera:
            mock_virtual_camera.VirtualCamera.side_effect = Exception("Driver error")

            result = error_obs_integration._setup_virtual_camera()

            assert result == False

    def test_frame_push_error_handling(self, error_obs_integration, mock_frame):
        """Test frame push error handling"""
        error_obs_integration.is_connected = True
        error_obs_integration.virtual_camera = Mock()

        with patch.object(
            error_obs_integration,
            "_push_frame_virtual_camera",
            side_effect=Exception("Push error"),
        ):
            result = error_obs_integration.push_frame_to_obs(mock_frame)

            assert result == False

    def test_streaming_error_handling(self, error_obs_integration):
        """Test streaming error handling"""
        error_obs_integration.is_connected = True

        def error_source():
            raise Exception("Source error")

        with patch.object(
            error_obs_integration, "push_frame_to_obs", return_value=True
        ):
            result = error_obs_integration.start_streaming(error_source)

            assert result == True
            # Wait a bit for streaming to start and encounter error
            time.sleep(0.1)

            # Stop streaming
            error_obs_integration.stop_streaming()
