"""
Trading Robot Dependency Injection Container - V2 Compliant DI Framework
Centralized dependency management with service registration and resolution
REFACTORED: Clean DI container with comprehensive service management
V2 COMPLIANCE: Under 300-line limit, comprehensive error handling, modular design

@author Agent-7 - Web Development Specialist (adapted for Trading Robot)
@version 1.0.0 - V2 COMPLIANCE DEPENDENCY INJECTION
@license MIT
"""



class DependencyInjectionError(Exception):
    """Custom exception for dependency injection errors."""
    pass


class TradingDependencyContainer:
    """Dependency injection container for trading robot components."""

    def __init__(self):
        """Initialize DI container."""
        self.logger = UnifiedLoggingSystem("TradingDependencyContainer")
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
        self._scoped_instances: Dict[str, Dict[str, Any]] = {}

        # Register default services
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default trading services."""
        try:
            self.logger.get_unified_logger().log_operation_start("register_defaults")

            # Register repository factory
            self.register_factory("trading_repository",
                                lambda: create_trading_repository(),
                                singleton=True)

            # Register service factory with dependency
            self.register_factory("trading_service",
                                lambda repo: create_trading_service(repo),
                                singleton=True)

            self.logger.get_unified_logger().log_operation_complete("register_defaults", {
                "services_registered": 2
            })

        except Exception as e:
            self.logger.log_error("register_defaults", str(e))
            raise DependencyInjectionError(f"Failed to register defaults: {e}")

    def register_factory(self, name: str, factory: Callable,
                        singleton: bool = False) -> None:
        """Register a service factory."""
        try:
            self.logger.get_unified_logger().log_operation_start("register_factory", {
                "service_name": name, "singleton": singleton
            })

            if not callable(factory):
                raise DependencyInjectionError(f"Factory for {name} must be callable")

            self._factories[name] = factory
            if singleton:
                self._services[name] = None  # Mark as singleton but not yet instantiated

            self.logger.get_unified_logger().log_operation_complete("register_factory", {
                "service_name": name, "factory_registered": True
            })

        except Exception as e:
            self.logger.log_error("register_factory", str(e), {"service_name": name})
            raise DependencyInjectionError(f"Failed to register factory {name}: {e}")

    def register_instance(self, name: str, instance: Any,
                        singleton: bool = True) -> None:
        """Register a service instance directly."""
        try:
            self.logger.get_unified_logger().log_operation_start(operation)_start("register_instance", {
                "service_name": name, "singleton": singleton
            })

            if singleton:
                self._singletons[name] = instance
            else:
                self._services[name] = instance

            self.logger.get_unified_logger().log_operation_start(operation)_complete("register_instance", {
                "service_name": name, "instance_registered": True
            })

        except Exception as e:
            self.logger.log_error("register_instance", str(e), {"service_name": name})
            raise DependencyInjectionError(f"Failed to register instance {name}: {e}")

    def resolve(self, name: str, scope: Optional[str] = None) -> Any:
        """Resolve a service by name."""
        try:
            self.logger.get_unified_logger().log_operation_start(operation)_start("resolve", {
                "service_name": name, "scope": scope
            })

            # Check if it's a scoped instance
            if scope and name in self._scoped_instances.get(scope, {}):
                instance = self._scoped_instances[scope][name]
                self.logger.get_unified_logger().log_operation_start(operation)_complete("resolve", {
                    "service_name": name, "resolved_from": "scoped_cache"
                })
                return instance

            # Check if it's a singleton
            if name in self._singletons:
                self.logger.get_unified_logger().log_operation_start(operation)_complete("resolve", {
                    "service_name": name, "resolved_from": "singleton"
                })
                return self._singletons[name]

            # Check if it's a cached instance
            if name in self._services and self._services[name] is not None:
                instance = self._services[name]
                self.logger.get_unified_logger().log_operation_start(operation)_complete("resolve", {
                    "service_name": name, "resolved_from": "cache"
                })
                return instance

            # Try to create from factory
            if name in self._factories:
                factory = self._factories[name]
                instance = self._create_from_factory(name, factory)

                # Cache singleton instances
                if self._services.get(name) is None:  # Marked as singleton
                    self._singletons[name] = instance
                else:
                    self._services[name] = instance

                # Cache scoped instances
                if scope:
                    if scope not in self._scoped_instances:
                        self._scoped_instances[scope] = {}
                    self._scoped_instances[scope][name] = instance

                self.logger.get_unified_logger().log_operation_start(operation)_complete("resolve", {
                    "service_name": name, "resolved_from": "factory"
                })
                return instance

            raise DependencyInjectionError(f"Service {name} not registered")

        except Exception as e:
            self.logger.log_error("resolve", str(e), {"service_name": name})
            raise DependencyInjectionError(f"Failed to resolve service {name}: {e}")

    def _create_from_factory(self, name: str, factory: Callable) -> Any:
        """Create instance from factory with dependency resolution."""
        try:
            sig = inspect.signature(factory)
            params = {}

            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue

                # Try to resolve parameter as a service
                try:
                    params[param_name] = self.resolve(param_name)
                except DependencyInjectionError:
                    # If parameter is not a registered service, it should be provided
                    if param.default == inspect.Parameter.empty:
                        raise DependencyInjectionError(
                            f"Cannot resolve parameter {param_name} for service {name}"
                        )
                    # Use default value if available
                    params[param_name] = param.default

            return factory(**params)

        except Exception as e:
            raise DependencyInjectionError(f"Failed to create {name} from factory: {e}")

    def has_service(self, name: str) -> bool:
        """Check if a service is registered."""
        return (name in self._services or
                name in self._factories or
                name in self._singletons)

    def clear_scope(self, scope: str) -> None:
        """Clear all scoped instances for a scope."""
        try:
            if scope in self._scoped_instances:
                self.logger.get_unified_logger().log_operation_start(operation)_start("clear_scope", {"scope": scope})
                del self._scoped_instances[scope]
                self.logger.get_unified_logger().log_operation_start(operation)_complete("clear_scope", {"scope": scope})
        except Exception as e:
            self.logger.log_error("clear_scope", str(e), {"scope": scope})

    def get_registered_services(self) -> Dict[str, str]:
        """Get list of all registered services with their types."""
        services = {}

        for name in self._singletons:
            services[name] = "singleton"
        for name in self._factories:
            services[name] = "factory"
        for name in self._services:
            services[name] = "instance"

        return services


# Global container instance
_trading_container = None


def get_trading_container() -> TradingDependencyContainer:
    """Get the global trading dependency container."""
    global _trading_container
    if _trading_container is None:
        _trading_container = TradingDependencyContainer()
    return _trading_container


def reset_trading_container() -> None:
    """Reset the global container (useful for testing)"""
    global _trading_container
    _trading_container = None


# Convenience functions for service resolution
def get_trading_repository() -> TradingRepositoryInterface:
    """Get trading repository from DI container."""
    return get_trading_container().resolve("trading_repository")


def get_trading_service() -> TradingService:
    """Get trading service from DI container."""
    return get_trading_container().resolve("trading_service")


# Export for DI
__all__ = [
    'TradingDependencyContainer',
    'DependencyInjectionError',
    'get_trading_container',
    'reset_trading_container',
    'get_trading_repository',
    'get_trading_service'
]
