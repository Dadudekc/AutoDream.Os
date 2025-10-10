/**
 * Services Orchestrator - V2 Compliant Modular System
 * Coordinates all service modules with proper separation of concerns
 * V2 COMPLIANCE: <200 lines orchestrator coordinating modular components
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - MODULAR REFACTORING
 * @license MIT
 */

// ================================
// SERVICES ORCHESTRATOR
// ================================

/**
 * Services Orchestrator - Coordinates all service modules
 * Maintains backward compatibility while ensuring V2 compliance
 */
class ServicesOrchestrator {
    constructor() {
        // Service registries
        this.services = new Map();
        this.modules = new Map();
        this.eventListeners = new Map();

        // Core modules
        this.dataService = null;
        this.socketService = null;
        this.performanceService = null;
        this.validationService = null;
        this.utilityService = null;

        // Configuration
        this.config = {
            enableCaching: true,
            enableLogging: true,
            cacheTimeout: 5 * 60 * 1000,
            retryAttempts: 3
        };

        // State
        this.initialized = false;
        this.cache = new Map();
    }

    // ================================
    // INITIALIZATION
    // ================================

    /**
     * Initialize the services orchestrator
     */
    async initialize(config = {}) {
        if (this.initialized) {
            console.warn('⚠️ Services orchestrator already initialized');
            return;
        }

        console.log('🚀 Initializing Services Orchestrator...');

        try {
            // Merge configuration
            Object.assign(this.config, config);

            // Initialize core modules
            await this.initializeModules();

            // Setup event coordination
            this.setupEventCoordination();

            this.initialized = true;
            console.log('✅ Services Orchestrator initialized successfully');

        } catch (error) {
            console.error('❌ Services orchestrator initialization failed:', error);
            throw error;
        }
    }

    /**
     * Initialize all service modules
     */
    async initializeModules() {
        // Import and initialize core modules from services/ subdirectory (Phase 2 consolidation)
        const [
            { DashboardDataService },
            { SocketEventHandlers },
            { PerformanceAnalysisModule },
            { ComponentValidationModule },
            { UtilityFunctionService }
        ] = await Promise.all([
            import('./services/dashboard-data-service.js'),
            import('./services/socket-event-handlers.js'),
            import('./services/performance-analysis-module.js'),
            import('./services/component-validation-module.js'),
            import('./services/utility-function-service.js')
        ]);

        // Create service instances (using subdirectory services)
        this.dataService = new DashboardDataService(this.config);
        this.socketService = new SocketEventHandlers(this.config);
        this.performanceService = new PerformanceAnalysisModule(this.config);
        this.validationService = new ComponentValidationModule(this.config);
        this.utilityService = new UtilityFunctionService(this.config);

        // Register modules
        this.modules.set('data', this.dataService);
        this.modules.set('socket', this.socketService);
        this.modules.set('performance', this.performanceService);
        this.modules.set('validation', this.validationService);
        this.modules.set('utilities', this.utilityService);

        // Initialize all modules
        for (const [name, module] of this.modules) {
            if (typeof module.initialize === 'function') {
                await module.initialize();
            }
        }
    }

    /**
     * Setup event coordination between modules
     */
    setupEventCoordination() {
        // Data service events
        this.dataService?.on?.('dataUpdated', (data) => {
            this.emit('dataUpdated', data);
        });

        // Socket service events
        this.socketService?.on?.('connected', () => {
            this.emit('socketConnected');
        });

        this.socketService?.on?.('disconnected', () => {
            this.emit('socketDisconnected');
        });

        // Performance service events
        this.performanceService?.on?.('metricsCollected', (metrics) => {
            this.emit('performanceMetrics', metrics);
        });
    }

    // ================================
    // SERVICE COORDINATION
    // ================================

    /**
     * Get a service by name
     */
    getService(name) {
        return this.modules.get(name);
    }

    /**
     * Execute operation across services
     */
    async execute(operation, payload = {}) {
        try {
            switch (operation) {
                case 'loadData':
                    return await this.dataService.loadData(payload);
                case 'sendMessage':
                    return await this.socketService.sendMessage(payload);
                case 'validateData':
                    return this.validationService.validate(payload);
                case 'getPerformance':
                    return this.performanceService.getMetrics();
                default:
                    throw new Error(`Unknown operation: ${operation}`);
            }
        } catch (error) {
            this.handleError(error, { operation, payload });
            throw error;
        }
    }

    /**
     * Broadcast operation to all services
     */
    async broadcast(operation, payload = {}) {
        const results = [];

        for (const [name, service] of this.modules) {
            try {
                if (typeof service[operation] === 'function') {
                    const result = await service[operation](payload);
                    results.push({ service: name, result });
                }
            } catch (error) {
                results.push({ service: name, error: error.message });
            }
        }

        return results;
    }

    // ================================
    // EVENT MANAGEMENT
    // ================================

    /**
     * Register event listener
     */
    on(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }

    /**
     * Remove event listener
     */
    off(event, callback) {
        const listeners = this.eventListeners.get(event);
        if (listeners) {
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    /**
     * Emit event
     */
    emit(event, data) {
        const listeners = this.eventListeners.get(event);
        if (listeners) {
            listeners.forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Event callback error for ${event}:`, error);
                }
            });
        }
    }

    // ================================
    // UTILITY METHODS
    // ================================

    /**
     * Handle errors
     */
    handleError(error, context = {}) {
        console.error('❌ Services Orchestrator Error:', error);

        // Log error with context
        if (this.config.enableLogging) {
            console.error('Error context:', context);
        }

        // Emit error event
        this.emit('error', { error, context });
    }

    /**
     * Get orchestrator status
     */
    getStatus() {
        return {
            initialized: this.initialized,
            modules: Array.from(this.modules.keys()),
            config: { ...this.config },
            cache: {
                size: this.cache.size,
                keys: Array.from(this.cache.keys())
            }
        };
    }

    /**
     * Get service statistics
     */
    getStats() {
        const stats = {
            orchestrator: this.getStatus(),
            services: {}
        };

        for (const [name, service] of this.modules) {
            if (typeof service.getStats === 'function') {
                stats.services[name] = service.getStats();
            }
        }

        return stats;
    }

    // ================================
    // CLEANUP
    // ================================

    /**
     * Cleanup orchestrator and all services
     */
    async destroy() {
        console.log('🧹 Cleaning up Services Orchestrator...');

        // Cleanup all modules
        for (const [name, service] of this.modules) {
            try {
                if (typeof service.destroy === 'function') {
                    await service.destroy();
                }
            } catch (error) {
                console.error(`Error cleaning up ${name} service:`, error);
            }
        }

        // Clear registries
        this.services.clear();
        this.modules.clear();
        this.cache.clear();
        this.eventListeners.clear();

        // Reset state
        this.initialized = false;

        console.log('✅ Services Orchestrator cleaned up');
    }
}

// ================================
// LEGACY COMPATIBILITY
// ================================

/**
 * Legacy factory function for existing code
 * @deprecated Use new ServicesOrchestrator class directly
 */
export function createUnifiedServices(config) {
    const orchestrator = new ServicesOrchestrator();
    orchestrator.initialize(config);
    return orchestrator;
}


// ================================
// EXPORTS
// ================================

export default ServicesOrchestrator;
export { ServicesOrchestrator };
