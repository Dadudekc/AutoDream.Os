#!/usr/bin/env python3
"""
Project Scanner - Legacy Report Generator
=========================================

Handles merging new analysis into existing project_analysis.json and ChatGPT context.

V2 Compliance: Extracted from projectscanner.py (1,153 lines → modular)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-10-11
License: MIT
"""

import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Handles merging new analysis into existing project_analysis.json and chatgpt context."""

    def __init__(self, project_root: Path, analysis: dict[str, dict]):
        self.project_root = project_root
        self.analysis = analysis  # e.g. { 'subdir/file.py': {language:..., classes:...}, ... }

    def load_existing_report(self, report_path: Path) -> dict[str, Any]:
        """Loads any existing project_analysis.json to preserve old entries."""
        if report_path.exists():
            try:
                with report_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading existing report {report_path}: {e}")
        return {}

    def save_report(self):
        """
        Merge new analysis results into old project_analysis.json, then write it out.
        Old data is kept; new files are added or updated.
        Separates test files into their own JSON file.
        """
        report_path = self.project_root / "project_analysis.json"
        test_report_path = self.project_root / "test_analysis.json"
        existing = self.load_existing_report(report_path)
        existing_tests = self.load_existing_report(test_report_path)

        # Split analysis into test and non-test files
        test_files = {}
        non_test_files = {}

        for file_path, analysis in self.analysis.items():
            if "test" in file_path.lower() or "tests" in file_path.lower():
                test_files[file_path] = analysis
            else:
                non_test_files[file_path] = analysis

        # Merge logic: new data overrides old entries with the same filename,
        # but preserves any old entries for files not in the current scan.
        merged = {**existing, **non_test_files}
        merged_tests = {**existing_tests, **test_files}

        # Save main analysis
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(merged, f, indent=4)
        logger.info(f"✅ Project analysis updated and saved to {report_path}")

        # Save test analysis
        with test_report_path.open("w", encoding="utf-8") as f:
            json.dump(merged_tests, f, indent=4)
        logger.info(f"✅ Test analysis saved to {test_report_path}")

    def generate_init_files(self, overwrite: bool = True):
        """Auto-generate __init__.py for all Python packages based on self.analysis."""
        package_modules = defaultdict(list)
        for rel_path in self.analysis.keys():
            if rel_path.endswith(".py"):
                file_path = Path(rel_path)
                if file_path.name == "__init__.py":
                    continue
                package_dir = file_path.parent
                module_name = file_path.stem
                package_modules[str(package_dir)].append(module_name)

        for package, modules in package_modules.items():
            package_path = self.project_root / package
            init_file = package_path / "__init__.py"
            package_path.mkdir(parents=True, exist_ok=True)

            lines = [
                "# AUTO-GENERATED __init__.py",
                "# DO NOT EDIT MANUALLY - changes may be overwritten\n",
            ]
            for module in sorted(modules):
                lines.append(f"from . import {module}")
            lines.append("\n__all__ = [")
            for module in sorted(modules):
                lines.append(f"    '{module}',")
            lines.append("]\n")
            content = "\n".join(lines)

            if overwrite or not init_file.exists():
                with init_file.open("w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"✅ Generated __init__.py in {package_path}")
            else:
                logger.info(f"ℹ️ Skipped {init_file} (already exists)")

    def load_existing_chatgpt_context(self, context_path: Path) -> dict[str, Any]:
        """Load any existing chatgpt_project_context.json."""
        if context_path.exists():
            try:
                with context_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading existing ChatGPT context: {e}")
        return {}

    def export_chatgpt_context(
        self, template_path: str | None = None, output_path: str | None = None
    ):
        """
        Merges current analysis details with old chatgpt_project_context.json.
        Again, old keys remain unless overridden by new data.
        If no template, write JSON. Else use Jinja to render a custom format.
        """
        if not output_path:
            context_path = self.project_root / "chatgpt_project_context.json"
        else:
            context_path = Path(output_path)
        context_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"💾 Writing ChatGPT context to: {context_path}")

        # If no template, do direct JSON merging
        if not template_path:
            existing_context = self.load_existing_chatgpt_context(context_path)
            payload = {
                "project_root": str(self.project_root),
                "num_files_analyzed": len(self.analysis),
                "analysis_details": self.analysis,
            }
            # New data overrides same keys, but preserves everything else.
            merged_context = {**existing_context, **payload}
            try:
                with context_path.open("w", encoding="utf-8") as f:
                    json.dump(merged_context, f, indent=4)
                logger.info(f"✅ Merged ChatGPT context saved to: {context_path}")
            except Exception as e:
                logger.error(f"❌ Error writing ChatGPT context: {e}")
            return

        # If we do have a template, we can still load old data, but we'll not attempt JSON merging.
        # We'll just produce a final rendered template containing the new analysis.
        try:
            from jinja2 import Template

            with open(template_path, encoding="utf-8") as tf:
                template_content = tf.read()
            t = Template(template_content)

            # Could load existing context if you want. We'll skip that for Jinja scenario.
            context_dict = {
                "project_root": str(self.project_root),
                "analysis": self.analysis,
                "num_files_analyzed": len(self.analysis),
            }
            rendered = t.render(context=context_dict)
            with context_path.open("w", encoding="utf-8") as outf:
                outf.write(rendered)
            logger.info(f"✅ Rendered ChatGPT context to: {output_path}")
        except ImportError:
            logger.error("⚠️ Jinja2 not installed. Run `pip install jinja2` and re-try.")
        except Exception as e:
            logger.error(f"❌ Error rendering Jinja template: {e}")
