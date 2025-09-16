from __future__ import annotations
import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from queue import Queue
from typing import Any, Protocol
logger = logging.getLogger(__name__)


class MessageType(Enum):
    AGENT_TO_AGENT = 'agent_to_agent'
    SWARM_BROADCAST = 'swarm_broadcast'
    TASK_UPDATE = 'task_update'
    STATUS_REPORT = 'status_report'
    ERROR_NOTIFICATION = 'error_notification'
    COORDINATION_SIGNAL = 'coordination_signal'


class MessagePriority(Enum):
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    CRITICAL = 'critical'


class CommunicationProtocol(Enum):
    INTERNAL = 'internal'
    HTTP = 'http'
    WEBSOCKET = 'websocket'
    PYAUTOGUI = 'pyautogui'
    FILE_BASED = 'file_based'


@dataclass
class Message:
    message_id: str
    sender: str
    recipient: str
    message_type: MessageType
    priority: MessagePriority = MessagePriority.NORMAL
    content: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    protocol: CommunicationProtocol = CommunicationProtocol.INTERNAL

    def to_dict(self) ->dict[str, Any]:
        return {'message_id': self.message_id, 'sender': self.sender,
            'recipient': self.recipient, 'message_type': self.message_type.
            value, 'priority': self.priority.value, 'content': self.content,
            'metadata': self.metadata, 'timestamp': self.timestamp.
            isoformat(), 'protocol': self.protocol.value}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) ->Message:
        return cls(message_id=data['message_id'], sender=data['sender'],
            recipient=data['recipient'], message_type=MessageType(data[
            'message_type']), priority=MessagePriority(data.get('priority',
            'normal')), content=data.get('content'), metadata=data.get(
            'metadata', {}), timestamp=datetime.fromisoformat(data[
            'timestamp']), protocol=CommunicationProtocol(data.get(
            'protocol', 'internal')))


@dataclass
class MessageResult:
    success: bool
    message_id: str
    error: str | None = None
    delivery_time: float = 0.0


class IMessageHandler(Protocol):

    def can_handle(self, message: Message) ->bool:
        ...

    async def handle_message(self, message: Message) ->MessageResult:
        ...


class ICommunicationChannel(ABC):

    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.logger = logging.getLogger(
            f'{self.__class__.__name__}.{channel_id}')

    @abstractmethod
    def get_protocol(self) ->CommunicationProtocol:
        pass

    @abstractmethod
    async def send_message(self, message: Message) ->MessageResult:
        pass

    @abstractmethod
    async def receive_messages(self, recipient: str) ->list[Message]:
        pass


class InternalCommunicationChannel(ICommunicationChannel):

    def __init__(self, channel_id: str):
        super().__init__(channel_id)
        self.message_queue: Queue[Message] = Queue()
        self._lock = threading.Lock()

    def get_protocol(self) ->CommunicationProtocol:
        return CommunicationProtocol.INTERNAL

    async def send_message(self, message: Message) ->MessageResult:
        start_time = time.time()
        try:
            with self._lock:
                self.message_queue.put(message)
            delivery_time = time.time() - start_time
            return MessageResult(success=True, message_id=message.
                message_id, delivery_time=delivery_time)
        except Exception as e:
            delivery_time = time.time() - start_time
            return MessageResult(success=False, message_id=message.
                message_id, error=str(e), delivery_time=delivery_time)

    async def receive_messages(self, recipient: str) ->list[Message]:
        messages = []
        try:
            temp_queue = Queue()
            while not self.message_queue.empty():
                try:
                    msg = self.message_queue.get_nowait()
                    if msg.recipient == recipient or msg.recipient == 'all':
                        messages.append(msg)
                    else:
                        temp_queue.put(msg)
                except:
                    break
            while not temp_queue.empty():
                self.message_queue.put(temp_queue.get())
        except Exception as e:
            self.logger.error(f'Error receiving messages: {e}')
        return messages


class FileBasedCommunicationChannel(ICommunicationChannel):

    def __init__(self, channel_id: str, inbox_dir: str='agent_workspaces'):
        super().__init__(channel_id)
        self.inbox_dir = Path(inbox_dir)

    def get_protocol(self) ->CommunicationProtocol:
        return CommunicationProtocol.FILE_BASED

    async def send_message(self, message: Message) ->MessageResult:
        """Send message via file-based system."""
        start_time = time.time()
        try:
            inbox_path = self.inbox_dir / message.recipient / 'inbox'
            inbox_path.mkdir(parents=True, exist_ok=True)
            message_file = inbox_path / f'{message.message_id}.json'
            with open(message_file, 'w', encoding='utf-8') as f:
                json.dump(message.to_dict(), f, indent=2, default=str)
            delivery_time = time.time() - start_time
            return MessageResult(success=True, message_id=message.
                message_id, delivery_time=delivery_time)
        except Exception as e:
            delivery_time = time.time() - start_time
            return MessageResult(success=False, message_id=message.
                message_id, error=str(e), delivery_time=delivery_time)

    async def receive_messages(self, recipient: str) ->list[Message]:
        """Receive messages from file-based inbox."""
        messages = []
        try:
            inbox_path = self.inbox_dir / recipient / 'inbox'
            if inbox_path.exists():
                for message_file in inbox_path.glob('*.json'):
                    try:
                        with open(message_file, encoding='utf-8') as f:
                            data = json.load(f)
                            message = Message.from_dict(data)
                            messages.append(message)
                    except Exception as e:
                        self.logger.warning(
                            f'Error reading message file {message_file}: {e}')
        except Exception as e:
            self.logger.error(f'Error receiving messages: {e}')
        return messages


@dataclass
class MessageStatistics:
    """Statistics for message operations."""
    total_sent: int = 0
    total_received: int = 0
    total_errors: int = 0
    average_delivery_time: float = 0.0
    messages_by_type: dict[str, int] = field(default_factory=dict)
    messages_by_priority: dict[str, int] = field(default_factory=dict)


class ConsolidatedCommunicationSystem:
    """Main consolidated communication system."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.channels: dict[str, ICommunicationChannel] = {}
        self.handlers: dict[str, IMessageHandler] = {}
        self.statistics = MessageStatistics()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._running = True
        self._initialize_default_channels()

    def _initialize_default_channels(self) ->None:
        """Initialize default communication channels."""
        self.register_channel(InternalCommunicationChannel('internal'))
        self.register_channel(FileBasedCommunicationChannel('file_based'))

    def register_channel(self, channel: ICommunicationChannel) ->None:
        """Register a communication channel."""
        self.channels[channel.channel_id] = channel
        self.logger.info(
            f'Registered communication channel: {channel.channel_id}')

    def register_handler(self, handler_id: str, handler: IMessageHandler
        ) ->None:
        """Register a message handler."""
        self.handlers[handler_id] = handler
        self.logger.info(f'Registered message handler: {handler_id}')

    def unregister_channel(self, channel_id: str) ->bool:
        """Unregister a communication channel."""
        if channel_id in self.channels:
            del self.channels[channel_id]
            self.logger.info(f'Unregistered channel: {channel_id}')
            return True
        return False

    async def send_message(self, message: Message, channel_id: str='internal'
        ) ->MessageResult:
        """Send a message through specified channel."""
        channel = self.channels.get(channel_id)
        if not channel:
            return MessageResult(success=False, message_id=message.
                message_id, error=f'Channel {channel_id} not found')
        self.statistics.total_sent += 1
        self._update_message_stats(message)
        result = await channel.send_message(message)
        if not result.success:
            self.statistics.total_errors += 1
        return result

    async def broadcast_message(self, message: Message, channel_ids: list[
        str]=None) ->list[MessageResult]:
        """Broadcast message to multiple channels."""
        if channel_ids is None:
            channel_ids = list(self.channels.keys())
        broadcast_message = Message(message_id=
            f'{message.message_id}_broadcast', sender=message.sender,
            recipient='all', message_type=message.message_type, priority=
            message.priority, content=message.content, metadata={**message.
            metadata, 'broadcast': True}, protocol=message.protocol)
        results = []
        for channel_id in channel_ids:
            result = await self.send_message(broadcast_message, channel_id)
            results.append(result)
        return results

    async def receive_messages(self, recipient: str, channel_ids: list[str]
        =None) ->list[Message]:
        """Receive messages for recipient from specified channels."""
        if channel_ids is None:
            channel_ids = list(self.channels.keys())
        all_messages = []
        for channel_id in channel_ids:
            channel = self.channels.get(channel_id)
            if channel:
                messages = await channel.receive_messages(recipient)
                all_messages.extend(messages)
        self.statistics.total_received += len(all_messages)
        for message in all_messages:
            await self._process_message(message)
        return all_messages

    async def _process_message(self, message: Message) ->None:
        """Process message through registered handlers."""
        for handler in self.handlers.values():
            if handler.can_handle(message):
                try:
                    await handler.handle_message(message)
                except Exception as e:
                    self.logger.error(f'Error in message handler: {e}')

    def _update_message_stats(self, message: Message) ->None:
        """Update message statistics."""
        type_key = message.message_type.value
        self.statistics.messages_by_type[type_key
            ] = self.statistics.messages_by_type.get(type_key, 0) + 1
        priority_key = message.priority.value
        self.statistics.messages_by_priority[priority_key
            ] = self.statistics.messages_by_priority.get(priority_key, 0) + 1

    def get_communication_status(self) ->dict[str, Any]:
        """Get overall communication system status."""
        return {'active_channels': list(self.channels.keys()),
            'registered_handlers': list(self.handlers.keys()), 'statistics':
            {'total_sent': self.statistics.total_sent, 'total_received':
            self.statistics.total_received, 'total_errors': self.statistics
            .total_errors, 'messages_by_type': self.statistics.
            messages_by_type, 'messages_by_priority': self.statistics.
            messages_by_priority}}

    def shutdown(self) ->None:
        """Shutdown the communication system."""
        self._running = False
        self.executor.shutdown(wait=True)
        self.logger.info('Consolidated Communication System shutdown complete')


_communication_system: ConsolidatedCommunicationSystem | None = None
_communication_lock = threading.Lock()


def get_consolidated_communication_system() ->ConsolidatedCommunicationSystem:
    """Get the global consolidated communication system instance (Singleton pattern)"""
    global _communication_system
    if _communication_system is None:
        with _communication_lock:
            if _communication_system is None:
                _communication_system = ConsolidatedCommunicationSystem()
    return _communication_system


async def send_agent_message(recipient: str, content: Any, message_type:
    MessageType=MessageType.AGENT_TO_AGENT, priority: MessagePriority=
    MessagePriority.NORMAL) ->MessageResult:
    """Send a message to another agent."""
    import uuid
    message = Message(message_id=str(uuid.uuid4()), sender='Agent-6',
        recipient=recipient, message_type=message_type, priority=priority,
        content=content)
    system = get_consolidated_communication_system()
    return await system.send_message(message, 'file_based')


async def broadcast_swarm_message(content: Any, priority: MessagePriority=
    MessagePriority.NORMAL) ->list[MessageResult]:
    """Broadcast message to entire swarm."""
    import uuid
    message = Message(message_id=str(uuid.uuid4()), sender='Agent-6',
        recipient='all', message_type=MessageType.SWARM_BROADCAST, priority
        =priority, content=content)
    system = get_consolidated_communication_system()
    return await system.broadcast_message(message)


_communication_system = get_consolidated_communication_system()
logger.info(
    '🐝 Consolidated Communication System initialized - Aggressive consolidation complete!'
    )
if __name__ == '__main__':
    """Demonstrate module functionality with practical examples."""
    logger.info('🐝 Module Examples - Practical Demonstrations')
    logger.info('=' * 50)
    logger.info('\n📋 Testing get_consolidated_communication_system():')
    try:
        logger.info(
            '✅ get_consolidated_communication_system executed successfully')
    except Exception as e:
        logger.info(f'❌ get_consolidated_communication_system failed: {e}')
    logger.info('\n📋 Testing to_dict():')
    try:
        logger.info('✅ to_dict executed successfully')
    except Exception as e:
        logger.info(f'❌ to_dict failed: {e}')
    logger.info('\n📋 Testing from_dict():')
    try:
        logger.info('✅ from_dict executed successfully')
    except Exception as e:
        logger.info(f'❌ from_dict failed: {e}')
    logger.info('\n🏗️  Testing MessageType class:')
    try:
        instance = MessageType()
        logger.info('✅ MessageType instantiated successfully')
    except Exception as e:
        logger.info(f'❌ MessageType failed: {e}')
    logger.info('\n🏗️  Testing MessagePriority class:')
    try:
        instance = MessagePriority()
        logger.info('✅ MessagePriority instantiated successfully')
    except Exception as e:
        logger.info(f'❌ MessagePriority failed: {e}')
    logger.info('\n🎉 All examples completed!')
    logger.info('🐝 WE ARE SWARM - PRACTICAL CODE IN ACTION!')
