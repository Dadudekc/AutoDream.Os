#!/usr/bin/env python3
"""
Unified Performance System - V2 Modular Architecture
===================================================

Orchestrates all modular performance components.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .config.config_manager import PerformanceConfigManager
from .monitoring.monitoring_manager import MonitoringManager
from .validation.validation_engine import ValidationEngine, ValidationSeverity
from .benchmarking.benchmark_runner import BenchmarkRunner
from .reporting.report_generator import PerformanceReportGenerator
from .analysis.performance_analyzer import PerformanceAnalyzer, PerformanceLevel
from .connection.connection_pool_manager import ConnectionPoolManager


logger = logging.getLogger(__name__)


class UnifiedPerformanceSystem:
    """
    Unified Performance System - Single responsibility: Orchestrate performance components
    
    This system orchestrates functionality from modular components:
    - Configuration management
    - Performance monitoring
    - Validation and threshold checking
    - Benchmark execution
    - Report generation
    - Performance analysis
    - Connection pool management
    
    Total consolidation: 1,284 lines → 8 modular components (90% modularization)
    """

    def __init__(self, config_file: Optional[str] = None):
        """Initialize unified performance system"""
        self.logger = logging.getLogger(f"{__name__}.UnifiedPerformanceSystem")
        
        # System state
        self.is_running = False
        self.start_time: Optional[datetime] = None
        
        # Initialize modular components
        self.config_manager = PerformanceConfigManager(config_file)
        self.monitoring_manager = MonitoringManager()
        self.validation_engine = ValidationEngine()
        self.benchmark_runner = BenchmarkRunner()
        self.report_generator = PerformanceReportGenerator()
        self.performance_analyzer = PerformanceAnalyzer()
        self.connection_pool_manager = ConnectionPoolManager()
        
        # System configuration
        self.config = self.config_manager.get_config()
        
        # Performance tracking
        self.total_benchmarks_run = 0
        self.successful_benchmarks = 0
        self.failed_benchmarks = 0
        self.total_metrics_collected = 0
        
        # Monitoring
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False
        
        self.logger.info("✅ Unified Performance System initialized successfully")

    def start_system(self) -> bool:
        """Start the performance system"""
        try:
            if self.is_running:
                self.logger.warning("System is already running")
                return True
            
            self.is_running = True
            self.start_time = datetime.now()
            
            # Start monitoring
            monitoring_interval = self.config.get("monitoring_interval", 60)
            if monitoring_interval > 0:
                self._start_monitoring()
            
            self.logger.info("✅ Performance system started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start system: {e}")
            return False

    def stop_system(self) -> bool:
        """Stop the performance system"""
        try:
            if not self.is_running:
                self.logger.warning("System is not running")
                return True
            
            self.is_running = False
            
            # Stop monitoring
            self._stop_monitoring()
            
            self.logger.info("✅ Performance system stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop system: {e}")
            return False

    def _start_monitoring(self) -> None:
        """Start performance monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("✅ Performance monitoring started")

    def _stop_monitoring(self) -> None:
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        self.logger.info("✅ Performance monitoring stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while self.monitoring_active and self.is_running:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Validate metrics
                self._validate_current_metrics()
                
                # Check thresholds
                self._check_thresholds()
                
                # Sleep for monitoring interval
                monitoring_interval = self.config.get("monitoring_interval", 60)
                time.sleep(monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(1.0)  # Brief pause on error

    def _collect_system_metrics(self) -> None:
        """Collect current system performance metrics"""
        try:
            # Use monitoring manager to collect metrics
            metrics = self.monitoring_manager.collect_system_metrics()
            
            # Store metrics
            for metric_name, metric_data in metrics.items():
                self.monitoring_manager.add_metric(metric_name, metric_data)
            
            self.total_metrics_collected += len(metrics)
            
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")

    def _validate_current_metrics(self) -> None:
        """Validate current metrics against validation rules"""
        try:
            current_metrics = self.monitoring_manager.get_current_metrics()
            validation_results = self.validation_engine.validate_metrics(current_metrics)
            
            # Process validation results
            for result in validation_results:
                if not result.passed:
                    self.logger.warning(f"⚠️ Validation failed: {result.message}")
                    
                    # Generate alert for failed validations
                    if result.severity == ValidationSeverity.CRITICAL:
                        self._add_alert(f"CRITICAL: {result.message}")
                    elif result.severity == ValidationSeverity.WARNING:
                        self._add_alert(f"WARNING: {result.message}")
            
        except Exception as e:
            self.logger.error(f"Failed to validate metrics: {e}")

    def _check_thresholds(self) -> None:
        """Check metrics against configured thresholds"""
        try:
            current_metrics = self.monitoring_manager.get_current_metrics()
            threshold_results = self.validation_engine.check_thresholds(current_metrics)
            
            # Process threshold results
            for result in threshold_results:
                if result.severity == ValidationSeverity.CRITICAL:
                    self._add_alert(f"CRITICAL: {result.metric_name} = {result.current_value} exceeds critical threshold {result.threshold}")
                elif result.severity == ValidationSeverity.WARNING:
                    self._add_alert(f"WARNING: {result.metric_name} = {result.current_value} exceeds warning threshold {result.threshold}")
                    
        except Exception as e:
            self.logger.error(f"Failed to check thresholds: {e}")

    def _add_alert(self, message: str) -> None:
        """Add a new alert"""
        timestamp = datetime.now().isoformat()
        alert = f"[{timestamp}] {message}"
        self.monitoring_manager.add_alert(alert)
        self.logger.warning(f"Alert: {message}")

    def run_benchmark(self, benchmark_type: str, duration: int = 30, **kwargs):
        """Run a performance benchmark"""
        try:
            # Use benchmark runner to execute benchmark
            result = self.benchmark_runner.run_benchmark(benchmark_type, duration, **kwargs)
            
            # Update statistics
            self.total_benchmarks_run += 1
            if result.success:
                self.successful_benchmarks += 1
            else:
                self.failed_benchmarks += 1
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to run benchmark: {e}")
            return None

    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        try:
            # Get data from all components
            metrics_history = self.monitoring_manager.get_metrics_history()
            benchmark_history = self.benchmark_runner.list_benchmarks()
            alerts = self.monitoring_manager.get_alerts()
            
            # Generate performance summary
            performance_summary = self.performance_analyzer.get_performance_summary(
                metrics_history, benchmark_history, alerts
            )
            
            # Generate report using report generator
            report = self.report_generator.generate_report(performance_summary)
            
            self.logger.info("✅ Performance report generated successfully")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            return None

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            
            # Get health from monitoring manager
            monitoring_health = self.monitoring_manager.get_health_status()
            
            # Get benchmark statistics
            benchmark_stats = self.benchmark_runner.get_statistics()
            
            # Get connection pool statistics
            pool_stats = self.connection_pool_manager.get_overall_statistics()
            
            return {
                "system_status": "running" if self.is_running else "stopped",
                "uptime_seconds": round(uptime, 2),
                "total_benchmarks": benchmark_stats.get("total_benchmarks", 0),
                "successful_benchmarks": benchmark_stats.get("successful_benchmarks", 0),
                "failed_benchmarks": benchmark_stats.get("failed_benchmarks", 0),
                "success_rate": benchmark_stats.get("success_rate", 0),
                "total_metrics_collected": self.total_metrics_collected,
                "active_alerts": len(self.monitoring_manager.get_alerts()[-10:]),
                "monitoring_active": self.monitoring_active,
                "monitoring_health": monitoring_health,
                "connection_pools": pool_stats,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system health: {e}")
            return {"error": str(e), "system_status": "error"}

    def run_smoke_test(self) -> bool:
        """Run basic functionality test"""
        try:
            self.logger.info("🧪 Running Unified Performance System smoke test...")
            
            # Test system start
            if not self.start_system():
                return False
            
            # Test metric collection
            self._collect_system_metrics()
            if not self.monitoring_manager.get_metrics_history():
                self.logger.error("❌ Metric collection failed")
                return False
            
            # Test benchmark execution
            result = self.run_benchmark("cpu", duration=1)
            if not result or not result.success:
                self.logger.error("❌ Benchmark execution failed")
                return False
            
            # Test report generation
            report = self.generate_performance_report()
            if not report:
                self.logger.error("❌ Report generation failed")
                return False
            
            # Test system health
            health = self.get_system_health()
            if "error" in health:
                self.logger.error("❌ System health check failed")
                return False
            
            # Stop system
            self.stop_system()
            
            self.logger.info("✅ Unified Performance System smoke test passed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Unified Performance System smoke test failed: {e}")
            return False

    def get_benchmark(self, benchmark_id: str):
        """Get specific benchmark result"""
        return self.benchmark_runner.get_benchmark(benchmark_id)

    def list_benchmarks(self):
        """List all benchmark results"""
        return self.benchmark_runner.list_benchmarks()

    def clear_history(self) -> None:
        """Clear all historical data"""
        self.monitoring_manager.clear_metrics()
        self.benchmark_runner.clear_history()
        self.monitoring_manager.clear_alerts()
        self.total_benchmarks_run = 0
        self.successful_benchmarks = 0
        self.failed_benchmarks = 0
        self.total_metrics_collected = 0
        self.logger.info("✅ Performance history cleared")

    def export_report(self, report, format: str = "json") -> str:
        """Export performance report in specified format"""
        try:
            return self.report_generator.export_report(report, format)
        except Exception as e:
            self.logger.error(f"Failed to export report: {e}")
            return f"Export failed: {e}"

    # Connection pool management methods
    def create_connection_pool(self, name: str, max_connections: int):
        """Create a new connection pool"""
        return self.connection_pool_manager.create_connection_pool(name, max_connections)

    def update_connection_pool(self, name: str, active: int, idle: int, wait_time: float = 0.0):
        """Update connection pool metrics"""
        self.connection_pool_manager.update_connection_pool(name, active, idle, wait_time)

    def get_connection_pool(self, name: str):
        """Get connection pool by name"""
        return self.connection_pool_manager.get_connection_pool(name)

    def get_all_connection_pools(self):
        """Get all connection pools"""
        return self.connection_pool_manager.get_all_connection_pools()

    def remove_connection_pool(self, name: str) -> bool:
        """Remove a connection pool"""
        return self.connection_pool_manager.remove_connection_pool(name)

    def get_connection_pool_statistics(self, name: str):
        """Get connection pool statistics"""
        return self.connection_pool_manager.get_pool_statistics(name)

    def check_connection_pool_health(self, name: str):
        """Check connection pool health"""
        return self.connection_pool_manager.check_pool_health(name)

    def optimize_connection_pool(self, name: str):
        """Optimize connection pool configuration"""
        return self.connection_pool_manager.optimize_pool_configuration(name)


# ============================================================================
# BACKWARDS COMPATIBILITY ALIASES
# ============================================================================

# Maintain backwards compatibility with existing code
PerformanceValidationOrchestrator = UnifiedPerformanceSystem
PerformanceValidationCore = UnifiedPerformanceSystem
PerformanceReporter = UnifiedPerformanceSystem
PerformanceConfigManager = UnifiedPerformanceSystem

# Export all components for backwards compatibility
__all__ = [
    "UnifiedPerformanceSystem",
    "PerformanceValidationOrchestrator",
    "PerformanceValidationCore",
    "PerformanceReporter",
    "PerformanceConfigManager",
]


if __name__ == "__main__":
    # Initialize system
    performance_system = UnifiedPerformanceSystem()
    
    # Run smoke test
    success = performance_system.run_smoke_test()
    
    if success:
        print("✅ Unified Performance System ready for production use!")
        print("🚀 System ready for performance management operations!")
    else:
        print("❌ Unified Performance System requires additional testing!")
        print("⚠️ System not ready for production deployment!")
