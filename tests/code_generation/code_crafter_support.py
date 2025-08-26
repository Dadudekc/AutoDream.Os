"""Lightweight CodeCrafter implementation used for testing."""

import logging
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass


logger = logging.getLogger(__name__)

# ============================================================================
# Lightweight module code (to avoid import issues in tests)
# ============================================================================


@dataclass
class CodeAnalysis:
    """Results of code analysis"""

    file_path: str
    complexity_score: float
    maintainability_index: float
    code_smells: List[str] = None
    suggestions: List[str] = None
    security_issues: List[str] = None
    performance_issues: List[str] = None
    documentation_coverage: float = 0.0
    test_coverage: float = 0.0

    def __post_init__(self):
        if self.code_smells is None:
            self.code_smells = []
        if self.suggestions is None:
            self.suggestions = []
        if self.security_issues is None:
            self.security_issues = []
        if self.performance_issues is None:
            self.performance_issues = []


@dataclass
class CodeGenerationRequest:
    """Request for code generation"""

    description: str
    language: str
    framework: Optional[str] = None
    requirements: List[str] = None
    constraints: List[str] = None
    style_guide: Optional[str] = None
    include_tests: bool = True
    include_docs: bool = True

    def __post_init__(self):
        if self.requirements is None:
            self.requirements = []
        if self.constraints is None:
            self.constraints = []


@dataclass
class CodeGenerationResult:
    """Result of code generation"""

    code: str
    explanation: str
    estimated_complexity: float
    tests: Optional[str] = None
    documentation: Optional[str] = None
    dependencies: List[str] = None
    usage_examples: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.usage_examples is None:
            self.usage_examples = []


class CodeCrafter:
    """AI-powered code generation and analysis tool"""

    def __init__(self):
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

            # Generate code using AI (mocked for testing)
            code = self._generate_code_content(request)
            tests = self._generate_tests(request) if request.include_tests else None
            documentation = (
                self._generate_documentation(request) if request.include_docs else None
            )

            # Calculate complexity
            complexity = self._calculate_complexity(code)

            # Extract dependencies
            dependencies = self._extract_dependencies(code, request.language)

            # Generate usage examples
            examples = self._generate_usage_examples(code, request.language)

            return CodeGenerationResult(
                code=code,
                tests=tests,
                documentation=documentation,
                explanation=f"Generated {request.language} code for: {request.description}",
                estimated_complexity=complexity,
                dependencies=dependencies,
                usage_examples=examples,
            )

        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            raise

    def analyze_code(self, file_path: str) -> CodeAnalysis:
        """
        Analyze existing code for quality metrics

        Args:
            file_path: Path to the code file

        Returns:
            Code analysis results
        """
        logger.info(f"Analyzing code file: {file_path}")

        try:
            # Read and parse code
            code_content = self._read_code_file(file_path)

            # Analyze complexity
            complexity = self._analyze_complexity(code_content)

            # Analyze maintainability
            maintainability = self._analyze_maintainability(code_content)

            # Detect code smells
            smells = self._detect_code_smells(code_content)

            # Generate suggestions
            suggestions = self._generate_suggestions(code_content, smells)

            # Check for security issues
            security_issues = self._check_security_issues(code_content)

            # Check for performance issues
            performance_issues = self._check_performance_issues(code_content)

            # Calculate documentation coverage
            doc_coverage = self._calculate_documentation_coverage(code_content)

            # Calculate test coverage (would need test files)
            test_coverage = 0.0

            return CodeAnalysis(
                file_path=file_path,
                complexity_score=complexity,
                maintainability_index=maintainability,
                code_smells=smells,
                suggestions=suggestions,
                security_issues=security_issues,
                performance_issues=performance_issues,
                documentation_coverage=doc_coverage,
                test_coverage=test_coverage,
            )

        except Exception as e:
            logger.error(f"Code analysis failed: {e}")
            raise

    def _validate_generation_request(self, request: CodeGenerationRequest) -> None:
        """Validate code generation request"""
        if not request.description:
            raise ValueError("Description is required")

        if request.language not in self.supported_languages:
            raise ValueError(f"Unsupported language: {request.language}")

        if (
            request.framework
            and request.framework
            not in self.supported_frameworks.get(request.language, [])
        ):
            raise ValueError(
                f"Unsupported framework: {request.framework} for language: {request.language}"
            )

    def _generate_code_content(self, request: CodeGenerationRequest) -> str:
        """Generate the main code content"""
        # Mock implementation for testing
        if request.language == "python":
            return self._generate_python_code(request)
        elif request.language == "javascript":
            return self._generate_javascript_code(request)
        else:
            return f"// Generated {request.language} code for: {request.description}"

    def _generate_python_code(self, request: CodeGenerationRequest) -> str:
        """Generate Python code"""
        code = f'''"""
{request.description}
Generated by CodeCrafter
"""

{self._generate_python_imports(request)}

def main():
    """Main function"""
    print("Hello from generated code!")
    
    # Implement core functionality based on request
    if request.framework == "flask":
        from flask import Flask, request, jsonify
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return jsonify({"message": "Hello from Flask!", "framework": f"{request.framework}"})
        
        @app.route('/api/data')
        def get_data():
            return jsonify({"data": [1, 2, 3, 4, 5], "count": 5})
        
        if __name__ == "__main__":
            app.run(debug=True)
    elif request.framework == "pandas":
        import pandas as pd
        import numpy as np
        # Data processing example
        data = {"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
        df = pd.DataFrame(data)
        print(f"DataFrame created with {len(df)} rows")
        print(df.head())
    else:
        # Standard Python functionality
        print(f"Framework: {request.framework or 'None'}")
        print("Standard Python code execution")

if __name__ == "__main__":
    main()
'''
        return code

    def _generate_javascript_code(self, request: CodeGenerationRequest) -> str:
        """Generate JavaScript code"""
        code = f"""/**
 * {request.description}
 * Generated by CodeCrafter
 */

{self._generate_javascript_imports(request)}

function main() {{
    console.log("Hello from generated code!");
    
    // Implement core functionality based on request
    if ("{request.framework}" === "express") {{
        const express = require('express');
        const app = express();
        
        app.get('/', (req, res) => {{
            res.json({{ message: 'Hello from Express!', framework: '{request.framework}' }});
        }});
        
        app.get('/api/data', (req, res) => {{
            res.json({{ data: [1, 2, 3, 4, 5], count: 5 }});
        }});
        
        const PORT = process.env.PORT || 3000;
        app.listen(PORT, () => {{
            console.log(`Server running on port ${PORT}`);
        }});
    }} else if ("{request.framework}" === "react") {{
        // React component example
        import React from 'react';
        const App = () => {{
            return React.createElement('div', null, 
                React.createElement('h1', null, 'Hello from React!'),
                React.createElement('p', null, `Framework: {request.framework}`)
            );
        }};
        
        console.log("React component created");
    }} else {{
        // Standard JavaScript functionality
        console.log(`Framework: ${request.framework || 'None'}`);
        console.log("Standard JavaScript code execution");
    }}
}}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ main }};
}}
"""
        return code

    def _generate_python_imports(self, request: CodeGenerationRequest) -> str:
        """Generate Python imports based on framework"""
        if request.framework == "flask":
            return "from flask import Flask, request, jsonify\n\napp = Flask(__name__)"
        elif request.framework == "pandas":
            return "import pandas as pd\nimport numpy as np"
        else:
            return "import os\nimport sys"

    def _generate_javascript_imports(self, request: CodeGenerationRequest) -> str:
        """Generate JavaScript imports based on framework"""
        if request.framework == "express":
            return "const express = require('express');\nconst app = express();"
        elif request.framework == "react":
            return "import React from 'react';"
        else:
            return "// Standard JavaScript"

    def _generate_tests(self, request: CodeGenerationRequest) -> str:
        """Generate test code"""
        if request.language == "python":
            return self._generate_python_tests(request)
        elif request.language == "javascript":
            return self._generate_javascript_tests(request)
        else:
            return f"// Tests for {request.language}"

    def _generate_python_tests(self, request: CodeGenerationRequest) -> str:
        """Generate Python tests"""
        return f'''"""
Tests for generated code
"""

import unittest
from unittest.mock import patch

class TestGeneratedCode(unittest.TestCase):
    """Test cases for generated code"""

    def test_main_function(self):
        """Test main function exists"""
        # Test that main function can be called without errors
        try:
            # Import the generated module
            import importlib.util
            spec = importlib.util.spec_from_file_location("generated_module", "generated_code.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Test main function exists
            self.assertTrue(hasattr(module, 'main'))
            self.assertTrue(callable(module.main))
            
        except Exception as e:
            self.fail(f"Failed to test main function: {e}")

    def test_framework_specific_functionality(self):
        """Test framework-specific features"""
        if "{request.framework}" == "flask":
            # Test Flask-specific functionality
            self.assertTrue(True)  # Placeholder for Flask tests
        elif "{request.framework}" == "pandas":
            # Test pandas functionality
            self.assertTrue(True)  # Placeholder for pandas tests
        else:
            # Test standard Python functionality
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
'''

    def _generate_javascript_tests(self, request: CodeGenerationRequest) -> str:
        """Generate JavaScript tests"""
        return f"""/**
 * Tests for generated code
 */

// Test framework setup with Jest
describe('Generated Code', () => {{
    it('should have main function', () => {{
        // Test that main function exists and is callable
        expect(typeof main).toBe('function');
    }});
    
    it('should execute without errors', () => {{
        // Test that main function executes without throwing
        expect(() => {{
            // Mock console.log to prevent output during tests
            const originalLog = console.log;
            console.log = jest.fn();
            
            try {{
                main();
            }} finally {{
                console.log = originalLog;
            }}
        }}).not.toThrow();
    }});
    
    it('should handle framework-specific functionality', () => {{
        if ("{request.framework}" === "express") {{
            // Test Express-specific functionality
            expect(true).toBe(true); // Placeholder for Express tests
        }} else if ("{request.framework}" === "react") {{
            // Test React-specific functionality
            expect(true).toBe(true); // Placeholder for React tests
        }} else {{
            // Test standard JavaScript functionality
            expect(true).toBe(true);
        }}
    }});
}});
"""

    def _generate_documentation(self, request: CodeGenerationRequest) -> str:
        """Generate documentation"""
        # Capitalize language name for display with special cases
        language_display = request.language.capitalize()
        if request.language == "javascript":
            language_display = "JavaScript"
        elif request.language == "typescript":
            language_display = "TypeScript"

        return f"""# {request.description}

## Overview
This code was generated by CodeCrafter for the following requirements:
- Language: {language_display}
- Framework: {request.framework or 'None'}
- Requirements: {', '.join(request.requirements) if request.requirements else 'None'}

## Usage
```{request.language}
# Example usage code here
```

## Dependencies
- TODO: List dependencies

## Testing
Run the tests using the appropriate test runner for {language_display}.
"""

    def _calculate_complexity(self, code: str) -> float:
        """Calculate code complexity"""
        # Simple complexity calculation based on lines and keywords
        lines = code.split("\n")
        complexity = len(lines) * 0.1

        # Add complexity for certain keywords
        complexity_keywords = ["if", "for", "while", "try", "except", "catch"]
        for keyword in complexity_keywords:
            complexity += code.count(keyword) * 0.5

        return round(complexity, 2)

    def _extract_dependencies(self, code: str, language: str) -> List[str]:
        """Extract dependencies from code"""
        dependencies = []

        if language == "python":
            import_lines = [
                line
                for line in code.split("\n")
                if line.strip().startswith("import") or line.strip().startswith("from")
            ]
            for line in import_lines:
                if "import" in line:
                    # Handle "import module" and "import module as alias"
                    if line.strip().startswith("import"):
                        parts = line.split("import")[1].strip()
                        if " as " in parts:
                            module = parts.split(" as ")[0].strip()
                        else:
                            module = parts.strip()
                        dependencies.append(module)
                    elif line.strip().startswith("from"):
                        # Handle "from module import item"
                        parts = line.split("from")[1].split("import")[0].strip()
                        dependencies.append(parts)

        elif language == "javascript":
            import_lines = [
                line
                for line in code.split("\n")
                if "require(" in line or "import" in line
            ]
            for line in import_lines:
                if "require(" in line:
                    dep = line.split("require(")[1].split(")")[0].strip("'\"")
                    dependencies.append(dep)

        return dependencies

    def _generate_usage_examples(self, code: str, language: str) -> List[str]:
        """Generate usage examples"""
        examples = []

        if language == "python":
            examples.append("python main.py")
            examples.append("from generated_code import main")
            examples.append("main()")

        elif language == "javascript":
            examples.append("node main.js")
            examples.append("const { main } = require('./main.js')")
            examples.append("main()")

        return examples

    def _read_code_file(self, file_path: str) -> str:
        """Read code file content"""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _analyze_complexity(self, code: str) -> float:
        """Analyze code complexity"""
        return self._calculate_complexity(code)

    def _analyze_maintainability(self, code: str) -> float:
        """Analyze code maintainability"""
        # Simple maintainability score (0-100)
        lines = code.split("\n")
        score = 100.0

        # Reduce score for long functions
        if len(lines) > 50:
            score -= 20

        # Reduce score for complex logic
        complexity = self._analyze_complexity(code)
        if complexity > 10:
            score -= 30

        return max(0.0, score)

    def _detect_code_smells(self, code: str) -> List[str]:
        """Detect code smells"""
        smells = []

        # Check for long functions
        lines = code.split("\n")
        if len(lines) > 50:
            smells.append("Long function detected (>50 lines)")

        # Check for magic numbers
        import re

        magic_numbers = re.findall(r"\b\d{3,}\b", code)
        if magic_numbers:
            smells.append(f"Magic numbers detected: {', '.join(set(magic_numbers))}")

        # Check for commented code
        if "#" in code and "TODO" in code:
            smells.append("Commented code or TODOs detected")

        return smells

    def _generate_suggestions(self, code: str, smells: List[str]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []

        if "Long function detected" in str(smells):
            suggestions.append(
                "Consider breaking down long functions into smaller, focused functions"
            )

        if "Magic numbers detected" in str(smells):
            suggestions.append("Replace magic numbers with named constants")

        if "Commented code or TODOs detected" in str(smells):
            suggestions.append("Remove commented code and implement TODO items")

        return suggestions

    def _check_security_issues(self, code: str) -> List[str]:
        """Check for security issues"""
        issues = []

        # Check for hardcoded secrets
        if "password" in code.lower() or "secret" in code.lower():
            issues.append("Potential hardcoded secrets detected")

        # Check for SQL injection patterns
        if "execute(" in code.lower() and "sql" in code.lower():
            issues.append("Potential SQL injection vulnerability")

        return issues

    def _check_performance_issues(self, code: str) -> List[str]:
        """Check for performance issues"""
        issues = []

        # Check for nested loops
        if code.count("for") > 1 or code.count("while") > 1:
            issues.append("Nested loops detected - consider optimization")

        # Check for large data structures
        if "list(" in code or "dict(" in code:
            issues.append("Large data structure creation detected")

        return issues

    def _calculate_documentation_coverage(self, code: str) -> float:
        """Calculate documentation coverage"""
        lines = code.split("\n")
        doc_lines = 0

        for line in lines:
            stripped = line.strip()
            if (
                stripped.startswith('"""')
                or stripped.startswith("'''")
                or stripped.startswith("#")
            ):
                doc_lines += 1

        if len(lines) == 0:
            return 0.0

        return round((doc_lines / len(lines)) * 100, 2)


# ============================================================================
