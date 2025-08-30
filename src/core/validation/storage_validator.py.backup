"""
Storage Validator - Unified Validation Framework

This module provides storage validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

from typing import Dict, List, Any, Optional
from .base_validator import (
    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class StorageValidator(BaseValidator):
    """Validates storage configurations and data persistence using unified validation framework"""

    def __init__(self):
        """Initialize storage validator"""
        super().__init__("StorageValidator")
        self.storage_types = [
            "file",
            "database",
            "cache",
            "cloud",
            "memory",
            "network",
            "archive",
        ]
        self.database_types = [
            "sqlite",
            "postgresql",
            "mysql",
            "mongodb",
            "redis",
            "elasticsearch",
            "dynamodb",
        ]

    def validate(
        self, storage_data: Dict[str, Any], **kwargs
    ) -> List[ValidationResult]:
        """Validate storage data and return validation results.

        Returns:
            List[ValidationResult]: Validation results produced during storage
            validation.
        """
        results = []

        try:
            # Validate storage data structure
            structure_results = self._validate_storage_structure(storage_data)
            results.extend(structure_results)

            # Validate required fields
            required_fields = ["type", "name", "configuration"]
            field_results = self._validate_required_fields(
                storage_data, required_fields
            )
            results.extend(field_results)

            # Validate storage type if present
            if "type" in storage_data:
                type_result = self._validate_storage_type(storage_data["type"])
                if type_result:
                    results.append(type_result)

            # Validate configuration if present
            if "configuration" in storage_data:
                config_results = self._validate_storage_configuration(
                    storage_data["configuration"], storage_data.get("type")
                )
                results.extend(config_results)

            # Validate connection settings if present
            if "connection" in storage_data:
                connection_results = self._validate_connection_settings(
                    storage_data["connection"]
                )
                results.extend(connection_results)

            # Validate performance settings if present
            if "performance" in storage_data:
                performance_results = self._validate_performance_settings(
                    storage_data["performance"]
                )
                results.extend(performance_results)

            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_storage_validation",
                    rule_name="Overall Storage Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Storage validation passed successfully",
                    details={"total_checks": len(results)},
                )
                results.append(success_result)

        except Exception as e:
            error_result = self._create_result(
                rule_id="storage_validation_error",
                rule_name="Storage Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Storage validation error: {str(e)}",
                details={"error_type": type(e).__name__},
            )
            results.append(error_result)

        return results

    def _validate_storage_structure(
        self, storage_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate storage data structure and format"""
        results = []

        if not isinstance(storage_data, dict):
            result = self._create_result(
                rule_id="storage_type",
                rule_name="Storage Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Storage data must be a dictionary",
                actual_value=type(storage_data).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        if len(storage_data) == 0:
            result = self._create_result(
                rule_id="storage_empty",
                rule_name="Storage Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="Storage data is empty",
                actual_value=storage_data,
                expected_value="non-empty storage data",
            )
            results.append(result)

        return results

    def _validate_storage_type(self, storage_type: Any) -> Optional[ValidationResult]:
        """Validate storage type value"""
        if not isinstance(storage_type, str):
            return self._create_result(
                rule_id="storage_type_value",
                rule_name="Storage Type Value Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Storage type must be a string",
                field_path="type",
                actual_value=type(storage_type).__name__,
                expected_value="str",
            )

        if storage_type.lower() not in self.storage_types:
            return self._create_result(
                rule_id="storage_type_invalid",
                rule_name="Storage Type Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid storage type: {storage_type}",
                field_path="type",
                actual_value=storage_type,
                expected_value=f"one of {self.storage_types}",
            )

        return None

    def _validate_storage_configuration(
        self, configuration: Any, storage_type: str = None
    ) -> List[ValidationResult]:
        """Validate storage configuration"""
        results = []

        if not isinstance(configuration, dict):
            result = self._create_result(
                rule_id="configuration_type",
                rule_name="Configuration Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Storage configuration must be a dictionary",
                field_path="configuration",
                actual_value=type(configuration).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate based on storage type
        if storage_type == "database":
            db_results = self._validate_database_configuration(configuration)
            results.extend(db_results)
        elif storage_type == "file":
            file_results = self._validate_file_configuration(configuration)
            results.extend(file_results)
        elif storage_type == "cache":
            cache_results = self._validate_cache_configuration(configuration)
            results.extend(cache_results)
        elif storage_type == "cloud":
            cloud_results = self._validate_cloud_configuration(configuration)
            results.extend(cloud_results)

        return results

    def _validate_database_configuration(
        self, configuration: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate database-specific configuration"""
        results = []

        # Validate database type
        if "database_type" in configuration:
            db_type = configuration["database_type"]
            if isinstance(db_type, str):
                if db_type.lower() not in self.database_types:
                    result = self._create_result(
                        rule_id="database_type_invalid",
                        rule_name="Database Type Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid database type: {db_type}",
                        field_path="configuration.database_type",
                        actual_value=db_type,
                        expected_value=f"one of {self.database_types}",
                    )
                    results.append(result)

        # Validate connection string if present
        if "connection_string" in configuration:
            conn_string = configuration["connection_string"]
            if isinstance(conn_string, str):
                if len(conn_string) == 0:
                    result = self._create_result(
                        rule_id="connection_string_empty",
                        rule_name="Connection String Empty Check",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Database connection string cannot be empty",
                        field_path="configuration.connection_string",
                        actual_value=conn_string,
                        expected_value="non-empty connection string",
                    )
                    results.append(result)

        # Validate pool settings if present
        if "pool_settings" in configuration:
            pool_settings = configuration["pool_settings"]
            if isinstance(pool_settings, dict):
                pool_results = self._validate_pool_settings(pool_settings)
                for pool_result in pool_results:
                    pool_result.field_path = (
                        f"configuration.pool_settings.{pool_result.field_path}"
                    )
                results.extend(pool_results)

        return results

    def _validate_file_configuration(
        self, configuration: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate file storage configuration"""
        results = []

        # Validate file path if present
        if "file_path" in configuration:
            file_path = configuration["file_path"]
            if isinstance(file_path, str):
                if len(file_path) == 0:
                    result = self._create_result(
                        rule_id="file_path_empty",
                        rule_name="File Path Empty Check",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="File path cannot be empty",
                        field_path="configuration.file_path",
                        actual_value=file_path,
                        expected_value="non-empty file path",
                    )
                    results.append(result)

        # Validate file format if present
        if "file_format" in configuration:
            file_format = configuration["file_format"]
            valid_formats = ["json", "csv", "xml", "yaml", "pickle", "binary"]

            if isinstance(file_format, str):
                if file_format.lower() not in valid_formats:
                    result = self._create_result(
                        rule_id="file_format_invalid",
                        rule_name="File Format Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid file format: {file_format}",
                        field_path="configuration.file_format",
                        actual_value=file_format,
                        expected_value=f"one of {valid_formats}",
                    )
                    results.append(result)

        return results

    def _validate_cache_configuration(
        self, configuration: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate cache storage configuration"""
        results = []

        # Validate TTL if present
        if "ttl" in configuration:
            ttl = configuration["ttl"]
            if isinstance(ttl, (int, float)):
                if ttl <= 0:
                    result = self._create_result(
                        rule_id="ttl_invalid",
                        rule_name="TTL Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="TTL must be greater than 0",
                        field_path="configuration.ttl",
                        actual_value=ttl,
                        expected_value="> 0",
                    )
                    results.append(result)

        # Validate max size if present
        if "max_size" in configuration:
            max_size = configuration["max_size"]
            if isinstance(max_size, int):
                if max_size <= 0:
                    result = self._create_result(
                        rule_id="max_size_invalid",
                        rule_name="Max Size Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Max size must be greater than 0",
                        field_path="configuration.max_size",
                        actual_value=max_size,
                        expected_value="> 0",
                    )
                    results.append(result)

        return results

    def _validate_cloud_configuration(
        self, configuration: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate cloud storage configuration"""
        results = []

        # Validate provider if present
        if "provider" in configuration:
            provider = configuration["provider"]
            valid_providers = ["aws", "azure", "gcp", "digitalocean", "linode"]

            if isinstance(provider, str):
                if provider.lower() not in valid_providers:
                    result = self._create_result(
                        rule_id="provider_invalid",
                        rule_name="Provider Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid cloud provider: {provider}",
                        field_path="configuration.provider",
                        actual_value=provider,
                        expected_value=f"one of {valid_providers}",
                    )
                    results.append(result)

        # Validate region if present
        if "region" in configuration:
            region = configuration["region"]
            if isinstance(region, str):
                if len(region) == 0:
                    result = self._create_result(
                        rule_id="region_empty",
                        rule_name="Region Empty Check",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Cloud region cannot be empty",
                        field_path="configuration.region",
                        actual_value=region,
                        expected_value="non-empty region",
                    )
                    results.append(result)

        return results

    def _validate_pool_settings(
        self, pool_settings: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate database connection pool settings"""
        results = []

        # Validate min connections
        if "min_connections" in pool_settings:
            min_conn = pool_settings["min_connections"]
            if isinstance(min_conn, int):
                if min_conn < 0:
                    result = self._create_result(
                        rule_id="min_connections_invalid",
                        rule_name="Min Connections Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Min connections cannot be negative",
                        field_path="min_connections",
                        actual_value=min_conn,
                        expected_value=">= 0",
                    )
                    results.append(result)

        # Validate max connections
        if "max_connections" in pool_settings:
            max_conn = pool_settings["max_connections"]
            if isinstance(max_conn, int):
                if max_conn <= 0:
                    result = self._create_result(
                        rule_id="max_connections_invalid",
                        rule_name="Max Connections Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Max connections must be greater than 0",
                        field_path="max_connections",
                        actual_value=max_conn,
                        expected_value="> 0",
                    )
                    results.append(result)

                # Check if max > min
                min_conn = pool_settings.get("min_connections", 0)
                if isinstance(min_conn, int) and max_conn < min_conn:
                    result = self._create_result(
                        rule_id="connection_pool_invalid",
                        rule_name="Connection Pool Invalid Range",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Max connections must be >= min connections",
                        field_path="max_connections",
                        actual_value=f"{max_conn} < {min_conn}",
                        expected_value="max_connections >= min_connections",
                    )
                    results.append(result)

        return results

    def _validate_connection_settings(self, connection: Any) -> List[ValidationResult]:
        """Validate connection settings"""
        results = []

        if not isinstance(connection, dict):
            result = self._create_result(
                rule_id="connection_type",
                rule_name="Connection Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Connection settings must be a dictionary",
                field_path="connection",
                actual_value=type(connection).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate timeout if present
        if "timeout" in connection:
            timeout = connection["timeout"]
            if isinstance(timeout, (int, float)):
                if timeout <= 0:
                    result = self._create_result(
                        rule_id="timeout_invalid",
                        rule_name="Timeout Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Connection timeout must be greater than 0",
                        field_path="connection.timeout",
                        actual_value=timeout,
                        expected_value="> 0",
                    )
                    results.append(result)

        # Validate retry settings if present
        if "retry_attempts" in connection:
            retry_attempts = connection["retry_attempts"]
            if isinstance(retry_attempts, int):
                if retry_attempts < 0:
                    result = self._create_result(
                        rule_id="retry_attempts_invalid",
                        rule_name="Retry Attempts Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Retry attempts cannot be negative",
                        field_path="connection.retry_attempts",
                        actual_value=retry_attempts,
                        expected_value=">= 0",
                    )
                    results.append(result)

        return results

    def _validate_performance_settings(
        self, performance: Any
    ) -> List[ValidationResult]:
        """Validate performance settings"""
        results = []

        if not isinstance(performance, dict):
            result = self._create_result(
                rule_id="performance_type",
                rule_name="Performance Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Performance settings must be a dictionary",
                field_path="performance",
                actual_value=type(performance).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate batch size if present
        if "batch_size" in performance:
            batch_size = performance["batch_size"]
            if isinstance(batch_size, int):
                if batch_size <= 0:
                    result = self._create_result(
                        rule_id="batch_size_invalid",
                        rule_name="Batch Size Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Batch size must be greater than 0",
                        field_path="performance.batch_size",
                        actual_value=batch_size,
                        expected_value="> 0",
                    )
                    results.append(result)

        # Validate compression if present
        if "compression" in performance:
            compression = performance["compression"]
            valid_compression = ["none", "gzip", "lz4", "zstd", "snappy"]

            if isinstance(compression, str):
                if compression.lower() not in valid_compression:
                    result = self._create_result(
                        rule_id="compression_invalid",
                        rule_name="Compression Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid compression type: {compression}",
                        field_path="performance.compression",
                        actual_value=compression,
                        expected_value=f"one of {valid_compression}",
                    )
                    results.append(result)

        return results

    def add_storage_type(self, storage_type: str) -> bool:
        """Add a custom storage type"""
        try:
            if storage_type not in self.storage_types:
                self.storage_types.append(storage_type)
                self.logger.info(f"Storage type added: {storage_type}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add storage type: {e}")
            return False

    def add_database_type(self, database_type: str) -> bool:
        """Add a custom database type"""
        try:
            if database_type not in self.database_types:
                self.database_types.append(database_type)
                self.logger.info(f"Database type added: {database_type}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add database type: {e}")
            return False

    def validate_data_integrity(self, data: Any, checksum: str) -> ValidationResult:
        """Validate data integrity using checksum (from PersistentStorageValidator)"""
        try:
            import hashlib
            import json

            # Calculate checksum
            data_str = json.dumps(data, sort_keys=True)
            calculated_checksum = hashlib.sha256(data_str.encode()).hexdigest()

            # Compare checksums
            if calculated_checksum == checksum:
                return ValidationResult(
                    rule_id="data_integrity",
                    rule_name="Data Integrity Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Data integrity validation passed",
                    details={
                        "calculated_checksum": calculated_checksum,
                        "provided_checksum": checksum,
                        "match": True,
                    },
                )
            else:
                return ValidationResult(
                    rule_id="data_integrity",
                    rule_name="Data Integrity Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Data integrity validation failed - checksum mismatch",
                    details={
                        "calculated_checksum": calculated_checksum,
                        "provided_checksum": checksum,
                        "match": False,
                    },
                )

        except Exception as e:
            return ValidationResult(
                rule_id="data_integrity",
                rule_name="Data Integrity Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Data integrity validation error: {str(e)}",
                details={"error": str(e)},
            )

    def calculate_checksum(self, data: Any) -> str:
        """Calculate checksum for data (from PersistentStorageValidator)"""
        try:

            data_str = json.dumps(data, sort_keys=True)
            return hashlib.sha256(data_str.encode()).hexdigest()

        except Exception as e:
            self.logger.error(f"Failed to calculate checksum: {e}")
            return ""
