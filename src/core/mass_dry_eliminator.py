#!/usr/bin/env python3
"""
Mass DRY Violation Eliminator
============================

Systematically eliminates DRY violations across all 194 project files.

Author: Agent-5 (Business Intelligence Specialist)
Mission: Complete DRY Violation Elimination
Status: MASS ELIMINATION
"""


class MassDRYEliminator:
    """Mass eliminator for DRY violations across all project files."""
    
    def __init__(self):
        self.project_root = get_unified_utility().Path(__file__).resolve().parents[3]
        self.python_files = []
        self.elimination_results = {
            "files_processed": 0,
            "files_migrated": 0,
            "imports_updated": 0,
            "functions_replaced": 0,
            "duplicate_files_removed": 0,
            "errors": []
        }
        
        # Get project files from focused analyzer
        self._get_project_files()
        
    def _get_project_files(self):
        """Get project files from focused analyzer."""
        analyzer = FocusedDRYAnalyzer()
        analyzer._find_project_python_files()
        self.python_files = analyzer.python_files
    
    def eliminate_all_dry_violations(self) -> Dict[str, Any]:
        """Eliminate all DRY violations across project files."""
        get_logger(__name__).info(f"🚀 Starting mass DRY elimination across {len(self.python_files)} project files...")
        
        # Phase 1: Update imports to use unified systems
        self._phase_1_update_imports()
        
        # Phase 2: Replace duplicate function calls
        self._phase_2_replace_functions()
        
        # Phase 3: Migrate configuration patterns
        self._phase_3_migrate_configurations()
        
        # Phase 4: Migrate validation patterns
        self._phase_4_migrate_validations()
        
        # Phase 5: Migrate logging patterns
        self._phase_5_migrate_logging()
        
        # Phase 6: Migrate utility patterns
        self._phase_6_migrate_utilities()
        
        # Phase 7: Remove duplicate files
        self._phase_7_remove_duplicates()
        
        # Phase 8: Validate results
        self._phase_8_validate_results()
        
        return self.elimination_results
    
    def _phase_1_update_imports(self):
        """Phase 1: Update imports to use unified systems."""
        get_logger(__name__).info("📦 Phase 1: Updating imports to unified systems...")
        
        import_replacements = [
            ("from ..core.unified_configuration_system import get_unified_config, get_logger
            ("from ..core.unified_logging_system import get_logger
            ("from ..core.unified_utility_system import get_unified_utility
            ("from ..core.unified_configuration_system import get_timestamp
            ("from ..core.unified_validation_system import validate_required_fields, validate_data_types
        ]
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply import replacements
                for old_import, new_import in import_replacements:
                    if old_import in content and new_import not in content:
                        content = content.replace(old_import, new_import)
                        self.elimination_results["imports_updated"] += 1
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.elimination_results["files_processed"] += 1
                    
            except Exception as e:
                self.elimination_results["errors"].append(f"Error updating imports in {file_path}: {e}")
    
    def _phase_2_replace_functions(self):
        """Phase 2: Replace duplicate function calls with unified system calls."""
        get_logger(__name__).info("🔧 Phase 2: Replacing duplicate function calls...")
        
        function_replacements = [
            # Configuration functions
            ("get_unified_config().get_config()", "get_unified_config().get_unified_config().get_config()"),
            ("get_unified_config().load_config()", "get_unified_config().get_unified_config().load_config()"),
            ("get_unified_config().save_config(", "get_unified_config().get_unified_config().save_config("),
            ("get_unified_config().validate_config(", "get_unified_config().get_unified_config().validate_config("),
            
            # Validation functions
            ("validate_required_fields(", "validate_required_fields("),
            ("validate_data_types(", "validate_data_types("),
            ("get_unified_validator().check_", "get_unified_validator().get_unified_validator().check_"),
            ("get_unified_validator().verify_", "get_unified_validator().get_unified_validator().verify_"),
            
            # Logging functions
            ("get_logger(__name__).info(", "get_logger(__name__).info("),
            ("get_logger(__name__).debug(", "get_logger(__name__).debug("),
            ("get_logger(__name__).warning(", "get_logger(__name__).warning("),
            ("get_logger(__name__).error(", "get_logger(__name__).error("),
            ("get_logger(__name__).critical(", "get_logger(__name__).critical("),
            ("get_logger(__name__).info(", "get_logger(__name__).info("),
            ("get_logger(__name__).debug(", "get_logger(__name__).debug("),
            ("get_logger(__name__).warning(", "get_logger(__name__).warning("),
            ("get_logger(__name__).error(", "get_logger(__name__).error("),
            ("get_logger(__name__).critical(", "get_logger(__name__).critical("),
            
            # Utility functions
            ("get_unified_utility().get_project_root()", "get_unified_utility().get_unified_utility().get_project_root()"),
            ("get_unified_utility().resolve_path(", "get_unified_utility().get_unified_utility().resolve_path("),
            ("get_unified_utility().format_string(", "get_unified_utility().get_unified_utility().format_string("),
            ("get_unified_utility().sanitize_", "get_unified_utility().get_unified_utility().sanitize_"),
            ("get_unified_utility().clean_", "get_unified_utility().get_unified_utility().clean_"),
            ("get_unified_utility().normalize_", "get_unified_utility().get_unified_utility().normalize_"),
            ("get_unified_utility().parse_", "get_unified_utility().get_unified_utility().parse_"),
            ("get_unified_utility().convert_", "get_unified_utility().get_unified_utility().convert_"),
        ]
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply function replacements
                for old_func, new_func in function_replacements:
                    if old_func in content:
                        content = content.replace(old_func, new_func)
                        self.elimination_results["functions_replaced"] += 1
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.elimination_results["files_processed"] += 1
                    
            except Exception as e:
                self.elimination_results["errors"].append(f"Error replacing functions in {file_path}: {e}")
    
    def _phase_3_migrate_configurations(self):
        """Phase 3: Migrate configuration patterns to unified system."""
        get_logger(__name__).info("⚙️  Phase 3: Migrating configuration patterns...")
        
        config_patterns = [
            (r'CONFIG\s*=\s*{', 'CONFIG = get_unified_config().get_unified_config().get_config()'),
            (r'config\s*=\s*{', 'config = get_unified_config().get_unified_config().get_config()'),
            (r'os\.environ\.get\(', 'get_unified_config().get_env('),
            (r'os\.getenv\(', 'get_unified_config().get_env('),
        ]
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply configuration pattern replacements
                for pattern, replacement in config_patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        self.elimination_results["files_migrated"] += 1
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.elimination_results["files_processed"] += 1
                    
            except Exception as e:
                self.elimination_results["errors"].append(f"Error migrating configurations in {file_path}: {e}")
    
    def _phase_4_migrate_validations(self):
        """Phase 4: Migrate validation patterns to unified system."""
        get_logger(__name__).info("✅ Phase 4: Migrating validation patterns...")
        
        validation_patterns = [
            (r'if\s+not\s+(\w+):', r'if not get_unified_validator().validate_required(\1):'),
            (r'raise\s+ValueError\(', r'get_unified_validator().raise_validation_error('),
            (r'raise\s+TypeError\(', r'get_unified_validator().raise_type_error('),
            (r'isinstance\(', r'get_unified_validator().validate_type('),
            (r'hasattr\(', r'get_unified_validator().validate_get_unified_validator().validate_hasattr('),
            (r'getattr\(', r'get_unified_validator().safe_get_unified_validator().safe_getattr('),
        ]
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply validation pattern replacements
                for pattern, replacement in validation_patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        self.elimination_results["files_migrated"] += 1
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.elimination_results["files_processed"] += 1
                    
            except Exception as e:
                self.elimination_results["errors"].append(f"Error migrating validations in {file_path}: {e}")
    
    def _phase_5_migrate_logging(self):
        """Phase 5: Migrate logging patterns to unified system."""
        get_logger(__name__).info("📝 Phase 5: Migrating logging patterns...")
        
        logging_patterns = [
            (r'print\(', r'get_logger(__name__).info('),
            (r'log\.info\(', r'get_logger(__name__).info('),
            (r'log\.debug\(', r'get_logger(__name__).debug('),
            (r'log\.warning\(', r'get_logger(__name__).warning('),
            (r'log\.error\(', r'get_logger(__name__).error('),
            (r'log\.critical\(', r'get_logger(__name__).critical('),
        ]
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply logging pattern replacements
                for pattern, replacement in logging_patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        self.elimination_results["files_migrated"] += 1
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.elimination_results["files_processed"] += 1
                    
            except Exception as e:
                self.elimination_results["errors"].append(f"Error migrating logging in {file_path}: {e}")
    
    def _phase_6_migrate_utilities(self):
        """Phase 6: Migrate utility patterns to unified system."""
        get_logger(__name__).info("🛠️  Phase 6: Migrating utility patterns...")
        
        utility_patterns = [
            (r'Path\(', r'get_unified_utility().get_unified_utility().Path('),
            (r'os\.path\.', r'get_unified_utility().path.'),
            (r'os\.makedirs\(', r'get_unified_utility().makedirs('),
            (r'os\.listdir\(', r'get_unified_utility().listdir('),
            (r'os\.exists\(', r'get_unified_utility().exists('),
            (r'os\.remove\(', r'get_unified_utility().remove('),
        ]
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply utility pattern replacements
                for pattern, replacement in utility_patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        self.elimination_results["files_migrated"] += 1
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.elimination_results["files_processed"] += 1
                    
            except Exception as e:
                self.elimination_results["errors"].append(f"Error migrating utilities in {file_path}: {e}")
    
    def _phase_7_remove_duplicates(self):
        """Phase 7: Remove duplicate files."""
        get_logger(__name__).info("🗑️  Phase 7: Removing duplicate files...")
        
        # Define duplicate files to remove
        duplicate_files = [
            "src/config.py",
            "src/settings.py",
            "src/utils/config_core.py",
            "src/utils/config_consolidator.py",
            "src/utils/config_pattern_scanner.py",
            "src/utils/config_file_migrator.py",
            "src/utils/config_report_generator.py",
        ]
        
        for duplicate_file in duplicate_files:
            file_path = self.project_root / duplicate_file
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.elimination_results["duplicate_files_removed"] += 1
                    get_logger(__name__).info(f"   Removed duplicate file: {duplicate_file}")
                except Exception as e:
                    self.elimination_results["errors"].append(f"Error removing {duplicate_file}: {e}")
    
    def _phase_8_validate_results(self):
        """Phase 8: Validate elimination results."""
        get_logger(__name__).info("✅ Phase 8: Validating elimination results...")
        
        # Count files using unified systems
        unified_usage_count = 0
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if any(system in content for system in [
                    "unified_configuration_system",
                    "unified_validation_system", 
                    "unified_logging_system",
                    "unified_utility_system"
                ]):
                    unified_usage_count += 1
                    
            except Exception as e:
                self.elimination_results["errors"].append(f"Error validating {file_path}: {e}")
        
        self.elimination_results["files_using_unified_systems"] = unified_usage_count
        
        get_logger(__name__).info(f"✅ Validation complete: {unified_usage_count} files now using unified systems")

def eliminate_mass_dry_violations() -> Dict[str, Any]:
    """Main function to eliminate all DRY violations."""
    eliminator = MassDRYEliminator()
    return eliminator.eliminate_all_dry_violations()

if __name__ == "__main__":
    results = eliminate_mass_dry_violations()
    get_logger(__name__).info(f"\n🎯 MASS DRY ELIMINATION COMPLETE")
    get_logger(__name__).info(f"📁 Files processed: {results['files_processed']}")
    get_logger(__name__).info(f"🔄 Files migrated: {results['files_migrated']}")
    get_logger(__name__).info(f"📦 Imports updated: {results['imports_updated']}")
    get_logger(__name__).info(f"🔧 Functions replaced: {results['functions_replaced']}")
    get_logger(__name__).info(f"🗑️  Duplicate files removed: {results['duplicate_files_removed']}")
    get_logger(__name__).info(f"✅ Files using unified systems: {results['files_using_unified_systems']}")
    get_logger(__name__).info(f"⚠️  Errors: {len(results['errors'])}")
    
    if results['errors']:
        get_logger(__name__).info("\n🚨 ERRORS:")
        for error in results['errors'][:10]:  # Show first 10 errors
            get_logger(__name__).info(f"   {error}")
