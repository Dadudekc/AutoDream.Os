"""Message sending interface."""

from abc import ABC, abstractmethod


class IMessageSender(ABC):
    """Interface for message sending capabilities."""

    @abstractmethod
    def send_message(self, recipient: str, message_content: str) -> bool:
        """Send a message to a recipient.

        Args:
            recipient: Target recipient identifier.
            message_content: Message payload.

        Returns:
            ``True`` if the message was sent successfully.
        """
        raise NotImplementedError("send_message must be implemented by subclasses")
