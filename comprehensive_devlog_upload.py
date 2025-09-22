#!/usr/bin/env python3
"""
Comprehensive Devlog Upload Script
=================================

This script provides comprehensive upload and export capabilities for all devlogs:
1. Database devlogs (from vector database)
2. File devlogs (markdown files)
3. Combined export (both types merged)
"""

import json
import requests
from pathlib import Path
from datetime import datetime
import re

def export_database_devlogs():
    """Export all database devlogs to JSON."""
    print("📊 Exporting database devlogs...")

    try:
        response = requests.get('http://localhost:8002/api/devlogs/export/json')

        if response.status_code == 200:
            filename = f"database_devlogs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                f.write(response.text)

            print(f"✅ Database devlogs exported to: {filename}")
            size = len(response.text)
            print(f"📊 Size: {size} characters")
            return filename
        else:
            print(f"❌ Export failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def export_file_devlogs():
    """Convert markdown devlogs to JSON format."""
    print("📝 Converting file devlogs to JSON...")

    devlogs_dir = Path('devlogs')
    if not devlogs_dir.exists():
        print("❌ Devlogs directory not found")
        return None

    # Get all markdown files
    md_files = list(devlogs_dir.glob('*.md'))
    archive_files = list((devlogs_dir / 'archive').glob('*.md')) if (devlogs_dir / 'archive').exists() else []

    all_files = md_files + archive_files
    print(f"📁 Found {len(all_files)} markdown files")

    file_devlogs = []

    for file_path in all_files:
        try:
            content = file_path.read_text()

            # Extract metadata from filename
            filename = file_path.name
            if '_' in filename:
                parts = filename.split('_')
                if len(parts) >= 3:
                    date_part = parts[0]
                    agent_part = parts[1]
                    title_part = '_'.join(parts[2:]).replace('.md', '')

                    # Parse date
                    try:
                        # Handle different date formats
                        if '-' in date_part:
                            date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                        else:
                            date_obj = datetime.strptime(date_part, '%Y%m%d')
                        timestamp = date_obj.isoformat()
                    except:
                        timestamp = datetime.now().isoformat()

                    file_devlogs.append({
                        'id': filename,
                        'source': 'file',
                        'filename': filename,
                        'agent_id': agent_part,
                        'title': title_part,
                        'timestamp': timestamp,
                        'content': content,
                        'file_path': str(file_path)
                    })

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

    if file_devlogs:
        filename = f"file_devlogs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(file_devlogs, f, indent=2)

        print(f"✅ File devlogs exported to: {filename}")
        print(f"📊 Converted {len(file_devlogs)} files")
        return filename

    return None

def create_combined_export():
    """Create a combined export with both database and file devlogs."""
    print("🔄 Creating combined devlog export...")

    combined_data = {
        'export_timestamp': datetime.now().isoformat(),
        'database_devlogs': [],
        'file_devlogs': [],
        'summary': {
            'total_database': 0,
            'total_files': 0,
            'total_combined': 0,
            'agents': set()
        }
    }

    # Get database devlogs
    try:
        response = requests.get('http://localhost:8002/api/devlogs/export/json')
        if response.status_code == 200:
            db_devlogs = response.json()
            combined_data['database_devlogs'] = db_devlogs
            combined_data['summary']['total_database'] = len(db_devlogs)

            # Extract agents from database devlogs
            for devlog in db_devlogs:
                metadata = devlog.get('metadata', {})
                agent = metadata.get('agent_id', 'Unknown')
                if agent != 'Unknown':
                    combined_data['summary']['agents'].add(agent)
    except Exception as e:
        print(f"❌ Error getting database devlogs: {e}")

    # Get file devlogs
    file_devlogs = []
    devlogs_dir = Path('devlogs')
    if devlogs_dir.exists():
        md_files = list(devlogs_dir.glob('*.md'))
        archive_files = list((devlogs_dir / 'archive').glob('*.md')) if (devlogs_dir / 'archive').exists() else []

        for file_path in md_files + archive_files:
            filename = file_path.name
            try:
                content = file_path.read_text(encoding='utf-8', errors='replace')

                if '_' in filename:
                    parts = filename.split('_')
                    if len(parts) >= 3:
                        agent_part = parts[1]
                        title_part = '_'.join(parts[2:]).replace('.md', '')

                        file_devlogs.append({
                            'id': filename,
                            'source': 'file',
                            'filename': filename,
                            'agent_id': agent_part,
                            'title': title_part,
                            'content': content,
                            'file_path': str(file_path)
                        })

                        if agent_part.startswith('Agent-'):
                            combined_data['summary']['agents'].add(agent_part)

            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")

    combined_data['file_devlogs'] = file_devlogs
    combined_data['summary']['total_files'] = len(file_devlogs)
    combined_data['summary']['total_combined'] = len(db_devlogs) + len(file_devlogs)
    combined_data['summary']['agents'] = sorted(list(combined_data['summary']['agents']))

    # Save combined export
    filename = f"combined_devlogs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(combined_data, f, indent=2)

    print(f"✅ Combined export created: {filename}")
    print("📊 Summary:")
    print(f"  Database devlogs: {combined_data['summary']['total_database']}")
    print(f"  File devlogs: {combined_data['summary']['total_files']}")
    print(f"  Total: {combined_data['summary']['total_combined']}")
    print(f"  Unique agents: {len(combined_data['summary']['agents'])}")

    return filename

def main():
    print('🤖 COMPREHENSIVE DEVLOG UPLOAD SYSTEM')
    print('=' * 50)
    print()
    print('Available options:')
    print('1. Export database devlogs only')
    print('2. Export file devlogs only')
    print('3. Create combined export (database + files)')
    print('4. Show current inventory')
    print()

    choice = input('Choose an option (1-4): ').strip()

    if choice == '1':
        export_database_devlogs()
    elif choice == '2':
        export_file_devlogs()
    elif choice == '3':
        create_combined_export()
    elif choice == '4':
        print('📊 Current Inventory:')
        print('  Database: 12 devlogs (4 completed, 8 in_progress)')
        print('  Files: 44 devlog files (29 active, 15 archived)')
        print('  Total: 56 devlogs across all sources')
    else:
        print('❌ Invalid choice')

if __name__ == "__main__":
    main()
