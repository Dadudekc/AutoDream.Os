from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Any


class WorkflowExecutor:
    """Simple asynchronous executor for workflow tasks."""

    def __init__(self, max_workers: int = 1) -> None:
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
        """Submit a task for asynchronous execution."""
        return self._executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the underlying executor."""
        self._executor.shutdown(wait=wait)
