#!/usr/bin/env python3
"""
DRY Violation Eliminator - Comprehensive DRY Elimination System
=============================================================

Systematically eliminates all DRY violations by migrating existing files
to use the unified systems and removing duplicate implementations.

Author: Agent-5 (Business Intelligence Specialist)
Mission: Complete DRY Violation Elimination
Status: EXECUTING - Comprehensive DRY Elimination
"""



class DRYViolationEliminator:
    """
    Comprehensive DRY violation elimination system.
    
    SYSTEMATICALLY ELIMINATES:
    - Duplicate configuration files
    - Duplicate validation implementations
    - Duplicate logging patterns
    - Duplicate utility functions
    - Duplicate import statements
    - Duplicate class patterns
    """
    
    def __init__(self):
        """Initialize DRY violation eliminator."""
        self.config = get_unified_config()
        self.logger = get_logger(__name__)
        self.unified_logger = get_unified_logger()
        self.utility = get_unified_utility()
        
        # DRY violation patterns to eliminate
        self.duplicate_files = {
            "configuration": [
                "src/config.py",
                "src/settings.py",
                "src/utils/config_core.py",
                "src/utils/config_consolidator.py",
                "src/utils/config_pattern_scanner.py",
                "src/utils/config_file_migrator.py",
                "src/utils/config_report_generator.py"
            ],
            "validation": [
                "src/core/validation/coordination_validator.py",
                "src/utils/config_pattern_scanner.py",
                "src/services/messaging_core.py",
                "src/core/validation/javascript_v2_compliance_validator.py",
                "src/core/validation/agent7_v2_compliance_coordinator.py",
                "src/core/validation/repository_pattern_validator.py",
                "src/core/validation/enhanced_cli_validation_framework.py",
                "src/core/validation/gaming_performance_threshold_checker.py"
            ],
            "logging": [
                # Files with duplicate logging patterns (25+ locations)
            ],
            "utilities": [
                "src/core/constants/paths.py",
                "src/utils/config_core.py",
                "src/services/messaging_core.py",
                "src/core/validation/coordination_validator.py",
                "src/core/processing/unified_processing_system.py"
            ]
        }
        
        # Import patterns to replace
        self.import_replacements = {
            "configuration": {
                "old": [
                    "from ..core.unified_configuration_system import get_unified_config, get_logger
                    "from ..core.unified_utility_system import get_unified_utility
                    "from ..core.unified_logging_system import get_logger
                    "from ..core.unified_configuration_system import get_timestamp
                ],
                "new": [
                    "from ..core.unified_configuration_system import get_unified_config, get_logger",
                    "from ..core.unified_validation_system import validate_required_fields, validate_data_types",
                    "from ..core.unified_logging_system import get_unified_logger",
                    "from ..core.unified_utility_system import get_unified_utility"
                ]
            }
        }
        
        # Function patterns to replace
        self.function_replacements = {
            "validate_required_fields": "validate_required_fields",
            "validate_data_types": "validate_data_types",
            "get_project_root": "get_unified_utility().get_unified_utility().get_project_root()",
            "resolve_path": "get_unified_utility().resolve_path",
            "get_logger": "get_logger",
            "log_operation": "get_unified_logger().log_operation_start"
        }
    
    def eliminate_all_dry_violations(self) -> Dict[str, Any]:
        """
        Eliminate all DRY violations systematically.
        
        Returns:
            Dict containing elimination results and metrics
        """
        self.get_logger(__name__).info("Starting comprehensive DRY violation elimination")
        
        results = {
            "files_migrated": 0,
            "duplicate_files_removed": 0,
            "imports_updated": 0,
            "functions_replaced": 0,
            "errors": []
        }
        
        try:
            # Phase 1: Migrate existing files to use unified systems
            results["files_migrated"] = self._migrate_files_to_unified_systems()
            
            # Phase 2: Remove duplicate files
            results["duplicate_files_removed"] = self._remove_duplicate_files()
            
            # Phase 3: Update import statements
            results["imports_updated"] = self._update_import_statements()
            
            # Phase 4: Replace duplicate function calls
            results["functions_replaced"] = self._replace_duplicate_functions()
            
            # Phase 5: Validate elimination
            self._validate_dry_elimination()
            
            self.get_logger(__name__).info(f"DRY violation elimination completed: {results}")
            
        except Exception as e:
            error_msg = f"Error during DRY elimination: {e}"
            self.get_logger(__name__).error(error_msg)
            results["errors"].append(error_msg)
        
        return results
    
    def _migrate_files_to_unified_systems(self) -> int:
        """Migrate existing files to use unified systems."""
        migrated_count = 0
        
        for category, files in self.duplicate_files.items():
            for file_path in files:
                if get_unified_utility().path.exists(file_path):
                    try:
                        self._migrate_file_to_unified_system(file_path, category)
                        migrated_count += 1
                        self.get_logger(__name__).info(f"Migrated {file_path} to unified {category} system")
                    except Exception as e:
                        self.get_logger(__name__).error(f"Failed to migrate {file_path}: {e}")
        
        return migrated_count
    
    def _migrate_file_to_unified_system(self, file_path: str, category: str):
        """Migrate a specific file to use unified systems."""
        content = self.utility.read_file(file_path)
        
        if not get_unified_validator().validate_required(content):
            return
        
        # Update imports based on category
        if category == "configuration":
            content = self._update_configuration_imports(content)
        elif category == "validation":
            content = self._update_validation_imports(content)
        elif category == "logging":
            content = self._update_logging_imports(content)
        elif category == "utilities":
            content = self._update_utility_imports(content)
        
        # Replace function calls
        content = self._replace_function_calls(content)
        
        # Add DRY elimination header
        content = self._add_dry_elimination_header(content, category)
        
        # Write updated content
        self.utility.write_file(file_path, content)
    
    def _update_configuration_imports(self, content: str) -> str:
        """Update imports for configuration files."""
        # Add unified configuration imports
        if "unified_configuration_system" not in content:
            content = content.replace(
                "from ..core.unified_configuration_system import get_unified_config, get_logger
                "from ..core.unified_configuration_system import get_unified_config, get_logger\nfrom ..core.unified_configuration_system import get_unified_config, get_logger
            )
        
        return content
    
    def _update_validation_imports(self, content: str) -> str:
        """Update imports for validation files."""
        # Add unified validation imports
        if "unified_validation_system" not in content:
            content = content.replace(
                "from ..core.unified_validation_system import validate_required_fields, validate_data_types
                "from ..core.unified_validation_system import validate_required_fields, validate_data_types\nfrom ..core.unified_validation_system import validate_required_fields, validate_data_types
            )
        
        return content
    
    def _update_logging_imports(self, content: str) -> str:
        """Update imports for logging files."""
        # Add unified logging imports
        if "unified_logging_system" not in content:
            content = content.replace(
                "from ..core.unified_logging_system import get_logger
                "from ..core.unified_logging_system import get_unified_logger\nfrom ..core.unified_logging_system import get_logger
            )
        
        return content
    
    def _update_utility_imports(self, content: str) -> str:
        """Update imports for utility files."""
        # Add unified utility imports
        if "unified_utility_system" not in content:
            content = content.replace(
                "from ..core.unified_utility_system import get_unified_utility
                "from ..core.unified_utility_system import get_unified_utility\nfrom ..core.unified_utility_system import get_unified_utility
            )
        
        return content
    
    def _replace_function_calls(self, content: str) -> str:
        """Replace duplicate function calls with unified system calls."""
        for old_func, new_func in self.function_replacements.items():
            # Replace function definitions
            pattern = f"def {old_func}\\("
            if re.search(pattern, content):
                content = re.sub(
                    pattern,
                    f"# MIGRATED TO UNIFIED SYSTEM: {old_func}\n    # def {old_func}(",
                    content
                )
        
        return content
    
    def _add_dry_elimination_header(self, content: str, category: str) -> str:
        """Add DRY elimination header to migrated files."""
        header = f'''"""
DRY VIOLATION ELIMINATION - {category.upper()}
==========================================

MIGRATED TO UNIFIED {category.upper()} SYSTEM - Eliminates duplicate {category} patterns.

This module now uses the unified {category} system instead of duplicate
{category} logic patterns.

DRY ELIMINATION: Migrated from duplicate {category} patterns to unified system.

Author: Agent-5 (Business Intelligence Specialist)
Mission: DRY Violation Elimination
Status: MIGRATED - Using Unified {category.title()} System
"""

'''
        
        # Find the first docstring and replace it
        lines = content.split('\n')
        new_lines = []
        in_docstring = False
        docstring_replaced = False
        
        for line in lines:
            if line.strip().startswith('"""') and not docstring_replaced:
                if not get_unified_validator().validate_required(in_docstring):
                    in_docstring = True
                    new_lines.append(header.rstrip())
                    docstring_replaced = True
                else:
                    in_docstring = False
            elif not in_docstring or docstring_replaced:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _remove_duplicate_files(self) -> int:
        """Remove duplicate files that are no longer needed."""
        removed_count = 0
        
        # Files that can be safely removed after migration
        files_to_remove = [
            "src/utils/config_consolidator.py",
            "src/utils/config_pattern_scanner.py",
            "src/utils/config_file_migrator.py",
            "src/utils/config_report_generator.py"
        ]
        
        for file_path in files_to_remove:
            if get_unified_utility().path.exists(file_path):
                try:
                    # Create backup before removal
                    backup_path = f"{file_path}.backup"
                    shutil.copy2(file_path, backup_path)
                    
                    # Remove the duplicate file
                    get_unified_utility().remove(file_path)
                    removed_count += 1
                    self.get_logger(__name__).info(f"Removed duplicate file: {file_path}")
                except Exception as e:
                    self.get_logger(__name__).error(f"Failed to remove {file_path}: {e}")
        
        return removed_count
    
    def _update_import_statements(self) -> int:
        """Update import statements across the codebase."""
        updated_count = 0
        
        # Find all Python files
        python_files = self.utility.list_files("src", "*.py", recursive=True)
        
        for file_path in python_files:
            try:
                content = self.utility.read_file(file_path)
                if not get_unified_validator().validate_required(content):
                    continue
                
                original_content = content
                
                # Update imports to use unified systems
                content = self._update_file_imports(content)
                
                if content != original_content:
                    self.utility.write_file(file_path, content)
                    updated_count += 1
                    self.get_logger(__name__).info(f"Updated imports in: {file_path}")
                    
            except Exception as e:
                self.get_logger(__name__).error(f"Failed to update imports in {file_path}: {e}")
        
        return updated_count
    
    def _update_file_imports(self, content: str) -> str:
        """Update imports in a specific file."""
        # Replace common duplicate import patterns
        replacements = [
            ("from ..core.unified_utility_system import get_unified_utility
            ("from ..core.unified_logging_system import get_logger
            ("from ..core.unified_configuration_system import get_timestamp
        ]
        
        for old_import, new_import in replacements:
            if old_import in content and new_import not in content:
                content = content.replace(old_import, f"{old_import}\n{new_import}")
        
        return content
    
    def _replace_duplicate_functions(self) -> int:
        """Replace duplicate function calls with unified system calls."""
        replaced_count = 0
        
        # Find all Python files
        python_files = self.utility.list_files("src", "*.py", recursive=True)
        
        for file_path in python_files:
            try:
                content = self.utility.read_file(file_path)
                if not get_unified_validator().validate_required(content):
                    continue
                
                original_content = content
                
                # Replace function calls
                for old_func, new_func in self.function_replacements.items():
                    if old_func in content:
                        content = content.replace(old_func, new_func)
                        replaced_count += 1
                
                if content != original_content:
                    self.utility.write_file(file_path, content)
                    self.get_logger(__name__).info(f"Replaced functions in: {file_path}")
                    
            except Exception as e:
                self.get_logger(__name__).error(f"Failed to replace functions in {file_path}: {e}")
        
        return replaced_count
    
    def _validate_dry_elimination(self):
        """Validate that DRY violations have been eliminated."""
        self.get_logger(__name__).info("Validating DRY elimination results")
        
        # Check that unified systems are being used
        python_files = self.utility.list_files("src", "*.py", recursive=True)
        
        unified_usage_count = 0
        duplicate_patterns_found = 0
        
        for file_path in python_files:
            try:
                content = self.utility.read_file(file_path)
                if not get_unified_validator().validate_required(content):
                    continue
                
                # Check for unified system usage
                if any(pattern in content for pattern in [
                    "unified_configuration_system",
                    "unified_validation_system", 
                    "unified_logging_system",
                    "unified_utility_system"
                ]):
                    unified_usage_count += 1
                
                # Check for remaining duplicate patterns
                if any(pattern in content for pattern in [
                    "def validate_required_fields(",
                    "def get_project_root(",
                    "def get_unified_utility().resolve_path(",
                    "from ..core.unified_logging_system import get_logger
                ]):
                    duplicate_patterns_found += 1
                    
            except Exception as e:
                self.get_logger(__name__).error(f"Failed to validate {file_path}: {e}")
        
        self.get_logger(__name__).info(f"DRY elimination validation: {unified_usage_count} files using unified systems, {duplicate_patterns_found} duplicate patterns remaining")
        
        if duplicate_patterns_found == 0:
            self.get_logger(__name__).info("✅ DRY VIOLATION ELIMINATION COMPLETE - All violations eliminated!")
        else:
            self.get_logger(__name__).warning(f"⚠️ {duplicate_patterns_found} duplicate patterns still remain")

# ================================
# CONVENIENCE FUNCTIONS
# ================================

def eliminate_all_dry_violations() -> Dict[str, Any]:
    """Eliminate all DRY violations in the codebase."""
    eliminator = DRYViolationEliminator()
    return eliminator.eliminate_all_dry_violations()

if __name__ == "__main__":
    # Execute DRY violation elimination
    results = eliminate_all_dry_violations()
    get_logger(__name__).info(f"DRY Violation Elimination Results: {results}")
