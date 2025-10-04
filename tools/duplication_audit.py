#!/usr/bin/env python3
"""
Duplication Audit Tool
=====================

Automated tool to audit codebase for duplication and integration issues.
Part of the Duplication Prevention Protocol.

Author: Agent 5 (Quality Assurance Specialist)
License: MIT
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = __import__("logging").getLogger(__name__)


class CodeDuplicationAnalyzer:
    """Analyze codebase for duplication and integration issues."""

    def __init__(self):
        """Initialize duplication analyzer."""
        self.duplicate_files = []
        self.integration_issues = []
        self.redundant_systems = []

    def analyze_v3_duplication(self) -> dict[str, Any]:
        """Analyze V3 system for duplication with V2."""
        results = {
            "total_files": 0,
            "duplicate_files": 0,
            "integration_issues": 0,
            "redundant_systems": [],
            "consolidation_opportunities": [],
            "files_to_keep": [],
            "files_to_delete": [],
        }

        # Get all V3 files
        v3_dir = Path("src/v3")
        if not v3_dir.exists():
            return results

        v3_files = list(v3_dir.rglob("*.py"))
        results["total_files"] = len(v3_files)

        # Analyze each V3 file
        for v3_file in v3_files:
            analysis = self._analyze_single_file(v3_file)
            if analysis["is_duplicate"]:
                results["duplicate_files"] += 1
                results["files_to_delete"].append(str(v3_file))
            elif analysis["has_value"]:
                results["files_to_keep"].append(str(v3_file))
            else:
                results["files_to_delete"].append(str(v3_file))

            if analysis["integration_issues"]:
                results["integration_issues"] += len(analysis["integration_issues"])
                results["consolidation_opportunities"].extend(analysis["integration_issues"])

        return results

    def _analyze_single_file(self, v3_file: Path) -> dict[str, Any]:
        """Analyze a single V3 file for duplication."""
        result = {
            "file": str(v3_file),
            "is_duplicate": False,
            "has_value": False,
            "integration_issues": [],
            "similar_files": [],
        }

        try:
            with open(v3_file) as f:
                content = f.read()

            # Check for V2 equivalent patterns
            v2_equivalent = self._find_v2_equivalent(v3_file, content)
            if v2_equivalent:
                result["is_duplicate"] = True
                result["similar_files"].append(v2_equivalent)

            # Check for valuable features
            if self._has_unique_value(content):
                result["has_value"] = True

            # Check for integration issues
            result["integration_issues"] = self._check_integration_issues(v3_file, content)

        except Exception as e:
            logger.error(f"Error analyzing {v3_file}: {e}")

        return result

    def _find_v2_equivalent(self, v3_file: Path, content: str) -> Optional[str]:
        """Find V2 equivalent for V3 file."""
        filename = v3_file.name.lower()

        # Known V3->V2 mappings
        mappings = {
            "cloud_infrastructure_coordinator.py": "src/infrastructure/cloud/",
            "ml_pipeline_coordinator.py": "src/ml/ml_pipeline_system.py",
            "tracing_coordinator.py": "src/tracing/distributed_tracing_system.py",
            "v3_011_api_gateway_core.py": "src/services/api_gateway/",
            "v3_012_mobile_app_framework.py": "src/mobile/",
            "v3_009_command_understanding.py": "src/services/messaging/",
            "web_dashboard_coordinator.py": "src/services/dashboard/",
        }

        for v3_pattern, v2_equivalent in mappings.items():
            if v3_pattern in filename:
                return v2_equivalent

        return None

    def _has_unique_value(self, content: str) -> bool:
        """Check if file has unique value beyond duplication."""
        # Check for production-ready features
        production_indicators = [
            "deploy",
            "production",
            "aws",
            "azure",
            "kubernetes",
            "docker",
            "terraform",
            "monitoring",
            "metrics",
            "app store",
            "mobile app",
            "real-time",
            "dashboard",
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in production_indicators)

    def _check_integration_issues(self, v3_file: Path, content: str) -> list[str]:
        """Check for integration issues with existing systems."""
        issues = []

        # Check for standalone implementation (should be integrated)
        if "class.*Coordinator" in content and "V3-" in str(v3_file):
            issues.append("Standalone coordinator - should integrate with existing system")

        # Check for duplicate imports
        if content.count("from src.") > 3:
            issues.append("Multiple imports suggest duplication")

        # Check for V3-specific patterns that should be generic
        if "V3-" in content and "V2" not in content:
            issues.append("V3-specific implementation - should be generic")

        return issues


class IntegrationHealthChecker:
    """Check integration health across systems."""

    def __init__(self):
        """Initialize health checker."""
        self.systems = self._load_systems()

    def _load_systems(self) -> dict[str, dict[str, Any]]:
        """Load system definitions."""
        return {
            "messaging": {
                "files": ["src/services/messaging_service.py"],
                "dependencies": ["coordinate_manager"],
                "status": "operational",
            },
            "ml_pipeline": {
                "files": ["src/ml/ml_pipeline_system.py"],
                "dependencies": ["tensorflow", "pytorch"],
                "status": "operational",
            },
            "tracing": {
                "files": ["src/tracing/distributed_tracing_system.py"],
                "dependencies": ["opentelemetry", "jaeger"],
                "status": "operational",
            },
            "dashboard": {
                "files": ["src/services/dashboard/"],
                "dependencies": ["web_interface"],
                "status": "operational",
            },
            "mobile": {
                "files": ["src/mobile/"],
                "dependencies": ["react_native"],
                "status": "built",
            },
        }

    def check_system_health(self) -> dict[str, Any]:
        """Check health of all systems."""
        health = {
            "overall_status": "healthy",
            "systems": {},
            "integration_issues": [],
            "recommendations": [],
        }

        for system_name, system_info in self.systems.items():
            system_health = self._check_single_system(system_name, system_info)
            health["systems"][system_name] = system_health

            if system_health["status"] != "healthy":
                health["overall_status"] = "degraded"
                health["integration_issues"].extend(system_health["issues"])

        return health

    def _check_single_system(self, system_name: str, system_info: dict[str, Any]) -> dict[str, Any]:
        """Check health of single system."""
        health = {"status": "healthy", "files_exist": True, "issues": [], "recommendations": []}

        # Check if files exist
        for file_path in system_info["files"]:
            if not Path(file_path).exists():
                health["status"] = "missing_files"
                health["issues"].append(f"Missing file: {file_path}")

        # Check V3 duplication
        v3_duplicates = self._find_v3_duplicates(system_name)
        if v3_duplicates:
            health["status"] = "has_duplicates"
            health["issues"].append(f"V3 duplicates found: {len(v3_duplicates)} files")
            health["recommendations"].append("Consolidate V3 features into this system")

        return health

    def _find_v3_duplicates(self, system_name: str) -> list[str]:
        """Find V3 files that duplicate this system."""
        duplicates = []

        v3_dir = Path("src/v3")
        if not v3_dir.exists():
            return duplicates

        # Mapping of system names to V3 file patterns
        v3_patterns = {
            "messaging": ["command_understanding", "nlp_pipeline", "response_generation"],
            "ml_pipeline": ["ml_pipeline", "v3_007"],
            "tracing": ["tracing", "v3_004"],
            "dashboard": ["web_dashboard", "v3_010"],
            "mobile": ["mobile_app", "ui_components", "v3_012"],
            "api_gateway": ["api_gateway", "v3_011"],
        }

        if system_name in v3_patterns:
            for pattern in v3_patterns[system_name]:
                for v3_file in v3_dir.rglob("*.py"):
                    if pattern in v3_file.name:
                        duplicates.append(str(v3_file))

        return duplicates


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Duplication Audit Tool")
    parser.add_argument("--v3-analysis", action="store_true", help="Analyze V3 duplication")
    parser.add_argument("--system-health", action="store_true", help="Check system health")
    parser.add_argument("--week-summary", action="store_true", help="Generate weekly summary")

    args = parser.parse_args()

    print("🛡️ DUPLICATION AUDIT TOOL")
    print("=" * 50)

    if args.v3_analysis:
        analyzer = CodeDuplicationAnalyzer()
        results = analyzer.analyze_v3_duplication()

        print("📊 V3 DUPLICATION ANALYSIS")
        print(f"Total V3 Files: {results['total_files']}")
        print(f"Duplicate Files: {results['duplicate_files']}")
        print(f"Integration Issues: {results['integration_issues']}")

        if results["files_to_keep"]:
            print(f"\n✅ Files to Keep ({len(results['files_to_keep'])}):")
            for file in results["files_to_keep"]:
                print(f"  • {file}")

        if results["files_to_delete"]:
            print(f"\n🗑️ Files to Delete ({len(results['files_to_delete'])}):")
            for file in results["files_to_delete"]:
                print(f"  • {file}")

    if args.system_health:
        health_checker = IntegrationHealthChecker()
        health = health_checker.check_system_health()

        print("🏥 SYSTEM HEALTH CHECK")
        print(f"Overall Status: {health['overall_status'].upper()}")

        for system_name, system_health in health["systems"].items():
            status_emoji = "✅" if system_health["status"] == "healthy" else "⚠️"
            print(f"  {status_emoji} {system_name}: {system_health['status']}")

            if system_health["issues"]:
                for issue in system_health["issues"]:
                    print(f"    • {issue}")

        if health["integration_issues"]:
            print("❌ INTEGRATION ISSUES:")
            for issue in health["integration_issues"]:
                print(f"  • {issue}")

    if args.week_summary:
        print("📅 WEEKLY AUDIT SUMMARY")
        print("Date: " + str(datetime.now().date()))
        print("Status: CONSOLIDATION IN PROGRESS")

        # Generate summary statistics
        analyzer = CodeDuplicationAnalyzer()
        v3_results = analyzer.analyze_v3_duplication()

        health_checker = IntegrationHealthChecker()
        health = health_checker.check_system_health()

        print("📊 CONSOLIDATION PROGRESS:")
        print(f"  • V3 Files Analyzed: {v3_results['total_files']}")
        print(f"  • Duplicates Identified: {v3_results['duplicate_files']}")
        print(f"  • Files Ready for Integration: {len(v3_results['files_to_keep'])}")
        print(f"  • System Health: {health['overall_status']}")

        print("🎯 NEXT WEEK PRIORITIES:")
        print("  1. Complete Phase 1: Critical Infrastructure")
        print("  2. Deploy ML pipeline to production")
        print("  3. Deploy API gateway with enhanced features")
        print("  4. Begin Phase 2: Monitoring & Tracing")

    return 0


if __name__ == "__main__":
    exit(main())
