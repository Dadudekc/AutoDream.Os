/**
 * Trading WebSocket Simplified - V2 Compliant
 * Simplified orchestrator for trading WebSocket management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE SIMPLIFICATION
 * @license MIT
 */

import { createUnifiedLoggingSystem } from './unified-logging-module.js';
import { createWebSocketCallbackManagerModule } from './websocket-callback-manager-module.js';
import { createWebSocketConnectionModule } from './websocket-connection-module.js';
import { createWebSocketMessageHandlerModule } from './websocket-message-handler-module.js';
import { createWebSocketSubscriptionModule } from './websocket-subscription-module.js';

// ================================
// TRADING WEBSOCKET SIMPLIFIED ORCHESTRATOR
// ================================

/**
 * Simplified orchestrator for trading WebSocket management
 */
export class TradingWebSocketSimplified {
    constructor() {
        // Initialize unified logging
        this.logger = createUnifiedLoggingSystem("TradingWebSocketSimplified");

        // Log unified systems deployment
        this.logger.logUnifiedSystemsDeployment('trading_websocket_simplified', 'active', {
            version: '2.0.0',
            agentId: 'Agent-7',
            integrationStatus: 'ACTIVE'
        });

        // Initialize modules
        this.callbackManager = createWebSocketCallbackManagerModule();
        this.connectionModule = createWebSocketConnectionModule();
        this.messageHandler = createWebSocketMessageHandlerModule();
        this.subscriptionModule = createWebSocketSubscriptionModule();
    }

    /**
     * Initialize simplified trading WebSocket orchestrator
     */
    initialize(wsUrl) {
        this.logger.logOperationStart('tradingWebSocketSimplifiedInitialization');
        this.connectionModule.initialize(wsUrl);
        this.messageHandler.initialize();
        this.subscriptionModule.initialize(this.connectionModule.sendMessage.bind(this.connectionModule));
        this.connectionModule.setMessageHandler(this.messageHandler.handleMessage.bind(this.messageHandler));

        // Setup cross-module communication
        this._setupModuleCommunication();

        this.logger.logOperationComplete('tradingWebSocketSimplifiedInitialization', {
            modules: ['connection', 'messageHandler', 'subscription', 'callbackManager'],
            unifiedLogging: true
        });
    }

    /**
     * Setup communication between modules
     */
    _setupModuleCommunication() {
        // Connect message handler to callback manager
        this.messageHandler.registerHandler('market_data', (payload) => {
            this.callbackManager.notifyMarketDataCallbacks(payload);
        });

        this.messageHandler.registerHandler('order_update', (payload) => {
            this.callbackManager.notifyOrderCallbacks(payload);
        });

        this.messageHandler.registerHandler('portfolio_update', (payload) => {
            this.callbackManager.notifyPortfolioCallbacks(payload);
        });

        this.messageHandler.registerHandler('error', (payload) => {
            this.callbackManager.notifyErrorCallbacks(payload);
        });
    }

    // ================================
    // CONNECTION METHODS
    // ================================

    async connect() {
        return this.connectionModule.connect();
    }

    disconnect() {
        return this.connectionModule.disconnect();
    }

    isConnected() {
        return this.connectionModule.isWebSocketConnected();
    }

    getConnectionStatus() {
        return this.connectionModule.getConnectionStatus();
    }

    configureReconnection(maxAttempts, baseDelay) {
        this.connectionModule.configureReconnection(maxAttempts, baseDelay);
    }

    getReconnectionInfo() {
        return this.connectionModule.getReconnectionInfo();
    }

    // ================================
    // SUBSCRIPTION METHODS
    // ================================

    subscribeToMarketData(symbols, dataTypes) {
        return this.subscriptionModule.subscribeToMarketData(symbols, dataTypes);
    }

    unsubscribeFromMarketData(symbols) {
        return this.subscriptionModule.unsubscribeFromMarketData(symbols);
    }

    subscribeToOrderUpdates() {
        return this.subscriptionModule.subscribeToOrderUpdates();
    }

    subscribeToPortfolioUpdates() {
        return this.subscriptionModule.subscribeToPortfolioUpdates();
    }

    unsubscribeFromAll() {
        return this.subscriptionModule.unsubscribeFromAll();
    }

    getCurrentSubscriptions() {
        return this.subscriptionModule.getCurrentSubscriptions();
    }

    getSubscriptionStatistics() {
        return this.subscriptionModule.getSubscriptionStatistics();
    }

    // ================================
    // CALLBACK METHODS
    // ================================

    onMarketData(callback) {
        return this.callbackManager.addMarketDataCallback(callback);
    }

    onConnection(callback) {
        return this.callbackManager.addConnectionCallback(callback);
    }

    onError(callback) {
        return this.callbackManager.addErrorCallback(callback);
    }

    onOrder(callback) {
        return this.callbackManager.addOrderCallback(callback);
    }

    onPortfolio(callback) {
        return this.callbackManager.addPortfolioCallback(callback);
    }

    // ================================
    // MESSAGE METHODS
    // ================================

    sendMessage(message) {
        return this.connectionModule.sendMessage(message);
    }

    validateMessage(message) {
        return this.messageHandler.validateMessage(message);
    }

    createMessageEnvelope(type, payload) {
        return this.messageHandler.createMessageEnvelope(type, payload);
    }

    getLatestMarketData() {
        return this.messageHandler.getLatestMarketData();
    }

    // ================================
    // STATISTICS METHODS
    // ================================

    getCallbackStatistics() {
        return this.callbackManager.getCallbackStatistics();
    }

    getStatus() {
        return {
            connected: this.isConnected(),
            connectionStatus: this.getConnectionStatus(),
            subscriptions: this.getCurrentSubscriptions().length,
            callbacks: this.getCallbackStatistics().totalCallbacks,
            latestMarketData: !!this.getLatestMarketData(),
            timestamp: new Date().toISOString()
        };
    }

    getComprehensiveStatistics() {
        return {
            status: this.getStatus(),
            callbackStats: this.getCallbackStatistics(),
            subscriptionStats: this.getSubscriptionStatistics(),
            reconnectionInfo: this.getReconnectionInfo(),
            loggerStats: this.logger.getStatistics(),
            timestamp: new Date().toISOString()
        };
    }

    // ================================
    // CLEANUP
    // ================================

    cleanup() {
        this.subscriptionModule.cleanup();
        this.callbackManager.cleanup();
        this.messageHandler.cleanup();
        this.connectionModule.cleanup();
        this.logger.cleanup();
        this.logger.log('💥 Trading WebSocket Simplified cleanup complete');
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy TradingWebSocketOrchestrator class for backward compatibility
 * @deprecated Use TradingWebSocketSimplified instead
 */
export class TradingWebSocketOrchestrator extends TradingWebSocketSimplified {
    constructor() {
        super();
        console.warn('[DEPRECATED] TradingWebSocketOrchestrator is deprecated. Use TradingWebSocketSimplified instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create simplified trading WebSocket instance
 */
export function createTradingWebSocketSimplified(wsUrl) {
    const websocket = new TradingWebSocketSimplified();
    if (wsUrl) {
        websocket.initialize(wsUrl);
    }
    return websocket;
}

/**
 * Create legacy orchestrator (backward compatibility)
 */
export function createTradingWebSocketOrchestrator(wsUrl) {
    const orchestrator = new TradingWebSocketOrchestrator();
    if (wsUrl) {
        orchestrator.initialize(wsUrl);
    }
    return orchestrator;
}

