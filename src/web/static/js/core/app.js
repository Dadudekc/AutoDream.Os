/**
 * V2 Swarm Application Core - Consolidated Main Controller
 * V2 COMPLIANT: 300 lines maximum
 * CONSOLIDATES: app.js (641 lines) → 300 lines orchestrator
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Main application orchestrator with dependency injection
 */

// ================================
// DEPENDENCY IMPORTS
// ================================

import { ConfigManager } from './config.js';
import { Router } from './router.js';
import { PerformanceMonitor } from '../modules/utils/performance-utils.js';
import { ErrorHandler } from '../modules/utils/error-utils.js';
import { ComponentLoader } from '../modules/components/component-loader.js';
import { WebSocketService } from '../modules/services/websocket-service.js';

// ================================
// MAIN APPLICATION CLASS
// ================================

/**
 * V2 Swarm Application Core
 * Orchestrates all application modules with dependency injection
 */
export class V2SwarmApp {
    constructor(options = {}) {
        // Core configuration
        this.version = '5.0.0';
        this.mode = 'V2_COMPLIANCE_MODE';
        this.isInitialized = false;

        // Dependency injection
        this.dependencies = {
            configManager: options.configManager || new ConfigManager(),
            router: options.router || new Router(),
            performanceMonitor: options.performanceMonitor || new PerformanceMonitor(),
            errorHandler: options.errorHandler || new ErrorHandler(),
            componentLoader: options.componentLoader || new ComponentLoader(),
            websocketService: options.websocketService || new WebSocketService()
        };

        // Application state
        this.components = new Map();
        this.currentView = 'dashboard';
        this.performanceMetrics = {
            loadTime: 0,
            initializationTime: 0,
            componentLoadTime: 0
        };

        // Initialize application
        this.init();
    }

    /**
     * Initialize the V2 Swarm application
     */
    async init() {
        if (this.isInitialized) {
            console.warn('⚠️ V2 Swarm App already initialized');
            return;
        }

        const startTime = performance.now();
        console.log('🚀 V2 Swarm App Initializing (V2 Compliant)...');

        try {
            // Initialize core systems
            await this.initializeCoreSystems();

            // Load critical components
            await this.loadCriticalComponents();

            // Setup event coordination
            this.setupEventCoordination();

            // Initialize current view
            await this.initializeCurrentView();

            // Mark as initialized
            this.isInitialized = true;
            this.performanceMetrics.loadTime = performance.now() - startTime;

            console.log(`✅ V2 Swarm App Ready - Load time: ${this.performanceMetrics.loadTime.toFixed(2)}ms`);

        } catch (error) {
            console.error('❌ V2 Swarm App initialization failed:', error);
            await this.dependencies.errorHandler.handleError(error, { context: 'app_initialization' });
            throw error;
        }
    }

    /**
     * Initialize core application systems
     */
    async initializeCoreSystems() {
        console.log('⚙️ Initializing core systems...');

        // Initialize configuration
        await this.dependencies.configManager.load();

        // Initialize router
        await this.dependencies.router.initialize();

        // Initialize performance monitoring
        this.dependencies.performanceMonitor.start();

        // Initialize WebSocket service
        await this.dependencies.websocketService.initialize();

        console.log('✅ Core systems initialized');
    }

    /**
     * Load critical application components
     */
    async loadCriticalComponents() {
        console.log('🔧 Loading critical components...');

        const criticalComponents = [
            'Navigation',
            'Dashboard',
            'AgentCoordinator'
        ];

        const startTime = performance.now();

        for (const componentName of criticalComponents) {
            await this.loadComponent(componentName, true);
        }

        this.performanceMetrics.componentLoadTime = performance.now() - startTime;
        console.log(`✅ Critical components loaded in ${this.performanceMetrics.componentLoadTime.toFixed(2)}ms`);
    }

    /**
     * Load a component with error handling
     */
    async loadComponent(componentName, isCritical = false) {
        try {
            const component = await this.dependencies.componentLoader.load(componentName, {
                app: this,
                dependencies: this.dependencies
            });

            if (component) {
                this.components.set(componentName, component);
                await component.initialize();

                if (isCritical) {
                    console.log(`✅ Critical component loaded: ${componentName}`);
                }
            }
        } catch (error) {
            console.error(`❌ Failed to load component ${componentName}:`, error);
            
            if (isCritical) {
                await this.dependencies.errorHandler.handleError(error, {
                    context: 'critical_component_load',
                    component: componentName
                });
            }
        }
    }

    /**
     * Setup event coordination between modules
     */
    setupEventCoordination() {
        console.log('📡 Setting up event coordination...');

        // Navigation events
        window.addEventListener('app:navigate', (event) => {
            this.handleNavigation(event.detail);
        });

        // Component events
        window.addEventListener('component:loaded', (event) => {
            this.handleComponentLoaded(event.detail);
        });

        // Performance events
        window.addEventListener('performance:measure', (event) => {
            this.handlePerformanceMeasure(event.detail);
        });

        // Error events
        window.addEventListener('error:occurred', (event) => {
            this.handleError(event.detail);
        });

        console.log('✅ Event coordination setup complete');
    }

    /**
     * Initialize the current view
     */
    async initializeCurrentView() {
        try {
            await this.dependencies.router.navigateTo(this.currentView);
            console.log(`✅ Current view initialized: ${this.currentView}`);
        } catch (error) {
            console.error('❌ Failed to initialize current view:', error);
            await this.dependencies.errorHandler.handleError(error, {
                context: 'view_initialization',
                view: this.currentView
            });
        }
    }

    /**
     * Handle navigation events
     */
    async handleNavigation(navigationData) {
        try {
            const { view, params } = navigationData;
            await this.dependencies.router.navigateTo(view, params);
            this.currentView = view;
            console.log(`🔄 Navigation to: ${view}`);
        } catch (error) {
            console.error('❌ Navigation failed:', error);
            await this.dependencies.errorHandler.handleError(error, {
                context: 'navigation',
                data: navigationData
            });
        }
    }

    /**
     * Handle component loaded events
     */
    handleComponentLoaded(componentData) {
        console.log('📦 Component loaded:', componentData.name);
        // Additional component initialization logic can be added here
    }

    /**
     * Handle performance measurement events
     */
    handlePerformanceMeasure(measurementData) {
        this.dependencies.performanceMonitor.record(measurementData);
    }

    /**
     * Handle error events
     */
    async handleError(errorData) {
        await this.dependencies.errorHandler.handleError(
            new Error(errorData.message),
            errorData.context
        );
    }

    /**
     * Switch to a different view
     */
    async switchView(viewName, params = {}) {
        try {
            await this.dependencies.router.navigateTo(viewName, params);
            this.currentView = viewName;
            
            // Dispatch navigation event
            window.dispatchEvent(new CustomEvent('app:navigate', {
                detail: { view: viewName, params }
            }));

        } catch (error) {
            console.error(`❌ Failed to switch to view ${viewName}:`, error);
            await this.dependencies.errorHandler.handleError(error, {
                context: 'view_switch',
                view: viewName,
                params
            });
        }
    }

    /**
     * Get application status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            version: this.version,
            mode: this.mode,
            currentView: this.currentView,
            components: Array.from(this.components.keys()),
            performance: { ...this.performanceMetrics },
            dependencies: Object.keys(this.dependencies)
        };
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return {
            ...this.performanceMetrics,
            ...this.dependencies.performanceMonitor.getMetrics()
        };
    }

    /**
     * Update application configuration
     */
    async updateConfig(newConfig) {
        try {
            await this.dependencies.configManager.update(newConfig);
            console.log('✅ Configuration updated');
        } catch (error) {
            console.error('❌ Failed to update configuration:', error);
            await this.dependencies.errorHandler.handleError(error, {
                context: 'config_update',
                config: newConfig
            });
        }
    }

    /**
     * Destroy the application and cleanup resources
     */
    async destroy() {
        console.log('🧹 Destroying V2 Swarm App...');

        try {
            // Destroy components
            for (const [name, component] of this.components) {
                if (component.destroy) {
                    await component.destroy();
                }
            }
            this.components.clear();

            // Destroy dependencies
            if (this.dependencies.websocketService.destroy) {
                await this.dependencies.websocketService.destroy();
            }
            if (this.dependencies.performanceMonitor.stop) {
                this.dependencies.performanceMonitor.stop();
            }

            // Reset state
            this.isInitialized = false;
            this.currentView = 'dashboard';

            console.log('✅ V2 Swarm App destroyed');

        } catch (error) {
            console.error('❌ Error during app destruction:', error);
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create V2 Swarm App with default dependencies
 */
export function createV2SwarmApp(options = {}) {
    return new V2SwarmApp(options);
}

/**
 * Create V2 Swarm App with custom dependencies
 */
export function createV2SwarmAppWithDependencies(dependencies, options = {}) {
    return new V2SwarmApp({ ...options, ...dependencies });
}

// ================================
// GLOBAL INITIALIZATION
// ================================

/**
 * Initialize application when DOM is ready
 */
function initializeApp() {
    const app = createV2SwarmApp();
    window.v2swarm = app;
    return app;
}

// Auto-initialize if DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Export for external access
export default V2SwarmApp;