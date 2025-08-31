#!/usr/bin/env python3
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
