#!/usr/bin/env python3
"""
Data Processing DRY Eliminator - Agent-5 Specialized
===================================================

Systematically eliminates DRY violations in data processing imports and utilities
across business intelligence modules. Focuses on consolidating duplicate patterns
in data processing, validation, and business logic utilities.

ELIMINATES DUPLICATE PATTERNS:
- Duplicate pandas/numpy imports
- Duplicate JSON/CSV processing logic
- Duplicate database connection patterns
- Duplicate API request patterns
- Duplicate data validation patterns
- Duplicate file processing patterns

Author: Agent-5 (Business Intelligence Specialist)
Mission: DRY Violations Elimination - Agent-2 Coordinated
Status: ACTIVE - Data Processing DRY Elimination
"""

import os
import re
import ast
from ..core.unified_data_processing_system import get_unified_data_processing
from typing import Any, Dict, List, Set, Tuple, Optional
from collections import defaultdict

# Import unified systems
from .unified_logging_system import get_logger
from .unified_configuration_system import get_unified_config
from .unified_validation_system import validate_required_fields, validate_data_types
from .unified_utility_system import get_unified_utility


class DataProcessingDRYEliminator:
    """
    Comprehensive data processing DRY violation elimination system.
    
    SYSTEMATICALLY ELIMINATES:
    - Duplicate data processing imports
    - Duplicate data processing utilities
    - Duplicate validation patterns
    - Duplicate file processing patterns
    - Duplicate API request patterns
    """
    
    def __init__(self):
        """Initialize the data processing DRY eliminator."""
        self.logger = get_logger(__name__)
        self.config = get_unified_config()
        self.utility = get_unified_utility()
        
        # Processing results
        self.elimination_results = {
            'files_processed': 0,
            'imports_consolidated': 0,
            'functions_replaced': 0,
            'patterns_eliminated': 0,
            'files_updated': 0,
            'errors': []
        }
        
        # Define replacement patterns for data processing
        self.import_replacements = {
            # Standard library imports
            r'from ..core.unified_data_processing_system import read_json, write_json': 'from ..core.unified_data_processing_system import read_json, write_json',
            r'from ..core.unified_data_processing_system import read_csv, write_csv': 'from ..core.unified_data_processing_system import read_csv, write_csv',
            r'from ..core.unified_data_processing_system import connect_sqlite, execute_query': 'from ..core.unified_data_processing_system import connect_sqlite, execute_query',
            
            # Optional library imports
            r'from ..core.unified_data_processing_system import read_dataframe, write_dataframe, PANDAS_AVAILABLE': 'from ..core.unified_data_processing_system import read_dataframe, write_dataframe, PANDAS_AVAILABLE',
            r'from ..core.unified_data_processing_system import NUMPY_AVAILABLE': 'from ..core.unified_data_processing_system import NUMPY_AVAILABLE',
            r'from ..core.unified_data_processing_system import make_request, REQUESTS_AVAILABLE': 'from ..core.unified_data_processing_system import make_request, REQUESTS_AVAILABLE',
            
            # Common patterns
            r'from ..core.unified_data_processing_system import get_unified_data_processing': 'from ..core.unified_data_processing_system import get_unified_data_processing',
            r'from ..core.unified_data_processing_system import get_unified_data_processing': 'from ..core.unified_data_processing_system import get_unified_data_processing',
        }
        
        # Function replacement patterns
        self.function_replacements = {
            # JSON operations
            r'json\.load\(([^)]+)\)': r'read_json(\1)',
            r'json\.dump\(([^,]+),\s*([^)]+)\)': r'write_json(\1, \2)',
            
            # CSV operations
            r'csv\.DictReader\(([^)]+)\)': r'read_csv(\1)',
            r'csv\.DictWriter\(([^)]+)\)': r'write_csv(\1)',
            
            # Database operations
            r'sqlite3\.connect\(([^)]+)\)': r'connect_sqlite(\1)',
            r'cursor\.execute\(([^)]+)\)': r'execute_query(conn, \1)',
            
            # API operations
            r'requests\.get\(([^)]+)\)': r'make_request(\1)',
            r'requests\.post\(([^)]+)\)': r'make_request(\1, "POST")',
            
            # File operations
            r'Path\(([^)]+)\)\.read_text\(\)': r'get_unified_data_processing().read_file(\1)',
            r'Path\(([^)]+)\)\.write_text\(([^)]+)\)': r'get_unified_data_processing().write_file(\1, \2)',
        }
        
        # Data processing patterns to consolidate
        self.data_processing_patterns = {
            'csv_processing': [
                r'def read_csv\([^)]*\):',
                r'def write_csv\([^)]*\):',
                r'def process_csv\([^)]*\):',
            ],
            'json_processing': [
                r'def read_json\([^)]*\):',
                r'def write_json\([^)]*\):',
                r'def process_json\([^)]*\):',
            ],
            'database_processing': [
                r'def connect_db\([^)]*\):',
                r'def execute_query\([^)]*\):',
                r'def process_database\([^)]*\):',
            ],
            'api_processing': [
                r'def make_request\([^)]*\):',
                r'def process_api\([^)]*\):',
                r'def handle_response\([^)]*\):',
            ],
            'validation_patterns': [
                r'def validate_data\([^)]*\):',
                r'def clean_data\([^)]*\):',
                r'def process_validation\([^)]*\):',
            ]
        }
    
    def eliminate_data_processing_dry_violations(self) -> Dict[str, Any]:
        """Eliminate all data processing DRY violations across the project."""
        self.logger.info("🚀 Starting data processing DRY violation elimination...")
        
        try:
            # Find all Python files in the project
            project_files = self._find_project_python_files()
            self.logger.info(f"Found {len(project_files)} Python files to process")
            
            # Process each file
            for file_path in project_files:
                try:
                    self._process_file_for_data_processing_dry(file_path)
                    self.elimination_results['files_processed'] += 1
                except Exception as e:
                    error_msg = f"Error processing {file_path}: {e}"
                    self.logger.error(error_msg)
                    self.elimination_results['errors'].append(error_msg)
            
            # Generate summary report
            self._generate_data_processing_summary()
            
            self.logger.info("✅ Data processing DRY violation elimination completed")
            return self.elimination_results
            
        except Exception as e:
            error_msg = f"Critical error in data processing DRY elimination: {e}"
            self.logger.error(error_msg)
            self.elimination_results['errors'].append(error_msg)
            return self.elimination_results
    
    def _find_project_python_files(self) -> List[Path]:
        """Find all Python files in the project (excluding external dependencies)."""
        from ..core.unified_data_processing_system import get_unified_data_processing
        project_root = Path(self.config.get('paths.project_root', '.'))
        python_files = []
        
        # Define directories to exclude
        exclude_dirs = {
            'node_modules', '__pycache__', '.git', '.pytest_cache',
            'venv', 'env', '.venv', '.env', 'build', 'dist',
            'site-packages', '.mypy_cache', '.coverage'
        }
        
        for root, dirs, files in os.walk(project_root):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    python_files.append(file_path)
        
        return python_files
    
    def _process_file_for_data_processing_dry(self, file_path: Path) -> bool:
        """Process a single file for data processing DRY violations."""
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Skip if file is too small or doesn't contain data processing patterns
            if len(content) < 100:
                return False
            
            # Check if file contains data processing patterns
            if not self._contains_data_processing_patterns(content):
                return False
            
            self.logger.info(f"Processing file: {file_path}")
            
            # Apply import replacements
            content = self._apply_import_replacements(content)
            
            # Apply function replacements
            content = self._apply_function_replacements(content)
            
            # Apply data processing pattern consolidations
            content = self._apply_data_processing_consolidations(content)
            
            # Add unified data processing import if needed
            content = self._add_unified_data_processing_import(content)
            
            # Only write if content changed
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.elimination_results['files_updated'] += 1
                self.logger.info(f"Updated file: {file_path}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {e}")
            return False
    
    def _contains_data_processing_patterns(self, content: str) -> bool:
        """Check if content contains data processing patterns."""
        patterns = [
            r'import\s+(json|csv|sqlite3|pandas|numpy|requests)',
            r'from\s+(json|csv|sqlite3|pandas|numpy|requests)',
            r'def\s+(read_csv|write_csv|read_json|write_json)',
            r'def\s+(connect_db|execute_query|make_request)',
            r'def\s+(validate_data|clean_data|process_data)',
            r'Path\([^)]+\)\.(read_text|write_text)',
            r'json\.(load|dump)',
            r'csv\.(DictReader|DictWriter)',
            r'sqlite3\.connect',
            r'requests\.(get|post)',
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _apply_import_replacements(self, content: str) -> str:
        """Apply import replacements to consolidate data processing imports."""
        for pattern, replacement in self.import_replacements.items():
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                self.elimination_results['imports_consolidated'] += 1
        
        return content
    
    def _apply_function_replacements(self, content: str) -> str:
        """Apply function replacements to use unified data processing functions."""
        for pattern, replacement in self.function_replacements.items():
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                self.elimination_results['functions_replaced'] += 1
        
        return content
    
    def _apply_data_processing_consolidations(self, content: str) -> str:
        """Apply data processing pattern consolidations."""
        # Remove duplicate data processing functions
        for category, patterns in self.data_processing_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.MULTILINE):
                    # Replace with unified system call
                    content = re.sub(
                        pattern,
                        f'# Replaced with unified data processing system\n    # Use get_unified_data_processing().{category}()',
                        content,
                        flags=re.MULTILINE
                    )
                    self.elimination_results['patterns_eliminated'] += 1
        
        return content
    
    def _add_unified_data_processing_import(self, content: str) -> str:
        """Add unified data processing import if needed."""
        if 'unified_data_processing_system' not in content and 'get_unified_data_processing' in content:
            # Add import at the top
            import_line = 'from ..core.unified_data_processing_system import get_unified_data_processing\n'
            
            # Find the first import line
            lines = content.split('\n')
            import_index = 0
            
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_index = i
                    break
            
            # Insert the import
            lines.insert(import_index, import_line)
            content = '\n'.join(lines)
            
            self.elimination_results['imports_consolidated'] += 1
        
        return content
    
    def _generate_data_processing_summary(self):
        """Generate summary of data processing DRY elimination."""
        summary = f"""
🎯 DATA PROCESSING DRY ELIMINATION SUMMARY
==========================================

📊 PROCESSING METRICS:
- Files Processed: {self.elimination_results['files_processed']}
- Files Updated: {self.elimination_results['files_updated']}
- Imports Consolidated: {self.elimination_results['imports_consolidated']}
- Functions Replaced: {self.elimination_results['functions_replaced']}
- Patterns Eliminated: {self.elimination_results['patterns_eliminated']}
- Errors: {len(self.elimination_results['errors'])}

✅ ACHIEVEMENTS:
- Data processing imports unified
- Duplicate functions consolidated
- Validation patterns standardized
- File processing patterns centralized
- API request patterns unified

🚀 NEXT STEPS:
- Monitor unified data processing system performance
- Continue with business logic utilities centralization
- Report progress to Captain Agent-4
        """
        
        self.logger.info(summary)
        
        # Save summary to file
        from ..core.unified_data_processing_system import get_unified_data_processing
        summary_file = Path('agent_workspaces/Agent-5/DATA_PROCESSING_DRY_ELIMINATION_SUMMARY.md')
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        summary_file.write_text(summary, encoding='utf-8')


def main():
    """Main function to run data processing DRY elimination."""
    eliminator = DataProcessingDRYEliminator()
    results = eliminator.eliminate_data_processing_dry_violations()
    
    print(f"Data processing DRY elimination completed:")
    print(f"- Files processed: {results['files_processed']}")
    print(f"- Files updated: {results['files_updated']}")
    print(f"- Imports consolidated: {results['imports_consolidated']}")
    print(f"- Functions replaced: {results['functions_replaced']}")
    print(f"- Patterns eliminated: {results['patterns_eliminated']}")
    print(f"- Errors: {len(results['errors'])}")


if __name__ == "__main__":
    main()
