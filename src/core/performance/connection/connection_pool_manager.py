#!/usr/bin/env python3
"""
Connection Pool Manager - V2 Modular Architecture
================================================

Handles connection pool management and monitoring.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


logger = logging.getLogger(__name__)


@dataclass
class ConnectionPool:
    """Connection pool definition"""
    name: str
    max_connections: int
    active_connections: int
    idle_connections: int
    total_connections: int
    wait_time: float
    utilization: float
    health_status: str


class ConnectionPoolManager:
    """
    Connection Pool Manager - Single responsibility: Manage connection pools
    
    Handles all connection pool operations including:
    - Pool creation and removal
    - Connection metrics tracking
    - Health status monitoring
    - Utilization calculations
    """

    def __init__(self):
        """Initialize connection pool manager"""
        self.logger = logging.getLogger(f"{__name__}.ConnectionPoolManager")
        self.connection_pools: Dict[str, ConnectionPool] = {}

    def create_connection_pool(self, name: str, max_connections: int) -> ConnectionPool:
        """Create a new connection pool"""
        try:
            pool = ConnectionPool(
                name=name,
                max_connections=max_connections,
                active_connections=0,
                idle_connections=0,
                total_connections=0,
                wait_time=0.0,
                utilization=0.0,
                health_status="healthy"
            )
            self.connection_pools[name] = pool
            self.logger.info(f"Created connection pool: {name} with {max_connections} max connections")
            return pool
        except Exception as e:
            self.logger.error(f"Failed to create connection pool {name}: {e}")
            raise

    def update_connection_pool(self, name: str, active: int, idle: int, wait_time: float = 0.0):
        """Update connection pool metrics"""
        try:
            if name not in self.connection_pools:
                self.logger.warning(f"Connection pool {name} not found")
                return
            
            pool = self.connection_pools[name]
            pool.active_connections = active
            pool.idle_connections = idle
            pool.total_connections = active + idle
            pool.wait_time = wait_time
            pool.utilization = (active / pool.max_connections) * 100 if pool.max_connections > 0 else 0
            
            # Update health status based on utilization
            if pool.utilization >= 95:
                pool.health_status = "critical"
            elif pool.utilization >= 85:
                pool.health_status = "warning"
            elif pool.utilization >= 70:
                pool.health_status = "degraded"
            else:
                pool.health_status = "healthy"
                
            self.logger.debug(f"Updated connection pool {name}: active={active}, idle={idle}, utilization={pool.utilization:.1f}%")
            
        except Exception as e:
            self.logger.error(f"Failed to update connection pool {name}: {e}")

    def get_connection_pool(self, name: str) -> Optional[ConnectionPool]:
        """Get connection pool by name"""
        return self.connection_pools.get(name)

    def get_all_connection_pools(self) -> Dict[str, ConnectionPool]:
        """Get all connection pools"""
        return self.connection_pools.copy()

    def remove_connection_pool(self, name: str) -> bool:
        """Remove a connection pool"""
        try:
            if name in self.connection_pools:
                del self.connection_pools[name]
                self.logger.info(f"Removed connection pool: {name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove connection pool {name}: {e}")
            return False

    def get_pool_statistics(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed statistics for a connection pool"""
        try:
            pool = self.get_connection_pool(name)
            if not pool:
                return None
            
            return {
                "name": pool.name,
                "max_connections": pool.max_connections,
                "active_connections": pool.active_connections,
                "idle_connections": pool.idle_connections,
                "total_connections": pool.total_connections,
                "wait_time": pool.wait_time,
                "utilization": pool.utilization,
                "health_status": pool.health_status,
                "available_connections": pool.max_connections - pool.active_connections,
                "connection_efficiency": (pool.active_connections / pool.max_connections) * 100 if pool.max_connections > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get pool statistics for {name}: {e}")
            return None

    def get_overall_statistics(self) -> Dict[str, Any]:
        """Get overall connection pool statistics"""
        try:
            total_pools = len(self.connection_pools)
            total_max_connections = sum(pool.max_connections for pool in self.connection_pools.values())
            total_active_connections = sum(pool.active_connections for pool in self.connection_pools.values())
            total_idle_connections = sum(pool.idle_connections for pool in self.connection_pools.values())
            
            overall_utilization = (total_active_connections / total_max_connections) * 100 if total_max_connections > 0 else 0
            
            # Count pools by health status
            health_counts = {}
            for pool in self.connection_pools.values():
                status = pool.health_status
                health_counts[status] = health_counts.get(status, 0) + 1
            
            return {
                "total_pools": total_pools,
                "total_max_connections": total_max_connections,
                "total_active_connections": total_active_connections,
                "total_idle_connections": total_idle_connections,
                "overall_utilization": overall_utilization,
                "health_distribution": health_counts,
                "average_pool_size": total_max_connections / total_pools if total_pools > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get overall statistics: {e}")
            return {"error": str(e)}

    def check_pool_health(self, name: str) -> Optional[Dict[str, Any]]:
        """Check health of a specific connection pool"""
        try:
            pool = self.get_connection_pool(name)
            if not pool:
                return None
            
            health_issues = []
            
            # Check utilization
            if pool.utilization >= 95:
                health_issues.append("Critical: Pool utilization at 95%+")
            elif pool.utilization >= 85:
                health_issues.append("Warning: Pool utilization at 85%+")
            
            # Check wait time
            if pool.wait_time > 1.0:  # More than 1 second wait
                health_issues.append("Warning: High connection wait time")
            
            # Check connection balance
            if pool.idle_connections == 0 and pool.active_connections > 0:
                health_issues.append("Warning: No idle connections available")
            
            return {
                "pool_name": pool.name,
                "health_status": pool.health_status,
                "utilization": pool.utilization,
                "active_connections": pool.active_connections,
                "idle_connections": pool.idle_connections,
                "wait_time": pool.wait_time,
                "health_issues": health_issues,
                "is_healthy": len(health_issues) == 0
            }
            
        except Exception as e:
            self.logger.error(f"Failed to check pool health for {name}: {e}")
            return None

    def optimize_pool_configuration(self, name: str) -> Optional[Dict[str, Any]]:
        """Suggest optimization for a connection pool"""
        try:
            pool = self.get_connection_pool(name)
            if not pool:
                return None
            
            recommendations = []
            
            # Utilization-based recommendations
            if pool.utilization >= 90:
                recommendations.append({
                    "type": "critical",
                    "message": "Increase max connections",
                    "current": pool.max_connections,
                    "suggested": int(pool.max_connections * 1.5)
                })
            elif pool.utilization >= 80:
                recommendations.append({
                    "type": "warning",
                    "message": "Consider increasing max connections",
                    "current": pool.max_connections,
                    "suggested": int(pool.max_connections * 1.2)
                })
            
            # Wait time recommendations
            if pool.wait_time > 0.5:
                recommendations.append({
                    "type": "warning",
                    "message": "High wait time detected - consider connection pooling optimization",
                    "current": pool.wait_time,
                    "suggested": "Implement connection reuse"
                })
            
            # Idle connection recommendations
            if pool.idle_connections == 0 and pool.active_connections > 0:
                recommendations.append({
                    "type": "info",
                    "message": "No idle connections - consider maintaining minimum idle pool",
                    "current": 0,
                    "suggested": "Maintain 10-20% idle connections"
                })
            
            return {
                "pool_name": pool.name,
                "current_config": {
                    "max_connections": pool.max_connections,
                    "utilization": pool.utilization,
                    "wait_time": pool.wait_time
                },
                "recommendations": recommendations,
                "optimization_score": self._calculate_optimization_score(pool)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to optimize pool configuration for {name}: {e}")
            return None

    def _calculate_optimization_score(self, pool: ConnectionPool) -> float:
        """Calculate optimization score for a pool (0-100, higher is better)"""
        try:
            score = 100.0
            
            # Deduct points for high utilization
            if pool.utilization >= 95:
                score -= 30
            elif pool.utilization >= 85:
                score -= 20
            elif pool.utilization >= 75:
                score -= 10
            
            # Deduct points for high wait time
            if pool.wait_time > 1.0:
                score -= 25
            elif pool.wait_time > 0.5:
                score -= 15
            
            # Deduct points for no idle connections
            if pool.idle_connections == 0:
                score -= 15
            
            return max(0.0, score)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate optimization score: {e}")
            return 50.0  # Default middle score

    def clear_all_pools(self) -> None:
        """Clear all connection pools"""
        try:
            self.connection_pools.clear()
            self.logger.info("Cleared all connection pools")
        except Exception as e:
            self.logger.error(f"Failed to clear all pools: {e}")

    def export_pool_configurations(self) -> Dict[str, Any]:
        """Export all pool configurations"""
        try:
            configurations = {}
            for name, pool in self.connection_pools.items():
                configurations[name] = {
                    "max_connections": pool.max_connections,
                    "health_status": pool.health_status,
                    "utilization": pool.utilization,
                    "active_connections": pool.active_connections,
                    "idle_connections": pool.idle_connections
                }
            
            return {
                "export_timestamp": datetime.now().isoformat(),
                "total_pools": len(configurations),
                "pools": configurations
            }
            
        except Exception as e:
            self.logger.error(f"Failed to export pool configurations: {e}")
            return {"error": str(e)}
