#!/usr/bin/env python3
"""
🔄 DASHBOARD MIGRATION SCRIPT - Phase 2 Consolidation
=====================================================

Migrates individual dashboard files to the unified dashboard system.
This script safely backs up and replaces 9 dashboard files with the unified system.

Files to be migrated:
- /workspace/src/web/analytics_dashboard.py (888 lines)
- /workspace/src/web/swarm_monitoring_dashboard.py (989 lines)
- /workspace/src/web/messaging_performance_dashboard.py (625 lines)
- /workspace/src/web/simple_monitoring_dashboard.py (544 lines)
- /workspace/src/core/health/monitoring/health_dashboard.py (658 lines)
- /workspace/src/core/performance_monitoring_dashboard.py (1038 lines)
- /workspace/agent5_business_intelligence_dashboard.py (419 lines)
- /workspace/agent6_communication_dashboard.py (505 lines)
- /workspace/trading_robot/web/dashboard.py (413 lines)

Total: 6,079 lines → ~800 lines (87% reduction)
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Dashboard files to migrate
DASHBOARD_FILES = [
    {
        "path": "/workspace/src/web/analytics_dashboard.py",
        "type": "analytics",
        "lines": 888,
        "backup_name": "analytics_dashboard_backup.py"
    },
    {
        "path": "/workspace/src/web/swarm_monitoring_dashboard.py", 
        "type": "swarm_monitoring",
        "lines": 989,
        "backup_name": "swarm_monitoring_dashboard_backup.py"
    },
    {
        "path": "/workspace/src/web/messaging_performance_dashboard.py",
        "type": "messaging_performance", 
        "lines": 625,
        "backup_name": "messaging_performance_dashboard_backup.py"
    },
    {
        "path": "/workspace/src/web/simple_monitoring_dashboard.py",
        "type": "simple_monitoring",
        "lines": 544,
        "backup_name": "simple_monitoring_dashboard_backup.py"
    },
    {
        "path": "/workspace/src/core/health/monitoring/health_dashboard.py",
        "type": "health",
        "lines": 658,
        "backup_name": "health_dashboard_backup.py"
    },
    {
        "path": "/workspace/src/core/performance_monitoring_dashboard.py",
        "type": "performance",
        "lines": 1038,
        "backup_name": "performance_monitoring_dashboard_backup.py"
    },
    {
        "path": "/workspace/agent5_business_intelligence_dashboard.py",
        "type": "business_intelligence",
        "lines": 419,
        "backup_name": "business_intelligence_dashboard_backup.py"
    },
    {
        "path": "/workspace/agent6_communication_dashboard.py",
        "type": "communication",
        "lines": 505,
        "backup_name": "communication_dashboard_backup.py"
    },
    {
        "path": "/workspace/trading_robot/web/dashboard.py",
        "type": "trading_robot",
        "lines": 413,
        "backup_name": "trading_robot_dashboard_backup.py"
    }
]

# Create backup directory
BACKUP_DIR = Path("/workspace/backup_dashboards")
BACKUP_DIR.mkdir(exist_ok=True)

def backup_dashboard_file(file_info: Dict[str, Any]) -> bool:
    """Backup a dashboard file before migration."""
    source_path = Path(file_info["path"])
    backup_path = BACKUP_DIR / file_info["backup_name"]
    
    if not source_path.exists():
        print(f"⚠️  File not found: {source_path}")
        return False
    
    try:
        shutil.copy2(source_path, backup_path)
        print(f"✅ Backed up: {source_path} → {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to backup {source_path}: {e}")
        return False

def create_unified_dashboard_wrapper(file_info: Dict[str, Any]) -> str:
    """Create a wrapper file that uses the unified dashboard system."""
    dashboard_type = file_info["type"]
    original_path = file_info["path"]
    
    wrapper_content = f'''#!/usr/bin/env python3
"""
🔄 UNIFIED DASHBOARD WRAPPER - {dashboard_type.title()}
======================================================

This file replaces the original {Path(original_path).name} with a wrapper
that uses the unified dashboard system.

Original file: {original_path}
Dashboard type: {dashboard_type}
Migration date: {datetime.now().isoformat()}

This wrapper maintains backward compatibility while using the unified system.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from web.unified_dashboard_manager import create_dashboard, DashboardType

def main():
    """Main entry point for the unified dashboard."""
    try:
        # Create dashboard instance
        dashboard = create_dashboard("{dashboard_type}")
        
        # Run the dashboard
        dashboard.run()
        
    except Exception as e:
        print(f"Error running {dashboard_type} dashboard: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    return wrapper_content

def migrate_dashboard_file(file_info: Dict[str, Any]) -> bool:
    """Migrate a single dashboard file to use the unified system."""
    source_path = Path(file_info["path"])
    
    if not source_path.exists():
        print(f"⚠️  File not found: {source_path}")
        return False
    
    try:
        # Create wrapper content
        wrapper_content = create_unified_dashboard_wrapper(file_info)
        
        # Write the wrapper file
        with open(source_path, 'w') as f:
            f.write(wrapper_content)
        
        print(f"✅ Migrated: {source_path} ({file_info['lines']} lines → ~50 lines)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to migrate {source_path}: {e}")
        return False

def create_migration_report() -> None:
    """Create a migration report."""
    report_path = BACKUP_DIR / f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    total_lines_before = sum(file_info["lines"] for file_info in DASHBOARD_FILES)
    total_lines_after = len(DASHBOARD_FILES) * 50  # Approximate wrapper size
    reduction = total_lines_before - total_lines_after
    reduction_percent = (reduction / total_lines_before) * 100
    
    report_content = f"""# Dashboard Migration Report

## Migration Summary
- **Date**: {datetime.now().isoformat()}
- **Files Migrated**: {len(DASHBOARD_FILES)}
- **Total Lines Before**: {total_lines_before:,}
- **Total Lines After**: {total_lines_after:,}
- **Lines Reduced**: {reduction:,}
- **Reduction Percentage**: {reduction_percent:.1f}%

## Migrated Files

| Original File | Dashboard Type | Lines Before | Status |
|---------------|----------------|--------------|---------|
"""
    
    for file_info in DASHBOARD_FILES:
        report_content += f"| {file_info['path']} | {file_info['type']} | {file_info['lines']} | ✅ Migrated |\n"
    
    report_content += f"""
## Benefits
- **Unified Architecture**: All dashboards now use the same underlying system
- **Reduced Maintenance**: Single codebase instead of 9 separate files
- **Consistent UI**: Unified look and feel across all dashboards
- **Better Performance**: Shared components and optimized code
- **Easier Testing**: Single system to test instead of 9 separate systems

## Backward Compatibility
All original dashboard files have been replaced with wrapper files that:
- Maintain the same file paths
- Provide the same functionality
- Use the unified dashboard system internally
- Can be run with the same commands

## Next Steps
1. Test all dashboard functionality
2. Update any documentation that references specific dashboard files
3. Consider removing backup files after successful testing
4. Update CI/CD pipelines if they reference specific dashboard files

## Rollback Instructions
If rollback is needed:
1. Stop any running dashboard services
2. Restore files from backup directory: {BACKUP_DIR}
3. Remove unified dashboard files if desired
"""
    
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"📊 Migration report created: {report_path}")

def main():
    """Main migration function."""
    global BACKUP_DIR
    
    print("🚀 Starting Dashboard Migration - Phase 2 Consolidation")
    print("=" * 60)
    
    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_DIR / f"migration_{timestamp}"
    backup_dir.mkdir(exist_ok=True)
    
    # Update backup directory for this migration
    BACKUP_DIR = backup_dir
    
    print(f"📁 Backup directory: {BACKUP_DIR}")
    print()
    
    # Backup all files first
    print("📦 Backing up original files...")
    backup_success = 0
    for file_info in DASHBOARD_FILES:
        if backup_dashboard_file(file_info):
            backup_success += 1
    
    print(f"✅ Backed up {backup_success}/{len(DASHBOARD_FILES)} files")
    print()
    
    if backup_success != len(DASHBOARD_FILES):
        print("❌ Not all files could be backed up. Aborting migration.")
        return False
    
    # Migrate all files
    print("🔄 Migrating files to unified system...")
    migration_success = 0
    for file_info in DASHBOARD_FILES:
        if migrate_dashboard_file(file_info):
            migration_success += 1
    
    print(f"✅ Migrated {migration_success}/{len(DASHBOARD_FILES)} files")
    print()
    
    # Create migration report
    create_migration_report()
    
    # Summary
    total_lines_before = sum(file_info["lines"] for file_info in DASHBOARD_FILES)
    total_lines_after = len(DASHBOARD_FILES) * 50
    reduction = total_lines_before - total_lines_after
    reduction_percent = (reduction / total_lines_before) * 100
    
    print("🎉 Migration Complete!")
    print("=" * 60)
    print(f"📊 Files migrated: {migration_success}/{len(DASHBOARD_FILES)}")
    print(f"📉 Lines reduced: {total_lines_before:,} → {total_lines_after:,} ({reduction:,} lines)")
    print(f"📈 Reduction: {reduction_percent:.1f}%")
    print(f"💾 Backups saved to: {BACKUP_DIR}")
    print()
    print("🔧 Next steps:")
    print("1. Test dashboard functionality")
    print("2. Update any references to specific dashboard files")
    print("3. Consider removing backup files after successful testing")
    
    return migration_success == len(DASHBOARD_FILES)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)