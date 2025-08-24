import pytest

from .code_crafter_support import CodeCrafter, CodeGenerationRequest


class TestCodeCrafterGeneration:
    """Tests focused on the CodeCrafter.generate_code workflow."""

    @pytest.mark.unit
    def test_code_crafter_initialization(self):
        crafter = CodeCrafter()

        assert "python" in crafter.supported_languages
        assert "javascript" in crafter.supported_languages
        assert "flask" in crafter.supported_frameworks["python"]
        assert "react" in crafter.supported_frameworks["javascript"]

    @pytest.mark.unit
    def test_generate_code_python(self):
        crafter = CodeCrafter()
        request = CodeGenerationRequest(
            description="Simple calculator function",
            language="python",
            include_tests=True,
            include_docs=True,
        )

        result = crafter.generate_code(request)

        assert result.code is not None
        assert "def main()" in result.code
        assert result.tests is not None
        assert "unittest" in result.tests
        assert result.documentation is not None
        assert "Python" in result.documentation
        assert result.explanation is not None
        assert result.estimated_complexity > 0
        assert len(result.dependencies) >= 0
        assert len(result.usage_examples) > 0

    @pytest.mark.unit
    def test_generate_code_javascript(self):
        crafter = CodeCrafter()
        request = CodeGenerationRequest(
            description="Web server",
            language="javascript",
            framework="express",
            include_tests=True,
            include_docs=True,
        )

        result = crafter.generate_code(request)

        assert result.code is not None
        assert "function main()" in result.code
        assert result.tests is not None
        assert "describe" in result.tests
        assert result.documentation is not None
        assert "JavaScript" in result.documentation
        assert result.explanation is not None
        assert result.estimated_complexity > 0
        assert len(result.dependencies) >= 0
        assert len(result.usage_examples) > 0

    @pytest.mark.unit
    def test_generate_code_invalid_language(self):
        crafter = CodeCrafter()
        request = CodeGenerationRequest(description="Test", language="invalid_language")

        with pytest.raises(ValueError, match="Unsupported language"):
            crafter.generate_code(request)

    @pytest.mark.unit
    def test_generate_code_invalid_framework(self):
        crafter = CodeCrafter()
        request = CodeGenerationRequest(
            description="Test", language="python", framework="invalid_framework"
        )

        with pytest.raises(ValueError, match="Unsupported framework"):
            crafter.generate_code(request)

    @pytest.mark.unit
    def test_generate_code_no_description(self):
        crafter = CodeCrafter()
        request = CodeGenerationRequest(description="", language="python")

        with pytest.raises(ValueError, match="Description is required"):
            crafter.generate_code(request)
