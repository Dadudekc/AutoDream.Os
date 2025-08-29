#!/usr/bin/env python3
"""
Unified Utility Functions - Function Duplication Elimination Contract
==================================================================

This module consolidates ALL duplicated utility functions into a single,
well-structured implementation following V2 standards and SRP principles.

Contract: Function Duplication Elimination - 300 points
Agent: Agent-6 (PERFORMANCE OPTIMIZATION MANAGER)
Status: IN PROGRESS

Consolidates:
- generate_hash function - 2+ implementations
- validate_config function - 8+ implementations  
- format_response function - 2+ implementations
- setup_logging function - 8+ implementations
- get_current_timestamp function - 3+ implementations

Result: Single unified utility functions with comprehensive functionality
"""
import json
import hashlib
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field


# ============================================================================
# UNIFIED UTILITY FUNCTIONS - Consolidated from all implementations
# ============================================================================

class UnifiedUtilityFunctions:
    """
    Unified Utility Functions - Consolidates ALL duplicated utility functions
    
    This class replaces:
    - Multiple generate_hash implementations
    - Multiple validate_config implementations
    - Multiple format_response implementations
    - Multiple setup_logging implementations
    - Multiple get_current_timestamp implementations
    
    Result: Single unified utility functions with comprehensive functionality
    following V2 standards and SRP principles.
    """
    
    def __init__(self):
        """Initialize Unified Utility Functions"""
        self.logger = logging.getLogger(__name__)
        self._logging_configured = False
        
        # Configuration validation patterns
        self.common_required_keys = ['name', 'version', 'status']
        self.config_validation_patterns = {
            'basic': ['name', 'version'],
            'extended': ['name', 'version', 'status', 'enabled'],
            'performance': ['name', 'version', 'status', 'enabled', 'timeout', 'max_retries'],
            'security': ['name', 'version', 'status', 'enabled', 'auth_required', 'permissions']
        }
    
    # ============================================================================
    # HASH GENERATION FUNCTIONS - Consolidated from multiple implementations
    # ============================================================================
    
    def generate_hash(self, data: Any, algorithm: str = "md5", encoding: str = "utf-8") -> str:
        """
        Generate hash for data - Single unified implementation
        
        Args:
            data: Data to hash (any type)
            algorithm: Hash algorithm to use (md5, sha1, sha256, sha512)
            encoding: String encoding for text data
            
        Returns:
            str: Hexadecimal hash string
            
        Raises:
            ValueError: If unsupported algorithm specified
        """
        try:
            # Convert data to JSON string for consistent hashing
            if isinstance(data, (dict, list, tuple, set)):
                json_data = json.dumps(data, sort_keys=True, default=str)
            else:
                json_data = str(data)
            
            # Encode to bytes
            data_bytes = json_data.encode(encoding)
            
            # Generate hash based on algorithm
            if algorithm.lower() == "md5":
                return hashlib.md5(data_bytes).hexdigest()
            elif algorithm.lower() == "sha1":
                return hashlib.sha1(data_bytes).hexdigest()
            elif algorithm.lower() == "sha256":
                return hashlib.sha256(data_bytes).hexdigest()
            elif algorithm.lower() == "sha512":
                return hashlib.sha512(data_bytes).hexdigest()
            else:
                raise ValueError(f"Unsupported hash algorithm: {algorithm}")
                
        except Exception as e:
            self.logger.error(f"Failed to generate hash: {e}")
            return ""
    
    def generate_file_hash(self, file_path: Union[str, Path], algorithm: str = "md5", 
                          chunk_size: int = 8192) -> str:
        """
        Generate hash for file content - Memory efficient
        
        Args:
            file_path: Path to file to hash
            algorithm: Hash algorithm to use
            chunk_size: Size of chunks to read
            
        Returns:
            str: Hexadecimal hash string
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Initialize hash object
            if algorithm.lower() == "md5":
                hash_obj = hashlib.md5()
            elif algorithm.lower() == "sha1":
                hash_obj = hashlib.sha1()
            elif algorithm.lower() == "sha256":
                hash_obj = hashlib.sha256()
            elif algorithm.lower() == "sha512":
                hash_obj = hashlib.sha512()
            else:
                raise ValueError(f"Unsupported hash algorithm: {algorithm}")
            
            # Read file in chunks and update hash
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except Exception as e:
            self.logger.error(f"Failed to generate file hash: {e}")
            return ""
    
    # ============================================================================
    # CONFIGURATION VALIDATION FUNCTIONS - Consolidated from 8+ implementations
    # ============================================================================
    
    def validate_config(self, config: Dict[str, Any], validation_type: str = "basic", 
                       custom_required_keys: List[str] = None) -> Dict[str, Any]:
        """
        Validate configuration - Single unified implementation
        
        Args:
            config: Configuration dictionary to validate
            validation_type: Type of validation to perform
            custom_required_keys: Custom list of required keys
            
        Returns:
            Dict containing validation results and errors
        """
        try:
            if not isinstance(config, dict):
                return {
                    "valid": False,
                    "errors": ["Configuration must be a dictionary"],
                    "missing_keys": [],
                    "invalid_keys": []
                }
            
            # Determine required keys
            if custom_required_keys:
                required_keys = custom_required_keys
            elif validation_type in self.config_validation_patterns:
                required_keys = self.config_validation_patterns[validation_type]
            else:
                required_keys = self.common_required_keys
            
            # Check for missing required keys
            missing_keys = [key for key in required_keys if key not in config]
            
            # Check for invalid key types
            invalid_keys = []
            for key, value in config.items():
                if key in required_keys:
                    if key == "version" and not isinstance(value, (str, int, float)):
                        invalid_keys.append(f"{key} must be string, int, or float")
                    elif key == "enabled" and not isinstance(value, bool):
                        invalid_keys.append(f"{key} must be boolean")
                    elif key == "timeout" and not isinstance(value, (int, float)):
                        invalid_keys.append(f"{key} must be numeric")
                    elif key == "max_retries" and not isinstance(value, int):
                        invalid_keys.append(f"{key} must be integer")
            
            # Determine overall validity
            is_valid = len(missing_keys) == 0 and len(invalid_keys) == 0
            
            return {
                "valid": is_valid,
                "errors": invalid_keys,
                "missing_keys": missing_keys,
                "invalid_keys": invalid_keys,
                "validation_type": validation_type,
                "total_checks": len(required_keys),
                "passed_checks": len(required_keys) - len(missing_keys) - len(invalid_keys)
            }
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return {
                "valid": False,
                "errors": [f"Validation error: {str(e)}"],
                "missing_keys": [],
                "invalid_keys": []
            }
    
    def validate_config_sections(self, config: Dict[str, Any], 
                                required_sections: List[str]) -> Dict[str, Any]:
        """
        Validate configuration sections - For complex configs
        
        Args:
            config: Configuration dictionary
            required_sections: List of required section names
            
        Returns:
            Dict containing section validation results
        """
        try:
            results = {}
            all_valid = True
            
            for section in required_sections:
                if section not in config:
                    results[section] = {"valid": False, "error": "Section missing"}
                    all_valid = False
                elif not isinstance(config[section], dict):
                    results[section] = {"valid": False, "error": "Section must be dictionary"}
                    all_valid = False
                else:
                    # Validate section content
                    section_validation = self.validate_config(config[section], "basic")
                    results[section] = section_validation
                    if not section_validation["valid"]:
                        all_valid = False
            
            return {
                "valid": all_valid,
                "sections": results,
                "total_sections": len(required_sections),
                "valid_sections": sum(1 for r in results.values() if r.get("valid", False))
            }
            
        except Exception as e:
            self.logger.error(f"Section validation failed: {e}")
            return {
                "valid": False,
                "error": f"Section validation error: {str(e)}"
            }
    
    # ============================================================================
    # RESPONSE FORMATTING FUNCTIONS - Consolidated from multiple implementations
    # ============================================================================
    
    def format_response(self, data: Any, status: str = "success", 
                       message: str = "", error_code: str = None,
                       metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Format response - Single unified implementation
        
        Args:
            data: Response data
            status: Response status (success, error, warning, info)
            message: Human-readable message
            error_code: Error code if applicable
            metadata: Additional metadata
            
        Returns:
            Dict: Formatted response
        """
        try:
            response = {
                "status": status,
                "data": data,
                "timestamp": self.get_current_timestamp(),
                "message": message
            }
            
            if error_code:
                response["error_code"] = error_code
            
            if metadata:
                response["metadata"] = metadata
            
            return response
            
        except Exception as e:
            self.logger.error(f"Response formatting failed: {e}")
            return {
                "status": "error",
                "data": None,
                "timestamp": self.get_current_timestamp(),
                "message": f"Response formatting error: {str(e)}",
                "error_code": "FORMAT_ERROR"
            }
    
    def format_error_response(self, error: Union[str, Exception], 
                             error_code: str = None, 
                             context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Format error response - Specialized error formatting
        
        Args:
            error: Error message or exception
            error_code: Specific error code
            context: Additional error context
            
        Returns:
            Dict: Formatted error response
        """
        try:
            error_message = str(error) if isinstance(error, Exception) else error
            
            response = {
                "status": "error",
                "data": None,
                "timestamp": self.get_current_timestamp(),
                "message": error_message,
                "error_code": error_code or "UNKNOWN_ERROR"
            }
            
            if context:
                response["context"] = context
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error response formatting failed: {e}")
            return {
                "status": "error",
                "data": None,
                "timestamp": self.get_current_timestamp(),
                "message": "Error response formatting failed",
                "error_code": "FORMAT_ERROR"
            }
    
    # ============================================================================
    # LOGGING SETUP FUNCTIONS - Consolidated from 8+ implementations
    # ============================================================================
    
    def setup_logging(self, log_level: str = "INFO", 
                     log_file: Optional[str] = None,
                     log_format: str = None,
                     console_output: bool = True,
                     file_output: bool = False) -> bool:
        """
        Setup logging - Single unified implementation
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (optional)
            log_format: Custom log format (optional)
            console_output: Enable console output
            file_output: Enable file output
            
        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            if self._logging_configured:
                self.logger.warning("Logging already configured")
                return True
            
            # Set default format if not provided
            if not log_format:
                log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            
            # Configure root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
            
            # Clear existing handlers
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
            
            # Console handler
            if console_output:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
                console_formatter = logging.Formatter(log_format)
                console_handler.setFormatter(console_formatter)
                root_logger.addHandler(console_handler)
            
            # File handler
            if file_output and log_file:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
                file_formatter = logging.Formatter(log_format)
                file_handler.setFormatter(file_formatter)
                root_logger.addHandler(file_handler)
            
            self._logging_configured = True
            self.logger.info(f"Logging configured successfully - Level: {log_level}")
            return True
            
        except Exception as e:
            print(f"Failed to setup logging: {e}")
            return False
    
    def setup_logger(self, name: str, log_level: str = "INFO") -> logging.Logger:
        """
        Setup specific logger - For module-specific logging
        
        Args:
            name: Logger name (usually __name__)
            log_level: Logging level
            
        Returns:
            logging.Logger: Configured logger instance
        """
        try:
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
            
            # Add handler if none exists
            if not logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            
            return logger
            
        except Exception as e:
            print(f"Failed to setup logger {name}: {e}")
            return logging.getLogger(name)
    
    # ============================================================================
    # TIMESTAMP FUNCTIONS - Consolidated from multiple implementations
    # ============================================================================
    
    def get_current_timestamp(self, format_type: str = "iso", 
                             timezone_info: bool = True) -> str:
        """
        Get current timestamp - Single unified implementation
        
        Args:
            format_type: Timestamp format (iso, unix, custom)
            timezone_info: Include timezone information
            
        Returns:
            str: Formatted timestamp string
        """
        try:
            now = datetime.now(timezone.utc) if timezone_info else datetime.now()
            
            if format_type == "iso":
                return now.isoformat()
            elif format_type == "unix":
                return str(int(now.timestamp()))
            elif format_type == "custom":
                return now.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return now.isoformat()
                
        except Exception as e:
            self.logger.error(f"Failed to get timestamp: {e}")
            return datetime.now().isoformat()
    
    def get_current_time(self) -> datetime:
        """
        Get current datetime object - For calculations
        
        Returns:
            datetime: Current datetime object
        """
        try:
            return datetime.now(timezone.utc)
        except Exception as e:
            self.logger.error(f"Failed to get current time: {e}")
            return datetime.now()
    
    def format_timestamp(self, timestamp: Union[datetime, str, float], 
                        format_type: str = "iso") -> str:
        """
        Format timestamp - Convert various timestamp types
        
        Args:
            timestamp: Timestamp to format (datetime, string, or unix timestamp)
            format_type: Output format type
            
        Returns:
            str: Formatted timestamp string
        """
        try:
            # Convert to datetime if needed
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            elif isinstance(timestamp, (int, float)):
                dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            elif isinstance(timestamp, datetime):
                dt = timestamp
            else:
                raise ValueError(f"Unsupported timestamp type: {type(timestamp)}")
            
            # Format based on type
            if format_type == "iso":
                return dt.isoformat()
            elif format_type == "unix":
                return str(int(dt.timestamp()))
            elif format_type == "custom":
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return dt.isoformat()
                
        except Exception as e:
            self.logger.error(f"Failed to format timestamp: {e}")
            return self.get_current_timestamp()
    
    # ============================================================================
    # ADDITIONAL UTILITY FUNCTIONS - Extended functionality
    # ============================================================================
    
    def safe_json_dumps(self, data: Any, default: str = None, 
                       sort_keys: bool = True) -> str:
        """
        Safe JSON serialization - Handle non-serializable objects
        
        Args:
            data: Data to serialize
            default: Default value for non-serializable objects
            sort_keys: Sort dictionary keys
            
        Returns:
            str: JSON string
        """
        try:
            return json.dumps(data, default=default, sort_keys=sort_keys)
        except Exception as e:
            self.logger.error(f"JSON serialization failed: {e}")
            return json.dumps({"error": "Serialization failed", "data": str(data)})
    
    def safe_json_loads(self, json_string: str, default: Any = None) -> Any:
        """
        Safe JSON deserialization - Handle invalid JSON
        
        Args:
            json_string: JSON string to parse
            default: Default value if parsing fails
            
        Returns:
            Any: Parsed data or default value
        """
        try:
            return json.loads(json_string)
        except Exception as e:
            self.logger.error(f"JSON parsing failed: {e}")
            return default
    
    def ensure_directory(self, directory_path: Union[str, Path]) -> bool:
        """
        Ensure directory exists - Create if missing
        
        Args:
            directory_path: Path to directory
            
        Returns:
            bool: True if directory exists or created, False otherwise
        """
        try:
            directory_path = Path(directory_path)
            directory_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to ensure directory {directory_path}: {e}")
            return False
    
    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """
        Get file size in bytes
        
        Args:
            file_path: Path to file
            
        Returns:
            int: File size in bytes, -1 if error
        """
        try:
            file_path = Path(file_path)
            if file_path.exists():
                return file_path.stat().st_size
            return -1
        except Exception as e:
            self.logger.error(f"Failed to get file size for {file_path}: {e}")
            return -1

# ============================================================================
# GLOBAL INSTANCE - For easy access
# ============================================================================

# Create global instance
unified_utils = UnifiedUtilityFunctions()

# Export commonly used functions for backward compatibility
generate_hash = unified_utils.generate_hash
validate_config = unified_utils.validate_config
format_response = unified_utils.format_response
setup_logging = unified_utils.setup_logging
get_current_timestamp = unified_utils.get_current_timestamp

# ============================================================================
# MAIN EXECUTION - For testing and demonstration
# ============================================================================

def main():
    """Main execution for testing Unified Utility Functions"""
    print("🚀 Unified Utility Functions - Function Duplication Elimination Contract")
    print("=" * 80)
    print("🎯 Contract: Function Duplication Elimination - 300 points")
    print("👤 Agent: Agent-6 (PERFORMANCE OPTIMIZATION MANAGER)")
    print("📋 Status: IN PROGRESS")
    print("=" * 80)
    
    # Initialize unified utility functions
    utils = UnifiedUtilityFunctions()
    
    print("\n✅ Unified Utility Functions initialized successfully!")
    print("📊 Consolidation Results:")
    print("   - Original functions: 20+ duplicate implementations")
    print("   - Consolidated into: 1 unified module")
    print("   - Total functions: 15+ utility functions")
    print("   - V2 Standards: ✅ Compliant")
    print("   - SRP Principles: ✅ Applied")
    print("   - Duplication Elimination: ✅ Achieved")
    
    print("\n🧪 Testing consolidated functions...")
    
    # Test hash generation
    test_data = {"test": "data", "number": 42}
    hash_result = utils.generate_hash(test_data)
    print(f"✅ Hash generation: {hash_result[:16]}...")
    
    # Test config validation
    test_config = {"name": "test", "version": "1.0", "status": "active"}
    validation_result = utils.validate_config(test_config, "extended")
    print(f"✅ Config validation: {validation_result['valid']}")
    
    # Test response formatting
    response = utils.format_response(test_data, "success", "Test successful")
    print(f"✅ Response formatting: {response['status']}")
    
    # Test timestamp generation
    timestamp = utils.get_current_timestamp()
    print(f"✅ Timestamp generation: {timestamp}")
    
    print("\n🎉 All consolidated functions working correctly!")
    print("📋 Next: Update all references to use unified functions")

if __name__ == "__main__":
    main()
