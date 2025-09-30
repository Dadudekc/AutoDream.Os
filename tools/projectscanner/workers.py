"""
Project Scanner Workers
======================

Multi-threaded processing workers for project scanning.
"""

import logging
import queue
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class BotWorker(threading.Thread):
    """Worker thread for processing files."""

    def __init__(self, worker_id: int, work_queue: queue.Queue, result_queue: queue.Queue):
        """Initialize worker thread."""
        super().__init__(daemon=True)
        self.worker_id = worker_id
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.running = False

        logger.debug(f"Initialized BotWorker {worker_id}")

    def run(self) -> None:
        """Main worker loop."""
        self.running = True
        logger.debug(f"BotWorker {self.worker_id} started")

        while self.running:
            try:
                # Get work item from queue
                work_item = self.work_queue.get(timeout=1.0)

                if work_item is None:  # Shutdown signal
                    break

                # Process work item
                result = self._process_work_item(work_item)

                # Put result in result queue
                self.result_queue.put(result)

                # Mark work item as done
                self.work_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"BotWorker {self.worker_id} error: {e}")
                self.work_queue.task_done()

        logger.debug(f"BotWorker {self.worker_id} stopped")

    def _process_work_item(self, work_item: dict[str, Any]) -> dict[str, Any]:
        """Process a single work item."""
        try:
            file_path = Path(work_item["file_path"])
            processor_func = work_item["processor"]

            # Process the file
            result = processor_func(file_path)

            return {
                "worker_id": self.worker_id,
                "file_path": str(file_path),
                "result": result,
                "status": "success",
            }

        except Exception as e:
            logger.error(f"BotWorker {self.worker_id} processing error: {e}")
            return {
                "worker_id": self.worker_id,
                "file_path": work_item.get("file_path", "unknown"),
                "error": str(e),
                "status": "error",
            }

    def stop(self) -> None:
        """Stop the worker thread."""
        self.running = False


class MultibotManager:
    """Manages multiple worker threads for parallel processing."""

    def __init__(self, num_workers: int = 4):
        """Initialize multibot manager."""
        self.num_workers = num_workers
        self.workers = []
        self.work_queue = queue.Queue(maxsize=1000)
        self.result_queue = queue.Queue(maxsize=1000)
        self.initialized = False

        logger.info(f"Initialized MultibotManager with {num_workers} workers")

    def initialize(self) -> None:
        """Initialize and start worker threads."""
        if self.initialized:
            return

        logger.info("Starting worker threads...")

        # Create and start workers
        for i in range(self.num_workers):
            worker = BotWorker(i, self.work_queue, self.result_queue)
            worker.start()
            self.workers.append(worker)

        self.initialized = True
        logger.info(f"Started {len(self.workers)} worker threads")

    def add_work(self, file_path: Path, processor: Callable[[Path], Any]) -> None:
        """Add work item to the queue."""
        work_item = {"file_path": str(file_path), "processor": processor}
        self.work_queue.put(work_item)

    def get_results(self) -> list[dict[str, Any]]:
        """Get all results from the result queue."""
        results = []
        while not self.result_queue.empty():
            try:
                result = self.result_queue.get_nowait()
                results.append(result)
            except queue.Empty:
                break
        return results

    def wait_for_completion(self) -> None:
        """Wait for all work items to be processed."""
        self.work_queue.join()

    def cleanup(self) -> None:
        """Clean up worker threads."""
        if not self.initialized:
            return

        logger.info("Stopping worker threads...")

        # Send shutdown signal to all workers
        for _ in self.workers:
            self.work_queue.put(None)

        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5.0)

        self.workers.clear()
        self.initialized = False
        logger.info("Worker threads stopped")


class FileProcessor:
    """Processes individual files for analysis."""

    def __init__(self):
        """Initialize file processor."""
        self.processed_files = 0
        self.errors = 0

        logger.debug("Initialized FileProcessor")

    def process_file(self, file_path: Path) -> dict[str, Any]:
        """Process a single file and return analysis results."""
        try:
            self.processed_files += 1

            # Basic file information
            stat = file_path.stat()
            file_info = {
                "path": str(file_path),
                "name": file_path.name,
                "size": stat.st_size,
                "extension": file_path.suffix,
                "modified": stat.st_mtime,
                "lines": 0,
                "is_binary": False,
            }

            # Try to read file content for line counting
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    file_info["lines"] = len(content.splitlines())
                    file_info["is_binary"] = "\0" in content
            except Exception:
                file_info["is_binary"] = True

            return {"status": "success", "file_info": file_info}

        except Exception as e:
            self.errors += 1
            logger.error(f"Error processing file {file_path}: {e}")
            return {"status": "error", "file_path": str(file_path), "error": str(e)}

    def get_stats(self) -> dict[str, int]:
        """Get processing statistics."""
        return {"processed_files": self.processed_files, "errors": self.errors}
