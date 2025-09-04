/**
 * Event Management Module - V2 Compliant
 * DOM event handling utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// EVENT MANAGEMENT MODULE
// ================================

/**
 * Event management utilities for DOM event handling
 */
export class EventManagementModule {
    constructor() {
        this.logger = console;
        this.eventListeners = new Map();
    }

    /**
     * Add event listener with cleanup tracking
     */
    addEventListener(element, event, handler, options = {}) {
        if (!element || !event || !handler) {
            this.logger.warn('Invalid parameters for addEventListener');
            return null;
        }

        try {
            const listenerId = this.generateListenerId(element, event, handler);
            element.addEventListener(event, handler, options);

            // Track listener for cleanup
            const listenerInfo = { element, event, handler, options, id: listenerId };
            this.eventListeners.set(listenerId, listenerInfo);

            return listenerInfo;
        } catch (error) {
            this.logger.error('Failed to add event listener', error);
            return null;
        }
    }

    /**
     * Remove event listener
     */
    removeEventListener(element, event, handler, options = {}) {
        if (!element || !event || !handler) {
            this.logger.warn('Invalid parameters for removeEventListener');
            return false;
        }

        try {
            element.removeEventListener(event, handler, options);

            // Remove from tracking
            const listenerId = this.generateListenerId(element, event, handler);
            this.eventListeners.delete(listenerId);

            return true;
        } catch (error) {
            this.logger.error('Failed to remove event listener', error);
            return false;
        }
    }

    /**
     * Remove all event listeners for an element
     */
    removeAllListeners(element) {
        if (!element) return false;

        try {
            const listenersToRemove = [];

            // Find all listeners for this element
            this.eventListeners.forEach((listener, id) => {
                if (listener.element === element) {
                    listenersToRemove.push(listener);
                }
            });

            // Remove each listener
            listenersToRemove.forEach(listener => {
                this.removeEventListener(listener.element, listener.event, listener.handler, listener.options);
            });

            return true;
        } catch (error) {
            this.logger.error('Failed to remove all listeners', error);
            return false;
        }
    }

    /**
     * Add multiple event listeners at once
     */
    addMultipleListeners(element, events) {
        if (!element || !events) return [];

        const addedListeners = [];

        try {
            Object.entries(events).forEach(([event, config]) => {
                if (typeof config === 'function') {
                    const listener = this.addEventListener(element, event, config);
                    if (listener) addedListeners.push(listener);
                } else if (typeof config === 'object') {
                    const listener = this.addEventListener(element, event, config.handler, config.options);
                    if (listener) addedListeners.push(listener);
                }
            });
        } catch (error) {
            this.logger.error('Failed to add multiple listeners', error);
        }

        return addedListeners;
    }

    /**
     * Generate unique listener ID
     */
    generateListenerId(element, event, handler) {
        return `${element.id || element.className || 'element'}_${event}_${handler.name || 'anonymous'}_${Date.now()}`;
    }

    /**
     * Get all tracked listeners
     */
    getTrackedListeners() {
        return Array.from(this.eventListeners.values());
    }

    /**
     * Clear all tracked listeners (cleanup)
     */
    clearAllListeners() {
        try {
            this.eventListeners.forEach(listener => {
                this.removeEventListener(listener.element, listener.event, listener.handler, listener.options);
            });
            this.eventListeners.clear();
            return true;
        } catch (error) {
            this.logger.error('Failed to clear all listeners', error);
            return false;
        }
    }

    /**
     * Dispatch custom event
     */
    dispatchEvent(element, eventName, detail = {}) {
        if (!element || !eventName) return false;

        try {
            const event = new CustomEvent(eventName, { detail });
            element.dispatchEvent(event);
            return true;
        } catch (error) {
            this.logger.error(`Failed to dispatch event: ${eventName}`, error);
            return false;
        }
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create event management module instance
 */
export function createEventManagementModule() {
    return new EventManagementModule();
}

