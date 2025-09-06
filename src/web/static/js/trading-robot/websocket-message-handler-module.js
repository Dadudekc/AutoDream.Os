/**
 * WebSocket Message Handler Module - V2 Compliant
 * WebSocket message parsing and handling
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// WEBSOCKET MESSAGE HANDLER MODULE
// ================================

/**
 * WebSocket message parsing and handling
 */
export class WebSocketMessageHandlerModule {
    constructor() {
        this.logger = console;
        this.messageHandlers = new Map();
        this.latestMarketData = null;
        this.eventDispatcher = null;
    }

    /**
     * Initialize message handler module
     */
    initialize(eventDispatcher = null) {
        this.eventDispatcher = eventDispatcher || document;
        this.setupDefaultHandlers();
        this.logger.log('📨 WebSocket Message Handler Module initialized');
    }

    /**
     * Setup default message handlers
     */
    setupDefaultHandlers() {
        this.registerHandler('market_data', this.handleMarketData.bind(this));
        this.registerHandler('order_update', this.handleOrderUpdate.bind(this));
        this.registerHandler('portfolio_update', this.handlePortfolioUpdate.bind(this));
        this.registerHandler('error', this.handleError.bind(this));
    }

    /**
     * Register a message handler
     */
    registerHandler(messageType, handler) {
        this.messageHandlers.set(messageType, handler);
    }

    /**
     * Unregister a message handler
     */
    unregisterHandler(messageType) {
        this.messageHandlers.delete(messageType);
    }

    /**
     * Handle incoming WebSocket message
     */
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);

            if (!data.type) {
                this.logger.warn('⚠️ Received message without type:', data);
                return;
            }

            const handler = this.messageHandlers.get(data.type);
            if (handler) {
                handler(data.payload, data);
            } else {
                this.logger.warn('⚠️ No handler registered for message type:', data.type);
            }
        } catch (error) {
            this.logger.error('❌ Error parsing WebSocket message:', error);
        }
    }

    /**
     * Handle market data messages
     */
    handleMarketData(marketData, fullMessage) {
        this.latestMarketData = marketData;

        // Dispatch custom event
        if (this.eventDispatcher) {
            const event = new CustomEvent('trading:marketData', {
                detail: { marketData, fullMessage }
            });
            this.eventDispatcher.dispatchEvent(event);
        }

        this.logger.log('📊 Market data received:', marketData);
    }

    /**
     * Handle order update messages
     */
    handleOrderUpdate(orderData, fullMessage) {
        // Dispatch custom event for order updates
        if (this.eventDispatcher) {
            const event = new CustomEvent('trading:orderUpdate', {
                detail: { orderData, fullMessage }
            });
            this.eventDispatcher.dispatchEvent(event);
        }

        this.logger.log('📝 Order update received:', orderData);
    }

    /**
     * Handle portfolio update messages
     */
    handlePortfolioUpdate(portfolioData, fullMessage) {
        // Dispatch custom event for portfolio updates
        if (this.eventDispatcher) {
            const event = new CustomEvent('trading:portfolioUpdate', {
                detail: { portfolioData, fullMessage }
            });
            this.eventDispatcher.dispatchEvent(event);
        }

        this.logger.log('💼 Portfolio update received:', portfolioData);
    }

    /**
     * Handle error messages
     */
    handleError(errorData, fullMessage) {
        this.logger.error('❌ Trading WebSocket error:', errorData);

        // Dispatch custom event for errors
        if (this.eventDispatcher) {
            const event = new CustomEvent('trading:error', {
                detail: { errorData, fullMessage }
            });
            this.eventDispatcher.dispatchEvent(event);
        }
    }

    /**
     * Get latest market data
     */
    getLatestMarketData() {
        return this.latestMarketData;
    }

    /**
     * Clear latest market data
     */
    clearLatestMarketData() {
        this.latestMarketData = null;
    }

    /**
     * Get all registered message types
     */
    getRegisteredMessageTypes() {
        return Array.from(this.messageHandlers.keys());
    }

    /**
     * Check if handler exists for message type
     */
    hasHandler(messageType) {
        return this.messageHandlers.has(messageType);
    }

    /**
     * Get message handler statistics
     */
    getHandlerStatistics() {
        return {
            registeredHandlers: this.messageHandlers.size,
            messageTypes: this.getRegisteredMessageTypes(),
            hasLatestMarketData: !!this.latestMarketData
        };
    }

    /**
     * Process message with custom logic
     */
    processMessage(message, customProcessor) {
        try {
            if (typeof customProcessor === 'function') {
                return customProcessor(message);
            }
            return this.handleMessage({ data: JSON.stringify(message) });
        } catch (error) {
            this.logger.error('❌ Error processing message:', error);
            return false;
        }
    }

    /**
     * Validate message structure
     */
    validateMessage(message) {
        try {
            const data = typeof message === 'string' ? JSON.parse(message) : message;

            if (!data || typeof data !== 'object') {
                return { valid: false, error: 'Message is not a valid object' };
            }

            if (!data.type || typeof data.type !== 'string') {
                return { valid: false, error: 'Message missing or invalid type field' };
            }

            return { valid: true };
        } catch (error) {
            return { valid: false, error: `JSON parsing error: ${error.message}` };
        }
    }

    /**
     * Create message envelope
     */
    createMessageEnvelope(type, payload) {
        return {
            type,
            payload,
            timestamp: new Date().toISOString(),
            version: '1.0'
        };
    }

    /**
     * Set event dispatcher
     */
    setEventDispatcher(dispatcher) {
        this.eventDispatcher = dispatcher;
    }

    /**
     * Cleanup message handler module
     */
    cleanup() {
        this.messageHandlers.clear();
        this.latestMarketData = null;
        this.eventDispatcher = null;
        this.logger.log('🧹 WebSocket Message Handler Module cleanup complete');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create WebSocket message handler module instance
 */
export function createWebSocketMessageHandlerModule(eventDispatcher) {
    const module = new WebSocketMessageHandlerModule();
    if (eventDispatcher !== undefined) {
        module.initialize(eventDispatcher);
    }
    return module;
}
