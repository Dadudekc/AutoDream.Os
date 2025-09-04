/**
 * Dashboard Loading Manager Module - V2 Compliant
 * Loading state management extracted from dashboard-data-manager.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// IMPORT DEPENDENCIES
// ================================

import { hideLoadingState, showLoadingState } from './dashboard-ui-helpers.js';

// ================================
// DASHBOARD LOADING MANAGER
// ================================

/**
 * Loading state management for dashboard operations
 */
class DashboardLoadingManager {
    constructor() {
        this.loadingStates = new Map();
    }

    /**
     * Set loading state for view
     */
    setLoadingState(view, isLoading) {
        const previousState = this.loadingStates.get(view);

        if (isLoading) {
            this.loadingStates.set(view, {
                loading: true,
                startTime: Date.now()
            });
            if (!previousState) {
                showLoadingState();
            }
        } else {
            this.loadingStates.delete(view);
            if (previousState) {
                hideLoadingState();
            }
        }
    }

    /**
     * Get loading state for view
     */
    getLoadingState(view) {
        const state = this.loadingStates.get(view);
        return state ? state.loading : false;
    }

    /**
     * Check if any view is loading
     */
    isAnyLoading() {
        return this.loadingStates.size > 0;
    }

    /**
     * Get loading statistics
     */
    getLoadingStats() {
        const stats = {
            loadingViews: this.loadingStates.size,
            views: []
        };

        for (const [view, state] of this.loadingStates) {
            stats.views.push({
                view: view,
                startTime: state.startTime,
                duration: Date.now() - state.startTime
            });
        }

        return stats;
    }

    /**
     * Clear all loading states
     */
    clearAllLoadingStates() {
        const wasLoading = this.loadingStates.size > 0;
        this.loadingStates.clear();

        if (wasLoading) {
            hideLoadingState();
        }
    }

    /**
     * Force hide loading (emergency)
     */
    forceHideLoading() {
        hideLoadingState();
        this.clearAllLoadingStates();
    }
}

// ================================
// GLOBAL LOADING MANAGER INSTANCE
// ================================

/**
 * Global loading manager instance
 */
const dashboardLoadingManager = new DashboardLoadingManager();

// ================================
// LOADING MANAGER API FUNCTIONS
// ================================

/**
 * Set loading state
 */
export function setDashboardLoadingState(view, isLoading) {
    dashboardLoadingManager.setLoadingState(view, isLoading);
}

/**
 * Get loading state
 */
export function getDashboardLoadingState(view) {
    return dashboardLoadingManager.getLoadingState(view);
}

/**
 * Check if any view is loading
 */
export function isAnyDashboardViewLoading() {
    return dashboardLoadingManager.isAnyLoading();
}

/**
 * Get loading statistics
 */
export function getDashboardLoadingStats() {
    return dashboardLoadingManager.getLoadingStats();
}

/**
 * Clear all loading states
 */
export function clearAllDashboardLoadingStates() {
    dashboardLoadingManager.clearAllLoadingStates();
}

/**
 * Force hide loading
 */
export function forceHideDashboardLoading() {
    dashboardLoadingManager.forceHideLoading();
}

// ================================
// EXPORTS
// ================================

export { DashboardLoadingManager, dashboardLoadingManager };
export default dashboardLoadingManager;





