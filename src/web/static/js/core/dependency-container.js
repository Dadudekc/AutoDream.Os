/**
 * Dependency Injection Container - V2 Compliance Implementation
 * Centralized dependency management with service registration and resolution
 * V2 Compliance: Eliminates circular dependencies and enables clean architecture
 */

export class DependencyContainer {
    constructor() {
        this.services = new Map();
        this.singletons = new Map();
        this.factories = new Map();
        this.config = {
            enableLogging: true,
            autoResolve: true,
            strictMode: false
        };
    }

    // Service registration methods
    registerService(serviceName, serviceClass, options = {}) {
        try {
            if (!serviceName || typeof serviceName !== 'string') {
                throw new Error('Invalid service name provided');
            }

            if (!serviceClass || typeof serviceClass !== 'function') {
                throw new Error('Invalid service class provided');
            }

            const serviceConfig = {
                name: serviceName,
                class: serviceClass,
                dependencies: options.dependencies || [],
                singleton: options.singleton !== false,
                factory: options.factory || false,
                instance: null,
                timestamp: Date.now()
            };

            this.services.set(serviceName, serviceConfig);
            
            if (this.config.enableLogging) {
                console.log(`[DIC] Service registered: ${serviceName}`);
            }

            return true;
        } catch (error) {
            this.logError('Service registration failed', error);
            return false;
        }
    }

    registerSingleton(serviceName, serviceClass, dependencies = []) {
        return this.registerService(serviceName, serviceClass, {
            dependencies: dependencies,
            singleton: true
        });
    }

    registerFactory(serviceName, factoryFunction, dependencies = []) {
        try {
            if (!factoryFunction || typeof factoryFunction !== 'function') {
                throw new Error('Invalid factory function provided');
            }

            this.factories.set(serviceName, {
                name: serviceName,
                factory: factoryFunction,
                dependencies: dependencies,
                timestamp: Date.now()
            });

            if (this.config.enableLogging) {
                console.log(`[DIC] Factory registered: ${serviceName}`);
            }

            return true;
        } catch (error) {
            this.logError('Factory registration failed', error);
            return false;
        }
    }

    // Service resolution methods
    resolve(serviceName, options = {}) {
        try {
            if (!serviceName || typeof serviceName !== 'string') {
                throw new Error('Invalid service name provided');
            }

            // Check if service exists
            if (!this.services.has(serviceName) && !this.factories.has(serviceName)) {
                throw new Error(`Service '${serviceName}' not registered`);
            }

            // Resolve factory
            if (this.factories.has(serviceName)) {
                return this.resolveFactory(serviceName, options);
            }

            // Resolve service
            return this.resolveService(serviceName, options);
        } catch (error) {
            this.logError(`Service resolution failed for '${serviceName}'`, error);
            
            if (this.config.strictMode) {
                throw error;
            }
            
            return null;
        }
    }

    resolveService(serviceName, options = {}) {
        const serviceConfig = this.services.get(serviceName);
        
        // Return existing singleton instance
        if (serviceConfig.singleton && serviceConfig.instance) {
            return serviceConfig.instance;
        }

        // Resolve dependencies
        const resolvedDependencies = this.resolveDependencies(serviceConfig.dependencies, options);
        
        // Create new instance
        const instance = new serviceConfig.class(...resolvedDependencies);
        
        // Store singleton instance
        if (serviceConfig.singleton) {
            serviceConfig.instance = instance;
        }

        return instance;
    }

    resolveFactory(serviceName, options = {}) {
        const factoryConfig = this.factories.get(serviceName);
        
        // Resolve dependencies
        const resolvedDependencies = this.resolveDependencies(factoryConfig.dependencies, options);
        
        // Execute factory function
        return factoryConfig.factory(...resolvedDependencies);
    }

    resolveDependencies(dependencies, options = {}) {
        try {
            const resolved = [];

            for (const dependency of dependencies) {
                if (typeof dependency === 'string') {
                    // Resolve service dependency
                    const resolvedDependency = this.resolve(dependency, options);
                    resolved.push(resolvedDependency);
                } else if (typeof dependency === 'function') {
                    // Resolve function dependency
                    resolved.push(dependency);
                } else if (dependency && typeof dependency === 'object') {
                    // Resolve object dependency
                    resolved.push(dependency);
                } else {
                    // Resolve primitive dependency
                    resolved.push(dependency);
                }
            }

            return resolved;
        } catch (error) {
            this.logError('Dependency resolution failed', error);
            return [];
        }
    }

    // Auto-registration methods
    autoRegister(modulePath) {
        try {
            // Dynamic import for auto-registration
            return import(modulePath).then(module => {
                if (module.default && typeof module.default === 'function') {
                    const serviceName = this.extractServiceName(modulePath);
                    this.registerService(serviceName, module.default);
                    return true;
                }
                return false;
            });
        } catch (error) {
            this.logError('Auto-registration failed', error);
            return Promise.resolve(false);
        }
    }

    extractServiceName(modulePath) {
        try {
            const parts = modulePath.split('/');
            const filename = parts[parts.length - 1];
            const nameWithoutExt = filename.replace(/\.[^/.]+$/, '');
            
            // Convert kebab-case or snake_case to camelCase
            return nameWithoutExt
                .replace(/[-_]([a-z])/g, (match, letter) => letter.toUpperCase())
                .replace(/^[a-z]/, letter => letter.toUpperCase());
        } catch (error) {
            this.logError('Service name extraction failed', error);
            return 'UnknownService';
        }
    }

    // Service management methods
    unregisterService(serviceName) {
        try {
            if (!serviceName || typeof serviceName !== 'string') {
                throw new Error('Invalid service name provided');
            }

            const removed = this.services.delete(serviceName);
            
            if (removed && this.config.enableLogging) {
                console.log(`[DIC] Service unregistered: ${serviceName}`);
            }

            return removed;
        } catch (error) {
            this.logError('Service unregistration failed', error);
            return false;
        }
    }

    getServiceInfo(serviceName) {
        try {
            if (this.services.has(serviceName)) {
                const config = this.services.get(serviceName);
                return {
                    name: config.name,
                    class: config.class.name,
                    dependencies: config.dependencies,
                    singleton: config.singleton,
                    hasInstance: !!config.instance,
                    timestamp: config.timestamp
                };
            }

            if (this.factories.has(serviceName)) {
                const config = this.factories.get(serviceName);
                return {
                    name: config.name,
                    type: 'factory',
                    dependencies: config.dependencies,
                    timestamp: config.timestamp
                };
            }

            return null;
        } catch (error) {
            this.logError('Service info retrieval failed', error);
            return null;
        }
    }

    listServices() {
        try {
            const serviceList = [];

            // Add registered services
            for (const [name, config] of this.services.entries()) {
                serviceList.push({
                    name: name,
                    type: 'service',
                    class: config.class.name,
                    singleton: config.singleton,
                    dependencies: config.dependencies.length,
                    hasInstance: !!config.instance
                });
            }

            // Add registered factories
            for (const [name, config] of this.factories.entries()) {
                serviceList.push({
                    name: name,
                    type: 'factory',
                    dependencies: config.dependencies.length
                });
            }

            return serviceList;
        } catch (error) {
            this.logError('Service listing failed', error);
            return [];
        }
    }

    // Configuration methods
    updateConfig(newConfig) {
        try {
            this.config = { ...this.config, ...newConfig };
            
            if (this.config.enableLogging) {
                console.log('[DIC] Configuration updated:', this.config);
            }
        } catch (error) {
            this.logError('Config update failed', error);
        }
    }

    getConfig() {
        return { ...this.config };
    }

    // Validation methods
    validateDependencies() {
        try {
            const issues = [];

            for (const [serviceName, config] of this.services.entries()) {
                for (const dependency of config.dependencies) {
                    if (typeof dependency === 'string') {
                        if (!this.services.has(dependency) && !this.factories.has(dependency)) {
                            issues.push({
                                service: serviceName,
                                dependency: dependency,
                                issue: 'Dependency not registered'
                            });
                        }
                    }
                }
            }

            return {
                valid: issues.length === 0,
                issues: issues
            };
        } catch (error) {
            this.logError('Dependency validation failed', error);
            return { valid: false, issues: [{ issue: 'Validation failed', error: error.message }] };
        }
    }

    detectCircularDependencies() {
        try {
            const visited = new Set();
            const recursionStack = new Set();
            const circularDeps = [];

            for (const serviceName of this.services.keys()) {
                if (!visited.has(serviceName)) {
                    this.dfsDetectCircular(serviceName, visited, recursionStack, circularDeps, []);
                }
            }

            return {
                hasCircular: circularDeps.length > 0,
                circularDependencies: circularDeps
            };
        } catch (error) {
            this.logError('Circular dependency detection failed', error);
            return { hasCircular: false, circularDependencies: [] };
        }
    }

    dfsDetectCircular(serviceName, visited, recursionStack, circularDeps, path) {
        try {
            if (recursionStack.has(serviceName)) {
                const cycle = [...path, serviceName];
                circularDeps.push(cycle);
                return;
            }

            if (visited.has(serviceName)) {
                return;
            }

            visited.add(serviceName);
            recursionStack.add(serviceName);
            path.push(serviceName);

            const serviceConfig = this.services.get(serviceName);
            if (serviceConfig) {
                for (const dependency of serviceConfig.dependencies) {
                    if (typeof dependency === 'string') {
                        this.dfsDetectCircular(dependency, visited, recursionStack, circularDeps, path);
                    }
                }
            }

            path.pop();
            recursionStack.delete(serviceName);
        } catch (error) {
            this.logError('DFS circular detection failed', error);
        }
    }

    // Cleanup methods
    clear() {
        try {
            this.services.clear();
            this.singletons.clear();
            this.factories.clear();
            
            if (this.config.enableLogging) {
                console.log('[DIC] All services cleared');
            }
        } catch (error) {
            this.logError('Container clearing failed', error);
        }
    }

    dispose() {
        try {
            // Dispose singleton instances
            for (const [name, config] of this.services.entries()) {
                if (config.instance && typeof config.instance.dispose === 'function') {
                    config.instance.dispose();
                }
            }

            this.clear();
        } catch (error) {
            this.logError('Container disposal failed', error);
        }
    }

    // Error handling methods
    logError(message, error) {
        if (this.config.enableLogging) {
            console.error(`[DIC] ${message}:`, error);
        }
    }

    logInfo(message, data) {
        if (this.config.enableLogging) {
            console.info(`[DIC] ${message}:`, data);
        }
    }
}

// Global dependency container instance
export const globalContainer = new DependencyContainer();

// Auto-registration helper
export function autoRegisterServices(services) {
    try {
        services.forEach(service => {
            if (service.name && service.class) {
                globalContainer.registerService(service.name, service.class, service.options);
            }
        });
        
        return true;
    } catch (error) {
        console.error('[DIC] Auto-registration failed:', error);
        return false;
    }
}
