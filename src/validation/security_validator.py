#!/usr/bin/env python3
"""
Security Validator
==================

Validates security measures and sensitive information handling.
V2 Compliance: ≤150 lines, focused responsibility, KISS principle.
"""

from pathlib import Path
from typing import Dict, List, Any


class SecurityValidator:
    """Validates security measures."""
    
    def validate(self) -> Dict[str, Any]:
        """Validate security measures."""
        print("🔍 Validating security measures...")
        
        # Check for security-related files
        security_files_status = self._check_security_files()
        
        # Check for sensitive information in code
        security_violations = self._scan_for_sensitive_info()
        
        security_clean = len(security_violations) == 0
        all_security_files_present = all(security_files_status.values())
        
        overall_security = security_clean and all_security_files_present
        
        return {
            "category": "security_validation",
            "status": "PASSED" if overall_security else "FAILED",
            "results": {
                "security_files_present": security_files_status,
                "security_violations": security_violations,
                "security_clean": security_clean
            },
            "summary": f"Security: {'Clean' if security_clean else f'{len(security_violations)} violations'}"
        }
    
    def _check_security_files(self) -> Dict[str, bool]:
        """Check if required security files exist."""
        security_files = [
            ".env",
            "requirements.txt",
            "quality_gates.py"
        ]
        
        security_status = {}
        for file in security_files:
            security_status[file] = Path(file).exists()
        
        return security_status
    
    def _scan_for_sensitive_info(self) -> List[str]:
        """Scan for sensitive information in code."""
        sensitive_patterns = [
            "password", "secret", "key", "token", "api_key"
        ]
        
        security_violations = []
        
        try:
            for py_file in Path(".").glob("**/*.py"):
                if "agent_workspaces" in str(py_file):
                    continue
                    
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    for pattern in sensitive_patterns:
                        if pattern in content and "example" not in content:
                            security_violations.append(f"{py_file}: {pattern}")
        
        except Exception:
            pass
        
        return security_violations
