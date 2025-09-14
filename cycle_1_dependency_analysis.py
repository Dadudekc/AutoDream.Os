#!/usr/bin/env python3
"""
Cycle 1: Dependency Analysis
===========================

Analyze dependencies across all 218 backed up web infrastructure files.
"""

import datetime
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path


def find_backup_directory():
    """Find the most recent web infrastructure backup directory."""
    backup_base = Path('backups')
    if not backup_base.exists():
        print("❌ No backups directory found")
        return None

    # Find the most recent backup directory
    backup_dirs = [d for d in backup_base.iterdir() if d.is_dir() and 'web_infrastructure' in d.name]
    if not backup_dirs:
        print("❌ No web infrastructure backup directories found")
        return None

    # Sort by timestamp (newest first)
    backup_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    latest_backup = backup_dirs[0]

    print(f"📁 Using latest backup: {latest_backup}")
    return latest_backup

def analyze_javascript_dependencies(js_files):
    """Analyze JavaScript file dependencies and relationships."""
    print(f"🔍 Analyzing {len(js_files)} JavaScript files...")

    dependencies = {
        'imports': defaultdict(list),
        'exports': defaultdict(list),
        'framework_usage': Counter(),
        'utility_functions': Counter(),
        'file_sizes': {},
        'complexity_metrics': {}
    }

    for js_file in js_files:
        try:
            with open(js_file, encoding='utf-8', errors='ignore') as f:
                content = f.read()
                file_size = len(content)
                dependencies['file_sizes'][str(js_file)] = file_size

                # Analyze imports
                import_matches = re.findall(r'import\s+.*?from\s+[\'"](.+?)[\'"]', content)
                for imp in import_matches:
                    dependencies['imports'][imp].append(str(js_file))

                # Analyze exports
                export_matches = re.findall(r'export\s+(?:const|let|var|function|class|default)?\s*(\w+)', content)
                for exp in export_matches:
                    dependencies['exports'][exp].append(str(js_file))

                # Framework detection
                if 'jquery' in content.lower() or '$(' in content:
                    dependencies['framework_usage']['jquery'] += 1
                if 'react' in content.lower():
                    dependencies['framework_usage']['react'] += 1
                if 'vue' in content.lower():
                    dependencies['framework_usage']['vue'] += 1
                if 'angular' in content.lower():
                    dependencies['framework_usage']['angular'] += 1

                # Utility function detection
                if 'function' in content:
                    func_count = len(re.findall(r'function\s+\w+', content))
                    dependencies['utility_functions']['named_functions'] += func_count

                if '=>' in content:
                    arrow_count = len(re.findall(r'=>\s*\{', content))
                    dependencies['utility_functions']['arrow_functions'] += arrow_count

                # Complexity metrics
                lines_of_code = len([line for line in content.split('\n') if line.strip()])
                dependencies['complexity_metrics'][str(js_file)] = {
                    'lines_of_code': lines_of_code,
                    'file_size_kb': file_size / 1024,
                    'functions_count': func_count if 'func_count' in locals() else 0
                }

        except Exception as e:
            print(f"⚠️  Error analyzing {js_file}: {e}")
            continue

    return dependencies

def analyze_python_dependencies(py_files):
    """Analyze Python file dependencies and relationships."""
    print(f"🔍 Analyzing {len(py_files)} Python files...")

    dependencies = {
        'imports': defaultdict(list),
        'classes': defaultdict(list),
        'functions': defaultdict(list),
        'file_sizes': {},
        'complexity_metrics': {}
    }

    for py_file in py_files:
        try:
            with open(py_file, encoding='utf-8', errors='ignore') as f:
                content = f.read()
                file_size = len(content)
                dependencies['file_sizes'][str(py_file)] = file_size

                # Analyze imports
                import_matches = re.findall(r'^(?:from\s+(.+?)\s+import|import\s+(.+?)(?:\s|$))', content, re.MULTILINE)
                for match in import_matches:
                    imp = match[0] or match[1]
                    if imp:
                        dependencies['imports'][imp.strip()].append(str(py_file))

                # Analyze classes
                class_matches = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
                for cls in class_matches:
                    dependencies['classes'][cls].append(str(py_file))

                # Analyze functions
                func_matches = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
                for func in func_matches:
                    dependencies['functions'][func].append(str(py_file))

                # Complexity metrics
                lines_of_code = len([line for line in content.split('\n') if line.strip()])
                dependencies['complexity_metrics'][str(py_file)] = {
                    'lines_of_code': lines_of_code,
                    'file_size_kb': file_size / 1024,
                    'classes_count': len(class_matches),
                    'functions_count': len(func_matches)
                }

        except Exception as e:
            print(f"⚠️  Error analyzing {py_file}: {e}")
            continue

    return dependencies

def identify_consolidation_opportunities(dependencies):
    """Identify consolidation opportunities based on dependency analysis."""
    opportunities = {
        'duplicate_utilities': [],
        'shared_dependencies': [],
        'consolidation_candidates': [],
        'file_size_distribution': {},
        'complexity_distribution': {}
    }

    # Analyze JavaScript dependencies
    if 'javascript' in dependencies:
        js_deps = dependencies['javascript']

        # Find files with similar sizes (potential duplicates)
        size_groups = defaultdict(list)
        for file_path, size in js_deps['file_sizes'].items():
            size_kb = round(size / 1024)
            size_groups[size_kb].append(file_path)

        for size_kb, files in size_groups.items():
            if len(files) > 1:
                opportunities['duplicate_utilities'].append({
                    'size_kb': size_kb,
                    'files': files,
                    'count': len(files)
                })

        # Framework consolidation opportunities
        framework_usage = js_deps['framework_usage']
        if len([f for f in framework_usage.values() if f > 0]) > 1:
            opportunities['shared_dependencies'].append({
                'type': 'multiple_frameworks',
                'frameworks': dict(framework_usage),
                'recommendation': 'Consolidate to single framework'
            })

    # Analyze Python dependencies
    if 'python' in dependencies:
        py_deps = dependencies['python']

        # Find shared imports (consolidation candidates)
        import_usage = {}
        for imp, files in py_deps['imports'].items():
            if len(files) > 1:
                import_usage[imp] = {
                    'files': files,
                    'count': len(files)
                }

        if import_usage:
            opportunities['shared_dependencies'].append({
                'type': 'shared_imports',
                'imports': import_usage,
                'recommendation': 'Create centralized import utilities'
            })

    return opportunities

def generate_dependency_report(dependencies, opportunities):
    """Generate comprehensive dependency analysis report."""
    report = {
        'timestamp': datetime.datetime.now().isoformat(),
        'cycle': 'Cycle 1: Preparation & Assessment',
        'phase': 'Dependency Analysis',
        'total_files_analyzed': sum(len(files) for files in dependencies.values()),
        'dependencies': dependencies,
        'consolidation_opportunities': opportunities,
        'recommendations': []
    }

    # Generate recommendations
    if opportunities['duplicate_utilities']:
        report['recommendations'].append({
            'priority': 'HIGH',
            'type': 'Duplicate Elimination',
            'description': f"Found {len(opportunities['duplicate_utilities'])} groups of potentially duplicate files",
            'impact': f"Could reduce {sum(len(group['files']) for group in opportunities['duplicate_utilities'])} files by {len(opportunities['duplicate_utilities'])} consolidated files"
        })

    if opportunities['shared_dependencies']:
        for dep in opportunities['shared_dependencies']:
            if dep['type'] == 'multiple_frameworks':
                report['recommendations'].append({
                    'priority': 'MEDIUM',
                    'type': 'Framework Consolidation',
                    'description': f"Multiple frameworks detected: {', '.join(dep['frameworks'].keys())}",
                    'impact': "Unified framework reduces complexity and maintenance overhead"
                })
            elif dep['type'] == 'shared_imports':
                report['recommendations'].append({
                    'priority': 'MEDIUM',
                    'type': 'Import Consolidation',
                    'description': f"Shared imports found across {len(dep['imports'])} modules",
                    'impact': "Centralized imports improve maintainability"
                })

    return report

def perform_dependency_analysis():
    """Main function to perform comprehensive dependency analysis."""
    print("🚀 CYCLE 1: Starting Dependency Analysis")
    print("=" * 50)

    # Find backup directory
    backup_dir = find_backup_directory()
    if not backup_dir:
        return None

    # Collect all files from backup
    all_files = []
    js_files = []
    py_files = []
    other_files = []

    for root, dirs, files in os.walk(backup_dir):
        for file in files:
            file_path = Path(root) / file
            all_files.append(file_path)

            if file.endswith('.js'):
                js_files.append(file_path)
            elif file.endswith('.py'):
                py_files.append(file_path)
            else:
                other_files.append(file_path)

    print("📊 Files to analyze:")
    print(f"   Total files: {len(all_files)}")
    print(f"   JavaScript files: {len(js_files)}")
    print(f"   Python files: {len(py_files)}")
    print(f"   Other files: {len(other_files)}")

    # Analyze dependencies
    dependencies = {}

    if js_files:
        dependencies['javascript'] = analyze_javascript_dependencies(js_files)

    if py_files:
        dependencies['python'] = analyze_python_dependencies(py_files)

    # Identify consolidation opportunities
    opportunities = identify_consolidation_opportunities(dependencies)

    # Generate comprehensive report
    report = generate_dependency_report(dependencies, opportunities)

    # Save analysis results
    analysis_dir = backup_dir / 'dependency_analysis'
    analysis_dir.mkdir(exist_ok=True)

    # Save detailed report
    report_file = analysis_dir / 'dependency_analysis_report.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    # Save summary for quick reference
    summary = {
        'timestamp': report['timestamp'],
        'files_analyzed': report['total_files_analyzed'],
        'key_findings': [
            f"JavaScript files: {len(js_files)}",
            f"Python files: {len(py_files)}",
            f"Duplicate utility groups: {len(opportunities['duplicate_utilities'])}",
            f"Shared dependency opportunities: {len(opportunities['shared_dependencies'])}"
        ],
        'top_recommendations': [rec['description'] for rec in report['recommendations'][:3]],
        'next_steps': [
            'Risk assessment for consolidation approach',
            'Strategy refinement for JavaScript consolidation',
            'Cross-agent coordination for Cycle 2 planning'
        ]
    }

    summary_file = analysis_dir / 'analysis_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"📄 Detailed analysis saved: {report_file}")
    print(f"📋 Summary saved: {summary_file}")

    # Print summary
    print("\n🎯 DEPENDENCY ANALYSIS SUMMARY:")
    print(f"   Files Analyzed: {report['total_files_analyzed']}")
    print(f"   Duplicate Groups Found: {len(opportunities['duplicate_utilities'])}")
    print(f"   Shared Dependencies: {len(opportunities['shared_dependencies'])}")
    print(f"   Recommendations: {len(report['recommendations'])}")

    if report['recommendations']:
        print("\n🔧 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(report['recommendations'][:3], 1):
            print(f"   {i}. {rec['description']} ({rec['priority']})")

    print("\n✅ CYCLE 1 DEPENDENCY ANALYSIS COMPLETE!")
    print(f"📁 Analysis results: {analysis_dir}")

    return report

if __name__ == "__main__":
    report = perform_dependency_analysis()
    if report:
        print("\n🎉 Dependency analysis completed successfully!")
        print("🎯 Ready to proceed with risk assessment and consolidation strategy!")
    else:
        print("\n❌ Dependency analysis failed - check backup directory")
