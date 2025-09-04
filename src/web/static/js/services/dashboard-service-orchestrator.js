/**
 * Dashboard Service Orchestrator - V2 Compliant
 * Main orchestrator for dashboard service modules
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// IMPORTS
// ================================

import { createDashboardDataService } from './dashboard-data-service.js';
import { createDashboardEventService } from './dashboard-event-service.js';
import { createDashboardInitService } from './dashboard-init-service.js';
import { createUtilityService } from './utility-service-v2.js';

// ================================
// DASHBOARD SERVICE ORCHESTRATOR
// ================================

/**
 * Main orchestrator for all dashboard service modules
 */
export class DashboardServiceOrchestrator {
    constructor(options = {}) {
        this.initialized = false;
        this.options = options;
        this.modules = new Map();
    }

    /**
     * Initialize the orchestrator
     */
    async initialize() {
        if (this.initialized) return;

        // Initialize modular components
        this.dashboardRepository = this.options.dashboardRepository;
        this.utilityService = this.options.utilityService || createUtilityService();

        this.modules.set('init', createDashboardInitService(
            this.dashboardRepository,
            this.utilityService
        ));
        this.modules.set('data', createDashboardDataService(
            this.dashboardRepository,
            this.utilityService
        ));
        this.modules.set('event', createDashboardEventService(
            this.utilityService
        ));

        this.initialized = true;
    }

    /**
     * Initialize dashboard
     */
    async initializeDashboard(config) {
        return this.modules.get('init').initializeDashboard(config);
    }

    /**
     * Load dashboard data
     */
    async loadDashboardData(view, options = {}) {
        return this.modules.get('data').loadDashboardData(view, options);
    }

    /**
     * Process dashboard data
     */
    async processDashboardData(data, options = {}) {
        return this.modules.get('data').processDashboardData(data, options);
    }

    /**
     * Calculate dashboard metrics
     */
    calculateDashboardMetrics(data) {
        return this.modules.get('data').calculateMetrics(data);
    }

    /**
     * Setup socket connection
     */
    setupSocketConnection(socketConfig) {
        return this.modules.get('event').setupSocketConnection(socketConfig);
    }

    /**
     * Add event listener
     */
    addEventListener(event, listener) {
        return this.modules.get('event').addEventListener(event, listener);
    }

    /**
     * Remove event listener
     */
    removeEventListener(event, listener) {
        return this.modules.get('event').removeEventListener(event, listener);
    }

    /**
     * Dispatch event
     */
    dispatchEvent(event, data) {
        return this.modules.get('event').dispatchEvent(event, data);
    }

    /**
     * Update dashboard view
     */
    async updateDashboardView(view, options = {}) {
        try {
            const data = await this.loadDashboardData(view, options);
            this.dispatchEvent('dashboard:viewChanged', {
                view,
                data,
                timestamp: this.utilityService.formatDate(new Date(), 'ISO')
            });
            return data;
        } catch (error) {
            this.utilityService.logError(`Dashboard view update failed for: ${view}`, error);
            throw error;
        }
    }

    /**
     * Refresh dashboard data
     */
    async refreshDashboardData(view) {
        try {
            this.modules.get('data').clearCache();
            const data = await this.loadDashboardData(view, { forceRefresh: true });
            this.dispatchEvent('dashboard:dataRefreshed', {
                view,
                data,
                timestamp: this.utilityService.formatDate(new Date(), 'ISO')
            });
            return data;
        } catch (error) {
            this.utilityService.logError(`Dashboard data refresh failed for: ${view}`, error);
            throw error;
        }
    }

    /**
     * Validate dashboard config
     */
    async validateDashboardConfig(config) {
        return this.modules.get('init').validateRequiredFields(config, ['defaultView']);
    }

    /**
     * Update dashboard config
     */
    async updateDashboardConfig(config) {
        try {
            const isValid = await this.validateDashboardConfig(config);
            if (!isValid) {
                throw new Error('Invalid dashboard configuration');
            }

            this.dispatchEvent('dashboard:configUpdated', {
                config,
                timestamp: this.utilityService.formatDate(new Date(), 'ISO')
            });

            return { success: true, message: 'Dashboard configuration updated' };
        } catch (error) {
            this.utilityService.logError('Dashboard configuration update failed', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Get dashboard stats
     */
    getDashboardStats() {
        try {
            return {
                cache: this.modules.get('data').getCacheStats(),
                events: {
                    socketHandlers: this.modules.get('event').socketHandlers.size,
                    eventListeners: this.modules.get('event').eventListeners.size,
                    queuedEvents: this.modules.get('event').eventQueue.length
                },
                timestamp: this.utilityService.formatDate(new Date(), 'ISO')
            };
        } catch (error) {
            this.utilityService.logError('Dashboard stats retrieval failed', error);
            return {};
        }
    }

    /**
     * Shutdown dashboard
     */
    async shutdownDashboard() {
        try {
            this.modules.get('event').cleanup();
            this.modules.get('data').clearCache();

            this.dispatchEvent('dashboard:shutdown', {
                timestamp: this.utilityService.formatDate(new Date(), 'ISO')
            });

            this.utilityService.logInfo('Dashboard shutdown completed');
            return { success: true, message: 'Dashboard shutdown completed' };
        } catch (error) {
            this.utilityService.logError('Dashboard shutdown failed', error);
            return { success: false, error: error.message };
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create dashboard service orchestrator
 */
export function createDashboardServiceOrchestrator(options = {}) {
    return new DashboardServiceOrchestrator(options);
}

