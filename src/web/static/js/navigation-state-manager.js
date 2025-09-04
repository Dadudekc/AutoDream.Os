/**
 * Navigation State Manager - Navigation State Management Module
 * Manages navigation state and active item tracking
 * V2 Compliance: Under 300-line limit achieved
 *
 * @author Agent-3 - Infrastructure & DevOps Specialist
 * @version 1.0.0 - V2 Compliance Navigation State
 * @license MIT
 */

import { getDefaultView, getNavigationElementId, isValidNavigationItem } from './navigation-config-manager.js';

/**
 * Navigation state manager class
 */
export class NavigationStateManager {
    constructor() {
        this.currentView = getDefaultView();
        this.navElement = null;
        this.eventListeners = new Map();
        this.isInitialized = false;
    }

    /**
     * Initialize navigation state manager
     */
    initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Navigation state manager already initialized');
            return;
        }

        this.setupNavigationElement();
        this.isInitialized = true;
        console.log('📊 Navigation state manager initialized');
    }

    /**
     * Setup navigation element reference
     */
    setupNavigationElement() {
        this.navElement = document.getElementById(getNavigationElementId());
        if (!this.navElement) {
            console.warn('⚠️ Navigation element not found');
            return;
        }

        // Add navigation class for styling
        this.navElement.classList.add('dashboard-navigation');
        console.log('📍 Navigation element configured');
    }

    /**
     * Get current navigation state
     */
    getCurrentState() {
        return {
            currentView: this.currentView,
            isInitialized: this.isInitialized,
            navElementFound: !!this.navElement
        };
    }

    /**
     * Update navigation state
     */
    updateNavigationState(newView) {
        if (!isValidNavigationItem(newView)) {
            console.error(`❌ Invalid navigation view: ${newView}`);
            return false;
        }

        const previousView = this.currentView;
        this.currentView = newView;

        // Update active navigation item
        this.updateActiveNavigationItem();

        console.log(`🧭 Navigation state updated from ${previousView} to ${newView}`);
        return true;
    }

    /**
     * Update active navigation item in DOM
     */
    updateActiveNavigationItem() {
        if (!this.navElement) return;

        // Remove active class from all items
        const navLinks = this.navElement.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            link.setAttribute('aria-selected', 'false');
        });

        // Add active class to current view
        const activeLink = this.navElement.querySelector(`[data-view="${this.currentView}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
            activeLink.setAttribute('aria-selected', 'true');
        }
    }

    /**
     * Set navigation state programmatically
     */
    setNavigationState(view) {
        return this.updateNavigationState(view);
    }

    /**
     * Get current view
     */
    getCurrentView() {
        return this.currentView;
    }

    /**
     * Check if navigation is initialized
     */
    isNavigationInitialized() {
        return this.isInitialized;
    }

    /**
     * Reset navigation state
     */
    resetNavigationState() {
        this.currentView = getDefaultView();
        this.updateActiveNavigationItem();
        console.log('🔄 Navigation state reset');
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
     * Handle navigation change event
     */
    handleNavigationChange(newView, previousView) {
        this.emitEvent('navigationChange', {
            newView,
            previousView,
            timestamp: new Date().toISOString()
        });
    }
}

/**
 * Create navigation state manager instance
 */
export function createNavigationStateManager() {
    return new NavigationStateManager();
}

