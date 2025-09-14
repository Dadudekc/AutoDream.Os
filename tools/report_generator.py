"""Report generation components for project scanning."""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ModularReportGenerator:
    """Creates modular, agent-digestible analysis files instead of one massive JSON."""

    def __init__(self, project_root: Path, analysis: dict[str, dict]):
        self.project_root = project_root
        self.analysis = analysis

    def generate_modular_reports(self):
        """Generate multiple smaller, focused analysis files."""
        logger.info("🔄 Generating modular analysis reports...")

        # Create analysis directory
        analysis_dir = self.project_root / "analysis"
        analysis_dir.mkdir(exist_ok=True)

        # Generate different types of analysis
        self._generate_agent_analysis(analysis_dir)
        self._generate_module_analysis(analysis_dir)
        self._generate_file_type_analysis(analysis_dir)
        self._generate_complexity_analysis(analysis_dir)
        self._generate_dependency_analysis(analysis_dir)
        self._generate_architecture_overview(analysis_dir)

        logger.info("✅ Modular analysis reports generated successfully!")

    def _generate_agent_analysis(self, analysis_dir: Path):
        """Generate agent-specific analysis files."""
        agent_analysis = {}

        for file_path, file_data in self.analysis.items():
            if file_path.startswith("agent_workspaces/"):
                # Extract agent ID from path (e.g., "agent_workspaces/Agent-1/status.json" -> "Agent-1")
                parts = file_path.split("/")
                if len(parts) >= 2 and parts[1].startswith("Agent-"):
                    agent_id = parts[1]
                    if agent_id not in agent_analysis:
                        agent_analysis[agent_id] = {
                            "agent_id": agent_id,
                            "files": [],
                            "total_functions": 0,
                            "total_classes": 0,
                            "total_complexity": 0,
                        }
                    agent_analysis[agent_id]["files"].append(
                        {
                            "path": file_path,
                            "functions": len(file_data.get("functions", [])),
                            "classes": len(file_data.get("classes", [])),
                            "complexity": file_data.get("complexity", 0),
                        }
                    )
                    agent_analysis[agent_id]["total_functions"] += len(
                        file_data.get("functions", [])
                    )
                    agent_analysis[agent_id]["total_classes"] += len(file_data.get("classes", []))
                    agent_analysis[agent_id]["total_complexity"] += file_data.get("complexity", 0)

        # Save agent analysis
        output_path = analysis_dir / "agent_analysis.json"
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(agent_analysis, f, indent=2)
        logger.info(f"📊 Agent analysis saved to {output_path}")

    def _generate_module_analysis(self, analysis_dir: Path):
        """Generate module/component-specific analysis."""
        module_analysis = {}

        for file_path, file_data in self.analysis.items():
            # Group by module/component (e.g., "src/core", "src/services", "tools", etc.)
            if "/" in file_path:
                module = file_path.split("/")[0]
                if module not in ["agent_workspaces", "__pycache__"]:
                    if module not in module_analysis:
                        module_analysis[module] = {
                            "module": module,
                            "files": [],
                            "total_functions": 0,
                            "total_classes": 0,
                            "languages": set(),
                            "total_complexity": 0,
                        }

                    module_analysis[module]["files"].append(
                        {
                            "path": file_path,
                            "language": file_data.get("language", "unknown"),
                            "functions": len(file_data.get("functions", [])),
                            "classes": len(file_data.get("classes", [])),
                            "complexity": file_data.get("complexity", 0),
                        }
                    )
                    module_analysis[module]["total_functions"] += len(
                        file_data.get("functions", [])
                    )
                    module_analysis[module]["total_classes"] += len(file_data.get("classes", []))
                    module_analysis[module]["languages"].add(file_data.get("language", "unknown"))
                    module_analysis[module]["total_complexity"] += file_data.get("complexity", 0)

                    # Convert set to list for JSON serialization
                    module_analysis[module]["languages"] = list(
                        module_analysis[module]["languages"]
                    )

        # Save module analysis
        output_path = analysis_dir / "module_analysis.json"
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(module_analysis, f, indent=2)
        logger.info(f"📊 Module analysis saved to {output_path}")

    def _generate_file_type_analysis(self, analysis_dir: Path):
        """Generate analysis grouped by file type."""
        file_type_analysis = {}

        for file_path, file_data in self.analysis.items():
            file_type = file_data.get("language", "unknown")
            if file_type not in file_type_analysis:
                file_type_analysis[file_type] = {
                    "file_type": file_type,
                    "files": [],
                    "total_functions": 0,
                    "total_classes": 0,
                    "total_complexity": 0,
                    "file_count": 0,
                }

            file_type_analysis[file_type]["files"].append(
                {
                    "path": file_path,
                    "functions": len(file_data.get("functions", [])),
                    "classes": len(file_data.get("classes", [])),
                    "complexity": file_data.get("complexity", 0),
                }
            )
            file_type_analysis[file_type]["total_functions"] += len(file_data.get("functions", []))
            file_type_analysis[file_type]["total_classes"] += len(file_data.get("classes", []))
            file_type_analysis[file_type]["total_complexity"] += file_data.get("complexity", 0)
            file_type_analysis[file_type]["file_count"] += 1

        # Save file type analysis
        output_path = analysis_dir / "file_type_analysis.json"
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(file_type_analysis, f, indent=2)
        logger.info(f"📊 File type analysis saved to {output_path}")

    def _generate_complexity_analysis(self, analysis_dir: Path):
        """Generate complexity-focused analysis."""
        complexity_analysis = {
            "complexity_distribution": {},
            "high_complexity_files": [],
            "low_complexity_files": [],
            "average_complexity": 0,
            "total_files": 0,
            "complexity_ranges": {
                "simple": [],  # complexity 1-5
                "moderate": [],  # complexity 6-15
                "complex": [],  # complexity 16-30
                "very_complex": [],  # complexity > 30
            },
        }

        total_complexity = 0
        file_count = 0

        for file_path, file_data in self.analysis.items():
            complexity = file_data.get("complexity", 0)
            total_complexity += complexity
            file_count += 1

            # Categorize by complexity ranges
            if complexity <= 5:
                complexity_analysis["complexity_ranges"]["simple"].append(file_path)
            elif complexity <= 15:
                complexity_analysis["complexity_ranges"]["moderate"].append(file_path)
            elif complexity <= 30:
                complexity_analysis["complexity_ranges"]["complex"].append(file_path)
            else:
                complexity_analysis["complexity_ranges"]["very_complex"].append(file_path)

            # Track high and low complexity files
            if complexity >= 20:
                complexity_analysis["high_complexity_files"].append(
                    {
                        "path": file_path,
                        "complexity": complexity,
                        "functions": len(file_data.get("functions", [])),
                        "classes": len(file_data.get("classes", [])),
                    }
                )
            elif complexity <= 3:
                complexity_analysis["low_complexity_files"].append(
                    {"path": file_path, "complexity": complexity}
                )

        if file_count > 0:
            complexity_analysis["average_complexity"] = total_complexity / file_count
        complexity_analysis["total_files"] = file_count

        # Save complexity analysis
        output_path = analysis_dir / "complexity_analysis.json"
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(complexity_analysis, f, indent=2)
        logger.info(f"📊 Complexity analysis saved to {output_path}")

    def _generate_dependency_analysis(self, analysis_dir: Path):
        """Generate dependency/import analysis."""
        dependency_analysis = {
            "imports_by_module": {},
            "most_imported_modules": {},
            "circular_dependencies": [],
            "external_dependencies": set(),
            "internal_dependencies": {},
        }

        # This is a simplified version - in practice you'd parse actual imports
        # For now, we'll create a structure that can be expanded
        for file_path, file_data in self.analysis.items():
            if file_path.endswith(".py"):
                module_name = file_path.replace("/", ".").replace(".py", "")
                dependency_analysis["internal_dependencies"][module_name] = {
                    "file_path": file_path,
                    "functions": file_data.get("functions", []),
                    "classes": file_data.get("classes", []),
                    "estimated_dependencies": [],  # Would be populated by actual import parsing
                }

        # Convert set to list for JSON
        dependency_analysis["external_dependencies"] = list(
            dependency_analysis["external_dependencies"]
        )

        # Save dependency analysis
        output_path = analysis_dir / "dependency_analysis.json"
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(dependency_analysis, f, indent=2)
        logger.info(f"📊 Dependency analysis saved to {output_path}")

    def _generate_architecture_overview(self, analysis_dir: Path):
        """Generate high-level architecture overview."""
        architecture_overview = {
            "project_structure": {},
            "key_components": [],
            "architecture_patterns": [],
            "code_metrics": {
                "total_files": len(self.analysis),
                "total_functions": 0,
                "total_classes": 0,
                "total_complexity": 0,
                "languages_used": set(),
            },
            "recommendations": [],
        }

        # Calculate metrics
        for file_path, file_data in self.analysis.items():
            architecture_overview["code_metrics"]["total_functions"] += len(
                file_data.get("functions", [])
            )
            architecture_overview["code_metrics"]["total_classes"] += len(
                file_data.get("classes", [])
            )
            architecture_overview["code_metrics"]["total_complexity"] += file_data.get(
                "complexity", 0
            )
            architecture_overview["code_metrics"]["languages_used"].add(
                file_data.get("language", "unknown")
            )

        # Convert set to list
        architecture_overview["code_metrics"]["languages_used"] = list(
            architecture_overview["code_metrics"]["languages_used"]
        )

        # Generate structure overview
        for file_path in self.analysis.keys():
            parts = file_path.split("/")
            if len(parts) > 1:
                top_level = parts[0]
                if top_level not in architecture_overview["project_structure"]:
                    architecture_overview["project_structure"][top_level] = []
                architecture_overview["project_structure"][top_level].append(file_path)

        # Save architecture overview
        output_path = analysis_dir / "architecture_overview.json"
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(architecture_overview, f, indent=2)
        logger.info(f"📊 Architecture overview saved to {output_path}")


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
        from collections import defaultdict

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
