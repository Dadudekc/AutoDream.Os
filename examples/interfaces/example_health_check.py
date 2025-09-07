"""Example health check strategy."""

from src.services.service_registry import (
    HealthCheckStrategy,
    ServiceInfo,
    ServiceStatus,
)


class PingHealthCheck(HealthCheckStrategy):
    """Always return healthy for demonstration purposes."""

    async def check_health(self, service: ServiceInfo) -> ServiceStatus:
        return ServiceStatus.HEALTHY
