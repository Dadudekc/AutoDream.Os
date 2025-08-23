"""
Test suite for Cross-System Communication Infrastructure
Comprehensive testing of all cross-system communication components.
"""

import pytest
import asyncio
import json
import time
import uuid
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pathlib import Path
import tempfile
import shutil

# Import the components we're testing
from src.services.cross_system_communication import (
    CrossSystemCommunicationManager,
    SystemEndpoint,
    CrossSystemMessage,
    CommunicationProtocol,
    MessageType,
    MessagePriority,
    CommunicationMetrics,
    HTTPCommunicationHandler,
    WebSocketCommunicationHandler,
    TCPCommunicationHandler,
    BaseCommunicationHandler,
)


class TestCommunicationProtocol:
    """Test suite for CommunicationProtocol enum."""

    def test_protocol_values(self):
        """Test that all protocol values are valid."""
        protocols = [
            CommunicationProtocol.HTTP,
            CommunicationProtocol.HTTPS,
            CommunicationProtocol.WEBSOCKET,
            CommunicationProtocol.TCP,
            CommunicationProtocol.UDP,
        ]

        for protocol in protocols:
            assert protocol.value in ["http", "https", "websocket", "tcp", "udp"]

    def test_protocol_from_string(self):
        """Test creating protocols from string values."""
        assert CommunicationProtocol("http") == CommunicationProtocol.HTTP
        assert CommunicationProtocol("https") == CommunicationProtocol.HTTPS
        assert CommunicationProtocol("websocket") == CommunicationProtocol.WEBSOCKET
        assert CommunicationProtocol("tcp") == CommunicationProtocol.TCP
        assert CommunicationProtocol("udp") == CommunicationProtocol.UDP


class TestMessageType:
    """Test suite for MessageType enum."""

    def test_message_type_values(self):
        """Test that all message type values are valid."""
        message_types = [
            MessageType.REQUEST,
            MessageType.RESPONSE,
            MessageType.EVENT,
            MessageType.COMMAND,
            MessageType.QUERY,
            MessageType.NOTIFICATION,
            MessageType.HEARTBEAT,
            MessageType.ERROR,
        ]

        for msg_type in message_types:
            assert msg_type.value in [
                "request",
                "response",
                "event",
                "command",
                "query",
                "notification",
                "heartbeat",
                "error",
            ]


class TestMessagePriority:
    """Test suite for MessagePriority enum."""

    def test_priority_values(self):
        """Test that all priority values are valid."""
        priorities = [
            MessagePriority.LOW,
            MessagePriority.NORMAL,
            MessagePriority.HIGH,
            MessagePriority.CRITICAL,
            MessagePriority.EMERGENCY,
        ]

        for priority in priorities:
            assert priority.value in [1, 2, 3, 4, 5]

    def test_priority_ordering(self):
        """Test that priority values are properly ordered."""
        assert MessagePriority.LOW.value < MessagePriority.NORMAL.value
        assert MessagePriority.NORMAL.value < MessagePriority.HIGH.value
        assert MessagePriority.HIGH.value < MessagePriority.CRITICAL.value
        assert MessagePriority.CRITICAL.value < MessagePriority.EMERGENCY.value


class TestSystemEndpoint:
    """Test suite for SystemEndpoint dataclass."""

    def test_system_endpoint_creation(self):
        """Test creating a system endpoint."""
        endpoint = SystemEndpoint(
            system_id="test_system",
            name="Test System",
            protocol=CommunicationProtocol.HTTP,
            host="localhost",
            port=8000,
        )

        assert endpoint.system_id == "test_system"
        assert endpoint.name == "Test System"
        assert endpoint.protocol == CommunicationProtocol.HTTP
        assert endpoint.host == "localhost"
        assert endpoint.port == 8000
        assert endpoint.path == ""
        assert endpoint.timeout == 30.0
        assert endpoint.retry_attempts == 3
        assert endpoint.health_check_interval == 60.0
        assert endpoint.is_healthy is True

    def test_system_endpoint_with_custom_values(self):
        """Test creating a system endpoint with custom values."""
        endpoint = SystemEndpoint(
            system_id="custom_system",
            name="Custom System",
            protocol=CommunicationProtocol.HTTPS,
            host="example.com",
            port=443,
            path="/api/v1",
            timeout=60.0,
            retry_attempts=5,
            health_check_interval=30.0,
            credentials={"api_key": "test_key"},
            metadata={"version": "1.0.0"},
        )

        assert endpoint.timeout == 60.0
        assert endpoint.retry_attempts == 5
        assert endpoint.health_check_interval == 30.0
        assert endpoint.credentials == {"api_key": "test_key"}
        assert endpoint.metadata == {"version": "1.0.0"}


class TestCrossSystemMessage:
    """Test suite for CrossSystemMessage dataclass."""

    def test_message_creation(self):
        """Test creating a cross-system message."""
        message = CrossSystemMessage(
            message_id="msg_123",
            source_system="system_a",
            target_system="system_b",
            message_type=MessageType.REQUEST,
            priority=MessagePriority.HIGH,
            timestamp=time.time(),
            payload={"data": "test"},
        )

        assert message.message_id == "msg_123"
        assert message.source_system == "system_a"
        assert message.target_system == "system_b"
        assert message.message_type == MessageType.REQUEST
        assert message.priority == MessagePriority.HIGH
        assert message.payload == {"data": "test"}
        assert message.headers == {}
        assert message.correlation_id is None
        assert message.reply_to is None
        assert message.ttl is None
        assert message.retry_count == 0
        assert message.max_retries == 3

    def test_message_with_optional_fields(self):
        """Test creating a message with optional fields."""
        message = CrossSystemMessage(
            message_id="msg_456",
            source_system="system_a",
            target_system="system_b",
            message_type=MessageType.RESPONSE,
            priority=MessagePriority.NORMAL,
            timestamp=time.time(),
            payload={"result": "success"},
            headers={"Content-Type": "application/json"},
            correlation_id="corr_123",
            reply_to="system_a",
            ttl=300.0,
            retry_count=1,
            max_retries=5,
        )

        assert message.headers == {"Content-Type": "application/json"}
        assert message.correlation_id == "corr_123"
        assert message.reply_to == "system_a"
        assert message.ttl == 300.0
        assert message.retry_count == 1
        assert message.max_retries == 5


class TestCommunicationMetrics:
    """Test suite for CommunicationMetrics dataclass."""

    def test_metrics_creation(self):
        """Test creating communication metrics."""
        metrics = CommunicationMetrics()

        assert metrics.total_messages_sent == 0
        assert metrics.total_messages_received == 0
        assert metrics.successful_communications == 0
        assert metrics.failed_communications == 0
        assert metrics.average_response_time == 0.0
        assert metrics.total_response_time == 0.0
        assert metrics.active_connections == 0
        assert metrics.error_count == 0

    def test_metrics_update(self):
        """Test updating metrics values."""
        metrics = CommunicationMetrics()

        metrics.total_messages_sent = 10
        metrics.total_messages_received = 8
        metrics.successful_communications = 9
        metrics.failed_communications = 1
        metrics.average_response_time = 0.5
        metrics.total_response_time = 5.0
        metrics.active_connections = 3
        metrics.error_count = 1

        assert metrics.total_messages_sent == 10
        assert metrics.total_messages_received == 8
        assert metrics.successful_communications == 9
        assert metrics.failed_communications == 1
        assert metrics.average_response_time == 0.5
        assert metrics.total_response_time == 5.0
        assert metrics.active_connections == 3
        assert metrics.error_count == 1


class TestBaseCommunicationHandler:
    """Test suite for BaseCommunicationHandler abstract class."""

    def test_abstract_class_instantiation(self):
        """Test that BaseCommunicationHandler cannot be instantiated."""
        with pytest.raises(TypeError):
            BaseCommunicationHandler(Mock())

    def test_abstract_methods(self):
        """Test that abstract methods are defined."""
        # This test ensures the abstract methods exist
        assert hasattr(BaseCommunicationHandler, "connect")
        assert hasattr(BaseCommunicationHandler, "disconnect")
        assert hasattr(BaseCommunicationHandler, "send_message")
        assert hasattr(BaseCommunicationHandler, "receive_message")


class TestHTTPCommunicationHandler:
    """Test suite for HTTPCommunicationHandler."""

    @pytest.fixture
    def http_endpoint(self):
        """Create a test HTTP endpoint."""
        return SystemEndpoint(
            system_id="test_http",
            name="Test HTTP",
            protocol=CommunicationProtocol.HTTP,
            host="localhost",
            port=8000,
        )

    @pytest.fixture
    def https_endpoint(self):
        """Create a test HTTPS endpoint."""
        return SystemEndpoint(
            system_id="test_https",
            name="Test HTTPS",
            protocol=CommunicationProtocol.HTTPS,
            host="localhost",
            port=8443,
        )

    @pytest.fixture
    def http_handler(self, http_endpoint):
        """Create a test HTTP handler."""
        return HTTPCommunicationHandler(http_endpoint)

    @pytest.fixture
    def https_handler(self, https_endpoint):
        """Create a test HTTPS handler."""
        return HTTPCommunicationHandler(https_endpoint)

    def test_handler_initialization(self, http_handler):
        """Test HTTP handler initialization."""
        assert http_handler.endpoint.protocol == CommunicationProtocol.HTTP
        assert http_handler.is_connected is False
        assert http_handler.session is None
        assert len(http_handler.error_callbacks) == 0
        assert len(http_handler.message_callbacks) == 0

    def test_ssl_context_setup_http(self, http_handler):
        """Test SSL context setup for HTTP."""
        # HTTP should not have SSL context
        assert not hasattr(http_handler, "ssl_context")

    def test_ssl_context_setup_https(self, https_handler):
        """Test SSL context setup for HTTPS."""
        # HTTPS should have SSL context
        assert hasattr(https_handler, "ssl_context")
        assert https_handler.ssl_context is not None

    @pytest.mark.asyncio
    async def test_connect_http(self, http_handler):
        """Test HTTP connection."""
        with patch("aiohttp.ClientSession") as mock_session:
            mock_session.return_value = AsyncMock()

            success = await http_handler.connect()

            assert success is True
            assert http_handler.is_connected is True
            assert http_handler.session is not None
            assert http_handler.connection_metrics.active_connections == 1

    @pytest.mark.asyncio
    async def test_connect_https(self, https_handler):
        """Test HTTPS connection."""
        with patch("aiohttp.ClientSession") as mock_session:
            mock_session.return_value = AsyncMock()

            success = await https_handler.connect()

            assert success is True
            assert https_handler.is_connected is True
            assert https_handler.session is not None
            assert https_handler.connection_metrics.active_connections == 1

    @pytest.mark.asyncio
    async def test_connect_failure(self, http_handler):
        """Test HTTP connection failure."""
        with patch("aiohttp.ClientSession", side_effect=Exception("Connection failed")):
            success = await http_handler.connect()

            assert success is False
            assert http_handler.is_connected is False
            assert http_handler.session is None

    @pytest.mark.asyncio
    async def test_disconnect(self, http_handler):
        """Test HTTP disconnection."""
        # First connect
        with patch("aiohttp.ClientSession") as mock_session:
            mock_session.return_value = AsyncMock()
            await http_handler.connect()

        # Then disconnect
        success = await http_handler.disconnect()

        assert success is True
        assert http_handler.is_connected is False
        assert http_handler.session is None
        assert http_handler.connection_metrics.active_connections == 0

    @pytest.mark.asyncio
    async def test_send_message_request(self, http_handler):
        """Test sending a request message."""
        # Setup mock session
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"status": "success"})

        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        http_handler.session = mock_session
        http_handler.is_connected = True

        # Create test message
        message = CrossSystemMessage(
            message_id="test_msg",
            source_system="test",
            target_system="target",
            message_type=MessageType.REQUEST,
            priority=MessagePriority.NORMAL,
            timestamp=time.time(),
            payload={"test": "data"},
        )

        # Send message
        success = await http_handler.send_message(message)

        assert success is True
        assert http_handler.connection_metrics.total_messages_sent == 1
        assert http_handler.connection_metrics.successful_communications == 1

    @pytest.mark.asyncio
    async def test_send_message_not_connected(self, http_handler):
        """Test sending message when not connected."""
        message = CrossSystemMessage(
            message_id="test_msg",
            source_system="test",
            target_system="target",
            message_type=MessageType.REQUEST,
            priority=MessagePriority.NORMAL,
            timestamp=time.time(),
            payload={"test": "data"},
        )

        success = await http_handler.send_message(message)

        assert success is False

    def test_add_callbacks(self, http_handler):
        """Test adding error and message callbacks."""

        def error_callback(error_msg, exception):
            pass

        def message_callback(message):
            pass

        http_handler.add_error_callback(error_callback)
        http_handler.add_message_callback(message_callback)

        assert len(http_handler.error_callbacks) == 1
        assert len(http_handler.message_callbacks) == 1
        assert http_handler.error_callbacks[0] == error_callback
        assert http_handler.message_callbacks[0] == message_callback


class TestWebSocketCommunicationHandler:
    """Test suite for WebSocketCommunicationHandler."""

    @pytest.fixture
    def websocket_endpoint(self):
        """Create a test WebSocket endpoint."""
        return SystemEndpoint(
            system_id="test_ws",
            name="Test WebSocket",
            protocol=CommunicationProtocol.WEBSOCKET,
            host="localhost",
            port=8080,
        )

    @pytest.fixture
    def websocket_handler(self, websocket_endpoint):
        """Create a test WebSocket handler."""
        return WebSocketCommunicationHandler(websocket_endpoint)

    def test_handler_initialization(self, websocket_handler):
        """Test WebSocket handler initialization."""
        assert websocket_handler.endpoint.protocol == CommunicationProtocol.WEBSOCKET
        assert websocket_handler.is_connected is False
        assert websocket_handler.websocket is None
        assert websocket_handler._receive_task is None

    @pytest.mark.asyncio
    async def test_connect_websocket(self, websocket_handler):
        """Test WebSocket connection."""
        with patch("websockets.connect") as mock_connect:
            mock_websocket = AsyncMock()
            mock_connect.return_value = mock_websocket

            success = await websocket_handler.connect()

            assert success is True
            assert websocket_handler.is_connected is True
            assert websocket_handler.websocket is not None
            assert websocket_handler._receive_task is not None
            assert websocket_handler.connection_metrics.active_connections == 1

    @pytest.mark.asyncio
    async def test_connect_websocket_failure(self, websocket_handler):
        """Test WebSocket connection failure."""
        with patch("websockets.connect", side_effect=Exception("Connection failed")):
            success = await websocket_handler.connect()

            assert success is False
            assert websocket_handler.is_connected is False
            assert websocket_handler.websocket is None

    @pytest.mark.asyncio
    async def test_disconnect_websocket(self, websocket_handler):
        """Test WebSocket disconnection."""
        # First connect
        with patch("websockets.connect") as mock_connect:
            mock_websocket = AsyncMock()
            mock_connect.return_value = mock_websocket
            await websocket_handler.connect()

        # Then disconnect
        success = await websocket_handler.disconnect()

        assert success is True
        assert websocket_handler.is_connected is False
        assert websocket_handler.websocket is None
        assert websocket_handler._receive_task is None
        assert websocket_handler.connection_metrics.active_connections == 0

    @pytest.mark.asyncio
    async def test_send_message(self, websocket_handler):
        """Test sending WebSocket message."""
        # Setup mock websocket
        mock_websocket = AsyncMock()
        websocket_handler.websocket = mock_websocket
        websocket_handler.is_connected = True

        # Create test message
        message = CrossSystemMessage(
            message_id="test_msg",
            source_system="test",
            target_system="target",
            message_type=MessageType.EVENT,
            priority=MessagePriority.NORMAL,
            timestamp=time.time(),
            payload={"test": "data"},
        )

        # Send message
        success = await websocket_handler.send_message(message)

        assert success is True
        assert websocket_handler.connection_metrics.total_messages_sent == 1
        mock_websocket.send.assert_called_once()


class TestTCPCommunicationHandler:
    """Test suite for TCPCommunicationHandler."""

    @pytest.fixture
    def tcp_endpoint(self):
        """Create a test TCP endpoint."""
        return SystemEndpoint(
            system_id="test_tcp",
            name="Test TCP",
            protocol=CommunicationProtocol.TCP,
            host="localhost",
            port=8000,
        )

    @pytest.fixture
    def tcp_handler(self, tcp_endpoint):
        """Create a test TCP handler."""
        return TCPCommunicationHandler(tcp_endpoint)

    def test_handler_initialization(self, tcp_handler):
        """Test TCP handler initialization."""
        assert tcp_handler.endpoint.protocol == CommunicationProtocol.TCP
        assert tcp_handler.is_connected is False
        assert tcp_handler.reader is None
        assert tcp_handler.writer is None
        assert tcp_handler._receive_task is None

    @pytest.mark.asyncio
    async def test_connect_tcp(self, tcp_handler):
        """Test TCP connection."""
        with patch("asyncio.open_connection") as mock_open_conn:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_open_conn.return_value = (mock_reader, mock_writer)

            success = await tcp_handler.connect()

            assert success is True
            assert tcp_handler.is_connected is True
            assert tcp_handler.reader is not None
            assert tcp_handler.writer is not None
            assert tcp_handler._receive_task is not None
            assert tcp_handler.connection_metrics.active_connections == 1

    @pytest.mark.asyncio
    async def test_connect_tcp_failure(self, tcp_handler):
        """Test TCP connection failure."""
        with patch(
            "asyncio.open_connection", side_effect=Exception("Connection failed")
        ):
            success = await tcp_handler.connect()

            assert success is False
            assert tcp_handler.is_connected is False
            assert tcp_handler.reader is None
            assert tcp_handler.writer is None

    @pytest.mark.asyncio
    async def test_disconnect_tcp(self, tcp_handler):
        """Test TCP disconnection."""
        # First connect
        with patch("asyncio.open_connection") as mock_open_conn:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_open_conn.return_value = (mock_reader, mock_writer)
            await tcp_handler.connect()

        # Then disconnect
        success = await tcp_handler.disconnect()

        assert success is True
        assert tcp_handler.is_connected is False
        assert tcp_handler.reader is None
        assert tcp_handler.writer is None
        assert tcp_handler._receive_task is None
        assert tcp_handler.connection_metrics.active_connections == 0


class TestCrossSystemCommunicationManager:
    """Test suite for CrossSystemCommunicationManager."""

    @pytest.fixture
    def communication_manager(self):
        """Create a test communication manager."""
        return CrossSystemCommunicationManager()

    @pytest.fixture
    def test_endpoint(self):
        """Create a test system endpoint."""
        return SystemEndpoint(
            system_id="test_system",
            name="Test System",
            protocol=CommunicationProtocol.HTTP,
            host="localhost",
            port=8000,
        )

    def test_manager_initialization(self, communication_manager):
        """Test communication manager initialization."""
        assert len(communication_manager.endpoints) == 0
        assert len(communication_manager.handlers) == 0
        assert communication_manager.running is False
        assert len(communication_manager.connection_callbacks) == 0
        assert len(communication_manager.message_callbacks) == 0
        assert len(communication_manager.error_callbacks) == 0

    def test_add_endpoint(self, communication_manager, test_endpoint):
        """Test adding a system endpoint."""
        success = communication_manager.add_endpoint(test_endpoint)

        assert success is True
        assert len(communication_manager.endpoints) == 1
        assert communication_manager.endpoints["test_system"] == test_endpoint

    def test_remove_endpoint(self, communication_manager, test_endpoint):
        """Test removing a system endpoint."""
        # First add endpoint
        communication_manager.add_endpoint(test_endpoint)

        # Then remove it
        success = communication_manager.remove_endpoint("test_system")

        assert success is True
        assert len(communication_manager.endpoints) == 0
        assert "test_system" not in communication_manager.endpoints

    def test_remove_nonexistent_endpoint(self, communication_manager):
        """Test removing a non-existent endpoint."""
        success = communication_manager.remove_endpoint("nonexistent")

        assert success is False

    @pytest.mark.asyncio
    async def test_start_manager(self, communication_manager):
        """Test starting the communication manager."""
        success = await communication_manager.start()

        assert success is True
        assert communication_manager.running is True
        assert communication_manager._message_processor_task is not None
        assert communication_manager._health_check_task is not None

    @pytest.mark.asyncio
    async def test_stop_manager(self, communication_manager):
        """Test stopping the communication manager."""
        # First start
        await communication_manager.start()

        # Then stop
        success = await communication_manager.stop()

        assert success is True
        assert communication_manager.running is False
        assert communication_manager._message_processor_task is None
        assert communication_manager._health_check_task is None

    def test_add_callbacks(self, communication_manager):
        """Test adding various callbacks."""

        def connection_callback(system_id, connected):
            pass

        def message_callback(message):
            pass

        def error_callback(error_msg, exception):
            pass

        communication_manager.add_connection_callback(connection_callback)
        communication_manager.add_message_callback(message_callback)
        communication_manager.add_error_callback(error_callback)

        assert len(communication_manager.connection_callbacks) == 1
        assert len(communication_manager.message_callbacks) == 1
        assert len(communication_manager.error_callbacks) == 1

    def test_get_system_status(self, communication_manager, test_endpoint):
        """Test getting system status."""
        communication_manager.add_endpoint(test_endpoint)

        status = communication_manager.get_system_status()

        assert "test_system" in status
        assert status["test_system"]["name"] == "Test System"
        assert status["test_system"]["protocol"] == "http"
        assert status["test_system"]["host"] == "localhost"
        assert status["test_system"]["port"] == 8000
        assert status["test_system"]["connected"] is False
        assert status["test_system"]["healthy"] is True

    def test_get_metrics(self, communication_manager):
        """Test getting communication metrics."""
        metrics = communication_manager.get_metrics()

        assert isinstance(metrics, CommunicationMetrics)
        assert metrics.total_messages_sent == 0
        assert metrics.total_messages_received == 0
        assert metrics.successful_communications == 0
        assert metrics.failed_communications == 0
        assert metrics.active_connections == 0


class TestIntegrationEndToEnd:
    """End-to-end integration tests."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_full_communication_workflow(self, temp_dir):
        """Test a complete communication workflow."""
        # Create communication manager
        manager = CrossSystemCommunicationManager()

        # Add test endpoints
        endpoint1 = SystemEndpoint(
            system_id="system_1",
            name="System 1",
            protocol=CommunicationProtocol.HTTP,
            host="localhost",
            port=8001,
        )

        endpoint2 = SystemEndpoint(
            system_id="system_2",
            name="System 2",
            protocol=CommunicationProtocol.HTTP,
            host="localhost",
            port=8002,
        )

        manager.add_endpoint(endpoint1)
        manager.add_endpoint(endpoint2)

        # Start manager
        await manager.start()

        try:
            # Verify endpoints are loaded
            assert len(manager.endpoints) == 2
            assert "system_1" in manager.endpoints
            assert "system_2" in manager.endpoints

            # Verify manager is running
            assert manager.running is True

            # Get status
            status = manager.get_system_status()
            assert len(status) == 2

            # Get metrics
            metrics = manager.get_metrics()
            assert isinstance(metrics, CommunicationMetrics)

        finally:
            # Cleanup
            await manager.stop()
            assert manager.running is False

    @pytest.mark.asyncio
    async def test_message_creation_and_validation(self):
        """Test message creation and validation workflow."""
        # Create test message
        message = CrossSystemMessage(
            message_id=f"test_{uuid.uuid4().hex[:8]}",
            source_system="test_source",
            target_system="test_target",
            message_type=MessageType.REQUEST,
            priority=MessagePriority.HIGH,
            timestamp=time.time(),
            payload={"test": "data", "timestamp": time.time()},
            correlation_id="test_correlation_123",
        )

        # Validate message structure
        assert message.message_id.startswith("test_")
        assert message.source_system == "test_source"
        assert message.target_system == "test_target"
        assert message.message_type == MessageType.REQUEST
        assert message.priority == MessagePriority.HIGH
        assert message.payload["test"] == "data"
        assert message.correlation_id == "test_correlation_123"

        # Test message priority ordering
        assert message.priority.value > MessagePriority.NORMAL.value
        assert message.priority.value < MessagePriority.CRITICAL.value

    @pytest.mark.asyncio
    async def test_protocol_handling(self):
        """Test different protocol handling."""
        protocols = [
            CommunicationProtocol.HTTP,
            CommunicationProtocol.HTTPS,
            CommunicationProtocol.WEBSOCKET,
            CommunicationProtocol.TCP,
        ]

        for protocol in protocols:
            endpoint = SystemEndpoint(
                system_id=f"test_{protocol.value}",
                name=f"Test {protocol.value.upper()}",
                protocol=protocol,
                host="localhost",
                port=8000,
            )

            # Verify endpoint creation
            assert endpoint.protocol == protocol
            assert endpoint.system_id == f"test_{protocol.value}"
            assert endpoint.name == f"Test {protocol.value.upper()}"

            # Verify protocol-specific settings
            if protocol in [CommunicationProtocol.HTTP, CommunicationProtocol.HTTPS]:
                assert endpoint.path == ""
            elif protocol == CommunicationProtocol.WEBSOCKET:
                assert endpoint.path == ""
            elif protocol == CommunicationProtocol.TCP:
                assert endpoint.path == ""


class TestPerformanceAndLoad:
    """Performance and load testing."""

    @pytest.mark.asyncio
    async def test_message_queue_performance(self):
        """Test message queue performance under load."""
        manager = CrossSystemCommunicationManager()

        # Create many messages
        messages = []
        for i in range(100):
            message = CrossSystemMessage(
                message_id=f"msg_{i}",
                source_system="source",
                target_system="target",
                message_type=MessageType.EVENT,
                priority=MessagePriority.NORMAL,
                timestamp=time.time(),
                payload={"index": i, "data": f"test_data_{i}"},
            )
            messages.append(message)

        # Test message creation performance
        start_time = time.time()
        for message in messages:
            # Simulate message processing
            assert message.message_id.startswith("msg_")
            assert message.payload["index"] >= 0
            assert message.payload["index"] < 100

        end_time = time.time()
        processing_time = end_time - start_time

        # Should process 100 messages in reasonable time
        assert processing_time < 1.0  # Less than 1 second for 100 messages
        assert len(messages) == 100

    @pytest.mark.asyncio
    async def test_endpoint_management_performance(self):
        """Test endpoint management performance."""
        manager = CrossSystemCommunicationManager()

        # Add many endpoints
        start_time = time.time()
        for i in range(50):
            endpoint = SystemEndpoint(
                system_id=f"system_{i}",
                name=f"System {i}",
                protocol=CommunicationProtocol.HTTP,
                host="localhost",
                port=8000 + i,
            )
            manager.add_endpoint(endpoint)

        end_time = time.time()
        add_time = end_time - start_time

        # Should add 50 endpoints in reasonable time
        assert add_time < 0.1  # Less than 100ms for 50 endpoints
        assert len(manager.endpoints) == 50

        # Test status retrieval performance
        start_time = time.time()
        status = manager.get_system_status()
        end_time = time.time()
        status_time = end_time - start_time

        # Should get status in reasonable time
        assert status_time < 0.01  # Less than 10ms for status
        assert len(status) == 50


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
