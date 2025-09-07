#!/usr/bin/env python3
"""
Standards Core Module
====================

Core functionality for coding standards implementation.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class StandardsViolation:
    """Represents a coding standards violation"""
    violation_type: str
    file_path: str
    line_number: Optional[int] = None
    details: str = ""
    severity: str = "medium"


@dataclass
class FileComplianceReport:
    """Represents compliance report for a single file"""
    file_path: str
    compliant: bool
    violations: List[StandardsViolation]
    line_count: int
    oop_score: float
    srp_score: float
    cli_score: float
    test_score: float


class StandardsCore:
    """Core coding standards functionality"""
    
    def __init__(self, workspace_root: str = "../../"):
        self.workspace_root = Path(workspace_root)
        self.standards_config = {
            "standard_loc_limit": 400,
            "gui_loc_limit": 600,
            "core_loc_limit": 400,
            "test_loc_limit": 500,
            "demo_loc_limit": 500
        }
        
        # V2 Coding Standards
        self.v2_standards = {
            "oop_design": "All code must be properly OOP",
            "single_responsibility": "One class = one responsibility",
            "cli_interface": "Every module must have CLI interface",
            "smoke_tests": "Basic functionality tests required",
            "agent_usability": "Easy to test and use",
            "line_count": "≤400 LOC (standard), ≤600 LOC (GUI)"
        }
        
    def analyze_file_standards_compliance(self, file_path: Path) -> FileComplianceReport:
        """Analyze a single file for coding standards compliance"""
        try:
            violations = []
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            line_count = len(lines)
            
            # Check line count compliance
            if not self._check_line_count_compliance(file_path, line_count):
                violations.append(StandardsViolation(
                    violation_type="line_count",
                    file_path=str(file_path),
                    details=f"File has {line_count} lines, exceeds limit"
                ))
            
            # Check OOP design compliance
            oop_score = self._check_oop_design_compliance(content)
            if oop_score < 0.7:
                violations.append(StandardsViolation(
                    violation_type="oop_design",
                    file_path=str(file_path),
                    details=f"OOP design score: {oop_score:.2f}"
                ))
            
            # Check single responsibility principle
            srp_score = self._check_srp_compliance(content)
            if srp_score < 0.7:
                violations.append(StandardsViolation(
                    violation_type="single_responsibility",
                    file_path=str(file_path),
                    details=f"SRP compliance score: {srp_score:.2f}"
                ))
            
            # Check CLI interface
            cli_score = self._check_cli_interface_compliance(content)
            if cli_score < 0.5:
                violations.append(StandardsViolation(
                    violation_type="cli_interface",
                    file_path=str(file_path),
                    details=f"CLI interface score: {cli_score:.2f}"
                ))
            
            # Check smoke tests
            test_score = self._check_smoke_tests_compliance(file_path)
            if test_score < 0.5:
                violations.append(StandardsViolation(
                    violation_type="smoke_tests",
                    file_path=str(file_path),
                    details=f"Smoke tests score: {test_score:.2f}"
                ))
            
            # Determine overall compliance
            compliant = len(violations) == 0
            
            return FileComplianceReport(
                file_path=str(file_path),
                compliant=compliant,
                violations=violations,
                line_count=line_count,
                oop_score=oop_score,
                srp_score=srp_score,
                cli_score=cli_score,
                test_score=test_score
            )
            
        except Exception as e:
            # Return failed report
            return FileComplianceReport(
                file_path=str(file_path),
                compliant=False,
                violations=[StandardsViolation(
                    violation_type="analysis_error",
                    file_path=str(file_path),
                    details=f"Error analyzing file: {str(e)}"
                )],
                line_count=0,
                oop_score=0.0,
                srp_score=0.0,
                cli_score=0.0,
                test_score=0.0
            )
    
    def _check_line_count_compliance(self, file_path: Path, line_count: int) -> bool:
        """Check if file meets line count requirements"""
        try:
            # Determine file type and applicable limit
            if "gui" in file_path.name.lower() or "frontend" in str(file_path):
                limit = self.standards_config["gui_loc_limit"]
            elif "test" in file_path.name.lower():
                limit = self.standards_config["test_loc_limit"]
            elif "demo" in file_path.name.lower():
                limit = self.standards_config["demo_loc_limit"]
            elif "core" in str(file_path):
                limit = self.standards_config["core_loc_limit"]
            else:
                limit = self.standards_config["standard_loc_limit"]
            
            return line_count <= limit
            
        except Exception:
            return False
    
    def _check_oop_design_compliance(self, content: str) -> float:
        """Check OOP design compliance score (0.0 - 1.0)"""
        try:
            score = 0.0
            
            # Check for class definitions
            if re.search(r'class\s+\w+', content):
                score += 0.3
            
            # Check for proper class structure
            if re.search(r'def\s+__init__', content):
                score += 0.2
            
            # Check for methods
            if re.search(r'def\s+\w+\s*\(', content):
                score += 0.2
            
            # Check for inheritance
            if re.search(r'class\s+\w+\s*\(', content):
                score += 0.2
            
            # Check for encapsulation (private methods)
            if re.search(r'def\s+_\w+', content):
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    def _check_srp_compliance(self, content: str) -> float:
        """Check single responsibility principle compliance (0.0 - 1.0)"""
        try:
            score = 0.0
            
            # Count classes
            class_count = len(re.findall(r'class\s+\w+', content))
            
            # Count methods per class (approximate)
            method_count = len(re.findall(r'def\s+\w+\s*\(', content))
            
            if class_count > 0:
                # Calculate methods per class
                methods_per_class = method_count / class_count
                
                # Score based on methods per class (fewer is better for SRP)
                if methods_per_class <= 5:
                    score += 0.4
                elif methods_per_class <= 10:
                    score += 0.2
                
                # Bonus for single class files
                if class_count == 1:
                    score += 0.3
                
                # Check for clear class names
                class_names = re.findall(r'class\s+(\w+)', content)
                for name in class_names:
                    if len(name.split('_')) <= 2:  # Simple names
                        score += 0.1
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    def _check_cli_interface_compliance(self, content: str) -> float:
        """Check CLI interface compliance (0.0 - 1.0)"""
        try:
            score = 0.0
            
            # Check for main function
            if re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', content):
                score += 0.3
            
            # Check for argument parsing
            if re.search(r'argparse|sys\.argv', content):
                score += 0.3
            
            # Check for print statements (basic CLI output)
            if re.search(r'print\s*\(', content):
                score += 0.2
            
            # Check for input handling
            if re.search(r'input\s*\(', content):
                score += 0.2
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    def _check_smoke_tests_compliance(self, file_path: Path) -> float:
        """Check smoke tests compliance (0.0 - 1.0)"""
        try:
            score = 0.0
            
            # Check if test file exists
            test_file = self._find_test_file(file_path)
            if test_file and test_file.exists():
                score += 0.5
                
                # Check test file content
                with open(test_file, 'r', encoding='utf-8') as f:
                    test_content = f.read()
                    
                    # Check for test functions
                    if re.search(r'def\s+test_', test_content):
                        score += 0.3
                    
                    # Check for basic assertions
                    if re.search(r'assert\s+', test_content):
                        score += 0.2
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    def _find_test_file(self, file_path: Path) -> Optional[Path]:
        """Find corresponding test file for a given file"""
        try:
            # Look for test file in tests directory
            tests_dir = self.workspace_root / "tests"
            if tests_dir.exists():
                # Try to find test file with similar name
                file_name = file_path.stem
                test_file = tests_dir / f"test_{file_name}.py"
                if test_file.exists():
                    return test_file
            
            return None
            
        except Exception:
            return None
    
    def get_standards_summary(self) -> Dict[str, Any]:
        """Get summary of coding standards"""
        return {
            "standards": self.v2_standards,
            "config": self.standards_config,
            "timestamp": datetime.now().isoformat()
        }
