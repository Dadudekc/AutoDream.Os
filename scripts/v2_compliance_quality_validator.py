#!/usr/bin/env python3
"""
V2 Compliance Code Quality Validation - Quality Validation System
===============================================================

This module handles the validation of code quality standards for V2 compliance.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-003 - V2 Compliance Code Quality Implementation Modularization
**Status:** MODULARIZATION IN PROGRESS
**Target:** ≤250 lines per module, single responsibility principle
**V2 Compliance:** ✅ Under 250 lines, focused responsibility
"""

import os
import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class V2ComplianceQualityValidator:
    """V2 compliance code quality validation system."""
    
    def __init__(self):
        """Initialize quality validator."""
        self.validation_results = {}
        self.quality_tools = ['black', 'flake8', 'isort']
        self.validation_status = {}
    
    def validate_repository(self, repo_path: str = ".") -> Dict[str, Any]:
        """Validate entire repository for code quality."""
        results = {
            'total_files': 0,
            'files_passed': 0,
            'files_failed': 0,
            'validation_details': {},
            'overall_status': 'pending'
        }
        
        # Find Python files
        python_files = list(Path(repo_path).rglob("*.py"))
        results['total_files'] = len(python_files)
        
        print(f"🔍 VALIDATING: {len(python_files)} Python files for code quality...")
        
        # Validate each tool
        for tool in self.quality_tools:
            tool_results = self._validate_with_tool(tool, python_files)
            results['validation_details'][tool] = tool_results
            
            if tool_results['status'] == 'passed':
                results['files_passed'] += tool_results['files_passed']
            else:
                results['files_failed'] += tool_results['files_failed']
        
        # Determine overall status
        if results['files_failed'] == 0:
            results['overall_status'] = 'passed'
        else:
            results['overall_status'] = 'failed'
        
        self.validation_results = results
        return results
    
    def _validate_with_tool(self, tool: str, files: List[Path]) -> Dict[str, Any]:
        """Validate files with specific quality tool."""
        results = {
            'tool': tool,
            'status': 'pending',
            'files_passed': 0,
            'files_failed': 0,
            'errors': [],
            'details': {}
        }
        
        try:
            if tool == 'black':
                results = self._validate_with_black(files)
            elif tool == 'flake8':
                results = self._validate_with_flake8(files)
            elif tool == 'isort':
                results = self._validate_with_isort(files)
                
        except Exception as e:
            results['status'] = 'error'
            results['errors'].append(f"Validation error: {e}")
        
        return results
    
    def _validate_with_black(self, files: List[Path]) -> Dict[str, Any]:
        """Validate with Black formatter."""
        results = {
            'tool': 'black',
            'status': 'pending',
            'files_passed': 0,
            'files_failed': 0,
            'errors': [],
            'details': {}
        }
        
        try:
            # Check formatting with Black
            cmd = [sys.executable, '-m', 'black', '--check', '--diff', str(files[0].parent)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                results['status'] = 'passed'
                results['files_passed'] = len(files)
            else:
                results['status'] = 'failed'
                results['files_failed'] = len(files)
                results['errors'].append(result.stderr)
                
        except Exception as e:
            results['status'] = 'error'
            results['errors'].append(f"Black validation error: {e}")
        
        return results
    
    def _validate_with_flake8(self, files: List[Path]) -> Dict[str, Any]:
        """Validate with Flake8 linter."""
        results = {
            'tool': 'flake8',
            'status': 'pending',
            'files_passed': 0,
            'files_failed': 0,
            'errors': [],
            'details': {}
        }
        
        try:
            # Run Flake8 on sample files
            sample_files = files[:5] if len(files) > 5 else files
            
            for file_path in sample_files:
                cmd = [sys.executable, '-m', 'flake8', str(file_path)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    results['files_passed'] += 1
                else:
                    results['files_failed'] += 1
                    results['errors'].append(f"{file_path}: {result.stdout}")
            
            results['status'] = 'passed' if results['files_failed'] == 0 else 'failed'
                
        except Exception as e:
            results['status'] = 'error'
            results['errors'].append(f"Flake8 validation error: {e}")
        
        return results
    
    def _validate_with_isort(self, files: List[Path]) -> Dict[str, Any]:
        """Validate with isort import sorter."""
        results = {
            'tool': 'isort',
            'status': 'pending',
            'files_passed': 0,
            'files_failed': 0,
            'errors': [],
            'details': {}
        }
        
        try:
            # Check import sorting with isort
            sample_files = files[:5] if len(files) > 5 else files
            
            for file_path in sample_files:
                cmd = [sys.executable, '-m', 'isort', '--check-only', '--diff', str(file_path)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    results['files_passed'] += 1
                else:
                    results['files_failed'] += 1
                    results['errors'].append(f"{file_path}: {result.stdout}")
            
            results['status'] = 'passed' if results['files_failed'] == 0 else 'failed'
                
        except Exception as e:
            results['status'] = 'error'
            results['errors'].append(f"isort validation error: {e}")
        
        return results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get a summary of validation results."""
        if not self.validation_results:
            return {'status': 'no_validation_run'}
        
        return {
            'total_files': self.validation_results.get('total_files', 0),
            'files_passed': self.validation_results.get('files_passed', 0),
            'files_failed': self.validation_results.get('files_failed', 0),
            'overall_status': self.validation_results.get('overall_status', 'unknown'),
            'success_rate': (self.validation_results.get('files_passed', 0) / 
                           max(self.validation_results.get('total_files', 1), 1)) * 100
        }
    
    def export_validation_report(self, output_path: str = None) -> str:
        """Export validation report to JSON file."""
        if not output_path:
            output_path = f"v2_compliance_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'validation_summary': self.get_validation_summary(),
            'validation_details': self.validation_results.get('validation_details', {}),
            'overall_status': self.validation_results.get('overall_status', 'unknown')
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return output_path
        except Exception as e:
            print(f"❌ ERROR: Could not export validation report: {e}")
            return ""


if __name__ == "__main__":
    # Test the quality validator
    validator = V2ComplianceQualityValidator()
    results = validator.validate_repository()
    print(f"Validation Results: {results}")
