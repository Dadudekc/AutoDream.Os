/**
 * WebSocket Order & Portfolio Callbacks Module - V2 Compliant
 * Specialized callback management for order and portfolio events
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// ORDER & PORTFOLIO CALLBACKS MODULE
// ================================

/**
 * Specialized callback management for order and portfolio events
 */
export class WebSocketOrderPortfolioCallbacks {
    constructor() {
        this.logger = console;
        this.orderCallbacks = [];
        this.portfolioCallbacks = [];
        this.eventHistory = [];
        this.maxHistorySize = 100;
    }

    /**
     * Add order callback
     */
    addOrderCallback(callback) {
        if (typeof callback === 'function') {
            this.orderCallbacks.push({
                callback,
                id: this.generateCallbackId('order'),
                addedAt: new Date()
            });
            return true;
        }
        this.logger.warn('⚠️ Invalid order callback provided');
        return false;
    }

    /**
     * Add portfolio callback
     */
    addPortfolioCallback(callback) {
        if (typeof callback === 'function') {
            this.portfolioCallbacks.push({
                callback,
                id: this.generateCallbackId('portfolio'),
                addedAt: new Date()
            });
            return true;
        }
        this.logger.warn('⚠️ Invalid portfolio callback provided');
        return false;
    }

    /**
     * Remove order callback
     */
    removeOrderCallback(callback) {
        const index = this.orderCallbacks.findIndex(cb => cb.callback === callback);
        if (index > -1) {
            this.orderCallbacks.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * Remove portfolio callback
     */
    removePortfolioCallback(callback) {
        const index = this.portfolioCallbacks.findIndex(cb => cb.callback === callback);
        if (index > -1) {
            this.portfolioCallbacks.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * Remove callback by ID
     */
    removeCallbackById(id) {
        let removed = false;

        const orderIndex = this.orderCallbacks.findIndex(cb => cb.id === id);
        if (orderIndex > -1) {
            this.orderCallbacks.splice(orderIndex, 1);
            removed = true;
        }

        const portfolioIndex = this.portfolioCallbacks.findIndex(cb => cb.id === id);
        if (portfolioIndex > -1) {
            this.portfolioCallbacks.splice(portfolioIndex, 1);
            removed = true;
        }

        return removed;
    }

    /**
     * Notify order callbacks
     */
    notifyOrderCallbacks(orderData) {
        this.orderCallbacks.forEach(cb => {
            try {
                cb.callback(orderData);
            } catch (error) {
                this.logger.error('❌ Error in order callback:', error);
            }
        });

        // Record event in history
        this.recordEvent('order', orderData);
    }

    /**
     * Notify portfolio callbacks
     */
    notifyPortfolioCallbacks(portfolioData) {
        this.portfolioCallbacks.forEach(cb => {
            try {
                cb.callback(portfolioData);
            } catch (error) {
                this.logger.error('❌ Error in portfolio callback:', error);
            }
        });

        // Record event in history
        this.recordEvent('portfolio', portfolioData);
    }

    /**
     * Get order callbacks
     */
    getOrderCallbacks() {
        return [...this.orderCallbacks];
    }

    /**
     * Get portfolio callbacks
     */
    getPortfolioCallbacks() {
        return [...this.portfolioCallbacks];
    }

    /**
     * Get callback counts
     */
    getCallbackCounts() {
        return {
            orderCallbacks: this.orderCallbacks.length,
            portfolioCallbacks: this.portfolioCallbacks.length,
            totalCallbacks: this.orderCallbacks.length + this.portfolioCallbacks.length
        };
    }

    /**
     * Clear all callbacks
     */
    clearAllCallbacks() {
        this.orderCallbacks = [];
        this.portfolioCallbacks = [];
        this.logger.log('🧹 All order and portfolio callbacks cleared');
    }

    /**
     * Generate unique callback ID
     */
    generateCallbackId(type) {
        return `${type}_cb_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Record event in history
     */
    recordEvent(type, data) {
        this.eventHistory.push({
            type,
            data,
            timestamp: new Date(),
            callbackCount: type === 'order' ? this.orderCallbacks.length : this.portfolioCallbacks.length
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
     * Get event statistics
     */
    getEventStatistics() {
        if (this.eventHistory.length === 0) {
            return { totalEvents: 0 };
        }

        const typeCounts = {};
        this.eventHistory.forEach(event => {
            typeCounts[event.type] = (typeCounts[event.type] || 0) + 1;
        });

        return {
            totalEvents: this.eventHistory.length,
            typeCounts,
            timeRange: {
                oldest: this.eventHistory[0].timestamp,
                newest: this.eventHistory[this.eventHistory.length - 1].timestamp
            }
        };
    }

    /**
     * Validate callback function
     */
    validateCallback(callback, type) {
        if (typeof callback !== 'function') {
            return { valid: false, error: 'Callback must be a function' };
        }

        if (callback.length === 0) {
            return { valid: false, error: `Callback should accept ${type} data parameter` };
        }

        return { valid: true };
    }

    /**
     * Add order callback with validation
     */
    addOrderCallbackValidated(callback) {
        const validation = this.validateCallback(callback, 'order');
        if (!validation.valid) {
            this.logger.error(`❌ Invalid order callback: ${validation.error}`);
            return false;
        }

        return this.addOrderCallback(callback);
    }

    /**
     * Add portfolio callback with validation
     */
    addPortfolioCallbackValidated(callback) {
        const validation = this.validateCallback(callback, 'portfolio');
        if (!validation.valid) {
            this.logger.error(`❌ Invalid portfolio callback: ${validation.error}`);
            return false;
        }

        return this.addPortfolioCallback(callback);
    }

    /**
     * Get statistics
     */
    getStatistics() {
        return {
            callbackCounts: this.getCallbackCounts(),
            eventHistorySize: this.eventHistory.length,
            maxHistorySize: this.maxHistorySize,
            eventStats: this.getEventStatistics()
        };
    }

    /**
     * Cleanup module
     */
    cleanup() {
        this.clearAllCallbacks();
        this.eventHistory = [];
        this.logger.log('🧹 Order and portfolio callbacks module cleanup complete');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create WebSocket order and portfolio callbacks instance
 */
export function createWebSocketOrderPortfolioCallbacks() {
    return new WebSocketOrderPortfolioCallbacks();
}

