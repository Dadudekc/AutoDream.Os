/**
 * Navigation Event Handler - Event Management Module
 * Handles navigation events and user interactions
 * V2 Compliance: Under 300-line limit achieved
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 1.0.0 - V2 Compliance Event Handler
 * @license MIT
 */

import { isValidNavigationItem } from './navigation-config-manager.js';

/**
 * Navigation event handler class
 */
export class NavigationEventHandler {
    constructor() {
        this.navElement = null;
        this.eventListeners = new Map();
        this.isInitialized = false;
    }

    /**
     * Initialize event handler
     */
    initialize(navElement) {
        if (this.isInitialized) {
            console.warn('⚠️ Event handler already initialized');
            return;
        }

        this.navElement = navElement;
        if (!this.navElement) {
            console.warn('⚠️ Navigation element not provided');
            return;
        }

        this.setupEventListeners();
        this.isInitialized = true;
        console.log('🎧 Navigation event handler initialized');
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Click handler for navigation items
        const clickHandler = (event) => {
            this.handleNavigationClick(event);
        };

        this.navElement.addEventListener('click', clickHandler);
        this.eventListeners.set('click', clickHandler);

        // Keyboard navigation handler
        const keyHandler = (event) => {
            this.handleKeyboardNavigation(event);
        };

        this.navElement.addEventListener('keydown', keyHandler);
        this.eventListeners.set('keydown', keyHandler);

        console.log('🎧 Navigation event listeners configured');
    }

    /**
     * Handle navigation click
     */
    handleNavigationClick(event) {
        const target = event.target.closest('.nav-link, [data-view]');
        if (!target) return;

        event.preventDefault();

        const view = target.dataset.view || target.getAttribute('data-view');
        if (!view) {
            console.warn('⚠️ Navigation item missing view data');
            return;
        }

        if (!isValidNavigationItem(view)) {
            console.error(`❌ Invalid navigation view: ${view}`);
            return;
        }

        // Emit navigation event
        this.emitEvent('navigationClick', {
            view,
            element: target,
            event: event,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Handle keyboard navigation
     */
    handleKeyboardNavigation(event) {
        const target = event.target.closest('.nav-link, [data-view]');
        if (!target) return;

        // Handle Enter and Space keys
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            target.click();
        }

        // Handle arrow key navigation
        if (event.key.startsWith('Arrow')) {
            this.handleArrowNavigation(event, target);
        }
    }

    /**
     * Handle arrow key navigation
     */
    handleArrowNavigation(event, currentElement) {
        const navItems = Array.from(this.navElement.querySelectorAll('.nav-link, [data-view]'));
        const currentIndex = navItems.indexOf(currentElement);

        if (currentIndex === -1) return;

        let nextIndex;

        switch (event.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                nextIndex = (currentIndex + 1) % navItems.length;
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
                nextIndex = currentIndex === 0 ? navItems.length - 1 : currentIndex - 1;
                break;
            default:
                return;
        }

        event.preventDefault();
        const nextElement = navItems[nextIndex];
        if (nextElement) {
            nextElement.focus();

            // Emit arrow navigation event
            this.emitEvent('arrowNavigation', {
                direction: event.key,
                fromIndex: currentIndex,
                toIndex: nextIndex,
                element: nextElement,
                timestamp: new Date().toISOString()
            });
        }
    }

    /**
     * Add event listener
     */
    addEventListener(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }

    /**
     * Remove event listener
     */
    removeEventListener(event, callback) {
        if (this.eventListeners.has(event)) {
            const listeners = this.eventListeners.get(event);
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    /**
     * Emit event to listeners
     */
    emitEvent(event, data) {
        if (this.eventListeners.has(event)) {
            this.eventListeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in navigation event listener:`, error);
                }
            });
        }
    }

    /**
     * Handle navigation change
     */
    handleNavigationChange(newView, previousView) {
        this.emitEvent('navigationChange', {
            newView,
            previousView,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Handle navigation error
     */
    handleNavigationError(error, view) {
        this.emitEvent('navigationError', {
            error: error.message,
            view,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Cleanup event listeners
     */
    cleanup() {
        if (!this.navElement) return;

        // Remove all event listeners
        this.eventListeners.forEach((listeners, event) => {
            listeners.forEach(callback => {
                this.navElement.removeEventListener(event, callback);
            });
        });

        this.eventListeners.clear();
        console.log('🧹 Navigation event listeners cleaned up');
    }
}

/**
 * Create navigation event handler instance
 */
export function createNavigationEventHandler() {
    return new NavigationEventHandler();
}

