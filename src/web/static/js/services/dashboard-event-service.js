/**
 * Dashboard Event Service - V2 Compliant
 * Handles dashboard event management and socket communication
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

import { createSocketEventHandlers } from './socket-event-handlers.js';

export class DashboardEventService {
    constructor(utilityService) {
        this.utilityService = utilityService;
        this.socketHandlers = new Map();
        this.eventListeners = new Map();
        this.eventQueue = [];
        this.isProcessing = false;
        this.socketEventHandlers = createSocketEventHandlers(utilityService);
    }

    /**
     * Setup socket connection and handlers
     */
    setupSocketConnection(socketConfig) {
        try {
            if (!socketConfig.enabled) {
                this.utilityService.logInfo('Socket connection disabled');
                return;
            }

            // Initialize socket connection
            this.initializeSocket(socketConfig);

            // Setup event handlers
            this.socketEventHandlers.setupSocketEventHandlers(this.socketHandlers);

            // Setup heartbeat monitoring
            this.setupHeartbeatMonitoring();

            this.utilityService.logInfo('Socket connection established', socketConfig);
        } catch (error) {
            this.utilityService.logError('Socket connection setup failed', error);
            throw error;
        }
    }

    /**
     * Initialize socket connection
     */
    initializeSocket(config) {
        try {
            // Socket initialization logic would go here
            // This is a placeholder for actual socket implementation
            this.socket = {
                connected: true,
                config,
                emit: (event, data) => this.handleSocketEmit(event, data),
                on: (event, handler) => this.registerSocketHandler(event, handler),
                off: (event, handler) => this.unregisterSocketHandler(event, handler)
            };

            this.utilityService.logInfo('Socket initialized', config);
        } catch (error) {
            this.utilityService.logError('Socket initialization failed', error);
            throw error;
        }
    }

    /**
     * Setup heartbeat monitoring
     */
    setupHeartbeatMonitoring() {
        try {
            this.heartbeatInterval = setInterval(() => {
                if (this.socket?.connected) {
                    this.socket.emit('heartbeat', { timestamp: Date.now() });
                }
            }, 30000); // 30 seconds

            this.utilityService.logInfo('Heartbeat monitoring activated');
        } catch (error) {
            this.utilityService.logError('Heartbeat monitoring setup failed', error);
        }
    }

    /**
     * Add dashboard event listener
     */
    addEventListener(event, listener) {
        try {
            if (!this.eventListeners.has(event)) {
                this.eventListeners.set(event, []);
            }
            this.eventListeners.get(event).push(listener);
            this.utilityService.logDebug(`Event listener added for: ${event}`);
        } catch (error) {
            this.utilityService.logError(`Failed to add event listener for: ${event}`, error);
        }
    }

    /**
     * Remove dashboard event listener
     */
    removeEventListener(event, listener) {
        try {
            const listeners = this.eventListeners.get(event);
            if (listeners) {
                const index = listeners.indexOf(listener);
                if (index > -1) {
                    listeners.splice(index, 1);
                    this.utilityService.logDebug(`Event listener removed for: ${event}`);
                }
            }
        } catch (error) {
            this.utilityService.logError(`Failed to remove event listener for: ${event}`, error);
        }
    }

    /**
     * Dispatch dashboard event
     */
    dispatchEvent(event, data) {
        try {
            const listeners = this.eventListeners.get(event);
            if (listeners) {
                listeners.forEach(listener => {
                    try {
                        listener(data);
                    } catch (error) {
                        this.utilityService.logError(`Event listener error for ${event}`, error);
                    }
                });
            }

            // Also dispatch as DOM custom event
            if (typeof window !== 'undefined') {
                window.dispatchEvent(new CustomEvent(event, { detail: data }));
            }
        } catch (error) {
            this.utilityService.logError(`Event dispatch failed for: ${event}`, error);
        }
    }

    /**
     * Queue event for processing
     */
    queueEvent(event, data) {
        try {
            this.eventQueue.push({ event, data });
            this.processEventQueue();
        } catch (error) {
            this.utilityService.logError('Event queuing failed', error);
        }
    }

    /**
     * Process event queue
     */
    async processEventQueue() {
        if (this.isProcessing || this.eventQueue.length === 0) {
            return;
        }

        this.isProcessing = true;

        try {
            while (this.eventQueue.length > 0) {
                const { event, data } = this.eventQueue.shift();
                await this.processQueuedEvent(event, data);
            }
        } catch (error) {
            this.utilityService.logError('Event queue processing failed', error);
        } finally {
            this.isProcessing = false;
        }
    }

    /**
     * Process individual queued event
     */
    async processQueuedEvent(event, data) {
        try {
            // Add delay for processing
            await new Promise(resolve => setTimeout(resolve, 10));
            this.dispatchEvent(event, data);
        } catch (error) {
            this.utilityService.logError(`Queued event processing failed for: ${event}`, error);
        }
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        try {
            // Clear intervals
            if (this.heartbeatInterval) {
                clearInterval(this.heartbeatInterval);
            }

            // Clear handlers
            this.socketHandlers.clear();
            this.eventListeners.clear();
            this.eventQueue = [];

            this.utilityService.logInfo('Dashboard event service cleaned up');
        } catch (error) {
            this.utilityService.logError('Event service cleanup failed', error);
        }
    }
}

// Factory function for creating dashboard event service
export function createDashboardEventService(utilityService) {
    return new DashboardEventService(utilityService);
}


