#!/usr/bin/env python3
"""
Create Combined Devlog Export
============================

This script creates a comprehensive export of all devlogs from both
the database and file system.
"""

import json
import requests
from pathlib import Path
from datetime import datetime

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
            print(f"✅ Loaded {len(db_devlogs)} database devlogs")
    except Exception as e:
        print(f"❌ Error getting database devlogs: {e}")

    # Get file devlogs
    file_devlogs = []
    devlogs_dir = Path('devlogs')
    if devlogs_dir.exists():
        md_files = list(devlogs_dir.glob('*.md'))
        archive_files = list((devlogs_dir / 'archive').glob('*.md')) if (devlogs_dir / 'archive').exists() else []

        processed_count = 0
        for file_path in md_files + archive_files:
            try:
                filename = file_path.name
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

                        processed_count += 1

            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")

        print(f"✅ Processed {processed_count} file devlogs")

    combined_data['file_devlogs'] = file_devlogs
    combined_data['summary']['total_files'] = len(file_devlogs)
    combined_data['summary']['total_combined'] = len(db_devlogs) + len(file_devlogs)
    combined_data['summary']['agents'] = sorted(list(combined_data['summary']['agents']))

    # Save combined export
    filename = f"complete_devlog_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(combined_data, f, indent=2)

    print(f"✅ Complete export created: {filename}")
    print("📊 Summary:")
    print(f"  Database devlogs: {combined_data['summary']['total_database']}")
    print(f"  File devlogs: {combined_data['summary']['total_files']}")
    print(f"  Total: {combined_data['summary']['total_combined']}")
    print(f"  Unique agents: {len(combined_data['summary']['agents'])}")

    # Show file size
    file_size = Path(filename).stat().st_size
    print(f"  File size: {file_size} bytes")

    return filename

if __name__ == "__main__":
    print('🤖 COMPLETE DEVLOG EXPORT')
    print('=' * 30)
    create_combined_export()
    print()
    print('🎉 All devlogs have been successfully exported!')
    print('💾 The export file is ready for upload to any system.')
