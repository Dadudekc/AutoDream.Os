from pathlib import Path


class TestLanguageAnalyzerGeneration:
    def test_analyze_file_python_with_routes(self, language_analyzer):
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
        assert len(result["routes"]) >= 4
        routes = result["routes"]
        users_routes = [r for r in routes if r["function"] == "users"]
        profile_routes = [r for r in routes if r["function"] == "profile"]
        login_routes = [r for r in routes if r["function"] == "login"]
        api_data_routes = [r for r in routes if r["function"] == "api_data"]
        assert len(users_routes) >= 2
        assert any(r["method"] == "GET" for r in users_routes)
        assert any(r["method"] == "POST" for r in users_routes)
        assert all(r["path"] == "/users" for r in users_routes)
        assert len(profile_routes) >= 1
        assert any(r["method"] == "GET" for r in profile_routes)
        assert all(r["path"] == "/profile" for r in profile_routes)
        assert len(login_routes) >= 1
        assert any(r["method"] == "POST" for r in login_routes)
        assert all(r["path"] == "/login" for r in login_routes)
        assert len(api_data_routes) >= 2
        assert any(r["method"] == "PUT" for r in api_data_routes)
        assert any(r["method"] == "DELETE" for r in api_data_routes)
        assert all(r["path"] == "/api/v1/data" for r in api_data_routes)

    def test_analyze_file_python_complexity_calculation(self, language_analyzer):
        python_code = """
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
"""
        result = language_analyzer.analyze_file(Path("complexity.py"), python_code)
        expected_complexity = 2 + 2 + 1
        assert result["complexity"] >= expected_complexity

    def test_analyze_file_with_imports_and_comments(self, language_analyzer):
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
        assert result["complexity"] >= 2

    def test_analyze_file_nested_functions(self, language_analyzer):
        python_code = """
def outer_function():
    def inner_function():
        pass
    return inner_function

class OuterClass:
    def outer_method(self):
        def inner_method():
            pass
        return inner_method
"""
        result = language_analyzer.analyze_file(Path("nested.py"), python_code)
        assert result["language"] == ".py"
        assert "outer_function" in result["functions"]
        assert "OuterClass" in result["classes"]
        assert "outer_method" in result["classes"]["OuterClass"]["methods"]
