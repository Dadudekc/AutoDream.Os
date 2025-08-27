from pathlib import Path


class TestLanguageAnalyzerValidation:
    def test_analyze_file_python_no_content(self, language_analyzer):
        result = language_analyzer.analyze_file(Path("empty.py"), "")
        assert result["language"] == ".py"
        assert result["functions"] == []
        assert result["classes"] == {}
        assert result["routes"] == []
        assert result["complexity"] == 0

    def test_analyze_file_python_syntax_error_handling(self, language_analyzer):
        invalid_python = """
    def invalid_function(
        # Missing closing parenthesis
        pass
    """
        result = language_analyzer.analyze_file(Path("invalid.py"), invalid_python)
        assert result["language"] == ".py"
        assert isinstance(result["functions"], list)
        assert isinstance(result["classes"], dict)
        assert isinstance(result["routes"], list)
        assert isinstance(result["complexity"], int)

    def test_analyze_file_unsupported_language(self, language_analyzer):
        result = language_analyzer.analyze_file(Path("test.txt"), "Some text content")
        assert result["language"] == ".txt"
        assert result["functions"] == []
        assert result["classes"] == {}
        assert result["routes"] == []
        assert result["complexity"] == 0

    def test_analyze_file_case_insensitive_extension(self, language_analyzer):
        python_code = "def test(): pass"
        result1 = language_analyzer.analyze_file(Path("test.PY"), python_code)
        result2 = language_analyzer.analyze_file(Path("test.Py"), python_code)
        result3 = language_analyzer.analyze_file(Path("test.py"), python_code)
        assert result1["language"] == ".py"
        assert result2["language"] == ".py"
        assert result3["language"] == ".py"
        assert result1["functions"] == result2["functions"]
        assert result2["functions"] == result3["functions"]
