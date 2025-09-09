"""
Integration Task Processor - V2 Compliant Module
===============================================

Handles processing of integration tasks and task management.
Extracted from enhanced_integration_orchestrator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio
import logging
from datetime import datetime
from queue import Empty, Queue
from typing import Any

from ..integration_models import IntegrationStatus, IntegrationTask, validate_integration_task


class IntegrationTaskProcessor:
    """Processor for integration tasks with queue management.

    Handles task submission, processing, and result collection.
    """

    def __init__(self, config):
        """Initialize task processor."""
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Task management
        self.task_queue = Queue()
        self.active_tasks: dict[str, IntegrationTask] = {}
        self.completed_tasks: list[dict[str, Any]] = []

        # Processing state
        self.is_processing = False
        self.processing_lock = asyncio.Lock()

    def submit_integration_task(self, task: IntegrationTask) -> bool:
        """Submit integration task for processing."""
        try:
            if not validate_integration_task(task):
                self.logger.error(f"Invalid integration task: {task.task_id}")
                return False

            self.task_queue.put(task)
            self.logger.debug(f"Task submitted: {task.task_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error submitting task: {e}")
            return False

    async def process_integration_tasks(self, status: IntegrationStatus) -> list[dict[str, Any]]:
        """Process integration tasks from queue."""
        results = []

        try:
            while not self.task_queue.empty() and status == IntegrationStatus.ACTIVE:
                try:
                    task = self.task_queue.get_nowait()

                    if task.is_expired():
                        self.logger.warning(f"Task expired: {task.task_id}")
                        continue

                    result = await self._execute_integration_task(task)
                    results.append(result)

                except Empty:
                    break
                except Exception as e:
                    self.logger.error(f"Error processing task: {e}")

            return results

        except Exception as e:
            self.logger.error(f"Error processing integration tasks: {e}")
            return []

    async def _execute_integration_task(self, task: IntegrationTask) -> dict[str, Any]:
        """Execute individual integration task."""
        start_time = datetime.now()

        try:
            # Add to active tasks
            self.active_tasks[task.task_id] = task

            # Execute task based on type
            result = await self._process_task_by_type(task)

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()

            # Create result
            task_result = {
                "task_id": task.task_id,
                "success": result.get("success", False),
                "execution_time": execution_time,
                "result": result.get("data"),
                "error": result.get("error"),
                "timestamp": datetime.now().isoformat(),
            }

            # Move to completed tasks
            self.completed_tasks.append(task_result)
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]

            return task_result

        except Exception as e:
            self.logger.error(f"Error executing task {task.task_id}: {e}")
            return {
                "task_id": task.task_id,
                "success": False,
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
        finally:
            # Ensure task is removed from active tasks
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]

    async def _process_task_by_type(self, task: IntegrationTask) -> dict[str, Any]:
        """Process task based on its type."""
        try:
            if task.integration_type == "vector_database":
                return await self._process_vector_database_task(task)
            elif task.integration_type == "performance_optimization":
                return await self._process_performance_task(task)
            elif task.integration_type == "system_coordination":
                return await self._process_coordination_task(task)
            else:
                return await self._process_generic_task(task)

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _process_vector_database_task(self, task: IntegrationTask) -> dict[str, Any]:
        """Process vector database integration task."""
        # Simulate vector database integration
        await asyncio.sleep(0.1)
        return {
            "success": True,
            "data": {"integration": "vector_database", "status": "completed"},
        }

    async def _process_performance_task(self, task: IntegrationTask) -> dict[str, Any]:
        """Process performance optimization task."""
        # Simulate performance optimization
        await asyncio.sleep(0.05)
        return {
            "success": True,
            "data": {"optimization": "performance", "status": "completed"},
        }

    async def _process_coordination_task(self, task: IntegrationTask) -> dict[str, Any]:
        """Process system coordination task."""
        # Simulate system coordination
        await asyncio.sleep(0.2)
        return {
            "success": True,
            "data": {"coordination": "system", "status": "completed"},
        }

    async def _process_generic_task(self, task: IntegrationTask) -> dict[str, Any]:
        """Process generic integration task."""
        # Simulate generic processing
        await asyncio.sleep(0.1)
        return {
            "success": True,
            "data": {"integration": "generic", "status": "completed"},
        }

    def get_task_queue_size(self) -> int:
        """Get current task queue size."""
        return self.task_queue.qsize()

    def get_active_tasks_count(self) -> int:
        """Get number of active tasks."""
        return len(self.active_tasks)

    def get_completed_tasks_count(self) -> int:
        """Get number of completed tasks."""
        return len(self.completed_tasks)

    def get_task_statistics(self) -> dict[str, Any]:
        """Get task processing statistics."""
        total_tasks = len(self.completed_tasks)
        successful_tasks = sum(1 for task in self.completed_tasks if task.get("success", False))

        return {
            "queue_size": self.get_task_queue_size(),
            "active_tasks": self.get_active_tasks_count(),
            "completed_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "success_rate": ((successful_tasks / total_tasks * 100) if total_tasks > 0 else 0),
        }

    def clear_completed_tasks(self):
        """Clear completed tasks history."""
        self.completed_tasks.clear()
        self.logger.info("Completed tasks cleared")

    def get_recent_tasks(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent completed tasks."""
        return self.completed_tasks[-limit:] if self.completed_tasks else []
