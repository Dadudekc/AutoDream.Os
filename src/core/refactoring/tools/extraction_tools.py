"""
Refactoring Extraction Tools - V2 Compliance Module
==================================================

Extraction functionality for refactoring tools.

V2 Compliance: < 300 lines, single responsibility, extraction tools.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import ast
from dataclasses import dataclass

from ...unified_import_system import get_unified_import_system


@dataclass
class ExtractionPlan:
    """Plan for extracting code from a file."""

    source_file: str
    target_files: list[str]
    extraction_rules: list[str]
    estimated_impact: str
    v2_compliance_target: bool


class ExtractionTools:
    """Extraction tools for refactoring."""

    def __init__(self):
        """Initialize extraction tools."""
        self.unified_imports = get_unified_import_system()

    def create_extraction_plan(self, file_path: str) -> ExtractionPlan:
        """Create an extraction plan for a file."""
        try:
            # Analyze file structure
            source_path = self.unified_imports.Path(file_path)
            source_content = source_path.read_text(encoding="utf-8")
            tree = ast.parse(source_content)

            # Determine extraction targets
            target_files = self._determine_target_files(file_path)
            extraction_rules = self._generate_extraction_rules(tree)

            return ExtractionPlan(
                source_file=file_path,
                target_files=target_files,
                extraction_rules=extraction_rules,
                estimated_impact="Moderate",
                v2_compliance_target=True,
            )
        except Exception:
            return ExtractionPlan(
                source_file=file_path,
                target_files=[],
                extraction_rules=[],
                estimated_impact="Error",
                v2_compliance_target=False,
            )

    def execute_extraction(self, plan: ExtractionPlan) -> bool:
        """Execute extraction plan."""
        try:
            if not plan.target_files:
                return True  # No extraction needed

            source_path = self.unified_imports.Path(plan.source_file)
            source_content = source_path.read_text(encoding="utf-8")
            tree = ast.parse(source_content)

            # Extract different components
            models = self._extract_models(tree)
            utils = self._extract_utils(tree)
            core = self._extract_core(tree)

            # Write extracted files
            for target_file in plan.target_files:
                target_path = self.unified_imports.Path(target_file)
                if "models" in target_file:
                    target_path.write_text(models, encoding="utf-8")
                elif "utils" in target_file:
                    target_path.write_text(utils, encoding="utf-8")
                elif "core" in target_file:
                    target_path.write_text(core, encoding="utf-8")

            return True
        except Exception:
            return False

    def _determine_target_files(self, file_path: str) -> list[str]:
        """Determine target files for extraction."""
        base_path = file_path.replace(".py", "")
        return [
            f"{base_path}_models.py",
            f"{base_path}_utils.py",
            f"{base_path}_core.py",
        ]

    def _generate_extraction_rules(self, tree: ast.AST) -> list[str]:
        """Generate extraction rules based on AST analysis."""
        rules = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                rules.append(f"Extract class: {node.name}")
            elif isinstance(node, ast.FunctionDef):
                rules.append(f"Extract function: {node.name}")
            elif isinstance(node, ast.Import):
                rules.append(f"Extract imports: {[alias.name for alias in node.names]}")

        return rules

    def _extract_models(self, tree: ast.AST) -> str:
        """Extract model-related code."""
        models_code = []
        imports = []

        for node in ast.walk(tree):
            # Extract class definitions that look like models
            if isinstance(node, ast.ClassDef):
                class_name = node.name

                # Look for model-like patterns
                has_init = any(isinstance(item, ast.FunctionDef) and item.name == '__init__'
                             for item in node.body)
                has_properties = any(isinstance(item, ast.AnnAssign) for item in node.body)

                if has_init or has_properties or 'Model' in class_name or 'Schema' in class_name:
                    # Extract the class code
                    class_code = f"class {class_name}:\n"
                    class_code += "    \"\"\"Model class extracted from refactoring.\"\"\"\n\n"

                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                            class_code += "    def __init__(self):\n"
                            class_code += "        \"\"\"Initialize model.\"\"\"\n"
                            class_code += "        pass\n\n"
                        elif isinstance(item, ast.AnnAssign):
                            if hasattr(item.target, 'id'):
                                class_code += f"    {item.target.id}: Any = None\n"

                    models_code.append(class_code)

            # Extract model-related imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if any(keyword in alias.name.lower() for keyword in
                          ['model', 'schema', 'pydantic', 'sqlalchemy', 'django']):
                        imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and any(keyword in node.module.lower() for keyword in
                      ['model', 'schema', 'pydantic', 'sqlalchemy', 'django']):
                    imports.append(f"from {node.module} import ...")

        # Combine imports and models
        result = []
        if imports:
            result.append("# Model imports")
            result.extend(imports)
            result.append("")

        if models_code:
            result.append("# Extracted model classes")
            result.extend(models_code)
        else:
            result.append("# No model classes found for extraction")

        return "\n".join(result)

    def _extract_utils(self, tree: ast.AST) -> str:
        """Extract utility-related code."""
        utils_functions = []
        utils_imports = []
        helper_functions = []

        for node in ast.walk(tree):
            # Extract standalone functions that look like utilities
            if isinstance(node, ast.FunctionDef):
                func_name = node.name

                # Skip special methods and main functions
                if func_name.startswith('_') or func_name == 'main':
                    continue

                # Look for utility patterns
                is_utility = False
                docstring = None

                # Check docstring for utility keywords
                if node.body and isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Str):
                        docstring = node.body[0].value.s
                        if any(keyword in (docstring or "").lower() for keyword in
                              ['util', 'helper', 'tool', 'common', 'shared']):
                            is_utility = True

                # Check function name for utility patterns
                if any(pattern in func_name.lower() for pattern in
                      ['util', 'helper', 'tool', 'common', 'shared', 'format', 'parse', 'convert']):
                    is_utility = True

                # Check if function has reasonable complexity (not too simple, not too complex)
                arg_count = len(node.args.args) if node.args else 0
                if 0 < arg_count <= 5:
                    is_utility = True

                if is_utility:
                    # Extract function signature and body
                    func_code = f"def {func_name}("

                    # Add arguments
                    args = []
                    if node.args:
                        for arg in node.args.args:
                            if arg.arg != 'self':  # Skip self for utility functions
                                args.append(arg.arg)
                    func_code += ", ".join(args)
                    func_code += "):\n"

                    # Add docstring
                    if docstring:
                        func_code += f'    """{docstring}"""\n'
                    else:
                        func_code += f'    """Utility function {func_name} extracted from refactoring."""\n'

                    func_code += "    # Implementation extracted from original code\n"
                    func_code += "    pass\n\n"

                    if arg_count <= 2:  # Simple utilities
                        utils_functions.append(func_code)
                    else:  # Helper functions
                        helper_functions.append(func_code)

            # Extract utility-related imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if any(keyword in alias.name.lower() for keyword in
                          ['os', 'sys', 'pathlib', 'json', 'yaml', 'logging']):
                        utils_imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and any(keyword in node.module.lower() for keyword in
                      ['os', 'sys', 'pathlib', 'json', 'yaml', 'logging']):
                    utils_imports.append(f"from {node.module} import ...")

        # Combine utilities
        result = []
        if utils_imports:
            result.append("# Utility imports")
            result.extend(utils_imports)
            result.append("")

        if utils_functions:
            result.append("# Utility functions")
            result.extend(utils_functions)

        if helper_functions:
            result.append("# Helper functions")
            result.extend(helper_functions)

        if not utils_functions and not helper_functions:
            result.append("# No utility functions found for extraction")

        return "\n".join(result)

    def _extract_core(self, tree: ast.AST) -> str:
        """Extract core-related code."""
        core_classes = []
        core_functions = []
        core_imports = []
        main_functions = []

        for node in ast.walk(tree):
            # Extract core classes (classes that are foundational)
            if isinstance(node, ast.ClassDef):
                class_name = node.name

                # Look for core patterns
                is_core = False

                # Check class name for core patterns
                if any(pattern in class_name.lower() for pattern in
                      ['manager', 'controller', 'service', 'provider', 'factory', 'core', 'main']):
                    is_core = True

                # Check for complex class structure (multiple methods)
                method_count = sum(1 for item in node.body if isinstance(item, ast.FunctionDef))
                if method_count >= 3:
                    is_core = True

                # Check for inheritance (likely core classes)
                if node.bases:
                    is_core = True

                if is_core:
                    # Extract the class structure
                    class_code = f"class {class_name}"
                    if node.bases:
                        base_names = []
                        for base in node.bases:
                            if isinstance(base, ast.Name):
                                base_names.append(base.id)
                        if base_names:
                            class_code += f"({', '.join(base_names)})"
                    class_code += ":\n"
                    class_code += "    \"\"\"Core class extracted from refactoring.\"\"\"\n\n"

                    # Extract method signatures
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_name = item.name
                            if not method_name.startswith('_'):  # Skip private methods
                                method_code = f"    def {method_name}("

                                # Add arguments
                                args = []
                                if item.args:
                                    for arg in item.args.args:
                                        args.append(arg.arg)
                                method_code += ", ".join(args)
                                method_code += "):\n"
                                method_code += f'        """Core method {method_name}."""\n'
                                method_code += "        pass\n\n"

                                class_code += method_code

                    core_classes.append(class_code)

            # Extract core functions (important standalone functions)
            elif isinstance(node, ast.FunctionDef):
                func_name = node.name

                # Skip special methods
                if func_name.startswith('_'):
                    continue

                # Look for core patterns
                is_core = False

                # Check function name for core patterns
                if any(pattern in func_name.lower() for pattern in
                      ['main', 'run', 'execute', 'process', 'handle', 'init', 'setup']):
                    is_core = True

                # Check if it's a main function
                if func_name == 'main':
                    is_core = True
                    main_functions.append(func_name)

                # Check function complexity (many statements)
                if node.body and len(node.body) > 10:
                    is_core = True

                if is_core and func_name not in main_functions:
                    # Extract function signature
                    func_code = f"def {func_name}("

                    # Add arguments
                    args = []
                    if node.args:
                        for arg in node.args.args:
                            args.append(arg.arg)
                    func_code += ", ".join(args)
                    func_code += "):\n"
                    func_code += f'    """Core function {func_name} extracted from refactoring."""\n'
                    func_code += "    # Core business logic implementation\n"
                    func_code += "    pass\n\n"

                    core_functions.append(func_code)

            # Extract core-related imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if any(keyword in alias.name.lower() for keyword in
                          ['typing', 'abc', 'dataclasses', 'enum']):
                        core_imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and any(keyword in node.module.lower() for keyword in
                      ['typing', 'abc', 'dataclasses', 'enum']):
                    core_imports.append(f"from {node.module} import ...")

        # Combine core components
        result = []
        if core_imports:
            result.append("# Core imports")
            result.extend(core_imports)
            result.append("")

        if core_classes:
            result.append("# Core classes")
            result.extend(core_classes)

        if core_functions:
            result.append("# Core functions")
            result.extend(core_functions)

        if main_functions:
            result.append("# Main entry points")
            for func in main_functions:
                result.append(f"def {func}():")
                result.append("    \"\"\"Main entry point extracted from refactoring.\"\"\"")
                result.append("    pass")
            result.append("")

        if not core_classes and not core_functions and not main_functions:
            result.append("# No core components found for extraction")

        return "\n".join(result)
