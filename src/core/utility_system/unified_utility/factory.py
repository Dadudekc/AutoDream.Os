"""
Utility Factory
===============

Factory for creating utility system components.
V2 Compliance: < 300 lines, single responsibility, factory pattern.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Dict, Any, Optional, Type
from .models import UtilityConfig, UtilityOperationType, UtilitySystemModels
from .coordinator import UtilityCoordinator


class UtilityFactory:
    """Factory for creating utility system components."""
    
    def __init__(self):
        """Initialize utility factory."""
        self._registered_operations: Dict[UtilityOperationType, Type] = {}
        self._default_config = UtilitySystemModels.create_utility_config()
    
    def create_coordinator(self, config: Optional[UtilityConfig] = None) -> UtilityCoordinator:
        """Create utility coordinator."""
        if config is None:
            config = self._default_config
        
        return UtilityCoordinator(config)
    
    def create_config(
        self,
        cache_enabled: bool = True,
        validation_enabled: bool = True,
        transformation_enabled: bool = True,
        coordination_enabled: bool = True,
        metrics_enabled: bool = True,
        max_cache_size: int = 1000,
        cache_ttl_seconds: int = 3600,
        validation_timeout_seconds: int = 30,
        transformation_timeout_seconds: int = 60,
        coordination_timeout_seconds: int = 120,
        metrics_collection_interval: int = 300
    ) -> UtilityConfig:
        """Create utility configuration."""
        return UtilitySystemModels.create_utility_config(
            cache_enabled=cache_enabled,
            validation_enabled=validation_enabled,
            transformation_enabled=transformation_enabled,
            coordination_enabled=coordination_enabled,
            metrics_enabled=metrics_enabled,
            max_cache_size=max_cache_size,
            cache_ttl_seconds=cache_ttl_seconds,
            validation_timeout_seconds=validation_timeout_seconds,
            transformation_timeout_seconds=transformation_timeout_seconds,
            coordination_timeout_seconds=coordination_timeout_seconds,
            metrics_collection_interval=metrics_collection_interval
        )
    
    def register_operation(
        self, 
        operation_type: UtilityOperationType, 
        operation_class: Type
    ) -> None:
        """Register operation class for specific type."""
        self._registered_operations[operation_type] = operation_class
    
    def create_operation(
        self, 
        operation_type: UtilityOperationType, 
        **kwargs
    ) -> Any:
        """Create operation instance."""
        if operation_type not in self._registered_operations:
            raise ValueError(f"No registered operation class for type: {operation_type}")
        
        operation_class = self._registered_operations[operation_type]
        return operation_class(**kwargs)
    
    def get_registered_operations(self) -> Dict[UtilityOperationType, Type]:
        """Get all registered operations."""
        return self._registered_operations.copy()
    
    def is_operation_registered(self, operation_type: UtilityOperationType) -> bool:
        """Check if operation type is registered."""
        return operation_type in self._registered_operations
    
    def unregister_operation(self, operation_type: UtilityOperationType) -> None:
        """Unregister operation type."""
        if operation_type in self._registered_operations:
            del self._registered_operations[operation_type]
    
    def create_default_config(self) -> UtilityConfig:
        """Create default configuration."""
        return self._default_config
    
    def create_optimized_config(self) -> UtilityConfig:
        """Create optimized configuration for high performance."""
        return UtilitySystemModels.create_utility_config(
            cache_enabled=True,
            validation_enabled=True,
            transformation_enabled=True,
            coordination_enabled=True,
            metrics_enabled=True,
            max_cache_size=5000,
            cache_ttl_seconds=7200,
            validation_timeout_seconds=15,
            transformation_timeout_seconds=30,
            coordination_timeout_seconds=60,
            metrics_collection_interval=60
        )
    
    def create_development_config(self) -> UtilityConfig:
        """Create development configuration with relaxed settings."""
        return UtilitySystemModels.create_utility_config(
            cache_enabled=False,
            validation_enabled=True,
            transformation_enabled=True,
            coordination_enabled=True,
            metrics_enabled=True,
            max_cache_size=100,
            cache_ttl_seconds=300,
            validation_timeout_seconds=60,
            transformation_timeout_seconds=120,
            coordination_timeout_seconds=240,
            metrics_collection_interval=600
        )
    
    def create_production_config(self) -> UtilityConfig:
        """Create production configuration with strict settings."""
        return UtilitySystemModels.create_utility_config(
            cache_enabled=True,
            validation_enabled=True,
            transformation_enabled=True,
            coordination_enabled=True,
            metrics_enabled=True,
            max_cache_size=10000,
            cache_ttl_seconds=3600,
            validation_timeout_seconds=10,
            transformation_timeout_seconds=20,
            coordination_timeout_seconds=30,
            metrics_collection_interval=300
        )
    
    def create_testing_config(self) -> UtilityConfig:
        """Create testing configuration."""
        return UtilitySystemModels.create_utility_config(
            cache_enabled=False,
            validation_enabled=True,
            transformation_enabled=True,
            coordination_enabled=False,
            metrics_enabled=True,
            max_cache_size=10,
            cache_ttl_seconds=60,
            validation_timeout_seconds=5,
            transformation_timeout_seconds=10,
            coordination_timeout_seconds=15,
            metrics_collection_interval=30
        )
    
    def get_config_presets(self) -> Dict[str, UtilityConfig]:
        """Get all available configuration presets."""
        return {
            'default': self.create_default_config(),
            'optimized': self.create_optimized_config(),
            'development': self.create_development_config(),
            'production': self.create_production_config(),
            'testing': self.create_testing_config()
        }
    
    def validate_config(self, config: UtilityConfig) -> Dict[str, Any]:
        """Validate configuration and return validation results."""
        validation_results = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Validate cache settings
        if config.cache_enabled and config.max_cache_size <= 0:
            validation_results['errors'].append("max_cache_size must be positive when cache is enabled")
            validation_results['is_valid'] = False
        
        if config.cache_ttl_seconds <= 0:
            validation_results['errors'].append("cache_ttl_seconds must be positive")
            validation_results['is_valid'] = False
        
        # Validate timeout settings
        if config.validation_timeout_seconds <= 0:
            validation_results['errors'].append("validation_timeout_seconds must be positive")
            validation_results['is_valid'] = False
        
        if config.transformation_timeout_seconds <= 0:
            validation_results['errors'].append("transformation_timeout_seconds must be positive")
            validation_results['is_valid'] = False
        
        if config.coordination_timeout_seconds <= 0:
            validation_results['errors'].append("coordination_timeout_seconds must be positive")
            validation_results['is_valid'] = False
        
        # Validate metrics settings
        if config.metrics_collection_interval <= 0:
            validation_results['errors'].append("metrics_collection_interval must be positive")
            validation_results['is_valid'] = False
        
        # Add warnings
        if config.max_cache_size > 10000:
            validation_results['warnings'].append("Large cache size may impact memory usage")
        
        if config.cache_ttl_seconds > 86400:  # 24 hours
            validation_results['warnings'].append("Long cache TTL may lead to stale data")
        
        if config.validation_timeout_seconds > 300:  # 5 minutes
            validation_results['warnings'].append("Long validation timeout may impact performance")
        
        return validation_results
