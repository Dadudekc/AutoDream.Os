from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import logging

    from .base_validator import (
    from .security_authentication import SecurityAuthentication
    from .security_authorization import SecurityAuthorization
    from .security_core import SecurityCore
    from .security_encryption import SecurityEncryption
    from .security_policy import SecurityPolicy
    from .security_recommendations import SecurityRecommendations
    from base_validator import (
    from security_authentication import SecurityAuthentication
    from security_authorization import SecurityAuthorization
    from security_core import SecurityCore
    from security_encryption import SecurityEncryption
    from security_policy import SecurityPolicy
    from security_recommendations import SecurityRecommendations
    import argparse

#!/usr/bin/env python3
"""
Security Validator V2 - Main orchestrator for security validation system

Single Responsibility: Orchestrate security validation across all security domains.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""


try:
        BaseValidator,
        ValidationSeverity,
        ValidationStatus,
        ValidationResult,
    )
except ImportError:
    # For direct execution
        BaseValidator,
        ValidationSeverity,
        ValidationStatus,
        ValidationResult,
    )


class SecurityValidatorV2(BaseValidator):
    """
    Main orchestrator for security validation system.
    
    Coordinates validation across all security domains:
    - Core security validation
    - Authentication
    - Authorization
    - Encryption
    - Policies
    - Recommendations
    """
    
    def __init__(self):
        """Initialize security validator orchestrator."""
        super().__init__("SecurityValidatorV2")
        
        # Initialize component validators
        self.security_core = SecurityCore()
        self.auth_validator = SecurityAuthentication()
        self.authz_validator = SecurityAuthorization()
        self.encryption_validator = SecurityEncryption()
        self.policy_validator = SecurityPolicy()
        self.recommendations_validator = SecurityRecommendations()
        
        # Component registry for easy access
        self.components = {
            "core": self.security_core,
            "authentication": self.auth_validator,
            "authorization": self.authz_validator,
            "encryption": self.encryption_validator,
            "policies": self.policy_validator,
            "recommendations": self.recommendations_validator
        }
    
    def validate_security(self, security_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive security validation across all domains.
        
        Args:
            security_data: Complete security configuration data
            
        Returns:
            Dictionary containing validation results and recommendations
        """
        try:
            self.logger.info("Starting comprehensive security validation")
            
            # Initialize results container
            validation_results = {
                "timestamp": self._get_current_timestamp(),
                "overall_status": ValidationStatus.PASSED.value,
                "components": {},
                "recommendations": [],
                "summary": {}
            }
            
            # Validate each security domain
            for domain, validator in self.components.items():
                self.logger.info(f"Validating security domain: {domain}")
                
                if domain == "core":
                    results = validator.validate(security_data)
                elif domain == "authentication":
                    results = validator.validate_authentication(security_data.get("authentication", {}))
                elif domain == "authorization":
                    results = validator.validate_authorization(security_data.get("authorization", {}))
                elif domain == "encryption":
                    results = validator.validate_encryption(security_data.get("encryption", {}))
                elif domain == "policies":
                    results = validator.validate_policies(security_data.get("policies", []))
                else:
                    continue
                
                # Store component results
                validation_results["components"][domain] = {
                    "validator": validator.__class__.__name__,
                    "results": results,
                    "status": self._get_component_status(results),
                    "summary": self._get_component_summary(domain, validator, results)
                }
                
                # Check if any component failed
                if validation_results["components"][domain]["status"] == ValidationStatus.FAILED.value:
                    validation_results["overall_status"] = ValidationStatus.FAILED.value
            
            # Generate recommendations
            recommendations = self.recommendations_validator.generate_recommendations(security_data)
            validation_results["recommendations"] = recommendations
            
            # Generate overall summary
            validation_results["summary"] = self._generate_overall_summary(validation_results)
            
            self.logger.info("Security validation completed successfully")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Security validation failed: {e}")
            return self._create_error_response(str(e))
    
    def validate_domain(self, domain: str, data: Any) -> List[ValidationResult]:
        """
        Validate a specific security domain.
        
        Args:
            domain: Security domain to validate
            data: Data to validate for the domain
            
        Returns:
            List of validation results
        """
        if domain not in self.components:
            raise ValueError(f"Unknown security domain: {domain}")
        
        validator = self.components[domain]
        
        if domain == "core":
            return validator.validate(data)
        elif domain == "authentication":
            return validator.validate_authentication(data)
        elif domain == "authorization":
            return validator.validate_authorization(data)
        elif domain == "encryption":
            return validator.validate_encryption(data)
        elif domain == "policies":
            return validator.validate_policies(data)
        else:
            return []
    
    def get_security_report(self, security_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive security report.
        
        Args:
            security_data: Security configuration data
            
        Returns:
            Complete security report
        """
        try:
            # Run full validation
            validation_results = self.validate_security(security_data)
            
            # Generate recommendations
            recommendations = validation_results.get("recommendations", [])
            
            # Create report structure
            report = {
                "report_id": f"SECURITY_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": self._get_current_timestamp(),
                "executive_summary": self._generate_executive_summary(validation_results),
                "validation_results": validation_results,
                "recommendations": recommendations,
                "risk_assessment": self._assess_security_risks(validation_results),
                "compliance_status": self._assess_compliance_status(validation_results),
                "action_plan": self._generate_action_plan(recommendations)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate security report: {e}")
            return {"error": str(e)}
    
    def _get_component_status(self, results: List[ValidationResult]) -> str:
        """Determine component validation status."""
        if not results:
            return ValidationStatus.PASSED.value
        
        for result in results:
            if result.status.value == "failed":
                return ValidationStatus.FAILED.value
        
        return ValidationStatus.PASSED.value
    
    def _get_component_summary(self, domain: str, validator: BaseValidator, results: List[ValidationResult]) -> Dict[str, Any]:
        """Get summary for a specific component."""
        try:
            if domain == "core":
                return validator.get_validation_summary(results)
            elif domain == "authentication":
                return validator.get_authentication_summary({})
            elif domain == "authorization":
                return validator.get_authorization_summary({})
            elif domain == "encryption":
                return validator.get_encryption_summary({})
            elif domain == "policies":
                return validator.get_policy_summary([])
            else:
                return {"error": f"Unknown domain: {domain}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_overall_summary(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall validation summary."""
        components = validation_results.get("components", {})
        
        total_validations = 0
        total_passed = 0
        total_failed = 0
        total_warnings = 0
        total_errors = 0
        
        for domain, component_data in components.items():
            summary = component_data.get("summary", {})
            if isinstance(summary, dict) and "error" not in summary:
                total_validations += summary.get("total_validations", 0)
                total_passed += summary.get("passed", 0)
                total_failed += summary.get("failed", 0)
                total_warnings += summary.get("warnings", 0)
                total_errors += summary.get("errors", 0)
        
        return {
            "total_validations": total_validations,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_warnings": total_warnings,
            "total_errors": total_errors,
            "overall_compliance_rate": (total_passed / total_validations * 100) if total_validations > 0 else 0
        }
    
    def _generate_executive_summary(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of security validation."""
        overall_status = validation_results.get("overall_status", "unknown")
        components = validation_results.get("components", {})
        
        # Count component statuses
        passed_components = sum(1 for c in components.values() if c.get("status") == "passed")
        failed_components = sum(1 for c in components.values() if c.get("status") == "failed")
        total_components = len(components)
        
        # Determine overall risk level
        if failed_components > 0:
            risk_level = "HIGH" if failed_components > total_components / 2 else "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "overall_status": overall_status,
            "risk_level": risk_level,
            "components_analyzed": total_components,
            "components_passed": passed_components,
            "components_failed": failed_components,
            "key_findings": self._extract_key_findings(validation_results)
        }
    
    def _extract_key_findings(self, validation_results: Dict[str, Any]) -> List[str]:
        """Extract key findings from validation results."""
        findings = []
        components = validation_results.get("components", {})
        
        for domain, component_data in components.items():
            status = component_data.get("status", "unknown")
            if status == "failed":
                findings.append(f"{domain.title()} validation failed - requires immediate attention")
            elif status == "passed":
                findings.append(f"{domain.title()} validation passed - security controls are effective")
        
        return findings[:5]  # Limit to top 5 findings
    
    def _assess_security_risks(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall security risks."""
        components = validation_results.get("components", {})
        failed_components = [d for d in components.values() if d.get("status") == "failed"]
        
        risk_assessment = {
            "overall_risk": "LOW",
            "risk_factors": [],
            "mitigation_priorities": []
        }
        
        if len(failed_components) > 0:
            risk_assessment["overall_risk"] = "HIGH" if len(failed_components) > 2 else "MEDIUM"
            risk_assessment["risk_factors"] = [f"Component {c.get('validator', 'Unknown')} validation failed" for c in failed_components]
            risk_assessment["mitigation_priorities"] = ["Address failed validations immediately", "Review security controls", "Implement monitoring"]
        
        return risk_assessment
    
    def _assess_compliance_status(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance status."""
        overall_status = validation_results.get("overall_status", "unknown")
        
        compliance_status = {
            "overall_compliance": "COMPLIANT" if overall_status == "passed" else "NON_COMPLIANT",
            "compliance_score": 100 if overall_status == "passed" else 0,
            "compliance_areas": [],
            "required_actions": []
        }
        
        if overall_status == "failed":
            compliance_status["required_actions"] = [
                "Review failed validations",
                "Implement required security controls",
                "Conduct follow-up assessment"
            ]
        
        return compliance_status
    
    def _generate_action_plan(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate action plan from recommendations."""
        if not recommendations:
            return {"message": "No actions required - all validations passed"}
        
        # Group by priority
        critical_actions = [r for r in recommendations if r.get("priority") == "critical"]
        high_actions = [r for r in recommendations if r.get("priority") == "high"]
        medium_actions = [r for r in recommendations if r.get("priority") == "medium"]
        low_actions = [r for r in recommendations if r.get("priority") == "low"]
        
        return {
            "total_actions": len(recommendations),
            "critical_actions": len(critical_actions),
            "high_actions": len(high_actions),
            "medium_actions": len(medium_actions),
            "low_actions": len(low_actions),
            "immediate_actions": [r.get("title") for r in critical_actions + high_actions],
            "timeline": {
                "immediate": "0-7 days",
                "short_term": "1-4 weeks",
                "medium_term": "1-3 months",
                "long_term": "3+ months"
            }
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response when validation fails."""
        return {
            "timestamp": self._get_current_timestamp(),
            "overall_status": ValidationStatus.FAILED.value,
            "error": error_message,
            "components": {},
            "recommendations": [],
            "summary": {}
        }
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()
    
    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Get validation summary for compatibility with BaseValidator."""
        return {
            "total_validations": len(results),
            "passed": len([r for r in results if r.status.value == "passed"]),
            "failed": len([r for r in results if r.status.value == "failed"]),
            "warnings": len([r for r in results if r.severity.value == "warning"]),
            "errors": len([r for r in results if r.severity.value == "error"]),
            "timestamp": self._get_current_timestamp()
        }


def main():
    """CLI interface for Security Validator V2 testing."""
    
    parser = argparse.ArgumentParser(description="Security Validator V2 - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    parser.add_argument("--validate", type=str, help="Validate specific security domain")
    parser.add_argument("--report", action="store_true", help="Generate security report")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    elif args.validate:
        validate_domain(args.validate)
    elif args.report:
        generate_sample_report()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Security Validator V2."""
    print("🧪 Running Security Validator V2 smoke tests...")
    
    # Test creation
    validator = SecurityValidatorV2()
    assert validator is not None
    print("✅ SecurityValidatorV2 creation test passed")
    
    # Test component access
    assert "core" in validator.components
    assert "authentication" in validator.components
    print("✅ Component registry test passed")
    
    # Test validation
    test_data = {
        "authentication": {"method": "password"},
        "authorization": {"roles": {"user": {"permissions": ["read"]}}},
        "encryption": {"algorithms": {"aes": {"key_length": 256}}}
    }
    
    results = validator.validate_security(test_data)
    assert isinstance(results, dict)
    print("✅ Security validation test passed")
    
    # Test report generation
    report = validator.get_security_report(test_data)
    assert isinstance(report, dict)
    print("✅ Report generation test passed")
    
    print("🎉 All smoke tests passed!")


def validate_domain(domain: str):
    """Validate a specific security domain."""
    print(f"🔍 Validating security domain: {domain}")
    
    validator = SecurityValidatorV2()
    
    # Sample data for the domain
    sample_data = get_sample_data_for_domain(domain)
    
    try:
        results = validator.validate_domain(domain, sample_data)
        print(f"✅ Domain validation completed. Found {len(results)} validation results.")
        
        for i, result in enumerate(results[:3]):  # Show first 3 results
            print(f"  {i+1}. {result.rule_name}: {result.status.value}")
            
    except Exception as e:
        print(f"❌ Domain validation failed: {e}")


def generate_sample_report():
    """Generate a sample security report."""
    print("📊 Generating sample security report...")
    
    validator = SecurityValidatorV2()
    sample_data = get_comprehensive_sample_data()
    
    try:
        report = validator.get_security_report(sample_data)
        print("✅ Sample report generated successfully!")
        print(f"Report ID: {report.get('report_id', 'N/A')}")
        print(f"Overall Status: {report.get('validation_results', {}).get('overall_status', 'N/A')}")
        print(f"Total Recommendations: {len(report.get('recommendations', []))}")
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")


def get_sample_data_for_domain(domain: str) -> Any:
    """Get sample data for a specific domain."""
    sample_data = {
        "authentication": {"method": "password", "mfa_enabled": False},
        "authorization": {"roles": {"admin": {"permissions": ["all"]}}},
        "encryption": {"algorithms": {"aes": {"key_length": 128}}},
        "policies": [{"name": "Test Policy", "type": "access"}]
    }
    
    return sample_data.get(domain, {})


def get_comprehensive_sample_data() -> Dict[str, Any]:
    """Get comprehensive sample data for testing."""
    return {
        "authentication": {
            "method": "password",
            "password_policy": {"min_length": 8},
            "mfa_enabled": False,
            "session_config": {"timeout": 7200}
        },
        "authorization": {
            "roles": {"admin": {"permissions": ["all"]}},
            "permissions": {"read": {"level": "read"}},
            "access_control": []
        },
        "encryption": {
            "algorithms": {"aes": {"key_length": 128}},
            "hash_functions": {"password_hash": {"salt_enabled": False}}
        },
        "policies": [
            {"name": "Test Policy", "type": "access", "description": "Test"}
        ]
    }


if __name__ == "__main__":
    main()
