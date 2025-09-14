from __future__ import annotations

from typing import Any

from .contracts import Engine, EngineContext, EngineResult


class CommunicationCoreEngine(Engine):
    """Core communication engine - consolidates all communication operations."""

    def __init__(self):
        self.channels: dict[str, Any] = {}
        self.messages: list[dict[str, Any]] = []
        self.is_initialized = False

    def initialize(self, context: EngineContext) -> bool:
        """Initialize communication core engine."""
        try:
            self.is_initialized = True
            context.logger.info("Communication Core Engine initialized")
            return True
        except Exception as e:
            context.logger.error(f"Failed to initialize Communication Core Engine: {e}")
            return False

    def execute(self, context: EngineContext, payload: dict[str, Any]) -> EngineResult:
        """Execute communication operation based on payload type."""
        try:
            operation = payload.get("operation", "unknown")

            if operation == "send":
                return self._send_message(context, payload)
            elif operation == "receive":
                return self._receive_message(context, payload)
            elif operation == "broadcast":
                return self._broadcast_message(context, payload)
            else:
                return EngineResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown communication operation: {operation}",
                )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def _send_message(self, context: EngineContext, payload: dict[str, Any]) -> EngineResult:
        """Send message through communication channel."""
        try:
            channel_id = payload.get("channel_id", "default")
            message = payload.get("message", "")
            recipient = payload.get("recipient", "unknown")

            message_data = {
                "channel_id": channel_id,
                "message": message,
                "recipient": recipient,
                "timestamp": context.metrics.get("timestamp", 0),
                "status": "sent",
            }

            self.messages.append(message_data)

            return EngineResult(success=True, data=message_data, metrics={"channel_id": channel_id})
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def _receive_message(self, context: EngineContext, payload: dict[str, Any]) -> EngineResult:
        """Receive message from communication channel."""
        try:
            channel_id = payload.get("channel_id", "default")

            # Simplified receive logic - return last message
            if self.messages:
                last_message = self.messages[-1]
                return EngineResult(
                    success=True, data=last_message, metrics={"channel_id": channel_id}
                )
            else:
                return EngineResult(
                    success=True,
                    data={"message": "No messages available"},
                    metrics={"channel_id": channel_id},
                )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def _broadcast_message(self, context: EngineContext, payload: dict[str, Any]) -> EngineResult:
        """Broadcast message to multiple channels."""
        try:
            message = payload.get("message", "")
            channels = payload.get("channels", ["default"])

            broadcast_results = []
            for channel_id in channels:
                message_data = {
                    "channel_id": channel_id,
                    "message": message,
                    "timestamp": context.metrics.get("timestamp", 0),
                    "status": "broadcast",
                }
                broadcast_results.append(message_data)
                self.messages.append(message_data)

            return EngineResult(
                success=True,
                data={"broadcast_results": broadcast_results},
                metrics={"channels_broadcast": len(channels)},
            )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: EngineContext) -> bool:
        """Cleanup communication core engine."""
        try:
            self.channels.clear()
            self.messages.clear()
            self.is_initialized = False
            context.logger.info("Communication Core Engine cleaned up")
            return True
        except Exception as e:
            context.logger.error(f"Failed to cleanup Communication Core Engine: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get communication core engine status."""
        return {
            "initialized": self.is_initialized,
            "channels_count": len(self.channels),
            "messages_count": len(self.messages),
        }
