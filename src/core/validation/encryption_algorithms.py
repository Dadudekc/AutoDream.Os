#!/usr/bin/env python3
"""
Encryption Algorithms - Algorithm validation for security system

Single Responsibility: Validate encryption algorithms configuration.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""

from typing import Dict, List, Any
from .base_validator import (
    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class EncryptionAlgorithms(BaseValidator):
    """Validates encryption algorithms configuration."""
    
    def __init__(self):
        """Initialize encryption algorithms validator."""
        super().__init__("EncryptionAlgorithms")
        self.valid_encryption_algorithms = [
            "AES", "RSA", "ChaCha20", "Blowfish", "Twofish", "Serpent"
        ]
        self.valid_key_lengths = [128, 192, 256, 512, 1024, 2048, 4096]
        self.min_key_length = 128
    
    def validate_algorithms(self, algorithms: Any) -> List[ValidationResult]:
        """Validate encryption algorithms configuration."""
        results = []
        
        if not isinstance(algorithms, dict):
            results.append(self._create_result(
                rule_id="algorithms_type",
                rule_name="Algorithms Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Algorithms must be a dictionary"
            ))
            return results
        
        for algo_name, algo_config in algorithms.items():
            if not isinstance(algo_name, str):
                results.append(self._create_result(
                    rule_id="algorithm_name_type",
                    rule_name="Algorithm Name Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Algorithm name must be a string: {algo_name}"
                ))
                continue
            
            if not isinstance(algo_config, dict):
                results.append(self._create_result(
                    rule_id="algorithm_config_type",
                    rule_name="Algorithm Config Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Algorithm config must be a dictionary for algorithm: {algo_name}"
                ))
                continue
            
            # Validate algorithm type
            if "type" in algo_config:
                algo_type = algo_config["type"]
                if algo_type not in self.valid_encryption_algorithms:
                    results.append(self._create_result(
                        rule_id="algorithm_type",
                        rule_name="Algorithm Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid algorithm type: {algo_type}. Valid types: {', '.join(self.valid_encryption_algorithms)}"
                    ))
            
            # Validate key length
            if "key_length" in algo_config:
                key_length = algo_config["key_length"]
                if not isinstance(key_length, int) or key_length < self.min_key_length:
                    results.append(self._create_result(
                        rule_id="algorithm_key_length",
                        rule_name="Algorithm Key Length",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Key length must be at least {self.min_key_length} bits for algorithm: {algo_name}"
                    ))
                elif key_length not in self.valid_key_lengths:
                    results.append(self._create_result(
                        rule_id="algorithm_key_length_valid",
                        rule_name="Algorithm Key Length Valid",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message=f"Key length {key_length} is not a standard length. Consider using: {', '.join(map(str, self.valid_key_lengths))}"
                    ))
            
            # Validate algorithm parameters
            if "parameters" in algo_config:
                params = algo_config["parameters"]
                if not isinstance(params, dict):
                    results.append(self._create_result(
                        rule_id="algorithm_parameters_type",
                        rule_name="Algorithm Parameters Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Algorithm parameters must be a dictionary for algorithm: {algo_name}"
                    ))
        
        return results


def main():
    """CLI interface for Encryption Algorithms testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Encryption Algorithms - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Encryption Algorithms."""
    print("🧪 Running Encryption Algorithms smoke tests...")
    
    # Test creation
    algo_validator = EncryptionAlgorithms()
    assert algo_validator is not None
    print("✅ EncryptionAlgorithms creation test passed")
    
    # Test validation
    test_data = {
        "aes_256": {
            "type": "AES",
            "key_length": 256,
            "parameters": {"mode": "GCM"}
        },
        "rsa_2048": {
            "type": "RSA",
            "key_length": 2048
        }
    }
    results = algo_validator.validate_algorithms(test_data)
    assert len(results) > 0
    print("✅ Algorithm validation test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
