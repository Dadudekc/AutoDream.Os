#!/usr/bin/env python3
"""
Advanced DRY Violation Analyzer
===============================

Identifies additional DRY violations and bloat reduction opportunities.

Author: Agent-5 (Business Intelligence Specialist)
Mission: Further DRY Violation Elimination
Status: ADVANCED ANALYSIS
"""


class AdvancedDRYAnalyzer:
    """Advanced analyzer for identifying additional DRY violations."""
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.python_files = []
        self.advanced_patterns = defaultdict(list)
        self.bloat_opportunities = []
        
    def analyze_advanced_dry_violations(self) -> Dict[str, Any]:
        """Analyze advanced DRY violations and bloat opportunities."""
        print("🔍 Starting advanced DRY analysis for further reduction opportunities...")
        
        # Find project Python files
        self._find_project_python_files()
        print(f"📁 Found {len(self.python_files)} project Python files to analyze")
        
        # Advanced analysis phases
        self._analyze_import_bloat()
        self._analyze_class_hierarchy_duplication()
        self._analyze_method_signature_duplication()
        self._analyze_constant_duplication()
        self._analyze_error_handling_duplication()
        self._analyze_data_structure_duplication()
        self._analyze_algorithm_duplication()
        self._analyze_interface_duplication()
        self._analyze_test_duplication()
        self._analyze_documentation_duplication()
        
        return self._compile_results()
    
    def _find_project_python_files(self):
        """Find project-specific Python files."""
        exclude_dirs = {
            '__pycache__', '.git', '.pytest_cache', 'node_modules',
            '.venv', 'venv', 'env', '.env', 'build', 'dist',
            'site-packages', 'lib', 'lib64', 'include', 'Scripts',
            'share', 'bin', 'etc', 'var', 'tmp', 'temp',
            '.tox', '.coverage', 'htmlcov', '.mypy_cache',
            '.ruff_cache', '.black_cache', '.isort.cache'
        }
        
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    if self._is_project_file(file_path):
                        self.python_files.append(file_path)
    
    def _is_project_file(self, file_path: Path) -> bool:
        """Check if file is part of the project (not external dependency)."""
        try:
            rel_path = file_path.relative_to(self.project_root)
            path_parts = rel_path.parts
            
            # Exclude common external dependency paths
            external_patterns = [
                'site-packages', 'lib', 'lib64', 'include', 'Scripts',
                'share', 'bin', 'etc', 'var', 'tmp', 'temp',
                '.tox', '.coverage', 'htmlcov', '.mypy_cache',
                '.ruff_cache', '.black_cache', '.isort.cache'
            ]
            
            return not any(pattern in str(rel_path) for pattern in external_patterns)
        except ValueError:
            return False
    
    def _analyze_import_bloat(self):
        """Analyze import statement bloat and duplication."""
        print("📦 Analyzing import bloat...")
        
        import_patterns = defaultdict(list)
        unused_imports = []
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse imports
                tree = ast.parse(content)
                file_imports = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            file_imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            file_imports.append(node.module)
                
                # Check for duplicate import patterns
                for imp in file_imports:
                    import_patterns[imp].append(str(file_path))
                
                # Check for unused imports (basic analysis)
                for imp in file_imports:
                    if imp not in content.replace(f"import {imp}", "").replace(f"from {imp}", ""):
                        unused_imports.append((str(file_path), imp))
                        
            except Exception as e:
                print(f"⚠️  Error analyzing imports in {file_path}: {e}")
        
        # Find duplicate import patterns
        for imp, files in import_patterns.items():
            if len(files) > 5:  # Imported in more than 5 files
                self.advanced_patterns["duplicate_imports"].append({
                    "import": imp,
                    "files": files,
                    "count": len(files)
                })
        
        self.bloat_opportunities.extend([
            f"Import bloat: {len(unused_imports)} potentially unused imports",
            f"Duplicate imports: {len([p for p in self.advanced_patterns['duplicate_imports'] if p['count'] > 10])} high-frequency imports"
        ])
    
    def _analyze_class_hierarchy_duplication(self):
        """Analyze class hierarchy duplication."""
        print("🏗️  Analyzing class hierarchy duplication...")
        
        class_signatures = defaultdict(list)
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        # Extract class signature
                        bases = [base.id if hasattr(base, 'id') else str(base) for base in node.bases]
                        signature = f"{node.name}({', '.join(bases)})"
                        class_signatures[signature].append(str(file_path))
                        
            except Exception as e:
                print(f"⚠️  Error analyzing classes in {file_path}: {e}")
        
        # Find duplicate class hierarchies
        for signature, files in class_signatures.items():
            if len(files) > 2:  # Same class signature in more than 2 files
                self.advanced_patterns["duplicate_class_hierarchies"].append({
                    "signature": signature,
                    "files": files,
                    "count": len(files)
                })
    
    def _analyze_method_signature_duplication(self):
        """Analyze method signature duplication."""
        print("🔧 Analyzing method signature duplication...")
        
        method_signatures = defaultdict(list)
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Extract method signature
                        args = [arg.arg for arg in node.args.args]
                        signature = f"{node.name}({', '.join(args)})"
                        method_signatures[signature].append(str(file_path))
                        
            except Exception as e:
                print(f"⚠️  Error analyzing methods in {file_path}: {e}")
        
        # Find duplicate method signatures
        for signature, files in method_signatures.items():
            if len(files) > 3:  # Same method signature in more than 3 files
                self.advanced_patterns["duplicate_method_signatures"].append({
                    "signature": signature,
                    "files": files,
                    "count": len(files)
                })
    
    def _analyze_constant_duplication(self):
        """Analyze constant duplication."""
        print("📊 Analyzing constant duplication...")
        
        constants = defaultdict(list)
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find constant patterns
                constant_patterns = [
                    r'^[A-Z_][A-Z0-9_]*\s*=\s*["\'].*["\']',  # String constants
                    r'^[A-Z_][A-Z0-9_]*\s*=\s*\d+',  # Numeric constants
                    r'^[A-Z_][A-Z0-9_]*\s*=\s*\[',  # List constants
                    r'^[A-Z_][A-Z0-9_]*\s*=\s*\{',  # Dict constants
                ]
                
                for line_num, line in enumerate(content.split('\n'), 1):
                    for pattern in constant_patterns:
                        if re.match(pattern, line.strip()):
                            const_name = line.split('=')[0].strip()
                            constants[const_name].append(str(file_path))
                            
            except Exception as e:
                print(f"⚠️  Error analyzing constants in {file_path}: {e}")
        
        # Find duplicate constants
        for const_name, files in constants.items():
            if len(files) > 2:  # Same constant in more than 2 files
                self.advanced_patterns["duplicate_constants"].append({
                    "constant": const_name,
                    "files": files,
                    "count": len(files)
                })
    
    def _analyze_error_handling_duplication(self):
        """Analyze error handling duplication."""
        print("⚠️  Analyzing error handling duplication...")
        
        error_patterns = defaultdict(list)
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find error handling patterns
                error_handling_patterns = [
                    r'except\s+(\w+)\s+as\s+(\w+):',
                    r'raise\s+(\w+)\(',
                    r'logger\.error\(',
                    r'print\s*\(\s*["\'].*error.*["\']',
                ]
                
                for pattern in error_handling_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        error_patterns[str(match)].append(str(file_path))
                        
            except Exception as e:
                print(f"⚠️  Error analyzing error handling in {file_path}: {e}")
        
        # Find duplicate error handling patterns
        for pattern, files in error_patterns.items():
            if len(files) > 3:  # Same error pattern in more than 3 files
                self.advanced_patterns["duplicate_error_handling"].append({
                    "pattern": pattern,
                    "files": files,
                    "count": len(files)
                })
    
    def _analyze_data_structure_duplication(self):
        """Analyze data structure duplication."""
        print("🗂️  Analyzing data structure duplication...")
        
        data_structures = defaultdict(list)
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find data structure patterns
                structure_patterns = [
                    r'@dataclass',
                    r'class\s+\w+.*:\s*$',
                    r'TypedDict\(',
                    r'NamedTuple\(',
                    r'Enum\(',
                ]
                
                for pattern in structure_patterns:
                    if re.search(pattern, content):
                        data_structures[pattern].append(str(file_path))
                        
            except Exception as e:
                print(f"⚠️  Error analyzing data structures in {file_path}: {e}")
        
        # Find duplicate data structure patterns
        for pattern, files in data_structures.items():
            if len(files) > 2:  # Same pattern in more than 2 files
                self.advanced_patterns["duplicate_data_structures"].append({
                    "pattern": pattern,
                    "files": files,
                    "count": len(files)
                })
    
    def _analyze_algorithm_duplication(self):
        """Analyze algorithm duplication."""
        print("🧮 Analyzing algorithm duplication...")
        
        algorithms = defaultdict(list)
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find algorithm patterns
                algorithm_patterns = [
                    r'for\s+\w+\s+in\s+range\(',
                    r'while\s+\w+.*:',
                    r'if\s+.*in\s+.*:',
                    r'sorted\(',
                    r'filter\(',
                    r'map\(',
                    r'reduce\(',
                ]
                
                for pattern in algorithm_patterns:
                    if re.search(pattern, content):
                        algorithms[pattern].append(str(file_path))
                        
            except Exception as e:
                print(f"⚠️  Error analyzing algorithms in {file_path}: {e}")
        
        # Find duplicate algorithm patterns
        for pattern, files in algorithms.items():
            if len(files) > 5:  # Same algorithm pattern in more than 5 files
                self.advanced_patterns["duplicate_algorithms"].append({
                    "pattern": pattern,
                    "files": files,
                    "count": len(files)
                })
    
    def _analyze_interface_duplication(self):
        """Analyze interface duplication."""
        print("🔌 Analyzing interface duplication...")
        
        interfaces = defaultdict(list)
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find interface patterns
                interface_patterns = [
                    r'class\s+\w+.*Protocol.*:',
                    r'class\s+\w+.*ABC.*:',
                    r'@abstractmethod',
                    r'def\s+\w+.*->\s*None:',
                ]
                
                for pattern in interface_patterns:
                    if re.search(pattern, content):
                        interfaces[pattern].append(str(file_path))
                        
            except Exception as e:
                print(f"⚠️  Error analyzing interfaces in {file_path}: {e}")
        
        # Find duplicate interface patterns
        for pattern, files in interfaces.items():
            if len(files) > 2:  # Same interface pattern in more than 2 files
                self.advanced_patterns["duplicate_interfaces"].append({
                    "pattern": pattern,
                    "files": files,
                    "count": len(files)
                })
    
    def _analyze_test_duplication(self):
        """Analyze test duplication."""
        print("🧪 Analyzing test duplication...")
        
        test_patterns = defaultdict(list)
        
        for file_path in self.python_files:
            if 'test' in str(file_path).lower():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find test patterns
                    test_patterns_found = [
                        r'def\s+test_\w+',
                        r'class\s+Test\w+',
                        r'@pytest\.fixture',
                        r'assert\s+',
                        r'mock\.',
                    ]
                    
                    for pattern in test_patterns_found:
                        if re.search(pattern, content):
                            test_patterns[pattern].append(str(file_path))
                            
                except Exception as e:
                    print(f"⚠️  Error analyzing tests in {file_path}: {e}")
        
        # Find duplicate test patterns
        for pattern, files in test_patterns.items():
            if len(files) > 3:  # Same test pattern in more than 3 files
                self.advanced_patterns["duplicate_tests"].append({
                    "pattern": pattern,
                    "files": files,
                    "count": len(files)
                })
    
    def _analyze_documentation_duplication(self):
        """Analyze documentation duplication."""
        print("📚 Analyzing documentation duplication...")
        
        doc_patterns = defaultdict(list)
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find documentation patterns
                doc_patterns_found = [
                    r'"""[\s\S]*?"""',
                    r"'''[\s\S]*?'''",
                    r'# TODO:',
                    r'# FIXME:',
                    r'# NOTE:',
                ]
                
                for pattern in doc_patterns_found:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if len(match) > 50:  # Only consider substantial documentation
                            doc_patterns[match[:100]].append(str(file_path))
                            
            except Exception as e:
                print(f"⚠️  Error analyzing documentation in {file_path}: {e}")
        
        # Find duplicate documentation patterns
        for pattern, files in doc_patterns.items():
            if len(files) > 2:  # Same documentation in more than 2 files
                self.advanced_patterns["duplicate_documentation"].append({
                    "pattern": pattern,
                    "files": files,
                    "count": len(files)
                })
    
    def _compile_results(self) -> Dict[str, Any]:
        """Compile analysis results."""
        results = {
            "total_files_analyzed": len(self.python_files),
            "advanced_patterns": dict(self.advanced_patterns),
            "bloat_opportunities": self.bloat_opportunities,
            "reduction_opportunities": []
        }
        
        # Calculate reduction opportunities
        total_duplicates = sum(len(patterns) for patterns in self.advanced_patterns.values())
        results["reduction_opportunities"] = [
            f"Import consolidation: {len(self.advanced_patterns.get('duplicate_imports', []))} patterns",
            f"Class hierarchy consolidation: {len(self.advanced_patterns.get('duplicate_class_hierarchies', []))} patterns",
            f"Method signature consolidation: {len(self.advanced_patterns.get('duplicate_method_signatures', []))} patterns",
            f"Constant consolidation: {len(self.advanced_patterns.get('duplicate_constants', []))} patterns",
            f"Error handling consolidation: {len(self.advanced_patterns.get('duplicate_error_handling', []))} patterns",
            f"Data structure consolidation: {len(self.advanced_patterns.get('duplicate_data_structures', []))} patterns",
            f"Algorithm consolidation: {len(self.advanced_patterns.get('duplicate_algorithms', []))} patterns",
            f"Interface consolidation: {len(self.advanced_patterns.get('duplicate_interfaces', []))} patterns",
            f"Test consolidation: {len(self.advanced_patterns.get('duplicate_tests', []))} patterns",
            f"Documentation consolidation: {len(self.advanced_patterns.get('duplicate_documentation', []))} patterns",
        ]
        
        return results

def analyze_advanced_dry_violations() -> Dict[str, Any]:
    """Main function to analyze advanced DRY violations."""
    analyzer = AdvancedDRYAnalyzer()
    return analyzer.analyze_advanced_dry_violations()

if __name__ == "__main__":
    results = analyze_advanced_dry_violations()
    print(f"\n📊 ADVANCED DRY ANALYSIS COMPLETE")
    print(f"📁 Total files analyzed: {results['total_files_analyzed']}")
    print(f"🎯 Advanced patterns found: {sum(len(patterns) for patterns in results['advanced_patterns'].values())}")
    print(f"💡 Bloat opportunities: {len(results['bloat_opportunities'])}")
    print(f"🚀 Reduction opportunities: {len(results['reduction_opportunities'])}")
    
    print("\n🚀 REDUCTION OPPORTUNITIES:")
    for opportunity in results['reduction_opportunities']:
        print(f"   {opportunity}")
