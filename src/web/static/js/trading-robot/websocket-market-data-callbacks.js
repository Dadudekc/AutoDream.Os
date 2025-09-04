/**
 * WebSocket Market Data Callbacks Module - V2 Compliant
 * Specialized callback management for market data events
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// MARKET DATA CALLBACKS MODULE
// ================================

/**
 * Specialized callback management for market data events
 */
export class WebSocketMarketDataCallbacks {
    constructor() {
        this.logger = console;
        this.callbacks = [];
        this.eventHistory = [];
        this.maxHistorySize = 100;
    }

    /**
     * Add market data callback
     */
    addCallback(callback) {
        if (typeof callback === 'function') {
            this.callbacks.push({
                callback,
                id: this.generateCallbackId(),
                addedAt: new Date()
            });
            return true;
        }
        this.logger.warn('⚠️ Invalid market data callback provided');
        return false;
    }

    /**
     * Remove callback by function reference
     */
    removeCallback(callback) {
        const index = this.callbacks.findIndex(cb => cb.callback === callback);
        if (index > -1) {
            this.callbacks.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * Remove callback by ID
     */
    removeCallbackById(id) {
        const index = this.callbacks.findIndex(cb => cb.id === id);
        if (index > -1) {
            this.callbacks.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * Notify all market data callbacks
     */
    notifyCallbacks(marketData) {
        this.callbacks.forEach(cb => {
            try {
                cb.callback(marketData);
            } catch (error) {
                this.logger.error('❌ Error in market data callback:', error);
            }
        });

        // Record event in history
        this.recordEvent('marketData', marketData);
    }

    /**
     * Get all callbacks
     */
    getCallbacks() {
        return [...this.callbacks];
    }

    /**
     * Get callback count
     */
    getCallbackCount() {
        return this.callbacks.length;
    }

    /**
     * Clear all callbacks
     */
    clearCallbacks() {
        this.callbacks = [];
        this.logger.log('🧹 Market data callbacks cleared');
    }

    /**
     * Generate unique callback ID
     */
    generateCallbackId() {
        return `market_cb_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Record event in history
     */
    recordEvent(type, data) {
        this.eventHistory.push({
            type,
            data,
            timestamp: new Date(),
            callbackCount: this.callbacks.length
        });

        // Maintain history size limit
        if (this.eventHistory.length > this.maxHistorySize) {
            this.eventHistory.shift();
        }
    }

    /**
     * Get event history
     */
    getEventHistory(limit = 10) {
        return this.eventHistory.slice(-limit);
    }

    /**
     * Validate callback function
     */
    validateCallback(callback) {
        if (typeof callback !== 'function') {
            return { valid: false, error: 'Callback must be a function' };
        }

        if (callback.length === 0) {
            return { valid: false, error: 'Callback should accept market data parameter' };
        }

        return { valid: true };
    }

    /**
     * Add callback with validation
     */
    addCallbackValidated(callback) {
        const validation = this.validateCallback(callback);
        if (!validation.valid) {
            this.logger.error(`❌ Invalid callback: ${validation.error}`);
            return false;
        }

        return this.addCallback(callback);
    }

    /**
     * Get statistics
     */
    getStatistics() {
        return {
            callbackCount: this.callbacks.length,
            eventHistorySize: this.eventHistory.length,
            maxHistorySize: this.maxHistorySize,
            oldestEvent: this.eventHistory.length > 0 ? this.eventHistory[0].timestamp : null,
            newestEvent: this.eventHistory.length > 0 ? this.eventHistory[this.eventHistory.length - 1].timestamp : null
        };
    }

    /**
     * Cleanup module
     */
    cleanup() {
        this.clearCallbacks();
        this.eventHistory = [];
        this.logger.log('🧹 Market data callbacks module cleanup complete');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create WebSocket market data callbacks instance
 */
export function createWebSocketMarketDataCallbacks() {
    return new WebSocketMarketDataCallbacks();
}

