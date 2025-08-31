#!/usr/bin/env python3
"""
V2 Compliance Validator - Agent-2
Identifies and reports V2 compliance violations across the repository
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class V2ComplianceValidator:
    """Validates V2 compliance standards across the repository."""
    
    def __init__(self):
        """Initialize V2 compliance validator."""
        self.compliance_thresholds = {
            'excellent': 300,      # ≤300 lines - V2 compliant
            'good': 500,           # ≤500 lines - acceptable
            'moderate': 800,       # ≤800 lines - needs attention
            'critical': 1000       # >1000 lines - critical violation
        }
        self.violations = {
            'critical': [],
            'major': [],
            'moderate': [],
            'minor': []
        }
        self.compliance_stats = {
            'total_files': 0,
            'compliant_files': 0,
            'violation_files': 0,
            'overall_compliance': 0.0
        }
    
    def scan_repository(self, root_path: str = ".") -> Dict[str, Any]:
        """Scan repository for Python files and analyze compliance."""
        print("🔍 Scanning repository for V2 compliance violations...")
        
        python_files = []
        for root, dirs, files in os.walk(root_path):
            # Skip common directories that shouldn't be analyzed
            dirs[:] = [d for d in dirs if d not in [
                '__pycache__', '.git', '.venv', 'venv', 'node_modules',
                'build', 'dist', '.pytest_cache', 'backups'
            ]]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)
        
        print(f"📁 Found {len(python_files)} Python files")
        return {'python_files': python_files}
    
    def analyze_file_compliance(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file for V2 compliance."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            line_count = len(lines)
            relative_path = os.path.relpath(file_path)
            
            # Determine compliance level
            if line_count <= self.compliance_thresholds['excellent']:
                compliance_level = 'excellent'
                status = '✅ COMPLIANT'
            elif line_count <= self.compliance_thresholds['good']:
                compliance_level = 'good'
                status = '🟡 ACCEPTABLE'
            elif line_count <= self.compliance_thresholds['moderate']:
                compliance_level = 'moderate'
                status = '🟠 NEEDS ATTENTION'
            elif line_count <= self.compliance_thresholds['critical']:
                compliance_level = 'major'
                status = '🔴 MAJOR VIOLATION'
            else:
                compliance_level = 'critical'
                status = '🚨 CRITICAL VIOLATION'
            
            return {
                'file_path': relative_path,
                'absolute_path': file_path,
                'line_count': line_count,
                'compliance_level': compliance_level,
                'status': status,
                'threshold': self.compliance_thresholds[compliance_level]
            }
            
        except Exception as e:
            return {
                'file_path': os.path.relpath(file_path),
                'absolute_path': file_path,
                'line_count': 0,
                'compliance_level': 'error',
                'status': f'❌ ERROR: {str(e)}',
                'threshold': 0
            }
    
    def categorize_violations(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Categorize files by compliance level."""
        print("📊 Categorizing compliance violations...")
        
        for result in analysis_results:
            if result['compliance_level'] == 'excellent':
                self.compliance_stats['compliant_files'] += 1
            else:
                self.compliance_stats['violation_files'] += 1
                level = result['compliance_level']
                if level in self.violations:
                    self.violations[level].append(result)
        
        self.compliance_stats['total_files'] = len(analysis_results)
        if self.compliance_stats['total_files'] > 0:
            self.compliance_stats['overall_compliance'] = (
                self.compliance_stats['compliant_files'] / 
                self.compliance_stats['total_files']
            ) * 100
        
        return self.violations
    
    def generate_compliance_report(self) -> str:
        """Generate comprehensive V2 compliance report."""
        print("📋 Generating V2 compliance report...")
        
        report = f"""# 🚨 V2 COMPLIANCE VALIDATION REPORT - AGENT-2

## 📊 **COMPLIANCE OVERVIEW**

**Generated:** {datetime.now().isoformat()}
**Total Python Files:** {self.compliance_stats['total_files']}
**Compliant Files:** {self.compliance_stats['compliant_files']}
**Violation Files:** {self.compliance_stats['violation_files']}
**Overall Compliance:** {self.compliance_stats['overall_compliance']:.1f}%

## 🎯 **COMPLIANCE THRESHOLDS**

- **✅ EXCELLENT (≤300 lines):** V2 compliant
- **🟡 GOOD (≤500 lines):** Acceptable
- **🟠 MODERATE (≤800 lines):** Needs attention
- **🔴 MAJOR (≤1000 lines):** Major violation
- **🚨 CRITICAL (>1000 lines):** Critical violation

## 🚨 **CRITICAL VIOLATIONS (>1000 lines)**

"""
        
        if self.violations['critical']:
            for violation in self.violations['critical']:
                report += f"- **{violation['file_path']}** ({violation['line_count']} lines) - {violation['status']}\n"
        else:
            report += "- **None** - All files under 1000 lines ✅\n"
        
        report += "\n## 🔴 **MAJOR VIOLATIONS (500-1000 lines)**\n"
        
        if self.violations['major']:
            for violation in self.violations['major']:
                report += f"- **{violation['file_path']}** ({violation['line_count']} lines) - {violation['status']}\n"
        else:
            report += "- **None** - All files under 500 lines ✅\n"
        
        report += "\n## 🟠 **MODERATE VIOLATIONS (300-500 lines)**\n"
        
        if self.violations['moderate']:
            for violation in self.violations['moderate']:
                report += f"- **{violation['file_path']}** ({violation['line_count']} lines) - {violation['status']}\n"
        else:
            report += "- **None** - All files under 300 lines ✅\n"
        
        report += "\n## 🟡 **MINOR VIOLATIONS (200-300 lines)**\n"
        
        if self.violations['minor']:
            for violation in self.violations['minor']:
                report += f"- **{violation['file_path']}** ({violation['line_count']} lines) - {violation['status']}\n"
        else:
            report += "- **None** - All files under 200 lines ✅\n"
        
        report += f"""

## 📈 **COMPLIANCE RECOMMENDATIONS**

### **Immediate Actions Required:**
"""
        
        if self.violations['critical']:
            report += f"- **URGENT:** Address {len(self.violations['critical'])} critical violations (>1000 lines)\n"
        if self.violations['major']:
            report += f"- **HIGH PRIORITY:** Address {len(self.violations['major'])} major violations (500-1000 lines)\n"
        if self.violations['moderate']:
            report += f"- **MEDIUM PRIORITY:** Address {len(self.violations['moderate'])} moderate violations (300-500 lines)\n"
        
        report += f"""
### **Compliance Targets:**
- **Week 1:** Achieve 90%+ compliance (address critical violations)
- **Week 2:** Achieve 95%+ compliance (address major violations)
- **Week 3:** Achieve 98%+ compliance (address moderate violations)
- **Week 4:** Achieve 100% compliance (address all violations)

## 🔧 **NEXT STEPS**

1. **Prioritize critical violations** for immediate refactoring
2. **Break down large files** into focused modules (≤250 lines each)
3. **Apply single responsibility principle** to complex classes
4. **Implement automated compliance monitoring** with pre-commit hooks
5. **Schedule regular compliance audits** to maintain standards

---

**Agent-2 (V2 Compliance Specialist)**  
**Status:** 🔍 **COMPLIANCE ANALYSIS COMPLETE**  
**Next Action:** Address identified violations based on priority
"""
        
        return report
    
    def save_report(self, report: str, filename: str = None) -> str:
        """Save compliance report to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/V2_COMPLIANCE_VALIDATION_REPORT_{timestamp}.md"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Report saved: {filename}")
        return filename
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete V2 compliance validation."""
        print("🚀 Starting V2 compliance validation...")
        
        # Step 1: Scan repository
        scan_results = self.scan_repository()
        
        # Step 2: Analyze each file
        print("🔍 Analyzing file compliance...")
        analysis_results = []
        for file_path in scan_results['python_files']:
            result = self.analyze_file_compliance(file_path)
            analysis_results.append(result)
        
        # Step 3: Categorize violations
        violations = self.categorize_violations(analysis_results)
        
        # Step 4: Generate report
        report = self.generate_compliance_report()
        
        # Step 5: Save report
        report_file = self.save_report(report)
        
        print("✅ V2 compliance validation complete!")
        
        return {
            'scan_results': scan_results,
            'analysis_results': analysis_results,
            'violations': violations,
            'compliance_stats': self.compliance_stats,
            'report_file': report_file,
            'report_content': report
        }


def main():
    """Main execution function."""
    validator = V2ComplianceValidator()
    results = validator.run_full_validation()
    
    print(f"\n📊 COMPLIANCE SUMMARY:")
    print(f"Total Files: {results['compliance_stats']['total_files']}")
    print(f"Compliant: {results['compliance_stats']['compliant_files']}")
    print(f"Violations: {results['compliance_stats']['violation_files']}")
    print(f"Overall Compliance: {results['compliance_stats']['overall_compliance']:.1f}%")
    
    if results['violations']['critical']:
        print(f"\n🚨 CRITICAL VIOLATIONS: {len(results['violations']['critical'])}")
    if results['violations']['major']:
        print(f"🔴 MAJOR VIOLATIONS: {len(results['violations']['major'])}")
    if results['violations']['moderate']:
        print(f"🟠 MODERATE VIOLATIONS: {len(results['violations']['moderate'])}")
    
    print(f"\n📄 Full report: {results['report_file']}")


if __name__ == "__main__":
    main()
