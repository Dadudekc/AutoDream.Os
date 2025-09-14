/**
 * Component Registry - V2 Compliant Component Management System
 * V2 COMPLIANT: 200 lines maximum
 * CONSOLIDATES: Component registration, loading, and management
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Unified component registry with registration, loading, and lifecycle management
 */

// ================================
// COMPONENT REGISTRY CLASS
// ================================

/**
 * Component Registry
 * Manages component registration, loading, and lifecycle
 */
export class ComponentRegistry {
    constructor(options = {}) {
        this.registeredComponents = new Map();
        this.loadedComponents = new Map();
        this.loadingPromises = new Map();
        this.componentPaths = new Map();
        this.dependencies = options.dependencies || {};
        this.isInitialized = false;
        this.config = {
            enableLazyLoading: true,
            enableDependencyInjection: true,
            enablePerformanceMonitoring: true,
            ...options.config
        };
    }

    /**
     * Initialize component registry
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Component registry already initialized');
            return;
        }

        console.log('🚀 Initializing Component Registry (V2 Compliant)...');

        try {
            // Setup default component paths
            this.setupDefaultPaths();

            // Register default components
            this.registerDefaultComponents();

            // Setup component event listeners
            this.setupComponentEventListeners();

            this.isInitialized = true;
            console.log('✅ Component Registry initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize component registry:', error);
            throw error;
        }
    }

    /**
     * Setup default component paths
     */
    setupDefaultPaths() {
        this.componentPaths.set('Navigation', './components/navigation.js');
        this.componentPaths.set('Dashboard', './components/dashboard.js');
        this.componentPaths.set('AgentCoordinator', './components/agent-coordinator.js');
        this.componentPaths.set('Analytics', './components/analytics.js');
        this.componentPaths.set('Settings', './components/settings.js');
        this.componentPaths.set('Performance', './components/performance.js');
        this.componentPaths.set('Monitoring', './components/monitoring.js');
    }

    /**
     * Register default components
     */
    registerDefaultComponents() {
        // Register built-in components
        this.register('BaseComponent', {
            path: './modules/components/base-component.js',
            type: 'base',
            dependencies: []
        });

        this.register('Navigation', {
            path: './components/navigation.js',
            type: 'ui',
            dependencies: ['BaseComponent']
        });

        this.register('Dashboard', {
            path: './components/dashboard.js',
            type: 'ui',
            dependencies: ['BaseComponent']
        });
    }

    /**
     * Setup component event listeners
     */
    setupComponentEventListeners() {
        // Listen for component load requests
        window.addEventListener('component:load', (event) => {
            this.handleLoadRequest(event.detail);
        });

        // Listen for component registration requests
        window.addEventListener('component:register', (event) => {
            this.handleRegistrationRequest(event.detail);
        });
    }

    /**
     * Register a component
     */
    register(name, config) {
        if (this.registeredComponents.has(name)) {
            console.warn(`⚠️ Component ${name} already registered`);
            return false;
        }

        const componentConfig = {
            name,
            path: config.path,
            type: config.type || 'ui',
            dependencies: config.dependencies || [],
            options: config.options || {},
            ...config
        };

        this.registeredComponents.set(name, componentConfig);
        console.log(`📋 Component registered: ${name}`);

        return true;
    }

    /**
     * Unregister a component
     */
    unregister(name) {
        if (!this.registeredComponents.has(name)) {
            console.warn(`⚠️ Component ${name} not registered`);
            return false;
        }

        this.registeredComponents.delete(name);
        console.log(`🗑️ Component unregistered: ${name}`);

        return true;
    }

    /**
     * Load a component
     */
    async load(name, options = {}) {
        // Check if already loaded
        if (this.loadedComponents.has(name)) {
            return this.loadedComponents.get(name);
        }

        // Check if currently loading
        if (this.loadingPromises.has(name)) {
            return this.loadingPromises.get(name);
        }

        // Check if component is registered
        if (!this.registeredComponents.has(name)) {
            throw new Error(`Component ${name} not registered`);
        }

        try {
            console.log(`📦 Loading component: ${name}`);

            // Create loading promise
            const loadingPromise = this.loadComponent(name, options);
            this.loadingPromises.set(name, loadingPromise);

            // Load component
            const component = await loadingPromise;

            // Store loaded component
            this.loadedComponents.set(name, component);

            // Remove from loading promises
            this.loadingPromises.delete(name);

            console.log(`✅ Component loaded: ${name}`);
            return component;

        } catch (error) {
            console.error(`❌ Failed to load component ${name}:`, error);
            this.loadingPromises.delete(name);
            throw error;
        }
    }

    /**
     * Load component implementation
     */
    async loadComponent(name, options) {
        const config = this.registeredComponents.get(name);
        
        // Load dependencies first
        if (this.config.enableDependencyInjection && config.dependencies.length > 0) {
            await this.loadDependencies(config.dependencies);
        }

        // Load component module
        const module = await this.loadModule(config.path);
        
        // Get component class
        const ComponentClass = module.default || module[config.exportName] || module[name];
        
        if (!ComponentClass) {
            throw new Error(`Component class not found in ${config.path}`);
        }

        // Create component instance
        const componentOptions = {
            ...config.options,
            ...options,
            dependencies: this.dependencies
        };

        const component = new ComponentClass(componentOptions);

        // Initialize component
        if (component.initialize) {
            await component.initialize();
        }

        return component;
    }

    /**
     * Load dependencies
     */
    async loadDependencies(dependencies) {
        const dependencyPromises = dependencies.map(dep => this.load(dep));
        await Promise.all(dependencyPromises);
    }

    /**
     * Load module
     */
    async loadModule(path) {
        try {
            const module = await import(path);
            return module;
        } catch (error) {
            console.error(`❌ Failed to load module ${path}:`, error);
            throw error;
        }
    }

    /**
     * Unload a component
     */
    async unload(name) {
        if (!this.loadedComponents.has(name)) {
            console.warn(`⚠️ Component ${name} not loaded`);
            return false;
        }

        try {
            const component = this.loadedComponents.get(name);

            // Destroy component
            if (component.destroy) {
                await component.destroy();
            }

            // Remove from loaded components
            this.loadedComponents.delete(name);

            console.log(`🗑️ Component unloaded: ${name}`);
            return true;

        } catch (error) {
            console.error(`❌ Failed to unload component ${name}:`, error);
            return false;
        }
    }

    /**
     * Get loaded component
     */
    get(name) {
        return this.loadedComponents.get(name);
    }

    /**
     * Check if component is loaded
     */
    isLoaded(name) {
        return this.loadedComponents.has(name);
    }

    /**
     * Check if component is registered
     */
    isRegistered(name) {
        return this.registeredComponents.has(name);
    }

    /**
     * Get all registered components
     */
    getRegisteredComponents() {
        return Array.from(this.registeredComponents.keys());
    }

    /**
     * Get all loaded components
     */
    getLoadedComponents() {
        return Array.from(this.loadedComponents.keys());
    }

    /**
     * Handle load request
     */
    async handleLoadRequest(data) {
        const { name, options, callback } = data;
        
        try {
            const component = await this.load(name, options);
            
            if (callback) {
                callback(null, component);
            }
            
            return component;
        } catch (error) {
            if (callback) {
                callback(error, null);
            }
            throw error;
        }
    }

    /**
     * Handle registration request
     */
    handleRegistrationRequest(data) {
        const { name, config, callback } = data;
        
        try {
            const success = this.register(name, config);
            
            if (callback) {
                callback(null, success);
            }
            
            return success;
        } catch (error) {
            if (callback) {
                callback(error, false);
            }
            throw error;
        }
    }

    /**
     * Get component info
     */
    getComponentInfo(name) {
        const registered = this.registeredComponents.get(name);
        const loaded = this.loadedComponents.get(name);
        
        return {
            name,
            registered: !!registered,
            loaded: !!loaded,
            config: registered,
            component: loaded
        };
    }

    /**
     * Get registry status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            registered: this.registeredComponents.size,
            loaded: this.loadedComponents.size,
            loading: this.loadingPromises.size,
            config: { ...this.config }
        };
    }

    /**
     * Destroy component registry
     */
    async destroy() {
        console.log('🧹 Destroying component registry...');

        // Unload all components
        const unloadPromises = Array.from(this.loadedComponents.keys()).map(name => this.unload(name));
        await Promise.all(unloadPromises);

        // Clear collections
        this.registeredComponents.clear();
        this.loadedComponents.clear();
        this.loadingPromises.clear();
        this.componentPaths.clear();

        this.isInitialized = false;

        console.log('✅ Component registry destroyed');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create component registry with default configuration
 */
export function createComponentRegistry(options = {}) {
    return new ComponentRegistry(options);
}

// Export default
export default ComponentRegistry;