/**
 * Trading WebSocket Core Module - V2 Compliant
 * Consolidated WebSocket functionality for Trading Robot
 * Combines all websocket-related modules into unified system
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - PHASE 2 CONSOLIDATION
 * @license MIT
 */

// ================================
// TRADING WEBSOCKET CORE MODULE
// ================================

/**
 * Unified Trading WebSocket Core Module
 * Consolidates all WebSocket functionality into a single V2-compliant module
 */
export class TradingWebSocketCore {
    constructor() {
        this.logger = console;
        this.websocket = null;
        this.isConnected = false;
        this.connectionStatus = 'disconnected';
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.wsUrl = null;
        this.messageHandlers = new Map();
        this.subscriptions = new Set();
        this.callbacks = {
            onConnect: [],
            onDisconnect: [],
            onMessage: [],
            onError: [],
            onReconnect: []
        };
        this.messageQueue = [];
        this.isReconnecting = false;
    }

    /**
     * Initialize WebSocket connection
     */
    async initialize(wsUrl) {
        try {
            this.wsUrl = wsUrl;
            this.logger.log(`Initializing Trading WebSocket Core with URL: ${wsUrl}`);

            await this.connect();
            this.setupMessageHandlers();
            this.startHeartbeat();

        } catch (error) {
            this.logger.error('Failed to initialize Trading WebSocket Core:', error);
            throw error;
        }
    }

    /**
     * Connect to WebSocket server
     */
    async connect() {
        return new Promise((resolve, reject) => {
            try {
                this.websocket = new WebSocket(this.wsUrl);

                this.websocket.onopen = () => {
                    this.isConnected = true;
                    this.connectionStatus = 'connected';
                    this.reconnectAttempts = 0;
                    this.logger.log('WebSocket connected successfully');

                    // Process queued messages
                    this.processMessageQueue();

                    // Trigger connect callbacks
                    this.callbacks.onConnect.forEach(callback => callback());

                    resolve();
                };

                this.websocket.onmessage = (event) => {
                    this.handleMessage(event.data);
                };

                this.websocket.onclose = () => {
                    this.isConnected = false;
                    this.connectionStatus = 'disconnected';
                    this.logger.log('WebSocket disconnected');

                    // Trigger disconnect callbacks
                    this.callbacks.onDisconnect.forEach(callback => callback());

                    // Attempt reconnection if not intentional
                    if (!this.isReconnecting) {
                        this.attemptReconnection();
                    }
                };

                this.websocket.onerror = (error) => {
                    this.logger.error('WebSocket error:', error);

                    // Trigger error callbacks
                    this.callbacks.onError.forEach(callback => callback(error));
                };

            } catch (error) {
                this.logger.error('Failed to create WebSocket connection:', error);
                reject(error);
            }
        });
    }

    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.close();
        }
        this.isConnected = false;
        this.connectionStatus = 'disconnected';
        this.logger.log('WebSocket disconnected by user');
    }

    /**
     * Send message to WebSocket server
     */
    sendMessage(message) {
        if (!this.isConnected) {
            this.logger.warn('WebSocket not connected, queuing message');
            this.messageQueue.push(message);
            return false;
        }

        try {
            const messageStr = typeof message === 'string' ? message : JSON.stringify(message);
            this.websocket.send(messageStr);
            return true;
        } catch (error) {
            this.logger.error('Failed to send message:', error);
            return false;
        }
    }

    /**
     * Subscribe to market data
     */
    subscribeToMarketData(symbol) {
        if (!this.subscriptions.has(symbol)) {
            this.subscriptions.add(symbol);
            this.sendMessage({
                type: 'subscribe',
                symbol: symbol,
                channel: 'market_data'
            });
            this.logger.log(`Subscribed to market data for: ${symbol}`);
        }
    }

    /**
     * Unsubscribe from market data
     */
    unsubscribeFromMarketData(symbol) {
        if (this.subscriptions.has(symbol)) {
            this.subscriptions.delete(symbol);
            this.sendMessage({
                type: 'unsubscribe',
                symbol: symbol,
                channel: 'market_data'
            });
            this.logger.log(`Unsubscribed from market data for: ${symbol}`);
        }
    }

    /**
     * Subscribe to order updates
     */
    subscribeToOrders() {
        this.sendMessage({
            type: 'subscribe',
            channel: 'orders'
        });
        this.logger.log('Subscribed to order updates');
    }

    /**
     * Subscribe to portfolio updates
     */
    subscribeToPortfolio() {
        this.sendMessage({
            type: 'subscribe',
            channel: 'portfolio'
        });
        this.logger.log('Subscribed to portfolio updates');
    }

    /**
     * Send trading order
     */
    sendOrder(order) {
        const orderMessage = {
            type: 'order',
            order: order,
            timestamp: new Date().toISOString()
        };

        this.sendMessage(orderMessage);
        this.logger.log('Order sent:', order);
    }

    /**
     * Cancel order
     */
    cancelOrder(orderId) {
        this.sendMessage({
            type: 'cancel_order',
            orderId: orderId
        });
        this.logger.log(`Order cancellation sent for ID: ${orderId}`);
    }

    /**
     * Handle incoming messages
     */
    handleMessage(data) {
        try {
            const message = typeof data === 'string' ? JSON.parse(data) : data;

            // Trigger message callbacks
            this.callbacks.onMessage.forEach(callback => callback(message));

            // Route message to appropriate handler
            this.routeMessage(message);

        } catch (error) {
            this.logger.error('Failed to parse WebSocket message:', error);
        }
    }

    /**
     * Route message to appropriate handler
     */
    routeMessage(message) {
        const handler = this.messageHandlers.get(message.type);
        if (handler) {
            handler(message);
        } else {
            this.logger.warn('No handler found for message type:', message.type);
        }
    }

    /**
     * Register message handler
     */
    registerMessageHandler(messageType, handler) {
        this.messageHandlers.set(messageType, handler);
        this.logger.log(`Message handler registered for type: ${messageType}`);
    }

    /**
     * Unregister message handler
     */
    unregisterMessageHandler(messageType) {
        this.messageHandlers.delete(messageType);
        this.logger.log(`Message handler unregistered for type: ${messageType}`);
    }

    /**
     * Setup default message handlers
     */
    setupMessageHandlers() {
        // Market data handler
        this.registerMessageHandler('market_data', (message) => {
            this.handleMarketData(message);
        });

        // Order update handler
        this.registerMessageHandler('order_update', (message) => {
            this.handleOrderUpdate(message);
        });

        // Portfolio update handler
        this.registerMessageHandler('portfolio_update', (message) => {
            this.handlePortfolioUpdate(message);
        });

        // Error handler
        this.registerMessageHandler('error', (message) => {
            this.handleError(message);
        });
    }

    /**
     * Handle market data messages
     */
    handleMarketData(message) {
        // Process market data (price updates, trades, etc.)
        this.logger.log('Market data received:', message.symbol, message.price);
    }

    /**
     * Handle order update messages
     */
    handleOrderUpdate(message) {
        // Process order updates (filled, partial fill, cancelled, etc.)
        this.logger.log('Order update received:', message.orderId, message.status);
    }

    /**
     * Handle portfolio update messages
     */
    handlePortfolioUpdate(message) {
        // Process portfolio updates (positions, balances, etc.)
        this.logger.log('Portfolio update received');
    }

    /**
     * Handle error messages
     */
    handleError(message) {
        this.logger.error('WebSocket error received:', message.error);
    }

    /**
     * Add event callback
     */
    addEventCallback(event, callback) {
        if (this.callbacks[event]) {
            this.callbacks[event].push(callback);
            this.logger.log(`Callback added for event: ${event}`);
        } else {
            this.logger.warn(`Unknown event type: ${event}`);
        }
    }

    /**
     * Remove event callback
     */
    removeEventCallback(event, callback) {
        if (this.callbacks[event]) {
            const index = this.callbacks[event].indexOf(callback);
            if (index > -1) {
                this.callbacks[event].splice(index, 1);
                this.logger.log(`Callback removed for event: ${event}`);
            }
        }
    }

    /**
     * Attempt reconnection
     */
    async attemptReconnection() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.logger.error('Max reconnection attempts reached');
            return;
        }

        this.isReconnecting = true;
        this.reconnectAttempts++;

        this.logger.log(`Attempting reconnection ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);

        // Trigger reconnect callbacks
        this.callbacks.onReconnect.forEach(callback => callback(this.reconnectAttempts));

        setTimeout(async () => {
            try {
                await this.connect();
                this.isReconnecting = false;
                this.logger.log('Reconnection successful');
            } catch (error) {
                this.logger.error('Reconnection failed:', error);
                this.attemptReconnection(); // Try again
            }
        }, this.reconnectDelay * this.reconnectAttempts);
    }

    /**
     * Start heartbeat mechanism
     */
    startHeartbeat() {
        setInterval(() => {
            if (this.isConnected) {
                this.sendMessage({ type: 'ping' });
            }
        }, 30000); // Send ping every 30 seconds
    }

    /**
     * Process queued messages
     */
    processMessageQueue() {
        while (this.messageQueue.length > 0 && this.isConnected) {
            const message = this.messageQueue.shift();
            this.sendMessage(message);
        }
    }

    /**
     * Get connection status
     */
    getConnectionStatus() {
        return {
            isConnected: this.isConnected,
            status: this.connectionStatus,
            reconnectAttempts: this.reconnectAttempts,
            subscriptions: Array.from(this.subscriptions),
            queuedMessages: this.messageQueue.length
        };
    }
}

/**
 * WebSocket Message Handler - Handles different message types
 */
class WebSocketMessageHandler {
    constructor(websocketCore) {
        this.websocketCore = websocketCore;
        this.handlers = new Map();
    }

    registerHandler(messageType, handler) {
        this.handlers.set(messageType, handler);
    }

    unregisterHandler(messageType) {
        this.handlers.delete(messageType);
    }

    handleMessage(message) {
        const handler = this.handlers.get(message.type);
        if (handler) {
            handler(message);
        }
    }
}

/**
 * WebSocket Subscription Manager - Manages data subscriptions
 */
class WebSocketSubscriptionManager {
    constructor(websocketCore) {
        this.websocketCore = websocketCore;
        this.activeSubscriptions = new Set();
    }

    subscribe(channel, symbol = null) {
        const subscriptionKey = symbol ? `${channel}:${symbol}` : channel;

        if (!this.activeSubscriptions.has(subscriptionKey)) {
            this.activeSubscriptions.add(subscriptionKey);
            this.websocketCore.sendMessage({
                type: 'subscribe',
                channel: channel,
                symbol: symbol
            });
        }
    }

    unsubscribe(channel, symbol = null) {
        const subscriptionKey = symbol ? `${channel}:${symbol}` : channel;

        if (this.activeSubscriptions.has(subscriptionKey)) {
            this.activeSubscriptions.delete(subscriptionKey);
            this.websocketCore.sendMessage({
                type: 'unsubscribe',
                channel: channel,
                symbol: symbol
            });
        }
    }

    unsubscribeAll() {
        this.activeSubscriptions.forEach(subscription => {
            const [channel, symbol] = subscription.split(':');
            this.unsubscribe(channel, symbol || null);
        });
        this.activeSubscriptions.clear();
    }

    getActiveSubscriptions() {
        return Array.from(this.activeSubscriptions);
    }
}

// ================================
// EXPORTS
// ================================

export {
    TradingWebSocketCore,
    WebSocketMessageHandler,
    WebSocketSubscriptionManager
};
