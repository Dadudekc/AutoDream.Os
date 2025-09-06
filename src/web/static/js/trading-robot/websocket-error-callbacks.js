/**
 * WebSocket Error Callbacks Module - V2 Compliant
 * Specialized callback management for error events
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// ERROR CALLBACKS MODULE
// ================================

/**
 * Specialized callback management for error events
 */
export class WebSocketErrorCallbacks {
    constructor() {
        this.logger = console;
        this.callbacks = [];
        this.errorHistory = [];
        this.maxHistorySize = 50;
        this.errorCounts = new Map();
    }

    /**
     * Add error callback
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
        this.logger.warn('⚠️ Invalid error callback provided');
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
     * Notify all error callbacks
     */
    notifyCallbacks(errorData) {
        this.callbacks.forEach(cb => {
            try {
                cb.callback(errorData);
            } catch (error) {
                this.logger.error('❌ Error in error callback:', error);
            }
        });

        // Record error in history
        this.recordError(errorData);
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
        this.logger.log('🧹 Error callbacks cleared');
    }

    /**
     * Generate unique callback ID
     */
    generateCallbackId() {
        return `error_cb_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Record error in history
     */
    recordError(errorData) {
        const errorKey = this.getErrorKey(errorData);

        this.errorHistory.push({
            errorData,
            timestamp: new Date(),
            callbackCount: this.callbacks.length,
            errorKey
        });

        // Update error counts
        this.errorCounts.set(errorKey, (this.errorCounts.get(errorKey) || 0) + 1);

        // Maintain history size limit
        if (this.errorHistory.length > this.maxHistorySize) {
            this.errorHistory.shift();
        }
    }

    /**
     * Get error key for categorization
     */
    getErrorKey(errorData) {
        if (errorData && errorData.code) {
            return `code_${errorData.code}`;
        }
        if (errorData && errorData.type) {
            return `type_${errorData.type}`;
        }
        if (errorData && errorData.message) {
            return `message_${errorData.message.substring(0, 50)}`;
        }
        return 'unknown_error';
    }

    /**
     * Get error history
     */
    getErrorHistory(limit = 10) {
        return this.errorHistory.slice(-limit);
    }

    /**
     * Get error statistics
     */
    getErrorStatistics() {
        const stats = {
            totalErrors: this.errorHistory.length,
            errorCounts: Object.fromEntries(this.errorCounts),
            timeRange: this.errorHistory.length > 0 ? {
                oldest: this.errorHistory[0].timestamp,
                newest: this.errorHistory[this.errorHistory.length - 1].timestamp
            } : null
        };

        // Calculate error frequency
        if (this.errorHistory.length > 1) {
            const timeSpan = this.errorHistory[this.errorHistory.length - 1].timestamp - this.errorHistory[0].timestamp;
            stats.errorsPerMinute = (this.errorHistory.length / timeSpan) * 60000;
        }

        return stats;
    }

    /**
     * Get most frequent errors
     */
    getMostFrequentErrors(limit = 5) {
        return Array.from(this.errorCounts.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .map(([errorKey, count]) => ({ errorKey, count }));
    }

    /**
     * Validate callback function
     */
    validateCallback(callback) {
        if (typeof callback !== 'function') {
            return { valid: false, error: 'Callback must be a function' };
        }

        if (callback.length === 0) {
            return { valid: false, error: 'Callback should accept error data parameter' };
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
     * Clear error history
     */
    clearErrorHistory() {
        this.errorHistory = [];
        this.errorCounts.clear();
        this.logger.log('🧹 Error history cleared');
    }

    /**
     * Get statistics
     */
    getStatistics() {
        return {
            callbackCount: this.callbacks.length,
            errorHistorySize: this.errorHistory.length,
            maxHistorySize: this.maxHistorySize,
            errorStats: this.getErrorStatistics(),
            mostFrequentErrors: this.getMostFrequentErrors()
        };
    }

    /**
     * Cleanup module
     */
    cleanup() {
        this.clearCallbacks();
        this.clearErrorHistory();
        this.logger.log('🧹 Error callbacks module cleanup complete');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create WebSocket error callbacks instance
 */
export function createWebSocketErrorCallbacks() {
    return new WebSocketErrorCallbacks();
}
