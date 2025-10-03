#!/usr/bin/env python3
"""
Memory Optimization Tool
========================

Automated memory optimization tool that fixes common memory leaks and sinks.
Focuses on HIGH severity issues first, then MEDIUM severity issues.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, focused optimization, automated fixes
"""

import ast
import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


@dataclass
class MemoryFix:
    """Represents a memory optimization fix."""
    file_path: str
    line_number: int
    fix_type: str
    original_code: str
    fixed_code: str
    description: str


class MemoryOptimizer:
    """Automatically fixes memory leaks and optimization issues."""

    def __init__(self, project_root: Path):
        """Initialize the memory optimizer."""
        self.project_root = project_root
        self.fixes: List[MemoryFix] = []
        
        # High-priority fixes
        self.critical_fixes = {
            "sqlite_context_manager": {
                "pattern": r"(\w+)\s*=\s*sqlite3\.connect\(([^)]+)\)",
                "replacement": r"with sqlite3.connect(\2) as \1:",
                "description": "Convert SQLite connections to context managers"
            },
            "file_context_manager": {
                "pattern": r"(\w+)\s*=\s*open\(([^)]+)\)",
                "replacement": r"with open(\2) as \1:",
                "description": "Convert file operations to context managers"
            },
            "thread_daemon": {
                "pattern": r"threading\.Thread\(([^)]+)\)",
                "replacement": r"threading.Thread(\1, daemon=True, daemon=True)",
                "description": "Add daemon=True to threads for automatic cleanup"
            },
            "queue_with_limit": {
                "pattern": r"queue\.Queue\(\)",
                "replacement": r"queue.Queue(maxsize=1000)",
                "description": "Add size limit to queues"
            },
            "deque_with_limit": {
                "pattern": r"collections\.deque\(\)",
                "replacement": r"collections.deque(maxlen=1000)",
                "description": "Add size limit to deques"
            }
        }

    def fix_file(self, file_path: Path) -> List[MemoryFix]:
        """Fix memory issues in a single file."""
        fixes = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                original_content = content
                
            # Apply critical fixes
            for fix_type, fix_info in self.critical_fixes.items():
                pattern = fix_info["pattern"]
                replacement = fix_info["replacement"]
                
                # Find all matches
                matches = list(re.finditer(pattern, content))
                
                for match in reversed(matches):  # Process in reverse to maintain line numbers
                    line_number = content[:match.start()].count('\n') + 1
                    original_code = match.group(0)
                    
                    # Apply the fix
                    fixed_code = re.sub(pattern, replacement, original_code)
                    
                    if fixed_code != original_code:
                        fix = MemoryFix(
                            file_path=str(file_path),
                            line_number=line_number,
                            fix_type=fix_type,
                            original_code=original_code,
                            fixed_code=fixed_code,
                            description=fix_info["description"]
                        )
                        fixes.append(fix)
                        
                        # Update content
                        content = content[:match.start()] + fixed_code + content[match.end():]
            
            # Write fixed content if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Applied {len(fixes)} fixes to {file_path}")
            
        except Exception as e:
            logger.error(f"Error fixing {file_path}: {e}")
            
        return fixes

    def fix_high_priority_files(self) -> Dict[str, Any]:
        """Fix high-priority files with most memory issues."""
        logger.info("Starting high-priority memory optimization...")
        
        # Load the memory leak report to identify high-priority files
        report_file = self.project_root / "memory_leak_report.json"
        if not report_file.exists():
            logger.error("Memory leak report not found. Run memory_leak_detector.py first.")
            return {"error": "Memory leak report not found"}
        
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        # Get top files with issues
        top_files = report["summary"]["top_files_with_issues"][:10]
        
        total_fixes = 0
        files_fixed = 0
        
        for file_info in top_files:
            file_path = Path(file_info["file"])
            if file_path.exists():
                fixes = self.fix_file(file_path)
                if fixes:
                    files_fixed += 1
                    total_fixes += len(fixes)
                    self.fixes.extend(fixes)
        
        # Fix files with HIGH severity issues
        high_severity_files = set()
        for issue in report["detailed_issues"]:
            if issue["severity"] == "HIGH":
                high_severity_files.add(issue["file"])
        
        for file_path_str in high_severity_files:
            file_path = Path(file_path_str)
            if file_path.exists():
                fixes = self.fix_file(file_path)
                if fixes:
                    files_fixed += 1
                    total_fixes += len(fixes)
                    self.fixes.extend(fixes)
        
        summary = {
            "files_processed": len(top_files) + len(high_severity_files),
            "files_fixed": files_fixed,
            "total_fixes": total_fixes,
            "fixes_by_type": self._count_fixes_by_type()
        }
        
        logger.info(f"High-priority optimization complete: {total_fixes} fixes applied to {files_fixed} files")
        return summary

    def _count_fixes_by_type(self) -> Dict[str, int]:
        """Count fixes by type."""
        counts = {}
        for fix in self.fixes:
            counts[fix.fix_type] = counts.get(fix.fix_type, 0) + 1
        return counts

    def create_memory_monitoring_tool(self) -> str:
        """Create a memory monitoring tool for ongoing leak detection."""
        monitoring_tool = '''#!/usr/bin/env python3
"""
Memory Monitor - Real-time Memory Leak Detection
===============================================

Real-time memory monitoring and leak detection tool.
Monitors memory usage and alerts on potential leaks.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import gc
import logging
import psutil
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


@dataclass
class MemorySnapshot:
    """Memory usage snapshot."""
    timestamp: float
    memory_mb: float
    cpu_percent: float
    objects_count: int
    garbage_count: int


class MemoryMonitor:
    """Real-time memory monitoring system."""
    
    def __init__(self, alert_threshold_mb: float = 1000.0):
        """Initialize memory monitor."""
        self.alert_threshold = alert_threshold_mb
        self.snapshots: List[MemorySnapshot] = []
        self.is_monitoring = False
        
    def take_snapshot(self) -> MemorySnapshot:
        """Take a memory snapshot."""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        snapshot = MemorySnapshot(
            timestamp=time.time(),
            memory_mb=memory_info.rss / 1024 / 1024,
            cpu_percent=process.cpu_percent(),
            objects_count=len(gc.get_objects()),
            garbage_count=len(gc.garbage)
        )
        
        self.snapshots.append(snapshot)
        
        # Keep only last 100 snapshots
        if len(self.snapshots) > 100:
            self.snapshots = self.snapshots[-100:]
            
        return snapshot
    
    def check_for_leaks(self) -> List[str]:
        """Check for potential memory leaks."""
        alerts = []
        
        if len(self.snapshots) < 10:
            return alerts
            
        # Check for increasing memory trend
        recent_snapshots = self.snapshots[-10:]
        memory_trend = [s.memory_mb for s in recent_snapshots]
        
        if all(memory_trend[i] < memory_trend[i+1] for i in range(len(memory_trend)-1)):
            alerts.append(f"🚨 Memory leak detected: {memory_trend[-1]:.1f}MB")
            
        # Check for high memory usage
        current_memory = recent_snapshots[-1].memory_mb
        if current_memory > self.alert_threshold:
            alerts.append(f"⚠️ High memory usage: {current_memory:.1f}MB")
            
        # Check for garbage collection issues
        if recent_snapshots[-1].garbage_count > 100:
            alerts.append(f"🗑️ High garbage count: {recent_snapshots[-1].garbage_count}")
            
        return alerts
    
    def force_cleanup(self):
        """Force garbage collection and cleanup."""
        collected = gc.collect()
        logger.info(f"Garbage collection freed {collected} objects")
        return collected
    
    def start_monitoring(self, interval: float = 30.0):
        """Start continuous monitoring."""
        self.is_monitoring = True
        logger.info(f"Memory monitoring started (interval: {interval}s)")
        
        while self.is_monitoring:
            snapshot = self.take_snapshot()
            alerts = self.check_for_leaks()
            
            if alerts:
                for alert in alerts:
                    logger.warning(alert)
                    
            time.sleep(interval)
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.is_monitoring = False
        logger.info("Memory monitoring stopped")


def main():
    """Main function for memory monitoring."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Monitor")
    parser.add_argument("--interval", type=float, default=30.0, help="Monitoring interval in seconds")
    parser.add_argument("--threshold", type=float, default=1000.0, help="Memory alert threshold in MB")
    parser.add_argument("--cleanup", action="store_true", help="Force cleanup before monitoring")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    monitor = MemoryMonitor(args.threshold)
    
    if args.cleanup:
        monitor.force_cleanup()
    
    try:
        monitor.start_monitoring(args.interval)
    except KeyboardInterrupt:
        monitor.stop_monitoring()


if __name__ == "__main__":
    main()
'''
        
        monitoring_file = self.project_root / "tools" / "memory_monitor.py"
        with open(monitoring_file, 'w', encoding='utf-8') as f:
            f.write(monitoring_tool)
        
        logger.info(f"Memory monitoring tool created: {monitoring_file}")
        return str(monitoring_file)

    def generate_optimization_report(self) -> str:
        """Generate optimization report."""
        report = {
            "timestamp": str(datetime.now()),
            "project_root": str(self.project_root),
            "total_fixes": len(self.fixes),
            "fixes_by_type": self._count_fixes_by_type(),
            "detailed_fixes": [
                {
                    "file": fix.file_path,
                    "line": fix.line_number,
                    "type": fix.fix_type,
                    "description": fix.description,
                    "original": fix.original_code,
                    "fixed": fix.fixed_code
                }
                for fix in self.fixes
            ]
        }
        
        report_file = self.project_root / "memory_optimization_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Optimization report saved to: {report_file}")
        return str(report_file)


def main():
    """Main function for memory optimization."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Optimizer")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    project_root = Path(args.project_root)
    optimizer = MemoryOptimizer(project_root)
    
    # Fix high-priority issues
    summary = optimizer.fix_high_priority_files()
    
    if "error" in summary:
        print(f"❌ Error: {summary['error']}")
        return
    
    # Create monitoring tool
    monitoring_tool = optimizer.create_memory_monitoring_tool()
    
    # Generate report
    report_file = optimizer.generate_optimization_report()
    
    # Print summary
    print(f"\n🔧 Memory Optimization Summary:")
    print(f"📊 Files processed: {summary['files_processed']}")
    print(f"✅ Files fixed: {summary['files_fixed']}")
    print(f"🔧 Total fixes: {summary['total_fixes']}")
    print(f"📈 Fixes by type: {summary['fixes_by_type']}")
    
    print(f"\n📄 Optimization report: {report_file}")
    print(f"📊 Memory monitor tool: {monitoring_tool}")


if __name__ == "__main__":
    main()
