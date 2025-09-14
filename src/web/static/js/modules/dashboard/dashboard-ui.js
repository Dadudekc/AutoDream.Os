/**
 * Dashboard UI - V2 Compliant UI Management System
 * V2 COMPLIANT: 200 lines maximum
 * CONSOLIDATES: dashboard-ui-helpers.js, dashboard-navigation.js, dashboard-alerts.js
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Unified UI management with helpers, navigation, and alerts
 */

// ================================
// DASHBOARD UI CLASS
// ================================

/**
 * Dashboard UI Manager
 * Consolidates all UI functionality into a single manager
 */
export class DashboardUI {
    constructor(options = {}) {
        this.isInitialized = false;
        this.alerts = new Map();
        this.navigation = {
            currentView: 'overview',
            history: []
        };
        this.config = {
            alertTimeout: 5000,
            maxAlerts: 10,
            ...options
        };
    }

    /**
     * Initialize dashboard UI
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Dashboard UI already initialized');
            return;
        }

        console.log('🚀 Initializing Dashboard UI (V2 Compliant)...');

        try {
            // Setup UI event listeners
            this.setupUIEventListeners();

            // Initialize navigation
            this.initializeNavigation();

            // Initialize alerts system
            this.initializeAlerts();

            this.isInitialized = true;
            console.log('✅ Dashboard UI initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize dashboard UI:', error);
            throw error;
        }
    }

    /**
     * Setup UI event listeners
     */
    setupUIEventListeners() {
        // Navigation events
        document.addEventListener('click', (event) => {
            if (event.target.matches('.nav-btn')) {
                const view = event.target.dataset.view;
                this.handleNavigationClick(view);
            }
        });

        // Alert close events
        document.addEventListener('click', (event) => {
            if (event.target.matches('.alert-close')) {
                const alertId = event.target.dataset.alertId;
                this.closeAlert(alertId);
            }
        });
    }

    /**
     * Initialize navigation system
     */
    initializeNavigation() {
        console.log('🧭 Initializing navigation system...');
        
        // Set initial active navigation
        this.updateNavigation('overview');
        
        console.log('✅ Navigation system initialized');
    }

    /**
     * Initialize alerts system
     */
    initializeAlerts() {
        console.log('🔔 Initializing alerts system...');
        
        // Create alerts container if it doesn't exist
        this.createAlertsContainer();
        
        console.log('✅ Alerts system initialized');
    }

    /**
     * Handle navigation click
     */
    handleNavigationClick(view) {
        try {
            this.navigateTo(view);
        } catch (error) {
            console.error('❌ Navigation failed:', error);
            this.showAlert('error', 'Navigation failed');
        }
    }

    /**
     * Navigate to a view
     */
    navigateTo(view) {
        try {
            // Update navigation state
            this.navigation.history.push({
                view: this.navigation.currentView,
                timestamp: Date.now()
            });

            // Limit history size
            if (this.navigation.history.length > 10) {
                this.navigation.history.shift();
            }

            // Update current view
            this.navigation.currentView = view;

            // Update navigation UI
            this.updateNavigation(view);

            // Dispatch navigation event
            window.dispatchEvent(new CustomEvent('dashboard:navigate', {
                detail: { view, params: {} }
            }));

            console.log(`🧭 Navigated to: ${view}`);

        } catch (error) {
            console.error(`❌ Failed to navigate to ${view}:`, error);
            throw error;
        }
    }

    /**
     * Update navigation UI
     */
    updateNavigation(activeView) {
        // Update navigation buttons
        document.querySelectorAll('.nav-btn').forEach(btn => {
            const isActive = btn.dataset.view === activeView;
            btn.classList.toggle('active', isActive);
        });

        // Update view visibility
        document.querySelectorAll('.view').forEach(view => {
            const isActive = view.id === `${activeView}-view`;
            view.classList.toggle('active', isActive);
        });
    }

    /**
     * Show alert
     */
    showAlert(type, message, options = {}) {
        const alertId = this.generateAlertId();
        const alert = {
            id: alertId,
            type,
            message,
            timestamp: Date.now(),
            options
        };

        // Add to alerts map
        this.alerts.set(alertId, alert);

        // Create alert element
        this.createAlertElement(alert);

        // Auto-remove if not persistent
        if (!options.persistent) {
            setTimeout(() => {
                this.closeAlert(alertId);
            }, this.config.alertTimeout);
        }

        // Limit alerts count
        if (this.alerts.size > this.config.maxAlerts) {
            const firstAlert = this.alerts.keys().next().value;
            this.closeAlert(firstAlert);
        }

        console.log(`🔔 Alert shown: ${type} - ${message}`);
    }

    /**
     * Close alert
     */
    closeAlert(alertId) {
        const alert = this.alerts.get(alertId);
        if (!alert) return;

        // Remove from DOM
        const alertElement = document.getElementById(`alert-${alertId}`);
        if (alertElement) {
            alertElement.remove();
        }

        // Remove from alerts map
        this.alerts.delete(alertId);

        console.log(`🔔 Alert closed: ${alertId}`);
    }

    /**
     * Create alert element
     */
    createAlertElement(alert) {
        const alertsContainer = document.getElementById('alerts-container');
        if (!alertsContainer) return;

        const alertElement = document.createElement('div');
        alertElement.id = `alert-${alert.id}`;
        alertElement.className = `alert alert-${alert.type}`;
        alertElement.innerHTML = `
            <span class="alert-message">${alert.message}</span>
            <button class="alert-close" data-alert-id="${alert.id}">&times;</button>
        `;

        alertsContainer.appendChild(alertElement);
    }

    /**
     * Create alerts container
     */
    createAlertsContainer() {
        if (document.getElementById('alerts-container')) return;

        const container = document.createElement('div');
        container.id = 'alerts-container';
        container.className = 'alerts-container';
        document.body.appendChild(container);
    }

    /**
     * Show loading state
     */
    showLoadingState(elementId) {
        const element = document.getElementById(elementId);
        if (!element) return;

        element.classList.add('loading');
        
        // Create loading indicator if it doesn't exist
        if (!element.querySelector('.loading-indicator')) {
            const indicator = document.createElement('div');
            indicator.className = 'loading-indicator';
            indicator.innerHTML = '<div class="spinner"></div><span>Loading...</span>';
            element.appendChild(indicator);
        }
    }

    /**
     * Hide loading state
     */
    hideLoadingState(elementId) {
        const element = document.getElementById(elementId);
        if (!element) return;

        element.classList.remove('loading');
        
        // Remove loading indicator
        const indicator = element.querySelector('.loading-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    /**
     * Update current time
     */
    updateCurrentTime() {
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString();
        }
    }

    /**
     * Start time updates
     */
    startTimeUpdates() {
        this.updateCurrentTime();
        setInterval(() => {
            this.updateCurrentTime();
        }, 60000); // Update every minute
    }

    /**
     * Format percentage
     */
    formatPercentage(value) {
        return `${Math.round(value)}%`;
    }

    /**
     * Format number
     */
    formatNumber(value) {
        return new Intl.NumberFormat().format(value);
    }

    /**
     * Get status class
     */
    getStatusClass(status) {
        const statusClasses = {
            'active': 'status-active',
            'idle': 'status-idle',
            'error': 'status-error',
            'warning': 'status-warning'
        };
        return statusClasses[status] || 'status-unknown';
    }

    /**
     * Show error
     */
    showError(error, context = {}) {
        console.error('❌ Dashboard error:', error);
        
        this.showAlert('error', `Error: ${error.message || error}`, {
            persistent: true
        });
    }

    /**
     * Generate alert ID
     */
    generateAlertId() {
        return `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Get current view
     */
    getCurrentView() {
        return this.navigation.currentView;
    }

    /**
     * Get navigation history
     */
    getNavigationHistory() {
        return [...this.navigation.history];
    }

    /**
     * Get active alerts
     */
    getActiveAlerts() {
        return Array.from(this.alerts.values());
    }

    /**
     * Clear all alerts
     */
    clearAllAlerts() {
        this.alerts.forEach((alert, alertId) => {
            this.closeAlert(alertId);
        });
    }

    /**
     * Destroy dashboard UI
     */
    async destroy() {
        console.log('🧹 Destroying dashboard UI...');

        // Clear all alerts
        this.clearAllAlerts();

        // Clear navigation history
        this.navigation.history = [];

        // Remove alerts container
        const alertsContainer = document.getElementById('alerts-container');
        if (alertsContainer) {
            alertsContainer.remove();
        }

        this.isInitialized = false;

        console.log('✅ Dashboard UI destroyed');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create dashboard UI with default configuration
 */
export function createDashboardUI(options = {}) {
    return new DashboardUI(options);
}

// Export default
export default DashboardUI;