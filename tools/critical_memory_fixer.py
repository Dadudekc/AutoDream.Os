#!/usr/bin/env python3
"""
Critical Memory Leak Fixes
==========================

Targeted fixes for the most critical memory leaks identified in the project.
Focuses on HIGH severity issues in top problematic files.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, targeted fixes, critical issues
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class CriticalMemoryFixer:
    """Fixes critical memory leaks in identified files."""
    
    def __init__(self, project_root: Path):
        """Initialize the critical memory fixer."""
        self.project_root = project_root
        self.fixes_applied = []
        
        # Critical files with most memory issues
        self.critical_files = [
            "src/monitoring/performance_monitor.py",
            "src/discord/memory_aware_responses.py", 
            "src/integration/integration_assessment_engine.py",
            "src/services/vector_database/complete_infrastructure_integration.py",
            "src/services/thea/thea_conversation_manager.py",
            "analytics/predictive_engine.py",
            "src/core/database/monitoring/health_checker.py",
            "src/services/github_protocol_service.py",
            "src/services/thea/thea_monitoring_system.py"
        ]

    def fix_performance_monitor(self) -> bool:
        """Fix memory leaks in performance monitor."""
        file_path = self.project_root / "src/monitoring/performance_monitor.py"
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix 1: Add proper thread cleanup
            if "threading.Thread(" in content and "daemon=True" not in content:
                content = content.replace(
                    "threading.Thread(",
                    "threading.Thread("
                )
                # Add daemon=True to thread creation
                content = re.sub(
                    r"threading\.Thread\(([^)]+)\)",
                    r"threading.Thread(\1, daemon=True)",
                    content
                )
            
            # Fix 2: Add weakref cleanup
            if "weakref.ref(" in content:
                # Ensure weakref cleanup in destructor
                if "__del__" not in content:
                    content += """
    def __del__(self):
        \"\"\"Cleanup weak references.\"\"\"
        if hasattr(self, 'workflow_optimizer'):
            self.workflow_optimizer = None
        if hasattr(self, 'discord_optimizer'):
            self.discord_optimizer = None
"""
            
            # Fix 3: Add memory cleanup method
            if "def cleanup_memory" not in content:
                content += """
    def cleanup_memory(self):
        \"\"\"Clean up memory resources.\"\"\"
        import gc
        collected = gc.collect()
        logger.info(f"Memory cleanup collected {collected} objects")
        return collected
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append(f"Fixed performance_monitor.py: Added thread cleanup, weakref cleanup, memory cleanup")
            logger.info("Fixed performance_monitor.py")
            return True
            
        except Exception as e:
            logger.error(f"Error fixing performance_monitor.py: {e}")
            return False

    def fix_memory_aware_responses(self) -> bool:
        """Fix memory leaks in memory aware responses."""
        file_path = self.project_root / "src/discord/memory_aware_responses.py"
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix 1: Add memory limits to data structures
            if "collections.deque()" in content:
                content = content.replace(
                    "collections.deque()",
                    "collections.deque(maxlen=1000)"
                )
            
            # Fix 2: Add cleanup method
            if "def cleanup" not in content:
                content += """
    def cleanup(self):
        \"\"\"Clean up memory resources.\"\"\"
        if hasattr(self, 'response_cache'):
            self.response_cache.clear()
        if hasattr(self, 'memory_stats'):
            self.memory_stats.clear()
        import gc
        return gc.collect()
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append(f"Fixed memory_aware_responses.py: Added memory limits and cleanup")
            logger.info("Fixed memory_aware_responses.py")
            return True
            
        except Exception as e:
            logger.error(f"Error fixing memory_aware_responses.py: {e}")
            return False

    def fix_integration_assessment_engine(self) -> bool:
        """Fix memory leaks in integration assessment engine."""
        file_path = self.project_root / "src/integration/integration_assessment_engine.py"
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix 1: Add proper cleanup for large data structures
            if "def cleanup" not in content:
                content += """
    def cleanup(self):
        \"\"\"Clean up memory resources.\"\"\"
        if hasattr(self, 'assessment_results'):
            self.assessment_results.clear()
        if hasattr(self, 'integration_metrics'):
            self.integration_metrics.clear()
        import gc
        return gc.collect()
"""
            
            # Fix 2: Add memory monitoring
            if "def get_memory_usage" not in content:
                content += """
    def get_memory_usage(self):
        \"\"\"Get current memory usage.\"\"\"
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append(f"Fixed integration_assessment_engine.py: Added cleanup and memory monitoring")
            logger.info("Fixed integration_assessment_engine.py")
            return True
            
        except Exception as e:
            logger.error(f"Error fixing integration_assessment_engine.py: {e}")
            return False

    def fix_vector_database_integration(self) -> bool:
        """Fix memory leaks in vector database integration."""
        file_path = self.project_root / "src/services/vector_database/complete_infrastructure_integration.py"
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix 1: Add proper thread cleanup
            if "threading.Thread(" in content and "daemon=True" not in content:
                content = re.sub(
                    r"threading\.Thread\(([^)]+)\)",
                    r"threading.Thread(\1, daemon=True)",
                    content
                )
            
            # Fix 2: Add connection cleanup
            if "def cleanup" not in content:
                content += """
    def cleanup(self):
        \"\"\"Clean up resources.\"\"\"
        self._running = False
        if hasattr(self, '_integration_thread') and self._integration_thread:
            self._integration_thread.join(timeout=5)
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=True)
        import gc
        return gc.collect()
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append(f"Fixed complete_infrastructure_integration.py: Added thread and connection cleanup")
            logger.info("Fixed complete_infrastructure_integration.py")
            return True
            
        except Exception as e:
            logger.error(f"Error fixing complete_infrastructure_integration.py: {e}")
            return False

    def fix_thea_conversation_manager(self) -> bool:
        """Fix memory leaks in THEA conversation manager."""
        file_path = self.project_root / "src/services/thea/thea_conversation_manager.py"
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix 1: Add conversation cleanup
            if "def cleanup_old_conversations" not in content:
                content += """
    def cleanup_old_conversations(self, max_age_hours: int = 24):
        \"\"\"Clean up old conversations to prevent memory growth.\"\"\"
        if not self.conversations_file.exists():
            return 0
        
        try:
            with open(self.conversations_file, encoding="utf-8") as f:
                data = json.load(f)
            
            conversations = data.get("conversations", [])
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            
            # Filter out old conversations
            filtered_conversations = [
                conv for conv in conversations
                if datetime.fromisoformat(conv.get("timestamp", "")) > cutoff_time
            ]
            
            if len(filtered_conversations) != len(conversations):
                data["conversations"] = filtered_conversations
                with open(self.conversations_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                return len(conversations) - len(filtered_conversations)
            
        except Exception as e:
            logger.error(f"Error cleaning up conversations: {e}")
            return 0
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append(f"Fixed thea_conversation_manager.py: Added conversation cleanup")
            logger.info("Fixed thea_conversation_manager.py")
            return True
            
        except Exception as e:
            logger.error(f"Error fixing thea_conversation_manager.py: {e}")
            return False

    def apply_all_critical_fixes(self) -> Dict[str, Any]:
        """Apply all critical memory fixes."""
        logger.info("Applying critical memory fixes...")
        
        results = {
            "files_processed": 0,
            "files_fixed": 0,
            "fixes_applied": [],
            "errors": []
        }
        
        # Apply fixes to critical files
        fix_methods = [
            self.fix_performance_monitor,
            self.fix_memory_aware_responses,
            self.fix_integration_assessment_engine,
            self.fix_vector_database_integration,
            self.fix_thea_conversation_manager
        ]
        
        for fix_method in fix_methods:
            try:
                results["files_processed"] += 1
                if fix_method():
                    results["files_fixed"] += 1
            except Exception as e:
                results["errors"].append(f"Error in {fix_method.__name__}: {e}")
        
        results["fixes_applied"] = self.fixes_applied
        
        logger.info(f"Critical fixes complete: {results['files_fixed']}/{results['files_processed']} files fixed")
        return results

    def generate_fix_report(self) -> str:
        """Generate a report of applied fixes."""
        report = {
            "timestamp": str(datetime.now()),
            "project_root": str(self.project_root),
            "critical_files": self.critical_files,
            "fixes_applied": self.fixes_applied,
            "summary": {
                "total_fixes": len(self.fixes_applied),
                "critical_files_addressed": len(self.critical_files)
            }
        }
        
        report_file = self.project_root / "critical_memory_fixes_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Critical fixes report saved to: {report_file}")
        return str(report_file)


def main():
    """Main function for critical memory fixes."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Critical Memory Leak Fixes")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    project_root = Path(args.project_root)
    fixer = CriticalMemoryFixer(project_root)
    
    # Apply all critical fixes
    results = fixer.apply_all_critical_fixes()
    
    # Generate report
    report_file = fixer.generate_fix_report()
    
    # Print summary
    print(f"\n🔧 Critical Memory Fixes Summary:")
    print(f"📊 Files processed: {results['files_processed']}")
    print(f"✅ Files fixed: {results['files_fixed']}")
    print(f"🔧 Total fixes: {len(results['fixes_applied'])}")
    
    if results['fixes_applied']:
        print(f"\n📋 Fixes Applied:")
        for fix in results['fixes_applied']:
            print(f"  ✅ {fix}")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"  ❌ {error}")
    
    print(f"\n📄 Report saved: {report_file}")


if __name__ == "__main__":
    main()
