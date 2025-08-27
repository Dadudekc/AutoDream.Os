import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from textwrap import dedent


class TestLanguageAnalyzerParsing:
    def test_language_analyzer_initialization(self, language_analyzer):
        assert language_analyzer is not None
        assert hasattr(language_analyzer, "python_analyzer")
        assert hasattr(language_analyzer, "tree_sitter_analyzer")

    @patch("src.services.tree_sitter_analyzer.Language")
    @patch("src.services.tree_sitter_analyzer.Parser")
    @patch("pathlib.Path.exists")
    def test_tree_sitter_initialization_success(
        self, mock_exists, mock_parser, mock_language, language_analyzer
    ):
        mock_language.return_value = "mock_language"
        mock_parser_instance = Mock()
        mock_parser.return_value = mock_parser_instance
        mock_exists.return_value = True

        result = language_analyzer.tree_sitter_analyzer._init_parser("rust")
        assert result == mock_parser_instance

        result = language_analyzer.tree_sitter_analyzer._init_parser("javascript")
        assert result == mock_parser_instance

    @patch("src.services.tree_sitter_analyzer.Language")
    @patch("src.services.tree_sitter_analyzer.Parser")
    def test_tree_sitter_initialization_failure(
        self, mock_parser, mock_language, language_analyzer
    ):
        mock_language.side_effect = Exception("Grammar not found")
        result = language_analyzer.tree_sitter_analyzer._init_parser("rust")
        assert result is None

    def test_analyze_file_python_success(self, language_analyzer):
        python_code = dedent(
            '''
            def test_function():
                """Test docstring"""
                pass

            class TestClass:
                """Test class docstring"""
                def test_method(self):
                    pass

            @app.route("/test")
            def test_route():
                return "test"
            '''
        )
        result = language_analyzer.analyze_file(Path("test.py"), python_code)
        assert result["language"] == ".py"
        assert "test_function" in result["functions"]
        assert "TestClass" in result["classes"]
        assert result["classes"]["TestClass"]["methods"] == ["test_method"]
        assert result["classes"]["TestClass"]["docstring"] == "Test class docstring"
        assert len(result["routes"]) == 1
        assert result["routes"][0]["function"] == "test_route"
        assert result["routes"][0]["path"] == "/test"
        assert result["complexity"] > 0

    def test_analyze_file_python_with_classes(self, language_analyzer):
        python_code = dedent(
            '''
            class BaseClass:
                """Base class docstring"""
                def base_method(self):
                    pass

            class DerivedClass(BaseClass):
                """Derived class docstring"""
                def derived_method(self):
                    pass

                def another_method(self):
                    pass

            class UtilityClass:
                def utility_method(self):
                    pass
            '''
        )
        result = language_analyzer.analyze_file(Path("classes.py"), python_code)
        assert result["language"] == ".py"
        assert "BaseClass" in result["classes"]
        assert "DerivedClass" in result["classes"]
        assert "UtilityClass" in result["classes"]
        assert "BaseClass" in result["classes"]["DerivedClass"]["base_classes"]
        assert "base_method" in result["classes"]["BaseClass"]["methods"]
        assert "derived_method" in result["classes"]["DerivedClass"]["methods"]
        assert "another_method" in result["classes"]["DerivedClass"]["methods"]
        assert "utility_method" in result["classes"]["UtilityClass"]["methods"]
        assert result["classes"]["BaseClass"]["docstring"] == "Base class docstring"
        assert (
            result["classes"]["DerivedClass"]["docstring"] == "Derived class docstring"
        )

    @patch("src.services.tree_sitter_analyzer.Language")
    @patch("src.services.tree_sitter_analyzer.Parser")
    def test_analyze_file_rust_success(
        self, mock_parser, mock_language, language_analyzer
    ):
        mock_language.return_value = "mock_rust_language"
        mock_parser_instance = Mock()
        mock_parser.return_value = mock_parser_instance
        mock_tree = Mock()
        mock_root = Mock()
        mock_parser_instance.parse.return_value = mock_tree
        mock_tree.root_node = mock_root
        mock_root.children = []

        rust_code = dedent(
            """
            fn test_function() {
                println!("Hello, world!");
            }

            struct TestStruct {
                field: i32,
            }

            impl TestStruct {
                fn new() -> Self {
                    TestStruct { field: 0 }
                }

                fn get_field(&self) -> i32 {
                    self.field
                }
            }
            """
        )
        result = language_analyzer.analyze_file(Path("test.rs"), rust_code)
        assert result["language"] == ".rs"
        assert isinstance(result["functions"], list)
        assert isinstance(result["classes"], dict)
        assert result["routes"] == []
        assert isinstance(result["complexity"], int)

    @patch("src.services.tree_sitter_analyzer.Language")
    @patch("src.services.tree_sitter_analyzer.Parser")
    def test_analyze_file_javascript_success(
        self, mock_parser, mock_language, language_analyzer
    ):
        mock_language.return_value = "mock_js_language"
        mock_parser_instance = Mock()
        mock_parser.return_value = mock_parser_instance
        mock_tree = Mock()
        mock_root = Mock()
        mock_parser_instance.parse.return_value = mock_tree
        mock_tree.root_node = mock_root
        mock_root.children = []

        javascript_code = dedent(
            """
            function testFunction() {
                console.log("Hello, world!");
            }

            class TestClass {
                constructor() {
                    this.field = 0;
                }

                testMethod() {
                    return this.field;
                }
            }

            const arrowFunction = () => {
                return "arrow";
            };

            // Express.js route
            app.get("/test", (req, res) => {
                res.send("test");
            });
            """
        )
        result = language_analyzer.analyze_file(Path("test.js"), javascript_code)
        assert result["language"] == ".js"
        assert isinstance(result["functions"], list)
        assert isinstance(result["classes"], dict)
        assert isinstance(result["routes"], list)
        assert isinstance(result["complexity"], int)
