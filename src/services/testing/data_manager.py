"""
Test Data Management
===================

Unified test data management for V2 services.
Consolidates test data management from all massive files.
Target: ≤300 LOC for V2 standards compliance.
"""

import os
import sys
import json
import time
import logging
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable, Coroutine, Type
from pathlib import Path
from datetime import datetime, timedelta
import traceback
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataType(Enum):
    """Test data types."""
    TEST_CONFIG = "test_config"
    TEST_RESULTS = "test_results"
    PERFORMANCE_METRICS = "performance_metrics"
    MESSAGE_HISTORY = "message_history"
    AGENT_REGISTRY = "agent_registry"
    EXECUTION_LOGS = "execution_logs"


class StorageFormat(Enum):
    """Data storage formats."""
    JSON = "json"
    CSV = "csv"
    XML = "xml"
    BINARY = "binary"


@dataclass
class DataMetadata:
    """Metadata for test data."""
    data_id: str
    data_type: DataType
    created_at: float
    updated_at: float
    size_bytes: int
    record_count: int
    checksum: str
    version: str = "1.0"
    tags: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class DataStorageConfig:
    """Configuration for data storage."""
    base_directory: str = "test_data"
    enable_compression: bool = True
    enable_encryption: bool = False
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    retention_days: int = 30
    backup_enabled: bool = True
    backup_interval_hours: int = 24


class DataPersistence:
    """Handles data persistence operations."""
    
    def __init__(self, config: DataStorageConfig):
        self.config = config
        self.base_path = Path(config.base_directory)
        self._ensure_base_directory()
        self._lock = threading.Lock()
    
    def _ensure_base_directory(self):
        """Ensure base directory exists."""
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Data directory ensured: {self.base_path}")
        except Exception as e:
            logger.error(f"Failed to create data directory: {e}")
    
    def save_data(self, data: Any, data_type: DataType, identifier: str) -> bool:
        """Save data to storage."""
        try:
            with self._lock:
                # Create type-specific directory
                type_dir = self.base_path / data_type.value
                type_dir.mkdir(parents=True, exist_ok=True)
                
                # Create file path
                file_path = type_dir / f"{identifier}.json"
                
                # Prepare data for storage
                storage_data = {
                    "metadata": self._create_metadata(data, data_type, identifier),
                    "data": data
                }
                
                # Save to file
                with open(file_path, 'w') as f:
                    json.dump(storage_data, f, default=str, indent=2)
                
                logger.info(f"Data saved: {file_path}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            return False
    
    def load_data(self, data_type: DataType, identifier: str) -> Optional[Any]:
        """Load data from storage."""
        try:
            with self._lock:
                file_path = self.base_path / data_type.value / f"{identifier}.json"
                
                if not file_path.exists():
                    logger.warning(f"Data file not found: {file_path}")
                    return None
                
                with open(file_path, 'r') as f:
                    storage_data = json.load(f)
                
                logger.info(f"Data loaded: {file_path}")
                return storage_data.get("data")
                
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return None
    
    def delete_data(self, data_type: DataType, identifier: str) -> bool:
        """Delete data from storage."""
        try:
            with self._lock:
                file_path = self.base_path / data_type.value / f"{identifier}.json"
                
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"Data deleted: {file_path}")
                    return True
                else:
                    logger.warning(f"Data file not found: {file_path}")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to delete data: {e}")
            return False
    
    def list_data(self, data_type: DataType) -> List[str]:
        """List available data identifiers for a type."""
        try:
            with self._lock:
                type_dir = self.base_path / data_type.value
                
                if not type_dir.exists():
                    return []
                
                files = [f.stem for f in type_dir.glob("*.json")]
                return files
                
        except Exception as e:
            logger.error(f"Failed to list data: {e}")
            return []
    
    def _create_metadata(self, data: Any, data_type: DataType, identifier: str) -> DataMetadata:
        """Create metadata for data."""
        data_str = json.dumps(data, default=str)
        checksum = str(hash(data_str))
        
        return DataMetadata(
            data_id=identifier,
            data_type=data_type,
            created_at=time.time(),
            updated_at=time.time(),
            size_bytes=len(data_str.encode('utf-8')),
            record_count=len(data) if isinstance(data, (list, dict)) else 1,
            checksum=checksum,
            tags=[data_type.value, identifier],
            description=f"Test data for {data_type.value}: {identifier}"
        )
    
    def cleanup_old_data(self) -> bool:
        """Clean up old data based on retention policy."""
        try:
            with self._lock:
                cutoff_time = time.time() - (self.config.retention_days * 24 * 3600)
                cleaned_count = 0
                
                for type_dir in self.base_path.iterdir():
                    if type_dir.is_dir():
                        for file_path in type_dir.glob("*.json"):
                            try:
                                # Check file modification time
                                if file_path.stat().st_mtime < cutoff_time:
                                    file_path.unlink()
                                    cleaned_count += 1
                            except Exception as e:
                                logger.warning(f"Failed to check file {file_path}: {e}")
                
                logger.info(f"Cleaned up {cleaned_count} old data files")
                return True
                
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")
            return False


class ResultManager:
    """Manages test results and execution data."""
    
    def __init__(self, data_persistence: DataPersistence):
        self.data_persistence = data_persistence
        self.results_cache: Dict[str, Any] = {}
        self._lock = threading.Lock()
    
    def store_test_result(self, test_id: str, result: Any) -> bool:
        """Store a test result."""
        try:
            with self._lock:
                # Store in cache
                self.results_cache[test_id] = result
                
                # Store in persistence
                success = self.data_persistence.save_data(
                    result, DataType.TEST_RESULTS, test_id
                )
                
                if success:
                    logger.info(f"Test result stored: {test_id}")
                    return True
                else:
                    logger.error(f"Failed to store test result: {test_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error storing test result: {e}")
            return False
    
    def get_test_result(self, test_id: str) -> Optional[Any]:
        """Get a test result."""
        try:
            with self._lock:
                # Check cache first
                if test_id in self.results_cache:
                    return self.results_cache[test_id]
                
                # Load from persistence
                result = self.data_persistence.load_data(DataType.TEST_RESULTS, test_id)
                
                if result:
                    # Update cache
                    self.results_cache[test_id] = result
                
                return result
                
        except Exception as e:
            logger.error(f"Error getting test result: {e}")
            return None
    
    def get_all_results(self) -> List[Any]:
        """Get all test results."""
        try:
            with self._lock:
                result_ids = self.data_persistence.list_data(DataType.TEST_RESULTS)
                results = []
                
                for result_id in result_ids:
                    result = self.get_test_result(result_id)
                    if result:
                        results.append(result)
                
                return results
                
        except Exception as e:
            logger.error(f"Error getting all results: {e}")
            return []
    
    def delete_test_result(self, test_id: str) -> bool:
        """Delete a test result."""
        try:
            with self._lock:
                # Remove from cache
                if test_id in self.results_cache:
                    del self.results_cache[test_id]
                
                # Remove from persistence
                success = self.data_persistence.delete_data(DataType.TEST_RESULTS, test_id)
                
                if success:
                    logger.info(f"Test result deleted: {test_id}")
                    return True
                else:
                    logger.error(f"Failed to delete test result: {test_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting test result: {e}")
            return False
    
    def clear_all_results(self) -> bool:
        """Clear all test results."""
        try:
            with self._lock:
                # Clear cache
                self.results_cache.clear()
                
                # Clear persistence
                result_ids = self.data_persistence.list_data(DataType.TEST_RESULTS)
                for result_id in result_ids:
                    self.data_persistence.delete_data(DataType.TEST_RESULTS, result_id)
                
                logger.info("All test results cleared")
                return True
                
        except Exception as e:
            logger.error(f"Error clearing all results: {e}")
            return False


class ReportGenerator:
    """Generates test reports and summaries."""
    
    def __init__(self, data_persistence: DataPersistence):
        self.data_persistence = data_persistence
    
    def generate_test_summary_report(self, output_file: str) -> bool:
        """Generate a comprehensive test summary report."""
        try:
            # Collect all test results
            results = self._collect_all_test_data()
            
            # Generate report
            report = self._create_summary_report(results)
            
            # Save report
            with open(output_file, 'w') as f:
                json.dump(report, f, default=str, indent=2)
            
            logger.info(f"Test summary report generated: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate test summary report: {e}")
            return False
    
    def generate_performance_report(self, output_file: str) -> bool:
        """Generate a performance-focused report."""
        try:
            # Collect performance data
            performance_data = self._collect_performance_data()
            
            # Generate performance report
            report = self._create_performance_report(performance_data)
            
            # Save report
            with open(output_file, 'w') as f:
                json.dump(report, f, default=str, indent=2)
            
            logger.info(f"Performance report generated: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate performance report: {e}")
            return False
    
    def _collect_all_test_data(self) -> Dict[str, Any]:
        """Collect all test data for reporting."""
        data = {}
        
        # Collect test results
        test_results = self.data_persistence.list_data(DataType.TEST_RESULTS)
        data["test_results"] = len(test_results)
        
        # Collect performance metrics
        performance_metrics = self.data_persistence.list_data(DataType.PERFORMANCE_METRICS)
        data["performance_metrics"] = len(performance_metrics)
        
        # Collect message history
        message_history = self.data_persistence.list_data(DataType.MESSAGE_HISTORY)
        data["message_history"] = len(message_history)
        
        # Collect agent registry
        agent_registry = self.data_persistence.list_data(DataType.AGENT_REGISTRY)
        data["agent_registry"] = len(agent_registry)
        
        return data
    
    def _collect_performance_data(self) -> Dict[str, Any]:
        """Collect performance data for reporting."""
        performance_data = {}
        
        # Get performance metrics
        metric_ids = self.data_persistence.list_data(DataType.PERFORMANCE_METRICS)
        
        for metric_id in metric_ids:
            metric_data = self.data_persistence.load_data(DataType.PERFORMANCE_METRICS, metric_id)
            if metric_data:
                performance_data[metric_id] = metric_data
        
        return performance_data
    
    def _create_summary_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary report from collected data."""
        return {
            "report_type": "test_summary",
            "generated_at": datetime.now().isoformat(),
            "data_summary": data,
            "total_records": sum(data.values()),
            "status": "completed"
        }
    
    def _create_performance_report(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a performance report from collected data."""
        return {
            "report_type": "performance_summary",
            "generated_at": datetime.now().isoformat(),
            "performance_metrics_count": len(performance_data),
            "performance_data": performance_data,
            "status": "completed"
        }


class TestDataManager:
    """Main test data management class."""
    
    def __init__(self, config: Optional[DataStorageConfig] = None):
        self.config = config or DataStorageConfig()
        self.data_persistence = DataPersistence(self.config)
        self.result_manager = ResultManager(self.data_persistence)
        self.report_generator = ReportGenerator(self.data_persistence)
    
    def store_data(self, data: Any, data_type: DataType, identifier: str) -> bool:
        """Store data of any type."""
        return self.data_persistence.save_data(data, data_type, identifier)
    
    def load_data(self, data_type: DataType, identifier: str) -> Optional[Any]:
        """Load data of any type."""
        return self.data_persistence.load_data(data_type, identifier)
    
    def delete_data(self, data_type: DataType, identifier: str) -> bool:
        """Delete data of any type."""
        return self.data_persistence.delete_data(data_type, identifier)
    
    def list_data(self, data_type: DataType) -> List[str]:
        """List available data of a type."""
        return self.data_persistence.list_data(data_type)
    
    def store_test_result(self, test_id: str, result: Any) -> bool:
        """Store a test result."""
        return self.result_manager.store_test_result(test_id, result)
    
    def get_test_result(self, test_id: str) -> Optional[Any]:
        """Get a test result."""
        return self.result_manager.get_test_result(test_id)
    
    def get_all_results(self) -> List[Any]:
        """Get all test results."""
        return self.result_manager.get_all_results()
    
    def delete_test_result(self, test_id: str) -> bool:
        """Delete a test result."""
        return self.result_manager.delete_test_result(test_id)
    
    def clear_all_results(self) -> bool:
        """Clear all test results."""
        return self.result_manager.clear_all_results()
    
    def generate_test_summary_report(self, output_file: str) -> bool:
        """Generate a test summary report."""
        return self.report_generator.generate_test_summary_report(output_file)
    
    def generate_performance_report(self, output_file: str) -> bool:
        """Generate a performance report."""
        return self.report_generator.generate_performance_report(output_file)
    
    def cleanup_old_data(self) -> bool:
        """Clean up old data."""
        return self.data_persistence.cleanup_old_data()
    
    def get_storage_status(self) -> Dict[str, Any]:
        """Get storage status information."""
        status = {}
        
        for data_type in DataType:
            data_count = len(self.data_persistence.list_data(data_type))
            status[data_type.value] = data_count
        
        status["total_records"] = sum(status.values())
        status["base_directory"] = str(self.config.base_directory)
        status["retention_days"] = self.config.retention_days
        
        return status
