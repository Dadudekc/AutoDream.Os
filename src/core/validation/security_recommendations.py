from datetime import datetime
from typing import Dict, List, Any, Optional
import re

    import argparse
from .base_validator import (

#!/usr/bin/env python3
"""
Security Recommendations - Security recommendations and best practices

Single Responsibility: Generate and validate security recommendations.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""


    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class SecurityRecommendations(BaseValidator):
    """Generates and validates security recommendations."""
    
    def __init__(self):
        """Initialize recommendations validator."""
        super().__init__("SecurityRecommendations")
        self.recommendation_categories = [
            "authentication", "authorization", "encryption", "network", "data", "compliance"
        ]
        self.priority_levels = ["low", "medium", "high", "critical"]
        self.implementation_effort = ["easy", "medium", "hard", "expert"]
    
    def generate_recommendations(self, security_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate security recommendations based on validation results."""
        recommendations = []
        
        try:
            # Generate authentication recommendations
            if "authentication" in security_data:
                auth_recs = self._generate_auth_recommendations(security_data["authentication"])
                recommendations.extend(auth_recs)
            
            # Generate authorization recommendations
            if "authorization" in security_data:
                authz_recs = self._generate_authz_recommendations(security_data["authorization"])
                recommendations.extend(authz_recs)
            
            # Generate encryption recommendations
            if "encryption" in security_data:
                enc_recs = self._generate_encryption_recommendations(security_data["encryption"])
                recommendations.extend(enc_recs)
            
            # Generate policy recommendations
            if "policies" in security_data:
                policy_recs = self._generate_policy_recommendations(security_data["policies"])
                recommendations.extend(policy_recs)
            
            # Generate general security recommendations
            general_recs = self._generate_general_recommendations(security_data)
            recommendations.extend(general_recs)
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
            error_rec = {
                "category": "error",
                "priority": "high",
                "effort": "easy",
                "title": "Recommendation Generation Error",
                "description": f"Failed to generate recommendations: {str(e)}",
                "action_items": ["Check system logs", "Verify data integrity"],
                "timestamp": self._get_current_timestamp()
            }
            recommendations.append(error_rec)
        
        return recommendations
    
    def _generate_auth_recommendations(self, auth_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate authentication recommendations."""
        recommendations = []
        
        # Check for weak password policies
        if "password_policy" in auth_data:
            policy = auth_data["password_policy"]
            if policy.get("min_length", 0) < 12:
                recommendations.append({
                    "category": "authentication",
                    "priority": "high",
                    "effort": "easy",
                    "title": "Increase Minimum Password Length",
                    "description": "Current minimum password length is below recommended 12 characters",
                    "action_items": [
                        "Update password policy to require minimum 12 characters",
                        "Consider requiring 16+ characters for admin accounts"
                    ],
                    "timestamp": self._get_current_timestamp()
                })
        
        # Check for MFA configuration
        if not auth_data.get("mfa_enabled", False):
            recommendations.append({
                "category": "authentication",
                "priority": "critical",
                "effort": "medium",
                "title": "Enable Multi-Factor Authentication",
                "description": "MFA is not enabled, significantly increasing security risk",
                "action_items": [
                    "Enable MFA for all user accounts",
                    "Configure backup MFA methods",
                    "Implement MFA bypass procedures for emergencies"
                ],
                "timestamp": self._get_current_timestamp()
            })
        
        # Check session configuration
        if "session_config" in auth_data:
            session_config = auth_data["session_config"]
            timeout = session_config.get("timeout", 0)
            if timeout > 3600:  # More than 1 hour
                recommendations.append({
                    "category": "authentication",
                    "priority": "medium",
                    "effort": "easy",
                    "title": "Reduce Session Timeout",
                    "description": "Session timeout is very long, increasing exposure risk",
                    "action_items": [
                        "Reduce session timeout to 1 hour or less",
                        "Enable session renewal for active users",
                        "Implement automatic logout for inactive sessions"
                    ],
                    "timestamp": self._get_current_timestamp()
                })
        
        return recommendations
    
    def _generate_authz_recommendations(self, authz_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate authorization recommendations."""
        recommendations = []
        
        # Check for role-based access control
        if "roles" in authz_data:
            roles = authz_data["roles"]
            if len(roles) < 3:
                recommendations.append({
                    "category": "authorization",
                    "priority": "medium",
                    "effort": "medium",
                    "title": "Implement Role-Based Access Control",
                    "description": "Limited role definitions may indicate insufficient access control granularity",
                    "action_items": [
                        "Define clear role hierarchies",
                        "Implement principle of least privilege",
                        "Create role templates for common job functions"
                    ],
                    "timestamp": self._get_current_timestamp()
                })
        
        # Check for permission granularity
        if "permissions" in authz_data:
            permissions = authz_data["permissions"]
            if len(permissions) < 5:
                recommendations.append({
                    "category": "authorization",
                    "priority": "medium",
                    "effort": "hard",
                    "title": "Improve Permission Granularity",
                    "description": "Limited permission definitions may indicate overly broad access controls",
                    "action_items": [
                        "Break down broad permissions into specific actions",
                        "Implement resource-level permissions",
                        "Add context-aware permission checks"
                    ],
                    "timestamp": self._get_current_timestamp()
                })
        
        # Check for access control lists
        if "access_control" not in authz_data:
            recommendations.append({
                "category": "authorization",
                "priority": "high",
                "effort": "medium",
                "title": "Implement Access Control Lists",
                "description": "No access control lists found, indicating potential security gaps",
                "action_items": [
                    "Define access control lists for all resources",
                    "Implement regular access reviews",
                    "Automate access provisioning and deprovisioning"
                ],
                "timestamp": self._get_current_timestamp()
            })
        
        return recommendations
    
    def _generate_encryption_recommendations(self, enc_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate encryption recommendations."""
        recommendations = []
        
        # Check encryption algorithms
        if "algorithms" in enc_data:
            algorithms = enc_data["algorithms"]
            for algo_name, algo_config in algorithms.items():
                if "key_length" in algo_config:
                    key_length = algo_config["key_length"]
                    if key_length < 256:
                        recommendations.append({
                            "category": "encryption",
                            "priority": "high",
                            "effort": "medium",
                            "title": f"Upgrade {algo_name} Key Length",
                            "description": f"Key length {key_length} bits is below recommended 256 bits",
                            "action_items": [
                                f"Upgrade {algo_name} to use 256-bit or longer keys",
                                "Consider AES-256-GCM for symmetric encryption",
                                "Use RSA-2048 or longer for asymmetric encryption"
                            ],
                            "timestamp": self._get_current_timestamp()
                        })
        
        # Check key management
        if "key_management" in enc_data:
            key_mgmt = enc_data["key_management"]
            if "key_rotation" not in key_mgmt:
                recommendations.append({
                    "category": "encryption",
                    "priority": "high",
                    "effort": "medium",
                    "title": "Implement Key Rotation",
                    "description": "No key rotation policy found, increasing long-term security risk",
                    "action_items": [
                        "Implement automated key rotation",
                        "Set rotation intervals (90 days recommended)",
                        "Establish key backup and recovery procedures"
                    ],
                    "timestamp": self._get_current_timestamp()
                })
            else:
                rotation = key_mgmt["key_rotation"]
                interval = rotation.get("interval", 0)
                if interval > 365:  # More than 1 year
                    recommendations.append({
                        "category": "encryption",
                        "priority": "medium",
                        "effort": "easy",
                        "title": "Reduce Key Rotation Interval",
                        "description": f"Key rotation interval of {interval} days is too long",
                        "action_items": [
                            "Reduce key rotation interval to 90 days or less",
                            "Implement automated rotation reminders",
                            "Monitor key usage patterns"
                        ],
                        "timestamp": self._get_current_timestamp()
                    })
        
        # Check hash functions
        if "hash_functions" in enc_data:
            hash_funcs = enc_data["hash_functions"]
            for func_name, func_config in hash_funcs.items():
                if not func_config.get("salt_enabled", False):
                    recommendations.append({
                        "category": "encryption",
                        "priority": "high",
                        "effort": "easy",
                        "title": f"Enable Salt for {func_name}",
                        "description": f"Hash function {func_name} does not use salt, making it vulnerable to rainbow table attacks",
                        "action_items": [
                            f"Enable salt generation for {func_name}",
                            "Use cryptographically secure random salt",
                            "Ensure salt length is at least 16 bytes"
                        ],
                        "timestamp": self._get_current_timestamp()
                    })
        
        return recommendations
    
    def _generate_policy_recommendations(self, policies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate policy recommendations."""
        recommendations = []
        
        # Check policy coverage
        if len(policies) < 5:
            recommendations.append({
                "category": "policies",
                "priority": "medium",
                "effort": "hard",
                "title": "Expand Security Policy Coverage",
                "description": "Limited number of security policies may indicate gaps in coverage",
                "action_items": [
                    "Develop comprehensive security policy framework",
                    "Cover all major security domains",
                    "Include incident response and business continuity policies"
                ],
                "timestamp": self._get_current_timestamp()
            })
        
        # Check policy enforcement
        for i, policy in enumerate(policies):
            if "enforcement" not in policy:
                recommendations.append({
                    "category": "policies",
                    "priority": "medium",
                    "effort": "medium",
                    "title": f"Add Enforcement to Policy {i+1}",
                    "description": f"Policy '{policy.get('name', f'Policy {i+1}')}' lacks enforcement mechanisms",
                    "action_items": [
                        "Define enforcement actions and procedures",
                        "Implement monitoring and alerting",
                        "Establish escalation procedures"
                    ],
                    "timestamp": self._get_current_timestamp()
                })
        
        return recommendations
    
    def _generate_general_recommendations(self, security_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate general security recommendations."""
        recommendations = []
        
        # Check for security monitoring
        if "monitoring" not in security_data:
            recommendations.append({
                "category": "general",
                "priority": "high",
                "effort": "hard",
                "title": "Implement Security Monitoring",
                "description": "No security monitoring configuration found",
                "action_items": [
                    "Implement SIEM (Security Information and Event Management)",
                    "Configure log collection and analysis",
                    "Set up real-time alerting for security events"
                ],
                "timestamp": self._get_current_timestamp()
            })
        
        # Check for incident response
        if "incident_response" not in security_data:
            recommendations.append({
                "category": "general",
                "priority": "high",
                "effort": "hard",
                "title": "Establish Incident Response Plan",
                "description": "No incident response procedures defined",
                "action_items": [
                    "Develop incident response playbook",
                    "Define roles and responsibilities",
                    "Establish communication procedures",
                    "Practice incident response scenarios"
                ],
                "timestamp": self._get_current_timestamp()
            })
        
        # Check for security training
        if "training" not in security_data:
            recommendations.append({
                "category": "general",
                "priority": "medium",
                "effort": "medium",
                "title": "Implement Security Awareness Training",
                "description": "No security training program found",
                "action_items": [
                    "Develop security awareness curriculum",
                    "Implement regular training sessions",
                    "Include phishing simulation exercises",
                    "Track training completion rates"
                ],
                "timestamp": self._get_current_timestamp()
            })
        
        return recommendations
    
    def validate_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[ValidationResult]:
        """Validate recommendation structure and content."""
        results = []
        
        if not isinstance(recommendations, list):
            results.append(self._create_result(
                rule_id="recommendations_type",
                rule_name="Recommendations Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Recommendations must be a list"
            ))
            return results
        
        for i, rec in enumerate(recommendations):
            if not isinstance(rec, dict):
                results.append(self._create_result(
                    rule_id="recommendation_item_type",
                    rule_name="Recommendation Item Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Recommendation item {i} must be a dictionary"
                ))
                continue
            
            # Validate required fields
            required_fields = ["category", "priority", "effort", "title", "description"]
            for field in required_fields:
                if field not in rec:
                    results.append(self._create_result(
                        rule_id=f"recommendation_missing_{field}",
                        rule_name=f"Recommendation Missing {field.title()}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Recommendation {i} missing required field: {field}"
                    ))
            
            # Validate category
            if "category" in rec:
                category = rec["category"]
                if category not in self.recommendation_categories and category != "error":
                    results.append(self._create_result(
                        rule_id="recommendation_category",
                        rule_name="Recommendation Category",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid recommendation category: {category}. Valid categories: {', '.join(self.recommendation_categories)}"
                    ))
            
            # Validate priority
            if "priority" in rec:
                priority = rec["priority"]
                if priority not in self.priority_levels:
                    results.append(self._create_result(
                        rule_id="recommendation_priority",
                        rule_name="Recommendation Priority",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid recommendation priority: {priority}. Valid priorities: {', '.join(self.priority_levels)}"
                    ))
            
            # Validate effort
            if "effort" in rec:
                effort = rec["effort"]
                if effort not in self.implementation_effort:
                    results.append(self._create_result(
                        rule_id="recommendation_effort",
                        rule_name="Recommendation Effort",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid recommendation effort: {effort}. Valid effort levels: {', '.join(self.implementation_effort)}"
                    ))
            
            # Validate action items
            if "action_items" in rec:
                action_items = rec["action_items"]
                if not isinstance(action_items, list):
                    results.append(self._create_result(
                        rule_id="recommendation_action_items_type",
                        rule_name="Recommendation Action Items Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Recommendation action items must be a list for recommendation {i}"
                    ))
                else:
                    for j, item in enumerate(action_items):
                        if not isinstance(item, str):
                            results.append(self._create_result(
                                rule_id="recommendation_action_item_type",
                                rule_name="Recommendation Action Item Type",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=f"Recommendation action item {j} must be a string in recommendation {i}"
                            ))
        
        return results
    
    def get_recommendations_summary(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get recommendations summary."""
        try:
            validation_results = self.validate_recommendations(recommendations)
            
            # Count by category and priority
            category_counts = {}
            priority_counts = {}
            effort_counts = {}
            
            for rec in recommendations:
                category = rec.get("category", "unknown")
                priority = rec.get("priority", "unknown")
                effort = rec.get("effort", "unknown")
                
                category_counts[category] = category_counts.get(category, 0) + 1
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
                effort_counts[effort] = effort_counts.get(effort, 0) + 1
            
            return {
                "total_recommendations": len(recommendations),
                "validation_results": {
                    "total_validations": len(validation_results),
                    "passed": len([r for r in validation_results if r.status.value == "passed"]),
                    "failed": len([r for r in validation_results if r.status.value == "failed"])
                },
                "category_distribution": category_counts,
                "priority_distribution": priority_counts,
                "effort_distribution": effort_counts,
                "timestamp": self._get_current_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get recommendations summary: {e}")
            return {"error": str(e)}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()


def main():
    """CLI interface for Security Recommendations testing."""
    
    parser = argparse.ArgumentParser(description="Security Recommendations - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Security Recommendations."""
    print("🧪 Running Security Recommendations smoke tests...")
    
    # Test creation
    rec_validator = SecurityRecommendations()
    assert rec_validator is not None
    print("✅ SecurityRecommendations creation test passed")
    
    # Test recommendation generation
    test_data = {
        "authentication": {
            "password_policy": {"min_length": 8},
            "mfa_enabled": False,
            "session_config": {"timeout": 7200}
        },
        "authorization": {
            "roles": {"admin": {"permissions": ["all"]}},
            "permissions": {"read": {"level": "read"}}
        },
        "encryption": {
            "algorithms": {
                "aes": {"key_length": 128}
            },
            "hash_functions": {
                "password_hash": {"salt_enabled": False}
            }
        },
        "policies": [
            {"name": "Test Policy", "type": "access"}
        ]
    }
    
    recommendations = rec_validator.generate_recommendations(test_data)
    assert len(recommendations) > 0
    print("✅ Recommendation generation test passed")
    
    # Test validation
    validation_results = rec_validator.validate_recommendations(recommendations)
    assert len(validation_results) > 0
    print("✅ Recommendation validation test passed")
    
    # Test summary
    summary = rec_validator.get_recommendations_summary(recommendations)
    assert isinstance(summary, dict)
    print("✅ Summary test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
