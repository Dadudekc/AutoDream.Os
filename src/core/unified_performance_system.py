#!/usr/bin/env python3
"""
Unified Performance System - Main Orchestrator

Main entry point for the modularized performance system.
Replaces the monolithic 1285-line file with a clean orchestrator.

Author: Agent-1 (Phase 1 Consolidation)
License: MIT
"""

from __future__ import annotations

import logging
import warnings
from typing import Any, Dict, List, Optional
from pathlib import Path

# Import modular components
from .performance.unified_performance_orchestrator import UnifiedPerformanceOrchestrator
from .performance.performance_core import PerformanceCore
from .performance.performance_monitoring import PerformanceMonitoring
from .performance.performance_validation import PerformanceValidation
from .performance.performance_benchmarking import PerformanceBenchmarking
from .performance.performance_reporting import PerformanceReporting

logger = logging.getLogger(__name__)


class UnifiedPerformanceSystem:
    """
    Main performance system orchestrator.
    
    Provides a unified interface to all performance components
    while maintaining backward compatibility.
    """
    
    def __init__(self, config_path: Optional[Path] = None, **orchestrator_kwargs: Any):
        """Initialize the unified performance system.

        Any additional keyword arguments are forwarded to
        :class:`UnifiedPerformanceOrchestrator` for configurability.
        """
        if config_path is not None:
            orchestrator_kwargs["config_path"] = config_path

        self.orchestrator = UnifiedPerformanceOrchestrator(**orchestrator_kwargs)
        self.core = PerformanceCore()
        self.monitoring = PerformanceMonitoring()
        self.validation = PerformanceValidation()
        self.benchmarking = PerformanceBenchmarking()
        self.reporting = PerformanceReporting()
        
        logger.info("Unified Performance System initialized successfully")
    
    def start_system(self) -> bool:
        """Start the performance system."""
        try:
            return self.orchestrator.start_system()
        except Exception as e:
            logger.error(f"Failed to start performance system: {e}")
            return False
    
    def stop_system(self) -> bool:
        """Stop the performance system."""
        try:
            return self.orchestrator.stop_system()
        except Exception as e:
            logger.error(f"Failed to stop performance system: {e}")
            return False
    
    def run_benchmarks(self, benchmark_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run performance benchmarks."""
        try:
            return self.orchestrator.run_benchmarks(benchmark_types)
        except Exception as e:
            logger.error(f"Failed to run benchmarks: {e}")
            return {}
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        try:
            return self.orchestrator.get_performance_summary()
        except Exception as e:
            logger.error(f"Failed to get performance summary: {e}")
            return {}
    
    def validate_performance(self, rules: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Validate performance against rules."""
        try:
            return self.orchestrator.validate_performance(rules)
        except Exception as e:
            logger.error(f"Failed to validate performance: {e}")
            return {}
    
    def generate_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate performance report."""
        try:
            return self.orchestrator.generate_report(report_type)
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return {}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        try:
            return self.orchestrator.get_system_status()
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {}
    
    # Backward compatibility methods
    def start(self) -> bool:
        """Backward compatibility: start system."""
        warnings.warn("start() is deprecated; use start_system()", DeprecationWarning, stacklevel=2)
        return self.start_system()
    
    def stop(self) -> bool:
        """Backward compatibility: stop system."""
        warnings.warn("stop() is deprecated; use stop_system()", DeprecationWarning, stacklevel=2)
        return self.stop_system()
    
    def benchmark(self, types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Backward compatibility: run benchmarks."""
        warnings.warn("benchmark() is deprecated; use run_benchmarks()", DeprecationWarning, stacklevel=2)
        return self.run_benchmarks(types)
    
    def summary(self) -> Dict[str, Any]:
        """Backward compatibility: get summary."""
        warnings.warn("summary() is deprecated; use get_performance_summary()", DeprecationWarning, stacklevel=2)
        return self.get_performance_summary()
    
    def validate(self, rules: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Backward compatibility: validate performance."""
        warnings.warn("validate() is deprecated; use validate_performance()", DeprecationWarning, stacklevel=2)
        return self.validate_performance(rules)
    
    def report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Backward compatibility: generate report."""
        warnings.warn("report() is deprecated; use generate_report()", DeprecationWarning, stacklevel=2)
        return self.generate_report(report_type)
    
    def status(self) -> Dict[str, Any]:
        """Backward compatibility: get status."""
        warnings.warn("status() is deprecated; use get_system_status()", DeprecationWarning, stacklevel=2)
        return self.get_system_status()


# Factory function for easy instantiation
def create_performance_system(config_path: Optional[Path] = None) -> UnifiedPerformanceSystem:
    """Create and return a new performance system instance."""
    return UnifiedPerformanceSystem(config_path=config_path)


# Main execution for CLI usage
if __name__ == "__main__":
    import sys
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create system
    system = UnifiedPerformanceSystem()
    
    # Handle CLI arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            success = system.start_system()
            print(f"System start: {'SUCCESS' if success else 'FAILED'}")
        elif command == "stop":
            success = system.stop_system()
            print(f"System stop: {'SUCCESS' if success else 'FAILED'}")
        elif command == "status":
            status = system.get_system_status()
            print(f"System status: {status}")
        elif command == "benchmark":
            results = system.run_benchmarks()
            print(f"Benchmark results: {results}")
        elif command == "summary":
            summary = system.get_performance_summary()
            print(f"Performance summary: {summary}")
        elif command == "report":
            report = system.generate_report()
            print(f"Report generated: {report}")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: start, stop, status, benchmark, summary, report")
    else:
        print("Unified Performance System - CLI Interface")
        print("Usage: python unified_performance_system.py [command]")
        print("Commands: start, stop, status, benchmark, summary, report")
