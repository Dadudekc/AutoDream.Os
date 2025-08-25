#!/usr/bin/env python3
"""
Performance Validation CLI - V2 Core Performance Testing CLI Interface
====================================================================

Command-line interface for the performance validation system.
Follows V2 coding standards with clean OOP design and SRP compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import argparse
import json
import logging
from typing import Dict, Any

from src.utils.stability_improvements import stability_manager, safe_import

# Import the main performance validation system
try:
    from .performance_validation_system import PerformanceValidationSystem
    from .agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
    from .config_manager import ConfigManager
    from .assignment_engine import ContractManager
except ImportError:
    from performance_validation_system import PerformanceValidationSystem
    from agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
    from config_manager import ConfigManager
    from assignment_engine import ContractManager


class PerformanceValidationCLI:
    """Command-line interface for the performance validation system."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser."""
        parser = argparse.ArgumentParser(description="Performance Validation System CLI")
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Test command
        test_parser = subparsers.add_parser("test", help="Run smoke test")
        test_parser.set_defaults(func=self._run_test)
        
        # Benchmark command
        benchmark_parser = subparsers.add_parser("benchmark", help="Run comprehensive benchmark")
        benchmark_parser.set_defaults(func=self._run_benchmark)
        
        # Summary command
        summary_parser = subparsers.add_parser("summary", help="Show benchmark summary")
        summary_parser.set_defaults(func=self._show_summary)
        
        # Report command
        report_parser = subparsers.add_parser("report", help="Show latest performance report")
        report_parser.set_defaults(func=self._show_report)
        
        # Status command
        status_parser = subparsers.add_parser("status", help="Show system status")
        status_parser.set_defaults(func=self._show_status)
        
        return parser
    
    def _initialize_system(self) -> PerformanceValidationSystem:
        """Initialize the performance validation system."""
        try:
            # Initialize managers
            config_manager = ConfigManager()
            agent_manager = AgentManager()
            contract_manager = ContractManager(agent_manager, config_manager)
            
            # Initialize workflow engine (mock)
            class MockWorkflowEngine:
                def __init__(self):
                    self.workflows = {}
            
            workflow_engine = MockWorkflowEngine()
            
            # Initialize performance validation system
            return PerformanceValidationSystem(
                agent_manager, config_manager, contract_manager, workflow_engine
            )
            
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {e}")
            raise
    
    def _run_test(self, args: argparse.Namespace) -> bool:
        """Run smoke test."""
        try:
            print("🧪 Running Performance Validation System Smoke Test...")
            
            perf_system = self._initialize_system()
            success = perf_system.run_smoke_test()
            
            if success:
                print("✅ Performance Validation System Smoke Test PASSED")
            else:
                print("❌ Performance Validation System Smoke Test FAILED")
            
            return success
            
        except Exception as e:
            print(f"❌ Performance Validation System Smoke Test FAILED: {e}")
            return False
    
    def _run_benchmark(self, args: argparse.Namespace) -> None:
        """Run comprehensive benchmark."""
        try:
            print("🚀 Running Comprehensive Performance Benchmark...")
            
            perf_system = self._initialize_system()
            benchmark_id = perf_system.run_comprehensive_benchmark()
            
            if benchmark_id:
                print(f"✅ Benchmark completed successfully: {benchmark_id}")
            else:
                print("❌ Benchmark failed to complete")
                
        except Exception as e:
            print(f"❌ Benchmark execution failed: {e}")
    
    def _show_summary(self, args: argparse.Namespace) -> None:
        """Show benchmark summary."""
        try:
            print("📊 Performance Benchmark Summary:")
            
            perf_system = self._initialize_system()
            summary = perf_system.get_benchmark_summary()
            
            if "total_benchmarks" in summary:
                print(json.dumps(summary, indent=2))
            else:
                print("No benchmark data available")
                
        except Exception as e:
            print(f"❌ Failed to retrieve benchmark summary: {e}")
    
    def _show_report(self, args: argparse.Namespace) -> None:
        """Show latest performance report."""
        try:
            print("📋 Latest Performance Report:")
            
            perf_system = self._initialize_system()
            report = perf_system.get_latest_performance_report()
            
            if report:
                formatted_report = perf_system.report_generator.format_report_as_text(report)
                print(formatted_report)
            else:
                print("No performance reports available")
                
        except Exception as e:
            print(f"❌ Failed to retrieve performance report: {e}")
    
    def _show_status(self, args: argparse.Namespace) -> None:
        """Show system status."""
        try:
            print("🔍 Performance Validation System Status:")
            
            perf_system = self._initialize_system()
            
            # Get various status information
            benchmark_summary = perf_system.get_benchmark_summary()
            active_alerts = perf_system.get_active_alerts()
            alert_summary = perf_system.get_alert_summary()
            
            status_info = {
                "benchmarks": benchmark_summary,
                "active_alerts": len(active_alerts) if active_alerts else 0,
                "alert_summary": alert_summary
            }
            
            print(json.dumps(status_info, indent=2))
            
        except Exception as e:
            print(f"❌ Failed to retrieve system status: {e}")
    
    def run(self, args: list = None) -> int:
        """Run the CLI with the given arguments."""
        try:
            parsed_args = self.parser.parse_args(args)
            
            if not parsed_args.command:
                self.parser.print_help()
                return 1
            
            # Execute the selected command
            result = parsed_args.func(parsed_args)
            
            if isinstance(result, bool):
                return 0 if result else 1
            else:
                return 0
                
        except SystemExit:
            return 1
        except Exception as e:
            self.logger.error(f"CLI execution failed: {e}")
            print(f"❌ CLI execution failed: {e}")
            return 1


def main():
    """Main entry point for the CLI."""
    cli = PerformanceValidationCLI()
    exit_code = cli.run()
    exit(exit_code)


if __name__ == "__main__":
    main()
