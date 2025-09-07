#!/usr/bin/env python3
"""
Unified Service Registry - Agent-2 SSOT Consolidation Mission Phase 3
Provides unified service discovery and management for all consolidated services
"""
import os
import json
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, Callable
from datetime import datetime
import importlib
import logging

class ServiceMetadata:
    """Metadata for a registered service."""
    
    def __init__(self, name: str, service_type: str, file_path: str, 
                 description: str = "", dependencies: List[str] = None):
        self.name = name
        self.service_type = service_type
        self.file_path = file_path
        self.description = description
        self.dependencies = dependencies or []
        self.registration_time = datetime.now()
        self.last_accessed = datetime.now()
        self.access_count = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'name': self.name,
            'service_type': self.service_type,
            'file_path': self.file_path,
            'description': self.description,
            'dependencies': self.dependencies,
            'registration_time': self.registration_time.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'access_count': self.access_count
        }
    
    def update_access(self):
        """Update access statistics."""
        self.last_accessed = datetime.now()
        self.access_count += 1

class ServiceRegistry:
    """Unified service registry for all consolidated services."""
    
    def __init__(self):
        self.services: Dict[str, ServiceMetadata] = {}
        self.service_types: Dict[str, List[str]] = {}
        self.service_instances: Dict[str, Any] = {}
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service registry."""
        logger = logging.getLogger('ServiceRegistry')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def register_service(self, name: str, service_type: str, file_path: str,
                        description: str = "", dependencies: List[str] = None) -> bool:
        """Register a service in the registry."""
        try:
            if name in self.services:
                self.logger.warning(f"Service {name} already registered, updating metadata")
            
            metadata = ServiceMetadata(name, service_type, file_path, description, dependencies)
            self.services[name] = metadata
            
            # Add to service types index
            if service_type not in self.service_types:
                self.service_types[service_type] = []
            self.service_types[service_type].append(name)
            
            self.logger.info(f"Service {name} registered successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register service {name}: {e}")
            return False
    
    def unregister_service(self, name: str) -> bool:
        """Unregister a service from the registry."""
        try:
            if name not in self.services:
                self.logger.warning(f"Service {name} not found in registry")
                return False
            
            metadata = self.services[name]
            service_type = metadata.service_type
            
            # Remove from services
            del self.services[name]
            
            # Remove from service types index
            if service_type in self.service_types and name in self.service_types[service_type]:
                self.service_types[service_type].remove(name)
                if not self.service_types[service_type]:
                    del self.service_types[service_type]
            
            # Remove from instances
            if name in self.service_instances:
                del self.service_instances[name]
            
            self.logger.info(f"Service {name} unregistered successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister service {name}: {e}")
            return False
    
    def get_service(self, name: str) -> Optional[Any]:
        """Get a service instance by name."""
        try:
            if name not in self.services:
                self.logger.warning(f"Service {name} not found in registry")
                return None
            
            metadata = self.services[name]
            metadata.update_access()
            
            # Return cached instance if available
            if name in self.service_instances:
                return self.service_instances[name]
            
            # Try to import and instantiate the service
            try:
                module_path = metadata.file_path.replace('/', '.').replace('\\', '.')
                if module_path.endswith('.py'):
                    module_path = module_path[:-3]
                
                module = importlib.import_module(module_path)
                
                # Look for the service class/function
                service_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (inspect.isclass(attr) or inspect.isfunction(attr)) and attr_name.lower() in name.lower():
                        service_class = attr
                        break
                
                if service_class:
                    if inspect.isclass(service_class):
                        instance = service_class()
                    else:
                        instance = service_class
                    
                    self.service_instances[name] = instance
                    self.logger.info(f"Service {name} instantiated successfully")
                    return instance
                else:
                    self.logger.warning(f"Could not find service class/function for {name}")
                    return None
                    
            except Exception as e:
                self.logger.error(f"Failed to instantiate service {name}: {e}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting service {name}: {e}")
            return None
    
    def get_services_by_type(self, service_type: str) -> List[str]:
        """Get all service names of a specific type."""
        return self.service_types.get(service_type, [])
    
    def list_services(self, service_type: str = None) -> List[ServiceMetadata]:
        """List all services or services of a specific type."""
        if service_type:
            service_names = self.service_types.get(service_type, [])
            return [self.services[name] for name in service_names if name in self.services]
        else:
            return list(self.services.values())
    
    def search_services(self, query: str) -> List[ServiceMetadata]:
        """Search for services by name or description."""
        query = query.lower()
        results = []
        
        for metadata in self.services.values():
            if (query in metadata.name.lower() or 
                query in metadata.description.lower() or
                query in metadata.service_type.lower()):
                results.append(metadata)
        
        return results
    
    def get_service_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a service."""
        if name not in self.services:
            return None
        
        metadata = self.services[name]
        info = metadata.to_dict()
        
        # Add additional information
        info['is_instantiated'] = name in self.service_instances
        info['file_exists'] = os.path.exists(metadata.file_path)
        
        return info
    
    def export_registry(self, file_path: str = None) -> str:
        """Export the service registry to a file."""
        if not file_path:
            file_path = f"service_registry_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_services': len(self.services),
                'service_types': self.service_types,
                'services': {name: metadata.to_dict() for name, metadata in self.services.items()}
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            self.logger.info(f"Service registry exported to {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Failed to export service registry: {e}")
            return None
    
    def import_registry(self, file_path: str) -> bool:
        """Import a service registry from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Clear existing registry
            self.services.clear()
            self.service_types.clear()
            self.service_instances.clear()
            
            # Import services
            for name, service_data in import_data.get('services', {}).items():
                metadata = ServiceMetadata(
                    name=service_data['name'],
                    service_type=service_data['service_type'],
                    file_path=service_data['file_path'],
                    description=service_data.get('description', ''),
                    dependencies=service_data.get('dependencies', [])
                )
                metadata.registration_time = datetime.fromisoformat(service_data['registration_time'])
                metadata.last_accessed = datetime.fromisoformat(service_data['last_accessed'])
                metadata.access_count = service_data.get('access_count', 0)
                
                self.services[name] = metadata
                
                # Rebuild service types index
                service_type = metadata.service_type
                if service_type not in self.service_types:
                    self.service_types[service_type] = []
                self.service_types[service_type].append(name)
            
            self.logger.info(f"Service registry imported from {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import service registry: {e}")
            return False
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get statistics about the service registry."""
        total_services = len(self.services)
        total_types = len(self.service_types)
        instantiated_services = len(self.service_instances)
        
        type_counts = {service_type: len(services) for service_type, services in self.service_types.items()}
        
        return {
            'total_services': total_services,
            'total_service_types': total_types,
            'instantiated_services': instantiated_services,
            'service_type_distribution': type_counts,
            'registry_size': len(str(self.services)),
            'last_updated': datetime.now().isoformat()
        }

class ServiceDiscovery:
    """Service discovery utilities for the consolidated service layer."""
    
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
    
    def discover_services(self, base_path: str = "src/services") -> Dict[str, List[str]]:
        """Automatically discover services in the consolidated directory."""
        discovered = {}
        
        try:
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, base_path)
                        
                        # Determine service type based on file path or content
                        service_type = self._determine_service_type(file_path, relative_path)
                        
                        if service_type not in discovered:
                            discovered[service_type] = []
                        
                        discovered[service_type].append(relative_path)
            
            return discovered
            
        except Exception as e:
            self.registry.logger.error(f"Error discovering services: {e}")
            return {}
    
    def _determine_service_type(self, file_path: str, relative_path: str) -> str:
        """Determine the type of service based on file path and content."""
        try:
            # Check file content for service indicators
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # Determine type based on content and path
            if 'messaging' in relative_path.lower() or 'message' in content:
                return 'messaging'
            elif 'dashboard' in relative_path.lower() or 'dashboard' in content:
                return 'dashboard'
            elif 'orchestration' in relative_path.lower() or 'orchestrate' in content:
                return 'orchestration'
            elif 'test' in relative_path.lower() or 'test' in content:
                return 'testing'
            elif 'validation' in relative_path.lower() or 'validate' in content:
                return 'validation'
            elif 'api' in relative_path.lower() or 'api' in content:
                return 'api'
            else:
                return 'utility'
                
        except Exception:
            return 'unknown'
    
    def auto_register_discovered_services(self, base_path: str = "src/services") -> int:
        """Automatically register all discovered services."""
        discovered = self.discover_services(base_path)
        registered_count = 0
        
        for service_type, services in discovered.items():
            for service_path in services:
                service_name = os.path.splitext(os.path.basename(service_path))[0]
                full_path = os.path.join(base_path, service_path)
                
                if self.registry.register_service(
                    name=service_name,
                    service_type=service_type,
                    file_path=full_path,
                    description=f"Auto-discovered {service_type} service"
                ):
                    registered_count += 1
        
        return registered_count

# Global service registry instance
service_registry = ServiceRegistry()
service_discovery = ServiceDiscovery(service_registry)

def get_service_registry() -> ServiceRegistry:
    """Get the global service registry instance."""
    return service_registry

def get_service_discovery() -> ServiceDiscovery:
    """Get the global service discovery instance."""
    return service_discovery

def register_service(name: str, service_type: str, file_path: str,
                    description: str = "", dependencies: List[str] = None) -> bool:
    """Convenience function to register a service."""
    return service_registry.register_service(name, service_type, file_path, description, dependencies)

def get_service(name: str) -> Optional[Any]:
    """Convenience function to get a service."""
    return service_registry.get_service(name)

def list_services(service_type: str = None) -> List[ServiceMetadata]:
    """Convenience function to list services."""
    return service_registry.list_services(service_type)

if __name__ == "__main__":
    # Example usage and testing
    print("Unified Service Registry - Agent-2 SSOT Consolidation Mission")
    
    # Auto-discover and register services
    print("Discovering services...")
    discovered_count = service_discovery.auto_register_discovered_services()
    print(f"Discovered and registered {discovered_count} services")
    
    # Display registry statistics
    stats = service_registry.get_registry_stats()
    print(f"Registry statistics: {stats}")
    
    # Export registry
    export_file = service_registry.export_registry()
    if export_file:
        print(f"Registry exported to: {export_file}")
    
    print("Service registry initialization complete!")
