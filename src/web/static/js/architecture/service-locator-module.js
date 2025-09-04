/**
 * Service Locator Module - V2 Compliant
 * Service locator pattern implementation
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createDIContainer } from './di-container-module.js';

// ================================
// SERVICE LOCATOR MODULE
// ================================

/**
 * Service locator pattern implementation
 */
export class ServiceLocator {
    constructor() {
        this.container = createDIContainer();
        this.coordinationStatus = {
            agent7Support: 'ACTIVE',
            serviceLocator: 'OPERATIONAL',
            v2Compliance: 'READY'
        };
    }

    /**
     * Register service with locator
     */
    registerService(token, factory, options = {}) {
        this.container.register(token, factory, options);
        return this;
    }

    /**
     * Get service from locator
     */
    getService(token) {
        return this.container.resolve(token);
    }

    /**
     * Check if service exists
     */
    hasService(token) {
        return this.container.isRegistered(token);
    }

    /**
     * Get all available services
     */
    getAvailableServices() {
        return this.container.getRegisteredServices();
    }

    /**
     * Create scoped service locator
     */
    createScopedLocator(scopeName) {
        const scopedContainer = this.container.createScope(scopeName);
        const scopedLocator = new ServiceLocator();
        scopedLocator.container = scopedContainer;
        return scopedLocator;
    }

    /**
     * Get coordination status
     */
    getCoordinationStatus() {
        return {
            ...this.coordinationStatus,
            registeredServices: this.getAvailableServices(),
            containerStatus: this.container.coordinationStatus
        };
    }

    /**
     * Clear all services
     */
    clear() {
        this.container.clear();
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create service locator instance
 */
export function createServiceLocator() {
    return new ServiceLocator();
}

