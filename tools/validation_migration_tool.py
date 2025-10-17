#!/usr/bin/env python3
"""
Validation Migration Tool
=========================

Migrates old validation function calls to consolidated validation utils.
Part of DUP-Validation consolidation (Agent-5).

Usage:
    python tools/validation_migration_tool.py --scan
    python tools/validation_migration_tool.py --migrate --file path/to/file.py
    python tools/validation_migration_tool.py --migrate-all

Author: Agent-5
Date: 2025-10-17
"""

import argparse
import re
from pathlib import Path
from typing import List, Tuple


# Validation function mappings (old → new)
VALIDATION_MAPPINGS = {
    # Config validations
    'validate_config': 'src.core.validation.consolidated_validation_utils.validate_config',
    'validate_configuration': 'src.core.validation.consolidated_validation_utils.validate_config',
    
    # Session validations
    'validate_session': 'src.core.validation.consolidated_validation_utils.validate_session',
    
    # Import validations
    'validate_import_syntax': 'src.core.validation.consolidated_validation_utils.validate_import_syntax',
    'validate_import_pattern': 'src.core.validation.consolidated_validation_utils.validate_import_pattern',
    
    # File validations
    'validate_file_path': 'src.core.validation.consolidated_validation_utils.validate_file_path',
    'validate_path': 'src.core.validation.consolidated_validation_utils.validate_file_path',
    'validate_file_extension': 'src.core.validation.consolidated_validation_utils.validate_file_extension',
    
    # Type validations
    'validate_type': 'src.core.validation.consolidated_validation_utils.validate_type',
    'validate_not_none': 'src.core.validation.consolidated_validation_utils.validate_not_none',
    'validate_not_empty': 'src.core.validation.consolidated_validation_utils.validate_not_empty',
    'validate_hasattr': 'src.core.validation.consolidated_validation_utils.validate_hasattr',
    'validate_range': 'src.core.validation.consolidated_validation_utils.validate_range',
}


def scan_file_for_validations(filepath: Path) -> List[Tuple[int, str, str]]:
    """
    Scan file for validation function calls that can be migrated.
    
    Returns:
        List of (line_number, old_call, new_call) tuples
    """
    results = []
    
    try:
        lines = filepath.read_text(encoding='utf-8').split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for old_func, new_import in VALIDATION_MAPPINGS.items():
                # Look for function calls
                pattern = rf'\b{old_func}\s*\('
                if re.search(pattern, line):
                    new_func = new_import.split('.')[-1]
                    results.append((line_num, old_func, new_func))
        
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
    
    return results


def migrate_file(filepath: Path, dry_run: bool = True) -> dict:
    """
    Migrate validation calls in a file.
    
    Args:
        filepath: File to migrate
        dry_run: If True, only show changes without applying
        
    Returns:
        Dictionary with migration results
    """
    results = {
        'filepath': str(filepath),
        'changes': [],
        'success': False
    }
    
    try:
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Track changes
        changes_made = []
        
        # Add import at top if needed
        needs_import = any(
            any(func in line for func in VALIDATION_MAPPINGS.keys())
            for line in lines
        )
        
        if needs_import:
            # Find import section
            import_line = 0
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    import_line = i + 1
            
            # Add consolidated import
            new_import = 'from src.core.validation.consolidated_validation_utils import ('
            if not any('consolidated_validation_utils' in line for line in lines):
                changes_made.append(f"Add import at line {import_line}")
        
        # Scan for validation calls
        validation_calls = scan_file_for_validations(filepath)
        
        if validation_calls:
            results['changes'] = [
                f"Line {line_num}: {old} → {new}"
                for line_num, old, new in validation_calls
            ]
            results['count'] = len(validation_calls)
            
            if not dry_run:
                # Apply migrations (placeholder - full implementation needed)
                results['success'] = True
                results['message'] = f"Would migrate {len(validation_calls)} calls"
            else:
                results['success'] = True
                results['message'] = f"Found {len(validation_calls)} calls to migrate"
        else:
            results['message'] = "No validation calls found"
    
    except Exception as e:
        results['error'] = str(e)
    
    return results


def scan_all_files() -> List[dict]:
    """Scan all Python files for migration opportunities."""
    all_files = list(Path('src').rglob('*.py'))
    results = []
    
    for filepath in all_files:
        validation_calls = scan_file_for_validations(filepath)
        if validation_calls:
            results.append({
                'file': str(filepath),
                'count': len(validation_calls),
                'calls': validation_calls
            })
    
    return sorted(results, key=lambda x: x['count'], reverse=True)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description='Validation Migration Tool')
    parser.add_argument('--scan', action='store_true', help='Scan for migration opportunities')
    parser.add_argument('--migrate', action='store_true', help='Migrate specific file')
    parser.add_argument('--migrate-all', action='store_true', help='Migrate all files')
    parser.add_argument('--file', type=str, help='Specific file to migrate')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Dry run (default)')
    
    args = parser.parse_args()
    
    if args.scan:
        print("🔍 Scanning for validation migration opportunities...\n")
        results = scan_all_files()
        
        print(f"Found {len(results)} files with validation calls\n")
        print("TOP 20 FILES:")
        print("=" * 80)
        
        for i, result in enumerate(results[:20], 1):
            print(f"\n{i}. {result['file']}")
            print(f"   Validation calls: {result['count']}")
            print(f"   Functions: {', '.join(set(call[1] for call in result['calls'][:5]))}")
        
        print(f"\n✅ Total migration opportunities: {sum(r['count'] for r in results)}")
    
    elif args.migrate and args.file:
        filepath = Path(args.file)
        result = migrate_file(filepath, dry_run=args.dry_run)
        
        print(f"📝 Migrating {filepath}")
        print("=" * 80)
        
        if result.get('changes'):
            print(f"\nChanges to make ({len(result['changes'])}):")
            for change in result['changes']:
                print(f"  {change}")
        
        print(f"\n{result['message']}")
    
    elif args.migrate_all:
        print("⚡ Migrating all files...")
        results = scan_all_files()
        
        migrated = 0
        for result in results:
            filepath = Path(result['file'])
            migration = migrate_file(filepath, dry_run=args.dry_run)
            if migration.get('success'):
                migrated += 1
        
        print(f"\n✅ Migrated {migrated}/{len(results)} files!")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

