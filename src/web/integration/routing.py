from __future__ import annotations

from typing import Callable, Dict, Any


class MessageValidator:
    """Validates incoming messages according to protocol rules."""

    @staticmethod
    def validate_message(message: Dict[str, Any]) -> bool:
        required_fields = ["message_id", "timestamp", "sender_id", "message_type"]
        return all(field in message for field in required_fields)


class MessageRouter:
    """Routes messages to registered handlers."""

    def __init__(
        self,
        logger,
        send_response: Callable[[Dict[str, Any], bool, Dict[str, Any] | None], None]
        | None = None,
    ):
        self.logger = logger
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._send_response = send_response

    def register_handler(
        self, message_type: str, handler: Callable[[Dict[str, Any]], Any]
    ):
        """Register a handler for a specific message type."""
        self._handlers[message_type] = handler
        self.logger.info(f"Registered handler for message type: {message_type}")

    def route(self, message: Dict[str, Any]):
        """Route an incoming message to the appropriate handler."""
        if not MessageValidator.validate_message(message):
            self.logger.warning(f"Invalid message received: {message}")
            return

        handler = self._handlers.get(message["message_type"])
        if not handler:
            self.logger.warning(
                f"No handler registered for message type: {message['message_type']}"
            )
            return

        try:
            result = handler(message)
            if message.get("requires_response") and self._send_response:
                payload = {"result": result} if result is not None else None
                self._send_response(message, True, payload)
        except Exception as exc:
            self.logger.error(f"Error in message handler: {exc}")
            if message.get("requires_response") and self._send_response:
                self._send_response(
                    message,
                    False,
                    {"error": str(exc)},
                )
