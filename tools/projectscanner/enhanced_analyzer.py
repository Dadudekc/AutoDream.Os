"""
Enhanced Project Scanner with Advanced Language Analysis
======================================================

Integrates advanced language analysis, caching, and agent categorization
from the provided scanner code into our existing modular system.
"""

import ast
import hashlib
import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

logger = logging.getLogger(__name__)

# Optional: If tree-sitter grammars are present for Rust/JS/TS
try:
    from tree_sitter import Language, Parser
except ImportError:
    Language = None
    Parser = None
    logger.warning("⚠️ tree-sitter not installed. Rust/JS/TS AST parsing will be partially disabled.")


class EnhancedLanguageAnalyzer:
    """Enhanced language analyzer with advanced AST parsing and route detection."""
    
    def __init__(self):
        """Initialize enhanced language analyzers and parsers."""
        self.rust_parser = self._init_tree_sitter_language("rust")
        self.js_parser = self._init_tree_sitter_language("javascript")
        self.analysis_cache = {}
        
    def _init_tree_sitter_language(self, lang_name: str) -> Optional[Parser]:
        """Initialize tree-sitter parser for given language."""
        if not Language or not Parser:
            logger.warning("⚠️ tree-sitter not installed. Rust/JS/TS AST parsing will be partially disabled.")
            return None

        grammar_paths = {
            "rust": "path/to/tree-sitter-rust.so",
            "javascript": "path/to/tree-sitter-javascript.so"
        }
        
        if lang_name not in grammar_paths:
            logger.warning(f"⚠️ No grammar path for {lang_name}. Skipping.")
            return None

        grammar_path = grammar_paths[lang_name]
        if not Path(grammar_path).exists():
            logger.warning(f"⚠️ {lang_name} grammar not found at {grammar_path}")
            return None

        try:
            lang_lib = Language(grammar_path, lang_name)
            parser = Parser()
            parser.set_language(lang_lib)
            return parser
        except Exception as e:
            logger.error(f"⚠️ Failed to initialize tree-sitter {lang_name} parser: {e}")
            return None

    def analyze_file(self, file_path: Path, source_code: str) -> Dict[str, Any]:
        """
        Analyze source code based on file extension with enhanced features.
        
        Returns:
            Dict with structure {language, functions, classes, routes, complexity, maturity, agent_type}
        """
        suffix = file_path.suffix.lower()
        
        if suffix == ".py":
            return self._analyze_python_enhanced(source_code, file_path)
        elif suffix == ".rs" and self.rust_parser:
            return self._analyze_rust_enhanced(source_code)
        elif suffix in [".js", ".ts"] and self.js_parser:
            return self._analyze_javascript_enhanced(source_code)
        else:
            return {
                "language": suffix,
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
                "maturity": "Unknown",
                "agent_type": "Unknown"
            }

    def _analyze_python_enhanced(self, source_code: str, file_path: Path) -> Dict[str, Any]:
        """Enhanced Python analysis with route detection and agent categorization."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
            return {
                "language": ".py",
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
                "maturity": "Syntax Error",
                "agent_type": "Error"
            }
        
        functions = []
        classes = {}
        routes = []
        imports = []
        decorators = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "args": len(node.args.args),
                    "decorators": [self._get_decorator_name(dec) for dec in node.decorator_list]
                }
                functions.append(func_info)

                # Enhanced route detection for Flask/FastAPI/Django
                route_info = self._extract_route_info(node)
                if route_info:
                    routes.extend(route_info)

            elif isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                
                # Extract base classes with full path resolution
                base_classes = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_classes.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        base_parts = []
                        attr_node = base
                        while isinstance(attr_node, ast.Attribute):
                            base_parts.append(attr_node.attr)
                            attr_node = attr_node.value
                        if isinstance(attr_node, ast.Name):
                            base_parts.append(attr_node.id)
                        base_classes.append(".".join(reversed(base_parts)))
                    else:
                        base_classes.append(None)
                
                # Enhanced class analysis
                classes[node.name] = {
                    "methods": method_names,
                    "docstring": docstring,
                    "base_classes": base_classes,
                    "line": node.lineno,
                    "maturity": self._assess_class_maturity(node, docstring, method_names),
                    "agent_type": self._categorize_agent_type(node.name, docstring, method_names)
                }

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = self._extract_import_info(node)
                imports.append(import_info)

        # Calculate enhanced complexity score
        complexity = self._calculate_complexity(functions, classes, routes)
        
        return {
            "language": ".py",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "imports": imports,
            "complexity": complexity,
            "file_size": len(source_code.splitlines()),
            "maturity": self._assess_file_maturity(classes, functions),
            "agent_type": self._categorize_file_type(file_path, classes, functions)
        }

    def _analyze_rust_enhanced(self, source_code: str) -> Dict[str, Any]:
        """Enhanced Rust analysis using tree-sitter if available."""
        if not self.rust_parser:
            return self._analyze_rust_fallback(source_code)

        tree = self.rust_parser.parse(bytes(source_code, "utf-8"))
        functions = []
        structs = {}
        impls = {}

        def _traverse(node):
            if node.type == "function_item":
                fn_name_node = node.child_by_field_name("name")
                if fn_name_node:
                    functions.append({
                        "name": fn_name_node.text.decode("utf-8"),
                        "line": node.start_point[0] + 1
                    })
            elif node.type == "struct_item":
                struct_name_node = node.child_by_field_name("name")
                if struct_name_node:
                    struct_name = struct_name_node.text.decode("utf-8")
                    structs[struct_name] = {
                        "line": node.start_point[0] + 1,
                        "fields": []
                    }
            elif node.type == "impl_item":
                impl_type_node = node.child_by_field_name("type")
                if impl_type_node:
                    impl_name = impl_type_node.text.decode("utf-8")
                    impls[impl_name] = []
                    for child in node.children:
                        if child.type == "function_item":
                            method_node = child.child_by_field_name("name")
                            if method_node:
                                impls[impl_name].append(method_node.text.decode("utf-8"))
            for child in node.children:
                _traverse(child)

        _traverse(tree.root_node)
        complexity = len(functions) + sum(len(m) for m in impls.values())
        
        return {
            "language": ".rs",
            "functions": functions,
            "structs": structs,
            "impls": impls,
            "routes": [],  # Rust typically doesn't have web routes in the same way
            "complexity": complexity,
            "file_size": len(source_code.splitlines()),
            "maturity": "Core Asset",  # Rust code is typically well-structured
            "agent_type": "SystemAgent"
        }

    def _analyze_rust_fallback(self, source_code: str) -> Dict[str, Any]:
        """Fallback Rust analysis using text patterns."""
        functions = []
        structs = {}
        
        lines = source_code.splitlines()
        for i, line in enumerate(lines, 1):
            if "fn " in line and not line.strip().startswith("//"):
                # Extract function name
                parts = line.split("fn ")
                if len(parts) > 1:
                    func_part = parts[1].split("(")[0].strip()
                    functions.append({"name": func_part, "line": i})
            elif "struct " in line and not line.strip().startswith("//"):
                parts = line.split("struct ")
                if len(parts) > 1:
                    struct_name = parts[1].split("{")[0].split(" ")[0].strip()
                    structs[struct_name] = {"line": i, "fields": []}
        
        return {
            "language": ".rs",
            "functions": functions,
            "structs": structs,
            "impls": {},
            "routes": [],
            "complexity": len(functions) + len(structs),
            "file_size": len(lines),
            "maturity": "Core Asset",
            "agent_type": "SystemAgent"
        }

    def _analyze_javascript_enhanced(self, source_code: str) -> Dict[str, Any]:
        """Enhanced JS/TS analysis using tree-sitter if available."""
        if not self.js_parser:
            return self._analyze_javascript_fallback(source_code)

        tree = self.js_parser.parse(bytes(source_code, "utf-8"))
        root = tree.root_node
        functions = []
        classes = {}
        routes = []

        def get_node_text(node):
            return node.text.decode("utf-8")

        def _traverse(node):
            if node.type == "function_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    functions.append({
                        "name": get_node_text(name_node),
                        "line": node.start_point[0] + 1
                    })
            elif node.type == "class_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    cls_name = get_node_text(name_node)
                    classes[cls_name] = {
                        "line": node.start_point[0] + 1,
                        "methods": []
                    }
            elif node.type == "call_expression":
                # Enhanced route detection for Express.js, etc.
                route_info = self._extract_js_route_info(node)
                if route_info:
                    routes.append(route_info)
            
            for child in node.children:
                _traverse(child)

        _traverse(root)
        complexity = len(functions) + sum(len(v.get("methods", [])) for v in classes.values())
        
        return {
            "language": ".js",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "complexity": complexity,
            "file_size": len(source_code.splitlines()),
            "maturity": "Prototype",  # JS code varies widely in maturity
            "agent_type": "WebAgent"
        }

    def _analyze_javascript_fallback(self, source_code: str) -> Dict[str, Any]:
        """Fallback JS analysis using text patterns."""
        functions = []
        classes = {}
        routes = []
        
        lines = source_code.splitlines()
        for i, line in enumerate(lines, 1):
            # Function detection
            if "function " in line:
                parts = line.split("function ")
                if len(parts) > 1:
                    func_name = parts[1].split("(")[0].strip()
                    functions.append({"name": func_name, "line": i})
            # Class detection
            elif "class " in line:
                parts = line.split("class ")
                if len(parts) > 1:
                    class_name = parts[1].split("{")[0].split(" ")[0].strip()
                    classes[class_name] = {"line": i, "methods": []}
            # Route detection (Express.js patterns)
            elif any(method in line for method in [".get(", ".post(", ".put(", ".delete(", ".patch("]):
                route_info = self._extract_route_from_line(line)
                if route_info:
                    routes.append(route_info)
        
        return {
            "language": ".js",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "complexity": len(functions) + len(classes),
            "file_size": len(lines),
            "maturity": "Prototype",
            "agent_type": "WebAgent"
        }

    # Helper methods for enhanced analysis
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Extract decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr
        return "unknown"

    def _extract_route_info(self, func_node: ast.FunctionDef) -> List[Dict[str, str]]:
        """Extract route information from function decorators."""
        routes = []
        
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    func_attr = decorator.func.attr.lower()
                    if func_attr in {"route", "get", "post", "put", "delete", "patch"}:
                        path_arg = "/unknown"
                        methods = [func_attr.upper()]
                        
                        # Extract path from arguments
                        if decorator.args:
                            arg0 = decorator.args[0]
                            if isinstance(arg0, ast.Str):
                                path_arg = arg0.s
                            elif isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                                path_arg = arg0.value
                        
                        # Extract methods from keywords
                        for kw in decorator.keywords:
                            if kw.arg == "methods" and isinstance(kw.value, ast.List):
                                extracted_methods = []
                                for elt in kw.value.elts:
                                    if isinstance(elt, ast.Str):
                                        extracted_methods.append(elt.s.upper())
                                    elif isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                        extracted_methods.append(elt.value.upper())
                                if extracted_methods:
                                    methods = extracted_methods
                        
                        for method in methods:
                            routes.append({
                                "function": func_node.name,
                                "method": method,
                                "path": path_arg,
                                "line": func_node.lineno
                            })
        
        return routes

    def _extract_import_info(self, node: ast.AST) -> Dict[str, Any]:
        """Extract import information from AST node."""
        if isinstance(node, ast.Import):
            return {
                "type": "import",
                "module": None,
                "names": [alias.name for alias in node.names],
                "line": node.lineno
            }
        elif isinstance(node, ast.ImportFrom):
            return {
                "type": "from_import",
                "module": node.module,
                "names": [alias.name for alias in node.names],
                "level": node.level,
                "line": node.lineno
            }
        return {}

    def _extract_js_route_info(self, node) -> Optional[Dict[str, str]]:
        """Extract route information from JavaScript call expressions."""
        if node.child_count >= 2:
            callee_node = node.child_by_field_name("function")
            args_node = node.child_by_field_name("arguments")
            
            if callee_node:
                callee_text = callee_node.text.decode("utf-8")
                parts = callee_text.split(".")
                
                if len(parts) == 2:
                    obj, method = parts
                    if method.lower() in {"get", "post", "put", "delete", "patch"}:
                        path_str = "/unknown"
                        if args_node and args_node.child_count > 0:
                            first_arg = args_node.child(0)
                            if first_arg.type == "string":
                                path_str = first_arg.text.decode("utf-8").strip('"\'')
                        
                        return {
                            "object": obj,
                            "method": method.upper(),
                            "path": path_str,
                            "line": node.start_point[0] + 1
                        }
        return None

    def _extract_route_from_line(self, line: str) -> Optional[Dict[str, str]]:
        """Extract route information from a JavaScript line of code."""
        import re
        
        # Pattern for Express.js routes: app.get('/path', ...)
        pattern = r'(\w+)\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]'
        match = re.search(pattern, line)
        
        if match:
            obj, method, path = match.groups()
            return {
                "object": obj,
                "method": method.upper(),
                "path": path,
                "line": 0  # Line number not available in fallback
            }
        return None

    def _calculate_complexity(self, functions: List[Dict], classes: Dict, routes: List[Dict]) -> int:
        """Calculate enhanced complexity score."""
        base_complexity = len(functions) + sum(len(c.get("methods", [])) for c in classes.values())
        
        # Add complexity for routes (API endpoints are typically complex)
        route_complexity = len(routes) * 2
        
        # Add complexity for decorators and imports
        decorator_complexity = sum(len(f.get("decorators", [])) for f in functions)
        
        return base_complexity + route_complexity + decorator_complexity

    def _assess_class_maturity(self, class_node: ast.ClassDef, docstring: str, methods: List[str]) -> str:
        """Assess class maturity level."""
        score = 0
        
        if docstring:
            score += 2
        if len(methods) > 3:
            score += 2
        if any(base for base in class_node.bases if not isinstance(base, ast.Name) or base.id not in ("object",)):
            score += 1
        if class_node.name and class_node.name[0].isupper():
            score += 1
        
        if score >= 5:
            return "Core Asset"
        elif score >= 3:
            return "Prototype"
        else:
            return "Kiddie Script"

    def _categorize_agent_type(self, class_name: str, docstring: str, methods: List[str]) -> str:
        """Categorize class as agent type."""
        doc = (docstring or "").lower()
        
        # Check for agent-specific methods
        if "run" in methods or "execute" in methods:
            return "ActionAgent"
        if "transform" in doc or "parse" in doc or "process" in doc:
            return "DataAgent"
        if any(m in methods for m in ["predict", "analyze", "classify"]):
            return "SignalAgent"
        if "communicate" in doc or "message" in doc or "send" in methods:
            return "CommunicationAgent"
        if "scan" in doc or "monitor" in doc or "check" in methods:
            return "MonitoringAgent"
        
        return "UtilityAgent"

    def _assess_file_maturity(self, classes: Dict, functions: List[Dict]) -> str:
        """Assess overall file maturity."""
        if not classes and not functions:
            return "Empty"
        
        total_methods = sum(len(c.get("methods", [])) for c in classes.values())
        total_functions = len(functions)
        
        if total_methods + total_functions > 10:
            return "Core Asset"
        elif total_methods + total_functions > 5:
            return "Prototype"
        else:
            return "Kiddie Script"

    def _categorize_file_type(self, file_path: Path, classes: Dict, functions: List[Dict]) -> str:
        """Categorize file type based on content and location."""
        path_str = str(file_path).lower()
        
        if "test" in path_str:
            return "TestAgent"
        elif "agent" in path_str:
            return "AgentCore"
        elif "service" in path_str:
            return "ServiceAgent"
        elif "tool" in path_str:
            return "ToolAgent"
        elif any(cls.get("agent_type") == "CommunicationAgent" for cls in classes.values()):
            return "CommunicationAgent"
        elif any(cls.get("agent_type") == "MonitoringAgent" for cls in classes.values()):
            return "MonitoringAgent"
        else:
            return "UtilityAgent"


class EnhancedCachingSystem:
    """Enhanced caching system with file movement detection and hash-based tracking."""
    
    def __init__(self, cache_file: str = "dependency_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache = self.load_cache()
        self.cache_lock = threading.Lock()
        
    def load_cache(self) -> Dict[str, Any]:
        """Load cache from disk."""
        if self.cache_file.exists():
            try:
                with self.cache_file.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Failed to load cache: {e}")
        return {}
    
    def save_cache(self):
        """Save cache to disk."""
        try:
            with self.cache_lock:
                with self.cache_file.open("w", encoding="utf-8") as f:
                    json.dump(self.cache, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")
    
    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with file_path.open("rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def is_file_cached(self, file_path: Path, relative_path: str) -> bool:
        """Check if file is cached and unchanged."""
        current_hash = self.get_file_hash(file_path)
        cached_hash = self.cache.get(relative_path, {}).get("hash")
        return cached_hash == current_hash
    
    def update_file_cache(self, file_path: Path, relative_path: str, analysis_result: Dict[str, Any]):
        """Update cache with new analysis result."""
        current_hash = self.get_file_hash(file_path)
        with self.cache_lock:
            self.cache[relative_path] = {
                "hash": current_hash,
                "last_analyzed": time.time(),
                "analysis": analysis_result
            }
    
    def detect_moved_files(self, current_files: Set[Path], project_root: Path) -> Dict[str, str]:
        """Detect files that have been moved by comparing hashes."""
        moved_files = {}
        current_hashes = {}
        
        # Calculate hashes for current files
        for file_path in current_files:
            file_hash = self.get_file_hash(file_path)
            if file_hash:
                current_hashes[file_hash] = str(file_path.relative_to(project_root))
        
        # Find matches in cache
        with self.cache_lock:
            for cached_path, cached_data in self.cache.items():
                cached_hash = cached_data.get("hash")
                if cached_hash and cached_hash in current_hashes:
                    new_path = current_hashes[cached_hash]
                    if cached_path != new_path:
                        moved_files[cached_path] = new_path
        
        return moved_files
    
    def cleanup_missing_files(self, current_files: Set[Path], project_root: Path):
        """Remove cache entries for files that no longer exist."""
        current_paths = {str(f.relative_to(project_root)) for f in current_files}
        
        with self.cache_lock:
            missing_files = [path for path in self.cache.keys() if path not in current_paths]
            for missing_file in missing_files:
                del self.cache[missing_file]
                logger.debug(f"Removed cache entry for missing file: {missing_file}")


class EnhancedReportGenerator:
    """Enhanced report generator with merging capabilities and agent categorization."""
    
    def __init__(self, project_root: Path, analysis: Dict[str, Dict[str, Any]]):
        self.project_root = project_root
        self.analysis = analysis
        self.output_dir = project_root / "analysis"
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_enhanced_reports(self):
        """Generate all enhanced reports with merging capabilities."""
        self.save_project_analysis()
        self.save_test_analysis()
        self.save_agent_analysis()
        self.save_architecture_overview()
        self.export_chatgpt_context()
    
    def save_project_analysis(self):
        """Save enhanced project analysis with merging."""
        report_path = self.project_root / "project_analysis.json"
        existing = self._load_existing_report(report_path)
        
        # Merge new analysis with existing
        merged = {**existing, **self.analysis}
        
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(merged, f, indent=4)
        
        logger.info(f"✅ Enhanced project analysis saved to {report_path}")
    
    def save_test_analysis(self):
        """Save test analysis with enhanced categorization."""
        test_report_path = self.project_root / "test_analysis.json"
        existing_tests = self._load_existing_report(test_report_path)
        
        # Separate test files
        test_files = {}
        for file_path, analysis in self.analysis.items():
            if "test" in file_path.lower() or "tests" in file_path.lower():
                test_files[file_path] = analysis
        
        merged_tests = {**existing_tests, **test_files}
        
        with test_report_path.open("w", encoding="utf-8") as f:
            json.dump(merged_tests, f, indent=4)
        
        logger.info(f"✅ Enhanced test analysis saved to {test_report_path}")
    
    def save_agent_analysis(self):
        """Save enhanced agent analysis with categorization."""
        agent_data = {
            "agent_categories": {},
            "maturity_distribution": {},
            "agent_types": {},
            "swarm_coordination": {
                "total_agents": 8,
                "active_agents": 8,
                "coordination_method": "PyAutoGUI automation",
                "physical_positions": {
                    "Monitor 1": [(-1269, 481), (-308, 480), (-1269, 1001), (-308, 1000)],
                    "Monitor 2": [(652, 421), (1612, 419), (920, 851), (1611, 941)]
                }
            }
        }
        
        # Categorize agents from analysis
        for file_path, analysis in self.analysis.items():
            if analysis.get("language") == ".py":
                for class_name, class_data in analysis.get("classes", {}).items():
                    agent_type = class_data.get("agent_type", "Unknown")
                    maturity = class_data.get("maturity", "Unknown")
                    
                    if agent_type not in agent_data["agent_categories"]:
                        agent_data["agent_categories"][agent_type] = []
                    
                    agent_data["agent_categories"][agent_type].append({
                        "class": class_name,
                        "file": file_path,
                        "maturity": maturity,
                        "methods": len(class_data.get("methods", [])),
                        "complexity": analysis.get("complexity", 0)
                    })
                    
                    # Update distributions
                    agent_data["maturity_distribution"][maturity] = agent_data["maturity_distribution"].get(maturity, 0) + 1
                    agent_data["agent_types"][agent_type] = agent_data["agent_types"].get(agent_type, 0) + 1
        
        agent_report_path = self.output_dir / "enhanced_agent_analysis.json"
        with agent_report_path.open("w", encoding="utf-8") as f:
            json.dump(agent_data, f, indent=4)
        
        logger.info(f"✅ Enhanced agent analysis saved to {agent_report_path}")
    
    def save_architecture_overview(self):
        """Save enhanced architecture overview."""
        architecture_data = {
            "system_architecture": {
                "pattern": "Enhanced Modular Agent System with Swarm Intelligence",
                "components": [
                    "Enhanced Project Scanner",
                    "Agent Registry with Categorization",
                    "PyAutoGUI Communication Services",
                    "V2 Compliance Engine",
                    "Advanced Language Analysis",
                    "Intelligent Caching System"
                ],
                "enhancements": [
                    "Tree-sitter AST parsing for multiple languages",
                    "Advanced route detection for web frameworks",
                    "Agent maturity and type categorization",
                    "File movement detection and cache optimization",
                    "Enhanced complexity analysis",
                    "Automatic __init__.py generation"
                ]
            },
            "quality_metrics": {
                "total_files_analyzed": len(self.analysis),
                "languages_supported": list(set(a.get("language", "unknown") for a in self.analysis.values())),
                "average_complexity": sum(a.get("complexity", 0) for a in self.analysis.values()) / max(len(self.analysis), 1),
                "agent_distribution": self._calculate_agent_distribution()
            },
            "v2_compliance": {
                "compliant_files": sum(1 for a in self.analysis.values() if a.get("file_size", 0) <= 400),
                "violation_files": sum(1 for a in self.analysis.values() if a.get("file_size", 0) > 400),
                "compliance_rate": 0.0  # Will be calculated
            }
        }
        
        # Calculate compliance rate
        total_files = len(self.analysis)
        if total_files > 0:
            compliant = architecture_data["v2_compliance"]["compliant_files"]
            architecture_data["v2_compliance"]["compliance_rate"] = (compliant / total_files) * 100
        
        arch_report_path = self.output_dir / "enhanced_architecture_overview.json"
        with arch_report_path.open("w", encoding="utf-8") as f:
            json.dump(architecture_data, f, indent=4)
        
        logger.info(f"✅ Enhanced architecture overview saved to {arch_report_path}")
    
    def export_chatgpt_context(self):
        """Export enhanced ChatGPT context with agent categorization."""
        context_path = self.project_root / "chatgpt_project_context.json"
        existing_context = self._load_existing_report(context_path)
        
        enhanced_context = {
            "project_root": str(self.project_root),
            "scan_timestamp": time.time(),
            "enhanced_features": [
                "Advanced language analysis with tree-sitter",
                "Agent categorization and maturity assessment",
                "Enhanced route detection",
                "Intelligent caching with file movement detection",
                "V2 compliance monitoring",
                "Swarm coordination analysis"
            ],
            "analysis_summary": {
                "total_files": len(self.analysis),
                "languages": list(set(a.get("language", "unknown") for a in self.analysis.values())),
                "total_complexity": sum(a.get("complexity", 0) for a in self.analysis.values()),
                "agent_types": self._calculate_agent_distribution(),
                "maturity_levels": self._calculate_maturity_distribution()
            },
            "swarm_intelligence": {
                "coordination_method": "PyAutoGUI automation across dual monitors",
                "agent_positions": "8 agents positioned at specific pixel coordinates",
                "communication_protocol": "Real-time agent-to-agent messaging",
                "achievements": ["8-agent debate coordination", "Multi-monitor architecture", "Physical swarm automation"]
            },
            "analysis_details": self.analysis
        }
        
        # Merge with existing context
        merged_context = {**existing_context, **enhanced_context}
        
        with context_path.open("w", encoding="utf-8") as f:
            json.dump(merged_context, f, indent=4)
        
        logger.info(f"✅ Enhanced ChatGPT context exported to {context_path}")
    
    def generate_init_files(self, overwrite: bool = True):
        """Generate __init__.py files for Python packages."""
        from collections import defaultdict
        
        package_modules = defaultdict(list)
        
        for rel_path in self.analysis.keys():
            if rel_path.endswith(".py") and not rel_path.endswith("__init__.py"):
                file_path = Path(rel_path)
                package_dir = file_path.parent
                module_name = file_path.stem
                package_modules[str(package_dir)].append(module_name)
        
        for package, modules in package_modules.items():
            package_path = self.project_root / package
            init_file = package_path / "__init__.py"
            package_path.mkdir(parents=True, exist_ok=True)
            
            if overwrite or not init_file.exists():
                lines = [
                    "# AUTO-GENERATED __init__.py",
                    "# Enhanced Project Scanner - DO NOT EDIT MANUALLY\n"
                ]
                
                for module in sorted(modules):
                    lines.append(f"from . import {module}")
                
                lines.extend([
                    "",
                    "__all__ = ["
                ])
                
                for module in sorted(modules):
                    lines.append(f"    '{module}',")
                
                lines.append("]\n")
                
                content = "\n".join(lines)
                
                with init_file.open("w", encoding="utf-8") as f:
                    f.write(content)
                
                logger.info(f"✅ Generated enhanced __init__.py in {package_path}")
    
    def _load_existing_report(self, report_path: Path) -> Dict[str, Any]:
        """Load existing report to preserve data during merging."""
        if report_path.exists():
            try:
                with report_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading existing report {report_path}: {e}")
        return {}
    
    def _calculate_agent_distribution(self) -> Dict[str, int]:
        """Calculate distribution of agent types."""
        distribution = {}
        
        for analysis in self.analysis.values():
            if analysis.get("language") == ".py":
                for class_data in analysis.get("classes", {}).values():
                    agent_type = class_data.get("agent_type", "Unknown")
                    distribution[agent_type] = distribution.get(agent_type, 0) + 1
        
        return distribution
    
    def _calculate_maturity_distribution(self) -> Dict[str, int]:
        """Calculate distribution of maturity levels."""
        distribution = {}
        
        for analysis in self.analysis.values():
            if analysis.get("language") == ".py":
                for class_data in analysis.get("classes", {}).values():
                    maturity = class_data.get("maturity", "Unknown")
                    distribution[maturity] = distribution.get(maturity, 0) + 1
        
        return distribution


