import tempfile
from pathlib import Path

import pytest

from .code_crafter_support import CodeCrafter, CodeGenerationRequest


@pytest.fixture
def temp_code_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    import shutil

    shutil.rmtree(temp_dir)


class TestCodeCrafterIntegration:
    """Integration tests covering the full workflow."""

    @pytest.mark.integration
    def test_full_code_generation_workflow(self, temp_code_dir):
        crafter = CodeCrafter()

        request = CodeGenerationRequest(
            description="Data processing pipeline",
            language="python",
            framework="pandas",
            requirements=["CSV input", "Data validation", "JSON output"],
            include_tests=True,
            include_docs=True,
        )

        result = crafter.generate_code(request)

        assert result.code is not None
        assert result.tests is not None
        assert result.documentation is not None
        assert "pandas" in result.dependencies

        code_file = temp_code_dir / "generated_code.py"
        code_file.write_text(result.code)

        analysis = crafter.analyze_code(str(code_file))

        assert analysis.file_path == str(code_file)
        assert analysis.complexity_score > 0
        assert analysis.maintainability_index > 0
        assert code_file.exists()
        assert code_file.stat().st_size > 0
