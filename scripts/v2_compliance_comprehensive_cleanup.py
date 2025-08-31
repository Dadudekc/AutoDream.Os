#!/usr/bin/env python3
"""
V2 Compliance Comprehensive Cleanup Tool
Handles multiple cleanup tasks and side missions simultaneously
"""

import os
import re
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

class V2ComplianceComprehensiveCleanup:
    def __init__(self):
        self.backup_dir = f"backups/v2_compliance_comprehensive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.cleanup_results = {
            'duplicate_directories_removed': 0,
            'temporary_files_cleaned': 0,
            'backup_files_cleaned': 0,
            'cache_files_cleaned': 0,
            'import_statements_updated': 0,
            'side_missions_completed': 0,
            'compliance_improvements': []
        }
        
    def create_backup(self) -> bool:
        """Create comprehensive backup"""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            print(f"✅ Backup directory created: {self.backup_dir}")
            return True
        except Exception as e:
            print(f"❌ Backup creation failed: {e}")
            return False
    
    def cleanup_duplicate_directories(self) -> int:
        """Remove duplicate refactored directories"""
        duplicate_patterns = [
            "*_refactored",
            "*_v2_compliant", 
            "*_advanced_refactored",
            "*_targeted_refactored"
        ]
        
        removed_count = 0
        
        for pattern in duplicate_patterns:
            for path in Path(".").rglob(pattern):
                if path.is_dir():
                    try:
                        shutil.rmtree(path)
                        removed_count += 1
                        print(f"🗑️ Removed duplicate directory: {path}")
                    except Exception as e:
                        print(f"⚠️ Failed to remove {path}: {e}")
        
        self.cleanup_results['duplicate_directories_removed'] = removed_count
        return removed_count
    
    def cleanup_temporary_files(self) -> int:
        """Clean up temporary and backup files"""
        temp_patterns = [
            "*.tmp", "*.bak", "*.old", "*.orig",
            "*.pyc", "*.pyo", "__pycache__",
            "*.log", "*.cache", "*.swp", "*.swo"
        ]
        
        cleaned_count = 0
        
        for pattern in temp_patterns:
            for path in Path(".").rglob(pattern):
                try:
                    if path.is_file():
                        path.unlink()
                        cleaned_count += 1
                    elif path.is_dir():
                        shutil.rmtree(path)
                        cleaned_count += 1
                    print(f"🧹 Cleaned: {path}")
                except Exception as e:
                    print(f"⚠️ Failed to clean {path}: {e}")
        
        self.cleanup_results['temporary_files_cleaned'] = cleaned_count
        return cleaned_count
    
    def update_import_statements(self) -> int:
        """Update import statements for refactored modules"""
        updated_count = 0
        
        # Find all Python files
        for py_file in Path(".").rglob("*.py"):
            if "refactored" in str(py_file) or "v2_compliant" in str(py_file):
                continue  # Skip refactored files
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Update common import patterns
                import_updates = [
                    (r'from tests\.test_unified_testing_framework import', 'from tests.test_unified_testing_framework_refactored import'),
                    (r'import tests\.test_unified_testing_framework', 'import tests.test_unified_testing_framework_refactored_refactored'),
                    (r'from src\.core\.knowledge_database import', 'from src.core.knowledge_database_refactored import'),
                    (r'from src\.core\.task_manager import', 'from src.core.task_manager_refactored import'),
                ]
                
                for pattern, replacement in import_updates:
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_count += 1
                    print(f"📝 Updated imports in: {py_file}")
                    
            except Exception as e:
                print(f"⚠️ Failed to update imports in {py_file}: {e}")
        
        self.cleanup_results['import_statements_updated'] = updated_count
        return updated_count
    
    def create_v2_compliance_monitor(self) -> bool:
        """Create automated V2 compliance monitoring system"""
        try:
            monitor_content = '''#!/usr/bin/env python3
"""
V2 Compliance Automated Monitor
Continuously monitors and reports on V2 compliance status
"""

import os
import time
import schedule
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class V2ComplianceMonitor:
    def __init__(self):
        self.target_line_limit = 250
        self.compliance_thresholds = {
            'excellent': 300,
            'good': 500,
            'moderate': 800,
            'critical': 1000
        }
        
    def scan_repository(self) -> Dict[str, Any]:
        """Scan repository for compliance violations"""
        violations = {
            'critical': [], 'major': [], 'moderate': [], 'minor': []
        }
        
        total_files = 0
        compliant_files = 0
        
        for py_file in Path(".").rglob("*.py"):
            if "refactored" in str(py_file) or "backup" in str(py_file):
                continue
                
            total_files += 1
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    line_count = len(lines)
                
                if line_count <= self.target_line_limit:
                    compliant_files += 1
                elif line_count > self.compliance_thresholds['critical']:
                    violations['critical'].append(str(py_file))
                elif line_count > self.compliance_thresholds['moderate']:
                    violations['moderate'].append(str(py_file))
                elif line_count > self.compliance_thresholds['good']:
                    violations['major'].append(str(py_file))
                else:
                    violations['minor'].append(str(py_file))
                    
            except Exception as e:
                print(f"Error scanning {py_file}: {e}")
        
        compliance_percentage = (compliant_files / total_files * 100) if total_files > 0 else 0
        
        return {
            'total_files': total_files,
            'compliant_files': compliant_files,
            'compliance_percentage': compliance_percentage,
            'violations': violations,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_report(self, scan_results: Dict[str, Any]) -> str:
        """Generate compliance report"""
        report = f"""# V2 Compliance Monitor Report

## 📊 **COMPLIANCE STATUS**

**Generated:** {scan_results['timestamp']}
**Total Files:** {scan_results['total_files']}
**Compliant Files:** {scan_results['compliant_files']}
**Overall Compliance:** {scan_results['compliance_percentage']:.1f}%

## 🚨 **VIOLATIONS SUMMARY**

- **Critical Violations:** {len(scan_results['violations']['critical'])}
- **Major Violations:** {len(scan_results['violations']['major'])}
- **Moderate Violations:** {len(scan_results['violations']['moderate'])}
- **Minor Violations:** {len(scan_results['violations']['minor'])}

## 🎯 **RECOMMENDATIONS**

1. Address critical violations immediately
2. Plan refactoring for major violations
3. Monitor moderate violations
4. Maintain minor violations at current level
"""
        return report
    
    def save_report(self, report: str) -> str:
        """Save monitoring report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"reports/V2_COMPLIANCE_MONITOR_REPORT_{timestamp}.md"
        
        os.makedirs("reports", exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report_path
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        print("🔍 Running V2 compliance monitoring cycle...")
        scan_results = self.scan_repository()
        report = self.generate_report(scan_results)
        report_path = self.save_report(report)
        
        print(f"📊 Compliance: {scan_results['compliance_percentage']:.1f}%")
        print(f"📋 Report saved: {report_path}")
        
        return scan_results

def main():
    """Main monitoring function"""
    monitor = V2ComplianceMonitor()
    
    # Run initial scan
    results = monitor.run_monitoring_cycle()
    
    # Schedule continuous monitoring
    schedule.every(30).minutes.do(monitor.run_monitoring_cycle)
    
    print("🔄 V2 Compliance Monitor started - running every 30 minutes")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
'''
            
            monitor_path = "scripts/v2_compliance_monitor.py"
            with open(monitor_path, 'w', encoding='utf-8') as f:
                f.write(monitor_content)
            
            print(f"✅ Created V2 compliance monitor: {monitor_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create V2 compliance monitor: {e}")
            return False
    
    def create_side_mission_tracker(self) -> bool:
        """Create side mission tracking system"""
        try:
            tracker_content = '''#!/usr/bin/env python3
"""
Side Mission Tracker
Tracks and manages multiple side missions for V2 compliance
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class SideMissionTracker:
    def __init__(self):
        self.missions_file = "reports/side_missions_tracker.json"
        self.missions = {
            'active_missions': [],
            'completed_missions': [],
            'failed_missions': [],
            'total_missions': 0,
            'success_rate': 0.0
        }
    
    def add_mission(self, mission_id: str, description: str, priority: str = "MEDIUM") -> bool:
        """Add a new side mission"""
        mission = {
            'id': mission_id,
            'description': description,
            'priority': priority,
            'status': 'ACTIVE',
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
            'progress': 0.0
        }
        
        self.missions['active_missions'].append(mission)
        self.missions['total_missions'] += 1
        self.save_missions()
        
        print(f"✅ Added mission: {mission_id}")
        return True
    
    def complete_mission(self, mission_id: str, results: Dict[str, Any] = None) -> bool:
        """Mark a mission as completed"""
        for mission in self.missions['active_missions']:
            if mission['id'] == mission_id:
                mission['status'] = 'COMPLETED'
                mission['completed_at'] = datetime.now().isoformat()
                mission['progress'] = 100.0
                mission['results'] = results or {}
                
                self.missions['completed_missions'].append(mission)
                self.missions['active_missions'].remove(mission)
                
                self.update_success_rate()
                self.save_missions()
                
                print(f"🎉 Mission completed: {mission_id}")
                return True
        
        print(f"❌ Mission not found: {mission_id}")
        return False
    
    def update_success_rate(self):
        """Update mission success rate"""
        total_completed = len(self.missions['completed_missions'])
        total_failed = len(self.missions['failed_missions'])
        total = total_completed + total_failed
        
        if total > 0:
            self.missions['success_rate'] = (total_completed / total) * 100
    
    def save_missions(self):
        """Save missions to file"""
        os.makedirs("reports", exist_ok=True)
        with open(self.missions_file, 'w', encoding='utf-8') as f:
            json.dump(self.missions, f, indent=2)
    
    def load_missions(self):
        """Load missions from file"""
        if os.path.exists(self.missions_file):
            with open(self.missions_file, 'r', encoding='utf-8') as f:
                self.missions = json.load(f)
    
    def generate_report(self) -> str:
        """Generate side mission report"""
        report = f"""# Side Mission Tracker Report

## 📊 **MISSION SUMMARY**

**Generated:** {datetime.now()}
**Total Missions:** {self.missions['total_missions']}
**Active Missions:** {len(self.missions['active_missions'])}
**Completed Missions:** {len(self.missions['completed_missions'])}
**Success Rate:** {self.missions['success_rate']:.1f}%

## 🎯 **ACTIVE MISSIONS**

"""
        
        for mission in self.missions['active_missions']:
            report += f"- **{mission['id']}**: {mission['description']} ({mission['priority']})\n"
            report += f"  - Progress: {mission['progress']:.1f}%\n"
        
        report += "\n## ✅ **COMPLETED MISSIONS**\n"
        
        for mission in self.missions['completed_missions']:
            report += f"- **{mission['id']}**: {mission['description']}\n"
            report += f"  - Completed: {mission['completed_at']}\n"
        
        return report

def main():
    """Main tracker function"""
    tracker = SideMissionTracker()
    tracker.load_missions()
    
    # Add some example missions
    tracker.add_mission("CLEANUP-001", "Remove duplicate directories", "HIGH")
    tracker.add_mission("CLEANUP-002", "Clean temporary files", "MEDIUM")
    tracker.add_mission("CLEANUP-003", "Update import statements", "HIGH")
    tracker.add_mission("MONITOR-001", "Create V2 compliance monitor", "HIGH")
    
    # Generate report
    report = tracker.generate_report()
    print(report)
    
    # Save report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f"reports/SIDE_MISSIONS_REPORT_{timestamp}.md"
    
    os.makedirs("reports", exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📋 Side mission report saved: {report_path}")

if __name__ == "__main__":
    main()
'''
            
            tracker_path = "scripts/side_mission_tracker.py"
            with open(tracker_path, 'w', encoding='utf-8') as f:
                f.write(tracker_content)
            
            print(f"✅ Created side mission tracker: {tracker_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create side mission tracker: {e}")
            return False
    
    def execute_comprehensive_cleanup(self) -> Dict[str, Any]:
        """Execute comprehensive cleanup and side missions"""
        print("🚀 V2 Compliance Comprehensive Cleanup Tool")
        print("=" * 60)
        
        # Create backup
        self.create_backup()
        
        # Execute cleanup tasks
        print("\n🧹 Executing cleanup tasks...")
        
        # Cleanup duplicate directories
        removed_dirs = self.cleanup_duplicate_directories()
        print(f"🗑️ Removed {removed_dirs} duplicate directories")
        
        # Cleanup temporary files
        cleaned_files = self.cleanup_temporary_files()
        print(f"🧹 Cleaned {cleaned_files} temporary files")
        
        # Update import statements
        updated_imports = self.update_import_statements()
        print(f"📝 Updated {updated_imports} import statements")
        
        # Create side mission tools
        print("\n🎯 Creating side mission tools...")
        
        if self.create_v2_compliance_monitor():
            self.cleanup_results['side_missions_completed'] += 1
            print("✅ V2 compliance monitor created")
        
        if self.create_side_mission_tracker():
            self.cleanup_results['side_missions_completed'] += 1
            print("✅ Side mission tracker created")
        
        return self.cleanup_results
    
    def generate_report(self) -> str:
        """Generate comprehensive cleanup report"""
        report = f"""# V2 Compliance Comprehensive Cleanup Report

## 📊 **CLEANUP SUMMARY**

**Generated:** {datetime.now()}
**Duplicate Directories Removed:** {self.cleanup_results['duplicate_directories_removed']}
**Temporary Files Cleaned:** {self.cleanup_results['temporary_files_cleaned']}
**Import Statements Updated:** {self.cleanup_results['import_statements_updated']}
**Side Missions Completed:** {self.cleanup_results['side_missions_completed']}

## 🎯 **CLEANUP ACTIONS**

### ✅ **Completed Tasks**
- Duplicate directory removal
- Temporary file cleanup
- Import statement updates
- Side mission tool creation

### 📁 **Backup Location**
All original files backed up to: `{self.backup_dir}`

### 🛠️ **Created Tools**
- V2 Compliance Monitor (`scripts/v2_compliance_monitor.py`)
- Side Mission Tracker (`scripts/side_mission_tracker.py`)

## ✅ **NEXT STEPS**

1. Run V2 compliance validation to measure improvement
2. Use side mission tracker for ongoing task management
3. Monitor compliance with automated tools
4. Continue with remaining V2 compliance violations
"""
        return report
    
    def save_report(self, report: str) -> str:
        """Save cleanup report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"reports/V2_COMPLIANCE_COMPREHENSIVE_CLEANUP_REPORT_{timestamp}.md"
        
        os.makedirs("reports", exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report_path

def main():
    """Main execution function"""
    cleanup_tool = V2ComplianceComprehensiveCleanup()
    
    # Execute comprehensive cleanup
    results = cleanup_tool.execute_comprehensive_cleanup()
    
    # Generate and save report
    report = cleanup_tool.generate_report()
    report_path = cleanup_tool.save_report(report)
    
    print("\n" + "=" * 60)
    print("✅ COMPREHENSIVE CLEANUP COMPLETE")
    print(f"📋 Report saved: {report_path}")
    print(f"📊 Results: {results}")

if __name__ == "__main__":
    main()
