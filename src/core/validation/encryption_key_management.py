#!/usr/bin/env python3
"""
Encryption Key Management - Key management validation for security system

Single Responsibility: Validate encryption key management configuration.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""

from typing import Dict, List, Any
from .base_validator import (
    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class EncryptionKeyManagement(BaseValidator):
    """Validates encryption key management configuration."""
    
    def __init__(self):
        """Initialize key management validator."""
        super().__init__("EncryptionKeyManagement")
        self.valid_key_sources = ["random", "hardware", "derived"]
        self.valid_storage_types = ["memory", "file", "database", "hardware", "cloud"]
        self.max_rotation_interval = 365  # 1 year
    
    def validate_key_management(self, key_mgmt: Any) -> List[ValidationResult]:
        """Validate key management configuration."""
        results = []
        
        if not isinstance(key_mgmt, dict):
            results.append(self._create_result(
                rule_id="key_management_type",
                rule_name="Key Management Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Key management must be a dictionary"
            ))
            return results
        
        # Validate key generation
        if "key_generation" in key_mgmt:
            key_gen_results = self._validate_key_generation(key_mgmt["key_generation"])
            results.extend(key_gen_results)
        
        # Validate key storage
        if "key_storage" in key_mgmt:
            storage_results = self._validate_key_storage(key_mgmt["key_storage"])
            results.extend(storage_results)
        
        # Validate key rotation
        if "key_rotation" in key_mgmt:
            rotation_results = self._validate_key_rotation(key_mgmt["key_rotation"])
            results.extend(rotation_results)
        
        return results
    
    def _validate_key_generation(self, key_gen: Any) -> List[ValidationResult]:
        """Validate key generation configuration."""
        results = []
        
        if not isinstance(key_gen, dict):
            results.append(self._create_result(
                rule_id="key_generation_type",
                rule_name="Key Generation Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Key generation must be a dictionary"
            ))
            return results
        
        # Validate key source
        if "source" in key_gen:
            source = key_gen["source"]
            if source not in self.valid_key_sources:
                results.append(self._create_result(
                    rule_id="key_generation_source",
                    rule_name="Key Generation Source",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid key generation source: {source}. Valid sources: {', '.join(self.valid_key_sources)}"
                ))
        
        return results
    
    def _validate_key_storage(self, key_storage: Any) -> List[ValidationResult]:
        """Validate key storage configuration."""
        results = []
        
        if not isinstance(key_storage, dict):
            results.append(self._create_result(
                rule_id="key_storage_type",
                rule_name="Key Storage Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Key storage must be a dictionary"
            ))
            return results
        
        # Validate storage type
        if "type" in key_storage:
            storage_type = key_storage["type"]
            if storage_type not in self.valid_storage_types:
                results.append(self._create_result(
                    rule_id="key_storage_type_value",
                    rule_name="Key Storage Type Value",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid key storage type: {storage_type}. Valid types: {', '.join(self.valid_storage_types)}"
                ))
        
        return results
    
    def _validate_key_rotation(self, key_rotation: Any) -> List[ValidationResult]:
        """Validate key rotation configuration."""
        results = []
        
        if not isinstance(key_rotation, dict):
            results.append(self._create_result(
                rule_id="key_rotation_type",
                rule_name="Key Rotation Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Key rotation must be a dictionary"
            ))
            return results
        
        # Validate rotation interval
        if "interval" in key_rotation:
            interval = key_rotation["interval"]
            if not isinstance(interval, int) or interval <= 0:
                results.append(self._create_result(
                    rule_id="key_rotation_interval",
                    rule_name="Key Rotation Interval",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Key rotation interval must be a positive integer"
                ))
            elif interval > self.max_rotation_interval:
                results.append(self._create_result(
                    rule_id="key_rotation_interval_long",
                    rule_name="Key Rotation Interval Long",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message=f"Key rotation interval is very long ({interval} days), consider reducing for security"
                ))
        
        return results


def main():
    """CLI interface for Encryption Key Management testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Encryption Key Management - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Encryption Key Management."""
    print("🧪 Running Encryption Key Management smoke tests...")
    
    # Test creation
    key_mgmt_validator = EncryptionKeyManagement()
    assert key_mgmt_validator is not None
    print("✅ EncryptionKeyManagement creation test passed")
    
    # Test validation
    test_data = {
        "key_generation": {"source": "random"},
        "key_storage": {"type": "hardware"},
        "key_rotation": {"interval": 90}
    }
    results = key_mgmt_validator.validate_key_management(test_data)
    assert len(results) > 0
    print("✅ Key management validation test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
