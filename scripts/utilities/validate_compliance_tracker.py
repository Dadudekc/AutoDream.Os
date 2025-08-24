#!/usr/bin/env python3
"""
V2 Compliance Tracker Validation Script
Maintains single source of truth for compliance tracking
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ComplianceTrackerValidator:
    """Validates and maintains V2 compliance tracker consistency"""
    
    def __init__(self, repo_root: str = None):
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).parent.parent.parent
        self.tracker_files = [
            self.repo_root / "V2_COMPLIANCE_PROGRESS_TRACKER.md",
            self.repo_root / "docs" / "reports" / "V2_COMPLIANCE_PROGRESS_TRACKER.md"
        ]
        
    def analyze_python_files(self) -> Dict[str, List[Tuple[str, int, str]]]:
        """Analyze all Python files and categorize by line count violations"""
        violations = {
            "critical": [],    # 800+ lines
            "major": [],       # 500-799 lines
            "moderate": [],    # 300-499 lines
            "compliant": []    # <300 lines
        }
        
        for py_file in self.repo_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                
                relative_path = str(py_file.relative_to(self.repo_root))
                
                if lines >= 800:
                    violations["critical"].append((relative_path, lines, str(py_file)))
                elif lines >= 500:
                    violations["major"].append((relative_path, lines, str(py_file)))
                elif lines >= 300:
                    violations["moderate"].append((relative_path, lines, str(py_file)))
                else:
                    violations["compliant"].append((relative_path, lines, str(py_file)))
                    
            except Exception as e:
                print(f"Error reading {py_file}: {e}")
                
        return violations
    
    def validate_tracker_consistency(self) -> Dict[str, any]:
        """Validate consistency between tracker files"""
        results = {
            "status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Check if both files exist
        if not all(f.exists() for f in self.tracker_files):
            results["status"] = "error"
            results["issues"].append("One or more tracker files missing")
            return results
            
        # Read both files
        try:
            with open(self.tracker_files[0], 'r', encoding='utf-8') as f:
                root_content = f.read()
            with open(self.tracker_files[1], 'r', encoding='utf-8') as f:
                docs_content = f.read()
        except Exception as e:
            results["status"] = "error"
            results["issues"].append(f"Error reading tracker files: {e}")
            return results
            
        # Check for Git merge conflicts
        if "<<<<<<< HEAD" in root_content or ">>>>>>>" in root_content:
            results["status"] = "error"
            results["issues"].append("Git merge conflicts detected in root tracker")
            
        # Check for duplicate entries
        if root_content.count("CONTRACT #021") > 1:
            results["status"] = "warning"
            results["issues"].append("Duplicate contract entries detected")
            
        # Check content consistency
        if root_content != docs_content:
            results["status"] = "warning"
            results["issues"].append("Tracker files are not identical")
            results["recommendations"].append("Synchronize tracker files")
        else:
            results["status"] = "consistent"
            
        return results
    
    def generate_compliance_report(self) -> Dict[str, any]:
        """Generate comprehensive compliance report"""
        violations = self.analyze_python_files()
        
        total_files = sum(len(files) for files in violations.values())
        compliant_files = len(violations["compliant"])
        compliance_percentage = (compliant_files / total_files * 100) if total_files > 0 else 0
        
        return {
            "summary": {
                "total_python_files": total_files,
                "compliant_files": compliant_files,
                "non_compliant_files": total_files - compliant_files,
                "compliance_percentage": round(compliance_percentage, 1)
            },
            "violations": {
                "critical": len(violations["critical"]),
                "major": len(violations["major"]),
                "moderate": len(violations["moderate"])
            },
            "contracts_needed": {
                "phase_1": len(violations["critical"]),
                "phase_2": len(violations["major"]),
                "phase_3": len(violations["moderate"]),
                "phase_4": 10  # Integration & validation
            },
            "detailed_violations": violations
        }
    
    def update_tracker_files(self, force_sync: bool = False) -> bool:
        """Update tracker files to maintain consistency"""
        try:
            # Read root file as source of truth
            with open(self.tracker_files[0], 'r', encoding='utf-8') as f:
                root_content = f.read()
                
            # Update docs file to match
            docs_file = self.tracker_files[1]
            docs_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(docs_file, 'w', encoding='utf-8') as f:
                f.write(root_content)
                
            print(f"✅ Synchronized {docs_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating tracker files: {e}")
            return False
    
    def run_full_validation(self) -> Dict[str, any]:
        """Run complete validation and return results"""
        print("🔍 Running V2 Compliance Tracker Validation...")
        print("=" * 60)
        
        # Analyze Python files
        print("\n📊 Analyzing Python files...")
        violations = self.analyze_python_files()
        
        total_files = sum(len(files) for files in violations.values())
        print(f"   Total Python files: {total_files}")
        print(f"   Critical violations (800+ lines): {len(violations['critical'])}")
        print(f"   Major violations (500-799 lines): {len(violations['major'])}")
        print(f"   Moderate violations (300-499 lines): {len(violations['moderate'])}")
        print(f"   Compliant files (<300 lines): {len(violations['compliant'])}")
        
        # Validate tracker consistency
        print("\n🔍 Validating tracker consistency...")
        consistency = self.validate_tracker_consistency()
        print(f"   Status: {consistency['status']}")
        
        if consistency['issues']:
            for issue in consistency['issues']:
                print(f"   ⚠️  Issue: {issue}")
                
        if consistency['recommendations']:
            for rec in consistency['recommendations']:
                print(f"   💡 Recommendation: {rec}")
        
        # Generate compliance report
        print("\n📈 Generating compliance report...")
        report = self.generate_compliance_report()
        
        print(f"   Compliance: {report['summary']['compliance_percentage']}%")
        print(f"   Contracts needed: {sum(report['contracts_needed'].values())}")
        
        # Update tracker files if needed
        if consistency['status'] != 'consistent':
            print("\n🔄 Updating tracker files...")
            if self.update_tracker_files():
                print("   ✅ Tracker files synchronized")
            else:
                print("   ❌ Failed to synchronize tracker files")
        
        print("\n" + "=" * 60)
        print("✅ Validation complete!")
        
        return {
            "violations": violations,
            "consistency": consistency,
            "report": report
        }

def main():
    """Main entry point"""
    validator = ComplianceTrackerValidator()
    
    try:
        results = validator.run_full_validation()
        
        # Save detailed results to JSON
        output_file = validator.repo_root / "data" / "compliance_validation_results.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
            
        print(f"\n📄 Detailed results saved to: {output_file}")
        
        # Exit with error code if issues found
        if results['consistency']['status'] == 'error':
            sys.exit(1)
        elif results['consistency']['status'] == 'warning':
            sys.exit(2)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

