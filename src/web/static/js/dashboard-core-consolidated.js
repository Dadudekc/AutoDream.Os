/**
 * Dashboard Core Consolidated Module - V2 Compliant
 * Consolidates all individual dashboard files into unified core modules
 * Combines dashboard-core.js, dashboard-main.js, dashboard.js, and related modules
 *
 * @author Agent-7 - Web Development Specialist
 * @version 3.0.0 - PHASE 2 FINAL CONSOLIDATION
 * @license MIT
 */

// ================================
// DASHBOARD CORE CONSOLIDATION
// ================================

/**
 * Unified Dashboard Core Module
 * Consolidates all dashboard functionality into V2-compliant modules
 */
export class DashboardCoreConsolidated {
    constructor(options = {}) {
        this.logger = console;
        this.isInitialized = false;

        // Core dashboard components
        this.stateManager = null;
        this.configManager = null;
        this.dataManager = null;
        this.uiManager = null;
        this.viewManager = null;
        this.communicationManager = null;
        this.errorHandler = null;

        // Configuration
        this.config = {
            enableRealTimeUpdates: true,
            enableNotifications: true,
            refreshInterval: 30000,
            maxDataPoints: 100,
            autoSave: true,
            ...options
        };

        // State
        this.currentView = 'overview';
        this.isLoading = false;
        this.lastUpdate = null;
        this.modules = new Map();
    }

    /**
     * Initialize the consolidated dashboard core
     */
    async initialize() {
        try {
            this.logger.log('🚀 Initializing Dashboard Core Consolidated...');

            // Initialize core components
            await this.initializeCoreComponents();

            // Setup communication and coordination
            this.setupCommunication();

            // Initialize views
            await this.initializeViews();

            // Setup event handlers
            this.setupEventHandlers();

            this.isInitialized = true;
            this.logger.log('✅ Dashboard Core Consolidated initialized successfully');

        } catch (error) {
            this.logger.error('❌ Dashboard Core Consolidated initialization failed:', error);
            throw error;
        }
    }

    /**
     * Initialize core dashboard components
     */
    async initializeCoreComponents() {
        // State Manager (from dashboard-state-manager.js)
        this.stateManager = new DashboardStateManager(this.config);

        // Config Manager (from dashboard-config-manager.js)
        this.configManager = new DashboardConfigManager(this.config);

        // Data Manager (from dashboard-data-manager.js)
        this.dataManager = new DashboardDataManager(this.config);

        // UI Manager (from dashboard-ui-helpers.js)
        this.uiManager = new DashboardUIManager(this.config);

        // View Manager (from dashboard-views.js)
        this.viewManager = new DashboardViewManager(this.config);

        // Communication Manager (from dashboard-communication.js)
        this.communicationManager = new DashboardCommunicationManager(this.config);

        // Error Handler (from dashboard-error-handler.js)
        this.errorHandler = new DashboardErrorHandler(this.config);

        // Initialize all components
        await Promise.all([
            this.stateManager.initialize(),
            this.configManager.initialize(),
            this.dataManager.initialize(),
            this.uiManager.initialize(),
            this.viewManager.initialize(),
            this.communicationManager.initialize(),
            this.errorHandler.initialize()
        ]);
    }

    /**
     * Setup communication between components
     */
    setupCommunication() {
        // Data manager ↔ State manager
        this.dataManager.on('dataUpdated', (data) => {
            this.stateManager.updateState({ data });
        });

        // Communication manager ↔ Data manager
        this.communicationManager.on('messageReceived', (message) => {
            this.dataManager.processMessage(message);
        });

        // Error handler ↔ All components
        this.setupErrorHandling();
    }

    /**
     * Setup error handling across all components
     */
    setupErrorHandling() {
        const components = [
            this.stateManager,
            this.configManager,
            this.dataManager,
            this.uiManager,
            this.viewManager,
            this.communicationManager
        ];

        components.forEach(component => {
            if (component && typeof component.on === 'function') {
                component.on('error', (error) => {
                    this.errorHandler.handleError(error, component.constructor.name);
                });
            }
        });
    }

    /**
     * Initialize dashboard views
     */
    async initializeViews() {
        // Overview view
        await this.viewManager.registerView('overview', {
            template: 'overview-template',
            controller: new DashboardOverviewController(this)
        });

        // Performance view
        await this.viewManager.registerView('performance', {
            template: 'performance-template',
            controller: new DashboardPerformanceController(this)
        });

        // Trading view
        await this.viewManager.registerView('trading', {
            template: 'trading-template',
            controller: new DashboardTradingController(this)
        });
    }

    /**
     * Setup event handlers
     */
    setupEventHandlers() {
        // Window resize handler
        window.addEventListener('resize', this.handleResize.bind(this));

        // Visibility change handler
        document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));

        // Online/offline handlers
        window.addEventListener('online', this.handleOnline.bind(this));
        window.addEventListener('offline', this.handleOffline.bind(this));
    }

    /**
     * Handle window resize
     */
    handleResize() {
        this.viewManager.resizeViews();
        this.uiManager.updateLayout();
    }

    /**
     * Handle visibility change
     */
    handleVisibilityChange() {
        if (document.hidden) {
            this.pauseUpdates();
        } else {
            this.resumeUpdates();
        }
    }

    /**
     * Handle online status
     */
    handleOnline() {
        this.communicationManager.reconnect();
        this.showNotification('Connection restored', 'success');
    }

    /**
     * Handle offline status
     */
    handleOffline() {
        this.showNotification('Connection lost', 'warning');
    }

    /**
     * Navigate to a specific view
     */
    async navigateToView(viewName, options = {}) {
        try {
            await this.viewManager.switchToView(viewName, options);
            this.currentView = viewName;
            this.stateManager.updateState({ currentView: viewName });
            this.logger.log(`Navigated to view: ${viewName}`);
        } catch (error) {
            this.errorHandler.handleError(error, 'Navigation');
        }
    }

    /**
     * Load dashboard data
     */
    async loadData(viewName, options = {}) {
        try {
            this.isLoading = true;
            this.uiManager.showLoadingState();

            const data = await this.dataManager.loadData(viewName, options);
            await this.viewManager.updateViewData(viewName, data);

            this.lastUpdate = new Date();
            this.stateManager.updateState({
                lastUpdate: this.lastUpdate,
                dataLoaded: true
            });

        } catch (error) {
            this.errorHandler.handleError(error, 'Data Loading');
        } finally {
            this.isLoading = false;
            this.uiManager.hideLoadingState();
        }
    }

    /**
     * Refresh current view
     */
    async refreshCurrentView() {
        await this.loadData(this.currentView, { forceRefresh: true });
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        this.uiManager.showAlert(message, type);
    }

    /**
     * Pause real-time updates
     */
    pauseUpdates() {
        this.communicationManager.pause();
        this.logger.log('Dashboard updates paused');
    }

    /**
     * Resume real-time updates
     */
    resumeUpdates() {
        this.communicationManager.resume();
        this.logger.log('Dashboard updates resumed');
    }

    /**
     * Get dashboard status
     */
    getStatus() {
        return {
            isInitialized: this.isInitialized,
            currentView: this.currentView,
            isLoading: this.isLoading,
            lastUpdate: this.lastUpdate,
            connectionStatus: this.communicationManager?.getStatus(),
            errorCount: this.errorHandler?.getErrorCount() || 0,
            dataPoints: this.dataManager?.getDataPointCount() || 0
        };
    }

    /**
     * Destroy dashboard and cleanup
     */
    destroy() {
        this.logger.log('Destroying Dashboard Core Consolidated...');

        // Pause updates
        this.pauseUpdates();

        // Destroy components
        const components = [
            this.stateManager,
            this.configManager,
            this.dataManager,
            this.uiManager,
            this.viewManager,
            this.communicationManager,
            this.errorHandler
        ];

        components.forEach(component => {
            if (component && typeof component.destroy === 'function') {
                component.destroy();
            }
        });

        // Clear modules
        this.modules.clear();

        // Remove event listeners
        window.removeEventListener('resize', this.handleResize);
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
        window.removeEventListener('online', this.handleOnline);
        window.removeEventListener('offline', this.handleOffline);

        this.isInitialized = false;
        this.logger.log('Dashboard Core Consolidated destroyed');
    }
}

// ================================
// COMPONENT CLASSES
// ================================

/**
 * Dashboard State Manager - Consolidated from dashboard-state-manager.js
 */
class DashboardStateManager {
    constructor(config) {
        this.config = config;
        this.state = {};
        this.listeners = new Map();
    }

    async initialize() {
        this.state = {
            currentView: 'overview',
            dataLoaded: false,
            lastUpdate: null,
            userPreferences: {},
            sessionData: {}
        };
    }

    updateState(updates) {
        Object.assign(this.state, updates);
        this.notifyListeners('stateChanged', this.state);
    }

    getState() {
        return { ...this.state };
    }

    subscribe(event, listener) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(listener);
    }

    notifyListeners(event, data) {
        const listeners = this.listeners.get(event) || [];
        listeners.forEach(listener => listener(data));
    }

    destroy() {
        this.listeners.clear();
    }
}

/**
 * Dashboard Config Manager - Consolidated from dashboard-config-manager.js
 */
class DashboardConfigManager {
    constructor(config) {
        this.config = config;
        this.userConfig = {};
    }

    async initialize() {
        // Load user configuration from storage
        this.userConfig = await this.loadUserConfig();
    }

    async loadUserConfig() {
        try {
            const stored = localStorage.getItem('dashboard-config');
            return stored ? JSON.parse(stored) : {};
        } catch (error) {
            console.warn('Failed to load user config:', error);
            return {};
        }
    }

    getConfig(key = null) {
        if (key) {
            return this.userConfig[key] || this.config[key];
        }
        return { ...this.config, ...this.userConfig };
    }

    async updateConfig(updates) {
        Object.assign(this.userConfig, updates);
        await this.saveUserConfig();
        return this.getConfig();
    }

    async saveUserConfig() {
        try {
            localStorage.setItem('dashboard-config', JSON.stringify(this.userConfig));
        } catch (error) {
            console.warn('Failed to save user config:', error);
        }
    }

    destroy() {
        // Cleanup if needed
    }
}

/**
 * Dashboard Data Manager - Consolidated from dashboard-data-manager.js
 */
class DashboardDataManager {
    constructor(config) {
        this.config = config;
        this.dataCache = new Map();
        this.listeners = new Map();
    }

    async initialize() {
        // Setup data cache cleanup
        setInterval(() => {
            this.cleanupExpiredCache();
        }, 60000); // Clean every minute
    }

    async loadData(viewName, options = {}) {
        const cacheKey = `${viewName}_${JSON.stringify(options)}`;

        if (!options.forceRefresh) {
            const cached = this.getCachedData(cacheKey);
            if (cached) {
                return cached;
            }
        }

        // Simulate data loading
        const data = await this.fetchData(viewName, options);

        this.setCachedData(cacheKey, data);
        this.notifyListeners('dataUpdated', data);

        return data;
    }

    async fetchData(viewName, options) {
        // Placeholder for actual data fetching logic
        return {
            view: viewName,
            timestamp: new Date().toISOString(),
            data: [],
            metadata: { count: 0, lastUpdate: new Date() }
        };
    }

    getCachedData(cacheKey) {
        const cached = this.dataCache.get(cacheKey);
        if (cached && Date.now() - cached.timestamp < 300000) { // 5 minutes
            return cached.data;
        }
        return null;
    }

    setCachedData(cacheKey, data) {
        this.dataCache.set(cacheKey, {
            data: data,
            timestamp: Date.now()
        });
    }

    cleanupExpiredCache() {
        const cutoff = Date.now() - 300000; // 5 minutes
        const expiredKeys = [];

        for (const [key, cached] of this.dataCache.entries()) {
            if (cached.timestamp < cutoff) {
                expiredKeys.push(key);
            }
        }

        expiredKeys.forEach(key => this.dataCache.delete(key));
    }

    subscribe(event, listener) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(listener);
    }

    notifyListeners(event, data) {
        const listeners = this.listeners.get(event) || [];
        listeners.forEach(listener => listener(data));
    }

    destroy() {
        this.dataCache.clear();
        this.listeners.clear();
    }
}

/**
 * Dashboard UI Manager - Consolidated from dashboard-ui-helpers.js
 */
class DashboardUIManager {
    constructor(config) {
        this.config = config;
        this.alertContainer = null;
    }

    async initialize() {
        // Create alert container
        this.alertContainer = document.createElement('div');
        this.alertContainer.id = 'dashboard-alerts';
        this.alertContainer.className = 'dashboard-alerts-container';
        document.body.appendChild(this.alertContainer);
    }

    showAlert(message, type = 'info') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;

        this.alertContainer.appendChild(alert);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 5000);
    }

    showLoadingState() {
        const loader = document.createElement('div');
        loader.id = 'dashboard-loader';
        loader.className = 'dashboard-loading-overlay';
        loader.innerHTML = '<div class="spinner"></div><div>Loading...</div>';
        document.body.appendChild(loader);
    }

    hideLoadingState() {
        const loader = document.getElementById('dashboard-loader');
        if (loader) {
            loader.parentNode.removeChild(loader);
        }
    }

    updateLayout() {
        // Handle responsive layout updates
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        // Update layout based on viewport size
        document.documentElement.style.setProperty('--viewport-width', `${viewportWidth}px`);
        document.documentElement.style.setProperty('--viewport-height', `${viewportHeight}px`);
    }

    destroy() {
        if (this.alertContainer && this.alertContainer.parentNode) {
            this.alertContainer.parentNode.removeChild(this.alertContainer);
        }
    }
}

/**
 * Dashboard View Manager - Consolidated from dashboard-views.js
 */
class DashboardViewManager {
    constructor(config) {
        this.config = config;
        this.views = new Map();
        this.currentView = null;
    }

    async initialize() {
        // Initialize view containers
        this.setupViewContainers();
    }

    setupViewContainers() {
        // Create main view container
        const container = document.createElement('div');
        container.id = 'dashboard-views-container';
        container.className = 'dashboard-views';

        // Create view containers for each view type
        ['overview', 'performance', 'trading'].forEach(viewName => {
            const viewContainer = document.createElement('div');
            viewContainer.id = `dashboard-view-${viewName}`;
            viewContainer.className = 'dashboard-view';
            viewContainer.style.display = 'none';
            container.appendChild(viewContainer);
        });

        document.body.appendChild(container);
    }

    async registerView(viewName, viewConfig) {
        this.views.set(viewName, viewConfig);
    }

    async switchToView(viewName, options = {}) {
        const viewConfig = this.views.get(viewName);
        if (!viewConfig) {
            throw new Error(`View not found: ${viewName}`);
        }

        // Hide current view
        if (this.currentView) {
            const currentContainer = document.getElementById(`dashboard-view-${this.currentView}`);
            if (currentContainer) {
                currentContainer.style.display = 'none';
            }
        }

        // Show new view
        const newContainer = document.getElementById(`dashboard-view-${viewName}`);
        if (newContainer) {
            newContainer.style.display = 'block';
        }

        this.currentView = viewName;

        // Initialize view controller if needed
        if (viewConfig.controller && typeof viewConfig.controller.initialize === 'function') {
            await viewConfig.controller.initialize(options);
        }
    }

    async updateViewData(viewName, data) {
        const viewConfig = this.views.get(viewName);
        if (viewConfig && viewConfig.controller && typeof viewConfig.controller.updateData === 'function') {
            await viewConfig.controller.updateData(data);
        }
    }

    resizeViews() {
        // Handle view resizing
        const containers = document.querySelectorAll('.dashboard-view');
        containers.forEach(container => {
            // Adjust view dimensions based on available space
            const rect = container.getBoundingClientRect();
            // Resize logic here
        });
    }

    destroy() {
        this.views.clear();
        const container = document.getElementById('dashboard-views-container');
        if (container) {
            container.parentNode.removeChild(container);
        }
    }
}

/**
 * Dashboard Communication Manager - Consolidated from dashboard-communication.js
 */
class DashboardCommunicationManager {
    constructor(config) {
        this.config = config;
        this.websocket = null;
        this.isConnected = false;
        this.listeners = new Map();
        this.messageQueue = [];
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.isPaused = false;
    }

    async initialize() {
        if (this.config.enableRealTimeUpdates) {
            await this.connect();
        }
    }

    async connect() {
        try {
            this.websocket = new WebSocket('ws://localhost:8080/dashboard');

            this.websocket.onopen = () => {
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.processMessageQueue();
                this.notifyListeners('connected');
            };

            this.websocket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                this.notifyListeners('messageReceived', message);
            };

            this.websocket.onclose = () => {
                this.isConnected = false;
                this.notifyListeners('disconnected');

                if (!this.isPaused) {
                    this.attemptReconnection();
                }
            };

            this.websocket.onerror = (error) => {
                this.notifyListeners('error', error);
            };

        } catch (error) {
            console.error('Failed to connect to dashboard WebSocket:', error);
            throw error;
        }
    }

    sendMessage(message) {
        if (this.isConnected && !this.isPaused) {
            this.websocket.send(JSON.stringify(message));
        } else {
            this.messageQueue.push(message);
        }
    }

    pause() {
        this.isPaused = true;
    }

    resume() {
        this.isPaused = false;
        if (this.isConnected) {
            this.processMessageQueue();
        }
    }

    processMessageQueue() {
        while (this.messageQueue.length > 0 && this.isConnected && !this.isPaused) {
            const message = this.messageQueue.shift();
            this.sendMessage(message);
        }
    }

    async attemptReconnection() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached');
            return;
        }

        this.reconnectAttempts++;
        const delay = 1000 * this.reconnectAttempts;

        setTimeout(async () => {
            try {
                await this.connect();
            } catch (error) {
                console.error('Reconnection failed:', error);
            }
        }, delay);
    }

    subscribe(event, listener) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(listener);
    }

    notifyListeners(event, data) {
        const listeners = this.listeners.get(event) || [];
        listeners.forEach(listener => listener(data));
    }

    getStatus() {
        return {
            isConnected: this.isConnected,
            isPaused: this.isPaused,
            reconnectAttempts: this.reconnectAttempts,
            queuedMessages: this.messageQueue.length
        };
    }

    reconnect() {
        if (!this.isConnected) {
            this.connect();
        }
    }

    destroy() {
        if (this.websocket) {
            this.websocket.close();
        }
        this.listeners.clear();
        this.messageQueue = [];
    }
}

/**
 * Dashboard Error Handler - Consolidated from dashboard-error-handler.js
 */
class DashboardErrorHandler {
    constructor(config) {
        this.config = config;
        this.errors = [];
        this.listeners = new Map();
    }

    async initialize() {
        // Setup global error handlers
        window.addEventListener('error', this.handleGlobalError.bind(this));
        window.addEventListener('unhandledrejection', this.handleUnhandledRejection.bind(this));
    }

    handleError(error, context = 'Unknown') {
        const errorEntry = {
            timestamp: new Date().toISOString(),
            error: error.message || error,
            stack: error.stack,
            context: context,
            userAgent: navigator.userAgent,
            url: window.location.href
        };

        this.errors.push(errorEntry);

        // Keep only last 100 errors
        if (this.errors.length > 100) {
            this.errors.shift();
        }

        // Log error
        console.error(`Dashboard Error [${context}]:`, error);

        // Show user-friendly error message
        this.showErrorNotification(error, context);

        // Notify listeners
        this.notifyListeners('errorOccurred', errorEntry);
    }

    handleGlobalError(event) {
        this.handleError(event.error, 'Global');
    }

    handleUnhandledRejection(event) {
        this.handleError(event.reason, 'Unhandled Promise Rejection');
    }

    showErrorNotification(error, context) {
        // Create user-friendly error message
        let message = 'An error occurred. Please try again.';

        if (context === 'Network') {
            message = 'Connection error. Please check your internet connection.';
        } else if (context === 'Data Loading') {
            message = 'Failed to load data. Please refresh the page.';
        }

        // Show notification (would integrate with UI manager)
        console.warn(`User notification: ${message}`);
    }

    getErrors(limit = 10) {
        return this.errors.slice(-limit);
    }

    getErrorCount() {
        return this.errors.length;
    }

    subscribe(event, listener) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(listener);
    }

    notifyListeners(event, data) {
        const listeners = this.listeners.get(event) || [];
        listeners.forEach(listener => listener(data));
    }

    clearErrors() {
        this.errors = [];
    }

    destroy() {
        window.removeEventListener('error', this.handleGlobalError);
        window.removeEventListener('unhandledrejection', this.handleUnhandledRejection);
        this.listeners.clear();
        this.errors = [];
    }
}

// ================================
// VIEW CONTROLLERS
// ================================

/**
 * Dashboard Overview Controller
 */
class DashboardOverviewController {
    constructor(dashboardCore) {
        this.dashboardCore = dashboardCore;
    }

    async initialize(options) {
        // Initialize overview view
        console.log('Initializing overview view');
    }

    async updateData(data) {
        // Update overview data
        console.log('Updating overview data');
    }
}

/**
 * Dashboard Performance Controller
 */
class DashboardPerformanceController {
    constructor(dashboardCore) {
        this.dashboardCore = dashboardCore;
    }

    async initialize(options) {
        // Initialize performance view
        console.log('Initializing performance view');
    }

    async updateData(data) {
        // Update performance data
        console.log('Updating performance data');
    }
}

/**
 * Dashboard Trading Controller
 */
class DashboardTradingController {
    constructor(dashboardCore) {
        this.dashboardCore = dashboardCore;
    }

    async initialize(options) {
        // Initialize trading view
        console.log('Initializing trading view');
    }

    async updateData(data) {
        // Update trading data
        console.log('Updating trading data');
    }
}

// ================================
// EXPORTS
// ================================

export {
    DashboardCoreConsolidated,
    DashboardStateManager,
    DashboardConfigManager,
    DashboardDataManager,
    DashboardUIManager,
    DashboardViewManager,
    DashboardCommunicationManager,
    DashboardErrorHandler,
    DashboardOverviewController,
    DashboardPerformanceController,
    DashboardTradingController
};
