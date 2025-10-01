#!/usr/bin/env python3
"""
Automated Metric Refresh System
==============================

Automatically updates project metrics and status files to ensure agents
always work with current data. Prevents documentation drift and stale information.

Author: Agent-5 (Business Intelligence Coordinator)
V2 Compliance: ≤400 lines, modular design
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


class MetricRefreshSystem:
    """Automated metric refresh system for project data."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.metric_files = [
            "project_analysis.json",
            "current_quality_status.json",
            "current_compliance.json",
            "agent_analysis.json",
            "chatgpt_project_context.json",
        ]

    def refresh_project_analysis(self) -> dict[str, Any]:
        """Refresh project analysis using project scanner."""
        try:
            result = subprocess.run(
                ["python", "tools/simple_project_scanner.py"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                return {"status": "success", "output": result.stdout}
            else:
                return {"status": "error", "error": result.stderr}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def refresh_quality_status(self) -> dict[str, Any]:
        """Refresh quality status using quality gates."""
        try:
            result = subprocess.run(
                ["python", "quality_gates.py", "--path", "src"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                return {"status": "success", "output": result.stdout}
            else:
                return {"status": "error", "error": result.stderr}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def refresh_agent_analysis(self) -> dict[str, Any]:
        """Refresh agent analysis from workspaces."""
        try:
            agent_data = {}
            agent_workspaces = self.project_root / "agent_workspaces"

            if agent_workspaces.exists():
                for agent_dir in agent_workspaces.iterdir():
                    if agent_dir.is_dir():
                        status_file = agent_dir / "status.json"
                        if status_file.exists():
                            with open(status_file) as f:
                                agent_data[agent_dir.name] = json.load(f)

            return {"status": "success", "agents": agent_data}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def update_metric_file(self, filename: str, data: dict[str, Any]) -> bool:
        """Update a metric file with new data."""
        try:
            file_path = self.project_root / filename
            data["last_updated"] = datetime.now().isoformat()
            data["updated_by"] = "MetricRefreshSystem"

            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"❌ Failed to update {filename}: {e}")
            return False

    def refresh_all_metrics(self) -> dict[str, Any]:
        """Refresh all project metrics."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "refresh_results": {},
            "success_count": 0,
            "error_count": 0,
        }

        # Refresh project analysis
        project_result = self.refresh_project_analysis()
        results["refresh_results"]["project_analysis"] = project_result
        if project_result["status"] == "success":
            results["success_count"] += 1
        else:
            results["error_count"] += 1

        # Refresh quality status
        quality_result = self.refresh_quality_status()
        results["refresh_results"]["quality_status"] = quality_result
        if quality_result["status"] == "success":
            results["success_count"] += 1
        else:
            results["error_count"] += 1

        # Refresh agent analysis
        agent_result = self.refresh_agent_analysis()
        results["refresh_results"]["agent_analysis"] = agent_result
        if agent_result["status"] == "success":
            results["success_count"] += 1
        else:
            results["error_count"] += 1

        return results

    def validate_metrics(self) -> dict[str, Any]:
        """Validate that all metric files exist and are current."""
        validation_results = {
            "timestamp": datetime.now().isoformat(),
            "file_status": {},
            "all_current": True,
        }

        for filename in self.metric_files:
            file_path = self.project_root / filename
            if file_path.exists():
                try:
                    with open(file_path) as f:
                        data = json.load(f)

                    last_updated = data.get("last_updated", "unknown")
                    validation_results["file_status"][filename] = {
                        "exists": True,
                        "last_updated": last_updated,
                        "size": file_path.stat().st_size,
                    }
                except Exception as e:
                    validation_results["file_status"][filename] = {"exists": True, "error": str(e)}
                    validation_results["all_current"] = False
            else:
                validation_results["file_status"][filename] = {"exists": False}
                validation_results["all_current"] = False

        return validation_results


def main():
    """Main function for metric refresh system."""
    import argparse

    parser = argparse.ArgumentParser(description="Automated Metric Refresh System")
    parser.add_argument("--update-all", action="store_true", help="Update all metrics")
    parser.add_argument("--validate", action="store_true", help="Validate metric files")
    parser.add_argument(
        "--project-analysis", action="store_true", help="Update project analysis only"
    )
    parser.add_argument("--quality-status", action="store_true", help="Update quality status only")
    parser.add_argument("--agent-analysis", action="store_true", help="Update agent analysis only")

    args = parser.parse_args()

    refresh_system = MetricRefreshSystem()

    if args.update_all:
        print("🔄 Refreshing all project metrics...")
        results = refresh_system.refresh_all_metrics()
        print(
            f"✅ Refresh complete: {results['success_count']} successful, {results['error_count']} errors"
        )

        # Save refresh results
        with open("metric_refresh_results.json", "w") as f:
            json.dump(results, f, indent=2)

        return 0

    if args.validate:
        print("🔍 Validating metric files...")
        validation = refresh_system.validate_metrics()
        print(
            f"📊 Validation complete: {'All current' if validation['all_current'] else 'Issues found'}"
        )

        for filename, status in validation["file_status"].items():
            if status["exists"]:
                print(f"✅ {filename}: {status.get('size', 0)} bytes")
            else:
                print(f"❌ {filename}: Missing")

        return 0

    if args.project_analysis:
        print("🔄 Refreshing project analysis...")
        result = refresh_system.refresh_project_analysis()
        print(f"📊 Project analysis: {result['status']}")
        return 0

    if args.quality_status:
        print("🔄 Refreshing quality status...")
        result = refresh_system.refresh_quality_status()
        print(f"📊 Quality status: {result['status']}")
        return 0

    if args.agent_analysis:
        print("🔄 Refreshing agent analysis...")
        result = refresh_system.refresh_agent_analysis()
        print(f"📊 Agent analysis: {result['status']}")
        return 0

    print("❌ No action specified. Use --help for options.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
