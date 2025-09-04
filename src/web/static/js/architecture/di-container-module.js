/**
 * DI Container Module - V2 Compliant
 * Core dependency injection container functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// DI CONTAINER MODULE
// ================================

/**
 * Core dependency injection container
 */
export class DIContainer {
    constructor() {
        this.services = new Map();
        this.scopes = new Map();
        this.coordinationStatus = {
            agent7Support: 'ACTIVE',
            framework: 'OPERATIONAL',
            v2Compliance: 'READY'
        };
    }

    /**
     * Register a service with the container
     */
    register(token, factory, options = {}) {
        const serviceConfig = {
            factory,
            singleton: options.singleton !== false,
            instance: null,
            dependencies: options.dependencies || [],
            scope: options.scope || 'global'
        };

        this.services.set(token, serviceConfig);
        return this;
    }

    /**
     * Resolve a service from the container
     */
    resolve(token) {
        const serviceConfig = this.services.get(token);

        if (!serviceConfig) {
            throw new Error(`Service '${token}' not registered`);
        }

        // Return singleton instance if available
        if (serviceConfig.singleton && serviceConfig.instance) {
            return serviceConfig.instance;
        }

        // Create new instance
        const instance = this.createInstance(serviceConfig);

        // Store singleton instance
        if (serviceConfig.singleton) {
            serviceConfig.instance = instance;
        }

        return instance;
    }

    /**
     * Create instance with dependency injection
     */
    createInstance(serviceConfig) {
        const dependencies = serviceConfig.dependencies.map(dep => this.resolve(dep));
        return serviceConfig.factory(...dependencies);
    }

    /**
     * Create a new scope
     */
    createScope(scopeName) {
        const scope = new DIContainer();
        scope.services = new Map(this.services);
        this.scopes.set(scopeName, scope);
        return scope;
    }

    /**
     * Get scope by name
     */
    getScope(scopeName) {
        return this.scopes.get(scopeName);
    }

    /**
     * Check if service is registered
     */
    isRegistered(token) {
        return this.services.has(token);
    }

    /**
     * Get all registered services
     */
    getRegisteredServices() {
        return Array.from(this.services.keys());
    }

    /**
     * Clear all services and scopes
     */
    clear() {
        this.services.clear();
        this.scopes.clear();
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create DI container instance
 */
export function createDIContainer() {
    return new DIContainer();
}

