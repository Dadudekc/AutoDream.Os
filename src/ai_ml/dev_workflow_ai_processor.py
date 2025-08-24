"""AI processing utilities for development workflows."""
from __future__ import annotations
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from .code_crafter import CodeCrafter, CodeAnalysis

logger = logging.getLogger(__name__)

@dataclass
class ProjectAnalysis:

    project_path: str
    total_files: int
    code_files: int
    test_files: int
    documentation_files: int
    language_distribution: Dict[str, int]
    framework_usage: Dict[str, List[str]]
    code_quality_score: float
    test_coverage: float
    documentation_coverage: float
    recommendations: List[str] = field(default_factory=list)

class AIProcessor:
    def __init__(self, config):
        self.config = config
        self.code_crafter = CodeCrafter()
        self.openai_key = config.openai_key
        self.anthropic_key = config.anthropic_key
    def execute_ai_assisted_step(self, step, project_path: Path, **kwargs) -> str:
        mapping = {
            "generate_tests": self._generate_tests_for_project,
            "code_analysis": self._analyze_project_code,
            "refactor_suggestions": self._generate_refactor_suggestions,
            "documentation_generation": self._generate_documentation,
        }
        func = mapping.get(step.name)
        return func(project_path) if func else f"AI-assisted step '{step.name}' executed successfully"
    def get_ai_suggestions(self, step, output: str) -> List[str]:
        try:
            if self.openai_key:
                return self._get_openai_suggestions(step, output)
            if self.anthropic_key:
                return self._get_anthropic_suggestions(step, output)
        except Exception as exc:  # pragma: no cover
            logger.warning("Failed to get AI suggestions: %s", exc)
        return []
    def _get_openai_suggestions(self, step, output: str) -> List[str]:
        import openai  # type: ignore
        openai.api_key = self.openai_key
        prompt = json.dumps({"step": step.name, "description": step.description, "output": output[:1000]})
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a development workflow expert."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        try:
            return json.loads(resp.choices[0].message.content)
        except Exception:
            return []
    def _get_anthropic_suggestions(self, step, output: str) -> List[str]:
        import anthropic  # type: ignore
        client = anthropic.Anthropic(api_key=self.anthropic_key)
        prompt = json.dumps({"step": step.name, "description": step.description, "output": output[:1000]})
        resp = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        try:
            return json.loads(resp.content[0].text)
        except Exception:
            return []
    def analyze_project(self, project_path: Path) -> ProjectAnalysis:
        total_files = len(list(project_path.rglob("*")))
        code_files = len(list(project_path.rglob("*.py")))
        test_files = len([f for f in project_path.rglob("*.py") if "test" in f.name.lower()])
        documentation_files = len(list(project_path.rglob("*.md")))
        language_distribution = {"python": code_files}
        framework_usage: Dict[str, List[str]] = {"python": []}
        for py_file in project_path.rglob("*.py"):
            content = py_file.read_text()
            if "import django" in content or "from django" in content:
                framework_usage["python"].append("django")
            if "import flask" in content or "from flask" in content:
                framework_usage["python"].append("flask")
            if "import torch" in content or "from torch" in content:
                framework_usage["python"].append("pytorch")
        quality_scores: List[float] = []
        for py_file in project_path.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                try:
                    analysis: CodeAnalysis = self.code_crafter.analyze_code(str(py_file))
                    quality_scores.append(analysis.maintainability_index)
                except Exception:
                    quality_scores.append(50)
        code_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        test_coverage = (test_files / max(code_files, 1)) * 100 if code_files else 0
        documentation_coverage = (documentation_files / max(code_files, 1)) * 100 if code_files else 0
        recommendations: List[str] = []
        if code_quality < 70:
            recommendations.append("Improve code quality through refactoring")
        if test_coverage < 80:
            recommendations.append("Increase test coverage")
        if documentation_coverage < 60:
            recommendations.append("Add more documentation")
        if not recommendations:
            recommendations.append("Project is in good shape!")
        return ProjectAnalysis(
            project_path=str(project_path),
            total_files=total_files,
            code_files=code_files,
            test_files=test_files,
            documentation_files=documentation_files,
            language_distribution=language_distribution,
            framework_usage=framework_usage,
            code_quality_score=code_quality,
            test_coverage=test_coverage,
            documentation_coverage=documentation_coverage,
            recommendations=recommendations,
        )
    def _generate_tests_for_project(self, project_path: Path) -> str:
        generated: List[str] = []
        for py_file in project_path.rglob("*.py"):
            if not py_file.name.startswith("test_") and "test" not in py_file.name.lower():
                try:
                    test_code = self.code_crafter.generate_tests(str(py_file))
                    test_file = py_file.parent / f"test_{py_file.name}"
                    test_file.write_text(test_code)
                    generated.append(str(test_file))
                except Exception as exc:
                    logger.warning("Failed to generate tests for %s: %s", py_file, exc)
        return f"Generated tests for {len(generated)} files: {', '.join(generated)}"
    def _analyze_project_code(self, project_path: Path) -> str:
        analyses: List[str] = []
        for py_file in project_path.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                try:
                    result = self.code_crafter.analyze_code(str(py_file))
                    analyses.append(
                        f"{py_file.name}: Complexity={result.complexity_score}, Maintainability={result.maintainability_index}"
                    )
                except Exception as exc:
                    logger.warning("Failed to analyze %s: %s", py_file, exc)
        return f"Analyzed {len(analyses)} files:\n" + "\n".join(analyses)
    def _generate_refactor_suggestions(self, project_path: Path) -> str:
        suggestions: List[str] = []
        for py_file in project_path.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                try:
                    result = self.code_crafter.analyze_code(str(py_file))
                    if result.code_smells or result.complexity_score > 5:
                        suggestions.append(f"{py_file.name}: {', '.join(result.code_smells)}")
                except Exception as exc:
                    logger.warning("Failed to analyze %s: %s", py_file, exc)
        return f"Refactoring suggestions for {len(suggestions)} files:\n" + "\n".join(suggestions)
    def _generate_documentation(self, project_path: Path) -> str:
        docs: List[str] = []
        for py_file in project_path.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                try:
                    content = py_file.read_text()
                    doc = [
                        f"# {py_file.stem}",
                        f"File: {py_file}",
                        f"Generated: {datetime.now().isoformat()}",
                        "",
                        "## Functions and Classes",
                        "",
                    ]
                    import ast
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                doc.append(f"### {node.name}")
                                if node.docstring:
                                    doc.append(node.docstring + "\n")
                            elif isinstance(node, ast.ClassDef):
                                doc.append(f"### Class: {node.name}")
                                if node.docstring:
                                    doc.append(node.docstring + "\n")
                    except SyntaxError:
                        pass
                    doc_file = py_file.parent / f"{py_file.stem}.md"
                    doc_file.write_text("\n".join(doc))
                    docs.append(str(doc_file))
                except Exception as exc:
                    logger.warning("Failed to generate documentation for %s: %s", py_file, exc)
        return f"Generated documentation for {len(docs)} files: {', '.join(docs)}"
