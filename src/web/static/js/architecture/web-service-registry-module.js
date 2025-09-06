/**
 * Web Service Registry Module - V2 Compliant
 * Web layer service registration and management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createServiceLocator } from './service-locator-module.js';

// ================================
// WEB LAYER SERVICE REGISTRY
// ================================

/**
 * Web layer service registry for managing web services
 */
export class WebLayerServiceRegistry {
    constructor() {
        this.locator = createServiceLocator();
        this.coordinationStatus = {
            agent7Support: 'ACTIVE',
            registry: 'OPERATIONAL',
            v2Compliance: 'READY'
        };
        this.registeredServices = new Set();
    }

    /**
     * Register dashboard services
     */
    async registerDashboardServices() {
        try {
            // Dynamic imports for dashboard services
            const services = [
                { module: '../repositories/dashboard-repository.js', token: 'dashboardRepository', className: 'DashboardRepository' },
                { module: '../services/dashboard-service.js', token: 'dashboardService', className: 'DashboardService' },
                { module: '../dashboard-state-manager.js', token: 'dashboardStateManager', className: 'DashboardStateManager' }
            ];

            for (const service of services) {
                try {
                    const module = await import(service.module);
                    const ServiceClass = module[service.className];
                    if (ServiceClass) {
                        this.locator.registerService(service.token, () => new ServiceClass());
                        this.registeredServices.add(service.token);
                    }
                } catch (error) {
                    console.warn(`Failed to register ${service.token}:`, error.message);
                }
            }
        } catch (error) {
            console.error('Error registering dashboard services:', error);
        }
    }

    /**
     * Register testing services
     */
    async registerTestingServices() {
        try {
            const services = [
                { module: '../repositories/testing-repository.js', token: 'testingRepository', className: 'TestingRepository' },
                { module: '../services/testing-service.js', token: 'testingService', className: 'TestingService' }
            ];

            for (const service of services) {
                try {
                    const module = await import(service.module);
                    const ServiceClass = module[service.className];
                    if (ServiceClass) {
                        this.locator.registerService(service.token, () => new ServiceClass());
                        this.registeredServices.add(service.token);
                    }
                } catch (error) {
                    console.warn(`Failed to register ${service.token}:`, error.message);
                }
            }
        } catch (error) {
            console.error('Error registering testing services:', error);
        }
    }

    /**
     * Register deployment services
     */
    async registerDeploymentServices() {
        try {
            const services = [
                { module: '../repositories/deployment-repository.js', token: 'deploymentRepository', className: 'DeploymentRepository' },
                { module: '../services/deployment-service.js', token: 'deploymentService', className: 'DeploymentService' }
            ];

            for (const service of services) {
                try {
                    const module = await import(service.module);
                    const ServiceClass = module[service.className];
                    if (ServiceClass) {
                        this.locator.registerService(service.token, () => new ServiceClass());
                        this.registeredServices.add(service.token);
                    }
                } catch (error) {
                    console.warn(`Failed to register ${service.token}:`, error.message);
                }
            }
        } catch (error) {
            console.error('Error registering deployment services:', error);
        }
    }

    /**
     * Register utility services
     */
    async registerUtilityServices() {
        try {
            const services = [
                { module: '../utilities/logging-utils.js', token: 'loggingUtils', factory: 'createLoggingUtils' },
                { module: '../utilities/validation-utils.js', token: 'validationUtils', className: 'ValidationUtils' }
            ];

            for (const service of services) {
                try {
                    const module = await import(service.module);
                    if (service.factory) {
                        const factory = module[service.factory];
                        if (factory) {
                            this.locator.registerService(service.token, factory);
                            this.registeredServices.add(service.token);
                        }
                    } else if (service.className) {
                        const ServiceClass = module[service.className];
                        if (ServiceClass) {
                            this.locator.registerService(service.token, () => new ServiceClass());
                            this.registeredServices.add(service.token);
                        }
                    }
                } catch (error) {
                    console.warn(`Failed to register ${service.token}:`, error.message);
                }
            }
        } catch (error) {
            console.error('Error registering utility services:', error);
        }
    }

    /**
     * Register all web layer services
     */
    async registerAllServices() {
        console.log('🚀 Registering all web layer services...');

        await Promise.all([
            this.registerDashboardServices(),
            this.registerTestingServices(),
            this.registerDeploymentServices(),
            this.registerUtilityServices()
        ]);

        console.log(`✅ ${this.registeredServices.size} web services registered`);
    }

    /**
     * Get service locator
     */
    getServiceLocator() {
        return this.locator;
    }

    /**
     * Get coordination status
     */
    getCoordinationStatus() {
        return {
            ...this.coordinationStatus,
            registeredServices: Array.from(this.registeredServices),
            totalServices: this.registeredServices.size,
            agent7Support: 'ACTIVE',
            v2Compliance: 'READY'
        };
    }

    /**
     * Check if service is registered
     */
    isServiceRegistered(token) {
        return this.registeredServices.has(token);
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create web layer service registry instance
 */
export function createWebLayerServiceRegistry() {
    return new WebLayerServiceRegistry();
}
