/**
 * Dashboard Core Module - V2 Compliant Modular Orchestrator
 * Main orchestrator using specialized modular components
 * REFACTORED: 317 lines → ~160 lines (49% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { createDashboardConfigManager } from './dashboard-config-manager.js';
import { createDashboardErrorHandler } from './dashboard-error-handler.js';
import { createDashboardStateManager } from './dashboard-state-manager.js';
import { createDashboardTimerManager } from './dashboard-timer-manager.js';

// ================================
// DASHBOARD CORE ORCHESTRATOR
// ================================

/**
 * Core dashboard orchestrator using specialized modules
 * COORDINATES all modular components for V2 compliance
 */
class DashboardCore {
    constructor() {
        // Initialize specialized modules
        this.stateManager = createDashboardStateManager();
        this.configManager = createDashboardConfigManager();
        this.timerManager = createDashboardTimerManager(this.configManager);
        this.errorHandler = createDashboardErrorHandler(this.stateManager, this.configManager);

        // Legacy properties for backward compatibility
        this.state = this.stateManager.state;
        this.config = this.configManager.config;
    }

    /**
     * Initialize dashboard core using modular components
     */
    async initialize() {
        if (this.stateManager.getState().isInitialized) {
            console.warn('⚠️ Dashboard core already initialized');
            return;
        }

        console.log('🚀 Initializing dashboard core (Modular V2 Compliant)...');

        try {
            // Load configuration from storage
            await this.configManager.loadFromStorage();

            // Start timers
            this.timerManager.startTimers();

            // Setup event listeners
            this.setupEventListeners();

            // Mark as initialized
            this.stateManager.setInitialized(true);

            console.log('✅ Dashboard core initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize dashboard core:', error);
            await this.errorHandler.handleError(error, { context: 'initialization' });
            throw error;
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Listen for timer events
        window.addEventListener('dashboard:dataUpdate', (event) => {
            this.handleDataUpdate(event.detail);
        });

        window.addEventListener('dashboard:timeUpdate', (event) => {
            this.handleTimeUpdate(event.detail);
        });

        // Listen for error events
        window.addEventListener('dashboard:error', (event) => {
            this.handleCoreError(event.detail);
        });
    }

    /**
     * Handle data update events
     */
    handleDataUpdate(detail) {
        console.log('📊 Data update triggered:', detail);
        // Implementation would handle data updates
    }

    /**
     * Handle time update events
     */
    handleTimeUpdate(detail) {
        // Update state with last update time
        this.stateManager.updateState({ lastUpdate: detail.timestamp });
    }

    /**
     * Handle core errors
     */
    async handleCoreError(detail) {
        await this.errorHandler.handleError(new Error(detail.error), detail);
    }

    // Delegated methods for backward compatibility
    updateView(view) {
        return this.stateManager.setCurrentView(view);
    }

    setSocket(socket) {
        return this.stateManager.setSocket(socket);
    }

    getState() {
        return this.stateManager.getState();
    }

    updateConfig(newConfig) {
        return this.configManager.update(newConfig);
    }

    getTimerStatus() {
        return this.timerManager.getTimerStatus();
    }

    async handleError(error, context) {
        return this.errorHandler.handleError(error, context);
    }

    // Cleanup method
    async destroy() {
        console.log('🧹 Destroying dashboard core...');

        // Stop timers
        this.timerManager.stopTimers();

        // Save configuration
        await this.configManager.saveToStorage();

        // Reset state
        this.stateManager.resetState();

        console.log('✅ Dashboard core destroyed');
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

// Legacy factory function for existing code
export function createDashboardCore() {
    return new DashboardCore();
}

// ================================
// EXPORTS
// ================================

export default DashboardCore;
