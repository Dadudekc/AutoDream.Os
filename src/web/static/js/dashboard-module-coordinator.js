/**
 * Dashboard Module Coordinator - V2 Compliant Module Coordination
 * Specialized module coordination for dashboard orchestrator
 * V2 COMPLIANCE: Under 100-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

export class DashboardModuleCoordinator {
    constructor(orchestrator) {
        this.orchestrator = orchestrator;
        this.modules = new Map();
        this.dependencies = new Map();
        this.healthStatus = new Map();
    }

    /**
     * Setup module coordination
     */
    setupModuleCoordination() {
        console.log('🔗 Setting up module coordination...');

        // Register core modules
        this.registerModule('communication', {
            initialized: false,
            dependencies: [],
            status: 'pending'
        });

        this.registerModule('navigation', {
            initialized: false,
            dependencies: ['communication'],
            status: 'pending'
        });

        this.registerModule('dataManager', {
            initialized: false,
            dependencies: ['communication'],
            status: 'pending'
        });

        this.registerModule('uiHelpers', {
            initialized: false,
            dependencies: [],
            status: 'pending'
        });

        this.registerModule('eventHandler', {
            initialized: false,
            dependencies: [],
            status: 'pending'
        });

        this.registerModule('timeManager', {
            initialized: false,
            dependencies: [],
            status: 'pending'
        });

        console.log('✅ Module coordination established');
    }

    /**
     * Register a module
     */
    registerModule(name, config) {
        this.modules.set(name, config);
        this.healthStatus.set(name, 'pending');
        console.log(`📦 Module registered: ${name}`);
    }

    /**
     * Mark module as initialized
     */
    markModuleInitialized(name) {
        if (this.modules.has(name)) {
            const module = this.modules.get(name);
            module.initialized = true;
            module.status = 'initialized';
            this.healthStatus.set(name, 'healthy');
            console.log(`✅ Module initialized: ${name}`);
        }
    }

    /**
     * Check if module dependencies are met
     */
    checkDependencies(name) {
        const module = this.modules.get(name);
        if (!module || !module.dependencies) return true;

        return module.dependencies.every(dep => {
            const depModule = this.modules.get(dep);
            return depModule && depModule.initialized;
        });
    }

    /**
     * Get module status
     */
    getModuleStatus(name) {
        return this.modules.get(name) || { initialized: false, status: 'not_found' };
    }

    /**
     * Get overall coordination status
     */
    getCoordinationStatus() {
        const totalModules = this.modules.size;
        const initializedModules = Array.from(this.modules.values())
            .filter(module => module.initialized).length;

        return {
            totalModules,
            initializedModules,
            healthPercentage: totalModules > 0 ? (initializedModules / totalModules) * 100 : 0,
            moduleStatuses: Object.fromEntries(this.modules),
            healthStatuses: Object.fromEntries(this.healthStatus),
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Validate module health
     */
    validateModuleHealth(name) {
        const module = this.modules.get(name);
        if (!module) return false;

        const dependenciesMet = this.checkDependencies(name);
        const isInitialized = module.initialized;

        const isHealthy = dependenciesMet && isInitialized;
        this.healthStatus.set(name, isHealthy ? 'healthy' : 'unhealthy');

        return isHealthy;
    }

    /**
     * Get unhealthy modules
     */
    getUnhealthyModules() {
        const unhealthy = [];
        for (const [name, status] of this.healthStatus) {
            if (status !== 'healthy') {
                unhealthy.push({
                    name,
                    status,
                    module: this.modules.get(name)
                });
            }
        }
        return unhealthy;
    }

    /**
     * Reset coordination
     */
    resetCoordination() {
        this.modules.clear();
        this.dependencies.clear();
        this.healthStatus.clear();
        console.log('🔄 Module coordination reset');
    }
}

// Factory function
export function createDashboardModuleCoordinator(orchestrator) {
    return new DashboardModuleCoordinator(orchestrator);
}

// ================================
// GLOBAL COORDINATOR INSTANCE
// ================================

let dashboardModuleCoordinator = null;

/**
 * Get global module coordinator instance
 */
export function getDashboardModuleCoordinator(orchestrator) {
    if (!dashboardModuleCoordinator) {
        dashboardModuleCoordinator = new DashboardModuleCoordinator(orchestrator);
    }
    return dashboardModuleCoordinator;
}
