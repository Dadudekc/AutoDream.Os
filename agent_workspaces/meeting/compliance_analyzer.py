#!/usr/bin/env python3
"""
Compliance Analyzer Module
V2 Compliance: File analysis and compliance checking functionality

This module contains the ComplianceAnalyzer class that analyzes files for
V2 coding standards compliance while maintaining V2 compliance limits.
"""

import re
from pathlib import Path
from typing import Dict, List, Any


class ComplianceAnalyzer:
    """
    File compliance analyzer for V2 coding standards.
    
    Single Responsibility: Analyze files for coding standards compliance.
    Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
    """
    
    def __init__(self, standards_config: Dict[str, Any]):
        self.standards_config = standards_config
    
    def analyze_codebase(self, workspace_root: Path) -> Dict[str, Any]:
        """
        Analyze the entire codebase for V2 coding standards compliance.
        
        Args:
            workspace_root: Root path of the workspace
            
        Returns:
            Dict containing compliance analysis and violation details
        """
        compliance_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_compliance": 0.0,
            "total_files": 0,
            "compliant_files": 0,
            "violations": {
                "line_count": [],
                "oop_design": [],
                "single_responsibility": [],
                "cli_interface": [],
                "smoke_tests": []
            },
            "recommendations": []
        }
        
        # Scan Python files in src directory
        src_path = workspace_root / "src"
        if src_path.exists():
            python_files = list(src_path.rglob("*.py"))
            compliance_report["total_files"] = len(python_files)
            
            for file_path in python_files:
                file_analysis = self._analyze_file_standards_compliance(file_path)
                if file_analysis["compliant"]:
                    compliance_report["compliant_files"] += 1
                else:
                    for violation_type, details in file_analysis["violations"].items():
                        if details:
                            compliance_report["violations"][violation_type].append({
                                "file": str(file_path),
                                "details": details
                            })
        
        # Calculate overall compliance
        if compliance_report["total_files"] > 0:
            compliance_report["overall_compliance"] = (
                compliance_report["compliant_files"] / compliance_report["total_files"]
            ) * 100
        
        # Generate recommendations
        compliance_report["recommendations"] = self._generate_standards_recommendations(
            compliance_report["violations"]
        )
        
        return compliance_report
    
    def _analyze_file_standards_compliance(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a single file for V2 coding standards compliance.
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            Dict containing compliance analysis for the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            analysis = {
                "file": str(file_path),
                "compliant": True,
                "line_count": len(lines),
                "violations": {},
                "recommendations": []
            }
            
            # Check line count compliance
            loc_violation = self._check_line_count_compliance(file_path, lines)
            if loc_violation:
                analysis["compliant"] = False
                analysis["violations"]["line_count"] = loc_violation
            
            # Check OOP design compliance
            oop_violation = self._check_oop_design_compliance(content)
            if oop_violation:
                analysis["compliant"] = False
                analysis["violations"]["oop_design"] = oop_violation
            
            # Check CLI interface compliance
            cli_violation = self._check_cli_interface_compliance(content)
            if cli_violation:
                analysis["compliant"] = False
                analysis["violations"]["cli_interface"] = cli_violation
            
            # Check smoke tests compliance
            tests_violation = self._check_smoke_tests_compliance(file_path)
            if tests_violation:
                analysis["compliant"] = False
                analysis["violations"]["smoke_tests"] = tests_violation
            
            return analysis
            
        except Exception as e:
            return {
                "file": str(file_path),
                "compliant": False,
                "error": str(e),
                "violations": {"error": f"Could not analyze file: {e}"}
            }
    
    def _check_line_count_compliance(self, file_path: Path, lines: List[str]) -> str:
        """
        Check if file complies with line count standards.
        
        Args:
            file_path: Path to the file
            lines: List of lines in the file
            
        Returns:
            Violation message if non-compliant, empty string if compliant
        """
        line_count = len(lines)
        file_name = file_path.name.lower()
        
        # Determine appropriate limit based on file type
        if "test" in file_name:
            limit = self.standards_config["test_loc_limit"]
            file_type = "test"
        elif "demo" in file_name or "example" in file_name:
            limit = self.standards_config["demo_loc_limit"]
            file_type = "demo/example"
        elif "gui" in file_name or "frontend" in file_name or "web" in file_name:
            limit = self.standards_config["gui_loc_limit"]
            file_type = "GUI"
        else:
            limit = self.standards_config["standard_loc_limit"]
            file_type = "standard"
        
        if line_count > limit:
            return f"File exceeds {file_type} limit: {line_count} lines (limit: {limit})"
        
        return ""
    
    def _check_oop_design_compliance(self, content: str) -> str:
        """
        Check if file follows OOP design principles.
        
        Args:
            content: File content as string
            
        Returns:
            Violation message if non-compliant, empty string if compliant
        """
        # Check for class definitions
        class_pattern = r'class\s+\w+'
        classes = re.findall(class_pattern, content)
        
        if not classes:
            return "No class definitions found - procedural code detected"
        
        # Check for proper class structure
        if not re.search(r'class\s+\w+.*:', content):
            return "Invalid class definition syntax"
        
        return ""
    
    def _check_cli_interface_compliance(self, content: str) -> str:
        """
        Check if file has CLI interface.
        
        Args:
            content: File content as string
            
        Returns:
            Violation message if non-compliant, empty string if compliant
        """
        # Check for main function or CLI interface
        if not re.search(r'def\s+main\s*\(', content) and not re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]', content):
            return "No CLI interface found - missing main function or __main__ block"
        
        return ""
    
    def _check_smoke_tests_compliance(self, file_path: Path) -> str:
        """
        Check if file has associated smoke tests.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Violation message if non-compliant, empty string if compliant
        """
        # Look for test file in same directory
        test_file = file_path.parent / f"test_{file_path.name}"
        if not test_file.exists():
            return "No associated test file found"
        
        return ""
    
    def _generate_standards_recommendations(self, violations: Dict[str, List]) -> List[str]:
        """
        Generate recommendations based on violations.
        
        Args:
            violations: Dictionary of violations by type
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if violations["line_count"]:
            recommendations.append(f"Refactor {len(violations['line_count'])} files to meet line count limits")
        
        if violations["oop_design"]:
            recommendations.append(f"Convert {len(violations['oop_design'])} procedural files to OOP structure")
        
        if violations["cli_interface"]:
            recommendations.append(f"Add CLI interfaces to {len(violations['cli_interface'])} modules")
        
        if violations["smoke_tests"]:
            recommendations.append(f"Create smoke tests for {len(violations['smoke_tests'])} components")
        
        if not recommendations:
            recommendations.append("All files are compliant with V2 standards")
        
        return recommendations


# Import datetime for timestamp generation
from datetime import datetime
