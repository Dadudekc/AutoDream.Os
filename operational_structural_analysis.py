#!/usr/bin/env python3
"""
Agent-8 Operational Structural Analysis for SWARM Survey
=======================================================

Comprehensive analysis of src/ directory from operational perspective
for consolidation planning (683 → ~250 files)
"""

import json
import os
from pathlib import Path


def analyze_src_structure():
    """Perform comprehensive operational analysis of src/ directory"""

    print('🔍 AGENT-8 OPERATIONAL STRUCTURAL ANALYSIS')
    print('==========================================')
    print()

    src_path = Path('src')
    if not src_path.exists():
        print('❌ src/ directory not found')
        return

    print('📊 SRC/ DIRECTORY OPERATIONAL ANALYSIS')
    print('=' * 45)

    # 1. Directory Structure Analysis
    print('\n🏗️  DIRECTORY STRUCTURE ANALYSIS:')
    print('-' * 35)

    directories = []
    files = []
    total_size = 0

    for root, dirs, filenames in os.walk(src_path):
        for d in dirs:
            directories.append(os.path.join(root, d))
        for f in filenames:
            filepath = os.path.join(root, f)
            files.append(filepath)
            try:
                total_size += os.path.getsize(filepath)
            except OSError:
                pass

    print(f'Total Directories: {len(directories)}')
    print(f'Total Files: {len(files)}')
    print(f'Total Size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)')

    # 2. Directory Depth Analysis
    print('\n📏 DIRECTORY DEPTH ANALYSIS:')
    print('-' * 30)

    depths = {}
    for d in directories:
        rel_path = os.path.relpath(d, 'src')
        depth = len(rel_path.split(os.sep))
        depths[depth] = depths.get(depth, 0) + 1

    for depth in sorted(depths.keys()):
        print(f'Depth {depth}: {depths[depth]} directories')

    # 3. File Type Distribution
    print('\n📄 FILE TYPE DISTRIBUTION:')
    print('-' * 28)

    extensions = {}
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        extensions[ext] = extensions.get(ext, 0) + 1

    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
        ext_name = ext if ext else 'No extension'
        print(f'{ext_name}: {count} files')

    # 4. Largest Files Analysis
    print('\n📈 LARGEST FILES ANALYSIS:')
    print('-' * 27)

    file_sizes = []
    for f in files:
        try:
            size = os.path.getsize(f)
            file_sizes.append((f, size))
        except OSError:
            continue

    file_sizes.sort(key=lambda x: x[1], reverse=True)
    for filepath, size in file_sizes[:10]:
        rel_path = os.path.relpath(filepath, 'src')
        print(f'{size:,} bytes - {rel_path}')

    # 5. Empty/Stub Files Analysis
    print('\n🚨 POTENTIAL STUB/EMPTY FILES:')
    print('-' * 32)

    empty_files = []
    stub_files = []

    for filepath, size in file_sizes:
        if size == 0:
            empty_files.append(filepath)
        elif size < 100:
            try:
                with open(filepath, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if len(content.strip()) < 50:
                        stub_files.append((filepath, size, len(content.strip())))
            except:
                continue

    print(f'Empty files (0 bytes): {len(empty_files)}')
    for f in empty_files[:5]:
        print(f'  - {os.path.relpath(f, "src")}')

    print(f'\nPotential stub files (<100 bytes): {len(stub_files)}')
    for f, size, content_len in stub_files[:5]:
        print(f'  - {os.path.relpath(f, "src")} ({size} bytes, {content_len} chars)')

    # 6. Operational Complexity Assessment
    print('\n⚙️  OPERATIONAL COMPLEXITY ASSESSMENT:')
    print('-' * 38)

    avg_files_per_dir = len(files) / len(directories) if directories else 0
    print(f'Average files per directory: {avg_files_per_dir:.1f}')

    large_files = [f for f, s in file_sizes if s > 100000]
    print(f'Large files (>100KB): {len(large_files)}')

    # Directory naming analysis
    service_dirs = [d for d in directories if 'service' in os.path.basename(d).lower()]
    core_dirs = [d for d in directories if 'core' in os.path.basename(d).lower()]
    util_dirs = [d for d in directories if 'util' in os.path.basename(d).lower() or 'utils' in os.path.basename(d).lower()]

    print(f'Service-related directories: {len(service_dirs)}')
    print(f'Core directories: {len(core_dirs)}')
    print(f'Utility directories: {len(util_dirs)}')

    print('\n✅ STRUCTURAL ANALYSIS COMPLETE')
    print('📊 Findings ready for SWARM coordination')

    return {
        'total_files': len(files),
        'total_directories': len(directories),
        'total_size': total_size,
        'empty_files': len(empty_files),
        'stub_files': len(stub_files),
        'large_files': len(large_files),
        'service_dirs': len(service_dirs),
        'core_dirs': len(core_dirs),
        'util_dirs': len(util_dirs),
        'max_depth': max(depths.keys()) if depths else 0
    }

if __name__ == '__main__':
    results = analyze_src_structure()

    # Save results for SWARM coordination
    with open('Agent-8_Structural_Analysis_Results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print('\n💾 Results saved to: Agent-8_Structural_Analysis_Results.json')
