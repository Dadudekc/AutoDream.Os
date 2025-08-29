"""
Code Parsing Utilities - Unified Validation Framework

Provides utilities for parsing source code into structures used by the
validation framework.
"""

import ast


class CodeParser:
    """Parses source code for further validation"""

    def parse_python(self, content: str) -> ast.AST:
        """Parse Python source code into an AST.

        Args:
            content: Python source code as a string.

        Returns:
            ast.AST: Parsed abstract syntax tree.

        Raises:
            SyntaxError: If the content cannot be parsed as Python.
        """
        return ast.parse(content)
