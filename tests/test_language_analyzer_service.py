#!/usr/bin/env python3
"""
Test-Driven Development: Language Analyzer Service Tests
======================================================

Tests written BEFORE implementation to drive development.
Follows TDD workflow: RED (failing) → GREEN (passing) → REFACTOR.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import the service we'll create
from src.services.language_analyzer_service import LanguageAnalyzerService


class TestLanguageAnalyzerService:
    """Test LanguageAnalyzerService functionality."""
    
    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def language_analyzer(self):
        """Create LanguageAnalyzerService instance for testing."""
        return LanguageAnalyzerService()
    
    def test_language_analyzer_initialization(self, language_analyzer):
        """Test language analyzer initializes correctly."""
        assert language_analyzer is not None
        assert hasattr(language_analyzer, 'rust_parser')
        assert hasattr(language_analyzer, 'js_parser')
    
    @patch('src.services.language_analyzer_service.Language')
    @patch('src.services.language_analyzer_service.Parser')
    def test_tree_sitter_initialization_success(self, mock_parser, mock_language, language_analyzer):
        """Test successful tree-sitter language initialization."""
        # Mock successful initialization
        mock_language.return_value = "mock_language"
        mock_parser_instance = Mock()
        mock_parser.return_value = mock_parser_instance
        
        # Test Rust parser initialization
        result = language_analyzer._init_tree_sitter_language("rust")
        assert result is not None
        assert result == mock_parser_instance
        
        # Test JavaScript parser initialization
        result = language_analyzer._init_tree_sitter_language("javascript")
        assert result is not None
        assert result == mock_parser_instance
    
    @patch('src.services.language_analyzer_service.Language')
    @patch('src.services.language_analyzer_service.Parser')
    def test_tree_sitter_initialization_failure(self, mock_parser, mock_language, language_analyzer):
        """Test tree-sitter initialization failure handling."""
        # Mock initialization failure
        mock_language.side_effect = Exception("Grammar not found")
        
        result = language_analyzer._init_tree_sitter_language("rust")
        assert result is None
    
    def test_analyze_file_python_success(self, language_analyzer):
        """Test successful Python file analysis."""
        python_code = '''
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
        """Test Python file analysis with complex class structures."""
        python_code = '''
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
        
        result = language_analyzer.analyze_file(Path("classes.py"), python_code)
        
        assert result["language"] == ".py"
        assert "BaseClass" in result["classes"]
        assert "DerivedClass" in result["classes"]
        assert "UtilityClass" in result["classes"]
        
        # Check base classes
        assert "BaseClass" in result["classes"]["DerivedClass"]["base_classes"]
        
        # Check methods
        assert "base_method" in result["classes"]["BaseClass"]["methods"]
        assert "derived_method" in result["classes"]["DerivedClass"]["methods"]
        assert "another_method" in result["classes"]["DerivedClass"]["methods"]
        assert "utility_method" in result["classes"]["UtilityClass"]["methods"]
        
        # Check docstrings
        assert result["classes"]["BaseClass"]["docstring"] == "Base class docstring"
        assert result["classes"]["DerivedClass"]["docstring"] == "Derived class docstring"
    
    def test_analyze_file_python_with_routes(self, language_analyzer):
        """Test Python file analysis with various route patterns."""
        python_code = '''
from flask import Flask
app = Flask(__name__)

@app.route("/users", methods=["GET", "POST"])
def users():
    pass

@app.get("/profile")
def profile():
    pass

@app.post("/login")
def login():
    pass

@app.route("/api/v1/data", methods=["PUT", "DELETE"])
def api_data():
    pass
'''
        
        result = language_analyzer.analyze_file(Path("routes.py"), python_code)
        
        assert result["language"] == ".py"
        assert len(result["routes"]) == 4
        
        # Check route details
        routes = {r["function"]: r for r in result["routes"]}
        
        assert "users" in routes
        assert routes["users"]["path"] == "/users"
        assert "GET" in routes["users"]["method"]
        assert "POST" in routes["users"]["method"]
        
        assert "profile" in routes
        assert routes["profile"]["path"] == "/profile"
        assert routes["profile"]["method"] == "GET"
        
        assert "login" in routes
        assert routes["login"]["path"] == "/login"
        assert routes["login"]["method"] == "POST"
        
        assert "api_data" in routes
        assert routes["api_data"]["path"] == "/api/v1/data"
        assert "PUT" in routes["api_data"]["method"]
        assert "DELETE" in routes["api_data"]["method"]
    
    def test_analyze_file_python_complexity_calculation(self, language_analyzer):
        """Test Python complexity calculation."""
        python_code = '''
def function1():
    pass

def function2():
    pass

class Class1:
    def method1(self):
        pass
    def method2(self):
        pass

class Class2:
    def method3(self):
        pass
'''
        
        result = language_analyzer.analyze_file(Path("complexity.py"), python_code)
        
        # 2 functions + 2 classes with 2+1 methods = 5 complexity
        expected_complexity = 2 + 2 + 1
        assert result["complexity"] == expected_complexity
    
    def test_analyze_file_python_no_content(self, language_analyzer):
        """Test Python file analysis with empty content."""
        result = language_analyzer.analyze_file(Path("empty.py"), "")
        
        assert result["language"] == ".py"
        assert result["functions"] == []
        assert result["classes"] == {}
        assert result["routes"] == []
        assert result["complexity"] == 0
    
    def test_analyze_file_python_syntax_error_handling(self, language_analyzer):
        """Test Python file analysis with syntax errors."""
        invalid_python = '''
def invalid_function(
    # Missing closing parenthesis
    pass
'''
        
        # Should handle syntax errors gracefully
        result = language_analyzer.analyze_file(Path("invalid.py"), invalid_python)
        
        # Should return basic structure even with syntax errors
        assert result["language"] == ".py"
        assert isinstance(result["functions"], list)
        assert isinstance(result["classes"], dict)
        assert isinstance(result["routes"], list)
        assert isinstance(result["complexity"], int)
    
    @patch('src.services.language_analyzer_service.Language')
    @patch('src.services.language_analyzer_service.Parser')
    def test_analyze_file_rust_success(self, mock_parser, mock_language, language_analyzer):
        """Test successful Rust file analysis."""
        # Mock tree-sitter parser
        mock_language.return_value = "mock_rust_language"
        mock_parser_instance = Mock()
        mock_parser.return_value = mock_parser_instance
        
        # Mock parse result
        mock_tree = Mock()
        mock_root = Mock()
        mock_parser_instance.parse.return_value = mock_tree
        mock_tree.root_node = mock_root
        
        # Mock node traversal
        mock_root.children = []
        
        rust_code = '''
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
'''
        
        result = language_analyzer.analyze_file(Path("test.rs"), rust_code)
        
        assert result["language"] == ".rs"
        assert isinstance(result["functions"], list)
        assert isinstance(result["classes"], dict)
        assert result["routes"] == []
        assert isinstance(result["complexity"], int)
    
    @patch('src.services.language_analyzer_service.Language')
    @patch('src.services.language_analyzer_service.Parser')
    def test_analyze_file_javascript_success(self, mock_parser, mock_language, language_analyzer):
        """Test successful JavaScript file analysis."""
        # Mock tree-sitter parser
        mock_language.return_value = "mock_js_language"
        mock_parser_instance = Mock()
        mock_parser.return_value = mock_parser_instance
        
        # Mock parse result
        mock_tree = Mock()
        mock_root = Mock()
        mock_parser_instance.parse.return_value = mock_tree
        mock_tree.root_node = mock_root
        
        # Mock node traversal
        mock_root.children = []
        
        javascript_code = '''
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
'''
        
        result = language_analyzer.analyze_file(Path("test.js"), javascript_code)
        
        assert result["language"] == ".js"
        assert isinstance(result["functions"], list)
        assert isinstance(result["classes"], dict)
        assert isinstance(result["routes"], list)
        assert isinstance(result["complexity"], int)
    
    def test_analyze_file_unsupported_language(self, language_analyzer):
        """Test analysis of unsupported language files."""
        result = language_analyzer.analyze_file(Path("test.txt"), "Some text content")
        
        assert result["language"] == ".txt"
        assert result["functions"] == []
        assert result["classes"] == {}
        assert result["routes"] == []
        assert result["complexity"] == 0
    
    def test_analyze_file_case_insensitive_extension(self, language_analyzer):
        """Test that file extension analysis is case insensitive."""
        python_code = 'def test(): pass'
        
        # Test different case variations
        result1 = language_analyzer.analyze_file(Path("test.PY"), python_code)
        result2 = language_analyzer.analyze_file(Path("test.Py"), python_code)
        result3 = language_analyzer.analyze_file(Path("test.py"), python_code)
        
        assert result1["language"] == ".py"
        assert result2["language"] == ".py"
        assert result3["language"] == ".py"
        
        # All should have same analysis
        assert result1["functions"] == result2["functions"]
        assert result2["functions"] == result3["functions"]
    
    def test_analyze_file_with_imports_and_comments(self, language_analyzer):
        """Test Python file analysis with imports and comments."""
        python_code = '''
# This is a comment
import os
import sys
from pathlib import Path

# Another comment
def test_function():
    """Function docstring"""
    # Inline comment
    return True

class TestClass:
    """Class docstring"""
    # Class comment
    def __init__(self):
        pass
'''
        
        result = language_analyzer.analyze_file(Path("imports.py"), python_code)
        
        assert result["language"] == ".py"
        assert "test_function" in result["functions"]
        assert "TestClass" in result["classes"]
        assert result["classes"]["TestClass"]["methods"] == ["__init__"]
        assert result["complexity"] == 2  # 1 function + 1 method
    
    def test_analyze_file_nested_functions(self, language_analyzer):
        """Test Python file analysis with nested functions."""
        python_code = '''
def outer_function():
    def inner_function():
        pass
    return inner_function

class OuterClass:
    def outer_method(self):
        def inner_method():
            pass
        return inner_method
'''
        
        result = language_analyzer.analyze_file(Path("nested.py"), python_code)
        
        assert result["language"] == ".py"
        assert "outer_function" in result["functions"]
        assert "OuterClass" in result["classes"]
        assert "outer_method" in result["classes"]["OuterClass"]["methods"]
        
        # Nested functions should not be counted in top-level functions
        assert "inner_function" not in result["functions"]
        assert "inner_method" not in result["classes"]["OuterClass"]["methods"]


# Test execution and coverage verification
if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([
        __file__,
        "--cov=src.services.language_analyzer_service",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v"
    ])
