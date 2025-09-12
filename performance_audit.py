#!/usr/bin/env python3
"""
Performance Audit Script for Agent-1 Mission
===========================================

Comprehensive performance analysis tool to identify bottlenecks,
memory usage issues, and optimization opportunities.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import cProfile
import io
import logging
import os
import pstats
import sys
import tracemalloc
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import psutil

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PerformanceAuditor:
    """Comprehensive performance auditing tool"""

    def __init__(self):
        self.results = {}
        self.project_root = Path(__file__).parent

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage statistics"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()

        return {
            'rss': memory_info.rss / 1024 / 1024,  # MB
            'vms': memory_info.vms / 1024 / 1024,  # MB
            'percent': process.memory_percent(),
            'cpu_percent': process.cpu_percent(interval=1.0)
        }

    def profile_module_import(self, module_path: str) -> Dict[str, Any]:
        """Profile the import time and memory usage of a module"""
        module_name = module_path.replace('/', '.').replace('\\', '.').replace('.py', '')

        # Start memory tracking
        tracemalloc.start()
        initial_memory = self.get_memory_usage()

        # Profile the import
        pr = cProfile.Profile()
        pr.enable()

        try:
            start_time = datetime.now()
            __import__(module_name)
            import_time = (datetime.now() - start_time).total_seconds() * 1000  # ms
        except ImportError as e:
            logger.warning(f"Failed to import {module_name}: {e}")
            return {'error': str(e)}

        pr.disable()

        # Get memory usage after import
        final_memory = self.get_memory_usage()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Get profiling stats
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(10)  # Top 10 functions
        profile_output = s.getvalue()

        return {
            'module': module_name,
            'import_time_ms': import_time,
            'memory_delta_mb': final_memory['rss'] - initial_memory['rss'],
            'peak_memory_mb': peak / 1024 / 1024,
            'cpu_percent': final_memory['cpu_percent'],
            'profile_stats': profile_output,
            'success': True
        }

    def find_large_files(self, min_lines: int = 400) -> List[Dict[str, Any]]:
        """Find Python files that exceed the line limit"""
        large_files = []

        for py_file in self.project_root.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    if len(lines) > min_lines:
                        large_files.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'lines': len(lines),
                            'size_kb': py_file.stat().st_size / 1024
                        })
            except Exception as e:
                logger.warning(f"Error reading {py_file}: {e}")

        return sorted(large_files, key=lambda x: x['lines'], reverse=True)

    def audit_imports(self) -> Dict[str, Any]:
        """Audit import patterns for optimization opportunities"""
        import_issues = {
            'unused_imports': [],
            'wildcard_imports': [],
            'circular_imports': [],
            'heavy_imports': []
        }

        # This is a basic implementation - could be enhanced with ast parsing
        heavy_modules = [
            'tensorflow', 'torch', 'pandas', 'numpy', 'matplotlib',
            'scipy', 'sklearn', 'PIL', 'opencv', 'requests'
        ]

        for py_file in self.project_root.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Check for wildcard imports
                    if 'from ' in content and ' import *' in content:
                        import_issues['wildcard_imports'].append(str(py_file.relative_to(self.project_root)))

                    # Check for heavy module imports
                    for module in heavy_modules:
                        if f'import {module}' in content or f'from {module}' in content:
                            import_issues['heavy_imports'].append({
                                'file': str(py_file.relative_to(self.project_root)),
                                'module': module
                            })

            except Exception as e:
                logger.warning(f"Error analyzing {py_file}: {e}")

        return import_issues

    def run_full_audit(self) -> Dict[str, Any]:
        """Run comprehensive performance audit"""
        logger.info("Starting comprehensive performance audit...")

        # Get system info
        system_info = {
            'platform': sys.platform,
            'python_version': sys.version,
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': psutil.virtual_memory().total / 1024 / 1024 / 1024
        }

        # Find large files (V2 compliance violations)
        large_files = self.find_large_files()

        # Audit imports
        import_audit = self.audit_imports()

        # Profile key modules
        key_modules = [
            'src.core.unified_config',
            'src.core.unified_messaging',
            'src.core.core_unified_system',
            'src.services.messaging_core'
        ]

        module_profiles = {}
        for module in key_modules:
            try:
                logger.info(f"Profiling {module}...")
                module_profiles[module] = self.profile_module_import(module)
            except Exception as e:
                logger.error(f"Failed to profile {module}: {e}")
                module_profiles[module] = {'error': str(e)}

        # Current memory usage
        current_memory = self.get_memory_usage()

        audit_results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': system_info,
            'current_memory_usage': current_memory,
            'large_files_violations': large_files,
            'import_audit': import_audit,
            'module_profiles': module_profiles,
            'summary': {
                'total_large_files': len(large_files),
                'total_files_analyzed': len(list(self.project_root.rglob('*.py'))),
                'modules_profiled': len([m for m in module_profiles.values() if 'error' not in m]),
                'heavy_imports_found': len(import_audit['heavy_imports']),
                'wildcard_imports_found': len(import_audit['wildcard_imports'])
            }
        }

        self.results = audit_results
        return audit_results

    def generate_report(self) -> str:
        """Generate a comprehensive performance report"""
        if not self.results:
            return "No audit results available. Run run_full_audit() first."

        report = []
        report.append("=" * 80)
        report.append("PERFORMANCE AUDIT REPORT - AGENT-1 MISSION")
        report.append("=" * 80)
        report.append(f"Generated: {self.results['timestamp']}")
        report.append("")

        # System info
        report.append("SYSTEM INFORMATION:")
        report.append("-" * 30)
        for key, value in self.results['system_info'].items():
            report.append(f"{key}: {value}")
        report.append("")

        # Current memory usage
        report.append("CURRENT MEMORY USAGE:")
        report.append("-" * 30)
        mem = self.results['current_memory_usage']
        report.append(f"RSS Memory: {mem['rss']:.2f} MB")
        report.append(f"Virtual Memory: {mem['vms']:.2f} MB")
        report.append(f"Memory Percent: {mem['percent']:.2f}%")
        report.append(f"CPU Usage: {mem['cpu_percent']:.2f}%")
        report.append("")

        # V2 Compliance violations
        report.append("V2 COMPLIANCE VIOLATIONS (FILES > 400 LINES):")
        report.append("-" * 50)
        large_files = self.results['large_files_violations']
        if large_files:
            for file_info in large_files[:10]:  # Top 10
                report.append(f"{file_info['file']}: {file_info['lines']} lines ({file_info['size_kb']:.1f} KB)")
            if len(large_files) > 10:
                report.append(f"... and {len(large_files) - 10} more files")
        else:
            report.append("No violations found!")
        report.append("")

        # Import issues
        report.append("IMPORT OPTIMIZATION OPPORTUNITIES:")
        report.append("-" * 40)
        import_audit = self.results['import_audit']
        if import_audit['heavy_imports']:
            report.append("Heavy module imports detected:")
            for imp in import_audit['heavy_imports'][:5]:
                report.append(f"  {imp['file']}: imports {imp['module']}")
        if import_audit['wildcard_imports']:
            report.append(f"Wildcard imports: {len(import_audit['wildcard_imports'])} files")
        report.append("")

        # Module performance
        report.append("MODULE PERFORMANCE PROFILE:")
        report.append("-" * 35)
        for module, profile in self.results['module_profiles'].items():
            if 'error' in profile:
                report.append(f"{module}: ERROR - {profile['error']}")
            else:
                report.append(f"{module}:")
                report.append(f"  Import time: {profile['import_time_ms']:.2f} ms")
                report.append(f"  Memory delta: {profile['memory_delta_mb']:.2f} MB")
                report.append(f"  Peak memory: {profile['peak_memory_mb']:.2f} MB")
                report.append("")

        # Summary
        report.append("AUDIT SUMMARY:")
        report.append("-" * 15)
        summary = self.results['summary']
        report.append(f"Total Python files analyzed: {summary['total_files_analyzed']}")
        report.append(f"Files exceeding 400 lines: {summary['total_large_files']}")
        report.append(f"Modules successfully profiled: {summary['modules_profiled']}")
        report.append(f"Heavy imports found: {summary['heavy_imports_found']}")
        report.append(f"Wildcard imports found: {summary['wildcard_imports_found']}")
        report.append("")

        report.append("RECOMMENDATIONS:")
        report.append("-" * 15)
        if summary['total_large_files'] > 0:
            report.append("• Refactor large files (>400 lines) to comply with V2 standards")
        if summary['heavy_imports_found'] > 0:
            report.append("• Implement lazy loading for heavy module imports")
        if summary['wildcard_imports_found'] > 0:
            report.append("• Replace wildcard imports with explicit imports")
        report.append("• Add performance monitoring to critical paths")
        report.append("• Implement proper resource cleanup and garbage collection")

        return "\n".join(report)


def main():
    """Main entry point for performance audit"""
    auditor = PerformanceAuditor()

    print("🔍 Starting comprehensive performance audit...")
    print("This may take a few minutes...")

    try:
        results = auditor.run_full_audit()
        report = auditor.generate_report()

        # Save report to file
        report_file = f"performance_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ Performance audit completed!")
        print(f"📊 Report saved to: {report_file}")
        print("\n" + "="*80)
        print(report)

    except Exception as e:
        logger.error(f"Performance audit failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
