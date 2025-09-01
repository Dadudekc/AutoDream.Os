/**
 * Dashboard Retry Manager Module - V2 Compliant
 * Retry logic extracted from dashboard-data-manager.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// DASHBOARD RETRY MANAGER
// ================================

/**
 * Retry management for dashboard operations
 */
class DashboardRetryManager {
    constructor() {
        this.retryAttempts = new Map();
        this.maxRetries = 3;
    }

    /**
     * Get retry count for view
     */
    getRetryCount(view) {
        return this.retryAttempts.get(view) || 0;
    }

    /**
     * Increment retry count for view
     */
    incrementRetryCount(view) {
        const current = this.getRetryCount(view);
        this.retryAttempts.set(view, current + 1);
        return current + 1;
    }

    /**
     * Reset retry count for view
     */
    resetRetryCount(view) {
        this.retryAttempts.delete(view);
    }

    /**
     * Check if should retry for view
     */
    shouldRetry(view) {
        return this.getRetryCount(view) < this.maxRetries;
    }

    /**
     * Get retry statistics
     */
    getRetryStats() {
        const stats = {
            totalRetries: 0,
            viewsWithRetries: []
        };

        for (const [view, count] of this.retryAttempts) {
            stats.totalRetries += count;
            stats.viewsWithRetries.push({
                view: view,
                retryCount: count,
                canRetry: count < this.maxRetries
            });
        }

        return stats;
    }

    /**
     * Clear all retry counts
     */
    clearAllRetryCounts() {
        const size = this.retryAttempts.size;
        this.retryAttempts.clear();
        console.log(`🔄 Cleared retry counts for ${size} views`);
    }

    /**
     * Get retry delay (exponential backoff)
     */
    getRetryDelay(view, baseDelay = 1000) {
        const attempt = this.getRetryCount(view);
        return baseDelay * Math.pow(2, attempt);
    }
}

// ================================
// GLOBAL RETRY MANAGER INSTANCE
// ================================

/**
 * Global retry manager instance
 */
const dashboardRetryManager = new DashboardRetryManager();

// ================================
// RETRY MANAGER API FUNCTIONS
// ================================

/**
 * Get retry count
 */
export function getDashboardRetryCount(view) {
    return dashboardRetryManager.getRetryCount(view);
}

/**
 * Increment retry count
 */
export function incrementDashboardRetryCount(view) {
    return dashboardRetryManager.incrementRetryCount(view);
}

/**
 * Reset retry count
 */
export function resetDashboardRetryCount(view) {
    dashboardRetryManager.resetRetryCount(view);
}

/**
 * Check if should retry
 */
export function shouldRetryDashboardOperation(view) {
    return dashboardRetryManager.shouldRetry(view);
}

/**
 * Get retry statistics
 */
export function getDashboardRetryStats() {
    return dashboardRetryManager.getRetryStats();
}

/**
 * Clear all retry counts
 */
export function clearAllDashboardRetryCounts() {
    dashboardRetryManager.clearAllRetryCounts();
}

/**
 * Get retry delay
 */
export function getDashboardRetryDelay(view, baseDelay = 1000) {
    return dashboardRetryManager.getRetryDelay(view, baseDelay);
}

// ================================
// EXPORTS
// ================================

export { DashboardRetryManager, dashboardRetryManager };
export default dashboardRetryManager;
