#!/usr/bin/env python3
"""
Contract Audit and Cleanup Script
Phase 1: Audit & Cleanup (Immediate)

This script performs a comprehensive audit of all contract files to:
1. Verify all contract file paths against actual repository
2. Remove contracts for non-existent files
3. Update line counts for existing files
4. Identify truly actionable violations
"""

import json
import os
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Any
import sys

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

class ContractAuditor:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.contracts_dir = project_root / "contracts"
        self.audit_results = {
            "total_contracts": 0,
            "valid_contracts": 0,
            "invalid_contracts": 0,
            "files_not_found": [],
            "files_already_refactored": [],
            "actionable_violations": [],
            "cleanup_actions": []
        }
        
    def get_all_contract_files(self) -> List[Path]:
        """Get all contract JSON files in the contracts directory."""
        contract_files = []
        if self.contracts_dir.exists():
            contract_files = list(self.contracts_dir.glob("*.json"))
        return contract_files
    
    def count_file_lines(self, file_path: Path) -> int:
        """Count the number of lines in a file."""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return len(f.readlines())
            return 0
        except Exception as e:
            print(f"Error counting lines in {file_path}: {e}")
            return 0
    
    def verify_file_exists(self, file_path: str) -> Tuple[bool, Path]:
        """Verify if a file path exists in the repository."""
        full_path = self.project_root / file_path
        return full_path.exists(), full_path
    
    def audit_contract_file(self, contract_file: Path) -> Dict[str, Any]:
        """Audit a single contract file."""
        print(f"🔍 Auditing {contract_file.name}...")
        
        try:
            with open(contract_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Error reading {contract_file}: {e}")
            return {"error": str(e)}
        
        audit_result = {
            "contract_file": contract_file.name,
            "total_contracts": 0,
            "valid_contracts": 0,
            "invalid_contracts": 0,
            "files_not_found": [],
            "files_already_refactored": [],
            "actionable_violations": [],
            "needs_update": False
        }
        
        if "contracts" in data:
            contracts = data["contracts"]
            audit_result["total_contracts"] = len(contracts)
            
            for contract in contracts:
                if "file_path" in contract:
                    file_path = contract["file_path"]
                    exists, full_path = self.verify_file_exists(file_path)
                    
                    if not exists:
                        audit_result["invalid_contracts"] += 1
                        audit_result["files_not_found"].append({
                            "contract_id": contract.get("contract_id", "UNKNOWN"),
                            "file_path": file_path,
                            "reason": "File not found"
                        })
                        audit_result["needs_update"] = True
                    else:
                        # File exists, check current line count
                        current_lines = self.count_file_lines(full_path)
                        contract_lines = contract.get("current_lines", 0)
                        
                        if current_lines != contract_lines:
                            audit_result["needs_update"] = True
                        
                        # Check if file is already compliant
                        target_lines = contract.get("target_lines", 400)
                        if current_lines <= target_lines:
                            audit_result["files_already_refactored"].append({
                                "contract_id": contract.get("contract_id", "UNKNOWN"),
                                "file_path": file_path,
                                "old_lines": contract_lines,
                                "current_lines": current_lines,
                                "target_lines": target_lines
                            })
                            audit_result["needs_update"] = True
                        else:
                            audit_result["valid_contracts"] += 1
                            audit_result["actionable_violations"].append({
                                "contract_id": contract.get("contract_id", "UNKNOWN"),
                                "file_path": file_path,
                                "current_lines": current_lines,
                                "target_lines": target_lines,
                                "priority": contract.get("priority", "UNKNOWN")
                            })
        
        return audit_result
    
    def update_contract_file(self, contract_file: Path, audit_result: Dict[str, Any]) -> bool:
        """Update a contract file by removing invalid contracts and updating line counts."""
        if not audit_result.get("needs_update", False):
            return False
            
        print(f"📝 Updating {contract_file.name}...")
        
        try:
            with open(contract_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Error reading {contract_file}: {e}")
            return False
        
        if "contracts" in data:
            original_count = len(data["contracts"])
            
            # Remove contracts for non-existent files
            if audit_result["files_not_found"]:
                not_found_paths = {item["file_path"] for item in audit_result["files_not_found"]}
                data["contracts"] = [
                    contract for contract in data["contracts"]
                    if contract.get("file_path") not in not_found_paths
                ]
            
            # Remove contracts for already refactored files
            if audit_result["files_already_refactored"]:
                already_refactored_paths = {item["file_path"] for item in audit_result["files_already_refactored"]}
                data["contracts"] = [
                    contract for contract in data["contracts"]
                    if contract.get("file_path") not in already_refactored_paths
                ]
            
            # Update line counts for remaining contracts
            for contract in data["contracts"]:
                if "file_path" in contract:
                    file_path = contract["file_path"]
                    exists, full_path = self.verify_file_exists(file_path)
                    if exists:
                        current_lines = self.count_file_lines(full_path)
                        contract["current_lines"] = current_lines
            
            # Update total files count
            if "total_files" in data:
                data["total_files"] = len(data["contracts"])
            
            # Write updated file
            with open(contract_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            new_count = len(data["contracts"])
            print(f"✅ Updated {contract_file.name}: {original_count} → {new_count} contracts")
            
            return True
        
        return False
    
    def generate_audit_report(self) -> str:
        """Generate a comprehensive audit report."""
        report = []
        report.append("# 🧹 Contract Audit Report - Phase 1: Audit & Cleanup")
        report.append(f"Generated: {Path().cwd()}")
        report.append("")
        
        # Summary
        report.append("## 📊 Audit Summary")
        report.append(f"- **Total Contract Files**: {len(self.audit_results.get('contract_files', []))}")
        report.append(f"- **Total Contracts**: {self.audit_results.get('total_contracts', 0)}")
        report.append(f"- **Valid Contracts**: {self.audit_results.get('valid_contracts', 0)}")
        report.append(f"- **Invalid Contracts**: {self.audit_results.get('invalid_contracts', 0)}")
        report.append("")
        
        # Files not found
        if self.audit_results.get("files_not_found"):
            report.append("## ❌ Files Not Found (Contracts to Remove)")
            for item in self.audit_results["files_not_found"]:
                report.append(f"- **{item['contract_id']}**: `{item['file_path']}` - {item['reason']}")
            report.append("")
        
        # Files already refactored
        if self.audit_results.get("files_already_refactored"):
            report.append("## ✅ Files Already Refactored (Contracts to Remove)")
            for item in self.audit_results["files_already_refactored"]:
                report.append(f"- **{item['contract_id']}**: `{item['file_path']}` - {item['old_lines']} → {item['current_lines']} lines (target: {item['target_lines']})")
            report.append("")
        
        # Actionable violations
        if self.audit_results.get("actionable_violations"):
            report.append("## 🎯 Actionable Violations (Valid Contracts)")
            for item in self.audit_results["actionable_violations"]:
                report.append(f"- **{item['contract_id']}**: `{item['file_path']}` - {item['current_lines']} lines (target: {item['target_lines']}) - Priority: {item['priority']}")
            report.append("")
        
        # Cleanup actions
        if self.audit_results.get("cleanup_actions"):
            report.append("## 🧹 Cleanup Actions Performed")
            for action in self.audit_results["cleanup_actions"]:
                report.append(f"- {action}")
            report.append("")
        
        return "\n".join(report)
    
    def run_full_audit(self) -> Dict[str, Any]:
        """Run the complete audit process."""
        print("🚀 Starting Contract Audit and Cleanup...")
        print(f"📁 Project Root: {self.project_root}")
        print(f"📋 Contracts Directory: {self.contracts_dir}")
        print()
        
        # Get all contract files
        contract_files = self.get_all_contract_files()
        print(f"📄 Found {len(contract_files)} contract files")
        print()
        
        self.audit_results["contract_files"] = contract_files
        
        # Audit each contract file
        for contract_file in contract_files:
            audit_result = self.audit_contract_file(contract_file)
            
            # Aggregate results
            self.audit_results["total_contracts"] += audit_result.get("total_contracts", 0)
            self.audit_results["valid_contracts"] += audit_result.get("valid_contracts", 0)
            self.audit_results["invalid_contracts"] += audit_result.get("invalid_contracts", 0)
            self.audit_results["files_not_found"].extend(audit_result.get("files_not_found", []))
            self.audit_results["files_already_refactored"].extend(audit_result.get("files_already_refactored", []))
            self.audit_results["actionable_violations"].extend(audit_result.get("actionable_violations", []))
            
            # Update contract file if needed
            if audit_result.get("needs_update", False):
                if self.update_contract_file(contract_file, audit_result):
                    self.audit_results["cleanup_actions"].append(f"Updated {contract_file.name}")
        
        print()
        print("🎯 Audit Complete!")
        print(f"📊 Total Contracts: {self.audit_results['total_contracts']}")
        print(f"✅ Valid Contracts: {self.audit_results['valid_contracts']}")
        print(f"❌ Invalid Contracts: {self.audit_results['invalid_contracts']}")
        print(f"🧹 Cleanup Actions: {len(self.audit_results['cleanup_actions'])}")
        
        return self.audit_results

def main():
    """Main entry point."""
    project_root = Path(__file__).resolve().parents[1]
    
    if not project_root.exists():
        print(f"❌ Project root not found: {project_root}")
        return 1
    
    # Run audit
    auditor = ContractAuditor(project_root)
    results = auditor.run_full_audit()
    
    # Generate and save report
    report = auditor.generate_audit_report()
    report_file = project_root / "docs" / "reports" / "CONTRACT_AUDIT_REPORT.md"
    
    try:
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📝 Audit report saved to: {report_file}")
    except Exception as e:
        print(f"❌ Error saving report: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("📋 AUDIT SUMMARY")
    print("="*60)
    print(f"Total Contracts: {results['total_contracts']}")
    print(f"Valid Contracts: {results['valid_contracts']}")
    print(f"Invalid Contracts: {results['invalid_contracts']}")
    print(f"Files Not Found: {len(results['files_not_found'])}")
    print(f"Already Refactored: {len(results['files_already_refactored'])}")
    print(f"Actionable Violations: {len(results['actionable_violations'])}")
    print(f"Cleanup Actions: {len(results['cleanup_actions'])}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
