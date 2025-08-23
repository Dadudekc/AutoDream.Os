#!/usr/bin/env python3
"""
CodeCrafter - AI-Powered Development Tools
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

Advanced AI-powered code generation, analysis, and development assistance
"""
import os
import json
import logging
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

from .api_key_manager import get_openai_api_key, get_anthropic_api_key
from .utils import performance_monitor, get_config_manager

logger = logging.getLogger(__name__)


@dataclass
class CodeAnalysis:
    """Results of code analysis"""

    file_path: str
    complexity_score: float
    maintainability_index: float
    code_smells: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    security_issues: List[str] = field(default_factory=list)
    performance_issues: List[str] = field(default_factory=list)
    documentation_coverage: float = 0.0
    test_coverage: float = 0.0


@dataclass
class CodeGenerationRequest:
    """Request for code generation"""

    description: str
    language: str
    framework: Optional[str] = None
    requirements: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    style_guide: Optional[str] = None
    include_tests: bool = True
    include_docs: bool = True


@dataclass
class CodeGenerationResult:
    """Result of code generation"""

    code: str
    tests: Optional[str] = None
    documentation: Optional[str] = None
    explanation: str
    estimated_complexity: float
    dependencies: List[str] = field(default_factory=list)
    usage_examples: List[str] = field(default_factory=list)


class CodeCrafter:
    """AI-powered code generation and analysis tool"""

    def __init__(self):
        self.config = get_config_manager()
        self.openai_key = get_openai_api_key()
        self.anthropic_key = get_anthropic_api_key()
        self.supported_languages = [
            "python",
            "javascript",
            "typescript",
            "java",
            "cpp",
            "csharp",
            "go",
            "rust",
        ]
        self.supported_frameworks = {
            "python": ["django", "flask", "fastapi", "pytorch", "tensorflow", "pandas"],
            "javascript": ["react", "vue", "angular", "node", "express"],
            "typescript": ["react", "vue", "angular", "node", "express"],
            "java": ["spring", "hibernate", "junit", "maven"],
            "cpp": ["boost", "qt", "opencv", "eigen"],
            "csharp": [".net", "asp.net", "entity", "xunit"],
            "go": ["gin", "echo", "gorm", "testify"],
            "rust": ["tokio", "serde", "actix", "criterion"],
        }

    @performance_monitor("code_generation")
    def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationResult:
        """
        Generate code based on natural language description

        Args:
            request: Code generation request

        Returns:
            Generated code with tests and documentation
        """
        logger.info(f"Generating {request.language} code for: {request.description}")

        try:
            # Validate request
            self._validate_generation_request(request)

            # Generate code using AI
            if self.openai_key:
                return self._generate_with_openai(request)
            elif self.anthropic_key:
                return self._generate_with_anthropic(request)
            else:
                raise ValueError("No AI API keys configured")

        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            raise

    def _validate_generation_request(self, request: CodeGenerationRequest) -> None:
        """Validate code generation request"""
        if not request.description.strip():
            raise ValueError("Code description cannot be empty")

        if request.language.lower() not in self.supported_languages:
            raise ValueError(f"Unsupported language: {request.language}")

        if (
            request.framework
            and request.framework
            not in self.supported_frameworks.get(request.language.lower(), [])
        ):
            raise ValueError(
                f"Unsupported framework {request.framework} for {request.language}"
            )

    def _generate_with_openai(
        self, request: CodeGenerationRequest
    ) -> CodeGenerationResult:
        """Generate code using OpenAI API"""
        try:
            import openai

            openai.api_key = self.openai_key

            # Build prompt
            prompt = self._build_openai_prompt(request)

            # Generate code
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software developer. Generate high-quality, production-ready code.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=4000,
                temperature=0.3,
            )

            # Parse response
            return self._parse_openai_response(response, request)

        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        except Exception as e:
            logger.error(f"OpenAI code generation failed: {e}")
            raise

    def _generate_with_anthropic(
        self, request: CodeGenerationRequest
    ) -> CodeGenerationResult:
        """Generate code using Anthropic Claude API"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_key)

            # Build prompt
            prompt = self._build_anthropic_prompt(request)

            # Generate code
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse response
            return self._parse_anthropic_response(response, request)

        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Run: pip install anthropic"
            )
        except Exception as e:
            logger.error(f"Anthropic code generation failed: {e}")
            raise

    def _build_openai_prompt(self, request: CodeGenerationRequest) -> str:
        """Build prompt for OpenAI"""
        prompt = f"""Generate high-quality {request.language} code for the following request:

DESCRIPTION: {request.description}

LANGUAGE: {request.language}
FRAMEWORK: {request.framework or 'Standard library'}
REQUIREMENTS: {', '.join(request.requirements) if request.requirements else 'None specified'}
CONSTRAINTS: {', '.join(request.constraints) if request.constraints else 'None specified'}

Please provide:
1. Clean, well-structured code
2. Proper error handling
3. Type hints (if applicable)
4. Comprehensive documentation
5. Unit tests (if requested)
6. Usage examples
7. Dependencies list
8. Complexity estimation

Format your response as JSON with keys: code, tests, documentation, explanation, estimated_complexity, dependencies, usage_examples"""

        return prompt

    def _build_anthropic_prompt(self, request: CodeGenerationRequest) -> str:
        """Build prompt for Anthropic Claude"""
        prompt = f"""You are an expert software developer. Generate high-quality {request.language} code for:

{request.description}

Language: {request.language}
Framework: {request.framework or 'Standard library'}
Requirements: {', '.join(request.requirements) if request.requirements else 'None'}
Constraints: {', '.join(request.constraints) if request.constraints else 'None'}

Provide:
- Clean, production-ready code
- Error handling
- Type hints (if applicable)
- Documentation
- Unit tests (if requested)
- Usage examples
- Dependencies
- Complexity estimate

Format as JSON with: code, tests, documentation, explanation, estimated_complexity, dependencies, usage_examples"""

        return prompt

    def _parse_openai_response(
        self, response: Any, request: CodeGenerationRequest
    ) -> CodeGenerationResult:
        """Parse OpenAI API response"""
        try:
            content = response.choices[0].message.content
            # Try to extract JSON from response
            json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(1))
            else:
                # Fallback: try to find JSON in the content
                data = json.loads(content)

            return CodeGenerationResult(
                code=data.get("code", ""),
                tests=data.get("tests") if request.include_tests else None,
                documentation=data.get("documentation")
                if request.include_docs
                else None,
                explanation=data.get("explanation", ""),
                estimated_complexity=data.get("estimated_complexity", 1.0),
                dependencies=data.get("dependencies", []),
                usage_examples=data.get("usage_examples", []),
            )

        except Exception as e:
            logger.error(f"Failed to parse OpenAI response: {e}")
            # Fallback: return basic result
            return CodeGenerationResult(
                code=response.choices[0].message.content,
                explanation="Code generated successfully",
                estimated_complexity=1.0,
            )

    def _parse_anthropic_response(
        self, response: Any, request: CodeGenerationRequest
    ) -> CodeGenerationResult:
        """Parse Anthropic API response"""
        try:
            content = response.content[0].text
            # Try to extract JSON from response
            json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(1))
            else:
                # Fallback: try to find JSON in the content
                data = json.loads(content)

            return CodeGenerationResult(
                code=data.get("code", ""),
                tests=data.get("tests") if request.include_tests else None,
                documentation=data.get("documentation")
                if request.include_docs
                else None,
                explanation=data.get("explanation", ""),
                estimated_complexity=data.get("estimated_complexity", 1.0),
                dependencies=data.get("dependencies", []),
                usage_examples=data.get("usage_examples", []),
            )

        except Exception as e:
            logger.error(f"Failed to parse Anthropic response: {e}")
            # Fallback: return basic result
            return CodeGenerationResult(
                code=response.content[0].text,
                explanation="Code generated successfully",
                estimated_complexity=1.0,
            )

    @performance_monitor("code_analysis")
    def analyze_code(self, file_path: Union[str, Path]) -> CodeAnalysis:
        """
        Analyze code quality and provide insights

        Args:
            file_path: Path to the code file

        Returns:
            Code analysis results
        """
        file_path = Path(file_path)
        logger.info(f"Analyzing code: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic analysis
            analysis = CodeAnalysis(file_path=str(file_path))

            # Language-specific analysis
            if file_path.suffix.lower() in [".py", ".pyw"]:
                analysis = self._analyze_python_code(content, analysis)
            elif file_path.suffix.lower() in [".js", ".jsx", ".ts", ".tsx"]:
                analysis = self._analyze_javascript_code(content, analysis)
            elif file_path.suffix.lower() in [".java"]:
                analysis = self._analyze_java_code(content, analysis)
            elif file_path.suffix.lower() in [".cpp", ".cc", ".cxx"]:
                analysis = self._analyze_cpp_code(content, analysis)
            else:
                analysis = self._analyze_generic_code(content, analysis)

            # AI-powered analysis
            analysis = self._enhance_analysis_with_ai(content, analysis)

            return analysis

        except Exception as e:
            logger.error(f"Code analysis failed: {e}")
            raise

    def _analyze_python_code(
        self, content: str, analysis: CodeAnalysis
    ) -> CodeAnalysis:
        """Analyze Python code"""
        try:
            tree = ast.parse(content)

            # Calculate complexity
            complexity = self._calculate_cyclomatic_complexity(tree)
            analysis.complexity_score = complexity

            # Check for code smells
            smells = []
            if complexity > 10:
                smells.append("High cyclomatic complexity")

            # Check for long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) > 20:
                        smells.append("Long function detected")
                    if len(node.args.args) > 5:
                        smells.append("Too many parameters")

            # Check documentation
            docstring_count = len(
                [
                    n
                    for n in ast.walk(tree)
                    if isinstance(n, ast.Expr) and isinstance(n.value, ast.Str)
                ]
            )
            total_functions = len(
                [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            )
            analysis.documentation_coverage = (
                docstring_count / max(total_functions, 1)
            ) * 100

            analysis.code_smells = smells
            analysis.maintainability_index = max(0, 100 - complexity * 2)

        except SyntaxError:
            analysis.code_smells.append("Syntax errors detected")
            analysis.complexity_score = 999
            analysis.maintainability_index = 0

        return analysis

    def _analyze_javascript_code(
        self, content: str, analysis: CodeAnalysis
    ) -> CodeAnalysis:
        """Analyze JavaScript/TypeScript code"""
        # Basic analysis for JavaScript
        lines = content.split("\n")
        analysis.complexity_score = len(
            [
                line
                for line in lines
                if any(keyword in line for keyword in ["if", "for", "while", "case"])
            ]
        )
        analysis.maintainability_index = max(0, 100 - analysis.complexity_score * 2)

        # Check for common issues
        smells = []
        if "console.log" in content:
            smells.append("Console.log statements in production code")
        if "eval(" in content:
            smells.append("Eval usage detected (security risk)")
        if "var " in content:
            smells.append("Var declarations (consider let/const)")

        analysis.code_smells = smells
        return analysis

    def _analyze_java_code(self, content: str, analysis: CodeAnalysis) -> CodeAnalysis:
        """Analyze Java code"""
        # Basic analysis for Java
        lines = content.split("\n")
        analysis.complexity_score = len(
            [
                line
                for line in lines
                if any(
                    keyword in line
                    for keyword in ["if", "for", "while", "case", "catch"]
                )
            ]
        )
        analysis.maintainability_index = max(0, 100 - analysis.complexity_score * 2)

        # Check for common issues
        smells = []
        if "System.out.println" in content:
            smells.append("System.out.println statements")
        if "catch (Exception e)" in content:
            smells.append("Generic exception catching")

        analysis.code_smells = smells
        return analysis

    def _analyze_cpp_code(self, content: str, analysis: CodeAnalysis) -> CodeAnalysis:
        """Analyze C++ code"""
        # Basic analysis for C++
        lines = content.split("\n")
        analysis.complexity_score = len(
            [
                line
                for line in lines
                if any(
                    keyword in line
                    for keyword in ["if", "for", "while", "case", "catch"]
                )
            ]
        )
        analysis.maintainability_index = max(0, 100 - analysis.complexity_score * 2)

        # Check for common issues
        smells = []
        if "using namespace std;" in content:
            smells.append("Using namespace std in header files")
        if "new " in content and "delete " not in content:
            smells.append("Memory allocation without deallocation")

        analysis.code_smells = smells
        return analysis

    def _analyze_generic_code(
        self, content: str, analysis: CodeAnalysis
    ) -> CodeAnalysis:
        """Analyze generic code"""
        lines = content.split("\n")
        analysis.complexity_score = len(
            [
                line
                for line in lines
                if any(keyword in line for keyword in ["if", "for", "while", "case"])
            ]
        )
        analysis.maintainability_index = max(0, 100 - analysis.complexity_score * 2)
        return analysis

    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for Python AST"""
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.With):
                complexity += 1
            elif isinstance(node, ast.Assert):
                complexity += 1
            elif isinstance(node, ast.Return):
                complexity += 1

        return complexity

    def _enhance_analysis_with_ai(
        self, content: str, analysis: CodeAnalysis
    ) -> CodeAnalysis:
        """Enhance analysis using AI insights"""
        try:
            if self.openai_key:
                return self._enhance_with_openai(content, analysis)
            elif self.anthropic_key:
                return self._enhance_with_anthropic(content, analysis)
        except Exception as e:
            logger.warning(f"AI enhancement failed: {e}")

        return analysis

    def _enhance_with_openai(
        self, content: str, analysis: CodeAnalysis
    ) -> CodeAnalysis:
        """Enhance analysis using OpenAI"""
        try:
            import openai

            openai.api_key = self.openai_key

            prompt = f"""Analyze this code and provide insights:

Code:
{content[:2000]}...

Current analysis:
- Complexity: {analysis.complexity_score}
- Maintainability: {analysis.maintainability_index}
- Smells: {', '.join(analysis.code_smells)}

Provide additional suggestions for:
1. Code improvements
2. Security considerations
3. Performance optimizations
4. Best practices

Format as JSON with: suggestions, security_issues, performance_issues"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a code review expert."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.3,
            )

            content = response.choices[0].message.content
            try:
                data = json.loads(content)
                analysis.suggestions.extend(data.get("suggestions", []))
                analysis.security_issues.extend(data.get("security_issues", []))
                analysis.performance_issues.extend(data.get("performance_issues", []))
            except json.JSONDecodeError:
                pass

        except Exception as e:
            logger.warning(f"OpenAI enhancement failed: {e}")

        return analysis

    def _enhance_with_anthropic(
        self, content: str, analysis: CodeAnalysis
    ) -> CodeAnalysis:
        """Enhance analysis using Anthropic Claude"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_key)

            prompt = f"""Analyze this code and provide insights:

Code:
{content[:2000]}...

Current analysis:
- Complexity: {analysis.complexity_score}
- Maintainability: {analysis.maintainability_index}
- Smells: {', '.join(analysis.code_smells)}

Provide additional suggestions for:
1. Code improvements
2. Security considerations
3. Performance optimizations
4. Best practices

Format as JSON with: suggestions, security_issues, performance_issues"""

            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text
            try:
                data = json.loads(content)
                analysis.suggestions.extend(data.get("suggestions", []))
                analysis.security_issues.extend(data.get("security_issues", []))
                analysis.performance_issues.extend(data.get("performance_issues", []))
            except json.JSONDecodeError:
                pass

        except Exception as e:
            logger.warning(f"Anthropic enhancement failed: {e}")

        return analysis

    def refactor_code(self, file_path: Union[str, Path], suggestions: List[str]) -> str:
        """
        Refactor code based on suggestions

        Args:
            file_path: Path to the code file
            suggestions: List of refactoring suggestions

        Returns:
            Refactored code
        """
        file_path = Path(file_path)
        logger.info(f"Refactoring code: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Use AI to refactor code
            if self.openai_key:
                return self._refactor_with_openai(
                    content, suggestions, file_path.suffix
                )
            elif self.anthropic_key:
                return self._refactor_with_anthropic(
                    content, suggestions, file_path.suffix
                )
            else:
                raise ValueError("No AI API keys configured for refactoring")

        except Exception as e:
            logger.error(f"Code refactoring failed: {e}")
            raise

    def _refactor_with_openai(
        self, content: str, suggestions: List[str], file_extension: str
    ) -> str:
        """Refactor code using OpenAI"""
        try:
            import openai

            openai.api_key = self.openai_key

            prompt = f"""Refactor this code based on the following suggestions:

Code:
{content}

Suggestions:
{chr(10).join(f"- {s}" for s in suggestions)}

Please provide the refactored code that addresses these suggestions while maintaining functionality and improving code quality.

Return only the refactored code."""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code refactoring specialist.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=4000,
                temperature=0.2,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI refactoring failed: {e}")
            raise

    def _refactor_with_anthropic(
        self, content: str, suggestions: List[str], file_extension: str
    ) -> str:
        """Refactor code using Anthropic Claude"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_key)

            prompt = f"""Refactor this code based on the following suggestions:

Code:
{content}

Suggestions:
{chr(10).join(f"- {s}" for s in suggestions)}

Please provide the refactored code that addresses these suggestions while maintaining functionality and improving code quality.

Return only the refactored code."""

            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Anthropic refactoring failed: {e}")
            raise

    def generate_tests(
        self, file_path: Union[str, Path], framework: Optional[str] = None
    ) -> str:
        """
        Generate unit tests for code

        Args:
            file_path: Path to the code file
            framework: Testing framework to use

        Returns:
            Generated test code
        """
        file_path = Path(file_path)
        logger.info(f"Generating tests for: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Determine testing framework
            if not framework:
                framework = self._detect_testing_framework(file_path)

            # Generate tests using AI
            if self.openai_key:
                return self._generate_tests_with_openai(
                    content, framework, file_path.suffix
                )
            elif self.anthropic_key:
                return self._generate_tests_with_anthropic(
                    content, framework, file_path.suffix
                )
            else:
                raise ValueError("No AI API keys configured for test generation")

        except Exception as e:
            logger.error(f"Test generation failed: {e}")
            raise

    def _detect_testing_framework(self, file_path: Path) -> str:
        """Detect appropriate testing framework based on file type"""
        if file_path.suffix.lower() in [".py", ".pyw"]:
            return "pytest"
        elif file_path.suffix.lower() in [".js", ".jsx", ".ts", ".tsx"]:
            return "jest"
        elif file_path.suffix.lower() in [".java"]:
            return "junit"
        elif file_path.suffix.lower() in [".cpp", ".cc", ".cxx"]:
            return "gtest"
        else:
            return "generic"

    def _generate_tests_with_openai(
        self, content: str, framework: str, file_extension: str
    ) -> str:
        """Generate tests using OpenAI"""
        try:
            import openai

            openai.api_key = self.openai_key

            prompt = f"""Generate comprehensive unit tests for this code using {framework}:

Code:
{content}

Requirements:
1. Test all public functions/methods
2. Include edge cases and error conditions
3. Use proper testing patterns and assertions
4. Include setup and teardown if needed
5. Mock external dependencies
6. Ensure good test coverage

Return only the test code."""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert testing specialist.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=3000,
                temperature=0.2,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI test generation failed: {e}")
            raise

    def _generate_tests_with_anthropic(
        self, content: str, framework: str, file_extension: str
    ) -> str:
        """Generate tests using Anthropic Claude"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_key)

            prompt = f"""Generate comprehensive unit tests for this code using {framework}:

Code:
{content}

Requirements:
1. Test all public functions/methods
2. Include edge cases and error conditions
3. Use proper testing patterns and assertions
4. Include setup and teardown if needed
5. Mock external dependencies
6. Ensure good test coverage

Return only the test code."""

            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Anthropic test generation failed: {e}")
            raise

    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages"""
        return self.supported_languages.copy()

    def get_supported_frameworks(self, language: str) -> List[str]:
        """Get supported frameworks for a specific language"""
        return self.supported_frameworks.get(language.lower(), []).copy()

    def is_configured(self) -> bool:
        """Check if CodeCrafter is properly configured"""
        return bool(self.openai_key or self.anthropic_key)


def get_code_crafter() -> CodeCrafter:
    """Get global CodeCrafter instance"""
    if not hasattr(get_code_crafter, "_instance"):
        get_code_crafter._instance = CodeCrafter()
    return get_code_crafter._instance


if __name__ == "__main__":
    # Example usage
    crafter = get_code_crafter()

    if crafter.is_configured():
        print("✅ CodeCrafter is configured and ready!")

        # Example code generation
        request = CodeGenerationRequest(
            description="Create a function to calculate fibonacci numbers with memoization",
            language="python",
            include_tests=True,
            include_docs=True,
        )

        try:
            result = crafter.generate_code(request)
            print(f"\n🎯 Generated Code:\n{result.code}")
            if result.tests:
                print(f"\n🧪 Generated Tests:\n{result.tests}")
            if result.documentation:
                print(f"\n📚 Generated Documentation:\n{result.documentation}")
        except Exception as e:
            print(f"❌ Code generation failed: {e}")
    else:
        print("❌ CodeCrafter not configured. Please set up API keys.")
