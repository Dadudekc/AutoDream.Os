/**
 * Component Loader - V2 Compliant Component Loading System
 * V2 COMPLIANT: 150 lines maximum
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Dynamic component loading with dependency injection
 */

// ================================
// COMPONENT LOADER CLASS
// ================================

/**
 * Component Loader
 * Handles dynamic component loading and initialization
 */
export class ComponentLoader {
    constructor(options = {}) {
        this.components = new Map();
        this.loadingPromises = new Map();
        this.componentPaths = new Map();
        this.dependencies = options.dependencies || {};
        
        this.setupDefaultPaths();
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
    }

    /**
     * Load a component with dependency injection
     */
    async load(componentName, options = {}) {
        // Check if already loaded
        if (this.components.has(componentName)) {
            return this.components.get(componentName);
        }

        // Check if currently loading
        if (this.loadingPromises.has(componentName)) {
            return this.loadingPromises.get(componentName);
        }

        // Start loading
        const loadingPromise = this.loadComponent(componentName, options);
        this.loadingPromises.set(componentName, loadingPromise);

        try {
            const component = await loadingPromise;
            this.components.set(componentName, component);
            this.loadingPromises.delete(componentName);
            
            // Dispatch component loaded event
            window.dispatchEvent(new CustomEvent('component:loaded', {
                detail: { name: componentName, component }
            }));
            
            return component;
        } catch (error) {
            this.loadingPromises.delete(componentName);
            throw error;
        }
    }

    /**
     * Load component from module
     */
    async loadComponent(componentName, options) {
        const componentPath = this.componentPaths.get(componentName);
        if (!componentPath) {
            throw new Error(`Component path not found for: ${componentName}`);
        }

        try {
            // Dynamic import
            const module = await import(componentPath);
            const ComponentClass = module[componentName] || module.default;
            
            if (!ComponentClass) {
                throw new Error(`Component class not found: ${componentName}`);
            }

            // Create component instance with dependency injection
            const component = new ComponentClass({
                ...options,
                dependencies: { ...this.dependencies, ...options.dependencies }
            });

            return component;
        } catch (error) {
            console.error(`❌ Failed to load component ${componentName}:`, error);
            throw new Error(`Component loading failed: ${componentName} - ${error.message}`);
        }
    }

    /**
     * Preload components
     */
    async preload(componentNames) {
        const preloadPromises = componentNames.map(name => 
            this.load(name).catch(error => {
                console.warn(`⚠️ Preload failed for ${name}:`, error);
                return null;
            })
        );

        const results = await Promise.all(preloadPromises);
        return results.filter(component => component !== null);
    }

    /**
     * Get loaded component
     */
    get(componentName) {
        return this.components.get(componentName);
    }

    /**
     * Check if component is loaded
     */
    isLoaded(componentName) {
        return this.components.has(componentName);
    }

    /**
     * Unload component
     */
    async unload(componentName) {
        const component = this.components.get(componentName);
        if (component && component.destroy) {
            await component.destroy();
        }
        this.components.delete(componentName);
    }

    /**
     * Add component path
     */
    addComponentPath(name, path) {
        this.componentPaths.set(name, path);
    }

    /**
     * Get all loaded components
     */
    getLoadedComponents() {
        return Array.from(this.components.keys());
    }

    /**
     * Get component loading status
     */
    getLoadingStatus() {
        return {
            loaded: this.getLoadedComponents(),
            loading: Array.from(this.loadingPromises.keys()),
            available: Array.from(this.componentPaths.keys())
        };
    }
}

// ================================
// COMPONENT UTILITIES
// ================================

/**
 * Create component with dependency injection
 */
export function createComponent(ComponentClass, dependencies, options = {}) {
    return new ComponentClass({
        ...options,
        dependencies: { ...dependencies, ...options.dependencies }
    });
}

/**
 * Load multiple components in parallel
 */
export async function loadComponents(componentNames, loader, options = {}) {
    const loadPromises = componentNames.map(name => 
        loader.load(name, options)
    );
    
    return Promise.all(loadPromises);
}

/**
 * Preload critical components
 */
export async function preloadCriticalComponents(loader) {
    const criticalComponents = ['Navigation', 'Dashboard', 'AgentCoordinator'];
    return loader.preload(criticalComponents);
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create component loader with default settings
 */
export function createComponentLoader(options = {}) {
    return new ComponentLoader(options);
}

// Export default
export default ComponentLoader;