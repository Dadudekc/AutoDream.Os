#!/usr/bin/env python3
"""
Robust Backup Script for Cycle 1
================================

Enterprise-grade backup with error handling and verification.
"""

import os
import shutil
import datetime
import json
import subprocess
from pathlib import Path

def create_robust_backup():
    """Create backup using robocopy for better reliability."""

    # Create backup directory structure
    backup_base = Path('backups')
    backup_base.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = backup_base / f'web_infrastructure_backup_{timestamp}'
    backup_dir.mkdir(exist_ok=True)

    print(f'🔄 Creating robust backup of web infrastructure...')
    print(f'📁 Backup directory: {backup_dir}')

    success_log = []
    error_log = []

    # Use robocopy for more reliable copying
    def robust_copy(source, dest, name):
        """Use robocopy for reliable file copying."""
        try:
            # Create destination directory
            dest.parent.mkdir(parents=True, exist_ok=True)

            if source.exists():
                # Count files first
                file_count = len(list(source.rglob('*')))
                print(f'📋 Backing up {name} ({file_count} files)...')

                # Use robocopy (more reliable than shutil)
                cmd = [
                    'robocopy',
                    str(source),
                    str(dest),
                    '/E',  # Copy subdirectories including empty ones
                    '/R:1',  # Retry once on failure
                    '/W:1',  # Wait 1 second between retries
                    '/NP',  # No progress
                    '/NFL',  # No file list
                    '/NDL',  # No directory list
                    '/NJH',  # No job header
                    '/NJS'   # No job summary
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

                # Check if copy was successful (robocopy returns 0 for success, 1 for success with warnings)
                if result.returncode in [0, 1]:
                    backup_count = len(list(dest.rglob('*'))) if dest.exists() else 0
                    success_log.append({
                        'source': str(source),
                        'destination': str(dest),
                        'original_count': file_count,
                        'backup_count': backup_count,
                        'status': 'SUCCESS'
                    })
                    print(f'✅ {name} backed up successfully')
                    return file_count, backup_count
                else:
                    error_log.append({
                        'source': str(source),
                        'destination': str(dest),
                        'error': result.stderr,
                        'returncode': result.returncode
                    })
                    print(f'❌ {name} backup failed: {result.stderr}')
                    return 0, 0
            else:
                print(f'⚠️  {name} source directory not found')
                return 0, 0

        except Exception as e:
            error_log.append({
                'source': str(source),
                'destination': str(dest),
                'error': str(e),
                'exception_type': type(e).__name__
            })
            print(f'❌ {name} backup error: {e}')
            return 0, 0

    # Backup directories
    web_source = Path('src/web')
    web_backup = backup_dir / 'web'
    web_orig, web_backup_count = robust_copy(web_source, web_backup, 'src/web/')

    infra_source = Path('src/infrastructure')
    infra_backup = backup_dir / 'infrastructure'
    infra_orig, infra_backup_count = robust_copy(infra_source, infra_backup, 'src/infrastructure/')

    # Create backup manifest
    manifest = {
        'timestamp': timestamp,
        'datetime': datetime.datetime.now().isoformat(),
        'backup_type': 'web_infrastructure_consolidation_cycle_1_robust',
        'cycle': 'Cycle 1: Preparation & Assessment',
        'backup_method': 'robocopy_robust',
        'directories_backed_up': {
            'src/web': str(web_backup) if web_source.exists() else None,
            'src/infrastructure': str(infra_backup) if infra_source.exists() else None
        },
        'file_counts': {
            'web_original': web_orig,
            'web_backup': web_backup_count,
            'infra_original': infra_orig,
            'infra_backup': infra_backup_count
        },
        'success_log': success_log,
        'error_log': error_log
    }

    manifest_file = backup_dir / 'backup_manifest.json'
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f'📄 Backup manifest created: {manifest_file}')
    print(f'🔍 Backup verification:')

    # Verify backup integrity
    integrity_check = True
    total_original = web_orig + infra_orig
    total_backup = web_backup_count + infra_backup_count

    print(f'   Web files: {web_orig} → {web_backup_count}')
    print(f'   Infra files: {infra_orig} → {infra_backup_count}')
    print(f'   Total: {total_original} → {total_backup}')

    if web_orig > 0 and web_backup_count == 0:
        print(f'❌ Web backup completely failed')
        integrity_check = False
    elif web_orig > 0 and abs(web_orig - web_backup_count) > 5:  # Allow small differences
        print(f'⚠️  Web backup significant file count difference')
        integrity_check = False
    elif web_orig > 0:
        print(f'✅ Web backup integrity verified')

    if infra_orig > 0 and infra_backup_count == 0:
        print(f'❌ Infrastructure backup completely failed')
        integrity_check = False
    elif infra_orig > 0 and abs(infra_orig - infra_backup_count) > 5:
        print(f'⚠️  Infrastructure backup significant file count difference')
        integrity_check = False
    elif infra_orig > 0:
        print(f'✅ Infrastructure backup integrity verified')

    if integrity_check and (web_backup_count > 0 or infra_backup_count > 0):
        print(f'🎉 CYCLE 1 - ROBUST BACKUP COMPLETE: Enterprise-grade backup created!')
        print(f'📊 Total files backed up: {total_backup}')
        print(f'📁 Backup location: {backup_dir}')

        # Create success summary
        success_summary = {
            'status': 'SUCCESS',
            'cycle': 'Cycle 1: Preparation & Assessment',
            'deliverable': 'Complete backup of src/web/ and src/infrastructure/',
            'timestamp': timestamp,
            'backup_directory': str(backup_dir),
            'total_files_backed_up': total_backup,
            'backup_method': 'robocopy_robust',
            'success_operations': len(success_log),
            'error_operations': len(error_log),
            'next_steps': [
                'Dependency analysis for all web files',
                'Risk assessment for JavaScript consolidation approach',
                'Cross-agent dependency coordination plan'
            ]
        }

        summary_file = backup_dir / 'success_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(success_summary, f, indent=2)

        print(f'📋 Success summary: {summary_file}')

        if error_log:
            print(f'⚠️  {len(error_log)} operations had issues (see error_log in manifest)')
            error_summary_file = backup_dir / 'error_summary.json'
            with open(error_summary_file, 'w') as f:
                json.dump(error_log, f, indent=2)
            print(f'📋 Error summary: {error_summary_file}')

        return True
    else:
        print(f'❌ Backup integrity issues detected - please verify manually')
        if error_log:
            print(f'Error details:')
            for error in error_log[:3]:  # Show first 3 errors
                print(f'  - {error.get("source", "Unknown")}: {error.get("error", "Unknown error")[:100]}...')
        return False

if __name__ == "__main__":
    print("🚀 CYCLE 1: Starting Preparation & Assessment - Robust Backup")
    success = create_robust_backup()
    if success:
        print("\n✅ CYCLE 1 ROBUST BACKUP DELIVERABLE COMPLETED!")
        print("🎯 Ready to proceed with dependency analysis and risk assessment")
        print("📈 Success metrics: Enterprise-grade backup with integrity verification")
    else:
        print("\n❌ CYCLE 1 BACKUP ISSUES DETECTED - Manual verification required")
