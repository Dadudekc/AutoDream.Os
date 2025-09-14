/**
 * WebSocket Service - V2 Compliant Real-time Communication
 * V2 COMPLIANT: 150 lines maximum
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description WebSocket service with reconnection and message handling
 */

// ================================
// WEBSOCKET SERVICE CLASS
// ================================

/**
 * WebSocket Service
 * Handles real-time communication with automatic reconnection
 */
export class WebSocketService {
    constructor(options = {}) {
        this.url = options.url || 'ws://localhost:8080/ws';
        this.reconnectInterval = options.reconnectInterval || 5000;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
        this.messageQueue = [];
        this.listeners = new Map();
        this.reconnectAttempts = 0;
        this.isConnected = false;
        this.socket = null;
    }

    /**
     * Initialize WebSocket connection
     */
    async initialize() {
        try {
            await this.connect();
            console.log('🔗 WebSocket service initialized');
        } catch (error) {
            console.error('❌ WebSocket initialization failed:', error);
            throw error;
        }
    }

    /**
     * Connect to WebSocket server
     */
    async connect() {
        return new Promise((resolve, reject) => {
            try {
                this.socket = new WebSocket(this.url);
                
                this.socket.onopen = () => {
                    this.isConnected = true;
                    this.reconnectAttempts = 0;
                    this.processMessageQueue();
                    this.notifyListeners('connected', { url: this.url });
                    console.log('🔗 WebSocket connected');
                    resolve();
                };

                this.socket.onmessage = (event) => {
                    this.handleMessage(event);
                };

                this.socket.onclose = (event) => {
                    this.isConnected = false;
                    this.notifyListeners('disconnected', { event });
                    console.log('🔌 WebSocket disconnected');
                    this.attemptReconnect();
                };

                this.socket.onerror = (error) => {
                    this.notifyListeners('error', { error });
                    console.error('❌ WebSocket error:', error);
                    reject(error);
                };

            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Send message through WebSocket
     */
    send(message) {
        if (this.isConnected && this.socket) {
            try {
                const data = typeof message === 'string' ? message : JSON.stringify(message);
                this.socket.send(data);
            } catch (error) {
                console.error('❌ Failed to send message:', error);
                this.queueMessage(message);
            }
        } else {
            this.queueMessage(message);
        }
    }

    /**
     * Queue message for later sending
     */
    queueMessage(message) {
        this.messageQueue.push({
            message,
            timestamp: Date.now()
        });
    }

    /**
     * Process queued messages
     */
    processMessageQueue() {
        while (this.messageQueue.length > 0 && this.isConnected) {
            const { message } = this.messageQueue.shift();
            this.send(message);
        }
    }

    /**
     * Handle incoming messages
     */
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            this.notifyListeners('message', data);
        } catch (error) {
            console.error('❌ Failed to parse message:', error);
            this.notifyListeners('message', { raw: event.data });
        }
    }

    /**
     * Attempt to reconnect
     */
    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('🚨 Max reconnection attempts reached');
            this.notifyListeners('reconnect_failed', { attempts: this.reconnectAttempts });
            return;
        }

        this.reconnectAttempts++;
        console.log(`🔄 Attempting reconnection (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        
        setTimeout(() => {
            this.connect().catch(error => {
                console.error('❌ Reconnection failed:', error);
            });
        }, this.reconnectInterval);
    }

    /**
     * Add message listener
     */
    addListener(type, listener) {
        if (!this.listeners.has(type)) {
            this.listeners.set(type, new Set());
        }
        this.listeners.get(type).add(listener);
    }

    /**
     * Remove message listener
     */
    removeListener(type, listener) {
        const typeListeners = this.listeners.get(type);
        if (typeListeners) {
            typeListeners.delete(listener);
        }
    }

    /**
     * Notify listeners
     */
    notifyListeners(type, data) {
        const typeListeners = this.listeners.get(type);
        if (typeListeners) {
            typeListeners.forEach(listener => {
                try {
                    listener(data);
                } catch (error) {
                    console.error('❌ WebSocket listener error:', error);
                }
            });
        }
    }

    /**
     * Get connection status
     */
    getStatus() {
        return {
            isConnected: this.isConnected,
            reconnectAttempts: this.reconnectAttempts,
            queuedMessages: this.messageQueue.length,
            url: this.url
        };
    }

    /**
     * Destroy WebSocket service
     */
    async destroy() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
        this.isConnected = false;
        this.messageQueue = [];
        this.listeners.clear();
        console.log('🧹 WebSocket service destroyed');
    }
}

// ================================
// WEBSOCKET UTILITIES
// ================================

/**
 * Create WebSocket service with default settings
 */
export function createWebSocketService(options = {}) {
    return new WebSocketService(options);
}

/**
 * Create WebSocket message handler
 */
export function createMessageHandler(service, messageType, handler) {
    service.addListener('message', (data) => {
        if (data.type === messageType) {
            handler(data);
        }
    });
}

// Export default
export default WebSocketService;