/**
 * WebSocket Connection Callbacks Module - V2 Compliant
 * Specialized callback management for connection events
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// CONNECTION CALLBACKS MODULE
// ================================

/**
 * Specialized callback management for connection events
 */
export class WebSocketConnectionCallbacks {
    constructor() {
        this.logger = console;
        this.callbacks = [];
        this.connectionHistory = [];
        this.maxHistorySize = 50;
    }

    /**
     * Add connection callback
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
        this.logger.warn('⚠️ Invalid connection callback provided');
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
     * Notify all connection callbacks
     */
    notifyCallbacks(status) {
        this.callbacks.forEach(cb => {
            try {
                cb.callback(status);
            } catch (error) {
                this.logger.error('❌ Error in connection callback:', error);
            }
        });

        // Record connection event
        this.recordConnectionEvent(status);
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
        this.logger.log('🧹 Connection callbacks cleared');
    }

    /**
     * Generate unique callback ID
     */
    generateCallbackId() {
        return `connection_cb_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Record connection event in history
     */
    recordConnectionEvent(status) {
        this.connectionHistory.push({
            status,
            timestamp: new Date(),
            callbackCount: this.callbacks.length
        });

        // Maintain history size limit
        if (this.connectionHistory.length > this.maxHistorySize) {
            this.connectionHistory.shift();
        }
    }

    /**
     * Get connection history
     */
    getConnectionHistory(limit = 10) {
        return this.connectionHistory.slice(-limit);
    }

    /**
     * Get connection statistics
     */
    getConnectionStatistics() {
        if (this.connectionHistory.length === 0) {
            return { totalEvents: 0 };
        }

        const statusCounts = {};
        this.connectionHistory.forEach(event => {
            statusCounts[event.status] = (statusCounts[event.status] || 0) + 1;
        });

        return {
            totalEvents: this.connectionHistory.length,
            statusCounts,
            timeRange: {
                oldest: this.connectionHistory[0].timestamp,
                newest: this.connectionHistory[this.connectionHistory.length - 1].timestamp
            }
        };
    }

    /**
     * Validate callback function
     */
    validateCallback(callback) {
        if (typeof callback !== 'function') {
            return { valid: false, error: 'Callback must be a function' };
        }

        if (callback.length === 0) {
            return { valid: false, error: 'Callback should accept status parameter' };
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
            connectionHistorySize: this.connectionHistory.length,
            maxHistorySize: this.maxHistorySize,
            connectionStats: this.getConnectionStatistics()
        };
    }

    /**
     * Cleanup module
     */
    cleanup() {
        this.clearCallbacks();
        this.connectionHistory = [];
        this.logger.log('🧹 Connection callbacks module cleanup complete');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create WebSocket connection callbacks instance
 */
export function createWebSocketConnectionCallbacks() {
    return new WebSocketConnectionCallbacks();
}

