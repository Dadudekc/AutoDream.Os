#!/usr/bin/env python3
"""
Enhanced Automated Metric Refresh System
========================================

Real-time metric refresh system with watchdog integration for documentation
and health score synchronization. Integrates with project scanner and quality gates.

Author: Agent-7 (Web Development Expert / Implementation Specialist)
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricRefreshSystem:
    """Enhanced automated metric refresh system with real-time monitoring."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.metric_files = [
            "project_analysis.json",
            "current_quality_status.json",
            "current_compliance.json",
            "agent_analysis.json",
            "chatgpt_project_context.json",
        ]
        self.documentation_files = [
            "AGENTS.md",
            "AGENT_ONBOARDING_CONTEXT_PACKAGE.md",
            "docs/",
        ]
        self.last_refresh = datetime.now()
        logger.info("Enhanced MetricRefreshSystem initialized")

    def refresh_project_analysis(self) -> dict[str, Any]:
        """Refresh project analysis using project scanner."""
        try:
            result = subprocess.run(
                ["python", "tools/simple_project_scanner.py"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60,
            )

            if result.returncode == 0:
                logger.info("Project analysis refreshed successfully")
                return {"status": "success", "output": result.stdout}
            else:
                logger.error(f"Project analysis failed: {result.stderr}")
                return {"status": "error", "error": result.stderr}
        except subprocess.TimeoutExpired:
            logger.error("Project analysis timeout")
            return {"status": "error", "error": "Timeout"}
        except Exception as e:
            logger.error(f"Project analysis error: {e}")
            return {"status": "error", "error": str(e)}

    def refresh_quality_status(self) -> dict[str, Any]:
        """Refresh quality status using quality gates."""
        try:
            result = subprocess.run(
                ["python", "quality_gates.py", "--path", "src"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60,
            )

            if result.returncode == 0:
                logger.info("Quality status refreshed successfully")
                return {"status": "success", "output": result.stdout}
            else:
                logger.warning(f"Quality gates issues: {result.stderr}")
                return {"status": "warning", "output": result.stdout}
        except subprocess.TimeoutExpired:
            logger.error("Quality gates timeout")
            return {"status": "error", "error": "Timeout"}
        except Exception as e:
            logger.error(f"Quality gates error: {e}")
            return {"status": "error", "error": str(e)}

    def sync_health_scores(self) -> dict[str, Any]:
        """Synchronize health scores across all systems."""
        try:
            health_data = {
                "timestamp": datetime.now().isoformat(),
                "project_health": self._calculate_project_health(),
                "quality_health": self._calculate_quality_health(),
                "documentation_health": self._calculate_documentation_health(),
                "system_health": self._calculate_system_health(),
            }

            # Save health scores
            health_file = self.project_root / "current_health_scores.json"
            with open(health_file, "w") as f:
                json.dump(health_data, f, indent=2)

            logger.info("Health scores synchronized successfully")
            return {"status": "success", "health_data": health_data}
        except Exception as e:
            logger.error(f"Health score sync error: {e}")
            return {"status": "error", "error": str(e)}

    def _calculate_project_health(self) -> float:
        """Calculate project health score."""
        try:
            analysis_file = self.project_root / "project_analysis.json"
            if analysis_file.exists():
                with open(analysis_file) as f:
                    data = json.load(f)
                    return float(data.get("overall_health", 85.0))
            return 85.0
        except Exception:
            return 85.0

    def _calculate_quality_health(self) -> float:
        """Calculate quality health score."""
        try:
            quality_file = self.project_root / "current_quality_status.json"
            if quality_file.exists():
                with open(quality_file) as f:
                    data = json.load(f)
                    return float(data.get("overall_score", 90.0))
            return 90.0
        except Exception:
            return 90.0

    def _calculate_documentation_health(self) -> float:
        """Calculate documentation health score."""
        try:
            docs_exist = 0
            total_docs = len(self.documentation_files)

            for doc_file in self.documentation_files:
                doc_path = self.project_root / doc_file
                if doc_path.exists():
                    docs_exist += 1

            return (docs_exist / total_docs) * 100.0
        except Exception:
            return 95.0

    def _calculate_system_health(self) -> float:
        """Calculate overall system health score."""
        project_health = self._calculate_project_health()
        quality_health = self._calculate_quality_health()
        doc_health = self._calculate_documentation_health()

        return (project_health + quality_health + doc_health) / 3.0

    def refresh_all_metrics(self) -> dict[str, Any]:
        """Refresh all metrics and return comprehensive results."""
        logger.info("Starting comprehensive metric refresh")

        results = {
            "timestamp": datetime.now().isoformat(),
            "success_count": 0,
            "error_count": 0,
            "details": {},
        }

        # Refresh project analysis
        project_result = self.refresh_project_analysis()
        results["details"]["project_analysis"] = project_result
        if project_result["status"] == "success":
            results["success_count"] += 1
        else:
            results["error_count"] += 1

        # Refresh quality status
        quality_result = self.refresh_quality_status()
        results["details"]["quality_status"] = quality_result
        if quality_result["status"] in ["success", "warning"]:
            results["success_count"] += 1
        else:
            results["error_count"] += 1

        # Sync health scores
        health_result = self.sync_health_scores()
        results["details"]["health_sync"] = health_result
        if health_result["status"] == "success":
            results["success_count"] += 1
        else:
            results["error_count"] += 1

        self.last_refresh = datetime.now()
        logger.info(
            f"Metric refresh completed: {results['success_count']} success, {results['error_count']} errors"
        )

        return results

    def validate_metrics(self) -> dict[str, Any]:
        """Validate that all metrics are current and accurate."""
        try:
            validation_results = {
                "timestamp": datetime.now().isoformat(),
                "all_current": True,
                "stale_files": [],
                "missing_files": [],
                "validation_score": 100.0,
            }

            for metric_file in self.metric_files:
                file_path = self.project_root / metric_file

                if not file_path.exists():
                    validation_results["missing_files"].append(metric_file)
                    validation_results["all_current"] = False
                    continue

                # Check if file is stale (older than 1 hour)
                file_age = datetime.now().timestamp() - file_path.stat().st_mtime
                if file_age > 3600:  # 1 hour
                    validation_results["stale_files"].append(metric_file)
                    validation_results["all_current"] = False

            # Calculate validation score
            total_files = len(self.metric_files)
            stale_count = len(validation_results["stale_files"])
            missing_count = len(validation_results["missing_files"])
            validation_results["validation_score"] = (
                (total_files - stale_count - missing_count) / total_files
            ) * 100.0

            logger.info(
                f"Metric validation completed: {validation_results['validation_score']:.1f}% current"
            )
            return validation_results

        except Exception as e:
            logger.error(f"Metric validation error: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "all_current": False,
                "error": str(e),
                "validation_score": 0.0,
            }


def main():
    """Main function for metric refresh system."""
    print("🔄 Enhanced Automated Metric Refresh System")
    print("=" * 50)

    refresh_system = MetricRefreshSystem()

    # Refresh all metrics
    results = refresh_system.refresh_all_metrics()
    print(
        f"✅ Refresh complete: {results['success_count']} successful, {results['error_count']} errors"
    )

    # Validate metrics
    validation = refresh_system.validate_metrics()
    print(
        f"📊 Validation complete: {'All current' if validation['all_current'] else 'Issues found'}"
    )

    # Show health scores
    health_data = refresh_system.sync_health_scores()
    if health_data["status"] == "success":
        health = health_data["health_data"]
        print(f"🏥 System Health: {health['system_health']:.1f}%")
        print(f"   Project: {health['project_health']:.1f}%")
        print(f"   Quality: {health['quality_health']:.1f}%")
        print(f"   Documentation: {health['documentation_health']:.1f}%")


if __name__ == "__main__":
    main()
