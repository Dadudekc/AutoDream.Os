from datetime import datetime
from typing import Dict, List, Any, Optional
import re

    import argparse
from .base_validator import (

#!/usr/bin/env python3
"""
Security Encryption - Encryption validation for security system

Single Responsibility: Validate encryption methods and configurations.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""


    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class SecurityEncryption(BaseValidator):
    """Validates encryption methods and configurations."""
    
    def __init__(self):
        """Initialize encryption validator."""
        super().__init__("SecurityEncryption")
        self.valid_encryption_algorithms = [
            "AES", "RSA", "ChaCha20", "Blowfish", "Twofish", "Serpent"
        ]
        self.valid_hash_algorithms = [
            "SHA-256", "SHA-512", "Blake2b", "Argon2", "bcrypt", "scrypt"
        ]
        self.valid_key_lengths = [128, 192, 256, 512, 1024, 2048, 4096]
        self.min_key_length = 128
    
    def validate_encryption(self, encryption_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate encryption configuration."""
        results = []
        
        try:
            # Validate encryption algorithms
            if "algorithms" in encryption_data:
                algo_results = self._validate_algorithms(encryption_data["algorithms"])
                results.extend(algo_results)
            
            # Validate key management
            if "key_management" in encryption_data:
                key_results = self._validate_key_management(encryption_data["key_management"])
                results.extend(key_results)
            
            # Validate hash functions
            if "hash_functions" in encryption_data:
                hash_results = self._validate_hash_functions(encryption_data["hash_functions"])
                results.extend(hash_results)
            
            # Validate encryption modes
            if "encryption_modes" in encryption_data:
                mode_results = self._validate_encryption_modes(encryption_data["encryption_modes"])
                results.extend(mode_results)
            
            # Validate certificate configuration
            if "certificates" in encryption_data:
                cert_results = self._validate_certificates(encryption_data["certificates"])
                results.extend(cert_results)
            
        except Exception as e:
            error_result = self._create_result(
                rule_id="encryption_validation_error",
                rule_name="Encryption Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Encryption validation failed: {str(e)}"
            )
            results.append(error_result)
        
        return results
    
    def _validate_algorithms(self, algorithms: Any) -> List[ValidationResult]:
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
    
    def _validate_key_management(self, key_mgmt: Any) -> List[ValidationResult]:
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
            key_gen = key_mgmt["key_generation"]
            if not isinstance(key_gen, dict):
                results.append(self._create_result(
                    rule_id="key_generation_type",
                    rule_name="Key Generation Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Key generation must be a dictionary"
                ))
            else:
                # Validate key source
                if "source" in key_gen:
                    source = key_gen["source"]
                    valid_sources = ["random", "hardware", "derived"]
                    if source not in valid_sources:
                        results.append(self._create_result(
                            rule_id="key_generation_source",
                            rule_name="Key Generation Source",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Invalid key generation source: {source}. Valid sources: {', '.join(valid_sources)}"
                        ))
        
        # Validate key storage
        if "key_storage" in key_mgmt:
            key_storage = key_mgmt["key_storage"]
            if not isinstance(key_storage, dict):
                results.append(self._create_result(
                    rule_id="key_storage_type",
                    rule_name="Key Storage Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Key storage must be a dictionary"
                ))
            else:
                # Validate storage type
                if "type" in key_storage:
                    storage_type = key_storage["type"]
                    valid_storage_types = ["memory", "file", "database", "hardware", "cloud"]
                    if storage_type not in valid_storage_types:
                        results.append(self._create_result(
                            rule_id="key_storage_type_value",
                            rule_name="Key Storage Type Value",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Invalid key storage type: {storage_type}. Valid types: {', '.join(valid_storage_types)}"
                        ))
        
        # Validate key rotation
        if "key_rotation" in key_mgmt:
            key_rotation = key_mgmt["key_rotation"]
            if not isinstance(key_rotation, dict):
                results.append(self._create_result(
                    rule_id="key_rotation_type",
                    rule_name="Key Rotation Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Key rotation must be a dictionary"
                ))
            else:
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
                    elif interval > 365:  # More than 1 year
                        results.append(self._create_result(
                            rule_id="key_rotation_interval_long",
                            rule_name="Key Rotation Interval Long",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.WARNING,
                            message="Key rotation interval is very long, consider reducing for security"
                        ))
        
        return results
    
    def _validate_hash_functions(self, hash_funcs: Any) -> List[ValidationResult]:
        """Validate hash functions configuration."""
        results = []
        
        if not isinstance(hash_funcs, dict):
            results.append(self._create_result(
                rule_id="hash_functions_type",
                rule_name="Hash Functions Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Hash functions must be a dictionary"
            ))
            return results
        
        for func_name, func_config in hash_funcs.items():
            if not isinstance(func_name, str):
                results.append(self._create_result(
                    rule_id="hash_function_name_type",
                    rule_name="Hash Function Name Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Hash function name must be a string: {func_name}"
                ))
                continue
            
            if not isinstance(func_config, dict):
                results.append(self._create_result(
                    rule_id="hash_function_config_type",
                    rule_name="Hash Function Config Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Hash function config must be a dictionary for function: {func_name}"
                ))
                continue
            
            # Validate hash algorithm
            if "algorithm" in func_config:
                algorithm = func_config["algorithm"]
                if algorithm not in self.valid_hash_algorithms:
                    results.append(self._create_result(
                        rule_id="hash_function_algorithm",
                        rule_name="Hash Function Algorithm",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid hash algorithm: {algorithm}. Valid algorithms: {', '.join(self.valid_hash_algorithms)}"
                    ))
            
            # Validate salt configuration
            if "salt_enabled" in func_config:
                salt_enabled = func_config["salt_enabled"]
                if not isinstance(salt_enabled, bool):
                    results.append(self._create_result(
                        rule_id="hash_function_salt_type",
                        rule_name="Hash Function Salt Type",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Salt enabled must be a boolean for function: {func_name}"
                    ))
                elif not salt_enabled:
                    results.append(self._create_result(
                        rule_id="hash_function_salt_disabled",
                        rule_name="Hash Function Salt Disabled",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message=f"Salt should be enabled for hash function: {func_name}"
                    ))
        
        return results
    
    def _validate_encryption_modes(self, modes: Any) -> List[ValidationResult]:
        """Validate encryption modes configuration."""
        results = []
        
        if not isinstance(modes, list):
            results.append(self._create_result(
                rule_id="encryption_modes_type",
                rule_name="Encryption Modes Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Encryption modes must be a list"
            ))
            return results
        
        valid_modes = ["CBC", "GCM", "CTR", "OFB", "CFB", "ECB"]
        
        for i, mode in enumerate(modes):
            if not isinstance(mode, str):
                results.append(self._create_result(
                    rule_id="encryption_mode_item_type",
                    rule_name="Encryption Mode Item Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Encryption mode item {i} must be a string"
                ))
                continue
            
            if mode not in valid_modes:
                results.append(self._create_result(
                    rule_id="encryption_mode_value",
                    rule_name="Encryption Mode Value",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid encryption mode: {mode}. Valid modes: {', '.join(valid_modes)}"
                ))
            
            # Warn about ECB mode (less secure)
            if mode == "ECB":
                results.append(self._create_result(
                    rule_id="encryption_mode_ecb",
                    rule_name="Encryption Mode ECB",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message="ECB mode is less secure, consider using GCM or CBC mode"
                ))
        
        return results
    
    def _validate_certificates(self, certificates: Any) -> List[ValidationResult]:
        """Validate certificate configuration."""
        results = []
        
        if not isinstance(certificates, dict):
            results.append(self._create_result(
                rule_id="certificates_type",
                rule_name="Certificates Type",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Certificates must be a dictionary"
            ))
            return results
        
        # Validate certificate authority
        if "ca" in certificates:
            ca = certificates["ca"]
            if not isinstance(ca, dict):
                results.append(self._create_result(
                    rule_id="certificate_ca_type",
                    rule_name="Certificate CA Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Certificate authority must be a dictionary"
                ))
            else:
                # Validate CA certificate path
                if "cert_path" in ca:
                    cert_path = ca["cert_path"]
                    if not isinstance(cert_path, str) or not cert_path:
                        results.append(self._create_result(
                            rule_id="certificate_ca_path",
                            rule_name="Certificate CA Path",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message="CA certificate path must be a non-empty string"
                        ))
        
        # Validate certificate validation
        if "validation" in certificates:
            validation = certificates["validation"]
            if not isinstance(validation, dict):
                results.append(self._create_result(
                    rule_id="certificate_validation_type",
                    rule_name="Certificate Validation Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Certificate validation must be a dictionary"
                ))
            else:
                # Validate CRL checking
                if "crl_checking" in validation:
                    crl_checking = validation["crl_checking"]
                    if not isinstance(crl_checking, bool):
                        results.append(self._create_result(
                            rule_id="certificate_crl_type",
                            rule_name="Certificate CRL Type",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message="CRL checking must be a boolean"
                        ))
                    elif not crl_checking:
                        results.append(self._create_result(
                            rule_id="certificate_crl_disabled",
                            rule_name="Certificate CRL Disabled",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.WARNING,
                            message="CRL checking should be enabled for security"
                        ))
        
        return results
    
    def get_encryption_summary(self, encryption_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get encryption validation summary."""
        try:
            results = self.validate_encryption(encryption_data)
            
            return {
                "total_validations": len(results),
                "passed": len([r for r in results if r.status.value == "passed"]),
                "failed": len([r for r in results if r.status.value == "failed"]),
                "warnings": len([r for r in results if r.severity.value == "warning"]),
                "errors": len([r for r in results if r.severity.value == "error"]),
                "timestamp": self._get_current_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get encryption summary: {e}")
            return {"error": str(e)}
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()


def main():
    """CLI interface for Security Encryption testing."""
    
    parser = argparse.ArgumentParser(description="Security Encryption - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for Security Encryption."""
    print("🧪 Running Security Encryption smoke tests...")
    
    # Test creation
    encryption_validator = SecurityEncryption()
    assert encryption_validator is not None
    print("✅ SecurityEncryption creation test passed")
    
    # Test validation
    test_data = {
        "algorithms": {
            "aes_256": {
                "type": "AES",
                "key_length": 256,
                "parameters": {"mode": "GCM"}
            }
        },
        "key_management": {
            "key_generation": {"source": "random"},
            "key_storage": {"type": "hardware"},
            "key_rotation": {"interval": 90}
        },
        "hash_functions": {
            "password_hash": {
                "algorithm": "bcrypt",
                "salt_enabled": True
            }
        },
        "encryption_modes": ["GCM", "CBC"],
        "certificates": {
            "ca": {"cert_path": "/path/to/ca.crt"},
            "validation": {"crl_checking": True}
        }
    }
    results = encryption_validator.validate_encryption(test_data)
    assert len(results) > 0
    print("✅ Encryption validation test passed")
    
    # Test summary
    summary = encryption_validator.get_encryption_summary(test_data)
    assert isinstance(summary, dict)
    print("✅ Summary test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
