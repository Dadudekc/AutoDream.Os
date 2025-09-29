#!/usr/bin/env python3
"""
V3-003: Database Health Checker
==============================

Health checking component for database monitoring system.
V2 Compliant: ≤400 lines, single responsibility, KISS principle.
"""

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import Any

import asyncpg

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    check_name: str
    status: HealthStatus
    message: str
    timestamp: datetime
    response_time_ms: float


class HealthChecker:
    """Database health checking component."""

    def __init__(self):
        """Initialize health checker."""
        logger.info("🏥 Health Checker initialized")

    async def perform_health_check(self, node_config: dict[str, Any]) -> HealthCheck:
        """Perform health check on a database node."""
        try:
            start_time = datetime.now()

            connection = await self._get_database_connection(node_config)
            if not connection:
                health_check = HealthCheck(
                    check_name="connectivity",
                    status=HealthStatus.UNHEALTHY,
                    message="Failed to connect to database",
                    timestamp=datetime.now(UTC),
                    response_time_ms=0.0,
                )
            else:
                try:
                    # Test basic query
                    await connection.fetchval("SELECT 1")

                    response_time = (datetime.now() - start_time).total_seconds() * 1000

                    health_check = HealthCheck(
                        check_name="connectivity",
                        status=HealthStatus.HEALTHY,
                        message="Database connection successful",
                        timestamp=datetime.now(UTC),
                        response_time_ms=response_time,
                    )

                finally:
                    await connection.close()

            return health_check

        except Exception as e:
            logger.error(f"❌ Error performing health check: {e}")

            health_check = HealthCheck(
                check_name="connectivity",
                status=HealthStatus.UNHEALTHY,
                message=f"Health check failed: {e}",
                timestamp=datetime.now(UTC),
                response_time_ms=0.0,
            )

            return health_check

    async def perform_comprehensive_health_check(
        self, node_config: dict[str, Any]
    ) -> list[HealthCheck]:
        """Perform comprehensive health checks on a database node."""
        checks = []

        try:
            # Basic connectivity check
            connectivity_check = await self.perform_health_check(node_config)
            checks.append(connectivity_check)

            # Database responsiveness check
            responsiveness_check = await self._check_database_responsiveness(node_config)
            checks.append(responsiveness_check)

            # Database locks check
            locks_check = await self._check_database_locks(node_config)
            checks.append(locks_check)

            # Database space check
            space_check = await self._check_database_space(node_config)
            checks.append(space_check)

        except Exception as e:
            logger.error(f"❌ Error performing comprehensive health check: {e}")

        return checks

    async def _get_database_connection(
        self, node_config: dict[str, Any]
    ) -> asyncpg.Connection | None:
        """Get database connection."""
        try:
            connection = await asyncpg.connect(
                host=node_config["host"],
                port=node_config["port"],
                user=node_config["username"],
                password=node_config["password"],
                database=node_config["database"],
            )
            return connection
        except Exception as e:
            logger.error(f"❌ Failed to connect to database: {e}")
            return None

    async def _check_database_responsiveness(self, node_config: dict[str, Any]) -> HealthCheck:
        """Check database responsiveness."""
        try:
            start_time = datetime.now()

            connection = await self._get_database_connection(node_config)
            if not connection:
                return HealthCheck(
                    check_name="responsiveness",
                    status=HealthStatus.UNHEALTHY,
                    message="Failed to connect for responsiveness check",
                    timestamp=datetime.now(UTC),
                    response_time_ms=0.0,
                )

            try:
                # Perform a more complex query to test responsiveness
                await connection.fetchval("SELECT count(*) FROM pg_stat_activity")

                response_time = (datetime.now() - start_time).total_seconds() * 1000

                if response_time < 1000:  # Less than 1 second
                    status = HealthStatus.HEALTHY
                    message = f"Database responsive ({response_time:.1f}ms)"
                elif response_time < 5000:  # Less than 5 seconds
                    status = HealthStatus.DEGRADED
                    message = f"Database slow ({response_time:.1f}ms)"
                else:
                    status = HealthStatus.UNHEALTHY
                    message = f"Database unresponsive ({response_time:.1f}ms)"

                return HealthCheck(
                    check_name="responsiveness",
                    status=status,
                    message=message,
                    timestamp=datetime.now(UTC),
                    response_time_ms=response_time,
                )

            finally:
                await connection.close()

        except Exception as e:
            logger.error(f"❌ Error checking database responsiveness: {e}")

            return HealthCheck(
                check_name="responsiveness",
                status=HealthStatus.UNHEALTHY,
                message=f"Responsiveness check failed: {e}",
                timestamp=datetime.now(UTC),
                response_time_ms=0.0,
            )

    async def _check_database_locks(self, node_config: dict[str, Any]) -> HealthCheck:
        """Check database locks."""
        try:
            connection = await self._get_database_connection(node_config)
            if not connection:
                return HealthCheck(
                    check_name="locks",
                    status=HealthStatus.UNHEALTHY,
                    message="Failed to connect for locks check",
                    timestamp=datetime.now(UTC),
                    response_time_ms=0.0,
                )

            try:
                # Check for blocking locks
                lock_count = await connection.fetchval(
                    "SELECT count(*) FROM pg_locks WHERE NOT granted"
                )

                if lock_count == 0:
                    status = HealthStatus.HEALTHY
                    message = "No blocking locks"
                elif lock_count < 10:
                    status = HealthStatus.DEGRADED
                    message = f"{lock_count} blocking locks"
                else:
                    status = HealthStatus.UNHEALTHY
                    message = f"{lock_count} blocking locks (high)"

                return HealthCheck(
                    check_name="locks",
                    status=status,
                    message=message,
                    timestamp=datetime.now(UTC),
                    response_time_ms=0.0,
                )

            finally:
                await connection.close()

        except Exception as e:
            logger.error(f"❌ Error checking database locks: {e}")

            return HealthCheck(
                check_name="locks",
                status=HealthStatus.UNHEALTHY,
                message=f"Locks check failed: {e}",
                timestamp=datetime.now(UTC),
                response_time_ms=0.0,
            )

    async def _check_database_space(self, node_config: dict[str, Any]) -> HealthCheck:
        """Check database space usage."""
        try:
            connection = await self._get_database_connection(node_config)
            if not connection:
                return HealthCheck(
                    check_name="space",
                    status=HealthStatus.UNHEALTHY,
                    message="Failed to connect for space check",
                    timestamp=datetime.now(UTC),
                    response_time_ms=0.0,
                )

            try:
                # Check database size
                db_size = await connection.fetchval("SELECT pg_database_size(current_database())")

                # This is a simplified check - in reality you'd check available disk space
                if db_size < 1000000000:  # Less than 1GB
                    status = HealthStatus.HEALTHY
                    message = f"Database size: {db_size / 1024 / 1024:.1f}MB"
                elif db_size < 10000000000:  # Less than 10GB
                    status = HealthStatus.DEGRADED
                    message = f"Database size: {db_size / 1024 / 1024:.1f}MB (large)"
                else:
                    status = HealthStatus.UNHEALTHY
                    message = f"Database size: {db_size / 1024 / 1024:.1f}MB (very large)"

                return HealthCheck(
                    check_name="space",
                    status=status,
                    message=message,
                    timestamp=datetime.now(UTC),
                    response_time_ms=0.0,
                )

            finally:
                await connection.close()

        except Exception as e:
            logger.error(f"❌ Error checking database space: {e}")

            return HealthCheck(
                check_name="space",
                status=HealthStatus.UNHEALTHY,
                message=f"Space check failed: {e}",
                timestamp=datetime.now(UTC),
                response_time_ms=0.0,
            )
