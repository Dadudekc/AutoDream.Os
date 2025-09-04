#!/usr/bin/env python3
"""
DRY Compliance Validator - V2 Compliant
=======================================

This module provides comprehensive DRY compliance validation across the entire codebase.

Author: Agent-7 - Web Development Specialist (DRY Consolidation)
Created: 2025-01-27
Purpose: Validate DRY compliance and identify violations
"""




class DRYComplianceValidator:
    """
    Comprehensive DRY compliance validation system.
    
    VALIDATES:
    - No duplicate code patterns
    - Proper use of unified utilities
    - Consistent import organization
    - No duplicate function definitions
    - No duplicate class patterns
    """
    
    def __init__(self):
        """Initialize DRY compliance validator."""
        self.logger = UnifiedLoggingUtility.get_logger(__name__)
        self.config = UnifiedConfigurationUtility.get_unified_config().load_config()
        self.project_root = get_unified_utility().Path(__file__).parent.parent.parent
        
        # DRY violation patterns to check
        self.violation_patterns = {
            "duplicate_logging": [
                r'logger\s*=\s*logging\.getLogger',
                r'logging\.basicConfig',
                r'logger\.error\(',
                r'logger\.info\(',
                r'logger\.warning\(',
                r'logger\.debug\('
            ],
            "duplicate_config": [
                r'config\s*=\s*\{\}',
                r'self\.config\s*=\s*config\s*or\s*\{\}',
                r'load.*config',
                r'get.*config'
            ],
            "duplicate_validation": [
                r'def validate_',
                r'class.*Validator',
                r'validation.*error',
                r'raise.*ValidationError'
            ],
            "duplicate_utilities": [
                r'def.*util',
                r'class.*Util',
                r'helper.*function',
                r'common.*function'
            ],
            "duplicate_imports": [
                r'^import\s+.*$',
                r'^from\s+.*import\s+.*$'
            ],
            "duplicate_functions": [
                r'def\s+\w+\([^)]*\):',
                r'class\s+\w+[^:]*:'
            ]
        }
        
        # Expected unified patterns
        self.unified_patterns = {
            "logging": [
                r'UnifiedLoggingUtility\.get_logger',
                r'UnifiedLoggingUtility\.log_info',
                r'UnifiedLoggingUtility\.log_error',
                r'UnifiedLoggingUtility\.log_warning',
                r'UnifiedLoggingUtility\.log_debug'
            ],
            "configuration": [
                r'UnifiedConfigurationUtility\.load_config',
                r'UnifiedConfigurationUtility\.get_config',
                r'UnifiedConfigurationUtility\.save_config'
            ],
            "error_handling": [
                r'UnifiedErrorHandlingUtility\.handle_operation_error',
                r'UnifiedErrorHandlingUtility\.handle_validation_error',
                r'UnifiedErrorHandlingUtility\.handle_system_error'
            ]
        }

    def validate_dry_compliance(self) -> Dict[str, Any]:
        """
        Validate DRY compliance across the entire codebase.
        
        Returns:
            Dict[str, Any]: Comprehensive compliance report
        """
        self.get_logger(__name__).info("🔍 Starting comprehensive DRY compliance validation...")
        
        compliance_report = {
            "total_files_checked": 0,
            "compliant_files": 0,
            "non_compliant_files": 0,
            "total_violations_found": 0,
            "violation_breakdown": {},
            "compliance_rate": 0.0,
            "recommendations": [],
            "errors": []
        }
        
        try:
            # Find all Python files
            python_files = list(self.project_root.rglob("*.py"))
            compliance_report["total_files_checked"] = len(python_files)
            
            # Check each file for compliance
            for file_path in python_files:
                try:
                    file_compliance = self._get_unified_validator().check_file_compliance(file_path)
                    
                    if file_compliance["is_compliant"]:
                        compliance_report["compliant_files"] += 1
                    else:
                        compliance_report["non_compliant_files"] += 1
                        compliance_report["total_violations_found"] += file_compliance["violation_count"]
                        
                        # Add to violation breakdown
                        for violation_type, count in file_compliance["violations"].items():
                            if violation_type not in compliance_report["violation_breakdown"]:
                                compliance_report["violation_breakdown"][violation_type] = 0
                            compliance_report["violation_breakdown"][violation_type] += count
                
                except Exception as e:
                    error_msg = f"Error checking {file_path}: {e}"
                    self.get_logger(__name__).error(error_msg)
                    compliance_report["errors"].append(error_msg)
            
            # Calculate compliance rate
            if compliance_report["total_files_checked"] > 0:
                compliance_report["compliance_rate"] = (
                    compliance_report["compliant_files"] / compliance_report["total_files_checked"]
                ) * 100
            
            # Generate recommendations
            compliance_report["recommendations"] = self._generate_recommendations(compliance_report)
            
            self.get_logger(__name__).info(f"✅ DRY compliance validation complete! Compliance rate: {compliance_report['compliance_rate']:.2f}%")
            
        except Exception as e:
            error_msg = f"Error during DRY compliance validation: {e}"
            self.get_logger(__name__).error(error_msg)
            compliance_report["errors"].append(error_msg)
        
        return compliance_report

    def _get_unified_validator().check_file_compliance(self, file_path: Path) -> Dict[str, Any]:
        """Check DRY compliance for a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            violations = {}
            total_violations = 0
            
            # Check for each type of violation
            for violation_type, patterns in self.violation_patterns.items():
                violation_count = 0
                
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    if matches:
                        violation_count += len(matches)
                
                if violation_count > 0:
                    violations[violation_type] = violation_count
                    total_violations += violation_count
            
            # Check for proper use of unified patterns
            unified_usage = self._get_unified_validator().check_unified_pattern_usage(content)
            
            # Determine if file is compliant
            is_compliant = total_violations == 0 and unified_usage["proper_usage"]
            
            return {
                "file_path": str(file_path),
                "is_compliant": is_compliant,
                "violation_count": total_violations,
                "violations": violations,
                "unified_usage": unified_usage
            }
            
        except Exception as e:
            self.get_logger(__name__).error(f"Error checking file {file_path}: {e}")
            return {
                "file_path": str(file_path),
                "is_compliant": False,
                "violation_count": 1,
                "violations": {"file_error": 1},
                "unified_usage": {"proper_usage": False, "issues": [str(e)]}
            }

    def _get_unified_validator().check_unified_pattern_usage(self, content: str) -> Dict[str, Any]:
        """Check if file properly uses unified patterns."""
        proper_usage = True
        issues = []
        
        # Check for proper logging usage
        if 'logger' in content and 'UnifiedLoggingUtility' not in content:
            proper_usage = False
            issues.append("Uses logger but not UnifiedLoggingUtility")
        
        # Check for proper config usage
        if 'config' in content and 'UnifiedConfigurationUtility' not in content:
            proper_usage = False
            issues.append("Uses config but not UnifiedConfigurationUtility")
        
        # Check for proper error handling usage
        if 'error' in content and 'UnifiedErrorHandlingUtility' not in content:
            proper_usage = False
            issues.append("Uses error handling but not UnifiedErrorHandlingUtility")
        
        return {
            "proper_usage": proper_usage,
            "issues": issues
        }

    def _generate_recommendations(self, compliance_report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on compliance report."""
        recommendations = []
        
        # Check violation breakdown for specific recommendations
        violation_breakdown = compliance_report.get("violation_breakdown", {})
        
        if "duplicate_logging" in violation_breakdown:
            recommendations.append(
                f"Replace {violation_breakdown['duplicate_logging']} duplicate logging patterns with UnifiedLoggingUtility"
            )
        
        if "duplicate_config" in violation_breakdown:
            recommendations.append(
                f"Replace {violation_breakdown['duplicate_config']} duplicate config patterns with UnifiedConfigurationUtility"
            )
        
        if "duplicate_validation" in violation_breakdown:
            recommendations.append(
                f"Consolidate {violation_breakdown['duplicate_validation']} duplicate validation patterns"
            )
        
        if "duplicate_utilities" in violation_breakdown:
            recommendations.append(
                f"Consolidate {violation_breakdown['duplicate_utilities']} duplicate utility patterns"
            )
        
        if "duplicate_imports" in violation_breakdown:
            recommendations.append(
                f"Standardize {violation_breakdown['duplicate_imports']} duplicate import statements"
            )
        
        if "duplicate_functions" in violation_breakdown:
            recommendations.append(
                f"Consolidate {violation_breakdown['duplicate_functions']} duplicate function definitions"
            )
        
        # General recommendations
        if compliance_report["compliance_rate"] < 80:
            recommendations.append("Overall compliance rate is below 80% - consider comprehensive refactoring")
        
        if compliance_report["non_compliant_files"] > 0:
            recommendations.append(f"Focus on {compliance_report['non_compliant_files']} non-compliant files first")
        
        return recommendations

    def validate_specific_file(self, file_path: str) -> Dict[str, Any]:
        """Validate DRY compliance for a specific file."""
        try:
            full_path = self.project_root / file_path
            if not full_path.exists():
                return {
                    "error": f"File {file_path} does not exist",
                    "is_compliant": False
                }
            
            return self._get_unified_validator().check_file_compliance(full_path)
            
        except Exception as e:
            return {
                "error": f"Error validating {file_path}: {e}",
                "is_compliant": False
            }

    def validate_directory(self, directory_path: str) -> Dict[str, Any]:
        """Validate DRY compliance for a specific directory."""
        try:
            full_path = self.project_root / directory_path
            if not full_path.exists():
                return {
                    "error": f"Directory {directory_path} does not exist",
                    "is_compliant": False
                }
            
            # Find all Python files in directory
            python_files = list(full_path.rglob("*.py"))
            
            directory_report = {
                "directory_path": str(full_path),
                "total_files": len(python_files),
                "compliant_files": 0,
                "non_compliant_files": 0,
                "total_violations": 0,
                "violation_breakdown": {},
                "files": []
            }
            
            # Check each file
            for file_path in python_files:
                file_compliance = self._get_unified_validator().check_file_compliance(file_path)
                directory_report["files"].append(file_compliance)
                
                if file_compliance["is_compliant"]:
                    directory_report["compliant_files"] += 1
                else:
                    directory_report["non_compliant_files"] += 1
                    directory_report["total_violations"] += file_compliance["violation_count"]
                    
                    # Add to violation breakdown
                    for violation_type, count in file_compliance["violations"].items():
                        if violation_type not in directory_report["violation_breakdown"]:
                            directory_report["violation_breakdown"][violation_type] = 0
                        directory_report["violation_breakdown"][violation_type] += count
            
            # Calculate compliance rate
            if directory_report["total_files"] > 0:
                directory_report["compliance_rate"] = (
                    directory_report["compliant_files"] / directory_report["total_files"]
                ) * 100
            
            return directory_report
            
        except Exception as e:
            return {
                "error": f"Error validating directory {directory_path}: {e}",
                "is_compliant": False
            }


# Convenience function for backward compatibility
def validate_dry_compliance() -> Dict[str, Any]:
    """Validate DRY compliance across the entire codebase."""
    validator = DRYComplianceValidator()
    return validator.validate_dry_compliance()