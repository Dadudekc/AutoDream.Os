/**
 * Socket Service Module - V2 Compliant
 * Handles WebSocket connections and real-time messaging
 * V2 COMPLIANCE: <200 lines, single responsibility
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - MODULAR COMPONENT
 * @license MIT
 */

class SocketService {
    constructor(config = {}) {
        this.config = { autoConnect: true, reconnectAttempts: 5, reconnectDelay: 1000, heartbeatInterval: 30000, ...config };
        this.socket = null;
        this.connected = false;
        this.reconnectCount = 0;
        this.eventListeners = new Map();
        this.subscriptions = new Set();
        this.heartbeatTimer = null;
        this.isInitialized = false;
    }

    async initialize() {
        if (this.isInitialized) return;
        console.log('🔌 Initializing Socket Service...');
        this.isInitialized = true;
    }

    async connect(url) {
        if (this.connected) return;

        try {
            this.socket = new WebSocket(url || this.config.url);

            return new Promise((resolve, reject) => {
                this.socket.onopen = () => {
                    this.connected = true;
                    this.reconnectCount = 0;
                    this.startHeartbeat();
                    this.emit('connected');
                    console.log('🔌 Connected to WebSocket server');
                    resolve();
                };

                this.socket.onmessage = (event) => this.handleMessage(event.data);
                this.socket.onclose = () => this.handleDisconnect();
                this.socket.onerror = (error) => { console.error('🔌 WebSocket error:', error); reject(error); };

                setTimeout(() => { if (!this.connected) reject(new Error('Connection timeout')); }, 5000);
            });
        } catch (error) {
            console.error('❌ Failed to connect to WebSocket:', error);
            throw error;
        }
    }

    async disconnect() {
        if (!this.connected) return;
        try {
            this.stopHeartbeat();
            if (this.socket) this.socket.close();
            this.connected = false;
            this.emit('disconnected');
            console.log('🔌 Disconnected from WebSocket server');
        } catch (error) {
            console.error('❌ Error disconnecting WebSocket:', error);
        }
    }

    async sendMessage(message) {
        if (!this.connected || !this.socket) throw new Error('WebSocket not connected');

        try {
            const data = typeof message === 'string' ? message : JSON.stringify(message);
            this.socket.send(data);
            this.emit('messageSent', message);
        } catch (error) {
            console.error('❌ Failed to send message:', error);
            throw error;
        }
    }

    subscribeToChannel(channel) {
        if (!this.subscriptions.has(channel)) {
            this.subscriptions.add(channel);
            this.sendMessage({ type: 'subscribe', channel });
            this.emit('subscribed', channel);
        }
    }

    unsubscribeFromChannel(channel) {
        if (this.subscriptions.has(channel)) {
            this.subscriptions.delete(channel);
            this.sendMessage({ type: 'unsubscribe', channel });
            this.emit('unsubscribed', channel);
        }
    }

    handleMessage(data) {
        try {
            const message = typeof data === 'string' ? JSON.parse(data) : data;
            this.emit('message', message);

            switch (message.type) {
                case 'heartbeat': this.handleHeartbeat(); break;
                case 'error': this.emit('error', message.error); break;
                case 'notification': this.emit('notification', message.data); break;
                default: this.emit('data', message);
            }
        } catch (error) {
            console.error('❌ Error handling message:', error);
            this.emit('messageError', error);
        }
    }

    handleDisconnect() {
        this.connected = false;
        this.stopHeartbeat();
        this.emit('disconnected');

        if (this.config.autoConnect && this.reconnectCount < this.config.reconnectAttempts) {
            this.scheduleReconnect();
        }
    }

    scheduleReconnect() {
        this.reconnectCount++;
        const delay = this.config.reconnectDelay * Math.pow(2, this.reconnectCount - 1);
        console.log(`🔄 Scheduling reconnect attempt ${this.reconnectCount} in ${delay}ms`);

        setTimeout(() => {
            this.connect().catch(error => console.error(`❌ Reconnect attempt ${this.reconnectCount} failed:`, error));
        }, delay);
    }

    startHeartbeat() {
        this.stopHeartbeat();
        this.heartbeatTimer = setInterval(() => {
            if (this.connected) this.sendMessage({ type: 'heartbeat', timestamp: Date.now() });
        }, this.config.heartbeatInterval);
    }

    stopHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
    }

    handleHeartbeat() { this.emit('heartbeat'); }

    on(event, callback) {
        if (!this.eventListeners.has(event)) this.eventListeners.set(event, []);
        this.eventListeners.get(event).push(callback);
    }

    off(event, callback) {
        const listeners = this.eventListeners.get(event);
        if (listeners) {
            const index = listeners.indexOf(callback);
            if (index > -1) listeners.splice(index, 1);
        }
    }

    emit(event, data) {
        const listeners = this.eventListeners.get(event);
        if (listeners) listeners.forEach(callback => { try { callback(data); } catch (error) { console.error('Event callback error:', error); } });
    }

    getStats() {
        return {
            connected: this.connected,
            subscriptionsCount: this.subscriptions.size,
            reconnectAttempts: this.reconnectCount,
            initialized: this.isInitialized
        };
    }

    async destroy() {
        await this.disconnect();
        this.subscriptions.clear();
        this.eventListeners.clear();
        this.isInitialized = false;
        console.log('🧹 Socket service cleaned up');
    }
}

export { SocketService };
export default SocketService;
