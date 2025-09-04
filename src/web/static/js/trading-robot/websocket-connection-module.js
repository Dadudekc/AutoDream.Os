/**
 * WebSocket Connection Module - V2 Compliant
 * WebSocket connection management and reconnection logic
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// WEBSOCKET CONNECTION MODULE
// ================================

/**
 * WebSocket connection management and reconnection logic
 */
export class WebSocketConnectionModule {
    constructor() {
        this.logger = console;
        this.websocket = null;
        this.isConnected = false;
        this.connectionStatus = 'disconnected';
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.wsUrl = null;
    }

    /**
     * Initialize connection module
     */
    initialize(wsUrl) {
        this.wsUrl = wsUrl || this.getDefaultWebSocketUrl();
        this.logger.log('🔌 WebSocket Connection Module initialized');
    }

    /**
     * Get default WebSocket URL
     */
    getDefaultWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/ws/trading/`;
    }

    /**
     * Connect to WebSocket server
     */
    async connect() {
        return new Promise((resolve, reject) => {
            try {
                if (!this.wsUrl) {
                    throw new Error('WebSocket URL not configured');
                }

                this.logger.log('🔗 Connecting to WebSocket...');
                this.websocket = new WebSocket(this.wsUrl);

                this.websocket.onopen = (event) => {
                    this.logger.log('🔗 WebSocket connected');
                    this.isConnected = true;
                    this.connectionStatus = 'connected';
                    this.reconnectAttempts = 0;
                    resolve(event);
                };

                this.websocket.onclose = (event) => {
                    this.logger.log('🔌 WebSocket disconnected');
                    this.isConnected = false;
                    this.connectionStatus = 'disconnected';
                    this.handleReconnect();
                };

                this.websocket.onerror = (error) => {
                    this.logger.error('❌ WebSocket error:', error);
                    this.connectionStatus = 'error';
                    reject(error);
                };

            } catch (error) {
                this.logger.error('❌ WebSocket connection failed:', error);
                reject(error);
            }
        });
    }

    /**
     * Handle reconnection logic
     */
    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * this.reconnectAttempts;

            this.logger.log(`🔄 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms...`);

            setTimeout(() => {
                this.connect().catch(error => {
                    this.logger.error('❌ Reconnection failed:', error);
                });
            }, delay);
        } else {
            this.logger.error('❌ Max reconnection attempts reached');
            this.connectionStatus = 'failed';
        }
    }

    /**
     * Send message through WebSocket
     */
    sendMessage(message) {
        if (!this.isConnected || !this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
            this.logger.warn('⚠️ WebSocket not connected, cannot send message');
            return false;
        }

        try {
            this.websocket.send(JSON.stringify(message));
            return true;
        } catch (error) {
            this.logger.error('❌ Error sending WebSocket message:', error);
            return false;
        }
    }

    /**
     * Set message handler
     */
    setMessageHandler(handler) {
        if (this.websocket) {
            this.websocket.onmessage = handler;
        }
    }

    /**
     * Disconnect WebSocket
     */
    disconnect() {
        if (this.websocket) {
            this.logger.log('🔌 Disconnecting WebSocket...');
            this.websocket.close();
            this.websocket = null;
        }
        this.isConnected = false;
        this.connectionStatus = 'disconnected';
        this.reconnectAttempts = 0;
    }

    /**
     * Check if WebSocket is connected
     */
    isWebSocketConnected() {
        return this.isConnected &&
               this.websocket &&
               this.websocket.readyState === WebSocket.OPEN;
    }

    /**
     * Get connection status
     */
    getConnectionStatus() {
        return this.connectionStatus;
    }

    /**
     * Get WebSocket ready state
     */
    getReadyState() {
        if (!this.websocket) return WebSocket.CLOSED;
        return this.websocket.readyState;
    }

    /**
     * Configure reconnection settings
     */
    configureReconnection(maxAttempts, baseDelay) {
        this.maxReconnectAttempts = maxAttempts || 5;
        this.reconnectDelay = baseDelay || 1000;
    }

    /**
     * Reset reconnection attempts
     */
    resetReconnectionAttempts() {
        this.reconnectAttempts = 0;
    }

    /**
     * Get reconnection info
     */
    getReconnectionInfo() {
        return {
            currentAttempt: this.reconnectAttempts,
            maxAttempts: this.maxReconnectAttempts,
            nextDelay: this.reconnectDelay * (this.reconnectAttempts + 1)
        };
    }

    /**
     * Cleanup connection module
     */
    cleanup() {
        this.disconnect();
        this.logger.log('🧹 WebSocket Connection Module cleanup complete');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create WebSocket connection module instance
 */
export function createWebSocketConnectionModule(wsUrl) {
    const module = new WebSocketConnectionModule();
    if (wsUrl) {
        module.initialize(wsUrl);
    }
    return module;
}

