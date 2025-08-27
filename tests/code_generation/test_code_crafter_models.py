import pytest

from .code_crafter_support import (
    CodeAnalysis,
    CodeGenerationRequest,
    CodeGenerationResult,
)


class TestCodeAnalysis:
    """Test CodeAnalysis dataclass."""

    @pytest.mark.unit
    def test_code_analysis_creation(self):
        analysis = CodeAnalysis(
            file_path="test.py",
            complexity_score=5.5,
            maintainability_index=85.0,
            code_smells=["Long function"],
            suggestions=["Break into smaller functions"],
            security_issues=["Hardcoded password"],
            performance_issues=["Nested loops"],
            documentation_coverage=75.0,
            test_coverage=60.0,
        )

        assert analysis.file_path == "test.py"
        assert analysis.complexity_score == 5.5
        assert analysis.maintainability_index == 85.0
        assert "Long function" in analysis.code_smells
        assert "Break into smaller functions" in analysis.suggestions
        assert "Hardcoded password" in analysis.security_issues
        assert "Nested loops" in analysis.performance_issues
        assert analysis.documentation_coverage == 75.0
        assert analysis.test_coverage == 60.0

    @pytest.mark.unit
    def test_code_analysis_defaults(self):
        analysis = CodeAnalysis(
            file_path="test.py", complexity_score=3.0, maintainability_index=90.0
        )

        assert analysis.file_path == "test.py"
        assert analysis.complexity_score == 3.0
        assert analysis.maintainability_index == 90.0
        assert analysis.code_smells == []
        assert analysis.suggestions == []
        assert analysis.security_issues == []
        assert analysis.performance_issues == []
        assert analysis.documentation_coverage == 0.0
        assert analysis.test_coverage == 0.0


class TestCodeGenerationRequest:
    """Test CodeGenerationRequest dataclass."""

    @pytest.mark.unit
    def test_code_generation_request_creation(self):
        request = CodeGenerationRequest(
            description="Create a web API endpoint",
            language="python",
            framework="flask",
            requirements=["RESTful", "JSON response"],
            constraints=["No external dependencies"],
            style_guide="PEP 8",
            include_tests=True,
            include_docs=True,
        )

        assert request.description == "Create a web API endpoint"
        assert request.language == "python"
        assert request.framework == "flask"
        assert "RESTful" in request.requirements
        assert "No external dependencies" in request.constraints
        assert request.style_guide == "PEP 8"
        assert request.include_tests is True
        assert request.include_docs is True

    @pytest.mark.unit
    def test_code_generation_request_minimal(self):
        request = CodeGenerationRequest(
            description="Simple function", language="javascript"
        )

        assert request.description == "Simple function"
        assert request.language == "javascript"
        assert request.framework is None
        assert request.requirements == []
        assert request.constraints == []
        assert request.style_guide is None
        assert request.include_tests is True
        assert request.include_docs is True


class TestCodeGenerationResult:
    """Test CodeGenerationResult dataclass."""

    @pytest.mark.unit
    def test_code_generation_result_creation(self):
        result = CodeGenerationResult(
            code="def hello(): print('Hello')",
            tests="def test_hello(): assert True",
            documentation="# Hello function",
            explanation="Simple greeting function",
            estimated_complexity=1.0,
            dependencies=["builtins"],
            usage_examples=["hello()"],
        )

        assert result.code == "def hello(): print('Hello')"
        assert result.tests == "def test_hello(): assert True"
        assert result.documentation == "# Hello function"
        assert result.explanation == "Simple greeting function"
        assert result.estimated_complexity == 1.0
        assert "builtins" in result.dependencies
        assert "hello()" in result.usage_examples

    @pytest.mark.unit
    def test_code_generation_result_minimal(self):
        result = CodeGenerationResult(
            code="print('Hello')",
            explanation="Simple print statement",
            estimated_complexity=0.5,
        )

        assert result.code == "print('Hello')"
        assert result.tests is None
        assert result.documentation is None
        assert result.explanation == "Simple print statement"
        assert result.estimated_complexity == 0.5
        assert result.dependencies == []
        assert result.usage_examples == []
