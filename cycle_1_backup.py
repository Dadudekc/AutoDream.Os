#!/usr/bin/env python3
"""
Cycle 1: Preparation & Assessment - Comprehensive Backup
=======================================================

Create enterprise-grade backup of web infrastructure for consolidation.
"""

import os
import shutil
import datetime
import json
from pathlib import Path

def create_comprehensive_backup():
    """Create comprehensive backup of web infrastructure directories."""

    # Create backup directory structure
    backup_base = Path('backups')
    backup_base.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = backup_base / f'web_infrastructure_backup_{timestamp}'
    backup_dir.mkdir(exist_ok=True)

    print(f'🔄 Creating comprehensive backup of web infrastructure...')
    print(f'📁 Backup directory: {backup_dir}')

    # Backup src/web/ directory
    web_source = Path('src/web')
    web_backup = backup_dir / 'web'
    web_count = 0
    if web_source.exists():
        web_count = len(list(web_source.rglob('*')))
        print(f'📋 Backing up src/web/ ({web_count} files)...')
        shutil.copytree(web_source, web_backup)
        print(f'✅ src/web/ backed up to {web_backup}')
    else:
        print(f'⚠️  src/web/ directory not found')

    # Backup src/infrastructure/ directory
    infra_source = Path('src/infrastructure')
    infra_backup = backup_dir / 'infrastructure'
    infra_count = 0
    if infra_source.exists():
        infra_count = len(list(infra_source.rglob('*')))
        print(f'📋 Backing up src/infrastructure/ ({infra_count} files)...')
        shutil.copytree(infra_source, infra_backup)
        print(f'✅ src/infrastructure/ backed up to {infra_backup}')
    else:
        print(f'⚠️  src/infrastructure/ directory not found')

    # Create backup manifest
    manifest = {
        'timestamp': timestamp,
        'datetime': datetime.datetime.now().isoformat(),
        'backup_type': 'web_infrastructure_consolidation_cycle_1',
        'cycle': 'Cycle 1: Preparation & Assessment',
        'directories_backed_up': {
            'src/web': str(web_backup) if web_source.exists() else None,
            'src/infrastructure': str(infra_backup) if infra_source.exists() else None
        },
        'file_counts': {
            'web_original': web_count,
            'web_backup': len(list(web_backup.rglob('*'))) if web_backup.exists() else 0,
            'infra_original': infra_count,
            'infra_backup': len(list(infra_backup.rglob('*'))) if infra_backup.exists() else 0
        }
    }

    manifest_file = backup_dir / 'backup_manifest.json'
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f'📄 Backup manifest created: {manifest_file}')
    print(f'🔍 Backup verification:')

    # Verify backup integrity
    integrity_check = True
    web_backup_count = len(list(web_backup.rglob('*'))) if web_backup.exists() else 0
    infra_backup_count = len(list(infra_backup.rglob('*'))) if infra_backup.exists() else 0

    print(f'   Web files: {web_count} → {web_backup_count}')
    print(f'   Infra files: {infra_count} → {infra_backup_count}')

    if web_source.exists() and web_backup.exists():
        if web_count != web_backup_count:
            print(f'⚠️  Web backup file count mismatch!')
            integrity_check = False
        else:
            print(f'✅ Web backup integrity verified')

    if infra_source.exists() and infra_backup.exists():
        if infra_count != infra_backup_count:
            print(f'⚠️  Infrastructure backup file count mismatch!')
            integrity_check = False
        else:
            print(f'✅ Infrastructure backup integrity verified')

    if integrity_check:
        print(f'🎉 CYCLE 1 - BACKUP COMPLETE: Enterprise-grade backup created successfully!')
        print(f'📊 Total files backed up: {web_backup_count + infra_backup_count}')
        print(f'📁 Backup location: {backup_dir}')

        # Create success summary
        success_summary = {
            'status': 'SUCCESS',
            'cycle': 'Cycle 1: Preparation & Assessment',
            'deliverable': 'Complete backup of src/web/ and src/infrastructure/',
            'timestamp': timestamp,
            'backup_directory': str(backup_dir),
            'total_files_backed_up': web_backup_count + infra_backup_count,
            'next_steps': [
                'Dependency analysis for all 170 web files',
                'Risk assessment for JavaScript consolidation approach',
                'Cross-agent dependency coordination plan'
            ]
        }

        summary_file = backup_dir / 'success_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(success_summary, f, indent=2)

        print(f'📋 Success summary: {summary_file}')
        return True
    else:
        print(f'❌ Backup integrity issues detected - please verify manually')
        return False

if __name__ == "__main__":
    print("🚀 CYCLE 1: Starting Preparation & Assessment - Comprehensive Backup")
    success = create_comprehensive_backup()
    if success:
        print("\n✅ CYCLE 1 BACKUP DELIVERABLE COMPLETED!")
        print("🎯 Ready to proceed with dependency analysis and risk assessment")
    else:
        print("\n❌ CYCLE 1 BACKUP ISSUES DETECTED - Manual verification required")
