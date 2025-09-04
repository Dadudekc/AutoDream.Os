/**
 * Service Registry Module - V2 Compliant
 * Service registration and management utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class ServiceRegistry {
    constructor(logger = console) {
        this.services = new Map();
        this.logger = logger;
    }

    /**
     * Register a service with the container
     */
    register(serviceName, serviceClass, options = {}) {
        try {
            this.validateRegistration(serviceName, serviceClass);

            const serviceConfig = this.createServiceConfig(serviceName, serviceClass, options);
            this.services.set(serviceName, serviceConfig);

            if (this.logger) {
                this.logger.log(`[DIC] Service registered: ${serviceName}`);
            }

            return true;
        } catch (error) {
            if (this.logger) {
                this.logger.error('Service registration failed', error);
            }
            return false;
        }
    }

    /**
     * Register a singleton service
     */
    registerSingleton(serviceName, serviceClass, options = {}) {
        return this.register(serviceName, serviceClass, {
            ...options,
            singleton: true
        });
    }

    /**
     * Register a factory function
     */
    registerFactory(serviceName, factoryFn, options = {}) {
        try {
            if (!serviceName || typeof serviceName !== 'string') {
                throw new Error('Invalid service name provided');
            }

            if (!factoryFn || typeof factoryFn !== 'function') {
                throw new Error('Invalid factory function provided');
            }

            const serviceConfig = {
                name: serviceName,
                factory: factoryFn,
                dependencies: options.dependencies || [],
                singleton: options.singleton !== false,
                instance: null,
                timestamp: Date.now()
            };

            this.services.set(serviceName, serviceConfig);

            if (this.logger) {
                this.logger.log(`[DIC] Factory registered: ${serviceName}`);
            }

            return true;
        } catch (error) {
            if (this.logger) {
                this.logger.error('Factory registration failed', error);
            }
            return false;
        }
    }

    /**
     * Check if a service is registered
     */
    isRegistered(serviceName) {
        return this.services.has(serviceName);
    }

    /**
     * Get service configuration
     */
    getServiceConfig(serviceName) {
        return this.services.get(serviceName) || null;
    }

    /**
     * Remove a service from registry
     */
    unregister(serviceName) {
        try {
            const removed = this.services.delete(serviceName);
            if (removed && this.logger) {
                this.logger.log(`[DIC] Service unregistered: ${serviceName}`);
            }
            return removed;
        } catch (error) {
            if (this.logger) {
                this.logger.error('Service unregistration failed', error);
            }
            return false;
        }
    }

    /**
     * Clear all registered services
     */
    clear() {
        try {
            const count = this.services.size;
            this.services.clear();
            if (this.logger) {
                this.logger.log(`[DIC] Registry cleared: ${count} services removed`);
            }
            return count;
        } catch (error) {
            if (this.logger) {
                this.logger.error('Registry clear failed', error);
            }
            return 0;
        }
    }

    /**
     * Get all registered service names
     */
    getServiceNames() {
        return Array.from(this.services.keys());
    }

    /**
     * Get registry statistics
     */
    getStats() {
        const stats = {
            totalServices: this.services.size,
            singletonServices: 0,
            factoryServices: 0
        };

        for (const config of this.services.values()) {
            if (config.singleton) stats.singletonServices++;
            if (config.factory) stats.factoryServices++;
        }

        return stats;
    }

    /**
     * Validate service registration parameters
     */
    validateRegistration(serviceName, serviceClass) {
        if (!serviceName || typeof serviceName !== 'string') {
            throw new Error('Invalid service name provided');
        }

        if (!serviceClass || typeof serviceClass !== 'function') {
            throw new Error('Invalid service class provided');
        }
    }

    /**
     * Create service configuration object
     */
    createServiceConfig(serviceName, serviceClass, options = {}) {
        return {
            name: serviceName,
            class: serviceClass,
            dependencies: options.dependencies || [],
            singleton: options.singleton !== false,
            factory: false,
            instance: null,
            timestamp: Date.now()
        };
    }
}

// Factory function for creating service registry instance
export function createServiceRegistry(logger = console) {
    return new ServiceRegistry(logger);
}


