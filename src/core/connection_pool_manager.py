"""
Connection Pool Manager - Agent Cellphone V2
===========================================

Advanced connection management system with health monitoring and optimization.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import threading
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Callable, Generic, TypeVar
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

# Type variable for connection objects
T = TypeVar('T')


class ConnectionState(Enum):
    """Connection states for health monitoring"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    RECOVERING = "recovering"


@dataclass
class ConnectionInfo:
    """Connection metadata and health information"""
    connection_id: str
    connection: T
    created_at: float
    last_used: float
    health_score: float
    state: ConnectionState
    error_count: int
    response_time: float
    is_active: bool = True


class ConnectionPool(Generic[T]):
    """
    Generic connection pool with health monitoring and optimization
    """

    def __init__(self,
                 max_connections: int = 10,
                 min_connections: int = 2,
                 health_check_interval: float = 30.0,
                 connection_timeout: float = 60.0):
        self.logger = logging.getLogger(f"{__name__}.ConnectionPool")
        self.max_connections = max_connections
        self.min_connections = min_connections
        self.health_check_interval = health_check_interval
        self.connection_timeout = connection_timeout

        self.connections: List[ConnectionInfo] = []
        self.available_connections: List[ConnectionInfo] = []
        self.in_use_connections: List[ConnectionInfo] = []
        self.connection_factory: Optional[Callable[[], T]] = None
        self.health_checker: Optional[Callable[[T], bool]] = None

        self.lock = threading.RLock()
        self.health_thread: Optional[threading.Thread] = None
        self.is_running = False

        # Performance metrics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.avg_response_time = 0.0

    def set_connection_factory(self, factory: Callable[[], T]):
        """Set the factory function for creating new connections"""
        self.connection_factory = factory

    def set_health_checker(self, checker: Callable[[T], bool]):
        """Set the health check function for connections"""
        self.health_checker = checker

    def start_pool(self):
        """Start the connection pool and health monitoring"""
        if self.is_running:
            return

        if not self.connection_factory:
            raise ValueError("Connection factory must be set before starting pool")

        self.is_running = True
        self._initialize_pool()

        # Start health monitoring thread
        self.health_thread = threading.Thread(target=self._health_monitor_loop, daemon=True)
        self.health_thread.start()

        self.logger.info(f"Connection pool started with {len(self.connections)} connections")

    def stop_pool(self):
        """Stop the connection pool and cleanup"""
        self.is_running = False

        if self.health_thread:
            self.health_thread.join(timeout=5)

        self._cleanup_all_connections()
        self.logger.info("Connection pool stopped")

    def get_connection(self) -> Optional[T]:
        """Get an available connection from the pool"""
        with self.lock:
            self.total_requests += 1

            # Try to get an available connection
            if self.available_connections:
                conn_info = self.available_connections.pop(0)
                conn_info.last_used = time.time()
                self.in_use_connections.append(conn_info)
                return conn_info.connection

            # Create new connection if under max limit
            if len(self.connections) < self.max_connections:
                return self._create_new_connection()

            # Wait for connection to become available
            return self._wait_for_connection()

    def return_connection(self, connection: T):
        """Return a connection to the pool"""
        with self.lock:
            conn_info = self._find_connection_info(connection)
            if conn_info and conn_info in self.in_use_connections:
                self.in_use_connections.remove(conn_info)
                self.available_connections.append(conn_info)
                self.successful_requests += 1

    def _create_new_connection(self) -> Optional[T]:
        """Create a new connection using the factory"""
        try:
            connection = self.connection_factory()
            conn_info = ConnectionInfo(
                connection_id=f"conn_{int(time.time())}_{len(self.connections)}",
                connection=connection,
                created_at=time.time(),
                last_used=time.time(),
                health_score=1.0,
                state=ConnectionState.HEALTHY,
                error_count=0,
                response_time=0.0
            )

            self.connections.append(conn_info)
            self.in_use_connections.append(conn_info)

            self.logger.debug(f"Created new connection: {conn_info.connection_id}")
            return connection

        except Exception as e:
            self.logger.error(f"Failed to create connection: {e}")
            self.failed_requests += 1
            return None

    def _wait_for_connection(self) -> Optional[T]:
        """Wait for a connection to become available"""
        # Simple implementation - in production, use condition variables
        time.sleep(0.1)
        return self.get_connection()

    def _find_connection_info(self, connection: T) -> Optional[ConnectionInfo]:
        """Find connection info by connection object"""
        for conn_info in self.connections:
            if conn_info.connection == connection:
                return conn_info
        return None

    def _initialize_pool(self):
        """Initialize the pool with minimum connections"""
        for _ in range(self.min_connections):
            self._create_new_connection()

        # Move initial connections to available pool
        self.available_connections.extend(self.connections[:])
        self.in_use_connections.clear()

    def _health_monitor_loop(self):
        """Main health monitoring loop"""
        while self.is_running:
            try:
                self._perform_health_checks()
                self._optimize_pool_size()
                time.sleep(self.health_check_interval)
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(10)  # Recovery pause

    def _perform_health_checks(self):
        """Perform health checks on all connections"""
        if not self.health_checker:
            return

        with self.lock:
            for conn_info in self.connections:
                try:
                    is_healthy = self.health_checker(conn_info.connection)
                    self._update_connection_health(conn_info, is_healthy)
                except Exception as e:
                    self.logger.error(f"Health check failed for {conn_info.connection_id}: {e}")
                    self._update_connection_health(conn_info, False)

    def _update_connection_health(self, conn_info: ConnectionInfo, is_healthy: bool):
        """Update connection health status"""
        if is_healthy:
            conn_info.health_score = min(1.0, conn_info.health_score + 0.1)
            conn_info.error_count = max(0, conn_info.error_count - 1)
            conn_info.state = ConnectionState.HEALTHY
        else:
            conn_info.health_score = max(0.0, conn_info.health_score - 0.2)
            conn_info.error_count += 1
            conn_info.state = ConnectionState.FAILED if conn_info.health_score < 0.3 else ConnectionState.DEGRADED

        # Remove failed connections
        if conn_info.health_score < 0.1:
            self._remove_connection(conn_info)

    def _remove_connection(self, conn_info: ConnectionInfo):
        """Remove a connection from the pool"""
        if conn_info in self.connections:
            self.connections.remove(conn_info)
        if conn_info in self.available_connections:
            self.available_connections.remove(conn_info)
        if conn_info in self.in_use_connections:
            self.in_use_connections.remove(conn_info)

        self.logger.info(f"Removed failed connection: {conn_info.connection_id}")

    def _optimize_pool_size(self):
        """Optimize pool size based on usage patterns"""
        with self.lock:
            current_size = len(self.connections)
            available_count = len(self.available_connections)

            # Reduce pool if too many idle connections
            if available_count > self.max_connections * 0.7 and current_size > self.min_connections:
                excess = min(available_count - int(self.max_connections * 0.5),
                           current_size - self.min_connections)
                self._reduce_pool_size(excess)

            # Increase pool if all connections are in use
            elif available_count == 0 and current_size < self.max_connections:
                self._increase_pool_size(1)

    def _reduce_pool_size(self, count: int):
        """Reduce pool size by removing idle connections"""
        removed = 0
        for conn_info in self.available_connections[:]:
            if removed >= count:
                break
            if conn_info.health_score < 0.8:  # Remove lower health connections first
                self._remove_connection(conn_info)
                removed += 1

    def _increase_pool_size(self, count: int):
        """Increase pool size by creating new connections"""
        for _ in range(count):
            if len(self.connections) < self.max_connections:
                self._create_new_connection()

    def get_pool_stats(self) -> Dict[str, Any]:
        """Get current pool statistics"""
        with self.lock:
            return {
                "total_connections": len(self.connections),
                "available_connections": len(self.available_connections),
                "in_use_connections": len(self.in_use_connections),
                "max_connections": self.max_connections,
                "min_connections": self.min_connections,
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "success_rate": self.successful_requests / max(self.total_requests, 1),
                "avg_response_time": self.avg_response_time,
                "health_distribution": self._get_health_distribution()
            }

    def _get_health_distribution(self) -> Dict[str, int]:
        """Get distribution of connection health states"""
        distribution = {state.value: 0 for state in ConnectionState}
        for conn_info in self.connections:
            distribution[conn_info.state.value] += 1
        return distribution

    def _cleanup_all_connections(self):
        """Clean up all connections when stopping"""
        with self.lock:
            self.connections.clear()
            self.available_connections.clear()
            self.in_use_connections.clear()


class ConnectionPoolManager:
    """
    Manages multiple connection pools for different services
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ConnectionPoolManager")
        self.pools: Dict[str, ConnectionPool] = {}
        self.pool_configs: Dict[str, Dict[str, Any]] = {}

    def create_pool(self, pool_name: str, config: Dict[str, Any]) -> ConnectionPool:
        """Create a new connection pool with configuration"""
        if pool_name in self.pools:
            raise ValueError(f"Pool '{pool_name}' already exists")

        pool = ConnectionPool(**config)
        self.pools[pool_name] = pool
        self.pool_configs[pool_name] = config

        self.logger.info(f"Created connection pool: {pool_name}")
        return pool

    def get_pool(self, pool_name: str) -> Optional[ConnectionPool]:
        """Get an existing connection pool"""
        return self.pools.get(pool_name)

    def remove_pool(self, pool_name: str):
        """Remove a connection pool"""
        if pool_name in self.pools:
            self.pools[pool_name].stop_pool()
            del self.pools[pool_name]
            del self.pool_configs[pool_name]
            self.logger.info(f"Removed connection pool: {pool_name}")

    def get_all_pool_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all pools"""
        return {name: pool.get_pool_stats() for name, pool in self.pools.items()}

    def start_all_pools(self):
        """Start all connection pools"""
        for name, pool in self.pools.items():
            try:
                pool.start_pool()
            except Exception as e:
                self.logger.error(f"Failed to start pool {name}: {e}")

    def stop_all_pools(self):
        """Stop all connection pools"""
        for name, pool in self.pools.items():
            try:
                pool.stop_pool()
            except Exception as e:
                self.logger.error(f"Failed to stop pool {name}: {e}")
