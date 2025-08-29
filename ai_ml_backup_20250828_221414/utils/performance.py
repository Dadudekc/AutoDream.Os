import json
import time
import logging
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class PerformanceDataStore(ABC):
    """Interface for storing performance data."""

    @abstractmethod
    def save(
        self,
        func_name: str,
        execution_time: float,
        memory_delta: int,
        success: bool,
        error: Optional[str],
    ) -> None:
        """Persist performance metrics."""


@dataclass
class JSONPerformanceDataStore(PerformanceDataStore):
    """Persist performance data to a JSON file."""

    file_path: Path

    def __post_init__(self) -> None:
        self.file_path = Path(self.file_path)

    def save(
        self,
        func_name: str,
        execution_time: float,
        memory_delta: int,
        success: bool,
        error: Optional[str],
    ) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                performance_data = json.load(f)
        else:
            performance_data = {"functions": {}}
        performance_data.setdefault("functions", {}).setdefault(func_name, []).append(
            {
                "timestamp": datetime.now().isoformat(),
                "execution_time": execution_time,
                "memory_delta": memory_delta,
                "success": success,
                "error": error,
            }
        )
        if len(performance_data["functions"][func_name]) > 100:
            performance_data["functions"][func_name] = performance_data["functions"][
                func_name
            ][-100:]
        with open(self.file_path, "w") as f:
            json.dump(performance_data, f, indent=2)


_default_store: PerformanceDataStore = JSONPerformanceDataStore(
    Path("workflow_data/ai_ml/performance_log.json")
)


def set_performance_data_store(store: PerformanceDataStore) -> None:
    """Set the global performance data store."""
    global _default_store
    _default_store = store


def _get_memory_usage() -> int:
    try:
        import psutil

        process = psutil.Process()
        return process.memory_info().rss
    except ImportError:  # pragma: no cover - optional dependency
        return 0


def performance_monitor(
    func: Optional[Callable] = None, *, store: Optional[PerformanceDataStore] = None
) -> Callable:
    """Decorator to monitor function performance."""

    if func is None:
        return lambda f: performance_monitor(f, store=store)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = _get_memory_usage()
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
            logger.error(f"Function {func.__name__} failed: {e}")
        end_time = time.time()
        end_memory = _get_memory_usage()
        execution_time = end_time - start_time
        memory_delta = end_memory - start_memory
        (store or _default_store).save(
            func.__name__, execution_time, memory_delta, success, error
        )
        if not success:
            raise Exception(error)
        return result

    return wrapper
