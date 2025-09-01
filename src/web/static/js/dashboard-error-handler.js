/**
 * Dashboard Error Handler Module - V2 Compliant
 * Error handling functionality extracted from dashboard-data-manager.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// IMPORT DEPENDENCIES
// ================================

import { showAlert } from './dashboard-ui-helpers.js';

// ================================
// DASHBOARD ERROR HANDLER
// ================================

/**
 * Error handling for dashboard operations
 */
class DashboardErrorHandler {
    constructor() {
        this.errorStates = new Map();
    }

    /**
     * Handle data operation errors
     */
    async handleDataError(view, error, options = {}) {
        const { silent = false, showRetry = true } = options;

        if (this.isRecoverableError(error)) {
            if (!silent) {
                console.warn(`🔄 Recoverable error for ${view}:`, error);
            }
            // Could implement auto-retry logic here
        } else {
            if (!silent) {
                console.error(`❌ Error for ${view}:`, error);
                this.showErrorMessage(view, error);
            }
        }

        // Store error state
        this.setErrorState(view, error);
    }

    /**
     * Check if error is recoverable
     */
    isRecoverableError(error) {
        // Network errors that might be temporary
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            return true;
        }

        // Request aborted (user navigation)
        if (error.name === 'AbortError') {
            return false; // Not recoverable, user initiated
        }

        // Server errors that might be temporary
        if (error.message.includes('HTTP 5')) {
            return true;
        }

        return false;
    }

    /**
     * Show appropriate error message
     */
    showErrorMessage(view, error) {
        let message = `An error occurred while loading ${view} data.`;

        if (error.name === 'TypeError') {
            message = 'Network error. Please check your connection and try again.';
        } else if (error.message.includes('HTTP 4')) {
            message = 'Data not found or access denied.';
        } else if (error.message.includes('HTTP 5')) {
            message = 'Server error. Please try again later.';
        }

        showAlert('error', message);
    }

    /**
     * Set error state for view
     */
    setErrorState(view, error) {
        this.errorStates.set(view, {
            error: error,
            timestamp: Date.now()
        });
    }

    /**
     * Get error state for view
     */
    getErrorState(view) {
        return this.errorStates.get(view);
    }

    /**
     * Clear error state for view
     */
    clearErrorState(view) {
        this.errorStates.delete(view);
    }

    /**
     * Clear all error states
     */
    clearAllErrorStates() {
        this.errorStates.clear();
    }

    /**
     * Get error statistics
     */
    getErrorStats() {
        return {
            errorCount: this.errorStates.size,
            errors: Object.fromEntries(this.errorStates)
        };
    }
}

// ================================
// GLOBAL ERROR HANDLER INSTANCE
// ================================

/**
 * Global error handler instance
 */
const dashboardErrorHandler = new DashboardErrorHandler();

// ================================
// ERROR HANDLER API FUNCTIONS
// ================================

/**
 * Handle data error
 */
export function handleDashboardDataError(view, error, options = {}) {
    return dashboardErrorHandler.handleDataError(view, error, options);
}

/**
 * Check if error is recoverable
 */
export function isRecoverableDashboardError(error) {
    return dashboardErrorHandler.isRecoverableError(error);
}

/**
 * Show error message
 */
export function showDashboardErrorMessage(view, error) {
    dashboardErrorHandler.showErrorMessage(view, error);
}

/**
 * Set error state
 */
export function setDashboardErrorState(view, error) {
    dashboardErrorHandler.setErrorState(view, error);
}

/**
 * Get error state
 */
export function getDashboardErrorState(view) {
    return dashboardErrorHandler.getErrorState(view);
}

/**
 * Clear error state
 */
export function clearDashboardErrorState(view) {
    dashboardErrorHandler.clearErrorState(view);
}

/**
 * Clear all error states
 */
export function clearAllDashboardErrorStates() {
    dashboardErrorHandler.clearAllErrorStates();
}

/**
 * Get error statistics
 */
export function getDashboardErrorStats() {
    return dashboardErrorHandler.getErrorStats();
}

// ================================
// EXPORTS
// ================================

export { DashboardErrorHandler, dashboardErrorHandler };
export default dashboardErrorHandler;
