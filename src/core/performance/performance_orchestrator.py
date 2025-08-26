#!/usr/bin/env python3
"""
Performance Orchestrator - Unified Performance Validation System Coordinator
==========================================================================

Main performance validation coordinator consolidated from multiple files.
Follows Single Responsibility Principle with focused orchestration functionality.

Author: Performance Validation Consolidation Team
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import the consolidated performance modules
try:
    from .performance_core import PerformanceValidationCore, BenchmarkResult
    from .performance_reporter import PerformanceReporter, SystemPerformanceReport
    from .performance_config import PerformanceConfigManager, PerformanceValidationConfig
    from .benchmark_executor import BenchmarkExecutor, BenchmarkExecutionConfig
    from .metrics_collector import PerformanceMetricsCollector
except ImportError:
    # Fallback imports for standalone testing
    from performance_core import PerformanceValidationCore, BenchmarkResult
    from performance_reporter import PerformanceReporter, SystemPerformanceReport
    from performance_config import PerformanceConfigManager, PerformanceValidationConfig
    from benchmark_executor import BenchmarkExecutor, BenchmarkExecutionConfig
    from metrics_collector import PerformanceMetricsCollector


class PerformanceValidationOrchestrator:
    """
    Main performance validation system coordinator.
    
    Responsibilities:
    - Main performance validation coordinator
    - Module orchestration
    - Workflow management
    - Error handling and recovery
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = logging.getLogger(f"{__name__}.PerformanceValidationOrchestrator")
        
        # Initialize core components
        self.config_manager = PerformanceConfigManager(config_file)
        self.core = PerformanceValidationCore()
        self.reporter = PerformanceReporter()
        self.benchmark_executor = BenchmarkExecutor()
        self.metrics_collector = PerformanceMetricsCollector()
        
        # System state
        self.is_running = False
        self.current_benchmark_id: Optional[str] = None
        self.benchmark_history: List[BenchmarkResult] = []
        
        # Performance tracking
        self.start_time: Optional[datetime] = None
        self.total_benchmarks_run = 0
        self.successful_benchmarks = 0
        self.failed_benchmarks = 0
        
        self.logger.info("Performance Validation Orchestrator initialized")
    
    def start_system(self) -> bool:
        """
        Start the performance validation system.
        
        Returns:
            True if system started successfully, False otherwise
        """
        try:
            if self.is_running:
                self.logger.warning("System is already running")
                return True
            
            # Validate configuration
            config_errors = self.config_manager.validate_config()
            if config_errors:
                self.logger.error(f"Configuration validation failed: {len(config_errors)} errors")
                for error in config_errors:
                    self.logger.error(f"  - {error}")
                return False
            
            # Initialize system state
            self.is_running = True
            self.start_time = datetime.now()
            self.total_benchmarks_run = 0
            self.successful_benchmarks = 0
            self.failed_benchmarks = 0
            
            self.logger.info("Performance validation system started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start system: {e}")
            return False
    
    def stop_system(self) -> bool:
        """
        Stop the performance validation system.
        
        Returns:
            True if system stopped successfully, False otherwise
        """
        try:
            if not self.is_running:
                self.logger.warning("System is not running")
                return True
            
            # Stop any running benchmarks
            if self.current_benchmark_id:
                self.logger.info(f"Stopping current benchmark: {self.current_benchmark_id}")
                self.current_benchmark_id = None
            
            # Update system state
            self.is_running = False
            
            # Generate final report
            if self.benchmark_history:
                self._generate_final_report()
            
            self.logger.info("Performance validation system stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop system: {e}")
            return False
    
    def run_comprehensive_benchmark(self) -> str:
        """
        Run comprehensive performance benchmark suite.
        
        Returns:
            Benchmark ID if successful, None otherwise
        """
        try:
            if not self.is_running:
                self.logger.error("System is not running")
                return None
            
            # Generate benchmark ID
            benchmark_id = str(uuid.uuid4())
            self.current_benchmark_id = benchmark_id
            
            self.logger.info(f"Starting comprehensive benchmark: {benchmark_id}")
            
            # Get enabled benchmarks
            enabled_benchmarks = self.config_manager.get_enabled_benchmarks()
            if not enabled_benchmarks:
                self.logger.warning("No benchmarks are currently enabled")
                return None
            
            # Run all enabled benchmarks
            benchmark_results = []
            start_time = datetime.now()
            
            for benchmark_type in enabled_benchmarks:
                try:
                    self.logger.info(f"Running {benchmark_type} benchmark...")
                    
                    # Get benchmark configuration
                    config = self.config_manager.get_benchmark_config(benchmark_type)
                    if not config:
                        self.logger.warning(f"Benchmark type '{benchmark_type}' not found or disabled")
                        continue
                    
                    # Convert to execution config
                    exec_config = BenchmarkExecutionConfig(
                        benchmark_type=benchmark_type,
                        timeout_seconds=config.timeout_seconds,
                        max_iterations=config.max_iterations,
                        warmup_iterations=config.warmup_iterations,
                        target_metrics=config.target_metrics
                    )
                    
                    # Run individual benchmark
                    result = self.benchmark_executor.execute_benchmark(
                        benchmark_type, exec_config, self.core
                    )
                    
                    if result:
                        benchmark_results.append(result)
                        self.successful_benchmarks += 1
                    else:
                        self.failed_benchmarks += 1
                    
                    self.total_benchmarks_run += 1
                    
                except Exception as e:
                    self.logger.error(f"Error running {benchmark_type} benchmark: {e}")
                    self.failed_benchmarks += 1
                    self.total_benchmarks_run += 1
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Store results
            self.benchmark_history.extend(benchmark_results)
            
            # Generate performance report
            if benchmark_results:
                report = self.reporter.generate_performance_report(benchmark_results)
                self.logger.info(f"Generated performance report: {report.report_id}")
            
            # Clear current benchmark
            self.current_benchmark_id = None
            
            self.logger.info(
                f"Comprehensive benchmark completed: {benchmark_id} "
                f"in {duration:.2f}s "
                f"({self.successful_benchmarks} successful, {self.failed_benchmarks} failed)"
            )
            
            return benchmark_id
            
        except Exception as e:
            self.logger.error(f"Error running comprehensive benchmark: {e}")
            self.current_benchmark_id = None
            return None
    
    def run_single_benchmark(self, benchmark_type: str) -> Optional[BenchmarkResult]:
        """
        Run a single benchmark type.
        
        Args:
            benchmark_type: Type of benchmark to run
            
        Returns:
            BenchmarkResult if successful, None otherwise
        """
        try:
            if not self.is_running:
                self.logger.error("System is not running")
                return None
            
            # Get benchmark configuration
            config = self.config_manager.get_benchmark_config(benchmark_type)
            if not config:
                self.logger.warning(f"Benchmark type '{benchmark_type}' not found or disabled")
                return None
            
            # Convert to execution config
            exec_config = BenchmarkExecutionConfig(
                benchmark_type=benchmark_type,
                timeout_seconds=config.timeout_seconds,
                max_iterations=config.max_iterations,
                warmup_iterations=config.warmup_iterations,
                target_metrics=config.target_metrics
            )
            
            # Execute benchmark
            result = self.benchmark_executor.execute_benchmark(
                benchmark_type, exec_config, self.core
            )
            
            if result:
                self.benchmark_history.append(result)
                self.successful_benchmarks += 1
                self.total_benchmarks_run += 1
                
                self.logger.info(
                    f"Benchmark {benchmark_type} completed: "
                    f"{result.performance_level} level in {result.duration:.2f}s"
                )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error running {benchmark_type} benchmark: {e}")
            self.failed_benchmarks += 1
            self.total_benchmarks_run += 1
            return None
    
    def get_benchmark_history(self) -> List[BenchmarkResult]:
        """Get complete benchmark execution history."""
        return self.benchmark_history.copy()
    
    def get_agent_health(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get health status for a specific agent.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Agent health data or None if not found
        """
        try:
            # This would typically integrate with the health monitoring system
            # For now, return basic status
            return {
                "agent_id": agent_id,
                "status": "healthy" if self.is_running else "inactive",
                "last_benchmark": self.current_benchmark_id,
                "total_benchmarks": self.total_benchmarks_run
            }
        except Exception as e:
            self.logger.error(f"Error getting agent health for {agent_id}: {e}")
            return None
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary."""
        try:
            return {
                "monitoring_active": self.is_running,
                "total_benchmarks": self.total_benchmarks_run,
                "successful_benchmarks": self.successful_benchmarks,
                "failed_benchmarks": self.failed_benchmarks,
                "success_rate": (self.successful_benchmarks / self.total_benchmarks_run * 100) if self.total_benchmarks_run > 0 else 0,
                "current_benchmark": self.current_benchmark_id,
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "uptime": (datetime.now() - self.start_time).total_seconds() if self.start_time and self.is_running else 0
            }
        except Exception as e:
            self.logger.error(f"Error generating health summary: {e}")
            return {"error": str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        try:
            uptime_seconds = (datetime.now() - self.start_time).total_seconds() if self.start_time and self.is_running else 0
            
            # Format uptime
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            seconds = int(uptime_seconds % 60)
            uptime_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            return {
                "system_status": "running" if self.is_running else "stopped",
                "uptime_seconds": uptime_seconds,
                "uptime_formatted": uptime_formatted,
                "current_benchmark": self.current_benchmark_id,
                "benchmarks_in_history": len(self.benchmark_history),
                "last_update": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    def _generate_final_report(self) -> Optional[SystemPerformanceReport]:
        """Generate final system report."""
        try:
            if not self.benchmark_history:
                self.logger.warning("No benchmark history to report")
                return None
            
            # Generate comprehensive report from all history
            report = self.reporter.generate_performance_report(
                self.benchmark_history,
                "json"
            )
            
            self.logger.info(f"Generated final system report: {report.report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate final report: {e}")
            return None
    
    def export_system_report(self, filepath: str, format_type: str = "json") -> bool:
        """
        Export complete system report to file.
        
        Args:
            filepath: Path to export file
            format_type: Export format
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if not self.benchmark_history:
                self.logger.warning("No benchmark history to export")
                return False
            
            # Generate comprehensive report
            report = self.reporter.generate_performance_report(
                self.benchmark_history,
                format_type
            )
            
            # Export to file
            formatted_report = self.reporter.format_report(report, format_type)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted_report)
            
            self.logger.info(f"System report exported to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export system report: {e}")
            return False
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get performance summary statistics.
        
        Returns:
            Dictionary containing performance summary
        """
        if not self.benchmark_history:
            return {"message": "No benchmark history available"}
        
        try:
            # Use the benchmark executor's summary functionality
            execution_summary = self.benchmark_executor.get_execution_summary()
            
            # Add system-specific information
            system_status = self.get_system_status()
            
            return {
                **execution_summary,
                "system_uptime": system_status.get("uptime_formatted", "Unknown"),
                "system_status": system_status.get("system_status", "Unknown")
            }
            
        except Exception as e:
            self.logger.error(f"Error generating performance summary: {e}")
            return {"error": str(e)}
    
    def run_smoke_test(self) -> bool:
        """Run basic smoke test to verify system functionality."""
        try:
            self.logger.info("Running performance orchestrator smoke test...")
            
            # Test basic initialization
            assert self.config_manager is not None, "Config manager not initialized"
            assert self.core is not None, "Core not initialized"
            assert self.reporter is not None, "Reporter not initialized"
            assert self.benchmark_executor is not None, "Benchmark executor not initialized"
            
            # Test system start/stop
            start_result = self.start_system()
            assert start_result, "System failed to start"
            
            stop_result = self.stop_system()
            assert stop_result, "System failed to stop"
            
            # Test status methods
            status = self.get_system_status()
            assert "system_status" in status, "System status missing required fields"
            
            health_summary = self.get_health_summary()
            assert "monitoring_active" in health_summary, "Health summary missing required fields"
            
            self.logger.info("✅ Performance orchestrator smoke test PASSED")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Performance orchestrator smoke test FAILED: {e}")
            return False
