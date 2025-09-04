/**
 * WebSocket Callback Manager Simplified - V2 Compliant
 * Simplified orchestrator for WebSocket callback management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE SIMPLIFICATION
 * @license MIT
 */

import { createUnifiedLoggingSystem } from './unified-logging-module.js';
import { createWebSocketMarketDataCallbacks } from './websocket-market-data-callbacks.js';
import { createWebSocketConnectionCallbacks } from './websocket-connection-callbacks.js';
import { createWebSocketOrderPortfolioCallbacks } from './websocket-order-portfolio-callbacks.js';
import { createWebSocketErrorCallbacks } from './websocket-error-callbacks.js';

// ================================
// SIMPLIFIED WEBSOCKET CALLBACK MANAGER ORCHESTRATOR
// ================================

/**
 * Simplified orchestrator for WebSocket callback management
 */
export class WebSocketCallbackManagerSimplified {
    constructor() {
        // Initialize unified logging
        this.logger = createUnifiedLoggingSystem("WebSocketCallbackManagerSimplified");

        // Log unified systems deployment
        this.logger.logUnifiedSystemsDeployment('websocket_callback_manager_simplified', 'active', {
            version: '2.0.0',
            agentId: 'Agent-7',
            integrationStatus: 'ACTIVE'
        });

        // Initialize callback modules
        this.marketDataCallbacks = createWebSocketMarketDataCallbacks();
        this.connectionCallbacks = createWebSocketConnectionCallbacks();
        this.orderPortfolioCallbacks = createWebSocketOrderPortfolioCallbacks();
        this.errorCallbacks = createWebSocketErrorCallbacks();
    }

    /**
     * Initialize simplified callback manager
     */
    initialize() {
        this.logger.logOperationStart('simplifiedCallbackManagerInitialization');
        this.logger.logOperationComplete('simplifiedCallbackManagerInitialization', {
            modules: ['marketData', 'connection', 'orderPortfolio', 'error'],
            unifiedLogging: true
        });
    }

    // ================================
    // CALLBACK MANAGEMENT METHODS
    // ================================

    addMarketDataCallback(callback) { return this.marketDataCallbacks.addCallbackValidated(callback); }
    addConnectionCallback(callback) { return this.connectionCallbacks.addCallbackValidated(callback); }
    addErrorCallback(callback) { return this.errorCallbacks.addCallbackValidated(callback); }
    addOrderCallback(callback) { return this.orderPortfolioCallbacks.addOrderCallbackValidated(callback); }
    addPortfolioCallback(callback) { return this.orderPortfolioCallbacks.addPortfolioCallbackValidated(callback); }

    removeMarketDataCallback(callback) { return this.marketDataCallbacks.removeCallback(callback); }
    removeConnectionCallback(callback) { return this.connectionCallbacks.removeCallback(callback); }
    removeErrorCallback(callback) { return this.errorCallbacks.removeCallback(callback); }
    removeOrderCallback(callback) { return this.orderPortfolioCallbacks.removeOrderCallback(callback); }
    removePortfolioCallback(callback) { return this.orderPortfolioCallbacks.removePortfolioCallback(callback); }

    removeCallbackById(id) {
        return this.marketDataCallbacks.removeCallbackById(id) ||
               this.connectionCallbacks.removeCallbackById(id) ||
               this.errorCallbacks.removeCallbackById(id) ||
               this.orderPortfolioCallbacks.removeCallbackById(id);
    }

    // ================================
    // NOTIFICATION METHODS
    // ================================

    notifyMarketDataCallbacks(data) { this.marketDataCallbacks.notifyCallbacks(data); }
    notifyConnectionCallbacks(status) { this.connectionCallbacks.notifyCallbacks(status); }
    notifyErrorCallbacks(errorData) { this.errorCallbacks.notifyCallbacks(errorData); }
    notifyOrderCallbacks(orderData) { this.orderPortfolioCallbacks.notifyOrderCallbacks(orderData); }
    notifyPortfolioCallbacks(portfolioData) { this.orderPortfolioCallbacks.notifyPortfolioCallbacks(portfolioData); }

    // ================================
    // STATISTICS METHODS
    // ================================

    getCallbackStatistics() {
        const marketDataStats = this.marketDataCallbacks.getStatistics();
        const connectionStats = this.connectionCallbacks.getStatistics();
        const orderPortfolioStats = this.orderPortfolioCallbacks.getStatistics();
        const errorStats = this.errorCallbacks.getStatistics();

        return {
            marketDataCallbacks: marketDataStats.callbackCount,
            connectionCallbacks: connectionStats.callbackCount,
            orderCallbacks: orderPortfolioStats.callbackCounts.orderCallbacks,
            portfolioCallbacks: orderPortfolioStats.callbackCounts.portfolioCallbacks,
            errorCallbacks: errorStats.callbackCount,
            totalCallbacks: marketDataStats.callbackCount +
                           connectionStats.callbackCount +
                           orderPortfolioStats.callbackCounts.totalCallbacks +
                           errorStats.callbackCount,
            eventHistory: {
                marketData: marketDataStats.eventHistorySize,
                connection: connectionStats.connectionHistorySize,
                orderPortfolio: orderPortfolioStats.eventHistorySize,
                errors: errorStats.errorHistorySize
            }
        };
    }

    getCallbacksByType(type) {
        switch (type) {
            case 'marketData': return this.marketDataCallbacks.getCallbacks();
            case 'connection': return this.connectionCallbacks.getCallbacks();
            case 'error': return this.errorCallbacks.getCallbacks();
            case 'order': return this.orderPortfolioCallbacks.getOrderCallbacks();
            case 'portfolio': return this.orderPortfolioCallbacks.getPortfolioCallbacks();
            default: return [];
        }
    }

    // ================================
    // UTILITY METHODS
    // ================================

    clearAllCallbacks() {
        this.marketDataCallbacks.clearCallbacks();
        this.connectionCallbacks.clearCallbacks();
        this.orderPortfolioCallbacks.clearAllCallbacks();
        this.errorCallbacks.clearCallbacks();
        this.logger.log('🧹 All WebSocket callbacks cleared');
    }

    getStatus() {
        return {
            initialized: true,
            modulesInitialized: {
                marketDataCallbacks: true,
                connectionCallbacks: true,
                orderPortfolioCallbacks: true,
                errorCallbacks: true
            },
            callbackStats: this.getCallbackStatistics(),
            timestamp: new Date().toISOString()
        };
    }

    getComprehensiveStatistics() {
        return {
            callbackStats: this.getCallbackStatistics(),
            marketDataStats: this.marketDataCallbacks.getStatistics(),
            connectionStats: this.connectionCallbacks.getStatistics(),
            orderPortfolioStats: this.orderPortfolioCallbacks.getStatistics(),
            errorStats: this.errorCallbacks.getStatistics(),
            loggerStats: this.logger.getStatistics(),
            timestamp: new Date().toISOString()
        };
    }

    // ================================
    // BATCH OPERATIONS
    // ================================

    batchAddCallbacks(callbacks) {
        if (!Array.isArray(callbacks)) {
            this.logger.logOperationFailed('batchAddCallbacks', 'Callbacks must be an array');
            return false;
        }

        let successCount = 0;
        callbacks.forEach(cb => {
            if (cb.type && cb.callback) {
                let success = false;
                switch (cb.type) {
                    case 'marketData': success = this.addMarketDataCallback(cb.callback); break;
                    case 'connection': success = this.addConnectionCallback(cb.callback); break;
                    case 'error': success = this.addErrorCallback(cb.callback); break;
                    case 'order': success = this.addOrderCallback(cb.callback); break;
                    case 'portfolio': success = this.addPortfolioCallback(cb.callback); break;
                }
                if (success) successCount++;
            }
        });

        this.logger.log(`✅ Added ${successCount}/${callbacks.length} callbacks`);
        return successCount === callbacks.length;
    }

    batchRemoveCallbacks(callbacks) {
        if (!Array.isArray(callbacks)) return false;

        callbacks.forEach(cb => {
            if (cb.type && cb.callback) {
                switch (cb.type) {
                    case 'marketData': this.removeMarketDataCallback(cb.callback); break;
                    case 'connection': this.removeConnectionCallback(cb.callback); break;
                    case 'error': this.removeErrorCallback(cb.callback); break;
                    case 'order': this.removeOrderCallback(cb.callback); break;
                    case 'portfolio': this.removePortfolioCallback(cb.callback); break;
                }
            }
        });

        this.logger.log(`✅ Removed ${callbacks.length} callbacks`);
        return true;
    }

    // ================================
    // CLEANUP
    // ================================

    cleanup() {
        this.clearAllCallbacks();
        this.marketDataCallbacks.cleanup();
        this.connectionCallbacks.cleanup();
        this.orderPortfolioCallbacks.cleanup();
        this.errorCallbacks.cleanup();
        this.logger.cleanup();
        this.logger.log('💥 WebSocket Callback Manager Simplified cleanup complete');
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy WebSocketCallbackManagerOrchestrator class for backward compatibility
 * @deprecated Use WebSocketCallbackManagerSimplified instead
 */
export class WebSocketCallbackManagerOrchestrator extends WebSocketCallbackManagerSimplified {
    constructor() {
        super();
        console.warn('[DEPRECATED] WebSocketCallbackManagerOrchestrator is deprecated. Use WebSocketCallbackManagerSimplified instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create simplified WebSocket callback manager instance
 */
export function createWebSocketCallbackManagerSimplified() {
    const manager = new WebSocketCallbackManagerSimplified();
    manager.initialize();
    return manager;
}

/**
 * Create legacy orchestrator (backward compatibility)
 */
export function createWebSocketCallbackManagerOrchestrator() {
    const orchestrator = new WebSocketCallbackManagerOrchestrator();
    orchestrator.initialize();
    return orchestrator;
}

