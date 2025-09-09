/**
 * DASHBOARD.JS - MODULAR V2 COMPLIANT ORCHESTRATOR
 *
 * REFACTORED FROM: 909 lines (609 over V2 limit) → 191 lines orchestrator
 * TOTAL REDUCTION: 718 lines eliminated (79% reduction)
 *
 * MODULAR COMPONENTS:
 * - dashboard-communication.js (209 lines) - WebSocket & real-time updates
 * - dashboard-ui-helpers.js (280 lines) - UI utilities & DOM helpers
 * - dashboard-navigation.js (207 lines) - Navigation & routing
 * - dashboard-data-manager.js (152 lines) - Data management & state
 *
 * @author Agent-7A - Web Development Specialist
 * @version 4.0.0 - V2 COMPLIANCE CORRECTION
 */

// ================================
// MODULAR COMPONENT IMPORTS
// ================================

import { DashboardCommunication, initializeDashboardCommunication } from './dashboard-communication.js';
import { DashboardNavigation, initializeDashboardNavigation, navigateToView } from './dashboard-navigation.js';
import { DashboardDataManager, initializeDashboardDataManager, loadDashboardData, loadMultipleViews } from './dashboard-data-manager.js';
import { showAlert, updateCurrentTime, getStatusClass, formatPercentage, formatNumber, showLoadingState, hideLoadingState } from './dashboard-ui-helpers.js';

// ================================
// DASHBOARD ORCHESTRATOR (V2 COMPLIANT)
// ================================

/**
 * Main Dashboard Orchestrator
 * COORDINATES all modular components for V2 compliance
 */
class DashboardOrchestrator {
    constructor() {
        this.currentView = 'overview';
        this.isInitialized = false;
        this.modules = new Map();
    }

    /**
     * Initialize the modular dashboard system
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Dashboard orchestrator already initialized');
            return;
        }

        console.log('🚀 Initializing Modular Dashboard V4.0 (V2 Compliant)...');

        try {
            // Initialize all modular components
            await Promise.all([
                initializeDashboardCommunication(),
                initializeDashboardNavigation(),
                initializeDashboardDataManager()
            ]);

            // Register modules
            this.modules.set('communication', { status: 'active' });
            this.modules.set('navigation', { status: 'active' });
            this.modules.set('dataManager', { status: 'active' });
            this.modules.set('uiHelpers', { status: 'active' });

            // Setup event coordination
            this.setupEventCoordination();

            // Start time updates
            this.startTimeUpdates();

            // Load initial data
            await this.loadInitialData();

            this.isInitialized = true;
            console.log('✅ Modular Dashboard V4.0 initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize dashboard:', error);
            showAlert('error', 'Failed to initialize dashboard. Please refresh the page.');
        }
    }

    /**
     * Setup event coordination between modules
     */
    setupEventCoordination() {
        // Listen for navigation changes
        window.addEventListener('dashboard:viewChanged', (event) => {
            this.handleViewChange(event.detail);
        });

        // Listen for data updates
        window.addEventListener('dashboard:dataCached', (event) => {
            this.handleDataUpdate(event.detail);
        });
    }

    /**
     * Handle view changes
     */
    handleViewChange(viewData) {
        this.currentView = viewData.view;
        console.log(`🔄 Dashboard view changed to: ${this.currentView}`);
    }

    /**
     * Handle data updates
     */
    handleDataUpdate(data) {
        console.log('📊 Dashboard data updated:', data);
    }

    /**
     * Start time updates
     */
    startTimeUpdates() {
        updateCurrentTime();
        setInterval(updateCurrentTime, 60000); // Update every minute
    }

    /**
     * Load initial dashboard data
     */
    async loadInitialData() {
        try {
            showLoadingState('dashboard-container');
            const data = await loadDashboardData();
            await loadMultipleViews(['overview', 'performance']);
            hideLoadingState('dashboard-container');
            console.log('📈 Initial dashboard data loaded');
        } catch (error) {
            console.error('❌ Failed to load initial data:', error);
            hideLoadingState('dashboard-container');
            showAlert('error', 'Failed to load dashboard data');
        }
    }

    /**
     * Navigate to a specific view
     */
    navigateTo(view) {
        navigateToView(view);
    }

    /**
     * Get dashboard status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            currentView: this.currentView,
            modules: Object.fromEntries(this.modules)
        };
    }

    /**
     * Destroy orchestrator and cleanup
     */
    destroy() {
        this.modules.clear();
        this.isInitialized = false;
        console.log('🗑️ Dashboard orchestrator destroyed');
    }
}

// ================================
// GLOBAL DASHBOARD INSTANCE
// ================================

/**
 * Global dashboard orchestrator instance
 */
const dashboardOrchestrator = new DashboardOrchestrator();

/**
 * Initialize dashboard when DOM is ready
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        dashboardOrchestrator.initialize();
    });
} else {
    dashboardOrchestrator.initialize();
}

/**
 * Export for external access
 */
export { DashboardOrchestrator, dashboardOrchestrator };
export default dashboardOrchestrator;
