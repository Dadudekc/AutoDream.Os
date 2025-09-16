#!/usr/bin/env python3
"""
Swarm Testing Framework Main Module
===================================

Main orchestration module for the swarm testing framework.
Part of the modularized swarm_testing_framework.py (651 lines → 3 modules).

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import sys
from pathlib import Path

from .swarm_testing_framework_core import ComponentDiscovery, SwarmTestingReport
from .swarm_testing_framework_execution import TestExecutor
from .swarm_testing_framework_reporting import ReportGenerator

logger = logging.getLogger(__name__)


class SwarmTestingFramework:
    """Main orchestration class for the swarm testing framework."""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.component_discovery = ComponentDiscovery(self.project_root)
        self.test_executor = TestExecutor(self.project_root)
        self.report_generator = ReportGenerator(self.project_root)
        
        logger.info("🐝 Swarm Testing Framework initialized")
        logger.info(f"📁 Project root: {self.project_root}")
    
    def discover_components(self) -> dict:
        """Discover all testable components in the project."""
        return self.component_discovery.discover_components()
    
    def run_comprehensive_testing(self) -> SwarmTestingReport:
        """Run comprehensive testing across all discovered components."""
        logger.info("🚀 Starting comprehensive swarm testing mission...")
        
        # Ensure we have discovered components
        if not self.component_discovery.components:
            self.discover_components()
        
        # Run comprehensive testing
        report = self.test_executor.run_comprehensive_testing(
            self.component_discovery.components
        )
        
        # Generate reports
        self.report_generator.generate_testing_report(report)
        self.report_generator.generate_analytics_report(report)
        
        # Print summary
        self.report_generator.print_summary(report)
        
        logger.info("🏆 Comprehensive testing mission completed!")
        return report
    
    def test_specific_component(self, component_name: str) -> bool:
        """Test a specific component by name."""
        if component_name not in self.component_discovery.components:
            logger.error(f"Component {component_name} not found")
            return False
        
        component = self.component_discovery.components[component_name]
        report = SwarmTestingReport()
        report.component_reports = {component_name: component}
        
        self.test_executor._test_component(component, report)
        
        return component.test_status == "passed"
    
    def get_component_status(self, component_name: str) -> dict:
        """Get detailed status information for a specific component."""
        if component_name not in self.component_discovery.components:
            return {"error": f"Component {component_name} not found"}
        
        component = self.component_discovery.components[component_name]
        
        return {
            "name": component.name,
            "path": str(component.path),
            "type": component.component_type,
            "priority": component.priority,
            "status": component.test_status,
            "coverage": component.test_coverage,
            "has_examples": component.example_usage,
            "last_tested": component.last_tested.isoformat() if component.last_tested else None,
            "dependencies": component.dependencies,
            "test_files": [str(f) for f in component.test_files]
        }
    
    def validate_framework(self) -> dict:
        """Validate the testing framework configuration."""
        validation_results = {
            "project_root_exists": self.project_root.exists(),
            "test_results_dir_exists": self.report_generator.test_results_dir.exists(),
            "components_discovered": len(self.component_discovery.components) > 0,
            "framework_ready": True
        }
        
        # Check for common issues
        issues = []
        if not validation_results["project_root_exists"]:
            issues.append("Project root directory does not exist")
        
        if not validation_results["test_results_dir_exists"]:
            issues.append("Test results directory could not be created")
        
        if not validation_results["components_discovered"]:
            issues.append("No components discovered - check project structure")
        
        validation_results["issues"] = issues
        validation_results["framework_ready"] = len(issues) == 0
        
        return validation_results


def main():
    """Main entry point for the swarm testing framework."""
    logger.info("🎯 Objective: Test every component, document every file")
    
    # Initialize framework
    framework = SwarmTestingFramework()
    
    # Validate framework
    validation = framework.validate_framework()
    if not validation["framework_ready"]:
        logger.error("Framework validation failed:")
        for issue in validation["issues"]:
            logger.error(f"  - {issue}")
        return 1
    
    # Discover all components
    components = framework.discover_components()
    logger.info(f"Discovered {len(components)} components")
    
    # Run comprehensive testing
    report = framework.run_comprehensive_testing()
    
    # Print final summary
    print(f"""
🐝 SWARM TESTING MISSION ACCOMPLISHMENT REPORT 🐝
================================================

📊 Testing Summary:
   • Total Components: {report.total_components}
   • Tested Components: {report.tested_components}
   • Passed Tests: {report.passed_tests}
   • Failed Tests: {report.failed_tests}
   • Documented Components: {report.documented_components}

🎯 Coverage Achieved:
   • Test Coverage: {report.coverage_percentage:.1f}%
   • Documentation Coverage: {(report.documented_components / report.total_components * 100):.1f}%

⚡ Mission Status: {"COMPLETE" if report.tested_components == report.total_components else "IN PROGRESS"}

🏆 Mission Accomplishment: {"SUCCESS" if report.failed_tests == 0 else "PARTIAL SUCCESS"}
""")
    
    return 0 if report.failed_tests == 0 else 1


if __name__ == "__main__":
    exit(main())
