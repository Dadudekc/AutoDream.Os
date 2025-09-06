/**
 * Dashboard Data Operations Module - V2 Compliant
 * Core data operations extracted from dashboard-data-manager.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// IMPORT DEPENDENCIES
// ================================

import { applyDashboardOptimisticUpdate, revertDashboardOptimisticUpdate } from './dashboard-optimistic-updates.js';
import { cacheDashboardData, getCachedDashboardData, isDashboardCacheValid } from './dashboard-cache-manager.js';
import { getDashboardRetryCount, getDashboardRetryDelay, incrementDashboardRetryCount, resetDashboardRetryCount, shouldRetryDashboardOperation } from './dashboard-retry-manager.js';
import { handleDashboardDataError, isRecoverableDashboardError } from './dashboard-error-handler.js';

import { setDashboardLoadingState } from './dashboard-loading-manager.js';
import { showAlert } from './dashboard-ui-helpers.js';

// ================================
// DASHBOARD DATA OPERATIONS
// ================================

/**
 * Core data operations for dashboard
 */
class DashboardDataOperations {
    constructor() {
        this.maxRetries = 3;
    }

    /**
     * Load dashboard data for specific view using repository pattern
     */
    async loadDashboardData(view, options = {}) {
        const {
            forceRefresh = false,
            showLoading = true,
            timeout = 10000,
            retryOnFailure = true
        } = options;

        // Set loading state
        if (showLoading) {
            setDashboardLoadingState(view, true);
        }

        try {
            // Use repository pattern for data access
            const { DashboardRepository } = await import('./repositories/dashboard-repository.js');
            const repository = new DashboardRepository();

            // If force refresh, clear cache first
            if (forceRefresh) {
                repository.clearCache();
            }

            const data = await repository.getDashboardData(view);

            // Reset loading state on success
            if (showLoading) {
                setDashboardLoadingState(view, false);
            }

            return data;

        } catch (error) {
            // Handle errors using error handler
            const { handleDashboardDataError } = await import('./dashboard-error-handler.js');
            await handleDashboardDataError(view, error, { silent: !showLoading });

            // Reset loading state on error
            if (showLoading) {
                setDashboardLoadingState(view, false);
            }

            throw error;

        } finally {
            // Clear loading state
            if (showLoading) {
                setDashboardLoadingState(view, false);
            }
        }
    }

    /**
     * Load multiple views concurrently
     */
    async loadMultipleViews(views, options = {}) {
        const { showLoading = true, concurrent = true } = options;

        if (showLoading) {
            setDashboardLoadingState('multiple', true);
        }

        try {
            const promises = views.map(view =>
                this.loadDashboardData(view, { ...options, showLoading: false })
            );

            if (concurrent) {
                const results = await Promise.allSettled(promises);

                const successful = [];
                const failed = [];

                results.forEach((result, index) => {
                    if (result.status === 'fulfilled') {
                        successful.push({ view: views[index], data: result.value });
                    } else {
                        failed.push(views[index]);
                    }
                });

                if (failed.length > 0) {
                    showAlert('warning', `${failed.length} out of ${views.length} views failed to load.`);
                }

                return { successful, failed };
            } else {
                // Sequential loading
                const successful = [];
                const failed = [];

                for (const view of views) {
                    try {
                        const data = await this.loadDashboardData(view, { ...options, showLoading: false });
                        successful.push({ view, data });
                    } catch (error) {
                        failed.push(view);
                    }
                }

                return { successful, failed };
            }

        } finally {
            if (showLoading) {
                setDashboardLoadingState('multiple', false);
            }
        }
    }

    /**
     * Update dashboard data
     */
    async updateDashboardData(view, updateData, options = {}) {
        const {
            showLoading = true,
            optimistic = false,
            timeout = 10000
        } = options;

        if (showLoading) {
            setDashboardLoadingState(view, true);
        }

        // Apply optimistic update if requested
        if (optimistic) {
            applyDashboardOptimisticUpdate(view, updateData);
        }

        try {
            // Make API request
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);

            const response = await fetch(`/api/dashboard/${view}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updateData),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();

            if (result.error) {
                throw new Error(result.error);
            }

            // Update cache
            const cacheKey = `dashboard_${view}`;
            cacheDashboardData(cacheKey, result);

            return result;

        } catch (error) {
            // Revert optimistic update on failure
            if (optimistic) {
                revertDashboardOptimisticUpdate(view);
            }

            await handleDashboardDataError(view, error, { silent: !showLoading });
            throw error;

        } finally {
            if (showLoading) {
                setDashboardLoadingState(view, false);
            }
        }
    }
}

// ================================
// GLOBAL DATA OPERATIONS INSTANCE
// ================================

/**
 * Global data operations instance
 */
const dashboardDataOperations = new DashboardDataOperations();

// ================================
// DATA OPERATIONS API FUNCTIONS
// ================================

/**
 * Load dashboard data
 */
export function loadDashboardViewData(view, options = {}) {
    return dashboardDataOperations.loadDashboardData(view, options);
}

/**
 * Load multiple views
 */
export function loadMultipleDashboardViews(views, options = {}) {
    return dashboardDataOperations.loadMultipleViews(views, options);
}

/**
 * Update dashboard data
 */
export function updateDashboardViewData(view, updateData, options = {}) {
    return dashboardDataOperations.updateDashboardData(view, updateData, options);
}

// ================================
// EXPORTS
// ================================

export { DashboardDataOperations, dashboardDataOperations };
export default dashboardDataOperations;
