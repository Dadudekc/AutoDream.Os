/**
 * Event Utilities - V2 Compliant Module
 * ====================================
 * 
 * Event handling and management utilities.
 * 
 * V2 Compliance: < 300 lines, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class EventUtils {
    constructor() {
        this.listeners = new Map();
        this.logger = console;
    }

    /**
     * Add event listener with automatic cleanup tracking
     */
    addEventListener(element, event, handler, options = {}) {
        const key = `${element.id || element.className}-${event}`;
        
        // Remove existing listener if present
        this.removeEventListener(element, event);
        
        element.addEventListener(event, handler, options);
        this.listeners.set(key, { element, event, handler, options });
    }

    /**
     * Remove event listener
     */
    removeEventListener(element, event) {
        const key = `${element.id || element.className}-${event}`;
        const listener = this.listeners.get(key);
        
        if (listener) {
            listener.element.removeEventListener(listener.event, listener.handler, listener.options);
            this.listeners.delete(key);
        }
    }

    /**
     * Add one-time event listener
     */
    addOnceEventListener(element, event, handler, options = {}) {
        const onceHandler = (e) => {
            handler(e);
            this.removeEventListener(element, event);
        };
        
        this.addEventListener(element, event, onceHandler, options);
    }

    /**
     * Delegate event handling
     */
    delegate(parent, selector, event, handler) {
        const delegatedHandler = (e) => {
            if (e.target.matches(selector)) {
                handler(e);
            }
        };
        
        this.addEventListener(parent, event, delegatedHandler);
    }

    /**
     * Emit custom event
     */
    emitEvent(element, eventName, detail = {}) {
        const event = new CustomEvent(eventName, { detail });
        element.dispatchEvent(event);
    }

    /**
     * Emit global event
     */
    emitGlobalEvent(eventName, detail = {}) {
        const event = new CustomEvent(eventName, { detail });
        document.dispatchEvent(event);
    }

    /**
     * Listen for global event
     */
    onGlobalEvent(eventName, handler) {
        this.addEventListener(document, eventName, handler);
    }

    /**
     * Remove global event listener
     */
    offGlobalEvent(eventName, handler) {
        this.removeEventListener(document, eventName);
    }

    /**
     * Throttle function execution
     */
    throttle(func, delay) {
        let timeoutId;
        let lastExecTime = 0;
        
        return function (...args) {
            const currentTime = Date.now();
            
            if (currentTime - lastExecTime > delay) {
                func.apply(this, args);
                lastExecTime = currentTime;
            } else {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    func.apply(this, args);
                    lastExecTime = Date.now();
                }, delay - (currentTime - lastExecTime));
            }
        };
    }

    /**
     * Debounce function execution
     */
    debounce(func, delay) {
        let timeoutId;
        
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    /**
     * Create event handler with error handling
     */
    createSafeHandler(handler) {
        return (event) => {
            try {
                handler(event);
            } catch (error) {
                this.logger.error('Event handler error:', error);
            }
        };
    }

    /**
     * Add event listener with error handling
     */
    addSafeEventListener(element, event, handler, options = {}) {
        const safeHandler = this.createSafeHandler(handler);
        this.addEventListener(element, event, safeHandler, options);
    }

    /**
     * Remove all event listeners for element
     */
    removeAllListeners(element) {
        const keysToRemove = [];
        
        this.listeners.forEach((listener, key) => {
            if (listener.element === element) {
                listener.element.removeEventListener(listener.event, listener.handler, listener.options);
                keysToRemove.push(key);
            }
        });
        
        keysToRemove.forEach(key => this.listeners.delete(key));
    }

    /**
     * Get all listeners for element
     */
    getElementListeners(element) {
        const elementListeners = [];
        
        this.listeners.forEach((listener, key) => {
            if (listener.element === element) {
                elementListeners.push({
                    key,
                    event: listener.event,
                    handler: listener.handler,
                    options: listener.options
                });
            }
        });
        
        return elementListeners;
    }

    /**
     * Cleanup all event listeners
     */
    cleanup() {
        this.listeners.forEach((listener) => {
            listener.element.removeEventListener(listener.event, listener.handler, listener.options);
        });
        
        this.listeners.clear();
        this.logger.log('🧹 Event Utils cleaned up');
    }

    /**
     * Get listener statistics
     */
    getStats() {
        return {
            totalListeners: this.listeners.size,
            elements: new Set(Array.from(this.listeners.values()).map(l => l.element)).size,
            events: new Set(Array.from(this.listeners.values()).map(l => l.event)).size
        };
    }
}
