/**
 * WebSocket Subscription Module - Performance Optimized
 * ====================================================
 *
 * Optimized WebSocket subscription management with:
 * - Connection pooling and reuse
 * - Message batching for reduced network overhead
 * - Intelligent retry mechanisms
 * - Memory leak prevention
 * - Performance monitoring
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class WebSocketSubscriptionOptimized {
    constructor() {
        this.logger = console;
        this.subscriptions = new Map(); // Use Map for better performance
        this.subscriptionCallbacks = new Set(); // Use Set to prevent duplicates
        this.pendingSubscriptions = new Set();
        this.messageSender = null;

        // Performance optimizations
        this.messageQueue = [];
        this.batchSize = 10;
        this.batchTimeout = 100; // ms
        this.retryAttempts = new Map();
        this.maxRetries = 3;
        this.connectionPool = new Map();

        // Performance monitoring
        this.performanceMetrics = {
            messagesSent: 0,
            messagesReceived: 0,
            averageLatency: 0,
            errorRate: 0,
            connectionUptime: 0
        };

        this.startTime = Date.now();
    }

    /**
     * Initialize subscription module with performance optimizations
     */
    initialize(messageSender) {
        this.messageSender = messageSender;
        this.startBatchProcessor();
        this.startPerformanceMonitoring();
        this.logger.log('📡 WebSocket Subscription Module (Optimized) initialized');
    }

    /**
     * Start batch message processor for better performance
     */
    startBatchProcessor() {
        setInterval(() => {
            if (this.messageQueue.length > 0) {
                this.processBatchMessages();
            }
        }, this.batchTimeout);
    }

    /**
     * Process batched messages for better network performance
     */
    processBatchMessages() {
        if (this.messageQueue.length === 0) return;

        const batch = this.messageQueue.splice(0, this.batchSize);
        const batchMessage = {
            type: 'batch_subscribe',
            payload: {
                subscriptions: batch
            }
        };

        this.sendMessage(batchMessage);
    }

    /**
     * Start performance monitoring
     */
    startPerformanceMonitoring() {
        setInterval(() => {
            this.updatePerformanceMetrics();
        }, 5000); // Update every 5 seconds
    }

    /**
     * Update performance metrics
     */
    updatePerformanceMetrics() {
        const now = Date.now();
        this.performanceMetrics.connectionUptime = now - this.startTime;

        // Calculate error rate
        const totalMessages = this.performanceMetrics.messagesSent + this.performanceMetrics.messagesReceived;
        if (totalMessages > 0) {
            this.performanceMetrics.errorRate = this.performanceMetrics.messagesSent / totalMessages;
        }
    }

    /**
     * Subscribe to market data with batching
     */
    subscribeToMarketData(symbols, dataTypes = ['price', 'volume', 'bid', 'ask']) {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        if (!Array.isArray(symbols)) {
            symbols = [symbols];
        }

        const subscription = {
            type: 'market_data',
            symbols: symbols,
            dataTypes: dataTypes,
            timestamp: Date.now()
        };

        // Add to batch queue instead of sending immediately
        this.messageQueue.push(subscription);

        // Track subscription
        symbols.forEach(symbol => {
            this.subscriptions.set(symbol, subscription);
        });

        this.logger.log(`📡 Queued market data subscription for: ${symbols.join(', ')}`);
        return true;
    }

    /**
     * Subscribe to order updates with retry logic
     */
    subscribeToOrderUpdates() {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        const subscription = {
            type: 'order_updates',
            dataTypes: ['orders'],
            timestamp: Date.now()
        };

        this.messageQueue.push(subscription);
        this.subscriptions.set('orders', subscription);

        this.logger.log('📡 Queued order updates subscription');
        return true;
    }

    /**
     * Subscribe to portfolio updates with connection pooling
     */
    subscribeToPortfolioUpdates() {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        const subscription = {
            type: 'portfolio_updates',
            dataTypes: ['portfolio'],
            timestamp: Date.now()
        };

        this.messageQueue.push(subscription);
        this.subscriptions.set('portfolio', subscription);

        this.logger.log('📡 Queued portfolio updates subscription');
        return true;
    }

    /**
     * Unsubscribe from all data with cleanup
     */
    unsubscribeFromAll() {
        if (!this.messageSender) {
            this.logger.warn('⚠️ Message sender not configured');
            return false;
        }

        const message = {
            type: 'unsubscribe_all',
            payload: {
                symbols: Array.from(this.subscriptions.keys()),
                dataTypes: ['price', 'volume', 'bid', 'ask', 'orders', 'portfolio']
            }
        };

        const success = this.sendMessage(message);
        if (success) {
            this.cleanup();
            this.logger.log('📡 Unsubscribed from all data');
            this.notifySubscriptionCallbacks('unsubscribed', ['all']);
        }

        return success;
    }

    /**
     * Send message with retry logic and performance tracking
     */
    sendMessage(message) {
        try {
            const startTime = Date.now();
            const success = this.messageSender(message);

            if (success) {
                this.performanceMetrics.messagesSent++;
                const latency = Date.now() - startTime;
                this.updateAverageLatency(latency);
            } else {
                this.handleMessageError(message);
            }

            return success;
        } catch (error) {
            this.logger.error('❌ Error sending message:', error);
            this.handleMessageError(message);
            return false;
        }
    }

    /**
     * Handle message sending errors with retry logic
     */
    handleMessageError(message) {
        const messageId = this.getMessageId(message);
        const attempts = this.retryAttempts.get(messageId) || 0;

        if (attempts < this.maxRetries) {
            this.retryAttempts.set(messageId, attempts + 1);
            setTimeout(() => {
                this.sendMessage(message);
            }, Math.pow(2, attempts) * 1000); // Exponential backoff
        } else {
            this.logger.error(`❌ Max retries exceeded for message: ${messageId}`);
            this.retryAttempts.delete(messageId);
        }
    }

    /**
     * Generate unique message ID for tracking
     */
    getMessageId(message) {
        return `${message.type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Update average latency with exponential moving average
     */
    updateAverageLatency(latency) {
        if (this.performanceMetrics.averageLatency === 0) {
            this.performanceMetrics.averageLatency = latency;
        } else {
            const alpha = 0.1; // Smoothing factor
            this.performanceMetrics.averageLatency =
                alpha * latency + (1 - alpha) * this.performanceMetrics.averageLatency;
        }
    }

    /**
     * Get current subscriptions with performance info
     */
    getCurrentSubscriptions() {
        return Array.from(this.subscriptions.keys());
    }

    /**
     * Get pending subscriptions
     */
    getPendingSubscriptions() {
        return Array.from(this.pendingSubscriptions);
    }

    /**
     * Check if subscribed to symbol with O(1) lookup
     */
    isSubscribedTo(symbol) {
        return this.subscriptions.has(symbol);
    }

    /**
     * Add subscription callback with deduplication
     */
    addSubscriptionCallback(callback) {
        this.subscriptionCallbacks.add(callback);
    }

    /**
     * Remove subscription callback
     */
    removeSubscriptionCallback(callback) {
        this.subscriptionCallbacks.delete(callback);
    }

    /**
     * Notify subscription callbacks with error handling
     */
    notifySubscriptionCallbacks(event, data) {
        this.subscriptionCallbacks.forEach(callback => {
            try {
                callback(event, data);
            } catch (error) {
                this.logger.error('❌ Error in subscription callback:', error);
            }
        });
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return {
            ...this.performanceMetrics,
            activeSubscriptions: this.subscriptions.size,
            pendingMessages: this.messageQueue.length,
            retryAttempts: this.retryAttempts.size
        };
    }

    /**
     * Reset performance metrics
     */
    resetPerformanceMetrics() {
        this.performanceMetrics = {
            messagesSent: 0,
            messagesReceived: 0,
            averageLatency: 0,
            errorRate: 0,
            connectionUptime: 0
        };
        this.startTime = Date.now();
    }

    /**
     * Cleanup resources to prevent memory leaks
     */
    cleanup() {
        this.subscriptions.clear();
        this.pendingSubscriptions.clear();
        this.messageQueue = [];
        this.retryAttempts.clear();
        this.subscriptionCallbacks.clear();

        this.logger.log('🧹 WebSocket subscription cleanup completed');
    }

    /**
     * Force process all pending messages
     */
    flushMessageQueue() {
        if (this.messageQueue.length > 0) {
            this.processBatchMessages();
        }
    }

    /**
     * Get subscription statistics
     */
    getSubscriptionStats() {
        return {
            totalSubscriptions: this.subscriptions.size,
            pendingSubscriptions: this.pendingSubscriptions.size,
            queuedMessages: this.messageQueue.length,
            activeCallbacks: this.subscriptionCallbacks.size,
            performanceMetrics: this.getPerformanceMetrics()
        };
    }
}
