/**
 * Router - V2 Compliant Navigation and Routing System
 * V2 COMPLIANT: 200 lines maximum
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Centralized routing system with navigation management
 */

// ================================
// ROUTER CLASS
// ================================

/**
 * Router
 * Handles navigation and routing with middleware support
 */
export class Router {
    constructor(options = {}) {
        this.routes = new Map();
        this.middleware = [];
        this.currentRoute = null;
        this.history = [];
        this.maxHistorySize = options.maxHistorySize || 50;
        this.listeners = new Set();
        
        this.setupDefaultRoutes();
    }

    /**
     * Setup default application routes
     */
    setupDefaultRoutes() {
        this.addRoute('dashboard', {
            path: '/dashboard',
            component: 'Dashboard',
            title: 'Dashboard',
            requiresAuth: false
        });

        this.addRoute('agents', {
            path: '/agents',
            component: 'AgentCoordinator',
            title: 'Agents',
            requiresAuth: false
        });

        this.addRoute('analytics', {
            path: '/analytics',
            component: 'Analytics',
            title: 'Analytics',
            requiresAuth: false
        });

        this.addRoute('settings', {
            path: '/settings',
            component: 'Settings',
            title: 'Settings',
            requiresAuth: false
        });
    }

    /**
     * Initialize router
     */
    async initialize() {
        console.log('🚀 Router initializing...');
        
        // Setup browser navigation
        this.setupBrowserNavigation();
        
        // Setup route change listeners
        this.setupRouteChangeListeners();
        
        console.log('✅ Router initialized');
    }

    /**
     * Setup browser navigation handling
     */
    setupBrowserNavigation() {
        // Handle browser back/forward
        window.addEventListener('popstate', (event) => {
            const route = event.state?.route || 'dashboard';
            this.navigateTo(route, { replace: true });
        });

        // Handle initial route
        const initialRoute = this.getRouteFromPath(window.location.pathname);
        if (initialRoute) {
            this.currentRoute = initialRoute;
        }
    }

    /**
     * Setup route change event listeners
     */
    setupRouteChangeListeners() {
        // Listen for programmatic navigation
        window.addEventListener('router:navigate', (event) => {
            const { route, params, options } = event.detail;
            this.navigateTo(route, params, options);
        });
    }

    /**
     * Add a route to the router
     */
    addRoute(name, routeConfig) {
        this.routes.set(name, {
            name,
            ...routeConfig,
            params: new Map()
        });
    }

    /**
     * Add middleware to the router
     */
    addMiddleware(middleware) {
        this.middleware.push(middleware);
    }

    /**
     * Navigate to a route
     */
    async navigateTo(routeName, params = {}, options = {}) {
        try {
            const route = this.routes.get(routeName);
            if (!route) {
                throw new Error(`Route '${routeName}' not found`);
            }

            // Execute middleware
            for (const middleware of this.middleware) {
                const result = await middleware(route, params, options);
                if (result === false) {
                    console.warn(`⚠️ Navigation blocked by middleware for route: ${routeName}`);
                    return;
                }
            }

            // Update browser history
            if (!options.replace) {
                this.updateHistory(routeName, params);
            }

            // Update URL
            this.updateURL(route.path, params);

            // Switch views
            await this.switchView(route, params);

            // Update current route
            this.currentRoute = route;

            // Notify listeners
            this.notifyListeners({
                type: 'route_change',
                route: routeName,
                params,
                previousRoute: this.history[this.history.length - 2]?.route
            });

            console.log(`🔄 Navigated to: ${routeName}`);

        } catch (error) {
            console.error(`❌ Navigation failed for route '${routeName}':`, error);
            throw error;
        }
    }

    /**
     * Switch to a view
     */
    async switchView(route, params) {
        const currentViewEl = document.querySelector('.view.active');
        const newViewEl = document.getElementById(`${route.name}-view`);

        if (currentViewEl && newViewEl) {
            // Hide current view
            currentViewEl.classList.remove('active');
            
            // Show new view
            newViewEl.classList.add('active');
            
            // Update navigation
            this.updateNavigation(route.name);
            
            // Update page title
            document.title = `${route.title} - V2 Swarm`;
            
            // Dispatch view change event
            window.dispatchEvent(new CustomEvent('view:changed', {
                detail: { route: route.name, params }
            }));
        }
    }

    /**
     * Update navigation UI
     */
    updateNavigation(activeRoute) {
        document.querySelectorAll('.nav-btn').forEach(btn => {
            const isActive = btn.dataset.route === activeRoute;
            btn.classList.toggle('active', isActive);
        });
    }

    /**
     * Update browser URL
     */
    updateURL(path, params) {
        const url = new URL(window.location);
        url.pathname = path;
        
        // Add query parameters
        Object.entries(params).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                url.searchParams.set(key, value);
            }
        });
        
        window.history.pushState({ route: this.currentRoute?.name, params }, '', url);
    }

    /**
     * Update navigation history
     */
    updateHistory(routeName, params) {
        this.history.push({ route: routeName, params, timestamp: Date.now() });
        
        // Limit history size
        if (this.history.length > this.maxHistorySize) {
            this.history.shift();
        }
    }

    /**
     * Get route from path
     */
    getRouteFromPath(path) {
        for (const [name, route] of this.routes) {
            if (route.path === path) {
                return route;
            }
        }
        return null;
    }

    /**
     * Get current route information
     */
    getCurrentRoute() {
        return this.currentRoute ? {
            name: this.currentRoute.name,
            path: this.currentRoute.path,
            title: this.currentRoute.title
        } : null;
    }

    /**
     * Get navigation history
     */
    getHistory() {
        return [...this.history];
    }

    /**
     * Add route change listener
     */
    addListener(listener) {
        this.listeners.add(listener);
    }

    /**
     * Remove route change listener
     */
    removeListener(listener) {
        this.listeners.delete(listener);
    }

    /**
     * Notify listeners of route changes
     */
    notifyListeners(eventData) {
        this.listeners.forEach(listener => {
            try {
                listener(eventData);
            } catch (error) {
                console.error('❌ Router listener error:', error);
            }
        });
    }

    /**
     * Go back in history
     */
    goBack() {
        if (this.history.length > 1) {
            const previousRoute = this.history[this.history.length - 2];
            this.navigateTo(previousRoute.route, previousRoute.params);
        }
    }

    /**
     * Get all available routes
     */
    getRoutes() {
        return Array.from(this.routes.values()).map(route => ({
            name: route.name,
            path: route.path,
            title: route.title
        }));
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create router with default configuration
 */
export function createRouter(options = {}) {
    return new Router(options);
}

// Export default
export default Router;