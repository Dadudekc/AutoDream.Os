#!/usr/bin/env python3
"""
Comprehensive DRY Violation Analyzer
===================================

Analyzes all 572 Python files for DRY violations and provides detailed reporting.

Author: Agent-5 (Business Intelligence Specialist)
Mission: Complete DRY Violation Elimination
Status: COMPREHENSIVE ANALYSIS
"""


class ComprehensiveDRYAnalyzer:
    """Comprehensive analyzer for all DRY violations across the entire codebase."""
    
    def __init__(self):
        self.project_root = get_unified_utility().Path(__file__).resolve().parents[3]
        self.python_files = []
        self.duplicate_patterns = defaultdict(list)
        self.function_signatures = defaultdict(list)
        self.class_definitions = defaultdict(list)
        self.import_patterns = defaultdict(list)
        self.configuration_patterns = defaultdict(list)
        self.validation_patterns = defaultdict(list)
        self.logging_patterns = defaultdict(list)
        self.utility_patterns = defaultdict(list)
        
    def analyze_all_files(self) -> Dict[str, Any]:
        """Analyze all Python files in the project."""
        get_logger(__name__).info("🔍 Starting comprehensive DRY analysis of all Python files...")
        
        # Find all Python files
        self._find_all_python_files()
        get_logger(__name__).info(f"📁 Found {len(self.python_files)} Python files to analyze")
        
        # Analyze each file
        for file_path in self.python_files:
            self._analyze_file(file_path)
        
        # Generate comprehensive report
        return self._generate_comprehensive_report()
    
    def _find_all_python_files(self):
        """Find all Python files in the project."""
        for root, dirs, files in os.walk(self.project_root):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in {
                '__pycache__', '.git', '.pytest_cache', 'node_modules', 
                '.venv', 'venv', 'env', '.env', 'build', 'dist'
            }]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = get_unified_utility().Path(root) / file
                    self.python_files.append(file_path)
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file for DRY violations."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for function and class analysis
            try:
                tree = ast.parse(content)
                self._analyze_ast(file_path, tree)
            except SyntaxError:
                # Handle files with syntax errors
                pass
            
            # Analyze patterns in content
            self._analyze_content_patterns(file_path, content)
            
        except Exception as e:
            get_logger(__name__).info(f"⚠️  Error analyzing {file_path}: {e}")
    
    def _analyze_ast(self, file_path: Path, tree: ast.AST):
        """Analyze AST for function and class definitions."""
        for node in ast.walk(tree):
            if get_unified_validator().validate_type(node, ast.FunctionDef):
                # Extract function signature
                signature = self._get_function_signature(node)
                self.function_signatures[signature].append(str(file_path))
                
            elif get_unified_validator().validate_type(node, ast.ClassDef):
                # Extract class definition
                class_info = self._get_class_info(node)
                self.class_definitions[class_info].append(str(file_path))
    
    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """Extract function signature for comparison."""
        args = [arg.arg for arg in node.args.args]
        return f"{node.name}({', '.join(args)})"
    
    def _get_class_info(self, node: ast.ClassDef) -> str:
        """Extract class information for comparison."""
        bases = [base.id if get_unified_validator().validate_hasattr(base, 'id') else str(base) for base in node.bases]
        return f"{node.name}({', '.join(bases)})"
    
    def _analyze_content_patterns(self, file_path: Path, content: str):
        """Analyze content for duplicate patterns."""
        # Import patterns
        self._analyze_import_patterns(file_path, content)
        
        # Configuration patterns
        self._analyze_configuration_patterns(file_path, content)
        
        # Validation patterns
        self._analyze_validation_patterns(file_path, content)
        
        # Logging patterns
        self._analyze_logging_patterns(file_path, content)
        
        # Utility patterns
        self._analyze_utility_patterns(file_path, content)
    
    def _analyze_import_patterns(self, file_path: Path, content: str):
        """Analyze import patterns."""
        import_lines = re.findall(r'^(from|import)\s+.*$', content, re.MULTILINE)
        for import_line in import_lines:
            self.import_patterns[import_line.strip()].append(str(file_path))
    
    def _analyze_configuration_patterns(self, file_path: Path, content: str):
        """Analyze configuration-related patterns."""
        config_patterns = [
            r'def\s+get_config\(',
            r'def\s+load_config\(',
            r'def\s+save_config\(',
            r'def\s+validate_config\(',
            r'class\s+.*Config',
            r'CONFIG\s*=',
            r'config\s*=\s*{',
            r'os\.environ\.get\(',
            r'os\.getenv\(',
        ]
        
        for pattern in config_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                self.configuration_patterns[pattern].append(str(file_path))
    
    def _analyze_validation_patterns(self, file_path: Path, content: str):
        """Analyze validation-related patterns."""
        validation_patterns = [
            r'def\s+validate_',
            r'def\s+get_unified_validator().check_',
            r'def\s+get_unified_validator().verify_',
            r'if\s+not\s+.*:',
            r'raise\s+ValueError',
            r'raise\s+TypeError',
            r'isinstance\(',
            r'hasattr\(',
            r'getattr\(',
        ]
        
        for pattern in validation_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                self.validation_patterns[pattern].append(str(file_path))
    
    def _analyze_logging_patterns(self, file_path: Path, content: str):
        """Analyze logging-related patterns."""
        logging_patterns = [
            r'logger\.(info|debug|warning|error|critical)',
            r'logging\.(info|debug|warning|error|critical)',
            r'print\(',
            r'log\.(info|debug|warning|error|critical)',
            r'def\s+log_',
            r'class\s+.*Logger',
        ]
        
        for pattern in logging_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                self.logging_patterns[pattern].append(str(file_path))
    
    def _analyze_utility_patterns(self, file_path: Path, content: str):
        """Analyze utility function patterns."""
        utility_patterns = [
            r'def\s+get_project_root\(',
            r'def\s+resolve_path\(',
            r'def\s+format_string\(',
            r'def\s+get_unified_utility().sanitize_',
            r'def\s+get_unified_utility().clean_',
            r'def\s+get_unified_utility().normalize_',
            r'def\s+get_unified_utility().parse_',
            r'def\s+get_unified_utility().convert_',
            r'Path\(',
            r'os\.path\.',
        ]
        
        for pattern in utility_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                self.utility_patterns[pattern].append(str(file_path))
    
    def _generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive DRY violation report."""
        report = {
            "total_files_analyzed": len(self.python_files),
            "duplicate_functions": self._analyze_duplicate_functions(),
            "duplicate_classes": self._analyze_duplicate_classes(),
            "duplicate_imports": self._analyze_duplicate_imports(),
            "configuration_duplicates": self._analyze_configuration_duplicates(),
            "validation_duplicates": self._analyze_validation_duplicates(),
            "logging_duplicates": self._analyze_logging_duplicates(),
            "utility_duplicates": self._analyze_utility_duplicates(),
            "priority_violations": self._identify_priority_violations(),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _analyze_duplicate_functions(self) -> Dict[str, Any]:
        """Analyze duplicate function definitions."""
        duplicates = {}
        for signature, files in self.function_signatures.items():
            if len(files) > 1:
                duplicates[signature] = {
                    "count": len(files),
                    "files": files,
                    "severity": "HIGH" if len(files) > 3 else "MEDIUM"
                }
        
        return {
            "total_duplicates": len(duplicates),
            "high_severity": len([d for d in duplicates.values() if d["severity"] == "HIGH"]),
            "medium_severity": len([d for d in duplicates.values() if d["severity"] == "MEDIUM"]),
            "details": duplicates
        }
    
    def _analyze_duplicate_classes(self) -> Dict[str, Any]:
        """Analyze duplicate class definitions."""
        duplicates = {}
        for class_info, files in self.class_definitions.items():
            if len(files) > 1:
                duplicates[class_info] = {
                    "count": len(files),
                    "files": files,
                    "severity": "HIGH" if len(files) > 2 else "MEDIUM"
                }
        
        return {
            "total_duplicates": len(duplicates),
            "high_severity": len([d for d in duplicates.values() if d["severity"] == "HIGH"]),
            "medium_severity": len([d for d in duplicates.values() if d["severity"] == "MEDIUM"]),
            "details": duplicates
        }
    
    def _analyze_duplicate_imports(self) -> Dict[str, Any]:
        """Analyze duplicate import patterns."""
        duplicates = {}
        for import_line, files in self.import_patterns.items():
            if len(files) > 5:  # More than 5 files using same import
                duplicates[import_line] = {
                    "count": len(files),
                    "files": files[:10],  # Limit to first 10 files
                    "severity": "HIGH" if len(files) > 20 else "MEDIUM"
                }
        
        return {
            "total_duplicates": len(duplicates),
            "high_severity": len([d for d in duplicates.values() if d["severity"] == "HIGH"]),
            "medium_severity": len([d for d in duplicates.values() if d["severity"] == "MEDIUM"]),
            "details": duplicates
        }
    
    def _analyze_configuration_duplicates(self) -> Dict[str, Any]:
        """Analyze configuration pattern duplicates."""
        duplicates = {}
        for pattern, files in self.configuration_patterns.items():
            if len(files) > 2:
                duplicates[pattern] = {
                    "count": len(files),
                    "files": files,
                    "severity": "HIGH" if len(files) > 5 else "MEDIUM"
                }
        
        return {
            "total_duplicates": len(duplicates),
            "high_severity": len([d for d in duplicates.values() if d["severity"] == "HIGH"]),
            "medium_severity": len([d for d in duplicates.values() if d["severity"] == "MEDIUM"]),
            "details": duplicates
        }
    
    def _analyze_validation_duplicates(self) -> Dict[str, Any]:
        """Analyze validation pattern duplicates."""
        duplicates = {}
        for pattern, files in self.validation_patterns.items():
            if len(files) > 3:
                duplicates[pattern] = {
                    "count": len(files),
                    "files": files,
                    "severity": "HIGH" if len(files) > 10 else "MEDIUM"
                }
        
        return {
            "total_duplicates": len(duplicates),
            "high_severity": len([d for d in duplicates.values() if d["severity"] == "HIGH"]),
            "medium_severity": len([d for d in duplicates.values() if d["severity"] == "MEDIUM"]),
            "details": duplicates
        }
    
    def _analyze_logging_duplicates(self) -> Dict[str, Any]:
        """Analyze logging pattern duplicates."""
        duplicates = {}
        for pattern, files in self.logging_patterns.items():
            if len(files) > 5:
                duplicates[pattern] = {
                    "count": len(files),
                    "files": files,
                    "severity": "HIGH" if len(files) > 20 else "MEDIUM"
                }
        
        return {
            "total_duplicates": len(duplicates),
            "high_severity": len([d for d in duplicates.values() if d["severity"] == "HIGH"]),
            "medium_severity": len([d for d in duplicates.values() if d["severity"] == "MEDIUM"]),
            "details": duplicates
        }
    
    def _analyze_utility_duplicates(self) -> Dict[str, Any]:
        """Analyze utility pattern duplicates."""
        duplicates = {}
        for pattern, files in self.utility_patterns.items():
            if len(files) > 3:
                duplicates[pattern] = {
                    "count": len(files),
                    "files": files,
                    "severity": "HIGH" if len(files) > 10 else "MEDIUM"
                }
        
        return {
            "total_duplicates": len(duplicates),
            "high_severity": len([d for d in duplicates.values() if d["severity"] == "HIGH"]),
            "medium_severity": len([d for d in duplicates.values() if d["severity"] == "MEDIUM"]),
            "details": duplicates
        }
    
    def _identify_priority_violations(self) -> List[Dict[str, Any]]:
        """Identify highest priority violations to fix first."""
        priorities = []
        
        # High priority: Functions with many duplicates
        for signature, files in self.function_signatures.items():
            if len(files) > 5:
                priorities.append({
                    "type": "function",
                    "pattern": signature,
                    "count": len(files),
                    "files": files,
                    "priority": "CRITICAL"
                })
        
        # High priority: Configuration patterns
        for pattern, files in self.configuration_patterns.items():
            if len(files) > 10:
                priorities.append({
                    "type": "configuration",
                    "pattern": pattern,
                    "count": len(files),
                    "files": files,
                    "priority": "HIGH"
                })
        
        # Sort by count (descending)
        priorities.sort(key=lambda x: x["count"], reverse=True)
        
        return priorities[:20]  # Top 20 priorities
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for DRY elimination."""
        recommendations = [
            "1. **CRITICAL**: Consolidate duplicate function definitions into unified utility modules",
            "2. **HIGH**: Migrate all configuration patterns to unified configuration system",
            "3. **HIGH**: Consolidate validation patterns into unified validation system",
            "4. **HIGH**: Standardize logging patterns using unified logging system",
            "5. **MEDIUM**: Create shared utility modules for common path and string operations",
            "6. **MEDIUM**: Implement dependency injection for shared services",
            "7. **LOW**: Standardize import patterns across modules",
            "8. **LOW**: Create base classes for common functionality"
        ]
        
        return recommendations

def analyze_comprehensive_dry_violations() -> Dict[str, Any]:
    """Main function to analyze all DRY violations."""
    analyzer = ComprehensiveDRYAnalyzer()
    return analyzer.analyze_all_files()

if __name__ == "__main__":
    results = analyze_comprehensive_dry_violations()
    get_logger(__name__).info(f"\n📊 COMPREHENSIVE DRY ANALYSIS COMPLETE")
    get_logger(__name__).info(f"📁 Total files analyzed: {results['total_files_analyzed']}")
    get_logger(__name__).info(f"🔧 Duplicate functions: {results['duplicate_functions']['total_duplicates']}")
    get_logger(__name__).info(f"🏗️  Duplicate classes: {results['duplicate_classes']['total_duplicates']}")
    get_logger(__name__).info(f"📦 Duplicate imports: {results['duplicate_imports']['total_duplicates']}")
    get_logger(__name__).info(f"⚙️  Configuration duplicates: {results['configuration_duplicates']['total_duplicates']}")
    get_logger(__name__).info(f"✅ Validation duplicates: {results['validation_duplicates']['total_duplicates']}")
    get_logger(__name__).info(f"📝 Logging duplicates: {results['logging_duplicates']['total_duplicates']}")
    get_logger(__name__).info(f"🛠️  Utility duplicates: {results['utility_duplicates']['total_duplicates']}")
    get_logger(__name__).info(f"🎯 Priority violations: {len(results['priority_violations'])}")
