/**
 * WebSocket Subscription Module - V2 Compliant
 * WebSocket subscription and unsubscription management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// WEBSOCKET SUBSCRIPTION MODULE
// ================================

/**
 * WebSocket subscription and unsubscription management
 */
export class WebSocketSubscriptionModule {
    constructor() {
        this.logger = console;
        this.subscriptions = new Set();
        this.subscriptionCallbacks = [];
        this.pendingSubscriptions = new Set();
        this.messageSender = null;
    }

    /**
     * Initialize subscription module
     */
    initialize(messageSender) {
        this.messageSender = messageSender;
        this.logger.log('📡 WebSocket Subscription Module initialized');
    }

    /**
     * Subscribe to market data
     */
    subscribeToMarketData(symbols, dataTypes = ['price', 'volume', 'bid', 'ask']) {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        if (!Array.isArray(symbols)) {
            symbols = [symbols];
        }

        const message = {
            type: 'subscribe',
            payload: {
                symbols: symbols,
                data_types: dataTypes
            }
        };

        const success = this.messageSender(message);
        if (success) {
            // Add to subscriptions
            symbols.forEach(symbol => this.subscriptions.add(symbol));
            // Track pending subscriptions
            symbols.forEach(symbol => this.pendingSubscriptions.add(symbol));

            this.logger.log('📡 Subscribed to market data:', symbols);
            this.notifySubscriptionCallbacks('subscribed', symbols);
        }

        return success;
    }

    /**
     * Unsubscribe from market data
     */
    unsubscribeFromMarketData(symbols) {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        if (!Array.isArray(symbols)) {
            symbols = [symbols];
        }

        const message = {
            type: 'unsubscribe',
            payload: {
                symbols: symbols
            }
        };

        const success = this.messageSender(message);
        if (success) {
            // Remove from subscriptions
            symbols.forEach(symbol => {
                this.subscriptions.delete(symbol);
                this.pendingSubscriptions.delete(symbol);
            });

            this.logger.log('📡 Unsubscribed from market data:', symbols);
            this.notifySubscriptionCallbacks('unsubscribed', symbols);
        }

        return success;
    }

    /**
     * Subscribe to order updates
     */
    subscribeToOrderUpdates() {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        const message = {
            type: 'subscribe',
            payload: {
                data_types: ['orders']
            }
        };

        const success = this.messageSender(message);
        if (success) {
            this.logger.log('📡 Subscribed to order updates');
            this.notifySubscriptionCallbacks('subscribed', ['orders']);
        }

        return success;
    }

    /**
     * Subscribe to portfolio updates
     */
    subscribeToPortfolioUpdates() {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        const message = {
            type: 'subscribe',
            payload: {
                data_types: ['portfolio']
            }
        };

        const success = this.messageSender(message);
        if (success) {
            this.logger.log('📡 Subscribed to portfolio updates');
            this.notifySubscriptionCallbacks('subscribed', ['portfolio']);
        }

        return success;
    }

    /**
     * Unsubscribe from all data
     */
    unsubscribeFromAll() {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        const message = {
            type: 'unsubscribe',
            payload: {
                symbols: Array.from(this.subscriptions),
                data_types: ['price', 'volume', 'bid', 'ask', 'orders', 'portfolio']
            }
        };

        const success = this.messageSender(message);
        if (success) {
            this.subscriptions.clear();
            this.pendingSubscriptions.clear();
            this.logger.log('📡 Unsubscribed from all data');
            this.notifySubscriptionCallbacks('unsubscribed', ['all']);
        }

        return success;
    }

    /**
     * Get current subscriptions
     */
    getCurrentSubscriptions() {
        return Array.from(this.subscriptions);
    }

    /**
     * Get pending subscriptions
     */
    getPendingSubscriptions() {
        return Array.from(this.pendingSubscriptions);
    }

    /**
     * Check if subscribed to symbol
     */
    isSubscribedTo(symbol) {
        return this.subscriptions.has(symbol);
    }

    /**
     * Confirm subscription (remove from pending)
     */
    confirmSubscription(symbol) {
        this.pendingSubscriptions.delete(symbol);
    }

    /**
     * Confirm multiple subscriptions
     */
    confirmSubscriptions(symbols) {
        symbols.forEach(symbol => this.confirmSubscription(symbol));
    }

    /**
     * Add subscription callback
     */
    addSubscriptionCallback(callback) {
        if (typeof callback === 'function') {
            this.subscriptionCallbacks.push(callback);
        }
    }

    /**
     * Remove subscription callback
     */
    removeSubscriptionCallback(callback) {
        this.subscriptionCallbacks = this.subscriptionCallbacks.filter(cb => cb !== callback);
    }

    /**
     * Notify subscription callbacks
     */
    notifySubscriptionCallbacks(action, data) {
        this.subscriptionCallbacks.forEach(callback => {
            try {
                callback(action, data);
            } catch (error) {
                this.logger.error('❌ Error in subscription callback:', error);
            }
        });
    }

    /**
     * Get subscription statistics
     */
    getSubscriptionStatistics() {
        return {
            activeSubscriptions: this.subscriptions.size,
            pendingSubscriptions: this.pendingSubscriptions.size,
            totalSubscriptions: this.subscriptions.size + this.pendingSubscriptions.size,
            subscriptionCallbacks: this.subscriptionCallbacks.length
        };
    }

    /**
     * Validate subscription request
     */
    validateSubscriptionRequest(symbols, dataTypes) {
        if (!Array.isArray(symbols) || symbols.length === 0) {
            return { valid: false, error: 'Symbols must be a non-empty array' };
        }

        if (symbols.some(symbol => typeof symbol !== 'string' || symbol.trim() === '')) {
            return { valid: false, error: 'All symbols must be non-empty strings' };
        }

        if (dataTypes && (!Array.isArray(dataTypes) || dataTypes.length === 0)) {
            return { valid: false, error: 'Data types must be a non-empty array if provided' };
        }

        return { valid: true };
    }

    /**
     * Batch subscribe to multiple symbols
     */
    batchSubscribe(symbols, dataTypes = ['price', 'volume']) {
        const validation = this.validateSubscriptionRequest(symbols, dataTypes);
        if (!validation.valid) {
            this.logger.error('❌ Invalid subscription request:', validation.error);
            return false;
        }

        return this.subscribeToMarketData(symbols, dataTypes);
    }

    /**
     * Batch unsubscribe from multiple symbols
     */
    batchUnsubscribe(symbols) {
        if (!Array.isArray(symbols) || symbols.length === 0) {
            this.logger.error('❌ Invalid unsubscription request: symbols must be a non-empty array');
            return false;
        }

        return this.unsubscribeFromMarketData(symbols);
    }

    /**
     * Set message sender
     */
    setMessageSender(sender) {
        this.messageSender = sender;
    }

    /**
     * Clear all subscriptions
     */
    clearSubscriptions() {
        this.subscriptions.clear();
        this.pendingSubscriptions.clear();
    }

    /**
     * Cleanup subscription module
     */
    cleanup() {
        this.clearSubscriptions();
        this.subscriptionCallbacks = [];
        this.messageSender = null;
        this.logger.log('🧹 WebSocket Subscription Module cleanup complete');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create WebSocket subscription module instance
 */
export function createWebSocketSubscriptionModule(messageSender) {
    const module = new WebSocketSubscriptionModule();
    if (messageSender) {
        module.initialize(messageSender);
    }
    return module;
}

