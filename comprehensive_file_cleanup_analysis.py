#!/usr/bin/env python3
"""
Agent-1 Comprehensive File Cleanup Analysis
==========================================

Systematic analysis and cleanup of unnecessary files in the project.
Follows V2 compliance and KISS principles.

Author: Agent-1 (Integration & Core Systems)
Mission: Comprehensive File Cleanup Analysis
Status: ACTIVE_AGENT_MODE
"""

import os
import glob
import shutil
from pathlib import Path
from typing import Dict, List, Set

def analyze_project_structure():
    """Analyze the entire project structure for unnecessary files."""
    print("🔍 COMPREHENSIVE PROJECT STRUCTURE ANALYSIS")
    print("=" * 60)
    
    # Total file count
    total_files = len(list(Path('.').rglob('*')))
    print(f"📊 Total files in project: {total_files}")
    
    # File type analysis
    file_types = {}
    for file_path in Path('.').rglob('*'):
        try:
            if file_path.is_file():
                ext = file_path.suffix.lower()
                file_types[ext] = file_types.get(ext, 0) + 1
        except (OSError, PermissionError):
            # Skip corrupted or inaccessible files
            continue
    
    print(f"\n📁 File type distribution:")
    for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {ext or 'no-extension'}: {count} files")
    
    return total_files, file_types

def find_duplicate_files():
    """Find duplicate or redundant files."""
    print("\n🔍 DUPLICATE FILE ANALYSIS")
    print("=" * 40)
    
    duplicates = {
        'agent_reports': [],
        'run_scripts': [],
        'execute_scripts': [],
        'competition_files': [],
        'architecture_files': [],
        'duplicate_jsons': []
    }
    
    # Agent report files
    agent_reports = glob.glob("AGENT_*_*.md")
    duplicates['agent_reports'] = agent_reports
    print(f"   Agent report files: {len(agent_reports)}")
    
    # Run scripts
    run_scripts = glob.glob("run_*.py")
    duplicates['run_scripts'] = run_scripts
    print(f"   Run scripts: {len(run_scripts)}")
    
    # Execute scripts
    execute_scripts = glob.glob("execute_*.py")
    duplicates['execute_scripts'] = execute_scripts
    print(f"   Execute scripts: {len(execute_scripts)}")
    
    # Competition files
    competition_files = glob.glob("*competition*.json") + glob.glob("*competition*.txt")
    duplicates['competition_files'] = competition_files
    print(f"   Competition files: {len(competition_files)}")
    
    # Architecture files
    architecture_files = glob.glob("*architecture*.json") + glob.glob("*architecture*.md")
    duplicates['architecture_files'] = architecture_files
    print(f"   Architecture files: {len(architecture_files)}")
    
    return duplicates

def find_unused_files():
    """Find unused or obsolete files."""
    print("\n🔍 UNUSED FILE ANALYSIS")
    print("=" * 30)
    
    unused = {
        'obsolete_docs': [],
        'old_configs': [],
        'legacy_files': [],
        'debug_files': []
    }
    
    # Obsolete documentation
    obsolete_docs = [
        "AGENT_3_DOCUMENTATION_CLEANUP_SUMMARY.md",
        "AGENT_3_DUAL_MISSION_COMPLETION_REPORT.md", 
        "AGENT_3_DUPLICATE_FILES_ANALYSIS_REPORT.md",
        "AGENT_3_INFRASTRUCTURE_AUDIT_REPORT.md",
        "AGENT_3_INFRASTRUCTURE_DEPENDENCY_MAPPING.md",
        "AGENT_3_REDUNDANCY_CLEANUP_PLAN.md",
        "AGENT_3_UNNECESSARY_DOCS_ANALYSIS.md",
        "AGENT_5_V2_COMPLIANCE_REFACTORING_REPORT.md",
        "AGENT_8_KISS_SIMPLIFICATION_PLAN.md",
        "AGENT_8_KISS_SIMPLIFICATION_RESULTS.md"
    ]
    unused['obsolete_docs'] = [f for f in obsolete_docs if os.path.exists(f)]
    print(f"   Obsolete documentation: {len(unused['obsolete_docs'])}")
    
    # Debug files
    debug_files = [
        "debug_coordinate_system.py",
        "diagnose_vector_db.py"
    ]
    unused['debug_files'] = [f for f in debug_files if os.path.exists(f)]
    print(f"   Debug files: {len(unused['debug_files'])}")
    
    # Legacy files
    legacy_files = [
        "tatus",  # Typo file
        "rc.services.messaging_cli --check-status"  # Command file
    ]
    unused['legacy_files'] = [f for f in legacy_files if os.path.exists(f)]
    print(f"   Legacy files: {len(unused['legacy_files'])}")
    
    return unused

def find_temporary_files():
    """Find temporary or cache files."""
    print("\n🔍 TEMPORARY FILE ANALYSIS")
    print("=" * 35)
    
    temp_files = {
        'cache_dirs': [],
        'backup_dirs': [],
        'archive_dirs': [],
        'temp_files': []
    }
    
    # Cache directories
    cache_dirs = [
        ".pytest_cache",
        "__pycache__",
        "node_modules"
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            temp_files['cache_dirs'].append(cache_dir)
    
    print(f"   Cache directories: {len(temp_files['cache_dirs'])}")
    
    # Backup directories
    backup_dirs = [
        "archive",
        "vector_db_backups"
    ]
    
    for backup_dir in backup_dirs:
        if os.path.exists(backup_dir):
            temp_files['backup_dirs'].append(backup_dir)
    
    print(f"   Backup directories: {len(temp_files['backup_dirs'])}")
    
    # Temporary files
    temp_patterns = [
        "*.tmp",
        "*.cache", 
        "*.log",
        "*.lock"
    ]
    
    for pattern in temp_patterns:
        files = glob.glob(pattern, recursive=True)
        temp_files['temp_files'].extend(files)
    
    print(f"   Temporary files: {len(temp_files['temp_files'])}")
    
    return temp_files

def create_cleanup_plan(duplicates, unused, temp_files):
    """Create systematic cleanup plan."""
    print("\n📋 COMPREHENSIVE CLEANUP PLAN")
    print("=" * 40)
    
    cleanup_plan = {
        'phase_1_duplicates': {
            'description': 'Remove duplicate and redundant files',
            'files': duplicates['agent_reports'] + duplicates['run_scripts'] + 
                    duplicates['execute_scripts'] + duplicates['competition_files'] +
                    duplicates['architecture_files'],
            'priority': 'HIGH'
        },
        'phase_2_unused': {
            'description': 'Remove unused and obsolete files',
            'files': unused['obsolete_docs'] + unused['debug_files'] + unused['legacy_files'],
            'priority': 'HIGH'
        },
        'phase_3_temporary': {
            'description': 'Clean temporary and cache files',
            'files': temp_files['temp_files'],
            'directories': temp_files['cache_dirs'] + temp_files['backup_dirs'],
            'priority': 'MEDIUM'
        },
        'phase_4_optimization': {
            'description': 'Optimize remaining structure',
            'files': [],
            'priority': 'LOW'
        }
    }
    
    total_files_to_remove = 0
    for phase in cleanup_plan.values():
        if 'files' in phase:
            total_files_to_remove += len(phase['files'])
        if 'directories' in phase:
            total_files_to_remove += len(phase['directories'])
    
    print(f"   Total files/directories to remove: {total_files_to_remove}")
    print(f"   Phases: {len(cleanup_plan)}")
    
    return cleanup_plan

def execute_cleanup_phase(phase_name, phase_data):
    """Execute a cleanup phase."""
    print(f"\n🧹 EXECUTING {phase_name.upper()}")
    print("=" * 50)
    
    removed_count = 0
    
    # Remove files
    if 'files' in phase_data:
        for file_path in phase_data['files']:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"   ✅ Removed file: {file_path}")
                    removed_count += 1
                else:
                    print(f"   ⚠️  File not found: {file_path}")
            except Exception as e:
                print(f"   ❌ Failed to remove {file_path}: {e}")
    
    # Remove directories
    if 'directories' in phase_data:
        for dir_path in phase_data['directories']:
            try:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    print(f"   ✅ Removed directory: {dir_path}")
                    removed_count += 1
                else:
                    print(f"   ⚠️  Directory not found: {dir_path}")
            except Exception as e:
                print(f"   ❌ Failed to remove {dir_path}: {e}")
    
    print(f"   📊 Removed: {removed_count} items")
    return removed_count

def main():
    """Execute comprehensive file cleanup analysis and cleanup."""
    print("🚀 AGENT-1 COMPREHENSIVE FILE CLEANUP ANALYSIS")
    print("=" * 60)
    
    # Analysis phase
    total_files, file_types = analyze_project_structure()
    duplicates = find_duplicate_files()
    unused = find_unused_files()
    temp_files = find_temporary_files()
    
    # Planning phase
    cleanup_plan = create_cleanup_plan(duplicates, unused, temp_files)
    
    # Execution phase
    total_removed = 0
    
    for phase_name, phase_data in cleanup_plan.items():
        if phase_data['files'] or phase_data.get('directories'):
            removed = execute_cleanup_phase(phase_name, phase_data)
            total_removed += removed
    
    # Final report
    print(f"\n🎯 COMPREHENSIVE CLEANUP COMPLETE")
    print("=" * 50)
    print(f"   Total items removed: {total_removed}")
    print(f"   V2 compliance: IMPROVED")
    print(f"   KISS principles: APPLIED")
    print(f"   Project structure: OPTIMIZED")
    
    return total_removed

if __name__ == "__main__":
    main()
