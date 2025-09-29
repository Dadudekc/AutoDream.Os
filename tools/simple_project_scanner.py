#!/usr/bin/env python3
"""
Simple Project Scanner
======================

A simplified version of the project scanner that works without complex dependencies.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SimpleProjectScanner:
    """Simple project scanner for basic project analysis."""

    def __init__(self, project_root: str = "."):
        """Initialize project scanner with project root."""
        self.project_root = Path(project_root).resolve()
        self.analysis_data: dict[str, Any] = {}

    def scan_project(self) -> dict[str, Any]:
        """Perform comprehensive project scan."""
        logger.info("🔍 Starting project scan...")

        # Basic project structure analysis
        self._analyze_project_structure()
        self._analyze_python_files()
        self._analyze_dependencies()

        logger.info("✅ Project scan completed")
        return self.analysis_data

    def _analyze_project_structure(self) -> None:
        """Analyze basic project structure."""
        structure = {"total_files": 0, "python_files": 0, "directories": [], "file_types": {}}

        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]

            for file in files:
                if not file.startswith("."):
                    structure["total_files"] += 1

                    # Count file types
                    ext = Path(file).suffix.lower()
                    if ext:
                        structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1

                    # Count Python files
                    if ext == ".py":
                        structure["python_files"] += 1

            # Add directories
            for dir_name in dirs:
                if not dir_name.startswith("."):
                    structure["directories"].append(str(Path(root) / dir_name))

        self.analysis_data["project_structure"] = structure

    def _analyze_python_files(self) -> None:
        """Analyze Python files for V2 compliance."""
        python_analysis = {
            "total_python_files": 0,
            "v2_compliant_files": 0,
            "non_compliant_files": [],
            "large_files": [],
            "average_lines": 0,
        }

        total_lines = 0
        python_files = []

        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]

            for file in files:
                if file.endswith(".py") and not file.startswith("."):
                    file_path = Path(root) / file
                    python_files.append(file_path)

                    try:
                        with open(file_path, encoding="utf-8") as f:
                            lines = len(f.readlines())
                            total_lines += lines

                            python_analysis["total_python_files"] += 1

                            if lines <= 400:
                                python_analysis["v2_compliant_files"] += 1
                            else:
                                python_analysis["non_compliant_files"].append(
                                    {"file": str(file_path), "lines": lines}
                                )

                            if lines > 600:
                                python_analysis["large_files"].append(
                                    {"file": str(file_path), "lines": lines}
                                )
                    except Exception as e:
                        logger.warning(f"Could not analyze {file_path}: {e}")

        if python_analysis["total_python_files"] > 0:
            python_analysis["average_lines"] = total_lines / python_analysis["total_python_files"]

        self.analysis_data["python_analysis"] = python_analysis

    def _analyze_dependencies(self) -> None:
        """Analyze project dependencies."""
        dependencies = {
            "requirements_files": [],
            "python_version": "Unknown",
            "key_dependencies": [],
        }

        # Check for requirements files
        req_files = ["requirements.txt", "requirements-test.txt", "requirements-testing.txt"]
        for req_file in req_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                dependencies["requirements_files"].append(req_file)

        # Try to get Python version
        try:
            import sys

            dependencies[
                "python_version"
            ] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        except:
            pass

        # Check for key dependencies
        key_deps = ["discord.py", "pyautogui", "pydantic", "yaml"]
        for dep in key_deps:
            try:
                if dep == "yaml":
                    import yaml
                elif dep == "discord.py":
                    import discord
                elif dep == "pyautogui":
                    import pyautogui
                elif dep == "pydantic":
                    import pydantic
                dependencies["key_dependencies"].append(dep)
            except ImportError:
                pass

        self.analysis_data["dependencies"] = dependencies

    def save_report(self, output_file: str = "project_analysis.json") -> None:
        """Save analysis report to file."""
        report_data = {
            "project_info": {
                "name": "Agent Cellphone V2",
                "version": "2.1.0",
                "description": "Advanced AI Agent System with Code Quality Standards",
                "scan_timestamp": datetime.now().isoformat(),
                "scanner_version": "SimpleProjectScanner 1.0.0",
            },
            "analysis": self.analysis_data,
        }

        output_path = self.project_root / output_file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"📊 Project analysis report saved to: {output_path}")


def main():
    """Main function to run the project scanner."""
    import argparse

    parser = argparse.ArgumentParser(description="Simple Project Scanner")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--output", default="project_analysis.json", help="Output file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    scanner = SimpleProjectScanner(args.project_root)
    analysis = scanner.scan_project()
    scanner.save_report(args.output)

    print("🎉 Project scan completed!")
    print(f"📁 Total files: {analysis['project_structure']['total_files']}")
    print(f"🐍 Python files: {analysis['python_analysis']['total_python_files']}")
    print(f"✅ V2 compliant: {analysis['python_analysis']['v2_compliant_files']}")
    print(f"❌ Non-compliant: {len(analysis['python_analysis']['non_compliant_files'])}")


if __name__ == "__main__":
    main()
