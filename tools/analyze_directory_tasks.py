#!/usr/bin/env python3
"""
Directory Analysis Task System - V2 Compliant
============================================

Analyzes all directories and files to determine what's actually needed
for inter-agent coordination. Creates tasks for agents to review and clean up.

Author: Agent-4 (Captain)
License: MIT
"""

import os
import json
from pathlib import Path
from collections import defaultdict


def analyze_directory_structure():
    """Analyze the entire directory structure and create review tasks."""
    root = Path(".")
    
    # Directory analysis
    directory_stats = defaultdict(lambda: {'files': 0, 'size': 0, 'types': set()})
    file_types = defaultdict(int)
    total_files = 0
    
    print("🔍 Analyzing directory structure...")
    
    for file_path in root.rglob("*"):
        if file_path.is_file():
            total_files += 1
            file_type = file_path.suffix or 'no_extension'
            file_types[file_type] += 1
            
            # Get directory
            dir_path = str(file_path.parent)
            directory_stats[dir_path]['files'] += 1
            directory_stats[dir_path]['types'].add(file_type)
            
            try:
                directory_stats[dir_path]['size'] += file_path.stat().st_size
            except:
                pass
    
    # Create task assignments
    tasks = []
    
    # High-priority cleanup tasks
    high_priority_dirs = [
        'src/ml', 'src/services', 'src/core', 'src/integration',
        'devlogs', 'reports', 'analysis', 'analytics'
    ]
    
    for dir_path in high_priority_dirs:
        if dir_path in directory_stats:
            stats = directory_stats[dir_path]
            tasks.append({
                'task_id': f"CLEANUP_{dir_path.replace('/', '_').upper()}",
                'directory': dir_path,
                'file_count': stats['files'],
                'file_types': list(stats['types']),
                'priority': 'HIGH',
                'agent': 'Agent-7',  # Implementation agent
                'description': f"Review and clean up {dir_path} directory with {stats['files']} files",
                'action': 'REVIEW_AND_CLEANUP'
            })
    
    # Medium-priority review tasks
    medium_priority_dirs = [
        'src/architecture', 'src/domain', 'src/monitoring',
        'src/observability', 'src/tracing', 'src/validation'
    ]
    
    for dir_path in medium_priority_dirs:
        if dir_path in directory_stats:
            stats = directory_stats[dir_path]
            tasks.append({
                'task_id': f"REVIEW_{dir_path.replace('/', '_').upper()}",
                'directory': dir_path,
                'file_count': stats['files'],
                'file_types': list(stats['types']),
                'priority': 'MEDIUM',
                'agent': 'Agent-6',  # Quality agent
                'description': f"Review {dir_path} directory for necessity",
                'action': 'REVIEW_ONLY'
            })
    
    # Low-priority analysis tasks
    low_priority_dirs = [
        'src/team_beta', 'src/v3', 'src/aletheia',
        'browser_service', 'swarm_brain'
    ]
    
    for dir_path in low_priority_dirs:
        if dir_path in directory_stats:
            stats = directory_stats[dir_path]
            tasks.append({
                'task_id': f"ANALYZE_{dir_path.replace('/', '_').upper()}",
                'directory': dir_path,
                'file_count': stats['files'],
                'file_types': list(stats['types']),
                'priority': 'LOW',
                'agent': 'Agent-8',  # SSOT Manager
                'description': f"Analyze {dir_path} directory for integration needs",
                'action': 'ANALYZE_ONLY'
            })
    
    # Create summary report
    summary = {
        'total_files': total_files,
        'total_directories': len(directory_stats),
        'file_type_breakdown': dict(file_types),
        'largest_directories': sorted(
            [(dir_path, stats['files']) for dir_path, stats in directory_stats.items()],
            key=lambda x: x[1],
            reverse=True
        )[:20],
        'tasks_created': len(tasks),
        'tasks_by_agent': {
            'Agent-6': len([t for t in tasks if t['agent'] == 'Agent-6']),
            'Agent-7': len([t for t in tasks if t['agent'] == 'Agent-7']),
            'Agent-8': len([t for t in tasks if t['agent'] == 'Agent-8'])
        }
    }
    
    return tasks, summary


def create_task_assignments(tasks, summary):
    """Create task assignments for agents."""
    
    # Save tasks to file
    with open('DIRECTORY_REVIEW_TASKS.json', 'w') as f:
        json.dump({
            'summary': summary,
            'tasks': tasks,
            'created_by': 'Agent-4',
            'created_at': '2025-01-01T00:00:00Z'
        }, f, indent=2)
    
    # Create individual task files for each agent
    for agent in ['Agent-6', 'Agent-7', 'Agent-8']:
        agent_tasks = [t for t in tasks if t['agent'] == agent]
        if agent_tasks:
            with open(f'{agent}_DIRECTORY_REVIEW_TASKS.json', 'w') as f:
                json.dump({
                    'agent': agent,
                    'tasks': agent_tasks,
                    'total_tasks': len(agent_tasks),
                    'assigned_by': 'Agent-4'
                }, f, indent=2)
    
    return len(tasks)


def main():
    """Main execution function."""
    print("🚀 Starting directory analysis task system...")
    
    # Analyze directory structure
    tasks, summary = analyze_directory_structure()
    
    # Create task assignments
    total_tasks = create_task_assignments(tasks, summary)
    
    # Print summary
    print(f"\n✅ Analysis complete!")
    print(f"  📊 Total files: {summary['total_files']:,}")
    print(f"  📁 Total directories: {summary['total_directories']}")
    print(f"  🎯 Tasks created: {total_tasks}")
    print(f"  👥 Tasks by agent:")
    for agent, count in summary['tasks_by_agent'].items():
        print(f"    {agent}: {count} tasks")
    
    print(f"\n📋 Top 10 largest directories:")
    for dir_path, file_count in summary['largest_directories'][:10]:
        print(f"  {dir_path}: {file_count:,} files")
    
    print(f"\n🎯 Next steps:")
    print(f"  1. Review DIRECTORY_REVIEW_TASKS.json")
    print(f"  2. Assign tasks to agents via messaging system")
    print(f"  3. Agents review and clean up unnecessary files")
    print(f"  4. Target: Reduce from {summary['total_files']:,} to ~500 essential files")
    
    return summary


if __name__ == "__main__":
    main()
