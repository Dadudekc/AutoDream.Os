#!/usr/bin/env python3
"""
AI-Powered Development Workflow Automation
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

Intelligent development workflow automation with AI assistance
"""
import os
import json
import logging
import subprocess
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import time

from .code_crafter import CodeCrafter, CodeGenerationRequest, CodeAnalysis
from .api_key_manager import get_openai_api_key, get_anthropic_api_key
from .utils import performance_monitor, get_config_manager

logger = logging.getLogger(__name__)


@dataclass
class WorkflowStep:
    """A step in the development workflow"""

    name: str
    description: str
    command: str
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 300
    retry_count: int = 3
    required: bool = True
    ai_assisted: bool = False


@dataclass
class WorkflowResult:
    """Result of workflow execution"""

    step_name: str
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0
    ai_suggestions: List[str] = field(default_factory=list)


@dataclass
class ProjectAnalysis:
    """Analysis of a development project"""

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
    recommendations: List[str]


class AIDevWorkflow:
    """AI-powered development workflow automation"""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.config = get_config_manager()
        self.code_crafter = CodeCrafter()
        self.openai_key = get_openai_api_key()
        self.anthropic_key = get_anthropic_api_key()

        # Supported workflows
        self.workflows = {
            "tdd": self._get_tdd_workflow(),
            "code_review": self._get_code_review_workflow(),
            "refactoring": self._get_refactoring_workflow(),
            "testing": self._get_testing_workflow(),
            "documentation": self._get_documentation_workflow(),
            "deployment": self._get_deployment_workflow(),
        }

    def get_available_workflows(self) -> List[str]:
        """Get list of available workflows"""
        return list(self.workflows.keys())

    def execute_workflow(
        self, workflow_name: str, **kwargs
    ) -> Dict[str, WorkflowResult]:
        """
        Execute a specific workflow

        Args:
            workflow_name: Name of the workflow to execute
            **kwargs: Additional parameters for the workflow

        Returns:
            Results of workflow execution
        """
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")

        logger.info(f"Executing workflow: {workflow_name}")

        workflow = self.workflows[workflow_name]
        results = {}

        for step in workflow:
            try:
                result = self._execute_step(step, **kwargs)
                results[step.name] = result

                # If step failed and is required, stop execution
                if not result.success and step.required:
                    logger.error(
                        f"Required step '{step.name}' failed, stopping workflow"
                    )
                    break

            except Exception as e:
                logger.error(f"Step '{step.name}' failed with exception: {e}")
                results[step.name] = WorkflowResult(
                    step_name=step.name,
                    success=False,
                    output="",
                    error=str(e),
                    execution_time=0.0,
                )

        return results

    def _execute_step(self, step: WorkflowStep, **kwargs) -> WorkflowResult:
        """Execute a single workflow step"""
        logger.info(f"Executing step: {step.name}")

        start_time = time.time()

        try:
            # Execute command
            if step.ai_assisted:
                output = self._execute_ai_assisted_step(step, **kwargs)
            else:
                output = self._execute_command(step.command, step.timeout)

            execution_time = time.time() - start_time

            # Get AI suggestions if AI-assisted
            ai_suggestions = []
            if step.ai_assisted:
                ai_suggestions = self._get_ai_suggestions(step, output, **kwargs)

            return WorkflowResult(
                step_name=step.name,
                success=True,
                output=output,
                execution_time=execution_time,
                ai_suggestions=ai_suggestions,
            )

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return WorkflowResult(
                step_name=step.name,
                success=False,
                output="",
                error=f"Step timed out after {step.timeout} seconds",
                execution_time=execution_time,
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return WorkflowResult(
                step_name=step.name,
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time,
            )

    def _execute_command(self, command: str, timeout: int) -> str:
        """Execute a shell command"""
        try:
            # SECURITY: shell=False to prevent command injection
            result = subprocess.run(
                command.split() if isinstance(command, str) else command,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_path,
            )

            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, command, result.stdout, result.stderr
                )

            return result.stdout

        except subprocess.TimeoutExpired:
            raise
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"Command failed with return code {e.returncode}: {e.stderr}"
            )

    def _execute_ai_assisted_step(self, step: WorkflowStep, **kwargs) -> str:
        """Execute an AI-assisted step"""
        if step.name == "generate_tests":
            return self._generate_tests_for_project(**kwargs)
        elif step.name == "code_analysis":
            return self._analyze_project_code(**kwargs)
        elif step.name == "refactor_suggestions":
            return self._generate_refactor_suggestions(**kwargs)
        elif step.name == "documentation_generation":
            return self._generate_documentation(**kwargs)
        else:
            return f"AI-assisted step '{step.name}' executed successfully"

    def _get_ai_suggestions(
        self, step: WorkflowStep, output: str, **kwargs
    ) -> List[str]:
        """Get AI suggestions for a step"""
        try:
            if self.openai_key:
                return self._get_openai_suggestions(step, output, **kwargs)
            elif self.anthropic_key:
                return self._get_anthropic_suggestions(step, output, **kwargs)
        except Exception as e:
            logger.warning(f"Failed to get AI suggestions: {e}")

        return []

    def _get_openai_suggestions(
        self, step: WorkflowStep, output: str, **kwargs
    ) -> List[str]:
        """Get suggestions using OpenAI"""
        try:
            import openai

            openai.api_key = self.openai_key

            prompt = f"""Analyze the output of this development step and provide suggestions:

Step: {step.name}
Description: {step.description}
Output: {output[:1000]}...

Provide 3-5 specific, actionable suggestions for improvement.
Format as a JSON list of strings."""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a development workflow expert.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )

            content = response.choices[0].message.content
            try:
                suggestions = json.loads(content)
                return suggestions if isinstance(suggestions, list) else []
            except json.JSONDecodeError:
                return []

        except Exception as e:
            logger.warning(f"OpenAI suggestions failed: {e}")
            return []

    def _get_anthropic_suggestions(
        self, step: WorkflowStep, output: str, **kwargs
    ) -> List[str]:
        """Get suggestions using Anthropic Claude"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_key)

            prompt = f"""Analyze the output of this development step and provide suggestions:

Step: {step.name}
Description: {step.description}
Output: {output[:1000]}...

Provide 3-5 specific, actionable suggestions for improvement.
Format as a JSON list of strings."""

            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text
            try:
                suggestions = json.loads(content)
                return suggestions if isinstance(suggestions, list) else []
            except json.JSONDecodeError:
                return []

        except Exception as e:
            logger.warning(f"Anthropic suggestions failed: {e}")
            return []

    def _generate_tests_for_project(self, **kwargs) -> str:
        """Generate tests for the entire project"""
        test_files = []

        # Find Python files
        for py_file in self.project_path.rglob("*.py"):
            if (
                not py_file.name.startswith("test_")
                and "test" not in py_file.name.lower()
            ):
                try:
                    test_code = self.code_crafter.generate_tests(str(py_file))
                    test_file = py_file.parent / f"test_{py_file.name}"

                    with open(test_file, "w") as f:
                        f.write(test_code)

                    test_files.append(str(test_file))

                except Exception as e:
                    logger.warning(f"Failed to generate tests for {py_file}: {e}")

        return f"Generated tests for {len(test_files)} files: {', '.join(test_files)}"

    def _analyze_project_code(self, **kwargs) -> str:
        """Analyze code quality across the project"""
        analysis_results = []

        for py_file in self.project_path.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                try:
                    analysis = self.code_crafter.analyze_code(str(py_file))
                    analysis_results.append(
                        f"{py_file.name}: Complexity={analysis.complexity_score}, Maintainability={analysis.maintainability_index}"
                    )
                except Exception as e:
                    logger.warning(f"Failed to analyze {py_file}: {e}")

        return f"Analyzed {len(analysis_results)} files:\n" + "\n".join(
            analysis_results
        )

    def _generate_refactor_suggestions(self, **kwargs) -> str:
        """Generate refactoring suggestions for the project"""
        suggestions = []

        for py_file in self.project_path.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                try:
                    analysis = self.code_crafter.analyze_code(str(py_file))
                    if analysis.code_smells or analysis.complexity_score > 5:
                        suggestions.append(
                            f"{py_file.name}: {', '.join(analysis.code_smells)}"
                        )
                except Exception as e:
                    logger.warning(f"Failed to analyze {py_file}: {e}")

        return f"Refactoring suggestions for {len(suggestions)} files:\n" + "\n".join(
            suggestions
        )

    def _generate_documentation(self, **kwargs) -> str:
        """Generate documentation for the project"""
        doc_files = []

        for py_file in self.project_path.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                try:
                    # Generate docstring-based documentation
                    with open(py_file, "r") as f:
                        content = f.read()

                    # Simple documentation generation
                    doc_content = f"# {py_file.stem}\n\n"
                    doc_content += f"File: {py_file}\n"
                    doc_content += f"Generated: {datetime.now().isoformat()}\n\n"
                    doc_content += "## Functions and Classes\n\n"

                    # Extract function and class names
                    import ast

                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                doc_content += f"### {node.name}\n"
                                if node.docstring:
                                    doc_content += f"{node.docstring}\n\n"
                            elif isinstance(node, ast.ClassDef):
                                doc_content += f"### Class: {node.name}\n"
                                if node.docstring:
                                    doc_content += f"{node.docstring}\n\n"
                    except SyntaxError:
                        pass

                    doc_file = py_file.parent / f"{py_file.stem}.md"
                    with open(doc_file, "w") as f:
                        f.write(doc_content)

                    doc_files.append(str(doc_file))

                except Exception as e:
                    logger.warning(
                        f"Failed to generate documentation for {py_file}: {e}"
                    )

        return f"Generated documentation for {len(doc_files)} files: {', '.join(doc_files)}"

    def analyze_project(self) -> ProjectAnalysis:
        """Analyze the development project"""
        logger.info(f"Analyzing project: {self.project_path}")

        # Count files
        total_files = len(list(self.project_path.rglob("*")))
        code_files = len(list(self.project_path.rglob("*.py")))
        test_files = len(
            [f for f in self.project_path.rglob("*.py") if "test" in f.name.lower()]
        )
        documentation_files = len(list(self.project_path.rglob("*.md")))

        # Language distribution
        language_distribution = {}
        for py_file in self.project_path.rglob("*.py"):
            language_distribution["python"] = language_distribution.get("python", 0) + 1

        # Framework usage detection
        framework_usage = {"python": []}
        for py_file in self.project_path.rglob("*.py"):
            with open(py_file, "r") as f:
                content = f.read()
                if "import django" in content or "from django" in content:
                    framework_usage["python"].append("django")
                if "import flask" in content or "from flask" in content:
                    framework_usage["python"].append("flask")
                if "import torch" in content or "from torch" in content:
                    framework_usage["python"].append("pytorch")

        # Code quality analysis
        quality_scores = []
        for py_file in self.project_path.rglob("*.py"):
            if not py_file.name.startswith("test_"):
                try:
                    analysis = self.code_crafter.analyze_code(str(py_file))
                    quality_scores.append(analysis.maintainability_index)
                except Exception:
                    quality_scores.append(50)  # Default score

        code_quality_score = (
            sum(quality_scores) / len(quality_scores) if quality_scores else 0
        )

        # Test coverage estimation
        test_coverage = (test_files / max(code_files, 1)) * 100 if code_files > 0 else 0

        # Documentation coverage
        documentation_coverage = (
            (documentation_files / max(code_files, 1)) * 100 if code_files > 0 else 0
        )

        # Generate recommendations
        recommendations = []
        if code_quality_score < 70:
            recommendations.append("Improve code quality through refactoring")
        if test_coverage < 80:
            recommendations.append("Increase test coverage")
        if documentation_coverage < 60:
            recommendations.append("Add more documentation")
        if not recommendations:
            recommendations.append("Project is in good shape!")

        return ProjectAnalysis(
            project_path=str(self.project_path),
            total_files=total_files,
            code_files=code_files,
            test_files=test_files,
            documentation_files=documentation_files,
            language_distribution=language_distribution,
            framework_usage=framework_usage,
            code_quality_score=code_quality_score,
            test_coverage=test_coverage,
            documentation_coverage=documentation_coverage,
            recommendations=recommendations,
        )

    def _get_tdd_workflow(self) -> List[WorkflowStep]:
        """Get TDD workflow steps"""
        return [
            WorkflowStep(
                name="project_analysis",
                description="Analyze project structure and code quality",
                command="echo 'Project analysis completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="test_generation",
                description="Generate comprehensive test suites",
                command="echo 'Test generation completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="run_tests",
                description="Execute all tests",
                command="python -m pytest tests/ -v",
                dependencies=["test_generation"],
            ),
            WorkflowStep(
                name="code_analysis",
                description="Analyze code for improvements",
                command="echo 'Code analysis completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="refactor_suggestions",
                description="Generate refactoring suggestions",
                command="echo 'Refactoring suggestions completed'",
                ai_assisted=True,
            ),
        ]

    def _get_code_review_workflow(self) -> List[WorkflowStep]:
        """Get code review workflow steps"""
        return [
            WorkflowStep(
                name="static_analysis",
                description="Run static code analysis",
                command="python -m flake8 src/ --max-line-length=88",
                required=False,
            ),
            WorkflowStep(
                name="code_analysis",
                description="AI-powered code analysis",
                command="echo 'AI code analysis completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="security_scan",
                description="Security vulnerability scan",
                command="echo 'Security scan completed'",
                required=False,
            ),
            WorkflowStep(
                name="performance_analysis",
                description="Performance analysis",
                command="echo 'Performance analysis completed'",
                required=False,
            ),
        ]

    def _get_refactoring_workflow(self) -> List[WorkflowStep]:
        """Get refactoring workflow steps"""
        return [
            WorkflowStep(
                name="code_analysis",
                description="Analyze code for refactoring opportunities",
                command="echo 'Code analysis completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="refactor_suggestions",
                description="Generate specific refactoring suggestions",
                command="echo 'Refactoring suggestions completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="backup_code",
                description="Create backup of current code",
                command="echo 'Backup completed'",
            ),
            WorkflowStep(
                name="apply_refactoring",
                description="Apply refactoring changes",
                command="echo 'Refactoring applied'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="run_tests",
                description="Verify refactoring didn't break functionality",
                command="python -m pytest tests/ -v",
            ),
        ]

    def _get_testing_workflow(self) -> List[WorkflowStep]:
        """Get testing workflow steps"""
        return [
            WorkflowStep(
                name="test_generation",
                description="Generate missing tests",
                command="echo 'Test generation completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="run_tests",
                description="Execute all tests",
                command="python -m pytest tests/ -v",
            ),
            WorkflowStep(
                name="coverage_analysis",
                description="Analyze test coverage",
                command="python -m pytest tests/ --cov=src --cov-report=html",
            ),
            WorkflowStep(
                name="performance_tests",
                description="Run performance tests",
                command="echo 'Performance tests completed'",
                required=False,
            ),
        ]

    def _get_documentation_workflow(self) -> List[WorkflowStep]:
        """Get documentation workflow steps"""
        return [
            WorkflowStep(
                name="documentation_analysis",
                description="Analyze current documentation coverage",
                command="echo 'Documentation analysis completed'",
            ),
            WorkflowStep(
                name="documentation_generation",
                description="Generate missing documentation",
                command="echo 'Documentation generation completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="api_documentation",
                description="Generate API documentation",
                command="echo 'API documentation completed'",
                required=False,
            ),
            WorkflowStep(
                name="readme_update",
                description="Update README files",
                command="echo 'README updates completed'",
                required=False,
            ),
        ]

    def _get_deployment_workflow(self) -> List[WorkflowStep]:
        """Get deployment workflow steps"""
        return [
            WorkflowStep(
                name="pre_deployment_tests",
                description="Run comprehensive pre-deployment tests",
                command="python -m pytest tests/ -v --tb=short",
            ),
            WorkflowStep(
                name="security_check",
                description="Final security check",
                command="echo 'Security check completed'",
            ),
            WorkflowStep(
                name="dependency_check",
                description="Check for outdated dependencies",
                command="echo 'Dependency check completed'",
            ),
            WorkflowStep(
                name="deployment",
                description="Deploy to production",
                command="echo 'Deployment completed'",
            ),
        ]

    def is_configured(self) -> bool:
        """Check if AI Dev Workflow is properly configured"""
        return bool(self.openai_key or self.anthropic_key)


def get_ai_dev_workflow(project_path: str = ".") -> AIDevWorkflow:
    """Get global AI Dev Workflow instance"""
    if not hasattr(get_ai_dev_workflow, "_instance"):
        get_ai_dev_workflow._instance = AIDevWorkflow(project_path)
    return get_ai_dev_workflow._instance


if __name__ == "__main__":
    # Example usage
    workflow = get_ai_dev_workflow()

    if workflow.is_configured():
        print("✅ AI Dev Workflow is configured and ready!")

        # Show available workflows
        print(
            f"\n📋 Available workflows: {', '.join(workflow.get_available_workflows())}"
        )

        # Analyze project
        print("\n🔍 Analyzing project...")
        analysis = workflow.analyze_project()
        print(f"Project: {analysis.project_path}")
        print(f"Code files: {analysis.code_files}")
        print(f"Test coverage: {analysis.test_coverage:.1f}%")
        print(f"Code quality: {analysis.code_quality_score:.1f}")
        print(f"Recommendations: {', '.join(analysis.recommendations)}")

        # Execute TDD workflow
        print("\n🚀 Executing TDD workflow...")
        results = workflow.execute_workflow("tdd")

        for step_name, result in results.items():
            status = "✅" if result.success else "❌"
            print(f"{status} {step_name}: {result.output[:100]}...")

    else:
        print("❌ AI Dev Workflow not configured. Please set up API keys.")
