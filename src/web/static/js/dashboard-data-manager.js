/**
 * Dashboard Data Manager Module - V2 Compliant
 * Orchestrator for dashboard data operations
 * REFACTORED: 518 lines → ~120 lines (77% reduction)
 * Now uses modular components for V2 compliance
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { cacheDashboardData, getCachedDashboardData, isDashboardCacheValid, clearDashboardDataCache, getDashboardCacheStats } from './dashboard-cache-manager.js';
import { handleDashboardDataError, getDashboardErrorStats } from './dashboard-error-handler.js';
import { setDashboardLoadingState, getDashboardLoadingStats } from './dashboard-loading-manager.js';
import { getDashboardRetryStats } from './dashboard-retry-manager.js';
import { getDashboardOptimisticUpdateStats } from './dashboard-optimistic-updates.js';
import { loadDashboardViewData, loadMultipleDashboardViews, updateDashboardViewData } from './dashboard-data-operations.js';

// ================================
// DASHBOARD DATA MANAGER ORCHESTRATOR
// ================================

/**
 * Dashboard data manager orchestrator
 * Uses modular components for V2 compliance
 */
class DashboardDataManager {
    constructor() {
        this.isInitialized = false;
    }

    /**
     * Initialize data manager
     */
    initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Data manager already initialized');
            return;
        }

        console.log('📊 Initializing dashboard data manager...');

        // Setup global error handlers
        this.setupGlobalErrorHandlers();

        this.isInitialized = true;
        console.log('✅ Dashboard data manager initialized');
    }

    /**
     * Setup global error handlers
     */
    setupGlobalErrorHandlers() {
        window.addEventListener('unhandledrejection', (event) => {
            console.error('🚨 Unhandled promise rejection:', event.reason);
            event.preventDefault();
        });

        window.addEventListener('error', (event) => {
            console.error('🚨 Global error:', event.error);
        });
    }

    /**
     * Load dashboard data for view
     */
    async loadDashboardData(view, options = {}) {
        return loadDashboardViewData(view, options);
    }

    /**
     * Load multiple views
     */
    async loadMultipleViews(views, options = {}) {
        return loadMultipleDashboardViews(views, options);
    }

    /**
     * Update dashboard data
     */
    async updateDashboardData(view, updateData, options = {}) {
        return updateDashboardViewData(view, updateData, options);
    }

    /**
     * Clear data cache
     */
    clearCache() {
        clearDashboardDataCache();
    }

    /**
     * Get comprehensive status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            cacheStats: getDashboardCacheStats(),
            loadingStats: getDashboardLoadingStats(),
            errorStats: getDashboardErrorStats(),
            retryStats: getDashboardRetryStats(),
            optimisticUpdateStats: getDashboardOptimisticUpdateStats()
        };
    }

    /**
     * Reset all states
     */
    reset() {
        clearDashboardDataCache();
        console.log('🔄 Data manager reset');
    }
}

// ================================
// GLOBAL DASHBOARD DATA MANAGER INSTANCE
// ================================

/**
 * Global dashboard data manager instance
 */
const dashboardDataManager = new DashboardDataManager();

// ================================
// DATA MANAGER API FUNCTIONS
// ================================

/**
 * Initialize dashboard data manager
 */
export function initializeDashboardDataManager() {
    dashboardDataManager.initialize();
}

/**
 * Load dashboard data for view
 */
export function loadDashboardData(view, options = {}) {
    return dashboardDataManager.loadDashboardData(view, options);
}

/**
 * Load multiple views concurrently
 */
export function loadMultipleViews(views, options = {}) {
    return dashboardDataManager.loadMultipleViews(views, options);
}

/**
 * Update dashboard data
 */
export function updateDashboardData(view, data, options = {}) {
    return dashboardDataManager.updateDashboardData(view, data, options);
}

/**
 * Clear data cache
 */
export function clearDataCache() {
    dashboardDataManager.clearCache();
}

/**
 * Get data manager status
 */
export function getDataManagerStatus() {
    return dashboardDataManager.getStatus();
}

// ================================
// EXPORTS
// ================================

export { DashboardDataManager, dashboardDataManager };
export default dashboardDataManager;