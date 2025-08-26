import threading
from typing import Callable, Dict, Optional

from .status_types import HealthStatus


class HealthMonitor:
    """Manage health checks and periodic execution."""

    def __init__(self, interval: int = 30):
        self.interval = interval
        self.health_checks: Dict[str, Callable[[], HealthStatus]] = {}
        self.timer: Optional[threading.Timer] = None

    # ------------------------------------------------------------------
    # Registration and default checks
    def setup_default_checks(self):
        self.register_health_check("system", self._check_system_health)
        self.register_health_check("memory", self._check_memory_health)
        self.register_health_check("disk", self._check_disk_health)

    def register_health_check(
        self, name: str, check_function: Callable[[], HealthStatus]
    ):
        self.health_checks[name] = check_function

    # Default check implementations ------------------------------------------------
    def _check_system_health(self) -> HealthStatus:
        """Basic system health check."""
        try:
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNKNOWN

    def _check_memory_health(self) -> HealthStatus:
        """Check memory usage via psutil if available."""
        try:  # pragma: no cover - psutil optional
            import psutil

            memory = psutil.virtual_memory()
            if memory.percent > 90:
                return HealthStatus.CRITICAL
            if memory.percent > 80:
                return HealthStatus.WARNING
            return HealthStatus.HEALTHY
        except ImportError:
            return HealthStatus.UNKNOWN
        except Exception:
            return HealthStatus.UNKNOWN

    def _check_disk_health(self) -> HealthStatus:
        """Check disk usage via psutil if available."""
        try:  # pragma: no cover - psutil optional
            import psutil

            disk = psutil.disk_usage("/")
            if disk.percent > 90:
                return HealthStatus.CRITICAL
            if disk.percent > 80:
                return HealthStatus.WARNING
            return HealthStatus.HEALTHY
        except ImportError:
            return HealthStatus.UNKNOWN
        except Exception:
            return HealthStatus.UNKNOWN

    # ------------------------------------------------------------------
    # Execution logic
    def run_checks(self) -> Dict[str, HealthStatus]:
        results: Dict[str, HealthStatus] = {}
        for name, check in self.health_checks.items():
            try:
                results[name] = check()
            except Exception as e:
                logger.error(f"Health check '{name}' failed: {e}")
                results[name] = HealthStatus.UNKNOWN
        return results

    def start(self):
        self.stop()
        self.timer = threading.Timer(self.interval, self._periodic_run)
        self.timer.daemon = True
        self.timer.start()

    def _periodic_run(self):
        try:
            self.run_checks()
        except Exception as e:
            logger.error(f"Periodic health check run failed: {e}")
        finally:
            self.start()

    def stop(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None


__all__ = ["HealthMonitor"]
