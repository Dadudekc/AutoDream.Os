#!/usr/bin/env python3
"""
Message Queue System - Agent Cellphone V2
=========================================

Persistent message queuing system for reliable message delivery.
Stores messages when immediate delivery fails and processes them asynchronously.

Features:
- Persistent queue storage with atomic operations
- Priority-based message processing
- Automatic retry with exponential backoff
- Queue statistics and monitoring
- Integration with file locking system

Architecture:
- Repository Pattern: MessageQueue handles persistent storage
- Service Layer: QueueProcessor orchestrates delivery attempts
- Dependency Injection: Modular components injected via constructor

@maintainer Agent-3 (Infrastructure & DevOps Specialist)
@license MIT
"""


logger = get_messaging_logger()


class MessageQueue:
    """Persistent message queue with atomic operations and priority processing.

    Provides reliable message queuing with automatic retry and cleanup. Integrates with
    file locking system for thread-safe operations.
    """

    def __init__(
        self,
        config: Optional[QueueConfig] = None,
        lock_config: Optional[LockConfig] = None,
    ):
        """Initialize message queue with configuration."""
        self.config = config or QueueConfig()
        self.lock_config = lock_config or LockConfig()
        self.lock_manager = FileLockManager(self.lock_config)
        self.queue_file = (
            get_unified_utility().Path(self.config.queue_directory) / "queue.json"
        )
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)

        # Validate configuration
        config_issues = MessageQueueUtils.validate_queue_config(self.config)
        if config_issues:
            get_unified_validator().raise_validation_error(
                f"Invalid queue configuration: {', '.join(config_issues)}"
            )

    def enqueue(
        self,
        message: UnifiedMessage,
        delivery_callback: Optional[Callable[[UnifiedMessage], bool]] = None,
    ) -> str:
        """Add message to queue with priority-based ordering.

        Args:
            message: Message to queue
            delivery_callback: Optional callback for delivery attempts

        Returns:
            Queue ID for tracking
        """
        queue_id = str(uuid.uuid4())
        now = datetime.now()

        # Calculate priority score
        priority_score = MessageQueueUtils.calculate_priority_score(
            message.priority.value, now
        )

        # Create queue entry
        entry = QueueEntry(
            message=message,
            queue_id=queue_id,
            priority_score=priority_score,
            status=QueueStatus.PENDING,
            created_at=now,
            updated_at=now,
            metadata={"delivery_callback": delivery_callback is not None},
        )

        # Atomic enqueue operation
        def _enqueue_operation():
            entries = self._load_entries()

            # Check queue size limit
            if len(entries) >= self.config.max_queue_size:
                raise RuntimeError(
                    f"Queue size limit exceeded: {self.config.max_queue_size}"
                )

            entries.append(entry)
            self._save_entries(entries)

            get_logger(__name__).info(
                f"Message queued: {queue_id} (priority: {message.priority.value})"
            )
            return queue_id

        return atomic_file_operation(
            self.queue_file, _enqueue_operation, self.lock_manager
        )

    def dequeue(self, batch_size: Optional[int] = None) -> List[QueueEntry]:
        """Get next messages for processing based on priority.

        Args:
            batch_size: Number of messages to retrieve (defaults to config)

        Returns:
            List of queue entries ready for processing
        """
        batch_size = batch_size or self.config.processing_batch_size

        def _dequeue_operation():
            entries = self._load_entries()

            # Build priority heap
            heap = MessageQueueUtils.build_priority_heap(entries)

            # Get next entries for processing
            entries_to_process = MessageQueueUtils.get_next_entries_for_processing(
                heap, batch_size, self.config.max_age_days
            )

            # Mark entries as processing
            for entry in entries_to_process:
                MessageQueueUtils.mark_entry_processing(entry)

            # Save updated entries
            self._save_entries(entries)

            get_logger(__name__).info(
                f"Dequeued {len(entries_to_process)} messages for processing"
            )
            return entries_to_process

        return atomic_file_operation(
            self.queue_file, _dequeue_operation, self.lock_manager
        )

    def mark_delivered(self, queue_id: str) -> bool:
        """Mark message as successfully delivered."""

        def _mark_delivered_operation():
            entries = self._load_entries()

            for entry in entries:
                if entry.queue_id == queue_id:
                    MessageQueueUtils.mark_entry_delivered(entry)
                    self._save_entries(entries)
                    get_logger(__name__).info(
                        f"Message marked as delivered: {queue_id}"
                    )
                    return True

            get_logger(__name__).warning(f"Queue entry not found: {queue_id}")
            return False

        return atomic_file_operation(
            self.queue_file, _mark_delivered_operation, self.lock_manager
        )

    def mark_failed(self, queue_id: str, error: str) -> bool:
        """Mark message as failed and schedule retry."""

        def _mark_failed_operation():
            entries = self._load_entries()

            for entry in entries:
                if entry.queue_id == queue_id:
                    MessageQueueUtils.mark_entry_failed(entry, error)

                    # Update for retry if attempts remaining
                    if entry.delivery_attempts < entry.max_attempts:
                        MessageQueueUtils.update_entry_for_retry(
                            entry,
                            self.config.retry_base_delay,
                            self.config.retry_max_delay,
                        )

                    self._save_entries(entries)
                    get_logger(__name__).warning(
                        f"Message marked as failed: {queue_id} - {error}"
                    )
                    return True

            get_logger(__name__).warning(f"Queue entry not found: {queue_id}")
            return False

        return atomic_file_operation(
            self.queue_file, _mark_failed_operation, self.lock_manager
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive queue statistics."""

        def _get_statistics_operation():
            entries = self._load_entries()
            return MessageQueueUtils.calculate_queue_statistics(entries)

        return atomic_file_operation(
            self.queue_file, _get_statistics_operation, self.lock_manager
        )

    def cleanup_expired(self) -> int:
        """Remove expired entries from queue."""

        def _cleanup_operation():
            entries = self._load_entries()
            original_count = len(entries)

            active_entries = MessageQueueUtils.cleanup_expired_entries(
                entries, self.config.max_age_days
            )

            expired_count = original_count - len(active_entries)
            self._save_entries(active_entries)

            if expired_count > 0:
                get_logger(__name__).info(f"Cleaned up {expired_count} expired entries")

            return expired_count

        return atomic_file_operation(
            self.queue_file, _cleanup_operation, self.lock_manager
        )

    def _load_entries(self) -> List[QueueEntry]:
        """Load queue entries from persistent storage."""
        if not self.queue_file.exists():
            return []

        try:
            with open(self.queue_file, "r", encoding="utf-8") as f:
                data = read_json(f)

            return [QueueEntry.from_dict(entry_data) for entry_data in data]
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            get_logger(__name__).error(f"Failed to load queue entries: {e}")
            return []

    def _save_entries(self, entries: List[QueueEntry]) -> None:
        """Save queue entries to persistent storage."""
        try:
            data = [entry.to_dict() for entry in entries]

            # Write to temporary file first, then atomic move
            temp_file = self.queue_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                write_json(data, f, indent=2, ensure_ascii=False)

            temp_file.replace(self.queue_file)
        except Exception as e:
            get_logger(__name__).error(f"Failed to save queue entries: {e}")
            raise


class QueueProcessor:
    """Asynchronous queue processor for message delivery.

    Processes queued messages with retry logic and error handling.
    """

    def __init__(
        self, queue: MessageQueue, delivery_callback: Callable[[UnifiedMessage], bool]
    ):
        """Initialize queue processor with delivery callback."""
        self.queue = queue
        self.delivery_callback = delivery_callback
        self.running = False
        self.last_cleanup = time.time()

    async def start_processing(self, interval: float = 5.0) -> None:
        """Start continuous queue processing."""
        self.running = True
        get_logger(__name__).info("Queue processor started")

        while self.running:
            try:
                await self._process_batch()
                await self._cleanup_if_needed()
                await asyncio.sleep(interval)
            except Exception as e:
                get_logger(__name__).error(f"Queue processing error: {e}")
                await asyncio.sleep(interval)

    def stop_processing(self) -> None:
        """Stop queue processing."""
        self.running = False
        get_logger(__name__).info("Queue processor stopped")

    async def _process_batch(self) -> None:
        """Process a batch of queued messages."""
        entries = self.queue.dequeue()

        for entry in entries:
            try:
                success = self.delivery_callback(entry.message)

                if success:
                    self.queue.mark_delivered(entry.queue_id)
                else:
                    self.queue.mark_failed(
                        entry.queue_id, "Delivery callback returned False"
                    )

            except Exception as e:
                self.queue.mark_failed(entry.queue_id, str(e))

    async def _cleanup_if_needed(self) -> None:
        """Perform cleanup if interval has passed."""
        now = time.time()
        if now - self.last_cleanup >= self.queue.config.cleanup_interval:
            expired_count = self.queue.cleanup_expired()
            if expired_count > 0:
                get_logger(__name__).info(
                    f"Cleanup completed: {expired_count} expired entries removed"
                )
            self.last_cleanup = now
