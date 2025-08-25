"""
Middleware Tools for Agent_Cellphone_V2_Repository
Provides advanced middleware capabilities for message queuing, caching, and data transformation.
"""

import asyncio
import json
import logging
import pickle
import time

from src.utils.stability_improvements import stability_manager, safe_import
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Union, TypeVar, Generic
from pathlib import Path
import hashlib
import threading
import weakref
from core.cache.cache_manager import CacheManager

# Configure logging
logger = logging.getLogger(__name__)

T = TypeVar("T")


class MessagePriority(Enum):
    """Message priority levels."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


@dataclass
class Message:
    """Represents a message in the queue."""

    id: str
    content: Any
    priority: MessagePriority
    timestamp: float
    source: str
    destination: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3


class MessageQueue:
    """Thread-safe message queue with priority support."""

    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.queues: Dict[MessagePriority, deque] = {
            priority: deque() for priority in MessagePriority
        }
        self.lock = threading.RLock()
        self.message_count = 0
        self._message_map: Dict[str, Message] = {}

    def enqueue(self, message: Message) -> bool:
        """Add a message to the queue."""
        with self.lock:
            if self.message_count >= self.max_size:
                logger.warning(
                    "Message queue is full, dropping oldest low priority message"
                )
                self._drop_oldest_low_priority()

            self.queues[message.priority].append(message)
            self._message_map[message.id] = message
            self.message_count += 1
            logger.debug(
                f"Enqueued message {message.id} with priority {message.priority.name}"
            )
            return True

    def dequeue(self) -> Optional[Message]:
        """Get the next message from the queue (highest priority first)."""
        with self.lock:
            for priority in reversed(list(MessagePriority)):
                if self.queues[priority]:
                    message = self.queues[priority].popleft()
                    del self._message_map[message.id]
                    self.message_count -= 1
                    logger.debug(
                        f"Dequeued message {message.id} with priority {message.priority.name}"
                    )
                    return message
            return None

    def peek(self) -> Optional[Message]:
        """Peek at the next message without removing it."""
        with self.lock:
            for priority in reversed(list(MessagePriority)):
                if self.queues[priority]:
                    return self.queues[priority][0]
            return None

    def _drop_oldest_low_priority(self):
        """Drop the oldest low priority message to make room."""
        for priority in MessagePriority:
            if self.queues[priority]:
                message = self.queues[priority].popleft()
                del self._message_map[message.id]
                self.message_count -= 1
                logger.info(f"Dropped low priority message {message.id} to make room")
                break

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status."""
        with self.lock:
            return {
                "total_messages": self.message_count,
                "max_size": self.max_size,
                "priority_counts": {
                    priority.name: len(queue) for priority, queue in self.queues.items()
                },
            }

    def clear(self):
        """Clear all messages from the queue."""
        with self.lock:
            for queue in self.queues.values():
                queue.clear()
            self._message_map.clear()
            self.message_count = 0
            logger.info("Message queue cleared")




class DataTransformer:
    """Handles data transformation and validation."""

    def __init__(self):
        self.transformers: Dict[str, Callable] = {}
        self.validators: Dict[str, Callable] = {}
        self._register_default_transformers()

    def _register_default_transformers(self):
        """Register default data transformers."""
        self.register_transformer("json", self._json_transform)
        self.register_transformer("pickle", self._pickle_transform)
        self.register_transformer("base64", self._base64_transform)
        self.register_transformer("hash", self._hash_transform)

    def register_transformer(self, name: str, transformer: Callable):
        """Register a custom data transformer."""
        self.transformers[name] = transformer
        logger.info(f"Registered transformer: {name}")

    def register_validator(self, name: str, validator: Callable):
        """Register a custom data validator."""
        self.validators[name] = validator
        logger.info(f"Registered validator: {name}")

    def transform(self, data: Any, format_name: str, **kwargs) -> Any:
        """Transform data using the specified format."""
        if format_name not in self.transformers:
            raise ValueError(f"Unknown transformer: {format_name}")

        try:
            return self.transformers[format_name](data, **kwargs)
        except Exception as e:
            logger.error(f"Transformation failed for {format_name}: {str(e)}")
            raise

    def validate(self, data: Any, validator_name: str, **kwargs) -> bool:
        """Validate data using the specified validator."""
        if validator_name not in self.validators:
            raise ValueError(f"Unknown validator: {validator_name}")

        try:
            return self.validators[validator_name](data, **kwargs)
        except Exception as e:
            logger.error(f"Validation failed for {validator_name}: {str(e)}")
            return False

    def _json_transform(self, data: Any, **kwargs) -> str:
        """Transform data to JSON."""
        return json.dumps(data, **kwargs)

    def _pickle_transform(self, data: Any, **kwargs) -> bytes:
        """Transform data using pickle."""
        return pickle.dumps(data, **kwargs)

    def _base64_transform(self, data: Any, **kwargs) -> str:
        """Transform data to base64 (placeholder)."""
        import base64

        if isinstance(data, str):
            return base64.b64encode(data.encode()).decode()
        elif isinstance(data, bytes):
            return base64.b64encode(data).decode()
        else:
            return base64.b64encode(pickle.dumps(data)).decode()

    def _hash_transform(self, data: Any, algorithm: str = "sha256", **kwargs) -> str:
        """Transform data to hash."""
        if algorithm == "sha256":
            hasher = hashlib.sha256()
        elif algorithm == "md5":
            hasher = hashlib.md5()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")

        if isinstance(data, str):
            hasher.update(data.encode())
        elif isinstance(data, bytes):
            hasher.update(data)
        else:
            hasher.update(pickle.dumps(data))

        return hasher.hexdigest()


class CircuitBreaker:
    """Circuit breaker pattern implementation for fault tolerance."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.lock = threading.RLock()

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        with self.lock:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                    logger.info("Circuit breaker moved to HALF_OPEN state")
                else:
                    raise Exception("Circuit breaker is OPEN")

            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise

    def _on_success(self):
        """Handle successful function call."""
        with self.lock:
            self.failure_count = 0
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                logger.info("Circuit breaker moved to CLOSED state")

    def _on_failure(self):
        """Handle failed function call."""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.warning(
                    f"Circuit breaker opened after {self.failure_count} failures"
                )

    def get_state(self) -> str:
        """Get current circuit breaker state."""
        return self.state

    def reset(self):
        """Reset circuit breaker to CLOSED state."""
        with self.lock:
            self.state = "CLOSED"
            self.failure_count = 0
            self.last_failure_time = 0


class RetryMiddleware:
    """Retry middleware with exponential backoff."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = self.base_delay * (2**attempt)
                    logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All {self.max_retries + 1} attempts failed")
                    break

        raise last_exception


# Global instances
message_queue = MessageQueue()
cache_manager = CacheManager()
data_transformer = DataTransformer()
retry_middleware = RetryMiddleware()


# Example usage and testing
async def example_usage():
    """Example usage of middleware tools."""

    # Test message queue
    message = Message(
        id="test_1",
        content="Hello World",
        priority=MessagePriority.HIGH,
        timestamp=time.time(),
        source="test",
        destination="test",
    )

    message_queue.enqueue(message)
    print("Message enqueued")

    # Test cache
    cache_manager.set("test_key", "test_value", ttl=60)
    cached_value = cache_manager.get("test_key")
    print(f"Cached value: {cached_value}")

    # Test data transformer
    json_data = data_transformer.transform({"key": "value"}, "json")
    print(f"JSON transformed: {json_data}")

    # Test circuit breaker
    def failing_function():
        raise Exception("Simulated failure")

    circuit_breaker = CircuitBreaker(failure_threshold=2)

    try:
        for i in range(3):
            circuit_breaker.call(failing_function)
    except Exception as e:
        print(f"Circuit breaker state: {circuit_breaker.get_state()}")

    # Test retry middleware
    def unreliable_function():
        import random

        if random.random() < 0.7:  # 70% failure rate
            raise Exception("Random failure")
        return "Success!"

    try:
        result = await retry_middleware.execute_with_retry(unreliable_function)
        print(f"Retry result: {result}")
    except Exception as e:
        print(f"Retry failed: {str(e)}")


if __name__ == "__main__":
    # Run example usage
    asyncio.run(example_usage())
