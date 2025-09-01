/**
 * Service Resolver Module - V2 Compliant
 * Service resolution and dependency injection utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class ServiceResolver {
    constructor(serviceRegistry, logger = console) {
        this.registry = serviceRegistry;
        this.logger = logger;
        this.resolutionCache = new Map();
        this.resolutionStack = [];
    }

    /**
     * Resolve a service by name
     */
    resolve(serviceName) {
        try {
            // Check for circular dependency
            if (this.resolutionStack.includes(serviceName)) {
                throw new Error(`Circular dependency detected: ${this.resolutionStack.join(' -> ')} -> ${serviceName}`);
            }

            // Check resolution cache for singletons
            const cached = this.resolutionCache.get(serviceName);
            if (cached && cached.config.singleton) {
                return cached.instance;
            }

            // Get service configuration
            const serviceConfig = this.registry.getServiceConfig(serviceName);
            if (!serviceConfig) {
                throw new Error(`Service not found: ${serviceName}`);
            }

            // Add to resolution stack
            this.resolutionStack.push(serviceName);

            try {
                // Resolve dependencies
                const dependencies = this.resolveDependencies(serviceConfig.dependencies);

                // Create service instance
                const instance = this.createServiceInstance(serviceConfig, dependencies);

                // Cache singleton instances
                if (serviceConfig.singleton) {
                    this.resolutionCache.set(serviceName, {
                        instance,
                        config: serviceConfig
                    });
                }

                if (this.logger) {
                    this.logger.log(`[DIC] Service resolved: ${serviceName}`);
                }

                return instance;
            } finally {
                // Remove from resolution stack
                this.resolutionStack.pop();
            }
        } catch (error) {
            if (this.logger) {
                this.logger.error('Service resolution failed', error);
            }
            throw error;
        }
    }

    /**
     * Resolve multiple services
     */
    resolveMultiple(serviceNames) {
        const results = {};
        for (const name of serviceNames) {
            results[name] = this.resolve(name);
        }
        return results;
    }

    /**
     * Resolve service dependencies
     */
    resolveDependencies(dependencies) {
        if (!Array.isArray(dependencies)) {
            return [];
        }

        return dependencies.map(dep => {
            if (typeof dep === 'string') {
                return this.resolve(dep);
            } else if (typeof dep === 'object' && dep.service) {
                const instance = this.resolve(dep.service);
                return dep.optional ? instance : instance;
            }
            return dep;
        });
    }

    /**
     * Create service instance
     */
    createServiceInstance(serviceConfig, dependencies) {
        try {
            if (serviceConfig.factory) {
                // Factory function
                return serviceConfig.factory(...dependencies);
            } else {
                // Constructor
                return new serviceConfig.class(...dependencies);
            }
        } catch (error) {
            throw new Error(`Failed to create service instance for ${serviceConfig.name}: ${error.message}`);
        }
    }

    /**
     * Check if service can be resolved
     */
    canResolve(serviceName) {
        try {
            const config = this.registry.getServiceConfig(serviceName);
            if (!config) return false;

            // Check if all dependencies can be resolved
            return config.dependencies.every(dep => {
                const depName = typeof dep === 'string' ? dep : dep.service;
                return this.registry.isRegistered(depName) || (dep.optional === true);
            });
        } catch (error) {
            return false;
        }
    }

    /**
     * Get service resolution info
     */
    getResolutionInfo(serviceName) {
        const config = this.registry.getServiceConfig(serviceName);
        if (!config) return null;

        return {
            name: config.name,
            dependencies: config.dependencies,
            singleton: config.singleton,
            canResolve: this.canResolve(serviceName),
            isResolved: this.resolutionCache.has(serviceName)
        };
    }

    /**
     * Clear resolution cache
     */
    clearCache() {
        try {
            const count = this.resolutionCache.size;
            this.resolutionCache.clear();
            if (this.logger) {
                this.logger.log(`[DIC] Resolution cache cleared: ${count} entries removed`);
            }
            return count;
        } catch (error) {
            if (this.logger) {
                this.logger.error('Cache clear failed', error);
            }
            return 0;
        }
    }

    /**
     * Get resolution statistics
     */
    getResolutionStats() {
        const stats = {
            cacheSize: this.resolutionCache.size,
            cachedServices: Array.from(this.resolutionCache.keys()),
            resolutionStack: [...this.resolutionStack]
        };

        return stats;
    }

    /**
     * Dispose of resolver resources
     */
    dispose() {
        this.clearCache();
        this.resolutionStack = [];
    }
}

// Factory function for creating service resolver instance
export function createServiceResolver(serviceRegistry, logger = console) {
    return new ServiceResolver(serviceRegistry, logger);
}
