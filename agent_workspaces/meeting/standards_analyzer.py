#!/usr/bin/env python3
"""
Standards Analyzer Module
Part of the modularized Coding Standards Implementation System

This module handles codebase analysis and compliance checking functionality.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime

class StandardsAnalyzer:
    """
    Standards analysis and compliance checking functionality.
    
    Single Responsibility: Analyze codebase for V2 coding standards compliance.
    Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
    """
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.standards_config = {
            "standard_loc_limit": 400,
            "gui_loc_limit": 600,
            "core_loc_limit": 400,
            "test_loc_limit": 500,
            "demo_loc_limit": 500
        }
    
    def analyze_codebase_standards_compliance(self) -> Dict[str, Any]:
        """
        Analyze the entire codebase for V2 coding standards compliance.
        
        Returns:
            Dict containing compliance analysis and violation details
        """
        print("🔍 ANALYZING CODEBASE FOR V2 CODING STANDARDS COMPLIANCE")
        print("=" * 60)
        
        compliance_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_compliance": 0.0,
            "total_files": 0,
            "compliant_files": 0,
            "violations": {
                "line_count": [],
                "oop_design": [],
                "cli_interface": [],
                "smoke_tests": []
            },
            "recommendations": []
        }
        
        # Scan Python files in src directory
        src_path = self.workspace_root / "src"
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
        
        # Check for function definitions outside classes
        function_pattern = r'^def\s+\w+'
        functions = re.findall(function_pattern, content, re.MULTILINE)
        
        # If no classes but functions exist, it's procedural code
        if not classes and functions:
            return "File contains procedural code without class structure"
        
        # If classes exist, check for proper OOP structure
        if classes:
            # Check for proper class structure (basic validation)
            if not re.search(r'class\s+\w+.*:', content):
                return "Classes defined but may not follow proper OOP structure"
        
        return ""
    
    def _check_cli_interface_compliance(self, content: str) -> str:
        """
        Check if file has CLI interface for testing.
        
        Args:
            content: File content as string
            
        Returns:
            Violation message if non-compliant, empty string if compliant
        """
        # Check for CLI interface patterns
        cli_patterns = [
            r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',
            r'argparse\.ArgumentParser',
            r'def\s+main\(',
            r'parse_args\('
        ]
        
        has_cli = any(re.search(pattern, content) for pattern in cli_patterns)
        
        if not has_cli:
            return "Missing CLI interface for testing and agent usability"
        
        return ""
    
    def _check_smoke_tests_compliance(self, file_path: Path) -> str:
        """
        Check if corresponding smoke tests exist.
        
        Args:
            file_path: Path to the source file
            
        Returns:
            Violation message if non-compliant, empty string if compliant
        """
        # Check for smoke tests in tests/smoke directory
        tests_path = self.workspace_root / "tests" / "smoke"
        if not tests_path.exists():
            return "Smoke tests directory not found"
        
        # Look for corresponding smoke test file
        file_name = file_path.stem
        test_file_name = f"test_{file_name}.py"
        test_file_path = tests_path / test_file_name
        
        if not test_file_path.exists():
            return f"Missing smoke test file: {test_file_name}"
        
        return ""
    
    def _generate_standards_recommendations(self, violations: Dict[str, List]) -> List[str]:
        """
        Generate recommendations based on violations found.
        
        Args:
            violations: Dictionary of violations by type
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if violations["line_count"]:
            recommendations.append(
                f"Refactor {len(violations['line_count'])} files to comply with line count limits"
            )
        
        if violations["oop_design"]:
            recommendations.append(
                f"Convert {len(violations['oop_design'])} procedural files to OOP structure"
            )
        
        if violations["cli_interface"]:
            recommendations.append(
                f"Add CLI interfaces to {len(violations['cli_interface'])} modules"
            )
        
        if violations["smoke_tests"]:
            recommendations.append(
                f"Create smoke tests for {len(violations['smoke_tests'])} components"
            )
        
        if not recommendations:
            recommendations.append("All files are compliant with V2 coding standards")
        
        return recommendations
