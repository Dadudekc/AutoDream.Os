#!/usr/bin/env python3
"""
Performance Core - Core Performance Engine
=========================================

Core performance orchestration engine that coordinates all performance components.
Follows V2 standards: ≤400 LOC, SRP, OOP design.

Author: Agent-1 (Phase 3 Modularization)
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority, ManagerMetrics, ManagerConfig
from .performance_models import (
    PerformanceMetric, ValidationRule, ValidationThreshold, ConnectionPool,
    BenchmarkResult, SystemPerformanceReport, PerformanceConfig, PerformanceLevel
)
from .performance_monitoring import PerformanceMonitoringManager
from .performance_validation import PerformanceValidationManager
from .performance_benchmarking import PerformanceBenchmarkingManager
from .performance_reporting import PerformanceReportingManager


@dataclass
class PerformanceCoreConfig(ManagerConfig):
    """Configuration for Performance Core"""
    max_concurrent_benchmarks: int = 10
    monitoring_interval_seconds: float = 5.0
    enable_auto_optimization: bool = False
    enable_alerting: bool = True
    enable_reporting: bool = True


class PerformanceCore(BaseManager):
    """
    Core Performance Engine - Orchestrates performance operations
    
    Single Responsibility: Coordinate performance monitoring, validation,
    benchmarking, and reporting for unified system performance management.
    """
    
    def __init__(self, manager_id: str, name: str = "Performance Core", description: str = ""):
        super().__init__(manager_id, name, description)
        
        # Configuration
        self.config = PerformanceCoreConfig(
            manager_id=manager_id,
            name=name,
            description=description
        )
        
        # Core components
        self.monitoring_manager = PerformanceMonitoringManager()
        self.validation_manager = PerformanceValidationManager()
        self.benchmarking_manager = PerformanceBenchmarkingManager()
        self.reporting_manager = PerformanceReportingManager()
        
        # Performance tracking
        self.metrics_history: List[PerformanceMetric] = []
        self.benchmark_history: List[BenchmarkResult] = []
        self.validation_results: List[Dict[str, Any]] = []
        self.alerts: List[str] = []
        self.connection_pools: Dict[str, ConnectionPool] = {}
        
        # System state
        self.is_running = False
        self.start_time: Optional[datetime] = None
        
        # Statistics
        self.total_benchmarks_run = 0
        self.successful_benchmarks = 0
        self.failed_benchmarks = 0
        self.total_metrics_collected = 0
        
        self.logger.info(f"PerformanceCore initialized: {manager_id}")
    
    def _on_start(self) -> bool:
        """Start performance core"""
        try:
            if self.is_running:
                self.logger.warning("Performance core is already running")
                return True
            
            # Start monitoring
            self.monitoring_manager.start_monitoring()
            
            # Start validation
            self.validation_manager.start_validation()
            
            # Start benchmarking
            self.benchmarking_manager.start_benchmarking()
            
            # Start reporting
            self.reporting_manager.start_reporting()
            
            self.is_running = True
            self.start_time = datetime.now()
            
            self.logger.info("✅ Performance core started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start performance core: {e}")
            return False
    
    def _on_stop(self) -> bool:
        """Stop performance core"""
        try:
            if not self.is_running:
                self.logger.warning("Performance core is not running")
                return True
            
            # Stop monitoring
            self.monitoring_manager.stop_monitoring()
            
            # Stop validation
            self.validation_manager.stop_validation()
            
            # Stop benchmarking
            self.benchmarking_manager.stop_benchmarking()
            
            # Stop reporting
            self.reporting_manager.stop_reporting()
            
            self.is_running = False
            self.start_time = None
            
            self.logger.info("✅ Performance core stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop performance core: {e}")
            return False
    
    def _on_heartbeat(self):
        """Performance core heartbeat"""
        try:
            if not self.is_running:
                return
            
            # Collect metrics
            metrics = self.monitoring_manager.collect_metrics()
            self.metrics_history.extend(metrics)
            self.total_metrics_collected += len(metrics)
            
            # Run validation
            validation_results = self.validation_manager.validate_metrics(metrics)
            self.validation_results.extend(validation_results)
            
            # Generate reports
            if self.config.enable_reporting:
                report = self.reporting_manager.generate_performance_report(
                    metrics, validation_results, self.benchmark_history
                )
                self.logger.info(f"Performance report generated: {report.report_id}")
            
            # Check for alerts
            if self.config.enable_alerting:
                new_alerts = self.validation_manager.check_alerts(validation_results)
                if new_alerts:
                    self.alerts.extend(new_alerts)
                    self.logger.warning(f"New performance alerts: {len(new_alerts)}")
            
        except Exception as e:
            self.logger.error(f"Error during Performance Core heartbeat: {e}")
    
    def run_benchmark(self, benchmark_type: str, parameters: Dict[str, Any]) -> BenchmarkResult:
        """Run a performance benchmark"""
        try:
            result = self.benchmarking_manager.run_benchmark(benchmark_type, parameters)
            
            if result.success:
                self.successful_benchmarks += 1
            else:
                self.failed_benchmarks += 1
            
            self.total_benchmarks_run += 1
            self.benchmark_history.append(result)
            
            self.logger.info(f"Benchmark completed: {result.name} - Success: {result.success}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to run benchmark: {e}")
            raise
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        return {
            "system_status": "running" if self.is_running else "stopped",
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            "total_metrics": self.total_metrics_collected,
            "total_benchmarks": self.total_benchmarks_run,
            "successful_benchmarks": self.successful_benchmarks,
            "failed_benchmarks": self.failed_benchmarks,
            "active_alerts": len(self.alerts),
            "connection_pools": len(self.connection_pools)
        }
    
    def add_connection_pool(self, pool: ConnectionPool) -> bool:
        """Add a connection pool to monitoring"""
        try:
            self.connection_pools[pool.name] = pool
            self.logger.info(f"Connection pool added: {pool.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add connection pool: {e}")
            return False
    
    def get_connection_pool_status(self, pool_name: str) -> Optional[ConnectionPool]:
        """Get connection pool status"""
        return self.connection_pools.get(pool_name)
    
    def update_connection_pool(self, pool_name: str, updates: Dict[str, Any]) -> bool:
        """Update connection pool information"""
        try:
            if pool_name in self.connection_pools:
                pool = self.connection_pools[pool_name]
                for key, value in updates.items():
                    if hasattr(pool, key):
                        setattr(pool, key, value)
                
                self.logger.info(f"Connection pool updated: {pool_name}")
                return True
            else:
                self.logger.warning(f"Connection pool not found: {pool_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to update connection pool: {e}")
            return False
